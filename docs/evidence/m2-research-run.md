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

Six of the seven errors involve `direct_answer`, either as the prediction or as the true label. These are counts, not explanations. Altan's reading of the individual errors follows.

## Error inspection

On October 26, 2026, the agent showed Altan the seven L2 errors and nine correct validation rows with their predicted probabilities. Altan wrote five exploratory hypotheses. His full text is in the [learning log](../learning-log.md#m2-error-hypotheses-october-26-2026).

1. L2 may react to how reference text is introduced. Both wrong Dolly rows say "Based on this paragraph". The correct ones say "Given this paragraph" or "Given a reference text".
2. Small winning margins could be treated as uncertainty in M4. Close correct rows mean this is a reason to test uncertainty handling, not to pick a threshold.
3. Explicit cues such as "table" or "fictional" may help, but they are neither necessary nor sufficient.
4. L2 may blur needing a particular external record with asking for factual information.
5. Source wording or class composition may contribute. That would need source totals to check.

He noted that the identical m2-a and m2-b results show repeatability, not independent confirmation.

The agent then checked the hypotheses against saved outputs and training text. These are measurements on this split, not explanations:

| Check | Result |
| --- | --- |
| Exact top-two margins of the errors | q0044 0.038, q0047 0.085, q0069 0.067, q0084 0.011, q0090 0.010, q0117 0.014, q0130 0.009 |
| Margin ranking, all 25 rows | The four smallest margins (0.009–0.014) are all errors. The next two (q0045 0.020, q0048 0.027) are correct. The remaining errors rank 8th, 11th, and 13th. |
| "Based on this paragraph" in training | 0 rows. "Given this paragraph" appears in 2 retrieval rows. "paragraph" appears in 3 retrieval and 2 direct-answer rows. |
| Errors by source, validation | Altan-authored 0 of 5; Dolly 2 of 5; BFCL 3 of 10; No Robots 2 of 5 |
| Source and label in training | No Robots rows are all direct answer (14), Dolly rows all retrieval (13). BFCL covers calculation (12) and lookup (11). Altan-authored rows cover all four classes. |

Because each public source except BFCL maps to one class in training, source style and label cannot be separated in this data. The collection brief's second-source rule addresses that confound for M3. The margin pattern is a validation observation. Any threshold chosen by looking at these 25 rows would be fitted to them, so M4 must choose confidence handling by its own protocol.

Seeing these errors is human exposure. Under the [collection brief](../collection-brief.md#what-not-to-do), M3 rows must not be collected, selected, or relabeled to target them, and the report must disclose that the inspection happened before collection.

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
- **Archive.** On October 28 the M2 inputs and runs were archived, restored into a new directory, and rerun from a fresh locked environment. The rerun reproduced `m2-a` byte for byte ([record](m1-m2-archive.md)).
- **Not done.** `select` is not run on M2.

Results stay in ignored `results/m2-a/` and `results/m2-b/`, and the prepared config in ignored `data/processed/m2-prepared.json`.
