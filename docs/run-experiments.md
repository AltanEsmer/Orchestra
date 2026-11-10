# Prepare data and run the required study

Use this procedure from the repository root. The agent can execute these steps after each human prerequisite is satisfied.
The [data protocol](data-and-evaluation.md) defines the scientific rules.
The commands below become research runs only after the human data gates pass.

## Prepare the local environment

Run `uv python install 3.12.13`, then `uv sync --locked`.
On macOS, run `brew install libomp` once so XGBoost can load its OpenMP runtime.
No GPU or database is required. Only the optional Jev collection needs an API key and a paid service.

Use `scripts/run_experiment.sh` for training runs.
The launcher sets `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, and `VECLIB_MAXIMUM_THREADS` to `1` before Python starts.
It runs the existing `python -m orchestra run` command through locked uv.
Relative paths resolve from the repository root, including when you invoke the launcher from another directory.
Pass `--config` and `--run-id` directly, without an extra `run` argument.

## Supply the pilot and decisions

Write 40 original English queries about fictional scenarios, initially 10 for each action.
Use `document_retrieval`, `knowledge_lookup`, `calculation`, and `direct_answer`.
Give each query a first-action rationale and a shared-request-template group under guide v1.
Keep at most four paraphrases per group.
Aim for at least five independent scenarios per class in the pilot.
Keep teaching examples out of the dataset.

You can fill the local worksheet `data/raw/pilot-intake.md` or send the same information in chat.
The agent can format your actual answers into JSONL.
The worksheet is ignored and now preserves forty actual queries with Altan's original labels and rationales. Keep it hidden from a blind reviewer.

Before accepting data, supply these decisions:

- The permission for q0001–q0040 is already recorded. Preserve it and record separate source-specific licenses before adopting any public supplement.
- The selected method is single-human annotation with disclosed AI checks. Preserve original human labels and separately record AI evidence; collect actual human decisions for flagged cases.
- Resolve ambiguous pilot boundaries before freezing guide v1. Keep the current rule that stable facts without a requested source use `direct_answer`, unless you explicitly revise the protocol.

Keep full queries and review records local. No publication decision is needed to start.
To request agent-generated candidates, explicitly change the human-authored collection plan and record their generation provenance separately.

## Validate draft rows and collect review evidence

Current local state, October 26: the pilot and `data/raw/reviews-v1.jsonl` contain 38 accepted pilot rows after Altan excluded q0014 and q0037 for practice. The legacy `pilot-v0.jsonl` path is retained for callers; each row’s `annotation_version` is `guide-v2` after the October 26 regrouping. Separate ignored `data/raw/pilot-audit-2026-10-25.jsonl` and `data/raw/reviews-audit-2026-10-25.jsonl` preserve all forty IDs at that dated snapshot, with later decisions retained separately. The audit preserves the five-member semantic g005 family and is not a release input for the four-row-cap validator. Keep practice rows outside supervised splits and report both exclusions. The [pilot record](evidence/pilot-guide-v1.md) has current hashes and counts. The guide-v2 [import](evidence/public-import-v2.md) added 90 public rows in ignored `data/raw/m1-v2.jsonl` (with the pilot) and `data/raw/import-v2/`. All 128 were accepted and frozen on October 26 as read-only `data/processed/m1-v1.jsonl`, with the read-only ledger `data/raw/reviews-v2.jsonl` ([review record](evidence/public-review-v2.md)).

Store pilot JSONL in `data/raw/pilot-v0.jsonl` using the nine fields in the [annotation guide](annotation-guide.md#row-format).
The current pilot contains 38 accepted guide-v1 rows with original human labels and rationales preserved. Pilot validity is not M1 release readiness.

```sh
uv run --locked python scripts/validate_dataset.py data/raw/pilot-v0.jsonl
```

Structural validation can pass an empty draft or a draft without a license.
It does not establish M1 readiness or correct labels.

Have the AI reviewer check at least 20% of each class without seeing your original labels or rationales.
Review all ambiguous cases and every accepted row in a mixed-label group.
At the balanced 40-row pilot, the minimum sample is two rows per class, plus those additional cases.
Record the original and review labels before discussing disagreements.
Store the common ledger fields plus required `ai_evidence` and `human_adjudication` fields from the [review protocol](data-and-evaluation.md#review-ledger-and-readiness) in a review ledger. The pilot used `data/raw/reviews-v1.jsonl`; the M1 release uses `data/raw/reviews-v2.jsonl`, which keeps the 38 pilot entries and adds the 90 import entries.
The ledger records actual AI output and genuine human adjudications only. Do not invent identities, dates, or decisions. An unresolved AI disagreement or flag blocks readiness; clear matches can retain original human labels.
Preserve the original review decisions when you later resolve labels.
Guide v1 is frozen after the completed pilot review. Apply it to new candidates; revise it only under a new recorded version.

## Release the first dataset

Grow to at least 120 accepted rows, with at least 30 rows and 15 distinct groups per class.
At 30 rows per class, review at least six rows per class, plus the additional required cases.
Resolve or exclude every `needs_review` row and retain exclusion reasons.
Record your actual permission in `data/manifests/sources.json`.
Freeze the accepted version as `data/processed/m1-v1.jsonl`.
Do not create that release file from empty templates.

Run this gate before splitting:

```sh
uv run --locked python scripts/validate_dataset.py data/processed/m1-v1.jsonl --review data/raw/reviews-v2.jsonl --ready
```

Proceed only after readiness passes and you have checked label correctness and review coverage of ambiguous cases by hand.
The `split` command checks structural validity but does not enforce the complete readiness gate.
Before inspecting M2 errors, freeze the M3 collection brief with class coverage, boundary cases, wording diversity, sources, and grouping rules.
Archive the rows, ledger, guide revision, permission manifest, and validation output outside Git.
Restore into a separate local directory and compare hashes before declaring the archive verified.
The October 28 [archive record](evidence/m1-m2-archive.md) did this for `m1-v1` and the M2 inputs. The ignored local script `work/m2-archive/run.sh` repeats it on this machine.

## Run and reproduce M2

Keep the supplied paths and seed 42 in `configs/m2.json` unless a recorded project decision requires a change.
After the data gate passes, run:

```sh
uv run --locked python -m orchestra prepare-study --config configs/m2.json --review data/raw/reviews-v2.jsonl --collection-brief docs/collection-brief.md --out data/processed/m2-prepared.json
scripts/run_experiment.sh --config data/processed/m2-prepared.json --run-id m2-a
scripts/run_experiment.sh --config data/processed/m2-prepared.json --run-id m2-b
uv run --locked python -m orchestra compare --left results/m2-a --right results/m2-b
```

Use new run IDs if those directories already exist. Runs refuse overwrites.
Keep the test file under `data/processed/sealed/` unopened during model selection.
Do not run `select` on M2. Selection requires all 14 M3 configurations.

## Extend the dataset and run M3

Follow the frozen collection brief to target 400 accepted rows, roughly 100 per class.
The October 28 [candidate import](evidence/m3-import.md) holds the candidates, the fill rule, and the local worksheet path.
Preserve every original row's text, label, group, and partition.
Add only independent new groups, at least five new groups per class.
Collect review and permission evidence for the additions.
Freeze the expanded dataset as `data/processed/m3-v1.jsonl` and the complete review ledger as `data/raw/m3-reviews-v1.jsonl`.
Run the readiness check against those two files before extension.
The current readiness check enforces M1 minimums. Check the M3 collection target and expansion protocol separately.

The agent runs `prepare-study` to validate the expanded rows and review ledger, record the collection-brief hash, and calculate the actual parent manifest hash. The original tracked config remains a reusable template. A supplied non-null parent hash must match.
Then run:

```sh
uv run --locked python -m orchestra prepare-study --config configs/m3.json --review data/raw/m3-reviews-v1.jsonl --collection-brief docs/collection-brief.md --out data/processed/m3-prepared.json
scripts/run_experiment.sh --config data/processed/m3-prepared.json --run-id m3-a
scripts/run_experiment.sh --config data/processed/m3-prepared.json --run-id m3-b
uv run --locked python -m orchestra compare --left results/m3-a --right results/m3-b
uv run --locked python -m orchestra select --run results/m3-a --out results/m3-a-selection.json
uv run --locked python -m orchestra report --run results/m3-a --selection results/m3-a-selection.json --train data/processed/m3/train.jsonl --validation data/processed/m3/validation.jsonl
```

Read the comparison table and validation mistakes in `results/m3-a-report/`.
Keep validation text out of Git.
Archive complete results and provenance with the data release.
Use the following commands for confidence, freezing, final evaluation, and plots after the real M3 artifacts exist.

## Run the M3.5 classifier comparison

The M3.5 release and its extended split exist since November 2 ([record](evidence/m3-5-dataset.md)): `prepare-study --config configs/m3-5.json --review data/raw/m3-5-reviews-v1.jsonl --collection-brief docs/collection-brief-m3-5.md --out data/processed/m3-5-prepared.json` wrote `data/processed/m3-5-prepared.json`. Check the release with `check-collection` as that record shows. Runs `m3-5-a` and `m3-5-b` of the 26 local configurations, their comparison, selection, report and the restored-archive rerun are recorded in the [M3.5 run record](evidence/m3-5-research-run.md); `work/m3-5-archive/run.sh` repeats the archive check on this machine.
[`configs/m3-5.json`](../configs/m3-5.json) names `"matrix": "m3.5"` and the 26 local configurations.
Check the Jev request without sending anything:

```sh
uv run --locked python -m orchestra jev --config data/processed/m3-5-prepared.json --log results/jev/m3-5-validation.jsonl --max-requests 1 --dry-run
```

Only after Altan approves the spending cap and sending validation queries to TypeSafe, export `TYPESAFE_API_KEY` in the shell and collect answers. Never print the key or write it to a file in the repository.
The command sends validation rows only, stops at the cap and appends every request and response to the ignored log.
Rerun it to fill rows whose request failed; answered rows are never sent again.

```sh
uv run --locked python -m orchestra jev --config data/processed/m3-5-prepared.json --log results/jev/m3-5-validation.jsonl --max-requests 700
```

Copy the prepared config to `data/processed/m3-5-prepared-jev.json` and add `{"family": "Jev", "responses": "results/jev/m3-5-validation.jsonl", "responses_sha256": "<printed hash>"}` to its configurations, so the 26-configuration input stays unchanged.
Then run, compare, select and report with new run IDs:

```sh
scripts/run_experiment.sh --config data/processed/m3-5-prepared-jev.json --run-id m3-5-full-a
scripts/run_experiment.sh --config data/processed/m3-5-prepared-jev.json --run-id m3-5-full-b
uv run --locked python -m orchestra compare --left results/m3-5-full-a --right results/m3-5-full-b
uv run --locked python -m orchestra select --run results/m3-5-full-a --out results/m3-5-full-a-selection.json
uv run --locked python -m orchestra report --run results/m3-5-full-a --selection results/m3-5-full-a-selection.json --train data/processed/m3-5/train.jsonl --validation data/processed/m3-5/validation.jsonl
```

A run replays the log offline and fails the Jev configuration if any validation query lacks a valid answer.
The selection is invalid until all 27 configurations are `ok`.
For a repeat that measures how much Jev's answers vary, collect into a second log such as `results/jev/m3-5-validation-repeat.jsonl`; `work/m3-5-archive/run-full.sh` archives both logs and repeats the restored rerun with all 27 configurations.
This was done on November 2 with Altan's key; the [27-configuration record](evidence/m3-5-full-run.md) holds the outputs.

## Prepare blind review

After draft rows pass structural validation, generate the reviewer worksheet:

```sh
uv run --locked python -m orchestra prepare-review --dataset data/raw/pilot-v0.jsonl --out data/raw/pilot-blind-review
```

Give the reviewer only `reviewer.jsonl`. Keep `steward.json` hidden until the reviewer has recorded independent labels. The command samples 20 percent per accepted class and includes mixed-label groups and unresolved rows. Repeat `--extra-id QUERY_ID` for additional known ambiguous cases. A human must still identify ambiguity and related scenarios that code cannot infer.

The agent can convert the returned human answers into the existing review ledger. It cannot supply reviewer identities, actual review dates, independent labels, or adjudication on Altan's behalf.

## Analyze confidence and record interpretations

Run the new commands under the same single-thread environment as training:

```sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
uv run --locked python -m orchestra confidence --run results/m3-a --selection results/m3-a-selection.json --out results/m4-validation
```

Research confidence requires the evidence written by `prepare-study`. The command verifies the saved M3 environment, refits every selected family on training only, and checks raw validation reproduction before calibration. It selects the logistic family by the recorded validation tolerance and family order. Its full pipeline is calibrated with sigmoid models on three grouped training folds. A class shortage or unresolved convergence warning produces saved diagnostics and a nonzero exit code. It blocks freezing.

Inspect at least 20 selected-system validation errors, or all if fewer exist, across true and predicted classes. Include correct comparisons. The agent can perform this inspection and propose explanations as hypotheses. Discuss questionable labels with Altan. Store the completed interpretations separately at `results/validation-interpretations.jsonl`, leaving the original prediction artifacts unchanged. Each row contains:

```json
{"configuration":"L2-C1","query_id":"ACTUAL_QUERY_ID","category":"vocabulary_mismatch","hypothesis":"A reasoned interpretation tied to the actual observed query."}
```

This is a format example, not a completed interpretation. The configuration and ID must match actual selected-system validation predictions. Allowed categories are `annotation_ambiguity`, `missing_context`, `vocabulary_mismatch`, `negation`, `multi_action_dependencies`, `out_of_scope`, and `other`. A correct comparison can use `other`. The freeze checks coverage and required fields, not the truth of an interpretation.

## Freeze decisions and evaluate once

```sh
uv run --locked python -m orchestra freeze --confidence results/m4-validation --error-review results/validation-interpretations.jsonl --out results/frozen-study.json
uv run --locked python -m orchestra final-test --freeze results/frozen-study.json --out results/final-test
```

Freeze binds selected systems, exact inputs and code, calibration folds, validation fallback choice, and the interpretation ledger. Do not edit those inputs afterward. No qualifying threshold is a valid recorded outcome. The final command evaluates all frozen family winners and calibrated logistic probabilities. It applies only the already selected threshold to test predictions.

### M3.5 decision set

For M3.5, run the same chain on the 27-configuration run. Freeze also needs `--jev-test-log` when the selection includes Jev. The path must be ignored by Git and must not exist yet, because Jev's test answers may come only from `final-test`:

```sh
uv run --locked python -m orchestra confidence --run results/m3-5-full-a --selection results/m3-5-full-a-selection.json --out results/m4-5-validation
uv run --locked python -m orchestra freeze --confidence results/m4-5-validation --error-review results/validation-interpretations-m3-5.jsonl --jev-test-log results/jev/m3-5-test.jsonl --out results/frozen-study-m3-5.json
uv run --locked python -m orchestra final-test --freeze results/frozen-study-m3-5.json --out results/final-test-m3-5 --send-jev-test
```

`--send-jev-test` sends the sealed test queries to TypeSafe and needs `TYPESAFE_API_KEY`. Run it only after Altan approves sending the test text. Without the flag, a Jev decision set is refused before any receipt is written. The log's folder must exist. Inside the reservation the command sends each unanswered test query at most once, logs every response, and stops with a resumable receipt if any query lacks a valid answer. A rejected key (401 or 403) stops after one request. `--resume` then sends only the missing queries, and refuses if the log changed since the last attempt. `confidence` writes `systems.json`: each chosen system's score type, validation metrics and calibration. Only the chosen logistic system is recalibrated. The tree families and Jev keep their own probabilities, and S1's margins get classification metrics only.

The canonical research receipt lives under `results/test-receipts/` and is keyed by split hash. Repeating an identical completed request verifies and returns its existing artifacts. A changed freeze or output location is refused. For an identical request that recorded a failure, add `--resume`. The command preserves failed attempts and partial output before retrying. Never delete a receipt to try a new model on exposed test data. An exact interrupted request can also resume after its process exits. A split-specific POSIX file lock excludes active evaluations; the operating system releases it on process exit. Receipt updates are atomic, and every resumed attempt stays in history. This recovery currently targets macOS and Linux.

`--fixture` on confidence is only for artificial software verification. It bypasses research evidence gates, marks artifacts as fixtures, and uses an isolated fixture receipt store. Never use it to bypass missing real review or permission.

### Interpret test mistakes after the freeze

Test mistakes are read only after `final-test` completes. Write their hypotheses to a separate ignored ledger in the validation ledger's format, then check it against the sealed test predictions:

```sh
uv run --locked python -m orchestra test-review --final-test results/final-test-m3-5 --interpretations results/test-interpretations-m3-5.jsonl
```

The command first verifies the final-test files against that directory's manifest. It then applies the freeze's coverage rule to every system named in the ledger: each row must name a real test prediction once, use an allowed category, and the ledger must cover at least min(20, all errors) plus a correct comparison. It checks only the systems the ledger names, so state which systems were reviewed. It prints the interpreted errors and category counts per system. It never changes the frozen selection or any final-test artifact. The manifest vouches only for itself; the test receipt's `result_manifest_sha256` is what ties it to the one sealed run, so compare that hash with the manifest's SHA-256 when reporting.

## Render saved evidence

```sh
uv run --locked python -m orchestra figures --run results/m3-a --selection results/m3-a-selection.json --train data/processed/m3/train.jsonl --validation data/processed/m3/validation.jsonl --confidence results/m4-validation --final results/final-test --out results/figures
```

Omit `--final` before final evaluation. Omit both optional artifact directories for M3-only figures. The renderer verifies hashes and exports SVG/PNG figures plus exact numeric inputs, per-figure source records, and a checksum manifest. It does not fit a model or open sealed source rows. Use a fresh output directory. The report source template is `report/main.tex`.

## Back up and reproduce

Create a JSON array of exact repository-relative regular-file paths at `work/archive-files.json`. Include the tracked source, Python/lock files, launcher, prepared configs, permitted local rows, sources/review ledger, collection brief, split manifests, complete runs, confidence/freeze/final artifacts, receipts, and figure source records. Include the files needed by any absolute references in configs. Do not include `.venv`, secrets, or course PDFs. The backup is local-only; distribution permission is a separate human decision. Keep the final report and study PDFs separately.

```sh
uv run --locked python -m orchestra archive --files work/archive-files.json --out work/study-backup.zip
uv run --locked python -m orchestra restore --archive work/study-backup.zip --out work/restored-study
```

The restore verifies member hashes and safe paths before writing a new directory, and preserves executable modes. Save the printed archive checksum. Reproduction also requires execution. In the restored directory, run `uv sync --locked`, create a new run config with relocated paths, and rerun training with a fresh ID. Compare the new run to the saved original. Keep content and lineage hashes unchanged. Do not use live test data for another selection. The agent handles the path relocation.

### Reproduce the reported study from a clean clone

The M3.5 and M4 study behind the report has committed scripts for this sequence. Build the archive from the checkout that holds the data, then run the reproduction inside a fresh clone:

```sh
scripts/archive_study.sh /path/to/data-checkout /path/to/orchestra-study.zip
git clone https://github.com/AltanEsmer/Orchestra.git clean && cd clean
scripts/reproduce_study.sh /path/to/orchestra-study.zip
```

`archive_study.sh` packs the ignored release, review evidence, Jev logs, interpretation ledgers and every saved output, and prints the archive SHA-256. `reproduce_study.sh` refuses a checkout with changes or saved results. It restores the archive into `work/m6-reproduction/original`, copies only the inputs into place, and runs the commands of this runbook from `validate_dataset.py --ready` to `figures` with run ID `m6-repro`. The final test uses `--replay-jev-test`: it reads Jev's archived test answers at the frozen log path and never sends a query. `scripts/compare_study.py` then compares splits, predictions, metrics, confidence, the freeze, the final test and all figures with the originals, and prints each expected difference with its reason. The log is `work/m6-reproduction/reproduce.log`. The November 10 run is recorded in the [M6 reproduction record](evidence/m6-reproduction.md).

`--replay-jev-test` is for reproduction only. In the checkout that opened the test, the completed receipt refuses any replay to a new output path.

To trace a new query through the frozen logistic system for oral practice, run `uv run --locked python scripts/route_query.py "your query"`. It refits the frozen configuration and calibration as the final test did, then prints both probability rows, the fallback decision, the strongest n-grams, and each word outside the model's capped vocabulary with the number of training rows that contain it. Jev is not routed.

The committed `scripts/verify_workflow.py` demonstrates this entire sequence with artificial rows and a clean restored environment. It is a software acceptance check, not the real study or a substitute for its archive.
