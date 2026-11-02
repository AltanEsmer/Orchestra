# M3.5 research run: all 27 configurations

Run November 2, 2026, on the [M3.5 release](m3-5-dataset.md) `m3-5-v1`, from a branch of `main` after [PR #28](https://github.com/AltanEsmer/Orchestra/pull/28) merged (merge commit `031e4e9`). Altan wrote "Create and merge PR for dataset updates and then complete m3.5" and pointed to a local file holding a TypeSafe key. The agent read that as approval to send the M3.5 validation queries to TypeSafe. Altan named no spending cap, so the agent capped each pass at 700 requests: at the measured mean of 504 input tokens per request, at most about $0.015 per pass at the published price. This completes the [first run](m3-5-research-run.md), which had no Jev outcome. It is a validation-only comparison: the sealed test was not opened.

## Jev collection

**Model check.** TypeSafe's [models page](https://docs.typesafe.ai/models), read November 2, lists `jev-1.14.0` as the newest release (available from October 14) and the target of the `jev-latest` alias. It lists input tokens at $0.042 per million, with output tokens free. It publishes no request-rate figure. The adapter's pinned model and frozen prompt in `src/orchestra/jev.py` were used unchanged.

**What was sent.** Each request held one validation query as `{"query": <unchanged text>}` with the frozen first-action question. Two passes were sent, each covering all 629 validation rows. No label, rationale, attachment or source metadata was sent. By source the rows are:

- **Public corpora:** No Robots 221, Dolly 156, GSM8K 51, CLINC150 44, DataBench 33, BFCL 30, MASSIVE 22, ToolAlpaca 22, TheoremQA 15, ToolACE 14 and oasst2 10.
- **M3 local rows:** 6 AI drafts and 5 authored by Altan.

The protocol already excludes personal queries. TypeSafe's terms govern what it does with the text. Whether its pretraining saw these public corpora is unknown.

**Key handling.** Each command read the key from Altan's local file into `TYPESAFE_API_KEY` for that process only. It is not in Git, configs, logs or this note. One disclosure: the agent's first look at the file, meant to list variable names only, printed the key line into the local session transcript, because the file does not use the `NAME=value` form the filter expected. The agent told Altan and advised rotating the key.

| Pass | Requests | Valid answers | Errors or retries | Input tokens | Network latency, median / p95 / max |
| --- | ---: | ---: | ---: | ---: | --- |
| Smoke test (first 3 rows, part of the main log) | 3 | 3 | 0 | 1,446 | |
| Main (`results/jev/m3-5-validation.jsonl`) | 629 in total | 629 | 0 | 317,282 | 0.197 / 0.264 / 0.456 s |
| Repeat (`results/jev/m3-5-validation-repeat.jsonl`) | 629 | 629 | 0 | 317,282 | 0.199 / 0.263 / 0.464 s |

The two passes used 634,564 input tokens in total, about $0.027 at the published price. That figure is inferred: the agent did not see a bill. Every answer had four valid probabilities, so the stricter rule in open decision 5 of the [implementation record](m3-5-classifiers.md) excluded nothing.

**Repeat agreement.** The repeat pass asked the same questions again on the same day. Two of the 629 top choices changed: q2851 and q3049, both retrieval rows with a top probability between 0.50 and 0.57. One flip turned a correct answer wrong and the other turned a wrong answer right, so the repeat log also scores macro-F1 0.975. 351 of the 629 probability vectors are identical, and no probability moved by more than 0.09. This repeat measures how much the API's answers vary. It is not an independent reproduction, and replaying the saved log only proves the log is intact.

## Commands

```sh
uv run --locked python -m orchestra jev --config data/processed/m3-5-prepared.json --log results/jev/m3-5-validation.jsonl --max-requests 3
uv run --locked python -m orchestra jev --config data/processed/m3-5-prepared.json --log results/jev/m3-5-validation.jsonl --max-requests 700
uv run --locked python -m orchestra jev --config data/processed/m3-5-prepared.json --log results/jev/m3-5-validation-repeat.jsonl --max-requests 700
scripts/run_experiment.sh --config data/processed/m3-5-prepared-jev.json --run-id m3-5-full-a
scripts/run_experiment.sh --config data/processed/m3-5-prepared-jev.json --run-id m3-5-full-b
uv run --locked python -m orchestra compare --left results/m3-5-full-a --right results/m3-5-full-b
uv run --locked python -m orchestra select --run results/m3-5-full-a --out results/m3-5-full-a-selection.json
uv run --locked python -m orchestra report --run results/m3-5-full-a --selection results/m3-5-full-a-selection.json --train data/processed/m3-5/train.jsonl --validation data/processed/m3-5/validation.jsonl
sh work/m3-5-archive/run-full.sh
```

`data/processed/m3-5-prepared-jev.json` (ignored) is the prepared config from `prepare-study` with one entry added: `{"family": "Jev", "responses": "results/jev/m3-5-validation.jsonl", "responses_sha256": "1f68d2f3534c2d5649f80f2caabef0eda2ddd6a37f28390b59858e0dc566f839"}`. A separate file keeps the first run's input byte for byte. The environment and thread settings match the [first run](m3-5-research-run.md).

Actual outputs:

- **Collection:** each pass exited 0 with `"missing": 0`.
- **Runs:** both runs reported all 27 configurations `ok`.
- **`compare`:** `PASS: runs reproduce`.
- **`select`:** `PASS: overall Jev`, with `valid: true`, `complete_matrix: true` and nothing missing.
- **`report`:** `PASS: report written to results/m3-5-full-a-report`.
- **Archive check:** `work/m3-5-archive/run-full.sh` printed `PASS: 62 restored files byte-identical to originals`. After a fresh `uv sync --locked` in the restored copy, the 27-configuration rerun, with Jev replaying its archived log, printed `PASS: runs reproduce` against `m3-5-full-a`. The script is the first run's archive script with three changes: the Jev logs, the Jev config and the new runs are added to the file list; the restored rerun reads the Jev config; and the rerun is wrapped in `time`.
- **Local scores:** the 26 local configurations' metrics equal those of `m3-5-a` exactly.

## Validation results

The rules are the frozen ones: within a family, the tie set lies within 0.01 macro-F1 of the best, inclusive, and the family's tie rule picks from it. Overall, the order B0, B1, L1, L2, S1, L3, DT, RF, XGB, Jev applies among winners within 0.01 of the best winner.

| Family | Winner | Macro-F1 | Accuracy |
| --- | --- | ---: | ---: |
| B0 | B0 | 0.121 | 0.318 |
| B1 | B1 | 0.878 | 0.874 |
| L1 | L1-C1 | 0.922 | 0.925 |
| L2 | L2-C1 | 0.924 | 0.925 |
| S1 | S1-C1 | 0.936 | 0.938 |
| L3 | L3-C10 | 0.952 | 0.954 |
| DT | DT-d30-leaf1 | 0.818 | 0.828 |
| RF | RF-dNone-leaf1 | 0.913 | 0.917 |
| XGB | XGB-d6-lr0.05 | 0.901 | 0.908 |
| **Jev** | **Jev** | **0.975** | **0.973** |

Jev's 0.975 is 0.023 above L3-C10's 0.952. No other family winner falls within 0.01 of it, so the order that favors local models has nothing to break, and **the overall selection is Jev**. Jev's per-class F1 is calculation 0.996, lookup 0.975, retrieval 0.967 and direct answer 0.963. L3-C10's is retrieval 0.975, calculation 0.954, lookup 0.943 and direct answer 0.938. These are observed validation scores on one split, not test results.

### By row origin

The validation partition keeps M3's 79 validation rows, which were labeled under guide v2 with Altan's primary label and a blind AI check. Its 550 new rows were labeled under guide v3 by an AI screen and an independent blind AI check, with Altan adjudicating disagreements ([release record](m3-5-dataset.md)).

| System | All 629 | 79 M3 rows | 550 new rows |
| --- | ---: | ---: | ---: |
| Jev | 0.975 | 0.962 | 0.978 |
| L3-C10 | 0.952 | 0.938 | 0.956 |
| S1-C1 | 0.936 | 0.900 | 0.943 |
| RF-dNone-leaf1 | 0.913 | 0.849 | 0.925 |
| XGB-d6-lr0.05 | 0.901 | 0.888 | 0.905 |

Macro-F1. Jev leads in both groups. On the 79 rows with human primary labels its lead over L3-C10 amounts to about two rows.

### Errors

Jev makes 17 errors on 629 rows and L3-C10 makes 29. Only one row is wrong for both.

| True label | Jev's wrong predictions |
| --- | --- |
| Retrieval | 10 predicted as direct answer |
| Lookup | 2 as retrieval, 1 as direct answer |
| Calculation | 1 as direct answer |
| Direct answer | 2 as lookup, 1 as retrieval |

By source, Jev's errors fall on these rows; every other source has none:

| Source | Errors / rows |
| --- | ---: |
| No Robots | 10 / 221 |
| Dolly | 3 / 156 |
| AI drafts | 2 / 6 |
| TheoremQA | 1 / 15 |
| ToolACE | 1 / 14 |

The No Robots and Dolly retrieval errors fit the attachment rule. The passage stays outside router text, so a query that refers to it only weakly reads like a general question. That is a hypothesis, not an inspected finding.

The brief's cue counts:

- **"dataset":** 35 rows, with one Jev error and none for L3-C10.
- **"my":** 57 rows, with two Jev errors and three for L3-C10.

`results/m3-5-full-a-report/errors.jsonl` holds the error texts and stays out of Git.

### Probability diagnostics

These are validation-only diagnostics, not M4's calibration analysis. S1 produces margins, not probabilities, so it is left out.

| System | Brier score (lower is better) | 10-bin ECE | Mean top probability | Accuracy |
| --- | ---: | ---: | ---: | ---: |
| Jev | 0.059 | 0.049 | 0.924 | 0.973 |
| L3-C10 | 0.096 | 0.100 | 0.854 | 0.954 |
| RF-dNone-leaf1 | 0.215 | 0.236 | 0.681 | 0.917 |
| XGB-d6-lr0.05 | 0.140 | 0.041 | 0.871 | 0.908 |

Jev's probabilities are underconfident on this set: its mean top probability, 0.92, sits below its accuracy, 0.97. No true class received probability zero. Jev's separate `confidence` field was saved and not used, as the plan requires.

## Resources

Altan has not formally answered the proposed limits of 15 minutes and 2 GiB per run, so they were applied as proposed.

| Measure | Result |
| --- | --- |
| Peak resident memory, `m3-5-full-a` / `m3-5-full-b` | 323.6 / 324.4 MiB (`timing.json`) |
| Restored-archive rerun, 27 configurations: the `run_experiment.sh` step after `uv sync` | 30.0 s (terminal `time` output, not saved to a file) |
| Jev replay inside a run | fit 0.005 s; median latency 0.27 ms for the 629-row batch |
| Jev over the network | 0.197 s median per query |

The wall times of `m3-5-full-a` and `m3-5-full-b` were not captured, so this note does not report them. The 26 local fits are the same as in the first run, about 22 s per run. The replay latency measures reading saved answers. Serving Jev live would cost one network round trip per query, plus the API price.

## What the result means

Under the rules frozen before any M3.5 score, Jev is the validation-selected system, ahead of the best local model by 0.023 macro-F1. Limits that bear on that reading:

- **Shared definitions.** Jev's criteria paraphrase the guide the labelers followed. Jev reads the rules, while the local models learn them only from 1,888 labeled examples. That is what the comparison sets out to test, but it makes Jev's agreement partly a test of how well a written rule set transfers.
- **AI labels.** On the 550 new rows the labels come from two Claude models. Jev is a different vendor's model, but agreement between AI systems is not human ground truth. The 79 rows with human primary labels show the same order with a small margin.
- **Pretraining overlap** with the public corpora is unknown and cannot be tested here.
- **Reproducibility** differs by kind. Local runs are deterministic. The API repeat flipped 2 of 629 top choices on the same day, and a later model version could answer differently.
- **Cost and dependence.** Jev needs a network call, an account and a per-token price. The local models need neither.
- **Unopened test.** The sealed test decides nothing yet. Freezing the selection and the final test are M4 work.

## Files

All are ignored and local except this note.

| File | SHA-256 |
| --- | --- |
| `results/jev/m3-5-validation.jsonl` | `1f68d2f3534c2d5649f80f2caabef0eda2ddd6a37f28390b59858e0dc566f839` |
| `results/jev/m3-5-validation-repeat.jsonl` | `c8c4cf63ca0dbb0ddf5debe746fd31d58cc1e8d40178b3d6a4050641a69c2916` |
| `data/processed/m3-5-prepared-jev.json` | `b87d441c83a95559fbb27f24a87dc979c5a6b61c2781f7e39f21c63a8de27230` |
| `results/m3-5-full-a/manifest.json` | `03abb688856b46d74fb35b4307f4a0307cccf9e54a4d4994e24ef96cec688fd7` |
| `results/m3-5-full-b/manifest.json` | `5b1b3a4597e417481dbb4f1f51d026fffc71342de4eb422a063d5ae3bd473ad3` |
| `results/m3-5-full-a-selection.json` | `6a247792f9fde51381f8f43b0463cd0811b85c65b8a011dc3925215b3a008168` |
| `work/m3-5-archive/m3-5-full-release.zip` (3,040,475 bytes, 62 files, both Jev logs included) | `f95b2d9e9449d6d7483caaf5e3ad1bdb7c3c3aa0671d18566f6ec89bad49b57f` |

The two Jev logs hold validation text and stay out of Git, like the other results. This archive lists them explicitly, so for this release the gap in open decision 6, an archive that does not copy the Jev log, is covered by the file list.

## Still open

- **M4 integration.** Confidence, freeze and final-test enumeration for the new families. Jev is now the validation choice, so a final test needs Jev answers for the 628 sealed test queries. That means sending the test text to TypeSafe once, after the freeze, and Altan's approval for that is separate from this validation approval. The plan forbids forcing Jev into the logistic calibration path.
- **Study guide.** The M3.5 study guide and PDF.
- **Limits.** Altan's formal answer on the 15-minute and 2 GiB limits.
- **Key rotation.** Altan rotates the TypeSafe key.
- **Practice prompts** in the plan and the learning log, unanswered.
