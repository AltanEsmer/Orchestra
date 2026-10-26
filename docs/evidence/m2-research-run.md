# M2 research split and baselines

On October 26, 2026, Altan said: "Start M2: run prepare-study with configs/m2.json and reviews-v2, run both baselines twice, and compare the runs. Stop before I inspect validation errors." These are the first research numbers. The [fixture record](m2-baselines.md) describes the runner design and its artificial checks.

## Split

`prepare-study` checked readiness on the frozen release and recorded the input hashes. It then wrote a grouped split with `StratifiedGroupKFold`, seed 42, five folds: three for training, one for validation, one for the sealed test.

| Partition | Rows | Groups | Retrieval | Lookup | Calculation | Direct answer |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Train | 78 | 64 | 19 | 19 | 19 | 21 |
| Validation | 25 | 22 | 6 | 7 | 6 | 6 |
| Sealed test | 25 | 22 | 6 | 6 | 7 | 6 |

| Input or output | SHA-256 |
| --- | --- |
| `data/processed/m1-v1.jsonl` | `3e02b6fa8a7c1987a44a6a9ae1c118bac768be16ad05c58d2948880b87633b2e` |
| `data/raw/reviews-v2.jsonl` | `5c449ce1f234490f351e1be7b1843346f46d9c1466136a0b14d5ddb6eb6c2de8` |
| `data/manifests/sources.json` | `67cfe73fa3517a87175ebc24f14fdbaeb2566023d1e21f58fc10b6d32c7f7420` |
| `docs/collection-brief.md` (commit `d541de9`) | `bbfa7ead97e96bcd8ed3457b97e982a3035498f318baebd2f81c90686f8dd65f` |
| `data/splits/m2-split.json` | `32a6753491078b395a57d287329b968a9c7d2cb8628e62ab5abc5477fd56bd07` |
| `data/processed/m2/train.jsonl` | `6f067779fe1a690c4e2ea4720fd814f1d92712099e245641a52abf06e641cac5` |
| `data/processed/m2/validation.jsonl` | `536d2f2904449304ab76ab24465fb8ff3eb0fc94da0bd4bffa42d6b3f79388a0` |

The split manifest holds query IDs, group IDs, and row hashes, but no query text. The collection brief is now bound to M2 by its hash.

## Baseline runs

The agent ran `scripts/run_experiment.sh` twice in separate processes, as `m2-a` and `m2-b`. Both configurations converged on the first attempt with no warnings. `compare` printed "PASS: runs reproduce". The prediction files are byte-identical (SHA-256 `6064c0b1…174d`), and so are the metric files (`1690ecd3…eb4`).

Validation results, 25 rows:

| Configuration | Correct | Accuracy | Macro-F1 | Never predicted |
| --- | ---: | ---: | ---: | --- |
| B0 (most frequent class) | 6 of 25 | 0.24 | 0.097 | retrieval, lookup, calculation |
| L2, C = 1 (TF-IDF + logistic regression) | 18 of 25 | 0.72 | 0.730 | none |

B0 always predicts `direct_answer`, the training majority (21 of 78).

L2 per-class F1:
- Retrieval: 0.80
- Lookup: 0.71
- Calculation: 0.83
- Direct answer: 0.57

L2 confusion counts (rows are true labels, columns are predictions, both in the order retrieval, lookup, calculation, direct answer):

| True \ predicted | Retrieval | Lookup | Calculation | Direct answer |
| --- | ---: | ---: | ---: | ---: |
| Retrieval | 4 | 0 | 0 | 2 |
| Lookup | 0 | 5 | 1 | 1 |
| Calculation | 0 | 0 | 5 | 1 |
| Direct answer | 0 | 2 | 0 | 4 |

Six of the seven errors involve `direct_answer`, either as the prediction or as the true label. These are counts, not explanations. Altan inspects the individual errors next.

## Resources, this host

| Configuration | Fit seconds | Median latency, 25-row batch (30 repetitions) |
| --- | ---: | ---: |
| B0 | 0.0040 | 0.00025 s |
| L2, C = 1 | 0.0067 | 0.00030 s |

Process peak memory was 122,863,616 bytes, about 117 MiB, including imports. This is far below the proposed 15-minute and 8 GB limits.

## Limits

- **Small sample.** With 25 validation rows, one row moves accuracy by 0.04, and per-class F1 rests on six or seven rows. These numbers describe this split only. They are not the M3 comparison.
- **Dirty tree in provenance.** Provenance records commit `d541de9` with `git_dirty: true`. The only change was the new, then-untracked `data/splits/m2-split.json` written by `prepare-study`. Its hash is recorded above. Altan then asked to track it, and the committed file has the same hash.
- **Sealed test.** The runner did not open the sealed test file. Nobody has looked at the test predictions, because none exist.
- **Not done.** The M2 inputs have not been archived and restored. Error inspection is Altan's next step. `select` is not run on M2.

Results stay in ignored `results/m2-a/` and `results/m2-b/`, and the prepared config in ignored `data/processed/m2-prepared.json`.
