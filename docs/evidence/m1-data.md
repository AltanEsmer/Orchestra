# M1 data tooling evidence (P1, tooling part)

This record covers the validator and review-ledger tooling only. It contains no research data, human labels, or agreement measurement. Every number below comes from an artificial fixture (source `fixture`, 120 generated rows, 32 generated review entries) written to a scratch directory outside the repository. It shows the tool's behavior, not dataset quality or annotator agreement.

## What changed

- `validate` stays structural. A source now needs `author` and `created`; `license` is no longer a structural error, so a draft pilot validates while permission is pending.
- `--review LEDGER` validates a review ledger and prints agreement (matching `original_label` and `review_label` divided by reviewed rows, plus counts by `review_kind`).
- `--ready` (requires `--review`) runs the M1 acceptance checks: 120 accepted rows, 30 per class, 15 groups per class, no `needs_review` row, a license on every used source, ceil(0.2 x class rows) reviewed rows per class, a nonempty ledger, and ledger `resolved_label` equal to the dataset label.
- The summary adds the dataset SHA-256, word-length min/median/max, source mix, group-size distribution, and excluded rows with reasons.

Ledger format: JSONL, exactly `query_id, original_label, review_label, reviewer_id, review_date, review_kind, resolved_label`. See the [data protocol](../data-and-evaluation.md#review-ledger-and-readiness).

## Fixture live runs (artificial)

Fixture: 120 accepted rows (30 per class, 15 two-row groups per class), one excluded row, ledger with 8 reviews per class where one review per class disagrees. Commands used `--sources` pointing at the scratch fixture manifest.

Structural mode, no ledger (summary abridged to key lines; the real output was longer):

```text
$ uv run --locked python scripts/validate_dataset.py data.jsonl --sources sources.json
  "sha256": "0b74b85d13a3c76ff46ec331d96d650ea1c2c9088643c4ec248f5cd651e7b6bd",
  "rows": 121,
  "status": {"accepted": 120, "needs_review": 0, "excluded": 1},
  "words": {"min": 5, "median": 5.0, "max": 5},
  "source_mix": {"fixture": 120},
  "group_sizes": {"2": 60},
  "excluded": [{"query_id": "f9000", "rationale": "needs live data"}]
PASS: 121 rows valid
```

With the ledger (exit 0), the agreement block:

```text
  "agreement": {"matching": 28, "reviewed": 32, "rate": 0.875,
                "by_kind": {"second_human": 16, "delayed_self": 16}}
PASS: 121 rows valid
```

Readiness mode (exit 0):

```text
$ uv run --locked python scripts/validate_dataset.py data.jsonl --sources sources.json --review ledger.jsonl --ready
PASS: ready for M2 (120 accepted rows, 32 reviewed)
```

Rejections (exit 1 and 2):

```text
$ ... --sources sources-draft.json --review ledger.jsonl --ready   # same fixture, license null
ERROR: source fixture: no license, permission missing
FAIL: 1 errors

$ ... --ready                                                      # no --review
validate_dataset.py: error: --ready requires --review
```

## Repository checks

```text
uv sync --locked          -> Resolved 9 packages / Checked 8 packages
scripts/smoke.py          -> PASS: environment-smoke-only; ... Python 3.12.13; scikit-learn 1.9.1
unittest discover         -> Ran 36 tests ... OK
ruff check .              -> All checks passed!
ruff format --check .     -> 19 files already formatted
git diff --check          -> exit 0
```

## Human gates still open

None of these is established by the tooling or this record.

- Pilot rows: the 40 pilot candidates are not written.
- Guide v1: `docs/annotation-guide.md` remains draft v0 until Altan freezes it.
- Human review: no second reviewer or delayed self-review exists; no real ledger or agreement figure.
- License: `data/manifests/sources.json` still has `license: null`, so real data cannot pass `--ready`.
- 120 accepted rows, with 30 per class and 15 groups per class: not collected.
- Collection brief for the 400-row expansion: not frozen.
- Archive and restore: no local rows exist to archive; restoration to another directory is unverified.
- Semantic label correctness is outside what any check here can tell.
