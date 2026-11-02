"""M3.5 collection: seeded pool orders, the weighted interleave and import adapters."""

import hashlib
import random
import re

from orchestra.data import LABELS

SCREEN_ID = "ai-screen"
ADJUDICATOR_ID = "A1"


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
