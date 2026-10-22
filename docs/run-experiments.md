# Prepare data and run the M1 to M3 experiments

Use this procedure from the repository root on PR #16's implementation branch.
The [data protocol](data-and-evaluation.md) defines the scientific rules.
The commands below become research runs only after the human data gates pass.

## Prepare the local environment

Run `uv python install 3.12.13`, then `uv sync --locked`.
No API key, GPU, database, or paid service is required.

Use `scripts/run_experiment.sh` for training runs.
The launcher sets `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, and `VECLIB_MAXIMUM_THREADS` to `1` before Python starts.
It runs the existing `python -m orchestra run` command through locked uv.
Relative paths resolve from the repository root, including when you invoke the launcher from another directory.
Pass `--config` and `--run-id` directly, without an extra `run` argument.

## Supply the pilot and decisions

Write 40 original English queries about fictional scenarios, initially 10 for each action.
Use `document_retrieval`, `knowledge_lookup`, `calculation`, and `direct_answer`.
Give each query a first-action rationale and a scenario group.
Keep at most four paraphrases per group.
Aim for at least five independent scenarios per class in the pilot.
Keep teaching examples out of the dataset.

You can fill the local worksheet `data/raw/pilot-intake.md` or send the same information in chat.
The agent can format your actual answers into JSONL.
The worksheet is ignored and contains no query examples or proposed human labels.

Before accepting data, supply these decisions:

- State the dataset license or explicit study-use permission and any redistribution limits. The source manifest's `license` remains `null` until you supply that record.
- Choose an independent second human or delayed blind self-review. Supply a reviewer pseudonym and availability, or the self-review interval. The existing plan proposes one week.
- Resolve ambiguous pilot boundaries before freezing guide v1. Keep the current rule that stable facts without a requested source use `direct_answer`, unless you explicitly revise the protocol.

Keep full queries and review records local. No publication decision is needed to start.
To request agent-generated candidates, explicitly change the human-authored collection plan and record their generation provenance separately.

## Validate draft rows and collect review evidence

Store pilot JSONL in `data/raw/pilot-v0.jsonl` using the nine fields in the [annotation guide](annotation-guide.md#row-format).
The local setup creates this file empty. An empty file is not accepted data.

```sh
uv run --locked python scripts/validate_dataset.py data/raw/pilot-v0.jsonl
```

Structural validation can pass an empty draft or a draft without a license.
It does not establish M1 readiness or correct labels.

Have the reviewer label at least 20% of each class without seeing your labels or rationales.
Review all ambiguous cases and every accepted row in a mixed-label group.
At the balanced 40-row pilot, the minimum sample is two rows per class, plus those additional cases.
Record the original and review labels before discussing disagreements.
Store the seven ledger fields from the [review protocol](data-and-evaluation.md#review-ledger-and-readiness) in `data/raw/reviews-v1.jsonl`.
This local file also starts empty. Do not prefill reviewer identities, dates, or agreement.
Preserve the original review decisions when you later resolve labels.
Freeze guide v1 after reviewing the pilot and relabel affected rows.

## Release the first dataset

Grow to at least 120 accepted rows, with at least 30 rows and 15 distinct groups per class.
At 30 rows per class, review at least six rows per class, plus the additional required cases.
Resolve or exclude every `needs_review` row and retain exclusion reasons.
Record your actual permission in `data/manifests/sources.json`.
Freeze the accepted version as `data/processed/m1-v1.jsonl`.
Do not create that release file from empty templates.

Run this gate before splitting:

```sh
uv run --locked python scripts/validate_dataset.py data/processed/m1-v1.jsonl --review data/raw/reviews-v1.jsonl --ready
```

Proceed only after readiness passes and you have checked label correctness and review coverage of ambiguous cases by hand.
The `split` command checks structural validity but does not enforce the complete readiness gate.
Before inspecting M2 errors, freeze the M3 collection brief with class coverage, boundary cases, wording diversity, sources, and grouping rules.
Archive the rows, ledger, guide revision, permission manifest, and validation output outside Git.
Restore into a separate local directory and compare hashes before declaring the archive verified.
The archive and restore remain pending until actual data exists.

## Run and reproduce M2

Keep the supplied paths and seed 42 in `configs/m2.json` unless a recorded project decision requires a change.
After the data gate passes, run:

```sh
uv run --locked python -m orchestra split --config configs/m2.json
scripts/run_experiment.sh --config configs/m2.json --run-id m2-a
scripts/run_experiment.sh --config configs/m2.json --run-id m2-b
uv run --locked python -m orchestra compare --left results/m2-a --right results/m2-b
```

Use new run IDs if those directories already exist. Runs refuse overwrites.
Keep the test file under `data/processed/sealed/` unopened during model selection.
Do not run `select` on M2. Selection requires all 14 M3 configurations.

## Extend the dataset and run M3

Follow the frozen collection brief to target 400 accepted rows, roughly 100 per class.
Preserve every original row's text, label, group, and partition.
Add only independent new groups, at least five new groups per class.
Collect review and permission evidence for the additions.
Freeze the expanded dataset as `data/processed/m3-v1.jsonl` and the complete review ledger as `data/raw/m3-reviews-v1.jsonl`.
Run the readiness check against those two files before extension.
The current readiness check enforces M1 minimums. Check the M3 collection target and expansion protocol separately.

Calculate the parent manifest hash after the actual M2 split exists:

```sh
shasum -a 256 data/splits/m2-split.json
```

Replace `parent_manifest_sha256: null` in `configs/m3.json` with the printed 64-character digest as a JSON string.
Leave the placeholder unset until that file exists. The agent can calculate and record the digest without another human decision.
Then run:

```sh
uv run --locked python -m orchestra extend --config configs/m3.json
scripts/run_experiment.sh --config configs/m3.json --run-id m3-a
scripts/run_experiment.sh --config configs/m3.json --run-id m3-b
uv run --locked python -m orchestra compare --left results/m3-a --right results/m3-b
uv run --locked python -m orchestra select --run results/m3-a --out results/m3-a-selection.json
uv run --locked python -m orchestra report --run results/m3-a --selection results/m3-a-selection.json --train data/processed/m3/train.jsonl --validation data/processed/m3/validation.jsonl
```

Read the comparison table and validation mistakes in `results/m3-a-report/`.
Keep validation text out of Git.
Archive complete results and provenance with the data release.
Calibration, fallback, plots, and final test evaluation are later work.
