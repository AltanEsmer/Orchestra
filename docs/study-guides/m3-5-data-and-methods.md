# M3.5: more public data, trees, boosting, and Jev

Study guide edition: November 3, 2026. Runs: `m3-5-full-a` and `m3-5-full-b`, plus the restored rerun `m3-5-full-restored`. Data release `m3-5-v1` (`be747dda…`), split manifest `7aacbc49…`, predictions `453807b4…`, metrics `104c7a2c…`, selection `6a247792…`. The runs used code at commit `031e4e9` with `git_dirty: true`. The first run record attributes that flag to two untracked folders, `output/` and `tmp/`. Full hashes are in the appendix. The project is course project 13, Learning to Route Queries in AI Systems.

## What you need to defend

M3.5 answers a supervisor request. After the M3 comparison on 400 rows, the supervisor asked for more public data and more methods. You chose four new methods: Decision Tree, Random Forest, XGBoost, and TypeSafe's Jev. The milestone has two parts. It grows the data from 400 rows to 3,145, and it compares 27 configurations instead of 14. The validation set grew too, from 79 to 629 rows.

The selected system is Jev, with validation macro-F1 0.975. The best local model is L3-C10, word and word-pair TF-IDF with logistic regression at `C = 10`, with 0.952. The frozen rule picks Jev because it leads by 0.023, more than the 0.01 tolerance. No test score exists. The sealed test was not opened.

You should be able to explain seven things. How the 3,145 labels were made and why they are not human ground truth. Why the classes are unequal. How a tree, a forest and a boosted model each turn words into a decision. Why Jev is a different kind of system, not a swapped classifier. How the selection rule reached Jev. What the two Jev passes show about reproducibility. Why a 0.023 gap on one validation set is still not a test result.

M3.5 has no test score, no human error inspection, and no M4 calibration claim. After the lesson and a one-query trace, the appendix gives the equations and file identities.

<!-- pagebreak -->

## The data

The release `m3-5-v1` has 3,145 accepted rows. The 400 M3 rows are unchanged. 2,745 rows are new. Source: `docs/evidence/m3-5-dataset.md`.

| Class | Rows | Share | Groups | Largest request type |
| --- | ---: | ---: | ---: | --- |
| Document retrieval | 1,000 | 31.8% | 982 | document question 400 (40.0%) |
| Direct answer | 1,000 | 31.8% | 960 | factual question 245 (25%) |
| Calculation | 651 | 20.7% | 562 | word problem 260 (39.9%) |
| Knowledge lookup | 494 | 15.7% | 223 | keyed record 105 (21%) |

The shares are my arithmetic from the row counts. **The release is not near-balanced.** Altan first chose a near-balanced 2,000-row design. When more data became the priority, he chose "up to 1,000 per class" and "keep all rules". Lookup stops at 494 because every listed lookup pool was walked. Calculation stops at 651 because its other sources ran out, and the 40% word-problem cap holds back the remaining GSM8K rows. Nothing was padded or switched to fill a class.

**The split.** `prepare-study` extended the pinned M3 split by whole groups. Every M3 row kept its partition.

| Partition | Rows | Groups | Retrieval | Lookup | Calculation | Direct answer |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Train | 1,888 | 1,628 | 601 | 296 | 390 | 601 |
| Validation | 629 | 545 | 199 | 100 | 130 | 200 |
| Sealed test | 628 | 546 | 200 | 98 | 131 | 199 |

The proportions are 0.600, 0.200 and 0.200. The sealed test was never opened. Only 38 rows are Altan-authored, 9 retrieval, 10 lookup, 9 calculation and 10 direct answer, and 5 of them are in validation.

**Sources.** Most rows are public text kept as written. The release record lists these by class:

| Class | Sources (rows) |
| --- | --- |
| Retrieval | No Robots 501, Dolly 490, Altan 9 |
| Lookup | DataBench 206, ToolACE 68, BFCL 62, ToolAlpaca 58, CLINC150 48, AI drafts 28, MASSIVE 14, Altan 10 |
| Calculation | GSM8K 255, CLINC150 117, TheoremQA 99, BFCL 82, MASSIVE 43, oasst2 37, Altan 9, Glaive 7, Dolly 2 |
| Direct answer | No Robots 598, Dolly 267, MASSIVE 69, CLINC150 56, Altan 10 |

Every class has at least two sources, and none exceeds 75%. Public does not mean human-written. ToolACE, ToolAlpaca and Glaive are generated, and the 28 lookup AI drafts came from M3.

**How the labels were made.** This is the weakest part of the data, so know it exactly.

1. An AI screen (Claude Sonnet 5.5, medium effort) proposed a label for 7,206 candidate rows. It saw each row's source.
2. A separate blind AI check (Claude Opus 5.5, high effort) labeled 3,828 rows without seeing the source or the screen's label. The two checks gave the same label on 3,676 rows, 96.0%.
3. Rows with a clear agreement and no flag were accepted without a human. Those are 2,471 of the 2,745 new rows.
4. 727 flagged or disagreeing rows went to Altan. He answered three worksheets by theme, each time adopting the defaults the agent proposed. 274 of those rows entered the release.

So the new labels are AI labels with human adjudication of disagreements. Altan did not label rows one by one, and the anchoring risk is high. Both checks are Claude models, so shared bias is possible. **No human agreement figure exists.** The 96.0% compares one AI judgment with another. The validator's `ai_consistency` of 3,143 of 3,145 counts accepted rows after adjudication, so it is not an agreement rate. The 400 M3 rows keep their M3 labels.

Two more points. Guide v3 added two lookup rules: a question about a table kept outside the router text counts as lookup, and the user's own stores count as structured sources. And "dataset" is almost a lookup-only cue: 195 lookup rows use it, against 6 rows in other classes.

<!-- pagebreak -->

## The four new methods

All three local families read the same training-only unigram TF-IDF as L2 and S1. The vocabulary has 7,000 columns, and the 10,000-feature cap does not bind. Every configuration uses seed 42 and one CPU thread. The 14 M3 configurations are rerun unchanged on the new split.

| Family | Grid | Fixed settings | IDs |
| --- | --- | --- | --- |
| DT | `max_depth` 10 or 30, `min_samples_leaf` 1 or 3 | `criterion="gini"`, no class weights | `DT-d10-leaf1` to `DT-d30-leaf3` |
| RF | `max_depth` 30 or none, `min_samples_leaf` 1 or 3 | 200 trees, bootstrap, `max_features="sqrt"`, `n_jobs=1` | `RF-d30-leaf1` to `RF-dNone-leaf3` |
| XGB | `max_depth` 3 or 6, `learning_rate` 0.05 or 0.1 | 200 rounds, `multi:softprob`, `tree_method="hist"`, `n_jobs=1` | `XGB-d3-lr0.05` to `XGB-d6-lr0.1` |
| Jev | none | model `jev-1.14.0`, one frozen four-option question | `Jev` |

The settings come from `docs/m3-5-plan.md` section 3 and from `build_dt`, `build_rf` and `build_xgb` in `src/orchestra/experiment.py`. The saved `config.json` shows every other XGBoost setting as unset, so it keeps the library default. That makes 4 + 4 + 4 + 1 = 13 new configurations beside the old 14, 27 in all.

### Decision Tree

A tree asks a chain of yes/no questions about the query. Each question tests one word: is this word's TF-IDF value at most a threshold? Training picks, at each node, the test that makes the child nodes purest, measured by Gini impurity. Growth stops at `max_depth` or when a leaf would have fewer than `min_samples_leaf` rows. A leaf predicts the class mix of the training rows that reached it.

A tree can fit any training set if it grows deep enough. That is its risk. `max_depth` and `min_samples_leaf` are the two brakes. A tree needs no scaling and can combine words, but one tree is unstable, since a small data change can change early splits.

### Random Forest (bagging)

A forest trains many trees and combines them. Each of the 200 trees sees a bootstrap sample, a random draw of training rows with replacement. At each split, a tree may test only a random subset of the words, `sqrt` of the vocabulary size. About 83 of 7,000 words is my arithmetic. The trees disagree in different places, and averaging their votes cancels much of that disagreement. This lowers variance.

The forest's score for a class is the mean of the trees' class probabilities. scikit-learn averages probabilities, where the lecture describes a majority vote. The two give the same answer on most rows.

### XGBoost (boosting)

Boosting builds trees one after another. Each new tree corrects what the earlier ones got wrong, and a small `learning_rate` shrinks each correction. With four classes the library fits one tree per class in every round. A refit I ran produced 800 trees from 200 rounds, which is 200 times 4. The class scores add up over rounds, and softmax turns the final scores into probabilities. Trees here are shallow, depth 3 or 6, because boosting wants weak trees. Boosting can reduce bias, but many rounds can overfit.

**Sparse semantics.** XGBoost treats an absent entry in a sparse matrix as missing, not zero. A word that does not occur follows each split's learned default branch. A fixture test confirmed that this holds for the TF-IDF matrix (`docs/evidence/m3-5-classifiers.md`). XGBoost also rejects string labels, so the code wraps it to fit on integer codes and decode them.

### TypeSafe Jev

Jev is a pretrained decision model reached through an API. The adapter sends one request per query. The body holds the unchanged query text, a fixed question, "which action must the assistant take first", and four options with short criteria that paraphrase the annotation guide. The API returns a choice and four option probabilities. No label, rationale, source or attachment is sent.

**Why this is a system comparison.** The other 26 configurations differ in the classifier, and some differ in the features. Jev has no TF-IDF step and no fitting on your 1,888 training rows. It reads written rules, was pretrained by someone else on unknown data, runs on a vendor's server, and costs a price per token. Its "fit" is replaying a saved answer log. A gap between Jev and L3-C10 mixes model, pretraining, input form and rule wording. You cannot read it as "a better classifier on the same features". The plan says to report Jev as a separate system comparison. Its probabilities are kept. Its separate `confidence` field is saved and not used.

<!-- pagebreak -->

## Selection on validation only

The rule was frozen before any M3.5 score existed. It lives in the code as `M3_5_RULES`, `SELECTION_TOLERANCE = 0.01` and the order `("B0", "B1", "L1", "L2", "S1", "L3", "DT", "RF", "XGB", "Jev")`.

1. Within each family, the tie set is every configuration with validation macro-F1 at least best minus 0.01 (inclusive). The family's tie rule picks one member.
2. Tie rules: the smallest `C` for L1, L2, S1 and L3. For DT and RF, the shallowest depth, then the largest `min_samples_leaf`, with unlimited depth last. For XGB, the shallowest depth, then the lowest learning rate. These are declared conventions, not theorems about complexity.
3. Overall, the tie set is every family winner within 0.01 of the best winner. The earliest family in the order wins. Latency, then ID, would break a remaining tie.

Here is the rule on the saved scores from `results/m3-5-full-a-selection.json` and `metrics.json`.

| Family | Scores in the tie set | Chosen |
| --- | --- | --- |
| L1 | C1 0.9216, C10 0.9185 | L1-C1 |
| L2 | C1 0.9239, C10 0.9324 | L2-C1 |
| S1 | C1 0.9358, C10 0.9402 (C0.1 at 0.9280 is 0.0122 below the best) | S1-C1 |
| L3 | C10 0.9524 (alone; C1 at 0.9297 is 0.0227 below) | L3-C10 |
| DT | d30-leaf1 0.8176 (alone) | DT-d30-leaf1 |
| RF | dNone-leaf1 0.9131 (alone) | RF-dNone-leaf1 |
| XGB | d6-lr0.05 0.9010, d6-lr0.1 0.9066 | XGB-d6-lr0.05 |

L2 and S1 show the point of the rule. In both, the highest score is at `C = 10`, but the gap to `C = 1` is under 0.01, so the smaller `C` wins. This prefers the stronger penalty when the evidence cannot separate the two.

**Overall.** The family winners include Jev at 0.9753 and L3-C10 at 0.9524. The cutoff is 0.9753 minus 0.01, which is 0.9653. L3-C10 is 0.0229 below Jev and falls outside the cutoff. Every other winner is lower still. The tie set is Jev alone, so the order that favors local models has nothing to break, and Jev is chosen. The selection file records `valid: true` and `overall: Jev`.

The M3.5 order lists the local families before Jev on purpose. In a near-tie the rule prefers the established local workflow. That is a project choice, not a claim that local models generalize better. Here the preference never applied.

Selection used validation, so Jev's 0.975 is optimistic. Only the sealed test, scored once in M4 after the frozen decisions, gives an estimate that selection did not touch.

<!-- pagebreak -->

## The results

Sources: `docs/evidence/m3-5-research-run.md`, `docs/evidence/m3-5-full-run.md`, and the saved run files `metrics.json` and `timing.json`. All numbers are validation scores on 629 rows.

| Family winner | Macro-F1 | Accuracy | Fit (s) | Median predict, 629 rows |
| --- | ---: | ---: | ---: | ---: |
| B0 | 0.121 | 0.318 | 0.017 | 3.6 ms |
| B1 | 0.878 | 0.874 | 0.015 | 3.6 ms |
| L1-C1 | 0.922 | 0.925 | 0.078 | 3.6 ms |
| L2-C1 | 0.924 | 0.925 | 0.049 | 3.7 ms |
| S1-C1 | 0.936 | 0.938 | 0.022 | 3.7 ms |
| L3-C10 | 0.952 | 0.954 | 0.123 | 6.9 ms |
| DT-d30-leaf1 | 0.818 | 0.828 | 0.045 | 3.8 ms |
| RF-dNone-leaf1 | 0.913 | 0.917 | 0.547 | 20.2 ms |
| XGB-d6-lr0.05 | 0.901 | 0.908 | 4.93 | 9.4 ms |
| **Jev** | **0.975** | **0.973** | 0.005 (replay) | 0.27 ms (replay) |

B0 predicts direct answer for every row, so its accuracy equals direct answer's share of validation, 200 of 629.

**Three patterns, each on one split.**

- **Trees against linear models.** The single tree scores 0.818, the lowest of the real classifiers. XGBoost, 0.901, and the forest, 0.913, are better than one tree, and both trail the best linear models. L3-C10 beats all three tree families.
- **Capacity matters for trees.** DT-d10 scores about 0.72 and DT-d30 about 0.80 to 0.82. RF without a depth limit is the best forest, 0.913. These are single comparisons, and their size has no interval.
- **More data, not a clean comparison.** M3's best was 0.925 on 79 validation rows. M3.5's best local model scores 0.952 on 629 rows. The validation set changed, so the two headline scores cannot be compared directly.

**Jev against L3-C10.** Per-class F1 for Jev is calculation 0.996, lookup 0.975, retrieval 0.967 and direct answer 0.963. For L3-C10 it is retrieval 0.975, calculation 0.954, lookup 0.943 and direct answer 0.938. Jev makes 17 errors in 629 rows and L3-C10 makes 29. Only one row is wrong for both. Ten of Jev's 17 errors are retrieval rows predicted as direct answer, and 10 fall on No Robots rows. The record offers a hypothesis, not an inspected finding. The passage stays outside the router text, so a query that mentions it weakly reads like a general question.

**By row origin.** On the 79 M3 validation rows, which have human primary labels, Jev scores 0.962 and L3-C10 0.938. On the 550 new rows they score 0.978 and 0.956. Jev leads in both groups, and on the 79 rows the lead is about two rows.

**Probability quality, validation only.** Jev's Brier score is 0.059 against L3-C10's 0.096. Its 10-bin ECE is 0.049 against 0.100. Its mean top probability, 0.924, is below its accuracy, 0.973, so it is underconfident here. This is a diagnostic, not M4's calibration analysis.

**Jev collection and cost.** Source: `docs/evidence/m3-5-full-run.md`.

| Pass | Requests | Valid answers | Errors | Input tokens | Median latency |
| --- | ---: | ---: | ---: | ---: | ---: |
| Main | 629 | 629 | 0 | 317,282 | 0.197 s |
| Repeat | 629 | 629 | 0 | 317,282 | 0.199 s |

The two passes used 634,564 input tokens. At the published $0.042 per million, that is about $0.027. This is inferred, since no bill was seen.

**Repeat disagreement.** The same questions asked again the same day changed 2 of 629 top choices, q2851 and q3049, both retrieval rows with a top probability between 0.50 and 0.57. One flip made a right answer wrong and the other made a wrong answer right, so the repeat log also scores 0.975. 351 of 629 probability vectors were identical, and no probability moved more than 0.09. So the API is mostly, not perfectly, repeatable. A later model version could answer differently.

**Reproduction.** The two local runs produced identical predictions (`453807b4…`) and metrics (`104c7a2c…`). `compare` printed `PASS: runs reproduce`. A restored-archive rerun, with Jev replaying its archived log, also reproduced. The 26 local metrics equal those of the first run `m3-5-a` exactly. Peak memory was 323.6 MiB and 324.4 MiB, and the first run took about 22 seconds. Both are inside the proposed limit of 15 minutes and 2 GiB, which Altan has not formally answered. Replaying the Jev log proves the log is intact. It is not an independent rerun.

<!-- pagebreak -->

## Trace one validation query

Take q0005 again, from Altan's own rows: "A train ticket costs 45 kr. How much do three tickets cost?" Its label is calculation, its group is g042, and its source is `altan-authored`. It is still in the validation file `data/processed/m3-5/validation.jsonl`, so no test text is involved.

All probabilities below come from the saved `results/m3-5-full-a/predictions.jsonl`. I also refit L3-C10, DT-d30-leaf1, RF-dNone-leaf1 and XGB-d6-lr0.05 on the training file only, in the locked environment, and each refit probability equals the saved value with a maximum difference of 0.0. Class order is retrieval, lookup, calculation, direct answer.

**From text to features, L3-C10.** The vectorizer lowercases and extracts 12 words, `a train ticket costs 45 kr how much do three tickets cost`. L3 adds 11 word pairs. Its vocabulary holds only 10,000 of the 35,447 words and pairs that occur in training, kept by overall frequency. Eleven of q0005's 23 features have a column: the words `a`, `train`, `costs`, `45`, `how`, `much`, `do`, `three`, `tickets` and `cost`, and the pair `how much`. `ticket` never occurs in training. `kr` occurs in training but did not survive the cap. Ten pairs are missing. Every model ignores a feature with no column.

**Local model, L3-C10.** Scores 0.0276, 0.0430, 0.8045 and 0.1249. It predicts calculation, which matches the label.

**Same query, other local families.**

| Configuration | Retrieval | Lookup | Calculation | Direct answer | Prediction |
| --- | ---: | ---: | ---: | ---: | --- |
| L3-C10 | 0.0276 | 0.0430 | 0.8045 | 0.1249 | calculation |
| DT-d30-leaf1 | 0 | 0 | 0 | 1 | direct answer |
| RF-dNone-leaf1 | 0.040 | 0.075 | 0.430 | 0.455 | direct answer |
| XGB-d6-lr0.05 | 0.0218 | 0.0138 | 0.0988 | 0.8656 | direct answer |

The three tree families all miss this row. The tree's path shows why its score is exactly 1. The tree asks 18 questions. For 16 of them q0005 has none of the tested word, such as `this`, `dataset` or `passage`, so each goes left. Two tests find a word: `much` at TF-IDF 0.224 against a threshold of 0.0627, then `how` at 0.147 against 0.1173. The path ends in a leaf holding 3 training rows, all direct answer. That leaf probability is a count in three rows, not strong evidence. The whole tree has depth 30 and 105 leaves.

The forest averages 200 deep trees. Its calculation and direct answer scores are 0.430 and 0.455. A gap of 0.025 is five trees of 200. Averaging many trees spread the vote where the single tree gave 1. XGBoost's 0.8656 for direct answer comes from added shallow trees, and it is confident and wrong here.

**Same query to Jev.** The request body is `{"query": <the text>}` with the fixed question and four options. The first pass returned choice calculation with probabilities 0, 0, 1 and 0, at 484 input tokens and 0.456 s. The repeat pass returned the same. Jev matches the label. The vendor's own `confidence` field also read 1.0, and the project does not use it.

**What the trace shows.** First, one row cannot rank anything. L3-C10 and Jev are right, and all three tree families are wrong. Second, a probability of 1 is a statement of the model, not proof of calibration. The tree and Jev both output a 1, one wrong and one right. Third, the systems get here by different routes. L3-C10 weights words and word pairs from 1,888 rows. Jev reads the written rules and sees none of your training rows. The saved artifacts do not show why Jev succeeded.

<!-- pagebreak -->

## Course connections

Course concepts support M3.5's design but do not show that Jev or any tree generalizes. Each paragraph gives the course concept, then the project choice. Pages are one-based PDF pages. I extracted each cited page with `pdftotext`.

**Scope.** `CourseProjects.pdf` p. 15 asks Project 13 to compare classifiers and feature representations and to analyze confidence and errors. M3.5 widens the comparison. Confidence and errors are M4.

**Decision trees.** `Lecture5-FundamentalClassificationAlgorithms.pdf` p. 31 describes a greedy attribute test chosen by a criterion. Page 38 defines the Gini index of a node as one minus the sum of squared class shares, and page 40 weights the child nodes by size. Page 50 names `max_depth` and `min_samples_leaf` as early-termination settings. `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` p. 10 lists a tree's strengths, such as robustness to missing values, and weaknesses, such as poor accuracy. The project choices are the Gini criterion, the depth grid 10 and 30, and the leaf grid 1 and 3. The lecture's tree examples use a few labeled attributes. The project's tree tests one TF-IDF word per node.

**Overfitting and simplicity.** `Lecture5-FundamentalClassificationAlgorithms.pdf` p. 53 defines overfitting as a model more complex than necessary, whose training error stops estimating performance on unseen records. Page 57 states Occam's razor. Page 5 says the test set must be separate from the training set. The depth-30 tree whose path ends in a 3-row leaf is an instance of fitting small regions. The project choices are the tie rules that prefer shallower trees and the order that prefers earlier families.

**Bagging and random forests.** `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` p. 11 defines bagging as sampling the training set and taking a majority vote, reducing variance but not bias. Page 12 lists the bootstrap samples and the vote. Page 14 adds a random sample of attributes at each split. Page 6 says an ensemble averages out the variance of unstable learners. The project choices are 200 trees, `max_features="sqrt"`, and averaging probabilities in place of a plain vote. The lecture also mentions out-of-bag samples, which the project does not use.

**Boosting and XGBoost.** `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` p. 18 describes models trained in sequence, each reducing the error of the earlier ones. Pages 28 to 29 present gradient boosting as new models that predict the residuals of prior models, with a gradient-descent view. Page 31 says boosting uses shallow trees and that the number of trees, the learning rate and the depth can be chosen by validation, with overfitting risk when there are many trees. Page 32 calls XGBoost an additive tree model with regularization. Pages 35 and 36 write the objective as training loss plus regularization. Page 38 says XGBoost has sparsity-aware split finding. Page 39 compares bagging and boosting. The project choices are the grid, a softmax objective over four classes, and the explicit missing-value semantics for absent words. The lecture's steps describe a regression setting with residuals, so the multiclass form in the appendix is a library and project detail.

**Validation and metrics.** `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` p. 52 divides data into training, validation and test sets, and page 54's title names the validation set as preventing leakage. Pages 56 and 57 give the confusion matrix, precision, recall and F1. Pages 80 and 81 separate parameters from hyperparameters. The project choices are one validation set, macro-F1 as the primary metric, and the 0.01 tolerance.

**Imbalance.** `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` p. 68 says a classifier tends to favor the majority class, and page 69 offers resampling and synthetic data. The release has unequal classes, 296 lookup against 601 retrieval in training. The project does not resample or weight classes (`class_weight=None`). It reports macro-F1, per-class scores and confusion matrices instead. That is a project choice.

**Data quality and sampling.** `Lecture2-Data Preprocessing and Feature Engineering.pdf` p. 3 names duplicate records and inconsistent data from different sources as cleaning problems. Page 8 asks how the data were sampled. Page 18 lists resolving redundancy as a cleaning task. The project's choices are the group splits, the source and request-type caps, and the near-duplicate checks.

**What the lectures do not cover.** None of the inspected pages teaches Jev, API-hosted decision models, TF-IDF, macro-F1, the 0.01 tolerance, the predeclared family order or a repeat pass on a vendor API. Those are project choices. The lecture's XGBoost pages are brief, so the multiclass softmax form and the library defaults are project and library details, not course content. Lecture 7 was added to `docs/course-sources.md` with this guide.

| Course concept | Project choice |
| --- | --- |
| Gini index, hyperparameter brakes, overfitting | DT grid 10 and 30, leaf 1 and 3, shallower-first ties |
| Bagging, bootstrap, attribute sampling | RF 200 trees, `sqrt` features, probability averaging |
| Gradient boosting, loss plus regularization, sparsity | XGB 200 rounds, softmax, absent words as missing |
| Three data roles, F1, imbalance | validation-only selection, macro-F1, no resampling |

<!-- pagebreak -->

## Choices and their reasons

- **Raise the data to up to 1,000 per class.** The supervisor and Altan wanted more data. The cost is imbalance, 494 to 1,000 rows. Every quality rule stayed, so classes stop where supply or caps stop them.
- **Change the review protocol.** Per-row human labeling does not scale to 7,206 candidates. Altan chose to adjudicate only disagreements and flags. The cost is that labels are AI labels, and he adopted agent-proposed defaults. This is disclosed, not repaired.
- **Run the M3 matrix again.** A forest cannot be called better than logistic regression unless both are scored on the same expanded split. Rerunning keeps comparisons matched. The headline score still cannot be compared with M3's.
- **Order and tie rules.** The shallow-first and low-learning-rate rules are declared conventions made before scoring. They prefer a simpler setting when the evidence cannot tell two apart. They are not proofs that such settings generalize.
- **One CPU thread and a laptop budget.** Local runs take about 22 seconds, and a GPU was never needed. The cost is that XGBoost's depth-6 fits take about 4 to 5 seconds.
- **Add XGBoost as a dependency.** XGBoost 3.4.1 is pinned. Linux and Windows install the CPU build of the same version, and macOS needs Homebrew's `libomp`. The cost is a second OpenMP runtime next to scikit-learn's. The evidence record says a pilot and the full suite ran without a conflict, and that a later macOS or Homebrew update could still change that.
- **Jev as a separate system.** Pinning `jev-1.14.0`, saving every request and replaying the log offline keeps local reruns free and deterministic. The cost is that Jev's reproducibility rests on a log from one day.
- **Capped Jev collection.** Altan named no spending cap, so each pass was capped at 700 requests. Jev was run on validation queries only. Sending the 628 test queries needs Altan's separate approval.

## Actual checks performed

Source: `docs/evidence/m3-5-research-run.md`, `docs/evidence/m3-5-full-run.md`, `docs/evidence/m3-5-dataset.md` and `docs/evidence/m3-5-classifiers.md`.

- **Release.** `check-collection` printed `PASS: M3.5 collection checks`. `validate_dataset.py --ready` printed `PASS: M1 readiness checks passed (3145 accepted rows, 3145 reviewed)`.
- **Local runs.** Both `m3-5-a` and `m3-5-b` reported all 26 configurations `ok`, and `compare` printed `PASS: runs reproduce`.
- **Full runs.** `m3-5-full-a` and `m3-5-full-b` reported all 27 configurations `ok`, and `compare` printed `PASS: runs reproduce`.
- **Selection.** `select` printed `PASS: overall Jev`, with `valid: true` and `complete_matrix: true`.
- **Archive.** The full archive script printed `PASS: 62 restored files byte-identical to originals`. After a fresh `uv sync --locked`, the restored 27-configuration rerun printed `PASS: runs reproduce`.
- **XGBoost behavior.** A fixture confirmed that absent sparse entries behave as missing values.
- **Trace.** For this guide I refit four configurations on the training file only and compared the q0005 probabilities with the saved ones. The maximum difference was 0.0 for all four.

Re-run for this guide on November 3, 2026, at commit `d0f3045` plus documentation changes:

- `sh scripts/check.sh` exited 0: the smoke check printed `PASS: environment-smoke-only`, 284 tests passed, and Ruff lint, Ruff format and `git diff --check` passed.
- `check-collection` on `m3-5-v1` printed `PASS: M3.5 collection checks` again, with 1,000 retrieval, 494 lookup, 651 calculation and 1,000 direct answer rows. A separate count of the release file found the same 3,145 rows.
- The lead compared the guide's selection scores and q0005 probabilities with `results/m3-5-full-a/metrics.json` and `predictions.jsonl`, and extracted five of the cited lecture pages again.

Not checked: no human read every accepted row, no human inspected the validation errors, and the sealed test has no score. The record marks one deviation from the brief: 142 rows were excluded on the screen label alone, and 19 of them had been held for Altan.

## What M3.5 can contribute to your report

For methods, M3.5 supplies the release with its sources and the label process, the grouped extension of the M3 split, the exact settings of all 27 configurations, the selection rule fixed in advance, and the Jev adapter with its frozen prompt. For results, it supplies the validation table, the per-family winners, the Jev passes and their disagreement, the error counts by source, and resource figures, each labeled as validation on 629 rows. The by-origin split and the probability diagnostics belong in the discussion as exploratory. The label process, imbalance and Jev limits belong in the limitations.

`ProjectRreportInstructions.pdf` p. 1 asks for an own-words report on the data and models, with visualizations, 5 to 12 pages, IEEE two-column. A macro-F1 by family chart is a candidate figure. Matplotlib is already pinned for the `figures` command, but no M3.5 figure has been rendered. This guide is study material, not report text.

## What M3.5 cannot support

- **No test performance.** The sealed test was never opened. M4 scores it once after the frozen decisions.
- **AI-labeled data.** The 2,745 new labels are AI labels with human adjudication of disagreements. There is no human agreement figure, and both checkers are Claude models.
- **Shared definitions.** Jev's criteria paraphrase the guide the labelers followed, so Jev's agreement partly tests how well written rules transfer.
- **Imbalance.** Classes run from 494 to 1,000 rows. A class-level result for lookup rests on 100 validation rows.
- **Pretraining overlap.** Whether Jev saw the public corpora in pretraining is unknown and cannot be tested here.
- **Jev non-determinism.** The repeat pass flipped 2 of 629 choices. A later model version could change more.
- **Validation-only, optimistic.** Jev's 0.975 comes from the rows that chose it.
- **Small differences against noise.** Jev leads L3-C10 by 0.023 and its lead on the 79 human-labeled rows is about two rows. No interval or significance test was computed.
- **No headline comparison with M3.** The validation set changed from 79 to 629 rows, and the training set from 242 to 1,888.
- **No error inspection.** The only error evidence is counts by class and source. Cause claims, such as the passage-attachment explanation, are hypotheses.
- **Cost and dependence.** Jev needs an account, a network call and a per-token price, and it sends query text to a vendor. About $0.027 for two passes is inferred, not billed.
- **One host, one seed, one split.** Identical reruns show determinism, not generalization.
- **No understanding claim.** Only Altan's answers change the learning record.

<!-- pagebreak -->

## Technical appendix: the models

Here `K = 4` classes, `n = 1,888` training rows, and `x` is a query's TF-IDF vector. The TF-IDF and logistic regression equations are in the M3 guide and are unchanged. The new equations follow, with the purpose of each first.

**Gini impurity.** A node is pure when all its rows share one class. Gini impurity measures how mixed a node is. A split is good when the size-weighted impurity of its children is low.

```text
G(t)        = 1 - sum over classes k of p_k(t)^2
G_split     = sum over children c of (n_c / n_t) * G(c)
```

Here `p_k(t)` is the share of class `k` among the training rows at node `t`, `n_t` is the number of rows at the node, and `n_c` the number in child `c`. `G` is 0 for a pure node and highest when the classes are equal. At each node the tree picks the word and threshold that give the lowest `G_split`. For example, a node of 3 rows, all direct answer, has `G = 0`.

**Random forest.** The forest turns many unstable trees into one steadier score by averaging.

```text
p_b,k(x)  = class-k share in the leaf that x reaches in tree b
p_k(x)    = (1 / B) * sum over trees b = 1..B of p_b,k(x)
prediction = the class k with the largest p_k(x)
```

Here `B = 200` is the number of trees. Each tree `b` is trained on a bootstrap sample of the training rows, and each split considers a random subset of the words. With unlimited depth and leaves of one row, a leaf is pure unless identical vectors carry different labels. Then each `p_b,k` is 0 or 1 and the average equals the vote share. In the trace, 0.455 and 0.430 are multiples of 1/200.

**Gradient boosting with softmax.** Boosting builds a score for each class by adding small trees. Softmax turns scores into probabilities. Each new tree is fitted to reduce the multiclass log loss.

```text
F_k^(0)(x) = initial score for class k
F_k^(m)(x) = F_k^(m-1)(x) + eta * f_k^(m)(x),    m = 1..M
p_k(x)     = exp(F_k^(M)(x)) / sum over classes j of exp(F_j^(M)(x))
loss       = sum over training rows i of -ln p_{y_i}(x_i)   (plus the library's penalty on leaf values)
g_ik       = p_k(x_i) - 1 if y_i = k, else p_k(x_i)
h_ik       = p_k(x_i) * (1 - p_k(x_i))
```

Here `eta` is the `learning_rate`, 0.05 or 0.1, and `M = 200` is the number of rounds. `f_k^(m)` is the tree added for class `k` in round `m`, and it has depth at most 3 or 6. So 200 rounds with 4 classes make 800 trees, which I confirmed on a refit. The quantity `g` is the slope of the loss with respect to a score, and `h` is its curvature. The library fits each new tree using these two quantities to reduce the loss. The code leaves the penalty and other settings at library defaults, whose values this guide does not verify. The `multi:softprob` objective is what the config names.

**Jev's output and the rule.** Jev gives a vector of four probabilities. The adapter accepts an answer only if each is a finite number in [0, 1] and they sum to 1 within 0.001. The rule in code, for scores `s` and best `b`, is `round(s, 12) >= round(b - 0.01, 12)`. The rounding keeps a gap of exactly 0.01 inside.

**Macro-F1.** Each class gets an F1 score and the four are averaged with equal weight, so small classes count as much as large ones.

```text
precision_k = TP_k / (TP_k + FP_k)
recall_k    = TP_k / (TP_k + FN_k)
F1_k        = 2 * TP_k / (2 * TP_k + FP_k + FN_k)
macro_F1    = (F1_retrieval + F1_lookup + F1_calculation + F1_direct) / 4
```

`TP`, `FP` and `FN` are the true positives, false positives and false negatives for class `k`, counted on the 629 validation rows.

## Technical appendix: file identities

| Artifact | SHA-256 |
| --- | --- |
| `data/processed/m3-5-v1.jsonl` | `be747dda8fd9f7c2ee432fa4ab29d6577607212b4d5a678d82205fef3386b2a8` |
| `data/raw/m3-5-reviews-v1.jsonl` | `326d63b5ce02514751ccfd57edc751dbc1c684ad1187827bd2728f5026cba51f` |
| `data/splits/m3-5-split.json` | `7aacbc497dd462e56a5fbcb3b5546c056ed4f835e35d0cf61334f17ce3a45e10` |
| `data/processed/m3-5/train.jsonl` | `dd3308af151e44ac242b639d6e4ba7e304156f6a26e93a3ff853e4cb5dc12bca` |
| `data/processed/m3-5/validation.jsonl` | `0e9dc93459342ccf173ab921136ce3bb30670519ccc33f4f92d3c98e7e888691` |
| `docs/collection-brief-m3-5.md`, amended | `5f881f83df5ed6a96585a3788ca9bd8c568286bba2570bf9bc6b9bdae8163f92` |
| `docs/collection-brief-m3-5.md`, as frozen | `5320797319b1206f4e11acae5ec7e16f90ea2500b14e21cc0f882ff80957e50e` |
| Predictions, `m3-5-full-a` and `m3-5-full-b` | `453807b4a11f5f9d0ae09791ead5c204bc45614fbad6626409c7a82151384e62` |
| Metrics, `m3-5-full-a` and `m3-5-full-b` | `104c7a2c06cae842ed274b3776dc8d84f053e94f0410a16144777eafe692f9f4` |
| `results/m3-5-full-a-selection.json` | `6a247792f9fde51381f8f43b0463cd0811b85c65b8a011dc3925215b3a008168` |
| `results/m3-5-full-a/manifest.json` | `03abb688856b46d74fb35b4307f4a0307cccf9e54a4d4994e24ef96cec688fd7` |
| `results/m3-5-full-b/manifest.json` | `5b1b3a4597e417481dbb4f1f51d026fffc71342de4eb422a063d5ae3bd473ad3` |
| `results/jev/m3-5-validation.jsonl` | `1f68d2f3534c2d5649f80f2caabef0eda2ddd6a37f28390b59858e0dc566f839` |
| `results/jev/m3-5-validation-repeat.jsonl` | `c8c4cf63ca0dbb0ddf5debe746fd31d58cc1e8d40178b3d6a4050641a69c2916` |
| `data/processed/m3-5-prepared-jev.json` | `b87d441c83a95559fbb27f24a87dc979c5a6b61c2781f7e39f21c63a8de27230` |
| `work/m3-5-archive/m3-5-full-release.zip` | `f95b2d9e9449d6d7483caaf5e3ad1bdb7c3c3aa0671d18566f6ec89bad49b57f` |

The run record names scikit-learn 1.9.1, XGBoost 3.4.1, NumPy 2.5.3, SciPy 1.18.1, Python 3.12.13 and macOS arm64 with 12 CPUs, with thread variables set to 1. The model seed is 42. The `uv.lock` hash recorded in `provenance.json` is `13bdff21661cf0a421c5ba00c3e1c7ad4e08c0247924e620d8c74f7d44f61929`. The Jev logs hold validation text and stay out of Git.

<!-- pagebreak -->

## Your M3.5 practice questions

Attempt these before asking for a worked answer. Use your own words and this guide's tables. All are unanswered, and no answer or status has been written on your behalf. The first three come from `docs/m3-5-plan.md`.

1. Why must we rerun logistic regression on the expanded split before claiming Random Forest is better? (Unanswered.)
2. How could 4,000 rows still contain too little independent evidence? (Unanswered.)
3. Why does Jev need a different fairness and reproducibility discussion from a decision tree? (Unanswered.)
4. Suppose Jev had scored 0.960 and every other family winner were unchanged. Apply the overall rule step by step. Which system is chosen, and which step decides? What would this change about how you report the result? (Unanswered.)
5. In the q0005 trace, DT, RF and XGB all predict direct answer, with scores 1, 0.455 and 0.8656. What does each number mean? Why is the tree's 1 weaker evidence than it looks, and what would you check before trusting XGBoost's 0.8656? (Unanswered.)
6. Describe how the 727 adjudicated rows reached the release. A reader asks, "Is Jev's 0.975 agreement with human labels?" What do you answer, and what evidence would a human agreement figure need? (Unanswered.)

Earlier prompts remain open, including the learning log's M3 prompts and the M1 to M3 guide questions. Record attempts and feedback in `docs/learning-log.md`.

## Inspected sources

Review date: November 3, 2026. Page numbers are one-based PDF pages. The files are under `/Users/altanesmer/Desktop/SM1/AI/`. I extracted each cited page with `pdftotext`, and the SHA-256 values below were computed with `shasum -a 256` on that date.

- `CourseProjects.pdf`, page 15: Project 13 scope.
- `Lecture2-Data Preprocessing and Feature Engineering.pdf`, pages 3, 8 and 18: duplicates and inconsistency, how data were sampled, cleaning tasks.
- `Lecture5-FundamentalClassificationAlgorithms.pdf`, pages 5, 31, 38, 40, 50, 53 and 57: separate test set, greedy splits, Gini, weighted split, tree hyperparameters, overfitting, Occam's razor.
- `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf`, pages 6, 10, 11, 12, 14, 18, 28, 29, 31, 32, 35, 36, 38, 39, 52, 54, 56, 57, 68, 69, 80 and 81: ensembles, trees, bagging, random forests, boosting, XGBoost, validation, metrics, imbalance, hyperparameters.
- `ProjectRreportInstructions.pdf`, page 1: report requirements.

| File | SHA-256 |
| --- | --- |
| `CourseProjects.pdf` | `d4e98da373cbdcd62f804d2cd0f957bbaa53294205762ba6d1dc04b26b74fdca` |
| `ProjectRreportInstructions.pdf` | `00ab8140f009f52fd9f552daa61ade6f628bdd1125096d62c54e07f06e1519a5` |
| `Lecture2-Data Preprocessing and Feature Engineering.pdf` | `e7bfec9a9a52954c038e58a84f680e76648efa582ef79acafe2a3bfaa582217f` |
| `Lecture5-FundamentalClassificationAlgorithms.pdf` | `c2995d1963da118c5b8f599a641a15b2c8ec8102aa61a66fee13a29eeb67980d` |
| `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` | `918f33dc045f3fbbaaae8a33b1a779e9eb7785e8625f1008aa5fc144b49813fd` |

Repository sources: `docs/m3-5-plan.md`, `docs/evidence/m3-5-dataset.md`, `docs/evidence/m3-5-research-run.md`, `docs/evidence/m3-5-full-run.md`, `docs/evidence/m3-5-classifiers.md`, `docs/collection-brief-m3-5.md`, `docs/data-and-evaluation.md`, `docs/course-sources.md`, `src/orchestra/experiment.py` (settings and selection rule), `src/orchestra/jev.py` (prompt and parser), `results/m3-5-full-a/` (predictions, metrics, timing, configuration) and `results/jev/` (request and response logs). The q0005 numbers were checked against the 27 saved rows for that query in `results/m3-5-full-a/predictions.jsonl` and the two Jev logs.
