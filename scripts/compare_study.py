"""Compare a reproduced study with the archived original, file by file."""

import argparse
import collections
import fnmatch
import json
import math
import sys
from pathlib import Path

from orchestra import experiment

ORIGINAL_RUN = "m3-5-full-a"
CONFIDENCE = "results/m4-5-validation"
FINAL = "results/final-test-m3-5"
FIGURES = "results/m5-figures"
TIMED = "hashes a file that records run times"

# Differences that a rerun must produce, each with its reason. A pattern
# matches the location printed for a difference; "{run}" is the new run ID.
FREEZE_EXPECTED = (
    ("/frozen_utc", "time of the rerun"),
    ("/git_sha", "commit of the rerun"),
    ("/confidence_manifest_sha256", TIMED),
    ("/config/hashes/*/results/{run}/manifest.json", TIMED),
    ("/config/hashes/*/results/{run}-selection.json", TIMED),
    ("/config/code_hashes/*/src/orchestra/__main__.py", "changed after the freeze"),
    ("/config/code_hashes/*/src/orchestra/confidence.py", "changed after the freeze"),
)
FIGURE_SOURCE_EXPECTED = tuple(
    (f"/sources/{name}", TIMED)
    for name in (
        "run/manifest.json",
        "selection.json",
        "confidence/manifest.json",
        "final/manifest.json",
    )
) + (("/files/*", "hashes the figure provenance files above"),)

# Each check names files by their original path; the reproduced copy has the
# same path with the run ID replaced. "bytes" needs identical files, "json"
# identical parsed content once paths and run IDs are mapped, and "run" the
# project's own run comparison.
CHECKS = (
    (
        "split",
        "bytes",
        [
            "data/processed/m3-5/train.jsonl",
            "data/processed/m3-5/validation.jsonl",
            "data/processed/sealed/m3-5-test.jsonl",
        ],
        (),
    ),
    ("collection check", "json", ["data/raw/m3-5-import/collection-check.json"], ()),
    (
        "prepared configs",
        "json",
        ["data/processed/m3-5-prepared.json", "data/processed/m3-5-prepared-jev.json"],
        (),
    ),
    ("validation run", "run", [f"results/{ORIGINAL_RUN}"], ()),
    ("selection", "json", [f"results/{ORIGINAL_RUN}-selection.json"], ()),
    ("validation errors", "json", [f"results/{ORIGINAL_RUN}-report/errors.jsonl"], ()),
    (
        "confidence",
        "json",
        [
            f"{CONFIDENCE}/{name}"
            for name in (
                "calibration-folds.json",
                "error-review.jsonl",
                "metrics.json",
                "outcomes.json",
                "predictions.jsonl",
                "reliability.json",
                "systems.json",
                "thresholds.json",
            )
        ],
        (),
    ),
    ("freeze", "json", ["results/frozen-study-m3-5.json"], FREEZE_EXPECTED),
    (
        "final test",
        "json",
        [
            f"{FINAL}/{name}"
            for name in (
                "confusion.json",
                "error-review.jsonl",
                "metrics.json",
                "predictions.jsonl",
                "reliability.json",
                "thresholds.json",
                "warnings.json",
            )
        ],
        (),
    ),
    ("figure data", "json", [f"{FIGURES}/plot-data.json"], ()),
)


def load(path):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in text.splitlines()]
    return json.loads(text)


def relocate(value, mapping):
    if isinstance(value, str):
        for old, new in mapping:
            value = value.replace(old, new)
        return value
    if isinstance(value, list):
        return [relocate(v, mapping) for v in value]
    if isinstance(value, dict):
        return {relocate(k, mapping): relocate(v, mapping) for k, v in value.items()}
    return value


def differences(a, b, where=""):
    if isinstance(a, dict) and isinstance(b, dict):
        out = []
        for key in sorted(set(a) | set(b)):
            if key not in a or key not in b:
                out.append((f"{where}/{key}", "present on one side only"))
            else:
                out += differences(a[key], b[key], f"{where}/{key}")
        return out
    if isinstance(a, list) and isinstance(b, list) and len(a) == len(b):
        return [
            d
            for i, (x, y) in enumerate(zip(a, b, strict=True))
            for d in differences(x, y, f"{where}[{i}]")
        ]
    both_nan = isinstance(a, float) and isinstance(b, float)
    both_nan = both_nan and math.isnan(a) and math.isnan(b)
    return [] if a == b or both_nan else [(where, f"{a!r} != {b!r}"[:200])]


def figure_files(original):
    images = sorted(original.glob(f"{FIGURES}/*.png")) + sorted(
        original.glob(f"{FIGURES}/*.svg")
    )
    sources = sorted(original.glob(f"{FIGURES}/*.source.json"))
    names = [str(p.relative_to(original)) for p in images]
    return (
        ("figure images", "bytes", names, ()),
        (
            "figure provenance",
            "json",
            [str(p.relative_to(original)) for p in sources]
            + [f"{FIGURES}/provenance.json", f"{FIGURES}/manifest.json"],
            FIGURE_SOURCE_EXPECTED,
        ),
    )


def report_figures(reproduced):
    """The report's PNGs are copies of the export; its reliability panel
    redraws the final-test bins kept in a sidecar."""
    problems = []
    for name in ("class-balance.png", "word-lengths.png", "final-confusion-Jev.png"):
        tracked = reproduced / "report/figures" / name
        if tracked.read_bytes() != (reproduced / FIGURES / name).read_bytes():
            problems.append(f"report/figures/{name}: differs from the export")
    sidecar = load(reproduced / "report/figures/test-reliability.source.json")
    bins = load(reproduced / FINAL / "reliability.json")
    for system, saved in sidecar["bins"].items():
        if saved != bins[system]:
            problems.append(f"test-reliability sidecar: {system} bins differ")
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", required=True, type=Path)
    parser.add_argument("--reproduced", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    args = parser.parse_args(argv)
    original, reproduced = args.original.resolve(), args.reproduced.resolve()
    prepared = load(original / "data/processed/m3-5-prepared.json")
    original_root = str(Path(prepared["results_dir"]).parent)
    mapping = [(original_root, str(reproduced)), (ORIGINAL_RUN, args.run_id)]
    failed = 0
    for name, mode, paths, expected in CHECKS + figure_files(original):
        problems, explained = [], collections.Counter()
        for path in paths:
            left = original / path
            right = reproduced / path.replace(ORIGINAL_RUN, args.run_id)
            if mode == "bytes":
                same = left.read_bytes() == right.read_bytes()
                problems += [] if same else [f"{path}: bytes differ"]
                continue
            if mode == "run":
                problems += [f"{path}: {d}" for d in experiment.compare(left, right)]
                continue
            for where, detail in differences(
                relocate(load(left), mapping), load(right)
            ):
                rule = next(
                    (
                        (pattern, reason)
                        for pattern, reason in expected
                        if fnmatch.fnmatchcase(where, pattern.format(run=args.run_id))
                    ),
                    None,
                )
                if rule:
                    explained[rule] += 1
                else:
                    problems.append(f"{path}{where}: {detail}")
        for (pattern, reason), count in explained.items():
            print(f"EXPECTED: {name}: {count} x {pattern}: {reason}")
        for problem in problems:
            print(f"DIFF: {name}: {problem}")
        print(f"{'FAIL' if problems else 'PASS'}: {name}, {len(paths)} files")
        failed += bool(problems)
    names = {p.name for p in (original / FIGURES).iterdir()}
    extra = sorted({p.name for p in (reproduced / FIGURES).iterdir()} - names)
    problems = [f"{FIGURES}/{name}: not in the original" for name in extra]
    problems += report_figures(reproduced)
    for problem in problems:
        print(f"DIFF: report figures: {problem}")
    print(f"{'FAIL' if problems else 'PASS'}: report figures and figure set")
    failed += bool(problems)
    print("FAIL: reproduction differs" if failed else "PASS: study reproduces")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
