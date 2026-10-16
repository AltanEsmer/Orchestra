# M2 split tooling evidence (P2)

Everything below ran on an artificial fixture (48 generated rows, source `fixture`, 4 classes x 6 groups x 2 rows, two mixed-label groups) in a temporary directory outside the repository. **No research split exists.** No manifest, row, or sealed file from this run is committed. The counts below describe the fixture, not Orchestra data, and say nothing about routing quality.

## Packaging: setuptools pin

- Chosen: `setuptools==84.0.0` in `[build-system].requires` (`setuptools.build_meta`), with `[tool.uv] package = true` and a `src/` layout.
- Selection: `uv pip install --dry-run setuptools` resolved `setuptools==84.0.0`; PyPI's JSON API lists 84.0.0 as the newest release (previous: 83.0.0), uploaded 2026-08-08, wheel plus sdist, `requires_python >=3.10`.
- Verification: `uv sync --locked --reinstall-package orchestra -v` logged `Adding direct dependency: setuptools>=84.0.0, <84.0.0+` and rebuilt the editable package; `uv run --locked python -c "import orchestra"` imports `src/orchestra/__init__.py` with no `PYTHONPATH` or `sys.path` edit.
- `uv lock` regenerated `uv.lock` (only change: `orchestra` source `virtual` -> `editable`). uv does not record build requirements in `uv.lock`, so the exact build pin lives in `pyproject.toml` only. `uv sync --locked` succeeds from the lock.

## Live run

Command (config paths point into the temp directory; the fixture's SHA-256 is `99e9428b75b9e1d5e3cc3ae4313dcf07931b69f99226aa6b915f5415810a94cd`):

```text
uv run --locked python -m orchestra split --config <tmp>/config.json
```

Output (path shortened to `<tmp>`):

```text
{
  "counts": {
    "train": {"document_retrieval": 6, "knowledge_lookup": 7, "calculation": 8, "direct_answer": 9},
    "validation": {"document_retrieval": 3, "knowledge_lookup": 2, "calculation": 2, "direct_answer": 3},
    "test": {"document_retrieval": 2, "knowledge_lookup": 2, "calculation": 2, "direct_answer": 2}
  },
  "proportions": {"train": 0.625, "validation": 0.2083, "test": 0.1667}
}
PASS: split written to <tmp>/splits/m2-split.json
```

(The real output prints each count on its own line; compacted here.) Exit code 0. Files written: train 30 lines, validation 10, sealed test 8 (`wc -l`), 48 in total. Manifest SHA-256 `e89588179e5fce8a1ea6fab6160295f58eafee51787b04e92b4b7887ceeea0b5`. A second identical run printed `PASS` again (byte-identical manifest accepted); a changed config seed is refused by the CLI test (`exists and differs; manifests are immutable`).

Observed on this fixture: proportions are 62.5/20.8/16.7, not exactly 60/20/20, because whole groups move together and `StratifiedGroupKFold` only approximates stratification. Research proportions must be reported from the real manifest.

## Boundaries and limits

- Sealing is a workflow boundary, not encryption. The splitter and the data steward read all rows; that exposure must be recorded when real data is split. Developers may check hashes, membership, and aggregate counts only.
- The CLI prints counts and proportions, never query text.
- The "partition lacks a class" guard in `make_split` is defensive; no small input was found that passes the five-groups-per-class check yet leaves a partition without a class, so it is covered through `check_split` only.
- The splitter has not run on accepted M1 data. That depends on P1's human evidence (labels, review ledger, licenses).
