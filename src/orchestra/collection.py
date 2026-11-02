"""M3.5 collection: seeded orders, interleave, import adapters and release checks."""

import hashlib
import random
import re
from collections import Counter
from fractions import Fraction

from orchestra.data import LABELS, MAX_GROUP_SIZE, normalize

SCREEN_ID = "ai-screen"
ADJUDICATOR_ID = "A1"
# Guide v2 batch limits, applied to the cumulative release (collection brief M3.5).
MAX_SOURCE_SHARE = Fraction(3, 4)
MAX_TYPE_SHARE = Fraction(2, 5)
MIN_SOURCES = 2
MIN_NEW_GROUPS = 5
CLOSE_PAIR = 0.5


def seeded_order(keys, seed=42, first=()):
    """Saved sample keys first, then the rest of the pool in a seeded shuffle.

    The rest is sorted before shuffling, so the input order never matters.
    """
    keys, first = list(keys), list(first)
    if len(set(keys)) != len(keys) or len(set(first)) != len(first):
        raise ValueError("pool keys must be unique")
    unknown = set(first) - set(keys)
    if unknown:
        raise ValueError(f"sample keys missing from the pool: {sorted(unknown)}")
    rest = sorted(set(keys) - set(first))
    random.Random(seed).shuffle(rest)
    return first + rest


def interleave(streams, weights):
    """Yield (name, item) from named iterators by smooth weighted round robin.

    Each step every live stream gains its weight; the highest total is drawn
    (ties go to the earlier stream) and pays back the sum of live weights.
    An exhausted stream drops out and the others continue in their ratio.
    """
    if set(streams) != set(weights) or any(w <= 0 for w in weights.values()):
        raise ValueError("every stream needs one positive weight")
    live = list(streams)
    current = dict.fromkeys(live, 0)
    while live:
        for name in live:
            current[name] += weights[name]
        name = max(live, key=lambda n: current[n])
        try:
            item = next(streams[name])
        except StopIteration:
            live.remove(name)
            continue
        current[name] -= sum(weights[n] for n in live)
        yield name, item


def import_row(query_id, group_id, text, label, source_id, rationale, adjudicated):
    """An accepted guide-v3 row with the public text exactly as written."""
    if label not in LABELS:
        raise ValueError(f"{query_id}: unknown label {label!r}")
    return {
        "query_id": query_id,
        "group_id": group_id,
        "text": text,
        "label": label,
        "status": "accepted",
        "source_id": source_id,
        "rationale": rationale,
        "annotator_ids": [SCREEN_ID, ADJUDICATOR_ID] if adjudicated else [SCREEN_ID],
        "annotation_version": "guide-v3",
    }


def split_passage(prompt, instruction):
    """Split an inline passage off by exact substring; the query is the instruction.

    The passage is everything else, character for character. A row whose
    instruction is missing, repeated or leaves no passage is skipped, not edited.
    """
    if not instruction.strip() or prompt.count(instruction) != 1:
        raise ValueError("instruction must occur exactly once in the prompt")
    before, after = prompt.split(instruction)
    passage = before + after
    if not passage.strip():
        raise ValueError("no passage left after the instruction")
    return instruction, passage


def passage_attachment(query_id, passage, expected_sha256=None):
    """A local passage attachment, checked against the hash the pool recorded."""
    digest = hashlib.sha256(passage.encode("utf-8")).hexdigest()
    if expected_sha256 is not None and digest != expected_sha256:
        raise ValueError(f"{query_id}: passage differs from its recorded hash")
    return {"query_id": query_id, "kind": "passage", "sha256": digest, "text": passage}


def table_attachment(query_id, path, revision, lfs_sha256):
    """A pinned reference to an upstream table, which is never downloaded."""
    if not re.fullmatch(r"[0-9a-f]{64}", lfs_sha256):
        raise ValueError(f"{query_id}: table LFS SHA-256 is malformed")
    return {
        "query_id": query_id,
        "kind": "table",
        "path": path,
        "revision": revision,
        "lfs_sha256": lfs_sha256,
    }


def tokens(text):
    return set(re.findall(r"[a-z0-9']+", text.casefold()))


def jaccard(left, right):
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def cap_hold(rows, types, candidate, candidate_type):
    """Why adding the candidate would push its class over a share cap, or None.

    Only the candidate's own source and type can rise, so only those are checked.
    """
    in_class = [r for r in rows if r["label"] == candidate["label"]]
    size = len(in_class) + 1
    same_source = 1 + sum(r["source_id"] == candidate["source_id"] for r in in_class)
    same_type = 1 + sum(types[r["query_id"]] == candidate_type for r in in_class)
    if same_source > MAX_SOURCE_SHARE * size:
        return f"source {candidate['source_id']}: {same_source} of {size}"
    if same_type > MAX_TYPE_SHARE * size:
        return f"type {candidate_type}: {same_type} of {size}"
    return None


def check_release(rows, parent_ids, types, pair_decisions):
    """Cumulative M3.5 count and batch checks over accepted rows.

    `parent_ids` are the frozen M3 rows, `types` maps every query ID to its
    request type, and `pair_decisions` records the hand check of each close
    new pair as {"pair": [a, b], "same_group": bool, "reason": str}. Messages
    name query IDs only, so sealed parent text is never printed.
    """
    errors = []
    new = [r for r in rows if r["query_id"] not in parent_ids]
    parent = [r for r in rows if r["query_id"] in parent_ids]

    first_by_text = {}
    for row in rows:
        key = normalize(row["text"])
        if key in first_by_text:
            errors.append(f"{row['query_id']}: same text as {first_by_text[key]}")
        first_by_text.setdefault(key, row["query_id"])
    for group, size in Counter(r["group_id"] for r in rows).items():
        if size > MAX_GROUP_SIZE:
            errors.append(f"group {group}: {size} rows exceeds {MAX_GROUP_SIZE}")
    missing = sorted(r["query_id"] for r in rows if r["query_id"] not in types)
    errors += [f"{query_id}: no request type" for query_id in missing]

    by_class = {}
    parent_groups = {r["group_id"] for r in parent}
    for label in LABELS:
        in_class = [r for r in rows if r["label"] == label]
        sources = Counter(r["source_id"] for r in in_class)
        kinds = Counter(types.get(r["query_id"]) for r in in_class)
        new_groups = {r["group_id"] for r in new if r["label"] == label}
        size = len(in_class)
        if len(sources) < MIN_SOURCES:
            errors.append(f"{label}: needs {MIN_SOURCES} sources, has {len(sources)}")
        for source, count in sources.items():
            if count > MAX_SOURCE_SHARE * size:
                errors.append(f"{label}: source {source} has {count} of {size}")
        for kind, count in kinds.items():
            if kind is not None and count > MAX_TYPE_SHARE * size:
                errors.append(f"{label}: type {kind} has {count} of {size}")
        if len(new_groups - parent_groups) < MIN_NEW_GROUPS:
            errors.append(
                f"{label}: {len(new_groups - parent_groups)} new groups, "
                f"need {MIN_NEW_GROUPS}"
            )
        by_class[label] = {
            "rows": size,
            "new_rows": sum(r["label"] == label for r in new),
            "groups": len({r["group_id"] for r in in_class}),
            "new_groups": len(new_groups - parent_groups),
            "sources": dict(sorted(sources.items())),
            "types": dict(sorted((str(k), v) for k, v in kinds.items())),
        }

    for row in new:
        if row["group_id"] in parent_groups:
            errors.append(f"{row['query_id']}: in parent group {row['group_id']}")
    parent_tokens = [(r["query_id"], tokens(r["text"])) for r in parent]
    new_tokens = [(r, tokens(r["text"])) for r in new]
    for row, words in new_tokens:
        for query_id, other in parent_tokens:
            if jaccard(words, other) >= CLOSE_PAIR:
                errors.append(f"{row['query_id']}: overlaps parent row {query_id}")

    decided = {tuple(sorted(d["pair"])): d["same_group"] for d in pair_decisions}
    pairs = []
    for i, (left, left_words) in enumerate(new_tokens):
        for right, right_words in new_tokens[i + 1 :]:
            score = jaccard(left_words, right_words)
            if score < CLOSE_PAIR:
                continue
            pair = tuple(sorted((left["query_id"], right["query_id"])))
            together = left["group_id"] == right["group_id"]
            pairs.append({"pair": list(pair), "jaccard": round(score, 4)})
            if together:
                continue
            if pair not in decided:
                errors.append(f"{pair[0]}, {pair[1]}: close pair needs a hand check")
            elif decided[pair]:
                errors.append(f"{pair[0]}, {pair[1]}: hand check says share a group")
    return {"errors": errors, "by_class": by_class, "close_pairs": pairs}
