import datetime
import hashlib
import json
import math
import re
import statistics
from collections import Counter
from fractions import Fraction

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
# License is a readiness check, so a draft pilot can validate while permission is pending.
SOURCE_FIELDS = ("author", "created")
REVIEW_FIELDS = (
    "query_id",
    "original_label",
    "review_label",
    "reviewer_id",
    "review_date",
    "review_kind",
    "resolved_label",
)
REVIEW_KINDS = ("second_human", "delayed_self", "ai_assisted")
M1_REQUIREMENTS = {
    "accepted": 120,
    "per_class": 30,
    "groups_per_class": 15,
    "review_fraction": 0.2,
}
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
                errors.append(f"{path} line {number}: not a JSON object")
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


def validate_reviews(reviews, rows):
    errors = []
    by_id = {row["query_id"]: row for row in rows if is_filled(row.get("query_id"))}
    seen_ids = set()
    for index, review in enumerate(reviews, start=1):
        ref = review.get("query_id") or f"review {index}"
        ai = review.get("review_kind") == "ai_assisted"
        fields = REVIEW_FIELDS + (("ai_evidence", "human_adjudication") if ai else ())
        missing = [field for field in fields if field not in review]
        unknown = sorted(set(review) - set(fields))
        if missing:
            errors.append(f"{ref}: review missing fields {', '.join(missing)}")
        if unknown:
            errors.append(f"{ref}: review unknown fields {', '.join(unknown)}")
        if missing:
            continue

        if not is_filled(review["query_id"]):
            errors.append(f"{ref}: review empty query_id")
        elif review["query_id"] not in by_id:
            errors.append(f"{ref}: review for unknown query_id")
        elif review["query_id"] in seen_ids:
            errors.append(f"{ref}: duplicate review")
        else:
            seen_ids.add(review["query_id"])
            annotators = by_id[review["query_id"]].get("annotator_ids")
            if (
                review["review_kind"] == "second_human"
                and isinstance(annotators, list)
                and review["reviewer_id"] in annotators
            ):
                errors.append(f"{ref}: second_human reviewer is an annotator")
        if not is_filled(review["reviewer_id"]):
            errors.append(f"{ref}: review empty reviewer_id")
        for field in ("original_label", "review_label", "resolved_label"):
            # null resolved_label records exclusion or pending AI adjudication
            if review[field] not in LABELS and not (
                (
                    field == "resolved_label"
                    or (
                        ai
                        and field == "review_label"
                        and isinstance(review["ai_evidence"], dict)
                        and review["ai_evidence"].get("judgment")
                        in ("ambiguous", "exclude")
                    )
                )
                and review[field] is None
            ):
                errors.append(f"{ref}: review {field} {review[field]!r} is not a label")
        if review["review_kind"] not in REVIEW_KINDS:
            errors.append(f"{ref}: unknown review_kind {review['review_kind']!r}")
        try:
            valid_date = datetime.date.fromisoformat(review["review_date"]).isoformat()
        except (TypeError, ValueError):
            valid_date = None
        if valid_date != review["review_date"] or valid_date is None:
            errors.append(f"{ref}: review_date must be YYYY-MM-DD")
        if ai:
            annotators = (
                by_id.get(review["query_id"], {}).get("annotator_ids", [])
                if is_filled(review["query_id"])
                else []
            )
            if not isinstance(annotators, list):
                annotators = []
            if (
                not (
                    is_filled(review["reviewer_id"])
                    and review["reviewer_id"].startswith("ai:")
                    and is_filled(review["reviewer_id"][3:])
                )
                or review["reviewer_id"] in annotators
            ):
                errors.append(
                    f"{ref}: ai_assisted reviewer_id must identify an AI, not an annotator"
                )
            evidence = review["ai_evidence"]
            evidence_fields = {
                "model",
                "prompt_sha256",
                "input_sha256",
                "output_sha256",
                "judgment",
                "flags",
            }
            if not isinstance(evidence, dict) or set(evidence) != evidence_fields:
                errors.append(
                    f"{ref}: ai_evidence must contain exactly {', '.join(sorted(evidence_fields))}"
                )
            else:
                if not is_filled(evidence["model"]):
                    errors.append(f"{ref}: ai_evidence model must be nonempty")
                for field in ("prompt_sha256", "input_sha256", "output_sha256"):
                    if not isinstance(evidence[field], str) or not re.fullmatch(
                        r"[0-9a-fA-F]{64}", evidence[field]
                    ):
                        errors.append(
                            f"{ref}: ai_evidence {field} must be a SHA-256 hex digest"
                        )
                if evidence["judgment"] not in ("clear", "ambiguous", "exclude"):
                    errors.append(
                        f"{ref}: ai_evidence judgment must be clear, ambiguous or exclude"
                    )
                if not isinstance(evidence["flags"], list) or not all(
                    is_filled(flag) for flag in evidence["flags"]
                ):
                    errors.append(
                        f"{ref}: ai_evidence flags must be a list of nonempty strings"
                    )
                if review["human_adjudication"] is None:
                    clear_match = (
                        evidence["judgment"] == "clear"
                        and not evidence["flags"]
                        and review["review_label"] == review["original_label"]
                    )
                    if (
                        clear_match
                        and review["resolved_label"] != review["original_label"]
                    ):
                        errors.append(
                            f"{ref}: clear matching AI check must retain original_label without human adjudication"
                        )
                    elif not clear_match and review["resolved_label"] is not None:
                        errors.append(
                            f"{ref}: AI flags or disagreement require human adjudication or null resolved_label"
                        )
            decision = review["human_adjudication"]
            if decision is not None:
                if not isinstance(decision, dict) or set(decision) != {
                    "annotator_id",
                    "date",
                    "label",
                    "rationale",
                }:
                    errors.append(
                        f"{ref}: human_adjudication must contain exactly annotator_id, date, label, rationale"
                    )
                else:
                    if (
                        not is_filled(decision["annotator_id"])
                        or decision["annotator_id"] not in annotators
                    ):
                        errors.append(
                            f"{ref}: human_adjudication annotator_id must be a row annotator"
                        )
                    try:
                        date = datetime.date.fromisoformat(decision["date"]).isoformat()
                    except (TypeError, ValueError):
                        date = None
                    if date != decision["date"] or date is None:
                        errors.append(
                            f"{ref}: human_adjudication date must be YYYY-MM-DD"
                        )
                    if (
                        decision["label"] is not None
                        and decision["label"] not in LABELS
                    ):
                        errors.append(
                            f"{ref}: human_adjudication label is not a label or null"
                        )
                    if not is_filled(decision["rationale"]):
                        errors.append(
                            f"{ref}: human_adjudication rationale must be nonempty"
                        )
                    if review["resolved_label"] != decision["label"]:
                        errors.append(
                            f"{ref}: resolved_label differs from human_adjudication label"
                        )
    return errors


def agreement(reviews):
    human = [r for r in reviews if r["review_kind"] != "ai_assisted"]
    ai = [r for r in reviews if r["review_kind"] == "ai_assisted"]
    reviewed = len(human)
    matching = sum(r["original_label"] == r["review_label"] for r in human)
    result = {
        "matching": matching,
        "reviewed": reviewed,
        "rate": matching / reviewed if reviewed else None,
        "by_kind": {
            k: {
                "matching": sum(
                    r["review_kind"] == k and r["original_label"] == r["review_label"]
                    for r in reviews
                ),
                "reviewed": sum(r["review_kind"] == k for r in reviews),
            }
            for k in REVIEW_KINDS
            if k != "ai_assisted"
        },
    }
    if ai:
        matching_ai = sum(r["original_label"] == r["review_label"] for r in ai)
        result["ai_consistency"] = {
            "matching": matching_ai,
            "reviewed": len(ai),
            "rate": matching_ai / len(ai),
        }
    return result


def readiness(rows, sources, reviews, requirements):
    """Check release requirements. Never judges whether a label is semantically right."""
    errors = []
    accepted = [row for row in rows if row["status"] == "accepted"]
    if not accepted:
        return ["no accepted rows: the training dataset is empty"]
    if len(accepted) < requirements["accepted"]:
        errors.append(f"{len(accepted)} accepted rows, need {requirements['accepted']}")
    unresolved = sum(row["status"] == "needs_review" for row in rows)
    if unresolved:
        errors.append(f"{unresolved} rows still need review")

    pending_ai = {
        r["query_id"]
        for r in reviews
        if r["review_kind"] == "ai_assisted"
        and r["human_adjudication"] is None
        and (
            r["ai_evidence"]["judgment"] != "clear"
            or r["ai_evidence"]["flags"]
            or r["review_label"] != r["original_label"]
            or r["resolved_label"] != r["original_label"]
        )
    }
    errors.extend(f"{qid}: pending AI adjudication" for qid in sorted(pending_ai))
    qualifying_reviews = [r for r in reviews if r["query_id"] not in pending_ai]
    by_id = {row["query_id"]: row for row in accepted}
    # Exact arithmetic: float math.ceil(0.2 * 35) is 8, not 7.
    fraction = Fraction(str(requirements["review_fraction"]))
    reviewed_by_label = Counter(
        by_id[r["query_id"]]["label"]
        for r in qualifying_reviews
        if r["query_id"] in by_id
    )
    for label in LABELS:
        in_class = [row for row in accepted if row["label"] == label]
        groups = {row["group_id"] for row in in_class}
        if len(in_class) < requirements["per_class"]:
            errors.append(
                f"{label}: {len(in_class)} accepted rows, need {requirements['per_class']}"
            )
        if len(groups) < requirements["groups_per_class"]:
            errors.append(
                f"{label}: {len(groups)} groups, need {requirements['groups_per_class']}"
            )
        needed = math.ceil(fraction * len(in_class))
        if reviewed_by_label[label] < needed:
            errors.append(
                f"{label}: {reviewed_by_label[label]} reviewed rows, need {needed}"
            )

    if not reviews:
        errors.append("no review evidence")
    all_by_id = {row["query_id"]: row for row in rows}
    for review in reviews:
        row = all_by_id[review["query_id"]]
        # needs_review rows are already reported as unresolved.
        expected = {"accepted": row["label"], "excluded": None}.get(
            row["status"], "skip"
        )
        if expected != "skip" and review["resolved_label"] != expected:
            errors.append(
                f"{review['query_id']}: ledger resolved {review['resolved_label']}"
                f" but dataset {row['status']} row expects {expected}"
            )

    labels_by_group = {}
    for row in accepted:
        labels_by_group.setdefault(row["group_id"], set()).add(row["label"])
    reviewed_ids = {r["query_id"] for r in qualifying_reviews}
    for row in accepted:
        if (
            len(labels_by_group[row["group_id"]]) > 1
            and row["query_id"] not in reviewed_ids
        ):
            errors.append(
                f"group {row['group_id']}: mixed labels need review of {row['query_id']}"
            )

    for source_id in sorted({row["source_id"] for row in accepted}):
        if not is_filled(sources[source_id].get("license")):
            errors.append(f"source {source_id}: no license, permission missing")
    return errors


def file_sha256(path):
    with open(path, "rb") as file:
        return hashlib.sha256(file.read()).hexdigest()


def summarize(rows, sha256):
    accepted = [row for row in rows if row["status"] == "accepted"]
    groups_by_label = {label: set() for label in LABELS}
    labels_by_group = {}
    group_sizes = Counter()
    for row in accepted:
        groups_by_label[row["label"]].add(row["group_id"])
        labels_by_group.setdefault(row["group_id"], set()).add(row["label"])
        group_sizes[row["group_id"]] += 1
    words = [len(row["text"].split()) for row in accepted]
    return {
        "sha256": sha256,
        "rows": len(rows),
        "status": {s: sum(r["status"] == s for r in rows) for s in STATUSES},
        "accepted_by_label": {
            label: sum(r["label"] == label for r in accepted) for label in LABELS
        },
        "groups_by_label": {label: len(groups_by_label[label]) for label in LABELS},
        "mixed_label_groups": sorted(
            group for group, labels in labels_by_group.items() if len(labels) > 1
        ),
        "words": {
            "min": min(words, default=None),
            "median": statistics.median(words) if words else None,
            "max": max(words, default=None),
        },
        "source_mix": dict(sorted(Counter(r["source_id"] for r in accepted).items())),
        "group_sizes": dict(sorted(Counter(group_sizes.values()).items())),
        "excluded": [
            {"query_id": r["query_id"], "rationale": r["rationale"]}
            for r in rows
            if r["status"] == "excluded"
        ],
    }
