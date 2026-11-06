# M4 confidence, freeze and final test

Run November 3, 2026, on the [M3.5 release](m3-5-dataset.md) `m3-5-v1` and the [27-configuration run](m3-5-full-run.md) `m3-5-full-a`, from branch `claude/m3-5-study-guide` at `8cb7ca1`. Altan accepted M3.5 ("Accept, run it") and approved the test send ("I approve to send 628 tests to Jev") in chat the same day. The sealed test was opened once, inside the receipt.

## Commands and outcomes

| Step | Command | Outcome |
| --- | --- | --- |
| Confidence | `confidence --run results/m3-5-full-a --selection results/m3-5-full-a-selection.json --out results/m4-5-validation` | `PASS`. All ten chosen systems refit on training rows only; only L3-C10 is calibrated, with sigmoid models on three grouped training folds. |
| Error review | `results/validation-interpretations-m3-5.jsonl`, SHA-256 `dd880262…` | All 17 Jev and all 29 L3-C10 validation errors, plus one correct comparison each, written as hypotheses by an agent and reviewed by the lead. |
| Freeze | `freeze --confidence results/m4-5-validation --error-review results/validation-interpretations-m3-5.jsonl --jev-test-log results/jev/m3-5-test.jsonl --out results/frozen-study-m3-5.json` | `PASS: final-test decisions frozen`. Freeze SHA-256 `e71f5b80…`. |
| Final test | `final-test --freeze results/frozen-study-m3-5.json --out results/final-test-m3-5 --send-jev-test` | `PASS: frozen final-test evidence`. One attempt, opened 15:15:28 UTC and completed 15:18:04 UTC. Receipt status `complete`. |

All commands ran with the four thread variables set to `1`. Outputs stay in ignored `results/`.

**Validation fallback threshold.** The rule prefers the widest coverage among thresholds whose accepted accuracy on validation is at least 0.90. Calibrated L3-C10 reaches 0.948 at threshold 0.0, so the frozen threshold is 0.0 and no query is withheld. Higher thresholds trade coverage for accuracy: 0.7 keeps 87.9% of validation rows at 0.984, and 0.9 keeps 66.5% at 0.998.

## Jev test collection

| Requests | Valid answers | Failed | Model | Input tokens | Latency, median / p95 / max |
| ---: | ---: | ---: | --- | ---: | --- |
| 628 | 628 | 0 | `jev-1.14.0` | 314,757 | 0.204 / 0.367 / 0.547 s |

At the published $0.042 per million input tokens this is about $0.013. The cost is inferred; no bill was seen. The key was read from Altan's local file into `TYPESAFE_API_KEY` for the one process. A scripted search found it in none of the outputs, logs or receipts. The test log `results/jev/m3-5-test.jsonl` (`bcdb69f2…`) holds test text and stays out of Git.

## Test results

Sealed test, 628 rows: 200 retrieval, 98 lookup, 131 calculation, 199 direct answer. Validation macro-F1 is shown for comparison only. Selection used validation and did not change after the test.

| Frozen system | Test macro-F1 | Test accuracy | Validation macro-F1 | Brier | ECE |
| --- | ---: | ---: | ---: | ---: | ---: |
| B0 | 0.120 | 0.317 | 0.121 | 1.366 | 0.683 |
| B1 | 0.863 | 0.858 | 0.878 | 0.212 | 0.072 |
| L1-C1 | 0.896 | 0.904 | 0.922 | 0.147 | 0.026 |
| L2-C1 | 0.903 | 0.914 | 0.924 | 0.210 | 0.219 |
| S1-C1 | 0.945 | 0.951 | 0.936 | n/a, margins | n/a |
| L3-C10 | 0.928 | 0.935 | 0.952 | 0.115 | 0.087 |
| L3-C10 calibrated | 0.927 | 0.932 | n/a | 0.113 | 0.055 |
| DT-d30-leaf1 | 0.807 | 0.822 | 0.818 | 0.329 | 0.119 |
| RF-dNone-leaf1 | 0.900 | 0.909 | 0.913 | 0.219 | 0.231 |
| XGB-d6-lr0.05 | 0.871 | 0.882 | 0.901 | 0.165 | 0.022 |
| **Jev (selected)** | **0.964** | **0.959** | **0.975** | 0.069 | 0.042 |

**Selected system.** Jev scores 0.964 test macro-F1, 0.011 below its validation score. Part of that drop may be the optimism of a validation-selected system. Most systems that were not selected fell more, L1-C1, L3-C10 and XGBoost by 0.025 to 0.030, so a test split that was harder for everyone is also likely. One split cannot separate the two. Jev's per-class test F1 is retrieval 0.954, lookup 0.990, calculation 0.969 and direct answer 0.942.

**Local systems.** S1-C1 scores 0.945 on test, above L3-C10's 0.928, although L3-C10 led on validation. This is one test split, and the frozen rule is not revisited. It shows that a 0.016 validation gap between local families does not reliably rank them.

**Fallback.** At the frozen threshold 0.0, calibrated L3-C10 accepts all 628 test rows with 0.932 accuracy, so the 0.90 target also holds on test. Calibration lowers L3-C10's test ECE from 0.087 to 0.055 at nearly unchanged accuracy.

**By row origin.** On the 79 test rows inherited from M3, Jev makes no error (macro-F1 1.000). L3-C10 makes 6 errors and S1-C1 makes 3. On the 549 new rows, Jev scores 0.959, L3-C10 0.930 and S1-C1 0.942.

## Test errors, counts only

Jev's confusion matrix, rows are the accepted label, columns the prediction, in the order retrieval, lookup, calculation, direct answer:

```text
retrieval    187   0    0   13
lookup         2  96    0    0
calculation    0   0  123    8
direct         3   0    0  196
```

| System | Errors | Largest groups |
| --- | ---: | --- |
| Jev | 26 | retrieval predicted direct answer: 11 No Robots, 2 Dolly; calculation predicted direct answer: 6 CLINC150, 1 TheoremQA, 1 MASSIVE; direct answer predicted retrieval: 3 No Robots; lookup predicted retrieval: 2 DataBench |
| L3-C10 | 41 | retrieval predicted direct answer: 5 No Robots; calculation predicted direct answer: 4 CLINC150; lookup predicted direct answer: 4 DataBench, 3 MASSIVE, 3 CLINC150 |

Eight test rows are wrong for both. The validation pattern repeats on test: 13 of Jev's 26 errors are retrieval queries whose passage the router never sees. The validation hypothesis, missing context in the router input, is still a hypothesis. The next section interprets every mistake of both systems.

## Test mistakes interpreted after the freeze

Every test mistake of Jev and raw L3-C10 now has a written hypothesis, in the same format as the validation ledger. A worker agent drafted the ledger from the sealed `error-review.jsonl` texts and the release's source fields. The lead read every row against its text and corrected five. Two inline-passage rows for Jev and one for L3-C10 moved from `multi_action_dependencies` to `vocabulary_mismatch`, because the passage is in the query and one action suffices. A reminder-list row moved from `annotation_ambiguity` to `vocabulary_mismatch`. One hypothesis that named the wrong predicted class was rewritten. Nothing in this section changes a label, the frozen selection or a reported score.

```text
$ uv run --locked python -m orchestra test-review --final-test results/final-test-m3-5 --interpretations results/test-interpretations-m3-5.jsonl
Jev: 26/26 errors interpreted, 1 correct comparison; annotation_ambiguity 8, missing_context 13, vocabulary_mismatch 5
L3-C10: 41/41 errors interpreted, 1 correct comparison; annotation_ambiguity 3, missing_context 9, multi_action_dependencies 1, other 5, vocabulary_mismatch 23
PASS: test interpretations match the final-test predictions
```

The ledger has 69 rows: all 67 errors plus the correct comparisons q2291 (Jev) and q2308 (L3-C10), both No Robots retrieval rows that name the missing text explicitly. It stays in ignored `results/` because it paraphrases test text.

Errors by category, validation ledger beside test ledger. Correct comparisons are excluded.

| Category | Jev validation | Jev test | L3-C10 validation | L3-C10 test |
| --- | ---: | ---: | ---: | ---: |
| missing context | 8 | 13 | 2 | 9 |
| annotation ambiguity | 4 | 8 | 6 | 3 |
| vocabulary mismatch | 3 | 5 | 16 | 23 |
| multi-action dependency | 1 | 0 | 2 | 1 |
| other | 1 | 0 | 3 | 5 |
| negation or out of scope | 0 | 0 | 0 | 0 |
| **Errors** | **17** | **26** | **29** | **41** |

Representative mistakes. Scores are the predicted class's probability; both systems output probabilities. The descriptions paraphrase; no test text is quoted.

| Query | System | Source | Accepted, predicted | Score | Category | Hypothesis |
| --- | --- | --- | --- | ---: | --- | --- |
| q2361 | Jev and L3-C10 | No Robots | retrieval, direct answer | 0.57 and 0.57 | missing context | The query points to text "below" that the router never receives, so it reads as an ordinary question. |
| q2814 | Jev | No Robots | retrieval, direct answer | 0.95 | missing context | A summary request names only a historical topic. Without the attached passage the topic looks answerable from knowledge. This is Jev's most confident retrieval error. |
| q0605 | Jev | CLINC150 | calculation, direct answer | 0.99 | annotation ambiguity | A kitchen unit conversion. Calculation comes from the adopted conversion default, and a direct answer is arguable. Six of Jev's eight calculation errors are such conversions. |
| q0549 | Jev | TheoremQA | calculation, direct answer | 0.99 | vocabulary mismatch | A well-known combinatorics result reads as recall. The calculation label itself is questionable. |
| q1529 | Jev | No Robots | direct answer, retrieval | 0.89 | vocabulary mismatch | The passage is pasted inline, but wording about quoted information suggests a document to fetch. The accepted label looks sound. |
| q2118 | L3-C10 | DataBench | lookup, direct answer | 0.76 | missing context | The question refers to an attached table the router never sees. |
| q1961 | L3-C10 | CLINC150 | lookup, direct answer | 0.78 | vocabulary mismatch | A request for the user's reminders without the word reminder. A word-count model has no lookup cue to use. |
| q0720 | L3-C10 | CLINC150 | calculation, direct answer | 0.86 | other | A bare sum of digits. Digits carry few of the word features the model learned. |

What the interpretations suggest, as hypotheses:

- **Jev's main failure is likely the router input, not the classifier.** About half of its errors on both validation (8 of 17) and test (13 of 26) are retrieval rows whose passage is withheld. The data contract keeps that passage out, so this is the likely cost of the contract. Only the confusion counts are measured; no run with the passage has tested the cause.
- **Jev's mistakes are mostly uncertain.** Their median predicted-class probability is 0.60. Five of the 26 reach 0.9 or more (q0470, q0549, q0605, q0718, q2814): four are calculation rows with arguable labels, and q2814 is the topic summary above.
- **L3-C10 fails on wording.** Its largest group is lookup predicted as direct answer, 14 rows: six personal-record requests (reminders, contacts, an appointment), four DataBench attached-table questions and four others. Vocabulary mismatch is the largest category on both splits, as expected from a bag-of-words model.
- **Some accepted labels are arguable.** The CLINC150 unit conversions, the four DataBench rows that rest on the attached-table rule, q2225 (no named store) and q3014 (a bare request to summarize) are flags for Altan's review. The frozen test labels stay as they are.

### Altan's review of the flagged labels, November 6, 2026

Altan kept all four sets of labels. Nothing changed: no file, frozen label or score. Keeping a label does not make every disagreement a clean classifier failure.

| Flagged case | Decision | Altan's reason |
| --- | --- | --- |
| CLINC150 unit conversions | Keep `calculation` | The adopted annotation default allows standard conversion factors, and it covers teaspoons and tablespoons, cups, pounds and kilos, and inches and centimeters consistently. Some one-unit questions resemble factual recall, so they stay boundary cases rather than clear reasoning failures. |
| DataBench q2118, q2280, q2281, q2283 | Keep `knowledge_lookup` | All four have pinned table references, and "listed" refers to those records. Reading the table comes before checking existence, counting or picking the most common or largest value. This follows the attached-table rule in the [M3.5 collection brief](../collection-brief-m3-5.md#guide-v3-two-lookup-rules). |
| q2225, company airplanes sorted by model | Keep `knowledge_lookup` | "Our company airplanes" names an organization's own inventory, and listing it requires reading records under the store-kind default. A database name is not needed. |
| q3014, "Please summarize:" | Keep `document_retrieval`, flag router context | Altan checked that it has a nonempty attached passage with a matching hash, so reading it is necessary. The label fits the full request, but the router sees neither the passage nor attachment metadata, so its task is underspecified. This is an input limitation, not a label error. |

The lead checked the DataBench and q2225 reasons against the collection brief. The conversion default is cited from the annotation decisions; the lead did not find it written in a tracked document, so its location is unverified here.

## Checks

- The receipt `results/test-receipts/7aacbc49….json` records one attempt, status `complete`, freeze `e71f5b80…`, and Jev log `bcdb69f2…`.
- The Jev test log has 628 unique query IDs, 628 status-200 responses and no error.
- `results/final-test-m3-5/warnings.json` is empty. Predictions cover 628 rows for each of the eleven evaluated systems.
- The lead recomputed the by-origin scores and error groups from `predictions.jsonl` and the release file.
- On November 3, after the test review, the receipt's `result_manifest_sha256` still equals the SHA-256 of `results/final-test-m3-5/manifest.json`, so the predictions that `test-review` checked are the sealed ones.

## Identities

| Artifact | SHA-256 |
| --- | --- |
| `results/frozen-study-m3-5.json` | `e71f5b80e1f85f3d548772a4e3b93ec2ed0af0e1cd0b35964669b729cd2a6284` |
| `results/validation-interpretations-m3-5.jsonl` | `dd880262275515070f025d4a44fa8c73294f14832da950c32480a8b3df948b92` |
| `results/test-interpretations-m3-5.jsonl`, written after the test | `c65a0b0b5ee6ce6dc3f246a1da5115e61bf0b94c938d67fdc358977b4b363f49` |
| `results/jev/m3-5-test.jsonl` | `bcdb69f2db765309d2504ff5ee2c1bdcb3e85b035644c0988f10d11bc935a105` |
| `results/final-test-m3-5/manifest.json` | `9b9b7f2103e325dabbfd53177f5bba2bba6da5e13ea488f3cb1ae1dee664b94a` |
| `results/final-test-m3-5/metrics.json` | `ba9cfe06640485c9441a8d8c5442d534006cce7d8d43ab6a8a6590cc19428b6e` |
| `results/final-test-m3-5/predictions.jsonl` | `97e0382b1fd03956731d697e79d32352ffc5d7466d65e073fa604678039cb9fb` |

## Limitations

- **One split, one opening.** No interval or significance test was computed. Small gaps, such as S1-C1 against L3-C10, are within what another split could reverse.
- **Labels.** Test labels share the M3.5 process: AI labels with Altan adjudicating disagreements. The scores measure agreement with those labels, not human agreement.
- **Jev.** Its test answers come from one pass on one day. Pretraining overlap with the public corpora is unknown, and the test text now sits with TypeSafe under its terms.
- **Missing context.** Retrieval rows whose passage is withheld from the router remain the largest error group for Jev on both validation and test.

## M4 closing work

- Done November 5: the M4 study guide and PDF, and Altan's answers to its nine questions.
- Done November 6: Altan reviewed the flagged test labels and kept all of them (see above).
- Done November 6: Altan accepted M4. The dated snapshot `M4-confidence-errors-2026-11-06.pdf` is identical to the November 3 edition.
