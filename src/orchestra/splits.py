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
    "counts",
    "proportions",
)


def _counts(rows_by_id, ids):
    labels = Counter(rows_by_id[query_id]["label"] for query_id in ids)
    return {label: labels[label] for label in LABELS}


def make_split(rows, dataset_sha256, seed=42):
    review = sorted(r["query_id"] for r in rows if r.get("status") == "needs_review")
    if review:
        raise ValueError(f"unresolved needs_review rows: {', '.join(review)}")
    accepted = sorted(
        (r for r in rows if r.get("status") == "accepted"), key=lambda r: r["query_id"]
    )
    for label in LABELS:
        groups = {r["group_id"] for r in accepted if r["label"] == label}
        if len(groups) < N_SPLITS:
            raise ValueError(
                f"class {label} has {len(groups)} groups; "
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
    counts = {name: _counts(rows_by_id, ids) for name, ids in partitions.items()}
    for name, by_label in counts.items():
        absent = [label for label in LABELS if by_label[label] == 0]
        if absent:
            raise ValueError(
                f"partition {name} has no rows for class {', '.join(absent)}; "
                "collect more groups instead of searching seeds"
            )
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
        "groups": {r["query_id"]: r["group_id"] for r in accepted},
        "counts": counts,
        "proportions": {
            name: round(len(ids) / len(accepted), 4) for name, ids in partitions.items()
        },
    }


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
    ):
        return ["manifest partitions or groups are malformed"]

    errors = []
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


def materialize(manifest, rows, train_path, validation_path, test_path):
    rows_by_id = {r["query_id"]: r for r in rows}
    paths = {"train": train_path, "validation": validation_path, "test": test_path}
    for name, path in paths.items():
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        ids = sorted(manifest["partitions"][name])
        lines = (json.dumps(rows_by_id[q], ensure_ascii=False) + "\n" for q in ids)
        with open(path, "w", encoding="utf-8") as file:
            file.writelines(lines)
