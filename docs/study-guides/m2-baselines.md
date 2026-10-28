# M2: validation, group splits, and the first baselines

Study guide edition: October 28, 2026. Runs: `m2-a`, `m2-b`, and the restored rerun `m2-restored`. Data release `m1-v1` (`3e02b6fa…`), split manifest `32a67534…`, predictions `6064c0b1…`, metrics `1690ecd3…`, input archive `253f1103…`. The runs used code at commit `d541de9`. Full hashes are in the appendix. The project is course project 13, Learning to Route Queries in AI Systems.

## What you need to defend

M2 is the first milestone with research numbers. It checks that the frozen M1 release of 128 accepted rows is ready. It splits the rows by group into training, validation, and sealed test partitions. Two baselines are fitted on the training rows and scored on the validation rows.

B0 always predicts the most frequent training class. It scores accuracy 0.24 and macro-F1 0.097 on 25 validation rows. L2 is TF-IDF features with L2-regularized logistic regression at `C = 1`. It gets 18 of 25 rows right, for accuracy 0.72 and macro-F1 0.730.

You should be able to explain five things. Why the split keeps groups together. Why the vectorizer is fitted on training rows only. Why macro-F1 punishes B0 harder than accuracy does. What identical runs establish, and what they do not. Why nobody may choose a confidence threshold from these 25 rows.

M2 is not the classifier comparison. That is M3, with 14 configurations on a larger split. M2 shows that the pipeline runs on real data, reproduces, and produces numbers that trace back to their inputs.

The lesson explains the gate, the split, fitting versus transforming, both baselines, reproduction, and the error inspection, then traces one validation query. The technical appendix gives the equations, the fitted state, and the file identities. Unanswered practice questions and the inspected sources close the guide.

<!-- pagebreak -->

## The readiness gate comes before any split

`scripts/validate_dataset.py` checks every row against the protocol schema. It rejects duplicate IDs, empty text, unknown labels, accepted rows without a label, missing provenance, absent group IDs, exact duplicates, and groups above four rows. The `--ready` flag adds the M1 acceptance checks. It requires at least 120 accepted rows, and at least 30 rows and 15 groups per class. No row may remain `needs_review`. Every source needs a recorded license, and each class needs reviewed rows for at least 20 percent of its rows. Ledger resolutions must equal the dataset labels.

On the frozen release the gate printed "PASS: M1 readiness checks passed (128 accepted rows, 128 reviewed)". `prepare-study` repeats the gate and refuses an empty collection brief. It records the SHA-256 of the dataset, review ledger, sources manifest, and brief, writes an immutable prepared config, and then splits.

These checks establish counts, permissions, and ledger consistency. They cannot tell whether a label is right. A wrong but well-formed label passes. Label correctness rests on Altan's annotation and the disclosed AI-assisted review from M1. The brief's hash also shows that the M3 collection rules existed before anyone saw an M2 error.

## Split by group, not by row

Some rows are close relatives: paraphrases of one request, variants of one scenario, or questions about one public record. Guide v2 gives them one `group_id`. q0079 and q0081 share g084, for example. If one relative sits in training and another in validation, the score gets easier. The model may have learned shared wording instead of the routing decision.

On October 25, Altan explained this mechanism in his own words. It "could make the test score look higher because the model has already seen a similar pattern". The learning log records that as explained independently for that question. The broader leakage topic remains needs practice.

The split assigns whole groups with scikit-learn's `StratifiedGroupKFold`: five shuffled folds, seed 42, rows sorted by query ID. Folds 0 to 2 become training, fold 3 validation, and fold 4 the sealed test. Each fold's own held-out indices are used, so no row lands twice.

| Partition | Rows | Groups | Retrieval | Lookup | Calculation | Direct answer | Share |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Train | 78 | 64 | 19 | 19 | 19 | 21 | 0.6094 |
| Validation | 25 | 22 | 6 | 7 | 6 | 6 | 0.1953 |
| Sealed test | 25 | 22 | 6 | 6 | 7 | 6 | 0.1953 |

The planned 60/20/20 is approximate, because whole groups move together. The project does not break groups to hit exact shares. In validation, q0075 and q0076 share g081, and q0097 and q0098 share g101. Neither pair has a partner in training.

The manifest stores query IDs, group IDs, row hashes, counts, and proportions, but no text. It is written once. Grouping limits one kind of leakage. Training and validation still share sources and writing styles, which matters below.

<!-- pagebreak -->

## Fit on training rows, transform validation rows

Each configuration is a scikit-learn `Pipeline`: a vectorizer, then a classifier. `fit` on the training texts fits both. The vectorizer learns its vocabulary and IDF weights, and the classifier learns coefficients from the resulting matrix. `predict_proba` on validation texts only transforms them with that fitted state. A validation word unseen in training has no column and contributes nothing.

The agent refitted the exact L2 configuration on the 78 training rows on October 28, 2026, in the locked environment. The vocabulary has 643 terms. The training matrix has shape `(78, 643)` with 1,315 stored nonzero entries, so the 10,000-feature cap had no effect. All 25 refit predictions and 100 probabilities equal the saved `m2-a` values exactly.

Fitting the vectorizer on all 128 rows would leak. Validation and test words would enter the vocabulary, and every IDF weight would change, even though no label crossed the boundary. The pipeline makes the training-only rule hold by construction.

The runner enforces the partitions. `run` reads only the train and validation files and checks them against the manifest before fitting. It never opens the full dataset or the sealed test file, and a unit test asserts that. Sealing is a workflow boundary, not encryption. The splitter read every row, and Altan labeled the test rows during M1. That exposure is disclosed.

## B0: the floor that ignores text

B0 is `DummyClassifier(strategy="most_frequent")`. Direct answer has 21 of 78 training rows, so B0 predicts `direct_answer` for every row. It sits behind the same TF-IDF step as L2 only so every configuration has one shape. It never reads the features.

Six validation rows are direct answer, so accuracy is 6/25 = 0.24. Macro-F1 averages four class F1 scores equally. Retrieval, lookup, and calculation are never predicted, so their F1 is zero. Direct answer has recall 1.0 and precision 6/25 = 0.24, so its F1 is 0.387. The average is 0.387 / 4 = 0.097.

Accuracy counts rows. Macro-F1 counts classes, so each ignored class costs a quarter of the score. Validation is nearly balanced, so accuracy is low too. On an imbalanced set, accuracy alone could look good. Macro-F1 as the headline metric is a project choice. Accuracy stays as secondary context.

<!-- pagebreak -->

## L2: TF-IDF with logistic regression

The vectorizer lowercases, keeps tokens matching `(?u)\b\w+\b`, and uses unigrams, no stop words, `min_df=1`, and L2 row normalization. Digits and single characters are kept. The classifier uses `C=1`, the `lbfgs` solver, a pure L2 penalty, `max_iter=100`, an intercept, no class weights, and `random_state=42`. It converged on the first attempt with no warnings. In the agent's refit, it stopped after 10 iterations.

`C = 1` is not tuned. It is one value from the M3 grid of 0.1, 1, and 10, which M3 searches by validation macro-F1.

| Configuration | Correct | Accuracy | Macro-F1 | Never predicted |
| --- | ---: | ---: | ---: | --- |
| B0 | 6 of 25 | 0.24 | 0.097 | retrieval, lookup, calculation |
| L2, C = 1 | 18 of 25 | 0.72 | 0.730 | none |

| L2 class | Precision | Recall | F1 | Support |
| --- | ---: | ---: | ---: | ---: |
| Retrieval | 1.00 | 0.67 | 0.80 | 6 |
| Lookup | 0.71 | 0.71 | 0.71 | 7 |
| Calculation | 0.83 | 0.83 | 0.83 | 6 |
| Direct answer | 0.50 | 0.67 | 0.57 | 6 |

Rows are true labels and columns are predictions.

| True \ predicted | Retrieval | Lookup | Calculation | Direct answer |
| --- | ---: | ---: | ---: | ---: |
| Retrieval | 4 | 0 | 0 | 2 |
| Lookup | 0 | 5 | 1 | 1 |
| Calculation | 0 | 0 | 5 | 1 |
| Direct answer | 0 | 2 | 0 | 4 |

The diagonal holds 18 correct rows. Six of the seven errors involve direct answer, as truth or prediction. The direct-answer column takes four wrong rows, so its precision is 0.50. No other class is predicted as retrieval, so retrieval's precision is 1.00, but two retrieval rows are missed. These are counts, not explanations.

<!-- pagebreak -->

## Trace one validation query

Take q0005, from Altan's own rows: "A train ticket costs 45 kr. How much do three tickets cost?" Its label is calculation, because the price and quantity are given. The numbers come from the agent's refit. Its prediction and probabilities for q0005 match the saved `m2-a` row.

**Tokens.** The vectorizer extracts 12 lowercase tokens: `a`, `train`, `ticket`, `costs`, `45`, `kr`, `how`, `much`, `do`, `three`, `tickets`, `cost`.

**Columns.** `ticket`, `45`, and `tickets` occur in no training row, so they have no column. The number 45 contributes nothing. `ticket` and `tickets` are distinct, because there is no stemming. Nine of the 643 columns are nonzero.

**Weights.** Rare training words weigh more. `costs`, `kr`, `train`, and `cost` each occur in one training row and get 0.376 after normalization. `a` occurs in 30 rows and gets 0.156.

**Scores.** Each class score is its intercept plus the sum of coefficient times feature value. They are retrieval −0.178, lookup −0.358, calculation 0.387, and direct answer 0.148.

**Probabilities.** Softmax gives retrieval 0.201, lookup 0.168, calculation 0.353, and direct answer 0.278.

**Prediction.** L2 predicts calculation, which is correct. The margin over direct answer is 0.075.

The contributions show what drove it. The two largest pushes toward calculation come from `how` (+0.106) and `a` (+0.094). These are function words, not numbers or arithmetic verbs. `three` adds +0.069. `costs` and `kr` add +0.068 each. Their only training occurrence is q0001, Altan's calculation row about a notebook that costs 80 kr.

One word pulls the other way. `train` pushes toward retrieval (+0.051). Its only training occurrence is a Dolly retrieval row asking to extract train tracks from a text. A bag-of-words model gives a train ticket and a train track the same column.

This is a correct prediction made partly for shallow reasons. The number that defines the task is invisible to the model, and the margin is small. One traced row illustrates the mechanism. It does not measure how L2 behaves in general.

<!-- pagebreak -->

## What the repeated runs establish

The agent ran the baselines twice as separate processes, `m2-a` and `m2-b`. `compare` printed "PASS: runs reproduce". The prediction and metric files are byte-identical.

On October 28, 2026, the M2 inputs were archived to `work/m2-archive/m2-inputs.zip`, 47 files. The archive holds the M1 release and review ledger. It holds the M2-time sources manifest and collection brief, extracted from commit `d541de9`, whose hashes match those `prepare-study` recorded. It also holds the split manifest, prepared config, train, validation, and sealed files, the code and lock file, and both run directories. All 47 restored files were byte-identical. After `uv sync --locked`, the rerun `m2-restored` passed `compare` against `m2-a` with the same prediction and metric hashes. The sealed test file was copied as bytes and never opened.

This establishes repeatability. The same inputs, code, and locked environment on one macOS arm64 host give the same bytes, and the archive is complete enough to rebuild M2.

It does not establish generalization, because all three runs score the same 25 rows. It is not independent confirmation, because nothing varied that could expose an error. It is not cross-machine reproduction, which was never tried. Altan drew this distinction in his own notes: identical results "show repeatability on this sample, not independent confirmation".

Provenance records `git_dirty: true`. The only uncommitted file was the new split manifest, committed later with the same hash.

## Resources on this host

| Configuration | Fit seconds | Median latency, 25-row batch, 30 repetitions |
| --- | ---: | ---: |
| B0 | 0.0040 | 0.00025 s |
| L2, C = 1 | 0.0067 | 0.00030 s |

Process peak memory was 122,863,616 bytes, about 117 MiB, including imports. The proposed limits are 15 minutes and 8 GB. These single measurements show that resources are no constraint at this size. They do not predict M3 or embedding costs.

<!-- pagebreak -->

## Error inspection and Altan's hypotheses

On October 26, the agent showed Altan the seven L2 errors and nine correct rows with their probabilities. He wrote five exploratory hypotheses, recorded verbatim in the learning log.

| Query | Source | True | Predicted | Top-two margin |
| --- | --- | --- | --- | ---: |
| q0044 | Dolly | retrieval | direct answer | 0.038 |
| q0047 | Dolly | retrieval | direct answer | 0.085 |
| q0069 | BFCL | lookup | calculation | 0.067 |
| q0084 | BFCL | lookup | direct answer | 0.011 |
| q0090 | BFCL | calculation | direct answer | 0.010 |
| q0117 | No Robots | direct answer | lookup | 0.014 |
| q0130 | No Robots | direct answer | lookup | 0.009 |

In summary, his hypotheses were these:

1. Wording that introduces reference text may matter. Both wrong Dolly rows say "Based on this paragraph". He read this as a "fragile boundary".
2. Small margins could be handled as uncertainty in M4. Some correct rows are close too, so he proposed testing that, "not choosing a threshold yet".
3. Cues such as "table" or "fictional" may help but are neither necessary nor sufficient.
4. L2 may blur needing a particular external record with asking for facts.
5. Source wording or class composition may contribute, which would need source totals to check.

The agent's checks against saved outputs and training text are measurements, not explanations. "Based on this paragraph" occurs in no training row, while "paragraph" occurs in 3 retrieval and 2 direct-answer rows. The four smallest margins of all 25 rows are errors, and the next two, q0045 (0.020) and q0048 (0.027), are correct. Errors by source are Altan-authored 0 of 5, Dolly 2 of 5, BFCL 3 of 10, and No Robots 2 of 5.

In training, all 14 No Robots rows are direct answer and all 13 Dolly rows are retrieval. BFCL covers calculation and lookup, and Altan's rows cover all four classes. Within a single-label source, style and label always occur together, so neither the model nor we can separate them. The M3 brief's second source per class is meant to break that link.

The agent's refit adds one measurement. The direct-answer intercept exceeds the retrieval intercept by 0.293. For q0047 the final raw-score gap is 0.272. Its words moved the scores slightly toward retrieval but did not overcome the intercepts. This describes the fit, not a cause.

A margin cut-off near 0.015 would isolate the four smallest-margin errors. Choosing it here would fit the threshold to these 25 rows, and its success would be optimistic by construction. M4 must choose confidence handling under its own protocol, before the test pass. Seeing these errors is also human exposure. The brief forbids targeting them in M3 collection, and the report must disclose the inspection.

<!-- pagebreak -->

## Course connections

These connections show how course principles support M2's choices. They are not evidence that L2 generalizes. Grouped splitting, macro-F1, B0, `C = 1`, and TF-IDF are project choices.

`CourseProjects.pdf`, page 15 [S1], asks for a classification formulation, classifier and representation comparisons, and confidence and error analysis. M2 supplies the setup and a first error inspection. The comparison is M3.

Lecture 5, pages 2 and 5 [S2], separate a training set that builds the model from a test set that checks it, and warn that the test set must stay separate. Lecture 7, page 52 [S6], divides data into training, validation, and test sets. Its page 54 diagram assigns fitting to training, parameter optimization to validation, and evaluation of generalization to the test set, and marks the first two estimates as biased. That is why M2 keeps the test sealed and sets no threshold on validation.

Lecture 7, page 53 [S6], warns that the test set must be truly independent of training. Grouping is our way to strengthen that when rows come in families. Page 49 describes stratified sampling, which `StratifiedGroupKFold` approximates under the group constraint. Page 50 describes k-fold cross-validation, which averages a metric over folds. M2 uses the folds once, as an allocator, and averages nothing.

Lecture 7, page 56 [S6], shows a confusion matrix where a model predicts only one class and still reaches accuracy 0.9777. Page 68 notes that classifiers tend to favour the majority class. B0 is the extreme case. Page 57 defines precision, recall, and F1 for one positive class. Averaging them over four classes is our extension.

Lecture 6, page 8 [S5], shows a neuron as logistic regression: a weighted sum plus a bias through a sigmoid. L2 computes one weighted sum per class and applies softmax. Lecture 5, pages 88 and 89 [S2], show one-vs-all for multiclass problems. The agent verified that this fit is a single softmax model instead: `predict_proba` equals softmax of the four raw scores.

Lecture 4, pages 61 to 63 [S3], add a squared penalty that shrinks coefficients, trading some bias for lower variance. Page 62 notes that least-squares estimates are very variable when there are fewer rows than features. L2 is a classifier, not a regression, but it has 78 rows and 643 features. Lecture 6, page 17 [S5], lists L2 regularization among regularizers. In scikit-learn, `C` is the inverse of the penalty strength. Lecture 4, page 67 [S3], picks the tuning parameter from a grid by estimated error. Lecture 7, pages 80 and 81 [S6], separate learned parameters from hyperparameters tuned during validation. Vocabulary, IDF weights, coefficients, and intercepts are learned. `C` and the token settings are hyperparameters, fixed in M2 and tuned in M3.

Lecture 2, page 33 [S4], defines feature extraction as a mapping to new features, which TF-IDF is. Lecture 6, pages 57 and 58 [S5], show that a bag of words loses order. The q0005 trace shows a related loss: one `train` column for two meanings. Lecture 5, pages 53 and 55 [S2], and Lecture 7, page 3 [S6], warn about overfitting, insufficient examples, and misleading training error. M2 reports no training score, and its 25-row validation set limits every claim. Lecture 7, page 62 [S6], sets accuracy beside running time, and M2 records both.

<!-- pagebreak -->

## What M2 can contribute to your report

M2 supplies the core of the methods section. Describe the readiness gate, the grouped split with its seed and fold map, the partition table, the training-only pipeline, and the exact B0 and L2 settings. Each claim traces to a hash in this guide.

It also supplies preliminary results: the baseline tables, the confusion table, and the reproduction result, labeled as validation results on 25 rows. The main comparison should come from M3. The source-label confound and the disclosure that errors were seen before M3 collection belong in the limitations.

`ProjectRreportInstructions.pdf`, page 1 [S7], asks for a report in your own words describing the data and models, with visualizations, 5 to 12 pages, in IEEE two-column format, due with the code on December 6, 2026. The partition table and confusion matrix are candidate figures. This guide is study material, not report text.

## What M2 cannot support

- **No model comparison.** Beating a text-blind B0 shows that L2 learned something from text. It does not rank representations or classifiers. That is M3.
- **No test performance.** The sealed test has never been scored.
- **No calibration claim.** L2's probabilities are raw outputs. Nobody has checked whether 0.35 means right 35 percent of the time. That is M4.
- **No threshold.** The margin pattern is a reason to study uncertainty, not a chosen cut-off.
- **Small sample.** One row moves accuracy by 0.04, and per-class F1 rests on six or seven rows. A one- or two-row difference is not a reliable difference.
- **No established cause.** The hypotheses and checks fit several explanations.
- **One host.** Reproduction was shown on one macOS arm64 machine.
- **No understanding claim.** Passing checks and this guide are implementation evidence. Only Altan's answers change the learning record.

<!-- pagebreak -->

## Technical appendix: TF-IDF, softmax, and the penalized loss

The vectorizer uses raw counts, smoothed IDF, and L2 row normalization. Here `n = 78` training rows, and `df(t)` counts training rows containing `t`.

```text
idf(t)    = ln((1 + n) / (1 + df(t))) + 1
raw(t, d) = count(t, d) * idf(t)
x(t, d)   = raw(t, d) / sqrt(sum over terms u of raw(u, d)^2)
```

For q0005, `df = 1` gives `ln(79/2) + 1 = 4.676301`, and `a` with `df = 30` gives `ln(79/31) + 1 = 1.935461`. Each term occurs once, so raw weight equals IDF. The row norm is about 12.425, so 4.676301 becomes 0.376355. Other values: `do` and `much` 0.343722, `three` 0.320569, `how` 0.264784, `a` 0.155768.

Class `k` has a raw score and a softmax probability:

```text
z_k      = b_k + sum over j of w_kj * x_j
p(k | x) = exp(z_k) / sum over classes m of exp(z_m)
```

`W` has shape `(4, 643)`. For q0005, in label order:

| Part | Retrieval | Lookup | Calculation | Direct answer |
| --- | ---: | ---: | ---: | ---: |
| Intercept | −0.0645 | −0.1360 | −0.0281 | 0.2286 |
| `how` | −0.0287 | −0.0052 | 0.1056 | −0.0717 |
| `a` | −0.0375 | −0.1207 | 0.0938 | 0.0644 |
| `three` | −0.0455 | −0.0400 | 0.0686 | 0.0169 |
| `costs` | −0.0197 | −0.0212 | 0.0679 | −0.0270 |
| `kr` | −0.0197 | −0.0212 | 0.0679 | −0.0270 |
| `train` | 0.0507 | −0.0146 | −0.0162 | −0.0199 |
| `do` | 0.0431 | −0.0304 | 0.0263 | −0.0390 |
| `much` | −0.0340 | −0.0270 | 0.0214 | 0.0396 |
| `cost` | −0.0218 | 0.0585 | −0.0200 | −0.0167 |
| Raw score `z` | −0.1776 | −0.3577 | 0.3871 | 0.1481 |
| Probability | 0.2008 | 0.1677 | 0.3533 | 0.2782 |

Each word row is `w_kj * x_j`. Column sums plus the intercept reproduce `z`, and softmax reproduces the saved probabilities. Training minimizes the L2-penalized multinomial log loss in scikit-learn's documented form:

```text
minimize over W, b:
  C * sum over training rows i of -ln p(y_i | x_i)  +  (1/2) * ||W||^2
```

`||W||^2` sums the squared coefficients, and intercepts are not penalized. A smaller `C` strengthens the penalty. `lbfgs` stops when improvement falls below `tol=1e-4` or at `max_iter`. The largest coefficients include `text` (0.869) for retrieval, `id` (0.789) and `the` (0.746) for lookup, `calculate` (0.738) and `i` (0.616) for calculation, and `write` (0.643) for direct answer. Function words carry real weight. That is consistent with the source-style concern but does not prove it.

<!-- pagebreak -->

## Technical appendix: metrics and identities

For class `c`, with undefined values set to zero:

```text
precision_c = TP_c / (TP_c + FP_c)
recall_c    = TP_c / (TP_c + FN_c)
F1_c        = 2 * precision_c * recall_c / (precision_c + recall_c)
macro_F1    = (F1_retrieval + F1_lookup + F1_calculation + F1_direct) / 4
```

For L2, (0.8000 + 0.7143 + 0.8333 + 0.5714) / 4 = 0.7298, reported as 0.730. For B0, (0 + 0 + 0 + 0.3871) / 4 = 0.0968, reported as 0.097.

Each run directory holds config, provenance, outcomes, predictions, metrics, confusion, warnings, timing, and a `manifest.json` that hashes the other eight files. Runs refuse to overwrite. Prediction scores are reordered from scikit-learn's alphabetical class order to the project's label order. `select` is not run on M2.

| Artifact | SHA-256 |
| --- | --- |
| `data/processed/m1-v1.jsonl` | `3e02b6fa8a7c1987a44a6a9ae1c118bac768be16ad05c58d2948880b87633b2e` |
| `data/raw/reviews-v2.jsonl` | `5c449ce1f234490f351e1be7b1843346f46d9c1466136a0b14d5ddb6eb6c2de8` |
| `data/manifests/sources.json`, M2 time | `67cfe73fa3517a87175ebc24f14fdbaeb2566023d1e21f58fc10b6d32c7f7420` |
| `docs/collection-brief.md`, M2 time | `bbfa7ead97e96bcd8ed3457b97e982a3035498f318baebd2f81c90686f8dd65f` |
| `data/splits/m2-split.json` | `32a6753491078b395a57d287329b968a9c7d2cb8628e62ab5abc5477fd56bd07` |
| `data/processed/m2/train.jsonl` | `6f067779fe1a690c4e2ea4720fd814f1d92712099e245641a52abf06e641cac5` |
| `data/processed/m2/validation.jsonl` | `536d2f2904449304ab76ab24465fb8ff3eb0fc94da0bd4bffa42d6b3f79388a0` |
| Predictions, all three runs | `6064c0b106ce97a1fe85012dac4861001e6c8e4fbdec6d4c8b6bf76be8d5174d` |
| Metrics, all three runs | `1690ecd372d57552671ff23db6129b7b48888276c9ba0c9a7eb9f23bbb59ceb4` |
| `work/m2-archive/m2-inputs.zip` | `253f110335b5327b3a256d52452be3b484fe0614de0ffe3c9321944a4b529d0b` |
| `uv.lock` at the runs | `2f51e2b6971c0332c321f4d17163943a98ee7bde7ec3dbd739948fddf2698213` |

Provenance records Python 3.12.13, uv 0.11.7, scikit-learn 1.9.1, numpy 2.5.3, scipy 1.18.1, `macOS-27.0-arm64-arm-64bit`, and single-thread settings. Split and model seeds are both 42.

The refit imported `build_l2` and `load_rows` from `orchestra.experiment` and fitted on the training file only. Against `results/m2-a/predictions.jsonl`, all 25 predictions agreed and the largest probability difference was 0.0. The script ran from a scratch folder and changed no repository file.

<!-- pagebreak -->

## Your M2 practice questions

Attempt these before asking for a worked answer. Use your own words and this guide's tables. No answer or status has been written on your behalf.

1. From the L2 confusion table, compute precision and recall for direct answer and name the cells you used. Why does direct answer have the lowest F1 although its recall equals retrieval's?
2. q0097 and q0098 share g101 and both sit in validation. Suppose a row-level split had put q0097 in training. What could happen to q0098's prediction and the reported score, and which question would that score stop answering?
3. In the q0005 trace, `45` contributes nothing and `train` pushes toward retrieval. Explain both from how the vectorizer was fitted. What do they say about trusting a correct prediction with a 0.075 margin?
4. An examiner says: "Your three identical runs confirm L2's 0.72 accuracy three times." Which part is supported? What would an independent check require?
5. A 0.015 margin threshold would flag the four smallest-margin errors and no correct row. Why may you not adopt it from these 25 rows, and which course page supports your answer?

Earlier prompts remain open. The learning log records the M0 checkpoint as never answered and carried forward. The three October 26 M2 questions, on macro-F1 versus accuracy, the 0.04 step per row, and the sealed test, are unanswered. So are the M1 freeze, collection-brief, and meeting rehearsal prompts. Altan's error hypotheses show that he attempted the error-analysis exercise. They leave the metrics and confidence topics not yet reviewed. Record attempts and feedback in `docs/learning-log.md`.

## Inspected sources

All numbers are one-based PDF page numbers. The files are under `/Users/altanesmer/Desktop/SM1/AI/`. The agent extracted each cited page with `pdftotext` on October 28, 2026, and rendered and viewed the image-based pages: Lecture 4 page 61, Lecture 6 page 8, and Lecture 7 pages 54, 56, and 62.

- [S1] `CourseProjects.pdf`, page 15. Project 13 scope.
- [S2] `Lecture5-FundamentalClassificationAlgorithms.pdf`, pages 2 and 5: training and test sets. Pages 53 and 55: overfitting and insufficient examples. Pages 88 and 89: one-vs-all multiclass.
- [S3] `Lecture4-LinearModelsforRegression.pdf`, pages 61 to 63: ridge penalty, shrinkage, bias and variance. Page 67: choosing the tuning parameter.
- [S4] `Lecture2-Data Preprocessing and Feature Engineering.pdf`, page 33: feature extraction versus selection.
- [S5] `Lecture6-ArtificialNeuralNetworks.pdf`, page 8: neuron and logistic regression. Page 17: L2 regularization. Pages 57 and 58: bag of words loses order.
- [S6] `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf`, page 3: misleading training error. Pages 49, 50, 52, 53, and 54: stratification, k-fold, three sets, test independence, validation leakage. Pages 56 and 57: confusion matrix and F1. Page 62: accuracy and running time. Page 68: majority-class bias. Pages 80 and 81: parameters and hyperparameters.
- [S7] `ProjectRreportInstructions.pdf`, page 1. Report requirements and deadline.

| File | SHA-256 |
| --- | --- |
| `CourseProjects.pdf` | `d4e98da373cbdcd62f804d2cd0f957bbaa53294205762ba6d1dc04b26b74fdca` |
| `ProjectRreportInstructions.pdf` | `00ab8140f009f52fd9f552daa61ade6f628bdd1125096d62c54e07f06e1519a5` |
| `Lecture2-Data Preprocessing and Feature Engineering.pdf` | `e7bfec9a9a52954c038e58a84f680e76648efa582ef79acafe2a3bfaa582217f` |
| `Lecture4-LinearModelsforRegression.pdf` | `8a58746abec856b9168dbca3bd64b446297425570cc78e8c3b378c358d4315cc` |
| `Lecture5-FundamentalClassificationAlgorithms.pdf` | `c2995d1963da118c5b8f599a641a15b2c8ec8102aa61a66fee13a29eeb67980d` |
| `Lecture6-ArtificialNeuralNetworks.pdf` | `4096ea75c917389ad65c0322bb1e045fcba82154ecde673f7221da3440b7d94d` |
| `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` | `918f33dc045f3fbbaaae8a33b1a779e9eb7785e8625f1008aa5fc144b49813fd` |

Implementation references are `src/orchestra/experiment.py`, `splits.py`, `study.py`, `data.py`, `scripts/validate_dataset.py`, and `configs/m2.json`. Evidence comes from `docs/evidence/m2-research-run.md`, the October 28 archive record, the saved runs, and `docs/learning-log.md`. Project decisions are in `docs/data-and-evaluation.md`. Lecture connections support those decisions without making them course requirements.
