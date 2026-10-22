import hashlib
import json
from collections import Counter
from pathlib import Path

import sklearn
from sklearn.model_selection import StratifiedGroupKFold

from orchestra.data import LABELS

MANIFEST_VERSION = 1
N_SPLITS = 5
PARTITIONS = ("train", "validation", "test")
# Held-out fold -> partition. Each fold's own test indices, never the overlapping training indices.
FOLD_PARTITION = {0: "train", 1: "train", 2: "train", 3: "validation", 4: "test"}
MANIFEST_KEYS = (
    "manifest_version",
    "dataset_sha256",
    "seed",
    "algorithm",
    "n_splits",
    "fold_partition",
    "sklearn_version",
    "class_order",
    "partitions",
    "groups",
    "row_sha256",
    "counts",
    "proportions",
)


def _counts(rows_by_id, ids):
    labels = Counter(rows_by_id[query_id]["label"] for query_id in ids)
    return {label: labels[label] for label in LABELS}


def row_hash(row):
    """Hash of the content that must never change once a row is frozen."""
    content = {k: row[k] for k in ("text", "label", "group_id")}
    text = json.dumps(
        content, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    )
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _accepted(rows):
    review = sorted(r["query_id"] for r in rows if r.get("status") == "needs_review")
    if review:
        raise ValueError(f"unresolved needs_review rows: {', '.join(review)}")
    return sorted(
        (r for r in rows if r.get("status") == "accepted"), key=lambda r: r["query_id"]
    )


def _allocate(accepted, seed, noun="groups"):
    """Assign sorted accepted rows to partitions; shared by make_split and extend_split."""
    for label in LABELS:
        groups = {r["group_id"] for r in accepted if r["label"] == label}
        if len(groups) < N_SPLITS:
            raise ValueError(
                f"class {label} has {len(groups)} {noun}; "
                f"need at least {N_SPLITS} for {N_SPLITS} folds"
            )

    folds = StratifiedGroupKFold(n_splits=N_SPLITS, shuffle=True, random_state=seed)
    labels = [r["label"] for r in accepted]
    groups = [r["group_id"] for r in accepted]
    partitions = {name: [] for name in PARTITIONS}
    for fold, (_, held_out) in enumerate(folds.split(labels, labels, groups)):
        partitions[FOLD_PARTITION[fold]] += [accepted[i]["query_id"] for i in held_out]
    partitions = {name: sorted(ids) for name, ids in partitions.items()}

    rows_by_id = {r["query_id"]: r for r in accepted}
    for name, ids in partitions.items():
        by_label = _counts(rows_by_id, ids)
        absent = [label for label in LABELS if by_label[label] == 0]
        if absent:
            raise ValueError(
                f"partition {name} has no rows for class {', '.join(absent)}; "
                "collect more groups instead of searching seeds"
            )
    return partitions


def _manifest(dataset_sha256, seed, partitions, accepted):
    rows_by_id = {r["query_id"]: r for r in accepted}
    return {
        "manifest_version": MANIFEST_VERSION,
        "dataset_sha256": dataset_sha256,
        "seed": seed,
        "algorithm": "StratifiedGroupKFold",
        "n_splits": N_SPLITS,
        "fold_partition": {str(k): v for k, v in FOLD_PARTITION.items()},
        "sklearn_version": sklearn.__version__,
        "class_order": list(LABELS),
        "partitions": partitions,
        "groups": {q: r["group_id"] for q, r in rows_by_id.items()},
        "row_sha256": {q: row_hash(r) for q, r in rows_by_id.items()},
        "counts": {name: _counts(rows_by_id, ids) for name, ids in partitions.items()},
        "proportions": {
            name: round(len(ids) / len(accepted), 4) for name, ids in partitions.items()
        },
    }


def make_split(rows, dataset_sha256, seed=42):
    accepted = _accepted(rows)
    partitions = _allocate(accepted, seed)
    return _manifest(dataset_sha256, seed, partitions, accepted)


def extend_split(
    parent_manifest,
    parent_rows,
    rows,
    parent_dataset_sha256,
    parent_manifest_sha256,
    dataset_sha256,
    seed,
):
    """Child manifest: parent memberships frozen, new independent groups allocated."""
    problems = check_split(parent_manifest, parent_rows, parent_dataset_sha256)
    if problems:
        raise ValueError(f"parent manifest is invalid: {problems[0]}")
    accepted = _accepted(rows)
    by_id = {r["query_id"]: r for r in accepted}
    where = {q: n for n, ids in parent_manifest["partitions"].items() for q in ids}
    for query_id in sorted(where):
        if query_id not in by_id:
            raise ValueError(f"{query_id}: parent row is missing from the extension")
        if row_hash(by_id[query_id]) != parent_manifest["row_sha256"][query_id]:
            raise ValueError(
                f"{query_id}: text, label or group_id differs from the parent; "
                "record the correction and build a named successor protocol "
                "instead of overwriting"
            )
    parent_groups = set(parent_manifest["groups"].values())
    new = [r for r in accepted if r["query_id"] not in where]
    for row in new:
        if row["group_id"] in parent_groups:
            raise ValueError(
                f"{row['query_id']}: group {row['group_id']} already exists in the "
                "parent; related variants belong in the challenge collection"
            )
    new_partitions = _allocate(new, seed, noun="new groups")

    partitions = {
        name: sorted(parent_manifest["partitions"][name] + new_partitions[name])
        for name in PARTITIONS
    }
    child = _manifest(dataset_sha256, seed, partitions, accepted)
    new_by_id = {r["query_id"]: r for r in new}
    child.update(
        parent_manifest_sha256=parent_manifest_sha256,
        parent_dataset_sha256=parent_dataset_sha256,
        new_groups={
            "by_class": {
                label: len({r["group_id"] for r in new if r["label"] == label})
                for label in LABELS
            },
            "by_partition": {
                name: len({new_by_id[q]["group_id"] for q in ids})
                for name, ids in new_partitions.items()
            },
        },
    )
    return child


def check_extension(
    child, parent, parent_rows, rows, dataset_sha256, parent_manifest_sha256
):
    """Every way a child manifest could disturb its parent's frozen evidence."""
    errors = [
        f"parent: {e}"
        for e in check_split(parent, parent_rows, _get(parent, "dataset_sha256"))
    ]
    errors += check_split(child, rows, dataset_sha256)
    if errors:
        return errors
    child_where = {q: n for n, ids in child["partitions"].items() for q in ids}
    for name, ids in parent["partitions"].items():
        for query_id in ids:
            if query_id not in child_where:
                errors.append(f"{query_id}: parent row missing from the child")
            elif child_where[query_id] != name:
                errors.append(
                    f"{query_id}: moved from parent {name} to {child_where[query_id]}"
                )
    # The rebuild catches everything else: reused groups, hand-moved new groups,
    # wrong lineage hashes or new-group counts.
    try:
        expected = extend_split(
            parent,
            parent_rows,
            rows,
            parent["dataset_sha256"],
            parent_manifest_sha256,
            dataset_sha256,
            child["seed"],
        )
    except (ValueError, TypeError) as error:
        return errors + [f"child cannot be rebuilt from the parent: {error}"]
    if child != expected:
        errors.append("child differs from the manifest rebuilt from parent and rows")
    return errors


def _get(manifest, key):
    return manifest.get(key) if isinstance(manifest, dict) else None


def check_split(manifest, rows, dataset_sha256):
    if not isinstance(manifest, dict):
        return ["manifest is not a JSON object"]
    missing = [key for key in MANIFEST_KEYS if key not in manifest]
    if missing:
        return [f"manifest missing fields: {', '.join(missing)}"]
    if manifest["manifest_version"] != MANIFEST_VERSION:
        return [f"unsupported manifest_version {manifest['manifest_version']!r}"]
    parts = manifest["partitions"]
    if (
        not isinstance(parts, dict)
        or set(parts) != set(PARTITIONS)
        or not all(isinstance(ids, list) for ids in parts.values())
        or not isinstance(manifest["groups"], dict)
        or not isinstance(manifest["row_sha256"], dict)
        or not all(isinstance(q, str) for ids in parts.values() for q in ids)
        or not all(isinstance(g, str) for g in manifest["groups"].values())
    ):
        return ["manifest partitions or groups are malformed"]

    errors = []
    for key, expected in (
        ("algorithm", "StratifiedGroupKFold"),
        ("n_splits", N_SPLITS),
        ("fold_partition", {str(k): v for k, v in FOLD_PARTITION.items()}),
        ("class_order", list(LABELS)),
    ):
        if manifest[key] != expected:
            errors.append(f"manifest {key} is {manifest[key]!r}, expected {expected!r}")
    if manifest["dataset_sha256"] != dataset_sha256:
        errors.append("stale dataset hash: manifest does not match the dataset file")
    for row in rows:
        if row.get("status") == "needs_review":
            errors.append(f"{row['query_id']}: needs_review row in dataset")

    accepted = {r["query_id"]: r for r in rows if r.get("status") == "accepted"}
    seen = Counter(query_id for ids in parts.values() for query_id in ids)
    for query_id in sorted(q for q, n in seen.items() if n > 1):
        errors.append(f"{query_id}: appears {seen[query_id]} times across partitions")
    for query_id in sorted(set(accepted) - set(seen)):
        errors.append(f"{query_id}: accepted row missing from partitions")
    for query_id in sorted(set(seen) - set(accepted)):
        errors.append(f"{query_id}: partition member is not an accepted row")
    for query_id, row in sorted(accepted.items()):
        if manifest["groups"].get(query_id) != row["group_id"]:
            errors.append(f"{query_id}: manifest group disagrees with dataset")

    for query_id, row in sorted(accepted.items()):
        if manifest["row_sha256"].get(query_id) != row_hash(row):
            errors.append(f"{query_id}: row content hash disagrees with dataset")
    for query_id in sorted(set(manifest["row_sha256"]) - set(accepted)):
        errors.append(f"{query_id}: row hash for a row that is not accepted")

    for query_id in sorted(set(manifest["groups"]) - set(accepted)):
        errors.append(f"{query_id}: manifest group for a row that is not accepted")
    recomputed = {
        name: _counts(accepted, [q for q in ids if q in accepted])
        for name, ids in parts.items()
    }
    if manifest["counts"] != recomputed:
        errors.append("manifest counts differ from the counts of its partitions")

    where = {}
    for name, ids in parts.items():
        for query_id in ids:
            if query_id in accepted:
                where.setdefault(accepted[query_id]["group_id"], set()).add(name)
    for group, names in sorted(where.items()):
        if len(names) > 1:
            errors.append(f"group {group} spans {', '.join(sorted(names))}")

    for name, ids in parts.items():
        present = {accepted[q]["label"] for q in ids if q in accepted}
        for label in LABELS:
            if label not in present:
                errors.append(f"partition {name} has no rows for class {label}")
    return errors


def check_materialized(manifest, partitions):
    """Check visible partitions against frozen content without opening test rows."""
    if not isinstance(manifest, dict) or any(k not in manifest for k in MANIFEST_KEYS):
        return ["split manifest is malformed or missing fields"]
    parts = manifest["partitions"]
    if (
        not isinstance(parts, dict)
        or set(parts) != set(PARTITIONS)
        or not all(
            isinstance(ids, list) and all(isinstance(q, str) for q in ids)
            for ids in parts.values()
        )
        or not isinstance(manifest["groups"], dict)
        or not isinstance(manifest["row_sha256"], dict)
    ):
        return ["manifest partitions or groups are malformed"]
    errors = []
    for key, expected in (
        ("manifest_version", MANIFEST_VERSION),
        ("algorithm", "StratifiedGroupKFold"),
        ("n_splits", N_SPLITS),
        ("fold_partition", {str(k): v for k, v in FOLD_PARTITION.items()}),
    ):
        if manifest[key] != expected:
            errors.append(f"manifest {key} differs from the split contract")
    ids = [q for members in parts.values() for q in members]
    if len(ids) != len(set(ids)):
        errors.append("query IDs overlap across partitions")
    if set(ids) != set(manifest["groups"]) or set(ids) != set(manifest["row_sha256"]):
        errors.append("manifest group and content hash IDs differ from partitions")
    group_parts = {}
    for name, members in parts.items():
        for q in members:
            group = manifest["groups"].get(q)
            if not isinstance(group, str) or not group:
                errors.append(f"{q}: manifest group is invalid")
                continue
            group_parts.setdefault(group, set()).add(name)
    if any(len(names) > 1 for names in group_parts.values()):
        errors.append("group spans multiple partitions")
    if manifest["class_order"] != list(LABELS):
        errors.append("manifest class_order differs from required labels")
    for name, rows in partitions.items():
        if sorted(r["query_id"] for r in rows) != sorted(parts[name]):
            errors.append(f"{name} query_ids differ from the split manifest")
        for row in rows:
            q = row["query_id"]
            if row.get("status") != "accepted":
                errors.append(f"{q}: materialized row is not accepted")
            if not isinstance(row.get("group_id"), str) or manifest["groups"].get(
                q
            ) != row.get("group_id"):
                errors.append(f"{q}: manifest group disagrees with materialized row")
            if not all(k in row for k in ("text", "label", "group_id")) or manifest[
                "row_sha256"
            ].get(q) != row_hash(row):
                errors.append(f"{q}: content hash disagrees with materialized row")
        counts = {label: sum(r["label"] == label for r in rows) for label in LABELS}
        if any(n == 0 for n in counts.values()):
            errors.append(f"{name} is missing a class")
        if (
            not isinstance(manifest["counts"], dict)
            or manifest["counts"].get(name) != counts
        ):
            errors.append(f"{name} counts differ from split manifest")
    return errors


def materialize(manifest, rows, train_path, validation_path, test_path):
    rows_by_id = {r["query_id"]: r for r in rows}
    paths = {"train": train_path, "validation": validation_path, "test": test_path}
    contents = {}
    for name, path in paths.items():
        ids = sorted(manifest["partitions"][name])
        contents[Path(path)] = "".join(
            json.dumps(rows_by_id[q], ensure_ascii=False) + "\n" for q in ids
        )
    for path, text in contents.items():
        if path.exists() and path.read_text(encoding="utf-8") != text:
            raise ValueError(
                f"{path} exists and differs; materialized files are immutable"
            )
    for path, text in contents.items():
        if not path.exists():
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
