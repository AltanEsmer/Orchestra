"""M3.5 collection: seeded pool orders and the weighted interleave across sources."""

import random


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
