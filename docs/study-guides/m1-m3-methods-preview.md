# M1 to M3 methods preview

This explanation accompanies the [M1 to M3 plan](../m1-m3-plan.md). It describes proposed work for the report, presentation, and oral practice. It does not authorize implementation or report completed research milestones. Implementation waits for Altan's subsequent approval.

As of October 16, 2026, Orchestra has a draft annotation guide, a source manifest, a row validator, validator tests, and an environment smoke check. There are no research query rows, trained routing models, or experimental scores. The smoke check verifies library operations on artificial fixtures. The validator checks row structure and provenance, not whether a human chose the correct action.

## One query explains the prediction target

Use this teaching query throughout the preview:

> Calculate the increase using the figures in the attached report.

The proposed first action is `document_retrieval`. The system needs the report's figures before it can calculate. The router's output would be that action label. Reading the report, extracting figures, and computing an answer are later operations outside this classification study.

This is an agent-selected teaching example already used in the project documents. It is excluded from the research dataset, along with its teaching paraphrases and the smoke fixtures. Its explanation is not an annotation supplied by Altan or an observed model prediction.

The four proposed actions are `document_retrieval`, `knowledge_lookup`, `calculation`, and `direct_answer`. Their boundaries depend on required information, not one keyword. A request that already supplies the numbers can start with calculation. An explanation of a mathematical idea can start with direct answering. A request with missing context remains `needs_review` until resolved or excluded. That status is annotation metadata, not a fifth class.

## M1 makes labels defensible

The planned collection begins with fictional scenarios and human-authored English queries. Altan owns query authorship, label decisions, rationales, and the dataset-license choice. The agent has prepared the guide and validation tooling. That preparation does not establish human review, an agreed license, or accepted examples.

The collection targets are 40 pilot queries, then 120 accepted rows for the first baseline, then 400 accepted rows for the main comparison. The pilot initially targets 10 per class. The first slice requires at least 30 accepted rows and 15 independent groups per class. The main target is roughly 100 rows per class. These are collection goals, not observed counts or guarantees of statistical precision.

Each row needs a source identifier, a rationale, an annotation version, and a group identifier. A source manifest records authorship and license. If agent-generated candidates are approved later, their provider, model revision, prompt, settings, date, and human edits must remain traceable. They must never be attributed to Altan as independently human-authored text. External datasets need an approved license and a justified mapping to first-action labels before use.

Human review is planned for every label. A second human independently reviews at least 20 percent, stratified by proposed class, plus every ambiguous row. Record disagreement before adjudication. If a second human is unavailable, use a recorded delayed blind self-review and disclose single-annotator bias. Agent agreement does not replace independent human annotation.

A group contains queries derived from one scenario, template, or paraphrase family. All variants of the teaching report request would belong together if they were study candidates. They remain excluded here. Actual research groups have at most four rows. Separate group identifiers do not make near-copies independent, so manual review must also detect related families.

If a paraphrase appears in training and another in test, the score can reward recognition of familiar wording. Assigning a whole group to one partition reduces that leakage. It cannot eliminate the broader similarity of an authored dataset to its own templates.

M1 evidence will include the frozen guide, cleared source records, accepted and excluded counts, independent group counts, disagreements, and class and length summaries. The validator can reject malformed rows. Human review must establish whether the first-action rationale is defensible.

## M2 separates learning from checking

The planned split assigns whole groups approximately 60 percent to training, 20 percent to validation, and 20 percent to a sealed test, with seed 42. Actual proportions and class counts must be recorded. Group boundaries take priority over exact percentages. Missing classes or too few independent groups require more data or a documented protocol decision.

Training learns vocabulary, term weights, and classifier parameters. Validation supports choices between settings. The sealed test remains unused until model and confidence choices freeze in M4. M2 and M3 therefore produce validation evidence, not final test conclusions. M3 preserves every M2 group assignment and allocates only new independent groups. Fresh comparable runs use the expanded version. No comparison may mix predictions from different dataset or split versions.

For the teaching query, imagine its research equivalent belonged to validation. A pipeline fitted on training text would transform that query using only the learned vocabulary and weights. It would predict an action, and evaluation would compare that prediction with a reviewed label. This is a planned trace. Today's validator does not fit this pipeline or predict an action.

The first baseline predicts the most frequent training class for every query. This dummy classifier tests whether learned text features improve on a class-frequency rule. A high accuracy from that rule could reflect imbalance, so accuracy alone cannot establish useful routing.

The learned baseline is TF-IDF with logistic regression. Two runs with the same committed configuration must produce identical split membership and predictions. Saved validation predictions, class metrics, a confusion matrix, and run metadata make that claim checkable. Repeating a run establishes reproducibility under the recorded conditions. It does not establish generalization to real users.

## M3 changes one choice at a time

Word counts record how often each training-vocabulary term occurs in a query. TF-IDF reduces the relative weight of terms that appear in many training queries. Both produce sparse numeric representations that discard most word order.

The proposed smoothed inverse document frequency is `idf(t) = log((1 + n) / (1 + df(t))) + 1`. Here `t` is a term, `n` is the number of training queries, and `df(t)` counts training queries containing that term. TF-IDF multiplies a term's count by its IDF, then applies the documented normalization. Validation and test text must not change the vocabulary or IDF.

This equation explains the proposed weighting choice. It is not a new equation implemented by Orchestra. scikit-learn supplies the representation. Counts may preserve useful repetition. TF-IDF may reduce common wording's influence, but neither is guaranteed to win. Bigrams add adjacent word pairs and may distinguish short phrases that unigrams lose.

The required matrix contains 14 configurations:

| Representation and classifier | Settings | Configurations |
| --- | --- | --- |
| No text, most-frequent dummy | Training majority | 1 |
| Unigram counts, multinomial naive Bayes | `alpha=1.0` | 1 |
| Unigram counts, logistic regression | `C=0.1, 1, 10` | 3 |
| Unigram TF-IDF, logistic regression | `C=0.1, 1, 10` | 3 |
| Unigram TF-IDF, linear SVM | `C=0.1, 1, 10` | 3 |
| Unigram and bigram TF-IDF, logistic regression | `C=0.1, 1, 10` | 3 |

Counts versus TF-IDF with logistic regression tests representation weighting. TF-IDF with logistic regression versus SVM tests the classifier. Unigrams versus unigrams plus bigrams tests short phrase information. Every configuration uses the same frozen rows and groups. Save unsuccessful runs and convergence warnings as well as successful outcomes.

Multinomial naive Bayes models term counts conditioned on a class and assumes conditional independence between terms. That assumption is imperfect for language. Smoothing with `alpha=1.0` gives a vocabulary term nonzero probability even when it did not occur in that class's training examples.

Logistic regression learns linear class scores and converts them into class probabilities. A linear SVM instead learns decision boundaries based on margins. Both can struggle when the correct action depends on information their sparse features fail to express. An SVM margin is not a probability. Logistic probabilities are not automatically calibrated.

`C` controls inverse regularization strength in these linear models. A smaller `C` applies stronger regularization, which discourages large coefficients. A larger `C` allows a closer fit to training examples and may increase overfitting. The same numeric `C` does not imply identical fitted behavior across classifiers. The three planned values bound tuning so the comparison remains explainable and reproducible.

Validation macro-F1 is the planned selection measure. Compute F1 separately for each class, then average the four values equally. This makes a weak class visible even when another class dominates the sample. Save class support and precision and recall alongside that average. Resolve validation ties within 0.01 by lower complexity, then prediction latency, using the rule fixed before comparison.

A frozen sentence encoder is an optional extension, outside the 14 required configurations. It needs a recorded model revision, license, representation settings, and measured resource check before use. The core comparison does not depend on that extension. No embedding download or new dependency is approved by this preview.

## Course concepts and external methods have different sources

The mappings below reuse the verified page references in [course sources](../course-sources.md), reviewed there on October 7, 2026. Page numbers count PDF pages from one. This preview does not claim a fresh slide inspection. Future milestone guides must inspect the relevant source copies and record their hashes and review date.

| Verified source and pages | Connection to the proposed study |
| --- | --- |
| `CourseProjects.pdf`, p. 15 | Project 13 requires classifier and feature comparisons, confidence analysis, and error analysis. Tool execution is optional. |
| `Lecture2-Data Preprocessing and Feature Engineering.pdf`, pp. 7–8, 26–28, 31–33, 68 | Sampling and privacy, exploration, transformation, feature extraction, and data quality support M1 review and M2 representations. |
| `Lecture5-FundamentalClassificationAlgorithms.pdf`, pp. 2, 4–5, 52–57 | Supervised classification, unseen testing, overfitting, and simplicity explain the prediction target and separation of data roles. |
| `Lecture5-FundamentalClassificationAlgorithms.pdf`, pp. 64, 67–72 | Bayes and naive Bayes support the count-based probabilistic baseline. |
| `Lecture5-FundamentalClassificationAlgorithms.pdf`, pp. 76–79, 86, 88–89 | SVM margins, regularization, and multiclass methods support the linear classifier comparison. |
| `Lecture6-ArtificialNeuralNetworks.pdf`, pp. 8, 57–58 | The neuron/logistic analogy and bag-of-words loss of order support the linear baseline and phrase comparison. |
| `Lecture4-LinearModelsforRegression.pdf`, pp. 60–65, 67 | Regularization, bias–variance, and hyperparameter validation supply supporting ideas. Orchestra predicts classes, not a continuous regression target. |
| `ProjectRreportInstructions.pdf`, p. 1 | The report describes data and models in Altan's own words, includes useful exploratory graphs, and uses 5–12 IEEE two-column pages. |

TF-IDF, macro-F1, confusion matrices, pretrained sentence embeddings, and calibration are project methods, not verified lecture mandates. The official scikit-learn references linked in [course sources](../course-sources.md#external-implementation-references) support feature extraction, leakage controls, and calibration. Their implementation details must match the locked library version. Confidence calibration and final test analysis belong to M4, beyond this preview's implementation scope.

## Evidence for the report and presentation

The report story begins with the action contract, then explains the reviewed data, the controlled comparison, and the limits of the findings. Slides can follow that same order. A useful opening slide traces the teaching query to its first action without implying that a tool ran.

M1 can later supply the data section and a slide about why labels need rationales and group review. Insert actual accepted counts, source attribution, disagreement records, exclusions, and class and query-length plots. M2 can supply a split diagram and a baseline comparison linked to saved validation predictions. M3 can supply the complete configuration table and a validation comparison whose rows name run IDs and resolved settings.

No result cells belong in this preview. Later claims need dataset and split hashes, the code commit and dirty status, the locked environment, resolved settings, seeds, predictions, metrics, and timing. A selected figure needs enough underlying data to recreate it. Ignored local results need an explicit archive, not merely a path that exists on one laptop.

Small authored samples cannot establish performance on live user traffic. Class balance is a study choice, not a measurement of real demand. Correlated scenarios reduce the amount of independent evidence. Labels may remain subjective, and a correct route does not establish a correct final answer. These limitations belong beside later scores.

Altan has requested milestone study material and owns the final report's explanation. Agents provide planning, tooling, and draft explanations within approved scope. The [learning log](../learning-log.md) records actual contributions and responses. This preview supplies no human labels, practice answers, or evidence that Altan has mastered a concept. Routing and split terminology still need practice.

Each future milestone gets an evidence-based Markdown guide and an exported, visually checked PDF after actual work. Record source and PDF identities under the [study-guide procedure](README.md). No M1, M2, or M3 PDF is delivered by this preview.

## Unanswered practice prompts

These prompts remain stored for later practice. Record Altan's attempt before giving a worked explanation or changing a learning status.

1. A new query asks for a price in a named catalog and then a percentage discount. Explain the first action and the information needed before calculation.
2. Two research queries describe the same fictional order using different words. Explain their group assignment, then explain what training may learn that validation must not change.
3. A future comparison shows better accuracy but worse macro-F1. Explain what class-level evidence you need before preferring that model, and why the sealed test cannot settle a tuning decision.

## Pilot update, October 26, 2026

Guide v1 defines a group as a shared request template: the same user goal solved by the same procedure, whatever the scenario. Sharing an operation or label is insufficient. The reviewed pilot has 38 accepted rows across 19 templates and two practice-only exclusions. These broader template families reduce independent group counts. The [pilot record](../evidence/pilot-guide-v1.md) gives class counts, hashes, actual human decisions, and the remaining 120-row coverage gate. Earlier preparation descriptions above are historical and do not override this observed pilot state. No research split, model result, or M1 completion is claimed.

For a concrete trace, a key-based existence query now shares a template with specific-record field lookups. Both use knowledge lookup first. That family has four pilot rows and remains one unit during any later split. A translation family contains two first-action labels because one request supplies its text and the other needs a document. A group is therefore not a target class. This is an agent explanation, not a new student response.
