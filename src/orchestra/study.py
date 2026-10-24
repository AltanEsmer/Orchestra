"""Prepare disclosed review evidence without supplying human decisions."""

import json
import math
import random
from pathlib import Path

from orchestra.data import (
    LABELS,
    M1_REQUIREMENTS,
    file_sha256,
    read_jsonl,
    readiness,
    validate,
    validate_reviews,
)


def _inputs(dataset, sources):
    rows, errors = read_jsonl(dataset)
    manifest = json.loads(Path(sources).read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise TypeError("sources must contain a JSON object")
    errors += validate(rows, manifest)
    if errors:
        raise ValueError("; ".join(errors))
    return rows, manifest


def status(dataset, sources, review):
    """Report machine-checkable M1 readiness, never semantic review completion."""
    blockers = [
        f"missing {kind} file: {path}"
        for kind, path in (
            ("dataset", dataset),
            ("sources", sources),
            ("review", review),
        )
        if not Path(path).is_file()
    ]
    if not blockers:
        try:
            rows, manifest = _inputs(dataset, sources)
            reviews, blockers = read_jsonl(review)
            blockers += validate_reviews(reviews, rows)
            if not blockers:
                blockers += readiness(rows, manifest, reviews, M1_REQUIREMENTS)
        except (OSError, ValueError, TypeError) as error:
            blockers.append(str(error))
    return {
        "ready": not blockers,
        "blockers": blockers,
        "next_action": (
            f"Resolve the first dataset prerequisite: {blockers[0]}"
            if blockers
            else "Verify all ambiguous cases and near-duplicates by human review before freezing the guide and splitting."
        ),
        "human_followup": [
            "Confirm semantic labels, ambiguous-case review and near-duplicate grouping.",
            "Record real permission, disclosed AI checks, human adjudications and guide-freeze evidence.",
        ],
    }


def prepare_review(dataset, sources, out, seed=42, extra_ids=()):
    """Create a blind worksheet and a separate original-label steward snapshot."""
    rows, _ = _inputs(dataset, sources)
    extra_ids = tuple(extra_ids)
    by_id = {row["query_id"]: row for row in rows}
    unknown = set(extra_ids) - by_id.keys()
    if unknown:
        raise ValueError(
            f"ambiguous review IDs missing from dataset: {sorted(unknown)}"
        )
    out = Path(out)
    if out.exists():
        raise FileExistsError(out)
    if any(out.resolve() == Path(p).resolve() for p in (dataset, sources)):
        raise ValueError("review output collides with an input")
    generator = random.Random(seed)
    selected = set(extra_ids)
    labels_by_group = {}
    for row in rows:
        if row["status"] == "accepted":
            labels_by_group.setdefault(row["group_id"], set()).add(row["label"])
    mixed = {group for group, labels in labels_by_group.items() if len(labels) > 1}
    for label in LABELS:
        candidates = sorted(
            row["query_id"]
            for row in rows
            if row["status"] == "accepted" and row["label"] == label
        )
        selected.update(generator.sample(candidates, math.ceil(len(candidates) / 5)))
    selected.update(
        row["query_id"]
        for row in rows
        if row["group_id"] in mixed or row["status"] == "needs_review"
    )
    ids = sorted(selected)
    generator.shuffle(ids)
    worksheet = "".join(
        json.dumps({"query_id": qid, "text": by_id[qid]["text"]}) + "\n" for qid in ids
    )
    snapshot = {
        "version": 1,
        "seed": seed,
        "dataset_sha256": file_sha256(dataset),
        "sources_sha256": file_sha256(sources),
        "sampling": "ceil(20% of accepted rows per class), mixed-label groups, unresolved rows and explicit ambiguous IDs",
        "original_labels": {qid: by_id[qid]["label"] for qid in ids},
        "human_followup": [
            "Keep steward.json hidden until blind human labels or disclosed AI checks have been recorded.",
            "For ai_assisted checks, preserve model and prompt/input/output hashes; the original annotator adjudicates every flag, abstention or disagreement.",
            "Retain original human labels as fallback; never invent human adjudication or treat AI consistency as human agreement.",
            "Unresolved rows need an original human label before a valid review ledger can be completed.",
            "Confirm that all ambiguous and related scenarios were identified; automatic sampling cannot establish that.",
        ],
        "unresolved_ids": [
            qid for qid in ids if by_id[qid]["status"] == "needs_review"
        ],
    }
    out.mkdir(parents=True)
    try:
        (out / "reviewer.jsonl").write_text(worksheet, encoding="utf-8")
        (out / "steward.json").write_text(
            json.dumps(snapshot, indent=2) + "\n", encoding="utf-8"
        )
    except OSError:
        for name in ("reviewer.jsonl", "steward.json"):
            (out / name).unlink(missing_ok=True)
        out.rmdir()
        raise
    return out


def prepare(config_path, review, collection_brief, out_config):
    """Freeze local intake evidence and create a split only after M1 checks pass."""
    config_path = Path(config_path).resolve()
    review, collection_brief = Path(review).resolve(), Path(collection_brief).resolve()
    out_config = Path(out_config).resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise TypeError("study config must be a JSON object")
    path_keys = (
        "dataset",
        "sources",
        "split_manifest",
        "train",
        "validation",
        "sealed_test",
        "results_dir",
        "parent_dataset",
        "parent_manifest",
    )
    for key in path_keys:
        if key in config:
            config[key] = str(Path(config[key]).resolve())
    required = (
        "dataset",
        "sources",
        "split_manifest",
        "train",
        "validation",
        "sealed_test",
        "results_dir",
    )
    missing = [key for key in required if key not in config]
    if missing:
        raise ValueError(f"study config is missing paths: {', '.join(missing)}")
    inputs = {
        config_path,
        review,
        collection_brief,
        Path(config["dataset"]),
        Path(config["sources"]),
    }
    if "parent_dataset" in config:
        inputs.add(Path(config["parent_dataset"]))
    if "parent_manifest" in config:
        inputs.add(Path(config["parent_manifest"]))
    outputs = [out_config] + [
        Path(config[key])
        for key in ("split_manifest", "train", "validation", "sealed_test")
    ]
    if len(set(outputs)) != len(outputs) or any(path in inputs for path in outputs):
        raise ValueError("study output aliases another output or an input")
    if any(
        a in b.parents or b in a.parents
        for a in outputs
        for b in inputs | set(outputs)
        if a != b
    ):
        raise ValueError(
            "study output file paths must not contain other inputs or outputs"
        )
    if Path(config["results_dir"]) in inputs | set(outputs):
        raise ValueError("results directory aliases a study file")
    sealed = Path(config["sealed_test"])
    if any(
        Path(config[key]).parent in sealed.parents for key in ("train", "validation")
    ):
        raise ValueError(
            "sealed test must not sit in the train or validation directory"
        )
    readiness_status = status(config["dataset"], config["sources"], review)
    if not readiness_status["ready"]:
        raise ValueError(
            "study is not ready: " + "; ".join(readiness_status["blockers"])
        )
    if not collection_brief.read_text(encoding="utf-8").strip():
        raise ValueError("collection brief must be nonempty before splitting")
    config["review"] = str(review)
    config["review_sha256"] = file_sha256(review)
    config["collection_brief"] = str(collection_brief)
    config["collection_brief_sha256"] = file_sha256(collection_brief)
    config["study_evidence"] = {
        "format_version": 1,
        "ready": True,
        "dataset_sha256": file_sha256(config["dataset"]),
        "sources_sha256": file_sha256(config["sources"]),
        "review_sha256": file_sha256(review),
        "collection_brief_sha256": file_sha256(collection_brief),
    }
    if "parent_manifest" in config:
        parent = Path(config["parent_manifest"])
        if not parent.is_file():
            raise ValueError(
                "parent manifest is missing; complete the baseline split first"
            )
        actual = file_sha256(parent)
        supplied = config.get("parent_manifest_sha256")
        if supplied is not None and supplied != actual:
            raise ValueError(
                "parent_manifest_sha256 differs from the actual parent manifest"
            )
        config["parent_manifest_sha256"] = actual
    text = json.dumps(config, indent=2) + "\n"
    if out_config.exists():
        if out_config.read_text(encoding="utf-8") != text:
            raise ValueError(
                "prepared config exists and differs; configs are immutable"
            )
    else:
        out_config.parent.mkdir(parents=True, exist_ok=True)
        with out_config.open("x", encoding="utf-8") as file:
            file.write(text)
    from orchestra.__main__ import main

    command = "extend" if "parent_manifest" in config else "split"
    if main([command, "--config", str(out_config)]) != 0:
        raise ValueError(
            f"prepared config saved, but {command} failed; inspect its reported errors"
        )
    return out_config
