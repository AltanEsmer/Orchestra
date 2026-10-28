# M3: comparing representations, classifiers, and regularization

Study guide edition: October 28, 2026. Runs: `m3-a`, `m3-b`, and the restored rerun `m3-restored`. Data release `m3-v1` (`4e9425fd…`), split manifest `6d48e18b…`, predictions `7bac6631…`, metrics `036679a7…`, archive `81e73da8…`. The runs used code at commit `92cbd09`, and the run record was committed as `d04a7ca`. Full hashes are in the appendix. The project is course project 13, Learning to Route Queries in AI Systems.

## What you need to defend

M3 is the main comparison of the project. It freezes a 400-row release, extends the M2 split by whole groups, and fits 14 configurations on 242 training rows. Each is scored on 79 validation rows. A rule fixed before any M3 score existed picks one configuration per family and one overall. The overall choice is L1-C10, word counts with logistic regression at `C = 10`. It scores macro-F1 0.925 and accuracy 0.924. The sealed test was never opened.

The comparison varies the representation (counts or TF-IDF), the classifier (naive Bayes, logistic regression, or a linear SVM), the phrase features (unigrams alone or with bigrams), and the regularization strength `C` (0.1, 1, or 10).

You should be able to explain six things. What each matched comparison holds fixed. How each classifier turns words into a decision. What `C` does. How the rule reaches L1-C10 although L3-C0.1 is within 0.01. Why 79 rows cannot separate the families. What the M2 rows inside M3 validation show about more training data.

M3 has no test score, no human error inspection, and no calibration. Those belong to M4. After the lesson and a one-query trace, the appendices give the equations and file identities.

<!-- pagebreak -->

## The data behind the comparison

The release `m3-v1` has 400 rows, 100 per class, in 360 groups. M1 supplied 128 rows. The M3 import supplied 272 under the collection brief.

| Class | Rows | Groups | Main source | Second source | Altan-authored |
| --- | ---: | ---: | --- | --- | ---: |
| Document retrieval | 100 | 97 | Dolly 75 | No Robots 16 | 9 |
| Knowledge lookup | 100 | 78 | BFCL 62 | AI drafts 28 | 10 |
| Calculation | 100 | 96 | BFCL 75 | GSM8K 16 | 9 |
| Direct answer | 100 | 97 | No Robots 75 | Dolly 15 | 10 |

The import fixed each pool's judging order in advance. No group may exceed four rows, and no request type or source may exceed 40 or 75 of a class's 100 rows.

**What the labels are.** M1's 128 labels are Altan's own, or agent proposals he approved. The 272 new labels are agent proposals approved by an AI reviewer, whose judgments Altan adopted as his A1 labels. A blind AI check agreed on 300 of 302 labelled candidates and disagreed on none. In the release, AI consistency is 399 of 400. That compares one AI judgment with another. The release has no human agreement figure, and the report must say so.

**The split.** `prepare-study` called `extend` with the M2 manifest's hash. Every M2 row kept its partition. New rows were allocated as whole groups.

| Partition | Rows | Groups | New groups | Retrieval | Lookup | Calculation | Direct answer |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Train | 242 | 215 | 151 | 61 | 60 | 60 | 61 |
| Validation | 79 | 72 | 50 | 19 | 21 | 19 | 20 |
| Sealed test | 79 | 73 | 51 | 20 | 19 | 21 | 19 |

The proportions are 60.5, 19.75, and 19.75 percent. Validation holds the 25 M2 validation rows plus 54 new ones. The sealed test file was written by `prepare-study` and never opened.

Sources still align with classes. GSM8K appears only in calculation and the AI drafts only in lookup. Dolly and No Robots now each span two classes, which dilutes the M1 source-label confound without removing it.

## What M3 compares, and what each comparison holds fixed

Every configuration is a scikit-learn `Pipeline` of a vectorizer and a classifier, fitted on training rows only. All vectorizers lowercase, keep tokens matching `(?u)\b\w+\b`, remove no stop words, and use `min_df=1`, `max_df=1.0`, and `max_features=10000`.

| ID | Representation | Classifier | C values |
| --- | --- | --- | --- |
| B0 | none read | `DummyClassifier(strategy="most_frequent")` | none |
| B1 | counts, unigrams | `MultinomialNB` | none |
| L1 | counts, unigrams | `LogisticRegression` | 0.1, 1, 10 |
| L2 | TF-IDF, unigrams | `LogisticRegression` | 0.1, 1, 10 |
| S1 | TF-IDF, unigrams | `LinearSVC` | 0.1, 1, 10 |
| L3 | TF-IDF, unigrams and bigrams | `LogisticRegression` | 0.1, 1, 10 |

Counts come from `CountVectorizer` with `ngram_range=(1, 1)`. TF-IDF comes from `TfidfVectorizer` with `norm="l2"`, `use_idf=True`, `smooth_idf=True`, and `sublinear_tf=False`. L3 sets `ngram_range=(1, 2)`. B0 shares the TF-IDF step only for a uniform shape and never reads the features.

Three matched comparisons each change one thing at the same `C`:

- **L1 to L2** changes counts to TF-IDF. Classifier and unigrams stay fixed.
- **L2 to S1** changes logistic regression to a linear SVM. TF-IDF unigrams stay fixed.
- **L2 to L3** adds bigrams. TF-IDF and logistic regression stay fixed.

When two settings differ at once, a score difference cannot be assigned to either. The q0005 trace meets this problem.

<!-- pagebreak -->

## Counts, TF-IDF, and bigrams

A bag of words turns a query into one number per vocabulary word and forgets the order. With counts, the number is how often the word occurs. Counts are not normalized, so a longer query can reach larger raw scores.

TF-IDF multiplies each count by an inverse document frequency. A word found in few training rows weighs more than a word found in many. Each row is then scaled to length one. The equations are in the appendix.

The training vocabulary has 1,655 unigram columns. Counts and TF-IDF share it, because their token settings are identical, so the 10,000-feature cap has no effect on unigrams. There are far more columns than training rows.

A bigram is a pair of adjacent tokens. L3 adds every training bigram as a column, so it sees some word order. "Good, not bad" and "bad, not good" share every unigram, but "not bad" and "not good" are different bigrams. More columns also mean more weights to estimate from the same 242 rows. In M3, bigrams are the only change whose sign was the same at every `C`.

## How each classifier decides

### Naive Bayes, B1

Naive Bayes applies Bayes' theorem and picks the most probable class given the words. It assumes the words are independent once the class is known. The probability of a query given a class becomes the class prior times one probability per word.

B1 is `MultinomialNB(alpha=1.0, force_alpha=True, fit_prior=True)` on counts. It estimates each word's probability per class from that class's training text. `alpha=1.0` adds one to every word count. A vocabulary word that never occurred in a class therefore gets a small probability instead of a zero that would wipe out the product. `fit_prior=True` takes each prior from the training shares. Smoothing cannot help a word absent from all training rows. That word has no column, and every model ignores it.

The independence assumption is false for text. "How much" and "cost" tend to occur together, but naive Bayes counts each as fresh evidence, which usually pushes its probabilities toward 0 or 1. B1 scores macro-F1 0.883. It finds all 19 retrieval rows but only 14 of 20 direct-answer rows.

### Logistic regression, L1, L2, and L3

Logistic regression gives each class one weight per column plus an intercept. A class's raw score is the intercept plus the sum of weight times feature value. Softmax turns the four scores into probabilities that sum to one.

The code sets `C`, `solver="lbfgs"`, `l1_ratio=0.0`, `tol=1e-4`, `max_iter=100`, `fit_intercept=True`, `class_weight=None`, and `random_state=42`. `l1_ratio=0.0` sets a pure L2 penalty. The code uses it because `penalty` is deprecated in scikit-learn 1.9.1. The code sets no multiclass option. With `lbfgs`, scikit-learn fits one joint softmax model, and the q0005 numbers are consistent with that. A convergence warning would trigger one retry at `max_iter=1000`. None occurred.

Training minimizes the log loss plus a penalty on the squared weights. `C` multiplies the loss. A large `C` lets weights grow to fit the training rows. A small `C` shrinks them toward zero. `C` is therefore the inverse of the regularization strength. Intercepts are not penalized.

### Linear SVM, S1

A linear SVM also computes one weighted sum per class. Training seeks a wide margin and penalizes rows inside it or on the wrong side.

S1 is `LinearSVC` with `C`, `penalty="l2"`, `loss="squared_hinge"`, `dual="auto"`, `tol=1e-4`, `max_iter=1000`, `fit_intercept=True`, `class_weight=None`, and `random_state=42`, with one retry at 10,000 iterations. `multi_class` stays at its default, `"ovr"`. S1 trains four binary classifiers, each separating one class from the rest, and predicts the class with the largest value.

The squared hinge loss is zero when a row's margin is at least one. Below that, the penalty is the squared shortfall. The plain hinge would use the shortfall itself. A larger `C` tolerates fewer training errors, and a smaller `C` prefers a wider margin.

S1 outputs margins from `decision_function`, saved with `score_type: margin`. They can all be negative, need not sum to one, and are not probabilities. M4 plans calibration only for the selected logistic model.

<!-- pagebreak -->

## Regularization strength C

The four `C` families share the grid 0.1, 1, and 10. A larger `C` means weaker regularization and larger weights. In logistic regression, larger weights give more extreme probabilities.

The families peak at different values. L1 rises with `C`, from 0.901 to 0.925. L2 peaks at 1. S1 is best at 0.1. L3 scores 0.923 at all three. Each step is one or two validation rows, so these shapes are weak evidence.

One reason the same `C` need not mean the same strength across representations is feature scale. A nonzero count is at least 1, while q0005's TF-IDF values are at most 0.366. A TF-IDF model needs larger weights for the same score, and the penalty resists them. This is a hypothesis, not a measurement.

With 242 rows and at least 1,655 columns, many weight settings fit the training rows. The penalty prefers small ones. That is the case for regularization here.

## Selection on validation only

The rule is in the code as `SELECTION_RULES`, with `SELECTION_TOLERANCE = 0.01` and `SIMPLICITY_ORDER = ("B0", "B1", "L1", "L2", "S1", "L3")`. The data protocol recorded it before any M3 score existed.

1. Within each family, the tie set is every configuration within 0.01, inclusive, of the family's best validation macro-F1. The smallest `C` wins.
2. Among family winners, the overall tie set is every winner within 0.01 of the best. The earliest family in the simplicity order wins.
3. Latency, then ID, would break a remaining tie. With one winner per family they never decide.

L1, L2, and S1 each have one configuration in their tie set. L3's three all score 0.9232, so the smallest `C` wins. The winners are B0, B1, L1-C10, L2-C1, S1-C0.1, and L3-C0.1. The best is L1-C10 at 0.9245. L3-C0.1, at 0.9232, is within 0.01. L2-C1 and S1-C0.1, at 0.9104, are not. L1 precedes L3 in the order, so the rule picks L1-C10.

L1-C10 also has the higher score, so the rule and the raw ranking agree. The rule still explains why. The choice would stay L1-C10 even if L3-C0.1 had scored up to 0.01 higher. The 0.01 tolerance is smaller than the 0.013 step one row makes in accuracy, so the rule treats such a gap as no evidence. Inside that band it prefers the simpler configuration. L1 uses unigram counts, one readable number per word. L3 uses TF-IDF weights on unigrams and bigrams. L1-C10 also predicts in about half the time, 0.50 against 0.97 ms, although latency played no part.

The data protocol calls the order "an explanatory and computational preference, not a theorem about model complexity". It is a project choice. Preferring the smallest `C` follows the same idea, since it is the strongest penalty.

Selection used validation, so the selected score is optimistic. L1-C10 was chosen partly because it scored highest on these rows. Only the sealed test, scored once in M4 after the choices are frozen, gives an estimate that selection did not touch.

<!-- pagebreak -->

## The results

| Configuration | Accuracy | Macro-F1 | Median latency, 79-row batch |
| --- | ---: | ---: | ---: |
| B0 | 0.253 | 0.101 | 0.54 ms |
| B1 | 0.886 | 0.883 | 0.48 ms |
| L1-C0.1 | 0.899 | 0.901 | 0.50 ms |
| L1-C1 | 0.911 | 0.912 | 0.51 ms |
| **L1-C10** | **0.924** | **0.925** | 0.50 ms |
| L2-C0.1 | 0.899 | 0.898 | 0.59 ms |
| L2-C1 | 0.911 | 0.910 | 0.59 ms |
| L2-C10 | 0.899 | 0.897 | 0.58 ms |
| S1-C0.1 | 0.911 | 0.910 | 0.59 ms |
| S1-C1 | 0.886 | 0.883 | 0.59 ms |
| S1-C10 | 0.886 | 0.883 | 0.59 ms |
| L3-C0.1 | 0.924 | 0.923 | 0.97 ms |
| L3-C1 | 0.924 | 0.923 | 0.95 ms |
| L3-C10 | 0.924 | 0.923 | 0.97 ms |

B0 predicts direct answer for all 79 rows. Retrieval and direct answer tie at 61 training rows, and scikit-learn's sorted class order puts `direct_answer` before `document_retrieval`. Every text-based configuration gets between 70 and 73 rows right.

Matched comparisons, second family minus first, in macro-F1:

| Comparison | C 0.1 | C 1 | C 10 |
| --- | ---: | ---: | ---: |
| Counts to TF-IDF (L1 to L2) | −0.003 | −0.002 | −0.028 |
| Logistic regression to linear SVM (L2 to S1) | +0.012 | −0.027 | −0.014 |
| Unigrams to unigrams and bigrams (L2 to L3) | +0.025 | +0.013 | +0.026 |

**How big is a difference?** One validation row moves accuracy by about 0.013. Every matched difference is about two rows or fewer. No interval or significance test was computed, so none of these differences is established. Counts and TF-IDF are indistinguishable except at `C = 10`, and the SVM's sign depends on `C`. Only bigrams keep one sign at every `C`, but all three signs come from the same 79 rows.

**Same accuracy, different errors.** L1-C10 and L3-C0.1 both get 73 of 79 rows right, but they place their six errors differently. Rows are true labels and columns are predictions.

| L1-C10 | Retrieval | Lookup | Calculation | Direct answer |
| --- | ---: | ---: | ---: | ---: |
| Retrieval | 17 | 0 | 0 | 2 |
| Lookup | 1 | 19 | 0 | 1 |
| Calculation | 0 | 0 | 19 | 0 |
| Direct answer | 0 | 1 | 1 | 18 |

| L3-C0.1 | Retrieval | Lookup | Calculation | Direct answer |
| --- | ---: | ---: | ---: | ---: |
| Retrieval | 19 | 0 | 0 | 0 |
| Lookup | 0 | 19 | 1 | 1 |
| Calculation | 0 | 0 | 19 | 0 |
| Direct answer | 1 | 1 | 2 | 16 |

L1-C10's per-class F1 is 0.919 retrieval, 0.927 lookup, 0.974 calculation, and 0.878 direct answer. Of its six errors, four are No Robots rows, one is BFCL, and one is an AI draft. No human has inspected them. The protocol's inspection of at least 20 validation errors belongs to M4.

**Resources and reproduction.** Peak memory was 161,808,384 bytes, and the slowest fit took 0.023 s. Both runs and the restored rerun `m3-restored` produced identical predictions and metrics. That shows determinism on one host, not generalization.

<!-- pagebreak -->

## M2 rows inside M3 validation

The agent split the saved predictions by each validation row's origin. This analysis was not pre-registered.

| Configuration | M2 rows (25), errors | M2 rows, macro-F1 | New rows (54), errors | New rows, macro-F1 |
| --- | ---: | ---: | ---: | ---: |
| L2-C1 in M2 (78 training rows) | 7 | 0.730 | n/a | n/a |
| L2-C1 in M3 (242 training rows) | 1 | 0.962 | 6 | 0.887 |
| L1-C10 in M3 | 0 | 1.000 | 6 | 0.890 |

On the same 25 rows, with the same settings, L2-C1 made seven errors with 78 training rows and one with 242. Only the training set changed. That change has two parts. The set grew, and its composition changed, with a second source per class and longer word problems. This comparison cannot say whether the gain came from more rows, different rows, or both.

Compare its size with model choice. Within M3, every text-based configuration gets between 70 and 73 of 79 rows right. Growing the training set removed six errors on 25 rows. The row sets differ, so the numbers are not directly comparable. They suggest that, here, training data mattered more than the choice among these models. That is a hypothesis for the discussion, not a finding.

A learning curve would test it. It fits one configuration on growing subsets of the training data and scores each fit on the same validation rows. M3 has two points from two milestones, not a curve. No learning curve is planned.

L1, L2, S1, and L3 all score lower on the 54 new rows than on the 25 M2 rows, while B1 scores about the same on both. Why is not established. The new rows are longer and come from more sources, which is one hypothesis.

Altan inspected the seven M2 errors before M3 collection. The collection followed fixed orders that did not use them, but the exposure must be disclosed.

<!-- pagebreak -->

## Trace one validation query

Take q0005 again, from Altan's own rows: "A train ticket costs 45 kr. How much do three tickets cost?" Its label is calculation, and it is still a validation row. The numbers come from a training-only refit that reproduces the saved `m3-a` scores exactly.

**Tokens and columns.** The vectorizer extracts the same 12 tokens as in M2. The M3 vocabulary has 1,655 columns, and only `ticket` is missing. In M2, `45`, `ticket`, and `tickets` had no column. Now 11 of the 12 tokens count.

**Pushes.** A push is a word's calculation contribution minus its direct-answer contribution, its feature value times the coefficient difference. Every token occurs once, so each L1-C10 count is 1.

| Token | L1-C10 push | L2-C1 TF-IDF value | L2-C1 push |
| --- | ---: | ---: | ---: |
| `how` | +0.762 | 0.189 | +0.080 |
| `three` | +0.585 | 0.279 | +0.052 |
| `costs` | +0.524 | 0.341 | +0.115 |
| `cost` | +0.506 | 0.297 | +0.222 |
| `kr` | +0.476 | 0.366 | +0.093 |
| `do` | +0.308 | 0.287 | −0.002 |
| `much` | +0.296 | 0.259 | +0.062 |
| `a` | +0.227 | 0.120 | −0.032 |
| `45` | +0.146 | 0.341 | +0.077 |
| `tickets` | +0.069 | 0.366 | +0.005 |
| `train` | +0.011 | 0.366 | +0.007 |
| `ticket` | no column | no column | no column |
| Intercept difference | −2.707 | | −0.236 |

**Probabilities.** In label order retrieval, lookup, calculation, direct answer, L1-C10 gives 0.0345, 0.0151, 0.7308, and 0.2197. L2-C1 gives 0.1858, 0.1677, 0.3939, and 0.2526. B1 gives calculation 0.9902. In M2, L2 at `C = 1` with 78 training rows gave calculation 0.353. All three M3 models predict calculation, which is correct.

The trace shows three things.

First, L1-C10 works on a larger scale. Its pushes sum to +3.910 against L2-C1's +0.679, and its intercept difference is −2.707 against −0.236. All eleven of its words push toward calculation and outweigh an intercept that leans toward direct answer. Two settings differ. `C = 10` is a weaker penalty than `C = 1`, so it allows larger weights. A count of 1 also exceeds every TF-IDF value here, so the same weight gives a larger push. One trace cannot apportion the effect between them.

Second, weighting changes which words matter. Under counts, the function word `how` pushes hardest. Under TF-IDF, `how` gets 0.189 because it is common in training, and `cost` leads. `kr`, `tickets`, and `train` share the largest value, 0.366, so they are the rarest of these words in training.

Third, B1 is the most extreme. 0.9902 fits the usual account of naive Bayes overconfidence, in which related words multiply as if independent. One correct row cannot show miscalibration, and it does not measure general behavior.

<!-- pagebreak -->

## Course connections

Course concepts support M3's design but do not show that L1-C10 generalizes. Each paragraph gives the course concept, then the project choice.

**Scope.** `CourseProjects.pdf` p. 15 [S1] asks Project 13 to compare classifiers and feature representations and to analyze confidence and errors. M3 does the comparison. Confidence and errors are M4.

**Representation.** `Lecture6-ArtificialNeuralNetworks.pdf` p. 57 [S5] turns a sentence into a bag-of-words vector, and page 58 shows two sentences that differ only in word order. `Lecture2-Data Preprocessing and Feature Engineering.pdf` p. 33 [S4] defines feature extraction, and page 31 warns that more features do not always improve accuracy. The project choices are TF-IDF, row normalization, and bigrams. No inspected lecture teaches TF-IDF, and `CourseProjects.pdf` p. 11 [S1] names it only for Project 9. The normalization on `Lecture2-Data Preprocessing and Feature Engineering.pdf` p. 28 rescales one attribute across records, while TF-IDF rescales each row.

**Naive Bayes.** `Lecture5-FundamentalClassificationAlgorithms.pdf` p. 64 [S2] states Bayes' theorem. Pages 67 and 68 state the independence assumption and estimate the probabilities from counts. Page 72 shows that one zero probability zeroes the product and gives the Laplace correction. Page 74 says naive Bayes suits text but independence may not hold. The project choices are the multinomial form over word counts and `alpha=1.0`.

**Logistic regression.** `Lecture6-ArtificialNeuralNetworks.pdf` p. 8 [S5] shows a neuron as logistic regression, a sigmoid of a weighted sum plus a bias. Page 17 lists L2 regularization. `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` p. 36 [S6] writes an objective as training loss plus regularization, with a logistic loss and an L2 norm. The inspected lectures do not develop softmax for several classes. The project choices are the four-class softmax form, `lbfgs`, and scikit-learn's `C`, which weights the loss instead of the penalty.

**SVM.** `Lecture5-FundamentalClassificationAlgorithms.pdf` p. 78 [S2] presents the SVM as the widest linear separation. Page 80 gives the soft margin, with a linear penalty when a margin falls below 1. Page 86 describes `C` as the misclassification penalty. Page 89 shows one-vs-all, predicting the class with the largest weighted sum. The project choices are a linear SVM without the kernels of page 83 and the squared hinge, which squares the shortfall that page 80 penalizes linearly.

**Regularization.** `Lecture4-LinearModelsforRegression.pdf` p. 61 [S3] adds a penalty of lambda times the sum of squared coefficients, shrinking them as lambda grows. Pages 62 and 63 say estimates are extremely variable when rows are fewer than features and state the bias and variance trade-off. `Lecture5-FundamentalClassificationAlgorithms.pdf` p. 53 [S2] defines overfitting as a model more complex than necessary. The project choices are `C` as the inverse of lambda and the grid 0.1, 1, and 10.

**Validation and selection.** `Lecture4-LinearModelsforRegression.pdf` p. 67 [S3] picks a tuning parameter from a grid by estimated error. `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` p. 52 [S6] divides data into training, validation, and test sets. Its page 54 diagram assigns parameter optimization to validation, marks that estimate as biased, and keeps the test set independent. Pages 80 and 81 separate parameters from hyperparameters. `Lecture5-FundamentalClassificationAlgorithms.pdf` p. 57 [S2] states Occam's razor, preferring the simpler of two models with similar error. The project choices are one validation set instead of cross-validation, the 0.01 tolerance, the smallest-`C` rule, and the simplicity order.

**Metrics.** `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` p. 56 [S6] shows a confusion matrix, page 57 defines precision, recall, and F1, and page 62 sets accuracy beside running time. Macro-averaging and the latency column are project choices.

**More data.** `UTF-8''Lecture1-Introduction%20to%20Big%20Data%20Analytics.pdf` p. 50 [S8], "No data like more data!", shows several learners' test accuracy rising with training words, with curves that cross. `Lecture5-FundamentalClassificationAlgorithms.pdf` p. 55 [S2] blames misclassification on too few training records. The M2-rows analysis is a project choice.

| Course concept | Project choice |
| --- | --- |
| Bag of words, Bayes' theorem, Laplace smoothing | TF-IDF, bigrams, multinomial naive Bayes |
| Logistic model, L2 penalty, soft margin, one-vs-all | Softmax, squared hinge, the `C` convention |
| Three data roles, Occam's razor, F1 | 0.01 tolerance, simplicity order, macro-F1 |

<!-- pagebreak -->

## What M3 can contribute to your report

For methods, M3 supplies the release with its sources and limits, the grouped extension, the exact settings of all 14 configurations, the matched comparisons, and the selection rule fixed in advance. For results, it supplies the validation table, the matched comparisons, the family selections, and the L1-C10 confusion matrix, each labeled as validation on 79 rows. The M2-rows analysis belongs in the discussion as exploratory. Label provenance, source alignment, and the exposure of the M2 errors belong in the limitations.

`ProjectRreportInstructions.pdf` p. 1 [S7] asks for an own-words report on the data and models, with visualizations, 5 to 12 pages, IEEE two-column, due with the code on December 6, 2026. A macro-F1 chart by family and `C` is a candidate figure, but plots wait on a dependency decision. This guide is study material, not report text.

## What M3 cannot support

- **No test performance.** The sealed test was never opened. M4 scores it once, after the systems and any threshold are frozen.
- **No ranking of families.** Differences are two rows or fewer, with no interval. "Counts beat TF-IDF" and "logistic regression beats the SVM" are unsupported. Bigrams show a consistent sign, not an established effect.
- **An optimistic score.** L1-C10's 0.925 comes from the rows that chose it.
- **No error analysis.** No human has inspected the M3 errors.
- **No calibration claim.** Probabilities are raw outputs, and S1 margins are not probabilities.
- **No human agreement.** The 272 new labels are human-adopted AI judgments. 399 of 400 is AI consistency.
- **Source cues remain.** Four of L1-C10's six errors are No Robots rows. Whether source style drives predictions is untested.
- **No cause for the data effect.** The M2-rows analysis cannot separate more rows from different rows.
- **One host, one seed, one split.** Identical reruns show determinism, not generalization.
- **No understanding claim.** Only Altan's answers change the learning record.

<!-- pagebreak -->

## Technical appendix: representations and models

Here `n = 242` training rows, `df(t)` counts training rows containing `t`, and `V = 1,655` is the unigram vocabulary size.

```text
count(t, d) = number of times t occurs in query d
idf(t)      = ln((1 + n) / (1 + df(t))) + 1
raw(t, d)   = count(t, d) * idf(t)
x(t, d)     = raw(t, d) / sqrt(sum over terms u of raw(u, d)^2)
```

L1 and B1 use `count(t, d)`. L2, S1, and L3 use `x(t, d)`. In q0005 every count is 1, so equal TF-IDF values mean equal document frequency, and the squared values sum to one.

Multinomial naive Bayes with `alpha = 1`, where `N(w, c)` counts word `w` in class `c`'s training text and `N(c)` is that class's total:

```text
P(c)       = training rows of class c / 242
P(w | c)   = (N(w, c) + 1) / (N(c) + V)
score(c,d) = ln P(c) + sum over w of count(w, d) * ln P(w | c)
```

Multinomial logistic regression, for L1, L2, and L3:

```text
z_k      = b_k + sum over j of w_kj * x_j
p(k | x) = exp(z_k) / sum over classes m of exp(z_m)
minimize over W, b:
  C * sum over training rows i of -ln p(y_i | x_i)  +  (1/2) * ||W||^2
```

Linear SVM, one-vs-rest, where `y_ik` is +1 if row `i` has class `k` and −1 otherwise. `LinearSVC` also penalizes its intercept.

```text
for each class k:
  minimize (1/2) * ||w_k||^2 + C * sum over i of max(0, 1 - y_ik * (w_k . x_i + b_k))^2
prediction = the class k with the largest w_k . x + b_k
```

Trace arithmetic on the rounded values. L1-C10's eleven pushes sum to +3.910, and with the −2.707 intercept difference the calculation score exceeds direct answer's by +1.203. For L2-C1 the sum is +0.679 and the gap is +0.443. Under softmax, a probability ratio equals `exp` of the score gap. `ln(0.7308 / 0.2197)` is about 1.202 and `ln(0.3939 / 0.2526)` about 0.444, matching within rounding. One-vs-rest probabilities would not satisfy this identity in general.

## Technical appendix: selection, metrics, and identities

Worked selection in validation macro-F1 from `comparison.md`:

| Family | C 0.1 | C 1 | C 10 | Tie set | Chosen |
| --- | ---: | ---: | ---: | --- | --- |
| L1 | 0.9012 | 0.9123 | 0.9245 | L1-C10 | L1-C10 |
| L2 | 0.8980 | 0.9104 | 0.8970 | L2-C1 | L2-C1 |
| S1 | 0.9104 | 0.8831 | 0.8829 | S1-C0.1 | S1-C0.1 |
| L3 | 0.9232 | 0.9232 | 0.9232 | all three | L3-C0.1 |

L1's cutoff, 0.9245 − 0.01 = 0.9145, excludes L1-C1. L2's and S1's cutoffs, 0.9004, exclude their other values. The overall cutoff, 0.9145, admits L3-C0.1 and excludes L2-C1, S1-C0.1, and B1 (0.8833). `within_tolerance` rounds to 12 decimals, so a gap of exactly 0.01 counts as inside.

```text
precision_c = TP_c / (TP_c + FP_c)
recall_c    = TP_c / (TP_c + FN_c)
F1_c        = 2 * TP_c / (2 * TP_c + FP_c + FN_c)
macro_F1    = mean of the four class F1 values
```

For L1-C10, retrieval is 34/37, lookup 38/41, calculation 38/39, and direct answer 36/41, giving 0.919, 0.927, 0.974, and 0.878, mean 0.9245. For B0, direct answer is 40/99 = 0.404 and the rest are zero, so macro-F1 is 0.101.

| Artifact | SHA-256 |
| --- | --- |
| `data/processed/m3-v1.jsonl` | `4e9425fd65e2572bff1c7fefd9ef21692bf219479818903d4ec33a372fc55bbf` |
| `data/raw/m3-reviews-v1.jsonl` | `e56b73a22a0e95893fb19efcbde1717ae803fb52ffa0ce668cbceb384a3248e9` |
| `data/splits/m3-split.json` | `6d48e18bae6ac319bffecc98c68b6b02c8c4483f68a75eddb63db2a52213225f` |
| `data/processed/m3-prepared.json` | `b19fccf5565eb1673f034678e682751f7e8993c6e85501c6ad95e7bca6754ecc` |
| `data/processed/m3/train.jsonl` | `5b6b6254028e910c73db7c9588ddff8d1a4a7598aed25140adb275086289d3dd` |
| `data/processed/m3/validation.jsonl` | `5cdda69c02ce8c90fe45a16348fb53d3c84e7efa048d72891129b086149756b6` |
| `docs/collection-brief.md`, as recorded | `d9238b34b573438c648ebd90cd4bc8564b2a6698ccba7b26ee8d0726d5105233` |
| Predictions, all three runs | `7bac66319eee0fdaa929d8838bf42a8f1a68907df55c66117c81bd94541598fa` |
| Metrics, all three runs | `036679a7f1e769b2f0514e22cd8f5c55dc0c256012767c8630bb29728a9cc367` |
| `work/m3-archive/m3-release.zip` | `81e73da8292c50ab68cf140e44d6070b4ac1643aaa038feae671f66a30b36d8c` |

The run record names scikit-learn 1.9.1, NumPy 2.5.3, SciPy 1.18.1, and macOS arm64 with 12 CPUs, with thread variables set to 1. The model seed is 42. Provenance records `git_dirty: false`.

<!-- pagebreak -->

## Your M3 practice questions

Attempt these before asking for a worked answer. Use your own words and this guide's tables. No answer or status has been written on your behalf.

1. Suppose the family winners had scored L1-C10 0.925, L2-C1 0.928, and L3-C0.1 0.934, with the others unchanged. Apply the overall rule step by step. Which configuration is chosen, and which step decides?
2. L1-C10 and L3-C0.1 both get 73 of 79 rows right. From the two confusion tables, compute direct-answer precision, recall, and F1 for L3-C0.1. Why can equal accuracy still give different macro-F1?
3. In the q0005 trace, L1-C10 gives calculation 0.7308 and L2-C1 gives 0.3939. Name the two settings that differ. Which saved configuration would you trace next to separate their effects, and what result would point to `C`?
4. `ticket` has no column, while some vocabulary words never occur in calculation's training text. What does `alpha=1.0` do for the second kind, and why can it not help the first? Why does B1's 0.9902 not show miscalibration?
5. S1 predicts with one-vs-rest margins. How could all four margins be negative while S1 still predicts a class? What would you need before quoting an S1 margin as confidence in your report?

Earlier prompts remain open, including the learning log's M3 prompts and the M1 and M2 guide questions. The topic ledger schedules naive Bayes, logistic regression and regularization, SVM, and model selection for this comparison. All four are not yet reviewed. Record attempts and feedback in `docs/learning-log.md`.

## Inspected sources

Review date: October 28, 2026. Page numbers are one-based PDF pages. The files are under `/Users/altanesmer/Desktop/SM1/AI/`. The agent extracted each cited page with `pdftotext` and viewed the rendered image of every page whose content is a figure or formula.

- [S1] `CourseProjects.pdf`, page 11: TF-IDF named for Project 9. Page 15: Project 13 scope.
- [S2] `Lecture5-FundamentalClassificationAlgorithms.pdf`, pages 53, 55, and 57: overfitting, insufficient examples, Occam's razor. Pages 64, 67, 68, 72, and 74: naive Bayes. Pages 78, 80, 83, 86, and 89: SVM, soft margin, kernels, `C`, one-vs-all.
- [S3] `Lecture4-LinearModelsforRegression.pdf`, pages 61 to 63: ridge penalty, variance, bias. Page 67: tuning from a grid.
- [S4] `Lecture2-Data Preprocessing and Feature Engineering.pdf`, page 28: normalization. Page 31: dimensionality. Page 33: feature extraction.
- [S5] `Lecture6-ArtificialNeuralNetworks.pdf`, page 8: neuron and logistic regression. Page 17: loss plus regularizer. Pages 57 and 58: bag of words loses order.
- [S6] `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf`, page 36: loss plus L2 norm. Pages 52 and 54: three sets, validation bias. Pages 56, 57, and 62: confusion matrix, F1, running time. Pages 80 and 81: hyperparameters.
- [S7] `ProjectRreportInstructions.pdf`, page 1: report requirements.
- [S8] `UTF-8''Lecture1-Introduction%20to%20Big%20Data%20Analytics.pdf`, page 50: more training data.

| File | SHA-256 |
| --- | --- |
| `CourseProjects.pdf` | `d4e98da373cbdcd62f804d2cd0f957bbaa53294205762ba6d1dc04b26b74fdca` |
| `ProjectRreportInstructions.pdf` | `00ab8140f009f52fd9f552daa61ade6f628bdd1125096d62c54e07f06e1519a5` |
| `UTF-8''Lecture1-Introduction%20to%20Big%20Data%20Analytics.pdf` | `9f16e0d8d8fc24ca12a4c93e4cca3fcdb26bec5f8a6c80cece83e2ed0ed8e1ee` |
| `Lecture2-Data Preprocessing and Feature Engineering.pdf` | `e7bfec9a9a52954c038e58a84f680e76648efa582ef79acafe2a3bfaa582217f` |
| `Lecture4-LinearModelsforRegression.pdf` | `8a58746abec856b9168dbca3bd64b446297425570cc78e8c3b378c358d4315cc` |
| `Lecture5-FundamentalClassificationAlgorithms.pdf` | `c2995d1963da118c5b8f599a641a15b2c8ec8102aa61a66fee13a29eeb67980d` |
| `Lecture6-ArtificialNeuralNetworks.pdf` | `4096ea75c917389ad65c0322bb1e045fcba82154ecde673f7221da3440b7d94d` |
| `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` | `918f33dc045f3fbbaaae8a33b1a779e9eb7785e8625f1008aa5fc144b49813fd` |

Repository sources: `docs/evidence/m3-research-run.md` at `d04a7ca`, `docs/evidence/m3-import.md`, `results/m3-a-report/comparison.md`, `src/orchestra/experiment.py` (model settings and selection rule), `configs/m3.json`, `docs/data-and-evaluation.md`, `docs/course-sources.md`, `docs/learning-log.md`, `docs/study-guides/m2-baselines.md`, and `docs/study-guides/README.md`. The q0005 probabilities were checked against its 14 rows in `results/m3-a/predictions.jsonl`, which hold no text.
