"""Training-only confidence analysis and a single frozen held-out evaluation."""

import contextlib
import fcntl
import json
import os
import warnings
from pathlib import Path

import numpy as np
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import StratifiedGroupKFold

from orchestra import experiment as ex
from orchestra import jev
from orchestra.data import LABELS, file_sha256
from orchestra.splits import check_materialized

RECEIPT_STORE = Path(__file__).resolve().parents[2] / "results" / "test-receipts"
ERROR_CATEGORIES = {
    "annotation_ambiguity",
    "missing_context",
    "vocabulary_mismatch",
    "negation",
    "multi_action_dependencies",
    "out_of_scope",
    "other",
}


def _research_evidence(config, manifest):
    evidence = config.get("study_evidence")
    if not isinstance(evidence, dict) or evidence.get("ready") is not True:
        raise ValueError("research confidence requires prepared study evidence")
    hashes = {}
    for key, evidence_key in (
        ("sources", "sources_sha256"),
        ("review", "review_sha256"),
        ("collection_brief", "collection_brief_sha256"),
    ):
        if not config.get(key) or not evidence.get(evidence_key):
            raise ValueError(f"study evidence missing {key}")
        hashes[str(Path(config[key]).resolve())] = evidence[evidence_key]
    _verify_hashes(hashes)
    if evidence.get("dataset_sha256") != manifest["dataset_sha256"]:
        raise ValueError("study evidence dataset differs from split")
    sources = _json(config["sources"])
    if (
        not isinstance(sources, dict)
        or not sources
        or any(
            not isinstance(source, dict)
            or not isinstance(source.get("license"), str)
            or not source["license"].strip()
            for source in sources.values()
        )
    ):
        raise ValueError("study evidence source permissions missing")
    if not Path(config["collection_brief"]).read_text(encoding="utf-8").strip():
        raise ValueError("study collection brief is empty")
    return hashes


def _error_interpretations(path, run, systems):
    if path is None:
        raise ValueError("research freeze requires validation error interpretations")
    from orchestra.data import read_jsonl

    rows, errors = read_jsonl(path)
    if errors:
        raise ValueError("; ".join(errors))
    selected = {entry["id"] for entry in systems}
    facts = {
        (r["configuration"], r["query_id"]): r
        for r in run["predictions.jsonl"]
        if r["configuration"] in selected
    }
    wrong = {key for key, fact in facts.items() if fact["label"] != fact["prediction"]}
    seen, reviewed_wrong, reviewed_correct = set(), set(), set()
    for row in rows:
        key = (row.get("configuration"), row.get("query_id"))
        if key not in facts or key in seen:
            raise ValueError(
                "error interpretation has unknown or duplicate configuration/query"
            )
        seen.add(key)
        if (
            row.get("category") not in ERROR_CATEGORIES
            or not isinstance(row.get("hypothesis"), str)
            or not row["hypothesis"].strip()
        ):
            raise ValueError(
                "error interpretation needs allowed category and nonempty hypothesis"
            )
        (reviewed_wrong if key in wrong else reviewed_correct).add(key)
    if len(reviewed_wrong) < min(20, len(wrong)) or (
        len(facts) > len(wrong) and not reviewed_correct
    ):
        raise ValueError(
            "interpret at least min(20, all errors) and a correct comparison"
        )
    return {str(Path(path).resolve()): file_sha256(path)}


def review_test(final_dir, path):
    from orchestra.data import read_jsonl

    final_dir = Path(final_dir)
    load_artifacts(final_dir)
    predictions, problems = read_jsonl(final_dir / "predictions.jsonl")
    ledger, ledger_problems = read_jsonl(path)
    if problems or ledger_problems:
        raise ValueError("; ".join(problems + ledger_problems))
    if not ledger:
        raise ValueError("test interpretation ledger is empty")
    systems = [{"id": c} for c in {row.get("configuration") for row in ledger}]
    _error_interpretations(path, {"predictions.jsonl": predictions}, systems)
    facts = {(p["configuration"], p["query_id"]): p for p in predictions}
    summary = {
        entry["id"]: {
            "errors": sum(
                p["configuration"] == entry["id"] and p["label"] != p["prediction"]
                for p in predictions
            ),
            "interpreted": 0,
            "correct": 0,
            "categories": {},
        }
        for entry in systems
    }
    for row in ledger:
        fact = facts[(row["configuration"], row["query_id"])]
        entry = summary[row["configuration"]]
        if fact["label"] == fact["prediction"]:
            entry["correct"] += 1
        else:
            entry["interpreted"] += 1
            categories = entry["categories"]
            categories[row["category"]] = categories.get(row["category"], 0) + 1
    return summary


def _json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _probabilities(labels, probabilities):
    values = np.asarray(probabilities, dtype=float)
    if not labels or any(label not in LABELS for label in labels):
        raise ValueError("probabilities require nonempty known labels")
    if (
        values.shape != (len(labels), len(LABELS))
        or not np.isfinite(values).all()
        or (values < 0).any()
        or (values > 1).any()
        # XGBoost's float32 probabilities miss 1 by about 1e-7.
        or not np.allclose(values.sum(axis=1), 1, atol=jev.SUM_TOLERANCE, rtol=0)
    ):
        raise ValueError("probabilities must be finite normalized Nx4 in LABELS order")
    return values


def probability_metrics(labels, probabilities, predictions=None):
    values = _probabilities(labels, probabilities)
    truth = np.array([LABELS.index(label) for label in labels])
    onehot = np.eye(len(LABELS))[truth]
    confidence = values.max(axis=1)
    if predictions is None:
        predictions = [LABELS[i] for i in values.argmax(axis=1)]
    if len(predictions) != len(labels) or any(p not in LABELS for p in predictions):
        raise ValueError("predictions must match probability rows")
    correct = np.array([p == y for p, y in zip(predictions, labels)])
    bins = []
    for i in range(5):
        selected = (confidence >= i / 5) & (
            (confidence < (i + 1) / 5) if i < 4 else (confidence <= 1)
        )
        count = int(selected.sum())
        bins.append(
            {
                "lower": i / 5,
                "upper": (i + 1) / 5,
                "count": count,
                "mean_confidence": float(confidence[selected].mean())
                if count
                else None,
                "accuracy": float(correct[selected].mean()) if count else None,
            }
        )
    return {
        "log_loss": float(
            -np.log(
                np.clip(values[np.arange(len(labels)), truth], np.finfo(float).eps, 1)
            ).mean()
        ),
        "brier": float(((values - onehot) ** 2).sum(axis=1).mean()),
        "ece": sum(
            b["count"] / len(labels) * abs(b["accuracy"] - b["mean_confidence"])
            for b in bins
            if b["count"]
        ),
        "bins": bins,
    }


def _threshold_rows(labels, predictions, probabilities, thresholds):
    values = _probabilities(labels, probabilities)
    if len(predictions) != len(labels) or any(p not in LABELS for p in predictions):
        raise ValueError("predictions must match labels")
    rows = []
    for threshold in thresholds:
        accepted = values.max(axis=1) >= threshold
        count = int(accepted.sum())
        correct = sum(
            bool(a) and p == y for a, p, y in zip(accepted, predictions, labels)
        )
        rows.append(
            {
                "threshold": threshold,
                "accepted": count,
                "total": len(labels),
                "coverage": count / len(labels),
                "correct_accepted": correct,
                "selective_accuracy": correct / count if count else None,
                "per_true_class_coverage": {
                    label: sum(bool(a) for a, y in zip(accepted, labels) if y == label)
                    / labels.count(label)
                    if label in labels
                    else None
                    for label in LABELS
                },
            }
        )
    return rows


def threshold_table(labels, predictions, probabilities):
    rows = _threshold_rows(
        labels, predictions, probabilities, (0.0, 0.5, 0.6, 0.7, 0.8, 0.9)
    )
    qualified = [r for r in rows if r["accepted"] and r["selective_accuracy"] >= 0.9]
    chosen = (
        min(qualified, key=lambda r: (-r["coverage"], r["threshold"]))
        if qualified
        else None
    )
    return {
        "rows": rows,
        "chosen": chosen["threshold"] if chosen else None,
        "status": "qualified" if chosen else "no_qualifying_threshold",
    }


def calibration_folds(rows):
    labels = [r["label"] for r in rows]
    groups = [r["group_id"] for r in rows]
    folds = list(
        StratifiedGroupKFold(n_splits=3, shuffle=True, random_state=42).split(
            np.zeros(len(rows)), labels, groups
        )
    )
    for fit, held in folds:
        if any({labels[i] for i in indices} != set(LABELS) for indices in (fit, held)):
            raise ValueError(
                "calibration shortage: every training fold side needs all classes"
            )
        if {groups[i] for i in fit} & {groups[i] for i in held}:
            raise ValueError("calibration group overlap")
    return folds


def _identity():
    root = Path(__file__).resolve().parents[2]
    paths = [root / "uv.lock", *sorted((root / "src/orchestra").glob("*.py"))]
    return {str(p): file_sha256(p) for p in paths}


def _verify_hashes(hashes):
    for path, digest in hashes.items():
        if file_sha256(path) != digest:
            raise ValueError(f"frozen input changed: {path}")


def _seal(out, names):
    ex.write_json(
        out / "manifest.json",
        {"complete": True, "files": {name: file_sha256(out / name) for name in names}},
    )


def load_artifacts(directory):
    directory = Path(directory)
    manifest = _json(directory / "manifest.json")
    if manifest.get("complete") is not True or not manifest.get("files"):
        raise ValueError("incomplete confidence/final artifacts")
    for name, digest in manifest["files"].items():
        if Path(name).name != name or file_sha256(directory / name) != digest:
            raise ValueError(f"artifact hash mismatch: {name}")
    return {
        name: _json(directory / name)
        for name in manifest["files"]
        if name.endswith(".json")
    }


def _context(run_dir, selection_path):
    run, problems = ex.load_run(run_dir)
    if problems:
        raise ValueError("; ".join(problems))
    expected = ex.select(run_dir)
    selection = _json(selection_path)
    if not expected["valid"] or {**selection, "run": None} != {**expected, "run": None}:
        raise ValueError("selection does not match verified M3 run")
    provenance = run["provenance.json"]
    environment = [
        ("sklearn", ex.sklearn.__version__),
        ("numpy", ex.numpy.__version__),
        ("scipy", ex.scipy.__version__),
        (
            "uv_lock_sha256",
            file_sha256(Path(__file__).resolve().parents[2] / "uv.lock"),
        ),
    ]
    matrix = run["config.json"]["config"].get("matrix", "m3")
    if matrix != "m3" or "xgboost" in provenance:  # M3 runs predate XGBoost
        environment.append(("xgboost", ex.xgboost.__version__))
    for key, actual in environment:
        if provenance.get(key) != actual:
            raise ValueError(f"M3 environment mismatch: {key}")
    config = run["config.json"]["config"]
    train, validation = [ex.load_rows(config[k], k) for k in ("train", "validation")]
    manifest = ex.check_inputs(config, train, validation)
    for key in ("train", "validation", "split_manifest"):
        if file_sha256(config[key]) != run["provenance.json"][key + "_sha256"]:
            raise ValueError(f"{key} changed since M3")
    systems = []
    for chosen in selection["families"].values():
        cid = chosen["chosen"]
        entry = next(e for e in run["config.json"]["configurations"] if e["id"] == cid)
        outcome = next(o for o in run["outcomes.json"] if o["id"] == cid)
        systems.append(
            {
                **entry,
                "max_iter": outcome["attempts"][-1]["max_iter"],
                "resolved_params": run["config.json"]["resolved_params"][cid],
            }
        )
    logistic = [e for e in systems if e["family"].startswith("L")]
    best = max(selection["configurations"][e["id"]]["macro_f1"] for e in logistic)
    logistic = next(
        e
        for e in logistic
        if ex.within_tolerance(selection["configurations"][e["id"]]["macro_f1"], best)
    )
    return run, config, train, validation, manifest, systems, logistic


def _fit(entry, train, rows):
    result = ex.fit_predict(entry, train, rows, entry["max_iter"])
    if ex.estimator_params(result["pipeline"]) != entry["resolved_params"]:
        raise ValueError("resolved estimator settings changed")
    if not result["converged"]:
        raise ValueError("frozen model did not converge")
    return result


def _calibrate(entry, train, rows, folds):
    model = CalibratedClassifierCV(
        ex.FAMILIES[entry["family"]]["build"](entry, entry["max_iter"]),
        method="sigmoid",
        cv=folds,
        ensemble=True,
        n_jobs=1,
    )
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        model.fit([r["text"] for r in train], [r["label"] for r in train])
    return {
        "pipeline": model,
        "predictions": [str(p) for p in model.predict([r["text"] for r in rows])],
        "scores": ex.score(model, [r["text"] for r in rows], "probability"),
        "warnings": [
            {"category": w.category.__name__, "message": str(w.message)} for w in caught
        ],
    }


def _save_predictions(out, results, rows):
    predictions, review = [], []
    for cid, result in results.items():
        for row, predicted, scores in zip(
            rows, result["predictions"], result["scores"]
        ):
            fact = {
                "configuration": cid,
                "query_id": row["query_id"],
                "group_id": row["group_id"],
                "label": row["label"],
                "prediction": predicted,
                "scores": scores,
                "score_type": result["score_type"],
            }
            predictions.append(fact)
            review.append(
                {
                    **fact,
                    "text": row["text"],
                    "correct": predicted == row["label"],
                    "category": None,
                    "hypothesis": None,
                    "reviewer": None,
                }
            )
    for name, records in (
        ("predictions.jsonl", predictions),
        ("error-review.jsonl", review),
    ):
        (out / name).write_text(
            "".join(json.dumps(r) + "\n" for r in records), encoding="utf-8"
        )


def analyze(run_dir, selection_path, out_dir, fixture=False):
    started = ex.now()
    run_dir, selection_path, out = (
        Path(run_dir).resolve(),
        Path(selection_path).resolve(),
        Path(out_dir).resolve(),
    )
    run, config, train, validation, manifest, systems, logistic = _context(
        run_dir, selection_path
    )
    evidence_hashes = {} if fixture else _research_evidence(config, manifest)
    labels = [r["label"] for r in validation]
    results, declared = {}, {}
    for entry in systems:
        result = _fit(entry, train, validation)
        recorded = [
            p for p in run["predictions.jsonl"] if p["configuration"] == entry["id"]
        ]
        if (
            [r["query_id"] for r in validation] != [p["query_id"] for p in recorded]
            or result["predictions"] != [p["prediction"] for p in recorded]
            or not np.allclose(
                result["scores"], [p["scores"] for p in recorded], atol=1e-10, rtol=0
            )
        ):
            raise ValueError(f"raw validation reproduction mismatch: {entry['id']}")
        if entry == logistic:
            results["raw"] = {**result, "score_type": "probability"}
        # Declared before freezing: only the chosen logistic system is recalibrated.
        # Jev and the tree families keep their own probabilities; margins get none.
        score_type = ex.FAMILIES[entry["family"]]["score"]
        declared[entry["id"]] = {
            "family": entry["family"],
            "score_type": score_type,
            "calibration": "sigmoid, three grouped training folds"
            if entry == logistic
            else "none",
            "metrics": {
                **ex.metrics(labels, result["predictions"]),
                **(
                    probability_metrics(labels, result["scores"], result["predictions"])
                    if score_type == "probability"
                    else {}
                ),
            },
        }
    outcome = {"status": "ok", "warnings": []}
    folds, fold_records = [], []
    try:
        folds = calibration_folds(train)
        fold_records = [
            {
                "fit_ids": [train[i]["query_id"] for i in fit],
                "held_ids": [train[i]["query_id"] for i in held],
                "fit_groups": sorted({train[i]["group_id"] for i in fit}),
                "held_groups": sorted({train[i]["group_id"] for i in held}),
            }
            for fit, held in folds
        ]
        calibrated = _calibrate(logistic, train, validation, folds)
        results["calibrated"] = {**calibrated, "score_type": "probability"}
        outcome["warnings"] = calibrated["warnings"]
        if any(w["category"] == "ConvergenceWarning" for w in calibrated["warnings"]):
            outcome["status"] = "unresolved_warning"
    except ValueError as error:
        outcome = {"status": "shortage", "error": str(error), "warnings": []}
    measured = {
        key: {
            **ex.metrics(labels, r["predictions"]),
            **probability_metrics(labels, r["scores"], r["predictions"]),
        }
        for key, r in results.items()
    }
    thresholds = (
        threshold_table(
            labels,
            results["calibrated"]["predictions"],
            results["calibrated"]["scores"],
        )
        if "calibrated" in results
        else {"rows": [], "chosen": None, "status": "calibration_unavailable"}
    )
    hashes = {
        str(Path(config[k]).resolve()): file_sha256(config[k])
        for k in ("train", "validation", "split_manifest")
    }
    hashes.update(evidence_hashes)
    hashes.update(
        {
            str(run_dir / "manifest.json"): file_sha256(run_dir / "manifest.json"),
            str(selection_path): file_sha256(selection_path),
        }
    )
    out.mkdir(parents=True)
    payloads = {
        "config.json": {
            "format_version": 1,
            "fixture": bool(fixture),
            "fixture_receipt_store": str(out.parent / "fixture-test-receipts")
            if fixture
            else None,
            "run": str(run_dir),
            "selection": str(selection_path),
            "inputs": config,
            "systems": systems,
            "logistic": logistic,
            "class_order": list(LABELS),
            "hashes": hashes,
            "code_hashes": _identity(),
            "calibration": {
                "method": "sigmoid",
                "folds": 3,
                "seed": 42,
                "ensemble": True,
            },
        },
        "provenance.json": ex.provenance(config, manifest, started, train + validation),
        "outcomes.json": outcome,
        "metrics.json": measured,
        "reliability.json": {key: value["bins"] for key, value in measured.items()},
        "systems.json": declared,
        "thresholds.json": thresholds,
        "calibration-folds.json": fold_records,
    }
    for name, value in payloads.items():
        ex.write_json(out / name, value)
    _save_predictions(out, results, validation)
    _seal(out, [*payloads, "predictions.jsonl", "error-review.jsonl"])
    return out


def _jev_test_log(systems, path):
    """The frozen path for Jev's test answers, required exactly when Jev is chosen."""
    if not any(entry["family"] == "Jev" for entry in systems):
        if path is not None:
            raise ValueError("no Jev system in the decision set; omit the Jev test log")
        return None
    if path is None:
        raise ValueError("the decision set includes Jev: freeze needs a Jev test log")
    path = Path(path).resolve()
    if jev.log_is_unsafe(path):
        raise ValueError(f"{path} is inside the repository and not ignored by Git")
    if not path.parent.is_dir():
        raise ValueError(f"Jev test log {path} has no folder; create it first")
    return path


def _log_digest(path):
    return file_sha256(path) if path.exists() else None


def freeze(confidence_dir, out_path, error_review=None, jev_test_log=None):
    directory, out = Path(confidence_dir).resolve(), Path(out_path)
    artifacts = load_artifacts(directory)
    config = artifacts["config.json"]
    _verify_hashes(config["hashes"])
    _verify_hashes(config["code_hashes"])
    run, inputs, _, _, manifest, systems, _ = _context(
        config["run"], config["selection"]
    )
    if not config["fixture"]:
        _research_evidence(inputs, manifest)
    review_hashes = (
        _error_interpretations(error_review, run, systems)
        if not config["fixture"]
        else {}
    )
    if artifacts["outcomes.json"]["status"] != "ok":
        raise ValueError("calibration shortage or unresolved warning blocks freeze")
    jev_test_log = _jev_test_log(systems, jev_test_log)
    frozen = {
        "format_version": 1,
        "fixture": config["fixture"],
        "error_review_hashes": review_hashes,
        "confidence_dir": str(directory),
        "confidence_manifest_sha256": file_sha256(directory / "manifest.json"),
        "config": config,
        "folds": artifacts["calibration-folds.json"],
        "fallback": artifacts["thresholds.json"],
        "jev_test_log": str(jev_test_log) if jev_test_log else None,
    }
    if out.exists():
        existing = _json(out)
        frozen["frozen_utc"] = existing.get("frozen_utc")
        frozen["git_sha"] = existing.get("git_sha")
        if existing != frozen:
            raise ValueError("refuse changed freeze")
    else:
        # Test answers may only come from final-test, inside its reservation.
        if jev_test_log is not None and jev_test_log.exists():
            raise ValueError(f"Jev test log {jev_test_log} already exists")
        frozen["frozen_utc"] = ex.now()
        frozen["git_sha"] = ex.git("rev-parse", "HEAD")
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("x", encoding="utf-8") as file:
            file.write(json.dumps(frozen, indent=2) + "\n")
    return frozen


def final_test(freeze_path, out_dir, resume=False, jev_send=None, jev_replay=False):
    started = ex.now()
    frozen = _json(freeze_path)
    config = frozen["config"]
    directory = Path(frozen["confidence_dir"])
    if file_sha256(directory / "manifest.json") != frozen["confidence_manifest_sha256"]:
        raise ValueError("confidence manifest changed")
    artifacts = load_artifacts(directory)
    if (
        config != artifacts["config.json"]
        or frozen["folds"] != artifacts["calibration-folds.json"]
        or frozen["fallback"] != artifacts["thresholds.json"]
    ):
        raise ValueError("freeze decisions changed")
    _verify_hashes(config["hashes"])
    _verify_hashes(config["code_hashes"])
    _verify_hashes(frozen["error_review_hashes"])
    _, inputs, train, _, manifest, systems, logistic = _context(
        config["run"], config["selection"]
    )
    if (
        systems != config["systems"]
        or logistic != config["logistic"]
        or artifacts["outcomes.json"]["status"] != "ok"
    ):
        raise ValueError("frozen systems changed")
    jev_log = _jev_test_log(systems, frozen.get("jev_test_log"))
    if jev_send is not None and jev_replay:
        raise ValueError("a replay sends nothing; omit --send-jev-test")
    if jev_log is None and (jev_send is not None or jev_replay):
        raise ValueError("no Jev system in the decision set; omit the Jev test option")
    if jev_log is not None and jev_send is None and not jev_replay:
        raise ValueError(
            "the decision set includes Jev: final-test needs --send-jev-test "
            "and TYPESAFE_API_KEY, which send the test queries to TypeSafe, "
            "or --replay-jev-test with an archived log at the frozen path"
        )
    split_digest = file_sha256(inputs["split_manifest"])
    store = (
        Path(config["fixture_receipt_store"]) if config["fixture"] else RECEIPT_STORE
    )
    with _final_lock(store, split_digest):
        return _evaluate_frozen(
            freeze_path,
            out_dir,
            resume,
            started,
            frozen,
            inputs,
            train,
            manifest,
            systems,
            logistic,
            split_digest,
            store,
            jev_log,
            jev_send,
            jev_replay,
        )


@contextlib.contextmanager
def _final_lock(store, split_digest):
    store.mkdir(parents=True, exist_ok=True)
    with (store / f"{split_digest}.lock").open("a", encoding="utf-8") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise ValueError(
                "an active final evaluation already holds this split"
            ) from error
        try:
            yield
        finally:
            fcntl.flock(lock.fileno(), fcntl.LOCK_UN)


def _write_receipt(path, value):
    temporary = path.with_suffix(".pending")
    ex.write_json(temporary, value)
    os.replace(temporary, path)


def _evaluate_frozen(
    freeze_path,
    out_dir,
    resume,
    started,
    frozen,
    inputs,
    train,
    manifest,
    systems,
    logistic,
    split_digest,
    store,
    jev_log,
    jev_send,
    jev_replay,
):
    config = frozen["config"]
    receipt_path = store / f"{split_digest}.json"
    out = Path(out_dir).resolve()
    request = {
        "freeze_sha256": file_sha256(freeze_path),
        "out": str(out),
        "split_sha256": split_digest,
        "fixture": config["fixture"],
    }
    if jev_replay:
        # Receipts written before replays existed lack this key; a resume
        # may not switch between replaying and sending.
        request["jev_replay"] = True
    history = []
    if receipt_path.exists():
        receipt = _json(receipt_path)
        if any(receipt.get(k) != request.get(k) for k in {*request, "jev_replay"}):
            raise ValueError(
                "split test already reserved/opened; changed evaluation refused"
            )
        if receipt.get("status") == "complete":
            load_artifacts(out)
            if file_sha256(out / "manifest.json") != receipt["result_manifest_sha256"]:
                raise ValueError("final result manifest changed")
            return out
        if not resume or receipt.get("status") not in {
            "failed_after_reservation",
            "opened",
            "reserved",
        }:
            raise ValueError(
                "split test has incomplete reservation; use identical --resume"
            )
        history = receipt.get("attempts", [])
        # A killed process records no digest; otherwise the log must be exactly
        # as the last attempt left it, so no answer is added between attempts.
        if (
            jev_log is not None
            and history
            and "jev_test_log_sha256" in history[-1]
            and _log_digest(jev_log) != history[-1]["jev_test_log_sha256"]
        ):
            raise ValueError("Jev test log changed since the last attempt")
        if out.exists():
            partial = out.with_name(out.name + f".failed-attempt-{len(history)}")
            if partial.exists():
                raise ValueError("failed attempt preservation path already exists")
            out.rename(partial)
    elif out.exists():
        raise ValueError("final output already exists; choose an unused path")
    elif jev_log is not None and jev_log.exists() != jev_replay:
        raise ValueError(
            f"replay needs the archived Jev test log at {jev_log}"
            if jev_replay
            else f"Jev test log {jev_log} exists before the test was reserved"
        )
    out.parent.mkdir(parents=True, exist_ok=True)
    if not receipt_path.exists():
        _write_receipt(receipt_path, {**request, "status": "reserved", "attempts": []})
    attempt = {"started_utc": started}
    try:
        out.mkdir()
        attempt["opened_utc"] = ex.now()
        _write_receipt(
            receipt_path,
            {**request, "status": "opened", "attempts": history + [attempt]},
        )
        test = ex.load_rows(inputs["sealed_test"], "test")
        errors = check_materialized(manifest, {"test": test})
        if errors:
            raise ValueError("; ".join(errors))
        folds = calibration_folds(train)
        actual_folds = [
            {
                "fit_ids": [train[i]["query_id"] for i in fit],
                "held_ids": [train[i]["query_id"] for i in held],
                "fit_groups": sorted({train[i]["group_id"] for i in fit}),
                "held_groups": sorted({train[i]["group_id"] for i in held}),
            }
            for fit, held in folds
        ]
        if actual_folds != frozen["folds"]:
            raise ValueError("frozen calibration folds changed")
        jev_record = {
            "jev_test_log_sha256": None,
            "jev_test_requests": None,
            "jev_test_replayed": jev_replay,
        }
        if jev_log is not None:
            # Each attempt sends every unanswered test query at most once;
            # a replay of an archived log may send none.
            budget = 0 if jev_replay else len(test)
            summary = jev.collect(test, jev_log, budget, jev_send)
            if summary["missing"]:
                raise ValueError(
                    f"{len(summary['missing'])} test queries have no valid Jev "
                    + (
                        "answer in the archived log"
                        if jev_replay
                        else "answer; rerun the identical command with --resume"
                    )
                )
            jev_record |= {
                "jev_test_log_sha256": file_sha256(jev_log),
                # Every request of every attempt is one log line.
                "jev_test_requests": len(jev.read_log(jev_log)),
            }
        results = {}
        for entry in systems:
            if entry["family"] == "Jev":
                # The frozen entry replays validation answers; the test replays
                # the answers collected above, under the same pinned prompt.
                result = ex.fit_predict(
                    {
                        **entry,
                        "responses": str(jev_log),
                        "responses_sha256": jev_record["jev_test_log_sha256"],
                    },
                    train,
                    test,
                )
            else:
                result = _fit(entry, train, test)
            results[entry["id"]] = {
                **result,
                "score_type": ex.FAMILIES[entry["family"]]["score"],
            }
        calibrated = _calibrate(logistic, train, test, folds)
        if any(w["category"] == "ConvergenceWarning" for w in calibrated["warnings"]):
            raise ValueError("frozen calibrated model did not converge")
        results["calibrated"] = {**calibrated, "score_type": "probability"}
        labels = [r["label"] for r in test]
        measured = {
            cid: {
                **ex.metrics(labels, r["predictions"]),
                **(
                    probability_metrics(labels, r["scores"], r["predictions"])
                    if r["score_type"] == "probability"
                    else {}
                ),
            }
            for cid, r in results.items()
        }
        threshold = frozen["fallback"]["chosen"]
        policy = (
            _threshold_rows(
                labels, calibrated["predictions"], calibrated["scores"], [threshold]
            )[0]
            if threshold is not None
            else None
        )
        payloads = {
            "config.json": frozen,
            "provenance.json": {
                **request,
                "started_utc": started,
                "opened_utc": attempt["opened_utc"],
                "test_sha256": file_sha256(inputs["sealed_test"]),
                **jev_record,
                "completed_utc": ex.now(),
            },
            "metrics.json": measured,
            "confusion.json": {
                cid: ex.confusion(labels, r["predictions"])
                for cid, r in results.items()
            },
            "reliability.json": {
                cid: m["bins"] for cid, m in measured.items() if "bins" in m
            },
            "thresholds.json": {"frozen_threshold": threshold, "evaluation": policy},
            "warnings.json": calibrated["warnings"],
        }
        for name, value in payloads.items():
            ex.write_json(out / name, value)
        _save_predictions(out, results, test)
        _seal(out, [*payloads, "predictions.jsonl", "error-review.jsonl"])
        if jev_log is not None:
            attempt["jev_test_log_sha256"] = _log_digest(jev_log)
        _write_receipt(
            receipt_path,
            {
                **request,
                "status": "complete",
                "attempts": history + [{**attempt, "completed_utc": ex.now()}],
                "result_manifest_sha256": file_sha256(out / "manifest.json"),
            },
        )
        return out
    except BaseException as error:
        if jev_log is not None:
            attempt["jev_test_log_sha256"] = _log_digest(jev_log)
        _write_receipt(
            receipt_path,
            {
                **request,
                "status": "failed_after_reservation",
                "attempts": history
                + [
                    {
                        **attempt,
                        "failed_utc": ex.now(),
                        "error": f"{type(error).__name__}: {error}",
                    }
                ],
                "error": f"{type(error).__name__}: {error}",
            },
        )
        raise
