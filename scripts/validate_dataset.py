import argparse
import json
from collections import Counter

LABELS = ("document_retrieval", "knowledge_lookup", "calculation", "direct_answer")
STATUSES = ("accepted", "needs_review", "excluded")
FIELDS = (
    "query_id",
    "group_id",
    "text",
    "label",
    "status",
    "source_id",
    "rationale",
    "annotator_ids",
    "annotation_version",
)
SOURCE_FIELDS = ("author", "license", "created")
MAX_GROUP_SIZE = 4
TEXT_FIELDS = ("query_id", "group_id", "text", "rationale", "annotation_version")


def is_filled(value):
    return isinstance(value, str) and value.strip() != ""


def normalize(text):
    return " ".join(text.split()).casefold()


def read_jsonl(path):
    rows, errors = [], []
    with open(path, encoding="utf-8") as file:
        for number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                row = None
            if isinstance(row, dict):
                rows.append(row)
            else:
                errors.append(f"line {number}: not a JSON object")
    return rows, errors


def validate(rows, sources):
    errors = []
    complete = []
    seen_ids = set()
    for index, row in enumerate(rows, start=1):
        ref = row.get("query_id") or f"row {index}"
        missing = [field for field in FIELDS if field not in row]
        unknown = sorted(set(row) - set(FIELDS))
        if missing:
            errors.append(f"{ref}: missing fields {', '.join(missing)}")
        if unknown:
            errors.append(f"{ref}: unknown fields {', '.join(unknown)}")
        if missing:
            continue
        complete.append((ref, row))

        if is_filled(row["query_id"]):
            if row["query_id"] in seen_ids:
                errors.append(f"{ref}: duplicate query_id")
            seen_ids.add(row["query_id"])
        for field in TEXT_FIELDS:
            if not is_filled(row[field]):
                errors.append(f"{ref}: empty {field}")

        if row["status"] not in STATUSES:
            errors.append(f"{ref}: unknown status {row['status']}")
        if row["label"] is not None and row["label"] not in LABELS:
            errors.append(f"{ref}: unknown label {row['label']}")
        if row["status"] == "accepted" and row["label"] is None:
            errors.append(f"{ref}: accepted row has no label")

        annotators = row["annotator_ids"]
        if not (
            isinstance(annotators, list)
            and annotators
            and all(is_filled(name) for name in annotators)
        ):
            errors.append(f"{ref}: annotator_ids must be a non-empty list of strings")

        # Check the type first: a list source_id is unhashable and would crash `in`.
        if not (isinstance(row["source_id"], str) and row["source_id"] in sources):
            errors.append(f"{ref}: unknown source_id {row['source_id']}")

    first_ref_by_text = {}
    group_sizes = Counter()
    used_sources = set()
    for ref, row in complete:
        if is_filled(row["text"]):
            key = normalize(row["text"])
            if key in first_ref_by_text:
                errors.append(f"{ref}: same text as {first_ref_by_text[key]}")
            else:
                first_ref_by_text[key] = ref
        if is_filled(row["group_id"]):
            group_sizes[row["group_id"]] += 1
        if isinstance(row["source_id"], str) and row["source_id"] in sources:
            used_sources.add(row["source_id"])

    for group_id, size in group_sizes.items():
        if size > MAX_GROUP_SIZE:
            errors.append(f"group {group_id}: {size} rows exceeds {MAX_GROUP_SIZE}")

    for source_id in sorted(used_sources):
        entry = sources[source_id] if isinstance(sources[source_id], dict) else {}
        for field in SOURCE_FIELDS:
            if not is_filled(entry.get(field)):
                errors.append(f"source {source_id}: missing {field}")
    return errors


def summarize(rows):
    accepted = [row for row in rows if row["status"] == "accepted"]
    groups_by_label = {label: set() for label in LABELS}
    labels_by_group = {}
    for row in accepted:
        groups_by_label[row["label"]].add(row["group_id"])
        labels_by_group.setdefault(row["group_id"], set()).add(row["label"])
    return {
        "rows": len(rows),
        "status": {s: sum(r["status"] == s for r in rows) for s in STATUSES},
        "accepted_by_label": {
            label: sum(r["label"] == label for r in accepted) for label in LABELS
        },
        "groups_by_label": {label: len(groups_by_label[label]) for label in LABELS},
        "mixed_label_groups": sorted(
            group for group, labels in labels_by_group.items() if len(labels) > 1
        ),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate the annotated query dataset."
    )
    parser.add_argument("dataset")
    parser.add_argument("--sources", default="data/manifests/sources.json")
    args = parser.parse_args(argv)

    try:
        rows, errors = read_jsonl(args.dataset)
        with open(args.sources, encoding="utf-8") as file:
            sources = json.load(file)
    except OSError as error:
        print(f"ERROR: cannot read {error.filename}: {error.strerror}")
        return 1
    except json.JSONDecodeError:
        print(f"ERROR: {args.sources}: not valid JSON")
        return 1
    if not isinstance(sources, dict):
        print(f"ERROR: {args.sources}: must be a JSON object")
        return 1

    errors += validate(rows, sources)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAIL: {len(errors)} errors")
        return 1
    print(json.dumps(summarize(rows), indent=2))
    print(f"PASS: {len(rows)} rows valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
