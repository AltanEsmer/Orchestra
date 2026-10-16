# M2 baseline runner evidence (P3)

Everything below ran on an artificial fixture (48 generated rows, source `fixture`, the same generator as the P2 tests) in a temporary directory outside the repository. **Fixture metrics are not research results.** No real data exists yet, no research run exists, and no file from this run is committed. Metrics here show only that the pipeline executes and that its numbers can be traced; the fixture's text contains its own query ID, so a classifier can read the label from the words.

## Design decisions

- B0 is `DummyClassifier(strategy="most_frequent")` behind the same TF-IDF step as L2. The dummy never reads the features; sharing the step keeps every family a `(vectorizer, classifier)` pipeline with the same fit/predict calls.
- L2 is `LogisticRegression(C=1, solver="lbfgs", l1_ratio=0.0, tol=1e-4, max_iter=100, fit_intercept=True, class_weight=None, random_state=42)`. `penalty` is not passed (deprecated in scikit-learn 1.9.1). `config.json` in each run holds the resolved parameters of both pipeline steps.
- Retry: a `ConvergenceWarning` triggers one refit of the whole family at `max_iter=1000`. Each attempt, with its warnings, stays in `outcomes.json`. Warnings that remain give status `unresolved_warning`, which the CLI reports as FAIL.
- Scores are `predict_proba` columns reordered to `LABELS` order (scikit-learn's `classes_` is alphabetical). A class missing from training would score 0. `score_type` is `probability`.
- `run` hashes `config["dataset"]` when that file exists, but never parses it, because it also contains the sealed test rows. The hash must equal the manifest's `dataset_sha256`. Provenance records the manifest's value either way.
- `config["seed"]` is the split seed and is recorded. Model seeds are the constant 42.
- Peak memory is process-wide `ru_maxrss` (bytes on macOS, kilobytes on Linux, converted to bytes). It is recorded once per run, so it cannot be attributed to a single configuration.
- The dataset hash check, partition check and run-directory refusal all happen before any model is fit.

## Live run

Thread limits were set before Python started: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`. Commands were `uv run --locked python -m orchestra ...` with `<tmp>` for the temporary directory. The fixture dataset SHA-256 is `99e9428b75b9e1d5e3cc3ae4313dcf07931b69f99226aa6b915f5415810a94cd`, and the split output was identical to the P2 evidence.

```text
$ python -m orchestra run --config <tmp>/config.json --run-id m2-a
B0: ok
L2-C1: ok
PASS: run written to <tmp>/results/m2-a
exit=0
$ python -m orchestra run --config <tmp>/config.json --run-id m2-b
B0: ok
L2-C1: ok
PASS: run written to <tmp>/results/m2-b
exit=0
$ python -m orchestra compare --left <tmp>/results/m2-a --right <tmp>/results/m2-b
PASS: runs reproduce
exit=0
$ python -m orchestra run --config <tmp>/config.json --run-id m2-a
ERROR: [Errno 17] File exists: '<tmp>/results/m2-a'
exit=1
```

The last message was reworded afterwards to `ERROR: run directory <path> already exists; pick a new run id` (covered by a test); the refusal and exit code are unchanged. The two runs were separate processes. `m2-a` contains `config.json`, `confusion.json`, `manifest.json`, `metrics.json`, `outcomes.json`, `predictions.jsonl`, `provenance.json`, `timing.json`, `warnings.json`. Both configurations had one attempt, converged, and no warnings.

### Fixture metrics (validation, 10 rows: 3, 2, 2, 3 per class in `LABELS` order)

| Configuration | Accuracy | Macro-F1 | Never predicted |
| --- | --- | --- | --- |
| B0 | 0.3 | 0.1154 | document_retrieval, knowledge_lookup, calculation |
| L2-C1 | 0.9 | 0.9143 | none |

B0 predicts `direct_answer` (the training majority, 9 of 30) for every row, so accuracy is 3/10. L2-C1 confusion counts (rows true, columns predicted, `LABELS` order): `[[3,0,0,0],[0,2,0,0],[0,0,2,0],[1,0,0,2]]`; the one error is a `direct_answer` row predicted as `document_retrieval`.

### Timing and memory (this host, fixture size only)

| Configuration | Fit seconds | Predict seconds |
| --- | --- | --- |
| B0 | 0.00125 | 0.00038 |
| L2-C1 | 0.00206 | 0.00040 |

Process peak RSS: 124,764,160 bytes (about 119 MiB), including the Python and scikit-learn imports. These are one measurement on 30 training rows. They say nothing about the real dataset and are not the planned 30-repetition latency measurement.

### Provenance recorded

Git SHA `547638128c659d9a777d5e688156263394504d04` with `git_dirty: true` (the run happened with uncommitted P3 work), Python 3.12.13, `uv 0.11.7`, scikit-learn 1.9.1, `uv.lock` SHA-256 `782a8fb7f1a52c85e3003795af93c9f5b5be04b3c40c107ad6071eb8bff5e243`, platform `macOS-27.0-arm64-arm-64bit`, 12 logical CPUs, the three thread variables as `1`, and the dataset, split manifest, train and validation file hashes. `manifest.json` lists a SHA-256 for each of the other eight files and `"complete": true`.

## Boundaries and limits

- `compare` proves two runs agree on the same host, environment and inputs. It does not prove agreement across machines or library versions.
- A dirty Git flag means the code state is not fully pinned by the SHA. A real evidence run should come from a clean commit.
- Results directories are ignored by Git. Nothing here is archived.

## Open gates

- Accepted M1 data does not exist. No B0 or L2 research number can be reported until P1's human gates (labels, review, license) pass and the research split is created.
- Inspect at least five validation errors (or all if fewer), with correct examples, and record them as hypotheses. This needs the real run.
- Restore the archived input and rerun from a clean locked environment on the same host. Preserve every run ID and explain any difference.
- Measure resources on the real split (training time, peak memory, 30-repetition prediction latency) before comparing against the proposed 15-minute and 8 GB limits.
