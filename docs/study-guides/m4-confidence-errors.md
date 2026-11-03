# M4: confidence, errors and the sealed test

Study guide edition: November 3, 2026. The evidence is the confidence analysis `results/m4-5-validation/`, the freeze `results/frozen-study-m3-5.json` (`e71f5b80…`), and the one final test `results/final-test-m3-5/`. The freeze recorded git commit `8cb7ca1` and was written at 15:15:12 UTC. The test was opened at 15:15:28 UTC. The run record is [the M4 final-test record](../evidence/m4-final-test.md). Data release `m3-5-v1`, split manifest `7aacbc49…`. Full hashes are in the appendix. The project is course project 13, Learning to Route Queries in AI Systems. This guide follows on from the [M3.5 guide](m3-5-data-and-methods.md).

## What you need to defend

M4 asks two questions. How far can a router's confidence be trusted, and what does the one untouched test say about the systems chosen on validation? The first answer comes from validation rows only. The second comes from the 628 sealed test rows, scored once.

You should be able to explain six things. What "confidence" means in this project and why an SVM margin is not a probability. What sigmoid calibration changes and what it cannot change. Why every choice is frozen before the test is opened. What the one opening showed. Which mistakes remain, and what the confusion matrix says about them. Why none of this proves how the router would behave on real users.

M4 adds no new model. It uses the ten systems chosen in M3.5 and one extra object, a calibrated version of L3-C10. Every test mistake of Jev and L3-C10 is interpreted in a separate section below. They are hypotheses, not findings.

## Confidence in plain words

A router picks one of four actions, and the confidence is how sure it says it is. Three different things get called confidence, so keep them apart.

1. **A margin.** An SVM such as S1-C1 outputs a score for each class. It is a signed distance from a dividing surface. A larger margin means the query sits farther from the boundary. It is not a probability. It does not sum to 1, and nothing says a margin of 1.4 is right 90% of the time. The project therefore gives S1 classification and error results only. This is stated in `docs/data-and-evaluation.md`.
2. **A probability.** Logistic regression, naive Bayes, the forest, XGBoost and Jev output four numbers that sum to 1. The largest one is the top-label confidence. Being a probability by form does not make it a trustworthy probability. The M3.5 trace already showed a tree and Jev both saying 1.0, one wrong and one right.
3. **A calibrated probability.** A probability is calibrated when, among rows given about 0.8, about 80% are right. Calibration is a second fitting step that bends the raw numbers toward that behaviour. It needs rows the first model was not fitted on. In M4 only L3-C10 gets this step. The data-and-evaluation document declares that choice before any test run, and the other systems keep their own probabilities with no extra calibration.

The practical use of confidence is a fallback. If the top probability is below a threshold, the router would ask for clarification or send the query to a person. No fallback tool exists in the project. M4 only measures how well such a rule could work.

**What calibration did here, validation, 629 rows.** Raw L3-C10 was underconfident, not overconfident. Its top-label confidence in the 0.4 to 0.6 bin averaged 0.520 while 75.5% of those rows were right. Calibration moved the numbers up toward the accuracy and left the picture still underconfident. Log loss fell from 0.214 to 0.189, Brier from 0.096 to 0.092 and ECE from 0.100 to 0.061. Accuracy went down slightly, from 0.954 to 0.948. The calibrated system is a different object from raw L3-C10. It averages three L3-C10 copies, each fitted on two thirds of the training rows, and renormalizes four per-class sigmoids, so a few close calls land on another class. All numbers are from `results/m4-5-validation/metrics.json`.

## Why choices are frozen before the test

The test is useful once. If a score from it can change a choice, it stops being an estimate that the choice never touched. M4 therefore works in this order.

1. **Confidence on validation.** The nine local systems are refit on the 1,888 training rows, and Jev's validation answers are replayed from its pinned log. The run checks that each system reproduces the saved M3.5 validation predictions and scores. Only then does it fit the calibration and write the threshold table.
2. **Error review on validation.** The 17 Jev and 29 L3-C10 validation errors were read and written up as hypotheses. This ledger is an input to the freeze, and its hash is recorded.
3. **Freeze.** The freeze file records the systems, the settings, the calibration folds, the fallback threshold, the hash of every input and code file, and the error-review hash. It also names an ignored path for the Jev test answers, and that path must not exist yet.
4. **Final test.** One command scores the sealed rows once.

**What the test may not do.** It may not pick a new winner, change a threshold, change a prompt or retrain anything. The report keeps the frozen choices even where the test disagrees with them.

**Sending the test to Jev.** Sending the 628 queries to a vendor is itself part of opening the test, and the text then sits with TypeSafe under its terms. Altan wrote "I approve to send 628 tests to Jev" in chat on November 3, and the final-test command needs an explicit `--send-jev-test` flag. The key was read once from Altan's local file, and a scripted search found it in no output according to the record.

## What the one opening showed

Every number below is from `results/final-test-m3-5/metrics.json` and the evidence record, except where marked.

1. **Jev stayed best, with a small drop.** Test macro-F1 is 0.964 against 0.975 on validation. From the three-decimal values the gap is 0.011, and the unrounded files give about 0.012 (my arithmetic). Picking the best system on validation can make its validation score optimistic, but this drop cannot show how much. Most systems that were not selected fell more, so part of the drop is likely a test split that was harder for everyone.
2. **Most systems fell.** Nine of the ten frozen systems scored lower on test than on validation. B0 fell by only 0.0003. S1-C1 rose by 0.0096. XGBoost fell most, by 0.030. These differences are my arithmetic from `results/m4-5-validation/systems.json` and the test metrics.
3. **The local ranking flipped.** S1-C1 scored 0.945 on test and L3-C10 0.928, although L3-C10 led on validation, 0.952 to 0.936. L3-C10 stays the frozen local choice. One 0.016 validation gap does not reliably rank two families, and one test split cannot settle it either way.
4. **The fallback target held.** At the frozen threshold 0.0, calibrated L3-C10 accepts all 628 rows with accuracy 0.932. The 0.90 target is met with nothing withheld. This is a design target, not a promise.
5. **Calibration helped the probabilities again.** L3-C10's test ECE fell from 0.087 to 0.055 and its Brier score from 0.115 to 0.113, at 0.935 and 0.932 accuracy.

## What your report can and cannot claim

It can say that the frozen systems were scored once and report the table below. It can say that the selected system lost a little on unseen rows and that the local ranking was unstable. It cannot say that Jev is better than a trained classifier in general, that 0.964 predicts real-user performance, or that the errors have the causes named in a hypothesis. The test scores agreement with accepted labels, which are AI checks with Altan adjudicating disagreements.

## Trace one query: q0005

q0005 is an Altan-authored validation row, "A train ticket costs 45 kr. How much do three tickets cost?" Its accepted label is calculation, its group is g042 and its source is `altan-authored`. It is a validation row, so no sealed text is involved. The numbers below were read from `results/m4-5-validation/predictions.jsonl`. Class order is retrieval, lookup, calculation, direct answer. The calculation below is mine, and the file is the only source of the probabilities.

| Row | Retrieval | Lookup | Calculation | Direct answer |
| --- | ---: | ---: | ---: | ---: |
| Raw L3-C10 | 0.0276 | 0.0430 | 0.8045 | 0.1249 |
| Calibrated L3-C10 | 0.0019 | 0.0163 | 0.8853 | 0.0965 |

**Prediction.** Both predict calculation, which matches the label. The top-label confidence is 0.8045 raw and 0.8853 calibrated. Calibration raised the confidence and the other three classes all fell.

**Reliability bin.** The five bins are [0, 0.2), [0.2, 0.4), [0.4, 0.6), [0.6, 0.8) and [0.8, 1.0], with the last bin closed. Raw 0.8045 lies 0.0045 above the edge, so it falls in the top bin. Calibrated 0.8853 is in the top bin too. In the calibrated validation table that bin holds 507 rows with mean confidence 0.9452 and accuracy 0.9921. q0005 sits below that bin's mean, so the bin average does not describe it exactly. A bin describes a group of rows, not one row.

**Threshold.** The calibrated top confidence 0.8853 is at least 0.0, so threshold 0.0 accepts it. It would also be accepted at 0.5, 0.6, 0.7 and 0.8. Threshold 0.9 would withhold it, since 0.8853 is below 0.9. The frozen threshold is 0.0, so nothing is withheld.

**Losses on this row.** With the true class calculation:

```text
raw log loss        = -ln(0.8045)  = 0.2176
calibrated log loss = -ln(0.8853)  = 0.1218
raw Brier           = 0.0008 + 0.0019 + 0.0382 + 0.0156 = 0.0565
calibrated Brier    = 0.0000 + 0.0003 + 0.0131 + 0.0093 = 0.0227
```

Calibration lowered both losses on this row. The mean over all 629 validation rows is 0.2139 raw and 0.1893 calibrated for log loss, and 0.0961 raw and 0.0923 calibrated for Brier. One row does not rank anything. It shows how a single number enters each metric.

**How a test row would travel.** `final-test` reserves the split, sends the unchanged query text with the frozen question to Jev, logs the answer, refits the nine local systems on training rows, applies the frozen threshold 0.0 to the calibrated L3-C10 probabilities and scores every system against the accepted label once. A test row never reaches the guide.

<!-- pagebreak -->

## Test results

Sealed test, 628 rows, 200 retrieval, 98 lookup, 131 calculation and 199 direct answer. Source is `docs/evidence/m4-final-test.md`, checked against `results/final-test-m3-5/metrics.json`. All values agree to three decimals. Validation macro-F1 is for comparison only.

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

Test log loss is in the same file. Jev has 0.141, calibrated L3-C10 0.229, raw L3-C10 0.245, and B0 24.62. B0 and DT show the cost of a probability of exactly 0 on the true class (see the appendix). The calibrated row has no validation macro-F1 in the evidence table because the validation-selection rule did not score it. Its validation macro-F1 in `metrics.json` is 0.945, and I did not use it for any choice.

**Jev per class, test F1.** Retrieval 0.954, lookup 0.990, calculation 0.969, direct answer 0.942.

**The optimism of a selected system.** Jev won because it scored highest on validation. A best-of-27 pick can be biased upward by luck in those rows, so its validation score may overstate what it will do on new rows. The test cannot isolate that bias. Jev fell by about 0.012, while L1-C1, L3-C10 and XGBoost, none of them the overall pick, fell by 0.025 to 0.030. A harder test split and selection optimism are both possible parts of the drop, and one split cannot separate them. Group-aware resampling, which the protocol allows, was not computed.

**Ranking instability.** S1-C1 beat L3-C10 on test by 0.017 macro-F1, with 31 errors against 41. On validation the order was reversed. Two reasons are plausible, and both are hypotheses. The validation gap was small and could sit inside split noise. The families may also differ in how well they carry to rows with different sources. The data cannot separate those. The frozen rule is not revisited, so L3-C10 is still the local system the report carries, and S1-C1's test lead is reported as a finding about this split.

**By row origin.** On the 79 test rows inherited from M3, Jev makes no error, with macro-F1 1.000. L3-C10 makes 6 errors and S1-C1 makes 3. On the 549 new rows, Jev scores 0.959, L3-C10 0.930 and S1-C1 0.942. The record says the lead recomputed these from `predictions.jsonl` and the release file. I took them from the record and did not recompute them.

**Fallback on test.** Calibrated L3-C10 at threshold 0.0 accepts 628 rows and gets 585 right, accuracy 0.9315 (`thresholds.json`). The frozen rule did not need a higher threshold because 0.0 already qualified on validation.

## Test errors, counts first

Jev's confusion matrix. Rows are the accepted label and columns the prediction, in the order retrieval, lookup, calculation, direct answer.

```text
retrieval    187   0    0   13
lookup         2  96    0    0
calculation    0   0  123    8
direct         3   0    0  196
```

It comes from `results/final-test-m3-5/confusion.json` and matches the evidence record. The diagonal gives 187 + 96 + 123 + 196 = 602 right and 26 wrong of 628.

| System | Errors | Largest groups, from the record |
| --- | ---: | --- |
| Jev | 26 | retrieval predicted direct answer, 11 No Robots and 2 Dolly; calculation predicted direct answer, 6 CLINC150, 1 TheoremQA and 1 MASSIVE; direct answer predicted retrieval, 3 No Robots; lookup predicted retrieval, 2 DataBench |
| L3-C10 | 41 | retrieval predicted direct answer, 5 No Robots; calculation predicted direct answer, 4 CLINC150; lookup predicted direct answer, 4 DataBench, 3 MASSIVE and 3 CLINC150 |

Eight test rows are wrong for both. For S1-C1 the matrix gives 31 errors, and for calibrated L3-C10 it gives 43 (my count from `confusion.json`).

**Precision and recall for Jev, from the matrix.** Precision of a class is its diagonal count over its column total. Recall is the diagonal over its row total.

| Class | Right | Column total | Row total | Precision | Recall |
| --- | ---: | ---: | ---: | ---: | ---: |
| Retrieval | 187 | 192 | 200 | 0.974 | 0.935 |
| Lookup | 96 | 96 | 98 | 1.000 | 0.980 |
| Calculation | 123 | 123 | 131 | 1.000 | 0.939 |
| Direct answer | 196 | 217 | 199 | 0.903 | 0.985 |

Direct answer has high recall and the lowest precision. Jev often says direct answer when the label is retrieval or calculation. Thirteen retrieval rows and eight calculation rows land there. The matrix agrees with `metrics.json` for these eight values.

Raw L3-C10's test confusion matrix, from the same file and in the same order, is for practice question 6:

```text
retrieval    195   0    0    5
lookup         1  80    3   14
calculation    1   2  120    8
direct         3   1    3  192
```

**Missing context.** Thirteen of Jev's 26 errors are retrieval rows predicted as direct answer. The router never sees the retrieval passage. The validation review proposed that this missing context is the cause. That is still a hypothesis. The test mistakes were read after the freeze, and the next section summarizes them.

<!-- pagebreak -->

## Test mistakes, read after the freeze

Every test mistake of Jev and raw L3-C10 now has a written hypothesis. A worker agent drafted them from the test texts, and the lead read each one against its text and corrected five. They sit in the ignored ledger `results/test-interpretations-m3-5.jsonl`, because they paraphrase test text. The command `test-review` checks that each entry names a real sealed-test prediction and counts the categories. The ledger changes no label, no selection and no score. The full record, with SHA-256 `c65a0b0b…`, is in [the M4 final-test record](../evidence/m4-final-test.md#test-mistakes-interpreted-after-the-freeze).

Errors by category, validation beside test. The two correct comparison rows are left out.

| Category | Jev validation | Jev test | L3-C10 validation | L3-C10 test |
| --- | ---: | ---: | ---: | ---: |
| missing context | 8 | 13 | 2 | 9 |
| annotation ambiguity | 4 | 8 | 6 | 3 |
| vocabulary mismatch | 3 | 5 | 16 | 23 |
| multi-action dependency | 1 | 0 | 2 | 1 |
| other | 1 | 0 | 3 | 5 |
| **Errors** | **17** | **26** | **29** | **41** |

Four examples, paraphrased. No test text is quoted. The score is the predicted class's probability.

- **q2361, both systems, retrieval predicted as direct answer, 0.57 each.** The query asks about text "below", and the router never receives that text. It reads as an ordinary question. Missing context.
- **q0605, Jev, calculation predicted as direct answer, 0.99.** A kitchen unit conversion. The calculation label comes from the adopted conversion default, so a direct answer is arguable. Six of Jev's eight calculation errors are such conversions. Annotation ambiguity.
- **q1529, Jev, direct answer predicted as retrieval, 0.89.** The passage is pasted into the query, but wording about quoted information suggests a document to fetch. The accepted label looks sound. Vocabulary mismatch.
- **q1961, L3-C10, lookup predicted as direct answer, 0.78.** A request for the user's reminders that never says reminder. A word-count model has no lookup cue to use. Vocabulary mismatch.

What the review suggests, as hypotheses. About half of Jev's errors on both splits involve withheld passages, so the router's input contract is the likely main cost for Jev, not its classifier. Jev's mistakes are mostly uncertain, with a median predicted-class probability of 0.60. L3-C10 fails mainly on wording, which fits a bag-of-words model. Some accepted labels are arguable: the unit conversions, four DataBench questions about an attached table, a lookup request that names no store, and one bare request to summarize. They are flags for your review. The frozen test labels stay as they are.

## Limitations

- **One split, one opening.** No interval or significance test was computed. A 0.017 gap such as S1-C1 against L3-C10 is within what another split could reverse.
- **Labels.** The accepted labels are AI checks with Altan adjudicating disagreements. The scores measure agreement with those labels, not with independent human judgments. No human agreement figure exists.
- **Jev.** Its test answers come from one pass on one day. Its pretraining overlap with the public corpora is unknown. The test text now sits with TypeSafe.
- **Missing passage context.** A retrieval query that depends on a withheld passage may look like a general question. Retrieval predicted as direct answer is Jev's largest error group on both splits, and no run with the passage has tested that cause.
- **ECE is bin sensitive.** The value moves with the number of bins. I computed calibrated validation ECE for several bin counts in `work/m4-guide/ece_bins.py`. It is 0.0600 with three bins, 0.0613 with five and ten, and 0.0620 with twenty. The five-and-ten match occurs because each ten-bin half has the same gap sign as its five-bin parent, so splitting a bin cannot cancel gaps. With small bins the sign can flip. Report the count of bins and the bin sizes, and do not read ECE as proof of calibration.
- **Small bins.** The calibrated validation bin [0.2, 0.4) holds one row, and its accuracy of 0.0 says nothing about calibration.
- **Calibration is one system.** Only L3-C10 was calibrated, so a comparison of calibrated probabilities across families does not exist. This was declared in advance.
- **Fallback is untested in use.** No fallback tool exists, so a threshold shows only how coverage and accuracy trade off.
- **Domain shift.** The test rows come from the same public sources and process as the validation rows. Real user queries may differ.

<!-- pagebreak -->

## Technical appendix: confidence metrics

Here `N` is the number of rows, `K = 4` classes, `y_i` the true class of row `i`, and `p_ik` the model's probability for class `k` on row `i`. Class order is retrieval, lookup, calculation, direct answer. The code is `probability_metrics` in `src/orchestra/confidence.py`.

**Multiclass log loss.** It measures how much probability the model gave the true class. A confident wrong answer costs a lot.

```text
LL = -(1 / N) * sum over rows i of ln( p_i,y_i )
```

The code clips `p_i,y_i` to at least machine epsilon, about 2.2e-16, so that a zero does not give infinity. The clip gives a finite cap, `-ln(2.2e-16)` is about 36.04. B0 puts probability 1 on direct answer for every row, so each of its 429 wrong test rows costs about 36.04. The mean is 36.04 times 429 / 628, which is about 24.62. That equals B0's reported test log loss 24.62 (my arithmetic check).

**Multiclass Brier score.** It is the mean over rows of the sum over classes of the squared error between the probability and the one-hot truth `o_ik`, which is 1 for the true class and 0 otherwise.

```text
Brier = (1 / N) * sum over rows i of sum over classes k of ( p_ik - o_ik )^2
```

It ranges from 0 to 2. A row with probability 1 on a wrong class scores 2. B0 is right on 199 of 628 test rows, so it is wrong on 429. Its Brier score is 2 times 429 / 628, which is 1.366 and equals the file (my arithmetic check).

**Five-bin top-label reliability.** The top-label confidence is `c_i = max over k of p_ik`. Rows are grouped by `c_i` into [0, 0.2), [0.2, 0.4), [0.4, 0.6), [0.6, 0.8) and [0.8, 1.0], the last closed. In each bin `b` with `n_b` rows, `conf_b` is the mean confidence and `acc_b` is the share of rows whose top label equals the truth.

```text
ECE = sum over bins b of ( n_b / N ) * | acc_b - conf_b |
```

With four classes the top probability is at least 0.25, so the first bin is always empty. That is my inference, and the files show 0 rows there.

**Worked example, calibrated L3-C10, validation, 629 rows.** From `results/m4-5-validation/reliability.json`.

| Bin | Rows | Mean confidence | Accuracy | Right | Gap | Weight x gap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| [0.0, 0.2) | 0 | none | none | none | none | 0 |
| [0.2, 0.4) | 1 | 0.3988 | 0.0000 | 0 | 0.3988 | 0.0006 |
| [0.4, 0.6) | 36 | 0.5197 | 0.6667 | 24 | 0.1470 | 0.0084 |
| [0.6, 0.8) | 85 | 0.7049 | 0.8118 | 69 | 0.1069 | 0.0144 |
| [0.8, 1.0] | 507 | 0.9452 | 0.9921 | 503 | 0.0469 | 0.0378 |

The weights are 1/629, 36/629, 85/629 and 507/629. The sum of the last column is 0.0612, and the saved `ece` is 0.0613 (0.06128 to five decimals). The bins sum to 629 rows. Every bin except the one-row [0.2, 0.4) bin has accuracy above confidence, so the calibrated model is still underconfident wherever there are enough rows to say so. Raw L3-C10 has bins of 15, 53, 107 and 454 rows with ECE 0.0997. Calibration pulled rows out of the middle bins toward the top. The test table for calibrated L3-C10, from `results/final-test-m3-5/reliability.json`, has bins of 3, 46, 91 and 488 rows, mean confidence 0.370, 0.519, 0.716 and 0.944, and accuracy 0.333, 0.587, 0.813 and 0.990.

**Sigmoid (Platt) calibration.** The raw model's scores for one class are mapped through a logistic curve fitted to hold-out labels.

```text
p_calibrated(class k) = 1 / ( 1 + exp( A_k * f_k(x) + B_k ) )
```

Here `f_k(x)` is the model's raw score for class `k`, and `A_k` and `B_k` are fitted on rows the model did not train on. The project uses `CalibratedClassifierCV(L3-C10, method="sigmoid", cv=folds, ensemble=True, n_jobs=1)`, with the seed-42 folds below. I checked the installed scikit-learn code. For each class it fits one sigmoid on the estimator's `decision_function`, one class against the rest, then normalizes the four values to sum to 1. With `ensemble=True` it keeps one calibrated model per fold and averages their probabilities at prediction time. Each fold's L3-C10 copy is fitted on about 1,258 rows, not all 1,888, which is why the calibrated system can predict a different class from raw L3-C10.

The folds come from `calibration_folds` in `confidence.py`, `StratifiedGroupKFold(n_splits=3, shuffle=True, random_state=42)` on the training rows. They are group-aware, so related rows never fall on both sides. The code raises an error if a fold side lacks any class or a group crosses a side. The saved `calibration-folds.json` has three folds.

| Fold | Rows to fit L3-C10 | Rows to fit sigmoids | Fit groups | Held groups |
| --- | ---: | ---: | ---: | ---: |
| 1 | 1,258 | 630 | 1,086 | 542 |
| 2 | 1,259 | 629 | 1,085 | 543 |
| 3 | 1,259 | 629 | 1,085 | 543 |

Each fold's fit side and held side together cover all 1,888 training rows. Validation and test rows are never used to fit the calibration. This is a project choice. The lectures do not teach calibration.

**Threshold rule.** The top calibrated probability is compared with each of 0.0, 0.5, 0.6, 0.7, 0.8 and 0.9. A row is accepted when `c_i` is at least the threshold.

```text
coverage           = accepted / total
selective accuracy = correct accepted / accepted     (undefined if nothing is accepted)
chosen threshold   = the qualifying one with the widest coverage
qualifying         = at least one accepted row and selective accuracy >= 0.90
```

If none qualify the status is `no_qualifying_threshold`. The 0.90 value is a design target, not a promise. Validation table for calibrated L3-C10, from `results/m4-5-validation/thresholds.json`:

| Threshold | Accepted | Coverage | Correct accepted | Accuracy of accepted |
| ---: | ---: | ---: | ---: | ---: |
| 0.0 | 629 | 1.000 | 596 | 0.948 |
| 0.5 | 619 | 0.984 | 590 | 0.953 |
| 0.6 | 592 | 0.941 | 572 | 0.966 |
| 0.7 | 553 | 0.879 | 544 | 0.984 |
| 0.8 | 507 | 0.806 | 503 | 0.992 |
| 0.9 | 418 | 0.665 | 417 | 0.998 |

All six qualify. The widest coverage is at 0.0, so the frozen threshold is 0.0. Accuracy rises as coverage falls, which is the point of a fallback. Per-class coverage at 0.9 is 0.769 retrieval, 0.710 lookup, 0.600 calculation and 0.580 direct answer, so a high threshold withholds more of the classes the model is less sure of.

## Technical appendix: freeze and receipt

**What `freeze` binds.** From `freeze` in `confidence.py`, the freeze file holds the `confidence` directory's manifest hash, the chosen systems and their resolved settings, the calibration settings and fold membership, the fallback threshold table, the hash of the input data and of every code file named in the run, the hash of the validation error-review ledger, and the ignored path for Jev's test log. It records the time and the git commit. It refuses to be rewritten with a different content, and it refuses to start if the Jev test log already exists, so no test answer can exist before the final test.

**Why `final-test` runs once per split.** The command first checks that the confidence manifest, config, folds, fallback and code hashes still equal the frozen ones. It takes a file lock on the split. It then looks for a receipt named by the split manifest's SHA-256. If a receipt exists for that split, a changed request is refused. A completed receipt returns the saved results without scoring again. An incomplete receipt can continue only with `--resume` and an identical request. Resume checks that the Jev test log has not changed since the last attempt, and it sends each unanswered query at most once. So the code does not forbid recovery from a crash. It forbids a second, different evaluation of the same split.

**The receipt for this run.** The receipt `results/test-receipts/7aacbc49….json` records freeze `e71f5b80…`, one attempt, status `complete`, and result manifest `9b9b7f21…`. The record says the attempt opened at 15:15:28 UTC and completed at 15:18:04 UTC. Jev answered 628 of 628 requests with model `jev-1.14.0` and 314,757 input tokens. The cost of about $0.013 at the published price is inferred, since no bill was seen.

**Why the Jev collection is inside the reservation.** The vendor sees the test text, so collecting answers outside the receipt would be an unrecorded opening of the test.

## Technical appendix: file identities

| Artifact | SHA-256 |
| --- | --- |
| `results/frozen-study-m3-5.json` | `e71f5b80e1f85f3d548772a4e3b93ec2ed0af0e1cd0b35964669b729cd2a6284` |
| `results/validation-interpretations-m3-5.jsonl` | `dd880262275515070f025d4a44fa8c73294f14832da950c32480a8b3df948b92` |
| `results/m3-5-full-a-selection.json` | `6a247792f9fde51381f8f43b0463cd0811b85c65b8a011dc3925215b3a008168` |
| `results/m4-5-validation/manifest.json` | `92050dc4e899f59eae749f2f474f1d28317b7ad0a31bc4e8bb99a14295ae4185` |
| `results/m4-5-validation/metrics.json` | `09f8a2d5f2350b80c17fb3f1766bafbd68886cb11cf369955fb65fd3194344d0` |
| `results/m4-5-validation/reliability.json` | `5a501dd4557882b56f430d6daf2981a3a824e5859848f4c1f4f68290c540e094` |
| `results/m4-5-validation/thresholds.json` | `346145c10a21ceed0b256966ded81fb6a6e5bec695ecac9a7bb131aa8f9398d2` |
| `results/m4-5-validation/predictions.jsonl` | `a483b26a0a45a4701e30f588208787bec1e26b17af51a5f927965366cee2314b` |
| `results/m4-5-validation/systems.json` | `65c512405318c5adfe9159e707bc6639bcc858c09ce6e9824e1b8e80f597d05d` |
| `results/m4-5-validation/calibration-folds.json` | `a5208b8581e6ebdd51d55cfb3e47e373310dfd272ca6519441c8dc31298f7750` |
| `results/jev/m3-5-test.jsonl` | `bcdb69f2db765309d2504ff5ee2c1bdcb3e85b035644c0988f10d11bc935a105` |
| `results/final-test-m3-5/manifest.json` | `9b9b7f2103e325dabbfd53177f5bba2bba6da5e13ea488f3cb1ae1dee664b94a` |
| `results/final-test-m3-5/metrics.json` | `ba9cfe06640485c9441a8d8c5442d534006cce7d8d43ab6a8a6590cc19428b6e` |
| `results/final-test-m3-5/reliability.json` | `16e54d3100ff04fe0c9fad1c038c543554b9326e9dd3b128be301db84b5ad76f` |
| `results/final-test-m3-5/thresholds.json` | `6a6a500680666afead0ba968697bc6ddb7a5ea7aacb0f251d01976ba1f1f932e` |
| `results/final-test-m3-5/confusion.json` | `165761528e0c2eb4786554b0dd0db5adcfc305cdd9d907eae3f3dd8db8844aac` |
| `results/final-test-m3-5/predictions.jsonl` | `97e0382b1fd03956731d697e79d32352ffc5d7466d65e073fa604678039cb9fb` |

The Jev test log holds test text and stays out of Git. The test outputs also stay in ignored `results/`.

<!-- pagebreak -->

## Report evidence

`docs/project-plan.md` names the "Confidence and error analysis" section, about 1.5 pages, with a reliability diagram, log loss and Brier score, an accuracy-versus-coverage curve and annotated error examples. Its stated risks are imperfect calibration and domain shift. The table maps each element to a saved artifact. No figure was rendered for this guide. The `figures` command exists, but I did not run it.

| Report element | Saved artifact | What it supports |
| --- | --- | --- |
| Reliability diagram, validation | `results/m4-5-validation/reliability.json`, keys `raw` and `calibrated` | Bin counts, mean confidence and accuracy per bin for L3-C10, raw against calibrated |
| Reliability diagram, test | `results/final-test-m3-5/reliability.json` | The same bins for every frozen system on 628 rows |
| Log loss and Brier score | `results/m4-5-validation/metrics.json`, `results/final-test-m3-5/metrics.json` | Raw against calibrated L3-C10 on both splits, and all probability systems on test |
| Accuracy versus coverage | `results/m4-5-validation/thresholds.json` for the curve, `results/final-test-m3-5/thresholds.json` for the one frozen test point | Coverage and accepted accuracy by threshold, and the 0.932 test accuracy at threshold 0.0 |
| Confusion matrices | `results/final-test-m3-5/confusion.json` | Raw and row-normalized counts for each system |
| Annotated errors, validation | `results/validation-interpretations-m3-5.jsonl` (ignored, hash above) | Hypotheses for the 17 Jev and 29 L3-C10 validation errors with comparison rows |
| Annotated errors, test | `results/test-interpretations-m3-5.jsonl` (ignored), checked by `test-review` | Hypotheses for all 26 Jev and 41 L3-C10 test mistakes, with no change to the frozen results |
| Selection and freeze | `results/frozen-study-m3-5.json`, the receipt and the evidence record | That the test was opened once, after the freeze |

A calibrated reliability diagram with bin counts is the main figure. Show counts beside the bars, because the bin with one row cannot support a claim. The accuracy-versus-coverage curve has six points and comes from validation. Add the single test point at threshold 0.0 as a check.

## Course connections

Pages are one-based PDF pages. I extracted each cited page with `pdftotext` on November 3, 2026. Course concepts are listed separately from project choices.

**Scope.** `CourseProjects.pdf` p. 15 asks Project 13 to compare classifiers and feature representations and to analyze prediction confidence and errors. `ProjectRreportInstructions.pdf` p. 1 asks for an own-words report with visualizations, 5 to 12 pages, in IEEE two-column format, due December 6, 2026.

**Unseen testing.** `Lecture5-FundamentalClassificationAlgorithms.pdf` p. 2 says that previously unseen records should be classified as accurately as possible and a test set is used to determine accuracy. Page 5 says the test set must be separate from the training set, or an overfit situation results. The frozen single test and the group-aware split put this into practice.

**Overfitting and optimism.** `Lecture5-FundamentalClassificationAlgorithms.pdf` p. 53 says that with overfitting the training error no longer estimates performance on unseen records. Page 56 separates the error on training from the generalization error and shows an optimistic approach that sets them equal. A validation score used to choose a system is an optimistic estimate of that kind. The sealed test scores the choice without that bias, but one split cannot say how much of a drop is optimism and how much is a harder test set. That link between the slide and selection bias is my reading.

**Margins.** `Lecture5-FundamentalClassificationAlgorithms.pdf` p. 79 lists a widest margin as one of three big SVM ideas, and page 80 describes a soft margin where a margin value of at least 1 incurs no penalty. These pages describe margins as distances used for fitting. They do not turn margins into probabilities, so the statement that S1 margins are not probabilities rests on the project documents, not on the slides.

**Evaluation roles.** `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` p. 52 describes dividing data into training, validation and test sets and checking predictive capability on the test set. Its fourth step says the validation error gives an unbiased estimate of predictive power. That holds for a model fixed in advance. Once validation picks the best of 27 configurations, the winner's validation score is optimistic, which is why the project keeps a separate test. That qualification is the project's reading, not the slide's. Page 53 warns to ensure the test set is truly independent of the training set. Page 54 is titled "Validation Set: Preventing Data Leakage" and its text layer holds only the title. Page 47 says cross-validation protects against overfitting by testing on different cases from training.

**Confusion matrix, precision and recall.** `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` p. 56 is titled "Confusion Matrix", with the content in its figure. Page 57 defines precision as TP over TP plus FP, recall as TP over TP plus FN, F1 as the harmonic mean, and says a precise classifier is selective while a high-recall classifier is inclusive. The test confusion matrices and the Jev table above use these definitions per class.

**Cross-validation for tuning.** `Lecture4-LinearModelsforRegression.pdf` p. 67 selects a tuning parameter by cross-validation over a grid. The calibration folds are a different use. They produce held-out predictions to fit the sigmoids, and they tune nothing. I cite the page only as the course's cross-validation idea.

**Probability-based classifiers.** `Lecture5-FundamentalClassificationAlgorithms.pdf` p. 64 titles the Bayes classifier a probability-based method for classification. The lecture does not check whether such probabilities match observed frequencies.

**Pages seen but not used.** `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` pp. 58 to 61 cover ROC curves and AUC. M4 reports no ROC or AUC.

**Lecture 8.** `UTF-8''Lecture8-Hadoop%20Fundamentals%20and%20MapReduce.pdf` has 106 pages and is new since November 2. I searched its text layer for classification, calibration, probability, evaluation and machine learning. The word probability appears on pp. 2 to 3 for hardware failures. Page 15 lists Spark, with machine learning as one application among several. No page supports a confidence, calibration or error-analysis choice. I judge Lecture 8 not relevant to M4. This is a text search of the extracted pages, and I did not render each page to look for image-only content.

**Project choices the slides do not teach.**

- Top-label confidence as a fallback signal and the six thresholds.
- Sigmoid calibration, `CalibratedClassifierCV` and its three group-aware folds.
- Multiclass log loss, the multiclass Brier score and the five-bin reliability diagram with ECE.
- The 0.90 accepted-accuracy target for choosing a threshold.
- Macro-F1 as the main metric. `docs/course-sources.md` states that calibration and macro-F1 are project choices, not lecture mandates.
- Freezing every choice before one final test and a receipt that blocks a second opening.
- Jev as a vendor system and sending test text to it.
- Reading errors as hypotheses by category.

## Your M4 practice questions

Attempt these before asking for a worked answer. Use your own words and this guide's tables. All are unanswered, and no answer or status has been written on your behalf. The first three come from the learning log's last section.

1. Jev lost 0.011 macro-F1 from validation to test, and S1-C1 gained 0.009. Why can a system that was not selected rise on test? (Unanswered.)
2. S1-C1 beat L3-C10 on test. Why must the report keep L3-C10 as the frozen local choice? (Unanswered.)
3. Jev made no error on the 79 inherited M3 test rows. What can and can't you conclude from that? (Unanswered.)
4. S1-C1 gives a margin for calculation and L3-C10 gives a probability of 0.8045 for q0005. Which of the two could you read as a chance of being right, and what would you have to check before trusting it? (Unanswered.)
5. On the test set, calibrated L3-C10's [0.4, 0.6) bin has 46 rows, mean confidence 0.519 and accuracy 0.587. Is the model over or underconfident there? About how many of the 46 were right? Why does its three-row bin [0.2, 0.4) tell you much less? (Unanswered.)
6. Using raw L3-C10's test confusion matrix in this guide, compute precision and recall for the lookup class. Is the class's weakness mainly precision or recall, and what does that mean for a user who needs a lookup? (Unanswered.)
7. Suppose threshold 0.7 had given higher test accuracy than the frozen 0.0. Why can you still not switch to 0.7 in the report, and what would you need to choose it legitimately? (Unanswered.)
8. Thirteen of Jev's test errors are retrieval rows predicted as direct answer. Design one experiment that could test the missing-context hypothesis without reopening this test. What data would it need, and what result would count against the hypothesis? (Unanswered.)
9. Calibration lowered L3-C10's ECE but also lowered its accuracy slightly. Does that mean calibration made the model worse? Explain which metrics changed in which direction. (Unanswered.)

Earlier prompts remain open, including the M3.5 and M3 prompts. Record attempts and feedback in `docs/learning-log.md`.

<!-- pagebreak -->

## Inspected sources

Review date: November 3, 2026. Page numbers are one-based PDF pages. The files are under `/Users/altanesmer/Desktop/SM1/AI/`. I extracted each cited page with `pdftotext`, and the SHA-256 values below were computed with `shasum -a 256` on that date.

- `CourseProjects.pdf`, page 15, and `ProjectRreportInstructions.pdf`, page 1: scope and report requirements.
- `Lecture4-LinearModelsforRegression.pdf`, page 67: cross-validation to select a tuning parameter.
- `Lecture5-FundamentalClassificationAlgorithms.pdf`, pages 2, 5, 53, 56, 64, 79 and 80: unseen testing, separate test set, overfitting, generalization error, Bayes classifier, SVM margins.
- `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf`, pages 47, 52, 53, 54, 56, 57 and 58 to 61: cross-validation, the three data roles, test independence, validation leakage, confusion matrix, precision and recall, ROC and AUC.
- `UTF-8''Lecture8-Hadoop%20Fundamentals%20and%20MapReduce.pdf`, pages 2, 3 and 15 read, and the whole text searched. It is not relevant to M4.

| File | SHA-256 |
| --- | --- |
| `CourseProjects.pdf` | `d4e98da373cbdcd62f804d2cd0f957bbaa53294205762ba6d1dc04b26b74fdca` |
| `ProjectRreportInstructions.pdf` | `00ab8140f009f52fd9f552daa61ade6f628bdd1125096d62c54e07f06e1519a5` |
| `Lecture4-LinearModelsforRegression.pdf` | `8a58746abec856b9168dbca3bd64b446297425570cc78e8c3b378c358d4315cc` |
| `Lecture5-FundamentalClassificationAlgorithms.pdf` | `c2995d1963da118c5b8f599a641a15b2c8ec8102aa61a66fee13a29eeb67980d` |
| `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` | `918f33dc045f3fbbaaae8a33b1a779e9eb7785e8625f1008aa5fc144b49813fd` |
| `UTF-8''Lecture8-Hadoop%20Fundamentals%20and%20MapReduce.pdf` | `997b6d2d5e9114951b0d05713f49d79c98e4f2a074fe2e8dc73bf2f5f31d3098` |

Repository sources: `docs/evidence/m4-final-test.md`, `docs/data-and-evaluation.md` (metrics, confidence and errors; the M4 integration paragraph), `docs/course-sources.md`, `docs/project-plan.md`, `docs/learning-log.md`, `src/orchestra/confidence.py` (`probability_metrics`, `threshold_table`, `calibration_folds`, `_calibrate`, `analyze`, `freeze`, `final_test`), `results/m4-5-validation/`, `results/final-test-m3-5/` and the installed scikit-learn `calibration.py`. The q0005 probabilities come from the two rows for that query in `results/m4-5-validation/predictions.jsonl`. The scratch scripts are `work/m4-guide/check.py`, `check2.py` and `ece_bins.py`.
