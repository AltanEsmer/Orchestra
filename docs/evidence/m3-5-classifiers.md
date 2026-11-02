# M3.5 classifier implementation

November 2, 2026. Altan asked to recheck [issue #25](https://github.com/AltanEsmer/Orchestra/issues/25) and to implement Random Forest, Jev, Decision Tree and XGBoost. The issue is open and was last updated on October 31. Its methods checklist asks for the 27-configuration matrix, shared TF-IDF features, checks of sparse semantics and probability order, Jev access and spending checks, and selector, report and freeze integration. This note records the implementation and its checks. No M3.5 comparison ran, no new family was scored on validation, and no Jev request was sent. Accepted rows remain **400**.

## What changed

| Piece | Implementation | Plan reference |
| --- | --- | --- |
| Decision Tree | `DT`: Gini, `max_depth` 10 or 30, `min_samples_leaf` 1 or 3, seed 42. IDs `DT-d10-leaf1` to `DT-d30-leaf3`. | Section 3 |
| Random Forest | `RF`: 200 trees, `max_depth` 30 or unlimited (`dNone`), `min_samples_leaf` 1 or 3, bootstrap, `max_features="sqrt"`, seed 42, one worker. | Section 3 |
| XGBoost | `XGB`: 200 rounds, `max_depth` 3 or 6, `learning_rate` 0.05 or 0.1, `multi:softprob`, histogram trees, seed 42, one worker. | Section 3 |
| Jev | `Jev`: one pinned `jev-1.14.0` Choice question. A capped command collects validation answers; a run replays them offline. | Sections 3 and 4 |
| Matrix | A config may name `"matrix": "m3.5"`, which requires the 27 IDs and applies the tree tie rules and the order B0 to Jev. Without the key a run is `m3`, unchanged. | Sections 4 and 5 |

All local tree families read the same training-only unigram TF-IDF as L2 and S1. Each family is one entry in the `FAMILIES` table in `src/orchestra/experiment.py`. The entry lists the family's configuration keys, how to name a configuration and how to break a tie inside the family. A configuration with missing or extra keys is refused before fitting. [`configs/m3-5.json`](../../configs/m3-5.json) lists the 26 local configurations for the future expanded split. Its Jev entry needs the response log's path and hash, so it is added after collection.

## Dependency and platform

XGBoost 3.4.1 (Apache-2.0, released August 15, 2026) is pinned. On Linux the `xgboost` wheel requires `nvidia-nccl-cu13`, a GPU communication library this CPU-only plan never uses, so Linux and Windows install the `xgboost-cpu` build of the same version. The macOS wheel is CPU-only but links Homebrew's OpenMP runtime. On this Mac it failed to load until `brew install libomp` (23.1.4) ran. numpy, scipy and scikit-learn keep their locked versions; the lock gained only the two XGBoost entries.

scikit-learn ships its own OpenMP runtime, so one process now loads two. A smoke test that fitted HistGradientBoosting and XGBoost and listed thread pools ran without the duplicate-runtime abort, and so did the full suite and the pilot below (measured). A future macOS or Homebrew update could still change that.

## Verified behavior

Measured with the pinned versions:

- **Sparse semantics.** XGBoost treats an entry absent from a sparse matrix as missing, not zero. On a fixture, `predict_proba` on the CSR TF-IDF matrix equals `predict_proba` on the dense matrix with absent entries set to NaN, and the vectorizer stores no explicit zeros. An absent word therefore follows each split's learned default branch. A test keeps this fixed.
- **Labels.** XGBoost 3.4.1 rejects string labels ("Invalid classes inferred from unique values of `y`"). The `EncodedLabels` wrapper fits on integer codes and decodes predictions. Probability columns follow `LABELS` order for every family; tests check that the highest score names the prediction.
- **Determinism.** Two fixture runs of DT, RF and XGB pass `compare`.
- **M3 compatibility.** `select` on the stored `results/m3-a` run equals the stored `results/m3-a-selection.json` byte for byte; it still chooses L1-C10. A fresh rerun of `data/processed/m3-prepared.json` as `m3-compat-nov2` compared `PASS: runs reproduce` against `m3-a`. This refit the frozen M3 matrix only.

## Training-only resource pilot

The plan asks for a training-only pilot before freezing time and memory limits. `work/m3-5-models/pilot.py` (ignored) fits all 26 local configurations on the 242 M3 training rows and predicts the same rows. It never opens validation or test files, so it yields no held-out score. Apple M4 Pro, 24 GB, one thread:

| Measure | Result |
| --- | --- |
| Wall time, all 26 configurations | 2.15 seconds |
| Slowest fit | `XGB-d6-lr0.05`, 0.59 seconds |
| Random Forest fits | 0.07 to 0.09 seconds |
| Decision Tree fits | under 0.005 seconds |
| Process peak memory after the last fit | 164.8 MiB |

The expanded training partition will be about five times larger. Proposed limits for the full M3.5 run, for Altan to accept or change before it starts: 15 minutes of wall time and 2 GiB peak memory per run, one CPU thread. These are proposals, not measurements at the new size.

## Jev adapter

`src/orchestra/jev.py` holds the frozen prompt bytes. The request sends one named state field, `{"query": <unchanged text>}`, and one Choice question, `first_action`, whose options are the four labels. The instructions ask which action must come first and restate the guide's rule for several actions. The criteria paraphrase guide v2 and the M3.5 lookup rules. The calculation option says its values must be stated in the query, because figures read from a document or record are the usual confusion. The wording follows TypeSafe's own integration guidance (a plain question, descriptive option names, the confusing case named in the criteria). No validation example informed it, and no request has tested it.

TypeSafe's [model page](https://docs.typesafe.ai/models) still lists `jev-1.14.0` as the current release on November 2. Its intent-routing pattern also uses one Choice question per message. The [API reference](https://docs.typesafe.ai/api/system-one) defines the request and response fields the adapter parses.

`python -m orchestra jev --config CONFIG --log PATH --max-requests N` sends validation rows only and needs `TYPESAFE_API_KEY` in the environment. It appends each request, response, status, latency and timestamp to the log as it goes, and skips rows that already hold a valid answer. `--dry-run` sends nothing and prints the pending count with an example body. The command refuses a log path inside the repository that Git would track, because the log holds query text. A run then replays the log after checking its SHA-256, so local reruns never call the API. An answer counts only when it came from `jev-1.14.0`, its logged request equals the current request body byte for byte, and its text hash matches the query. A log collected under an older prompt therefore replays as missing answers, never as stale ones. Failure policy, frozen with the code: a failed or invalid response is re-sent only because it failed; a validation query that never gets a valid answer fails the whole Jev configuration, and the M3.5 selection stays invalid until Altan records a scope decision. The latency in a run's `timing.json` times the replay, not the network; network latency per request is in the log's `latency_seconds`.

Expected cost is small but unmeasured. The instructions and criteria hold 112 words, and the JSON body without a query is 851 characters (measured). M3 training queries average 22 words. At roughly four characters per token a request is about 240 input tokens, so one pass over about 400 validation rows is about 96,000 tokens, or $0.004 at the published $0.042 per million (inferred, not billed). Usage lands in the log.

## Open decisions

1. **Jev access (decided).** On November 2 Altan supplied a key and asked to complete M3.5. The agent took that as approval to send the validation queries, capped each pass at 700 requests, and recorded the [27-configuration run](m3-5-full-run.md).
2. **Limits.** Accept or change the proposed 15-minute and 2 GiB limits before the full run.
3. **An early look (decided).** The new families could have run on the frozen M3 validation rows now. Those rows stay in the M3.5 validation partition, so the scores would be seen before the expanded comparison. On November 2 Altan chose to wait: no new family is scored on validation before the M3.5 comparison.
4. **A decomposed Jev variant.** TypeSafe's guidance prefers several yes/no questions combined by code. Here that would mean asking whether the query names a document, a structured record or a numeric result, with the guide's order applied in code. It would be a second Jev setup, outside the plan's single one.
5. **Answers without probabilities.** The adapter treats a Choice answer without four valid probabilities as invalid, so the row is re-sent and can fail the Jev configuration. Plan section 3 instead keeps classification metrics when probabilities are missing. The stricter rule keeps every saved score usable; Altan should confirm it. The November 2 collection ran without that confirmation; every answer had four valid probabilities, so the rule excluded nothing, and it still awaits Altan's confirmation.
6. **Archive.** `archive` and `restore` do not yet copy the Jev log. A restored archive can replay Jev only where the same log, with the same hash, sits at the configured path. The November 2 archive names both Jev logs in its file list, so it replays Jev.
7. **M4 (implemented).** On November 2 confidence, freeze and final test were extended to the M3.5 decision set; see the plan's checklist and the protocol's "M4 integration" paragraph. Sending Jev the sealed test queries still needs Altan's approval.

## Reproduction

From the repository root:

```bash
sh scripts/check.sh
```

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 uv run --locked python work/m3-5-models/pilot.py
```

```bash
uv run --locked python -m orchestra compare --left results/m3-a --right results/m3-compat-nov2
```

`pilot.py` writes `pilot.json` beside itself, with the training-file hash.
