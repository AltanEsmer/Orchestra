# M3.5 research run: 26 local configurations

Run November 2, 2026 on the [M3.5 release](m3-5-dataset.md) `m3-5-v1` after [PR #27](https://github.com/AltanEsmer/Orchestra/pull/27) merged into `main` (merge commit `0f481bcd00441d6e712ab709f511c7a26c4637f7`). This is a validation-only comparison. The sealed test was not opened. Jev has no response log, because Altan has no TypeSafe key, spending cap or data-handling approval, so the 27-configuration selection is invalid by design. That is the expected stop state. The per-family winners below follow the frozen tie rules, but none is "chosen" until Jev has an outcome or Altan records a scope decision.

## Data

| Partition | Rows | Retrieval | Lookup | Calculation | Direct |
| --- | ---: | ---: | ---: | ---: | ---: |
| Train | 1,888 | 601 | 296 | 390 | 601 |
| Validation | 629 | 199 | 100 | 130 | 200 |
| Test (sealed, unopened) | 628 | 200 | 98 | 131 | 199 |

The release record has the counts by source, the agreement, adjudication and exclusion counts and the cue counts by class. Validation macro-F1 weights the four classes equally, but the classes are unequal (lookup 100, retrieval 199 on validation).

## Commands

```sh
scripts/run_experiment.sh --config data/processed/m3-5-prepared.json --run-id m3-5-a
scripts/run_experiment.sh --config data/processed/m3-5-prepared.json --run-id m3-5-b
uv run --locked python -m orchestra compare --left results/m3-5-a --right results/m3-5-b
uv run --locked python -m orchestra select --run results/m3-5-a --out results/m3-5-a-selection.json
uv run --locked python -m orchestra report --run results/m3-5-a --selection results/m3-5-a-selection.json --train data/processed/m3-5/train.jsonl --validation data/processed/m3-5/validation.jsonl
sh work/m3-5-archive/run.sh
```

The launcher set `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS` and `VECLIB_MAXIMUM_THREADS` to 1, and each run was wrapped in `/usr/bin/time -l`. Environment: macOS 27.0 arm64, Python 3.12.13, uv 0.11.7, scikit-learn 1.9.1, XGBoost 3.4.1, NumPy 2.5.3. Both runs record `git_dirty: true` only because of two untracked folders in the checkout (`output/`, `tmp/`) that belong to Altan and were left alone; no tracked file differed, which the archive script also checks.

Actual outputs:

- Both runs: all 26 configurations `ok`, `PASS: run written`.
- `compare`: `PASS: runs reproduce`.
- `select`: exit 1, `FAIL: selection is not valid`, with `missing: ["Jev"]` and `complete_matrix: false`.
- `report`: `INVALID selection: Jev; report written to results/m3-5-a-report`.
- `work/m3-5-archive/run.sh`: `PASS: archived M3.5 inputs match the hashes recorded by prepare-study`, `PASS: 59 restored files byte-identical to originals`, and after a fresh `uv sync --locked` in the restored copy, `PASS: runs reproduce` for `m3-5-restored` against `m3-5-a`.

## Validation results

| Configuration | Macro-F1 | Accuracy | Fit (s) |
| --- | ---: | ---: | ---: |
| B0 | 0.121 | 0.318 | 0.02 |
| B1 | 0.878 | 0.874 | 0.02 |
| L1-C0.1 / C1 / C10 | 0.903 / 0.922 / 0.918 | 0.908 / 0.925 / 0.922 | 0.06 / 0.08 / 0.07 |
| L2-C0.1 / C1 / C10 | 0.734 / 0.924 / 0.932 | 0.774 / 0.925 / 0.935 | 0.03 / 0.05 / 0.08 |
| S1-C0.1 / C1 / C10 | 0.928 / 0.936 / 0.940 | 0.928 / 0.938 / 0.941 | 0.02 / 0.02 / 0.03 |
| L3-C0.1 / C1 / C10 | 0.704 / 0.930 / 0.952 | 0.754 / 0.933 / 0.954 | 0.06 / 0.11 / 0.13 |
| DT-d10-leaf1 / leaf3 | 0.716 / 0.714 | 0.742 / 0.742 | 0.03 / 0.03 |
| DT-d30-leaf1 / leaf3 | 0.818 / 0.801 | 0.828 / 0.817 | 0.05 / 0.04 |
| RF-d30-leaf1 / leaf3 | 0.883 / 0.859 | 0.893 / 0.874 | 0.32 / 0.17 |
| RF-dNone-leaf1 / leaf3 | 0.913 / 0.891 | 0.917 / 0.901 | 0.61 / 0.19 |
| XGB-d3-lr0.05 / lr0.1 | 0.879 / 0.894 | 0.886 / 0.901 | 1.84 / 1.64 |
| XGB-d6-lr0.05 / lr0.1 | 0.901 / 0.907 | 0.908 / 0.913 | 5.18 / 4.26 |

Per-family winners under the frozen rules (inclusive 0.01 tolerance; smallest C; shallower depth, then larger leaf or lower learning rate). The selection file records each family's tie set and leaves `chosen` empty because the matrix is incomplete:

| Family | Tie set | Winner | Macro-F1 | Median latency (629 rows) |
| --- | --- | --- | ---: | ---: |
| B0 | B0 | B0 | 0.121 | 3.8 ms |
| B1 | B1 | B1 | 0.878 | 3.7 ms |
| L1 | C1, C10 | L1-C1 | 0.922 | 3.7 ms |
| L2 | C1, C10 | L2-C1 | 0.924 | 3.8 ms |
| S1 | C1, C10 | S1-C1 | 0.936 | 3.8 ms |
| L3 | C10 | L3-C10 | 0.952 | 7.2 ms |
| DT | d30-leaf1 | DT-d30-leaf1 | 0.818 | 3.9 ms |
| RF | dNone-leaf1 | RF-dNone-leaf1 | 0.913 | 18.6 ms |
| XGB | d6-lr0.05, d6-lr0.1 | XGB-d6-lr0.05 | 0.901 | 9.7 ms |
| Jev | missing | none | | |

Among the local families, L3-C10 (unigram and bigram TF-IDF with logistic regression) has the highest validation macro-F1, 0.952. Its per-class F1 is retrieval 0.975, calculation 0.954, lookup 0.943 and direct answer 0.938. No overall system is chosen: the M3.5 overall order includes Jev, and the selection stays invalid until Jev has an outcome or Altan records a scope decision. On this split the tree families trail the linear models, and a single tree trails the forest and boosting. These are observed validation results on one split, not test results, and they cannot be compared directly with M3's 0.925, which came from a different 79-row validation set.

## Resources

Altan has not formally answered the proposed limits of 15 minutes and 2 GiB per run, so they were applied as proposed.

| Run | Wall time | Peak resident memory |
| --- | ---: | ---: |
| m3-5-a | 22.0 s | 319.4 MiB (334,954,496 bytes in `timing.json`) |
| m3-5-b | 21.8 s | 320.3 MiB (from `time -l`) |

The 26 fits take 15.2 s together; XGBoost depth 6 is the slowest (5.2 s). Both runs used one CPU thread.

## Validation errors: first look

L3-C10 makes 29 errors on 629 validation rows. The most frequent are direct answers predicted as retrieval (7), lookups predicted as direct answers (6), calculations predicted as direct answers (5) and direct answers predicted as calculations (4).

The brief asks for errors with and without each cue, and by source:

- **"dataset":** 35 validation rows contain it and L3-C10 makes no error on them. 33 are lookups, all predicted lookup; the one calculation and one direct answer that use it were also right.
- **"my":** 57 rows contain it, with 3 errors; the other 572 rows have 26.
- **By source:** DataBench 0 errors in 33 rows, No Robots 8 in 221, Dolly 2 in 156, MASSIVE 5 in 22, CLINC150 3 in 44, the AI drafts 3 in 6.

These counts are consistent with "dataset" acting as a lookup cue, but they do not show it. A cue test needs held-out rows that use the cue in other classes, and the release has only six. The full error inspection with interpretations is M4 work. `results/m3-5-a-report/errors.jsonl` holds validation text and stays out of Git.

## Files

All ignored and local except this note.

| File | SHA-256 |
| --- | --- |
| `results/m3-5-a/manifest.json` | `00185dcf4df70802d0903949c185768a046d50c160bd2b71448a4978ecae756f` |
| `results/m3-5-b/manifest.json` | `be6933d6a094f03e662ee3dd1cabbc6e44024f454f95b4ab19fd21091c357a86` |
| `results/m3-5-a-selection.json` | `b3009c2afc35831f33e7bd30da65505d79f4a7add623fe5c6d93f92e7a3f67e4` |
| `work/m3-5-archive/m3-5-release.zip` (2,785,613 bytes, 59 files) | `051e1a72eac78d7626700ce3fd114cb12b0c0331fcf0e8a3925a1d2b96f21ab5` |
| `data/splits/m3-5-split.json` (tracked) | `7aacbc497dd462e56a5fbcb3b5546c056ed4f835e35d0cf61334f17ce3a45e10` |

## Still open

- **Jev.** Done later on November 2 with Altan's key: the [27-configuration run](m3-5-full-run.md) collected Jev's answers, repeated both runs and the selection, and selected Jev.
- **Limits.** Altan's formal answer on the 15-minute and 2 GiB limits.
- **M4 integration.** Confidence and final-test integration of the new families, and the error interpretations.
