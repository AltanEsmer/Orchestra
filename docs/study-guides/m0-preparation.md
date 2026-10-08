# M0: preparation and the purpose of Orchestra

Study guide edition: October 8, 2026. Baseline implementation: `0350a8e`. This explanation accompanies the accepted M0 plan. The project is course project 13, Learning to Route Queries in AI Systems.

## What you need to defend

Orchestra studies how a machine-learning classifier can choose the first action needed to process a user query. A query is the input text. An action label is the output. The eventual study compares classifiers and ways to represent text, then examines confidence and errors. Project 13 describes this scope in `CourseProjects.pdf`, PDF page 15 [S1].

Consider "What is 18 percent of 250?" The numbers are already present. The proposed action is `calculation`. The router's job is to choose that action. A calculator would produce the number afterward. A correct route and a correct final answer are separate outcomes.

Now consider "Calculate the increase using the figures in the attached report." The system must read the report before calculating. The proposed first action is `document_retrieval`. This ordering makes the prediction target precise. A request can need several actions, while the classifier returns one first-action label.

M0 prepares the repository and environment for this study. The current script checks that text can become numerical features and that an elementary classifier can fit and predict. No research dataset, trained routing model, or measured routing result exists at this milestone.

The guide supports your December report and January oral preparation. The report must be your own synthesis. Reading the guide does not establish that you can explain the project independently. The checkpoint at the end asks you to transfer the ideas to new examples.

## What this edition contains

The first six sections explain the purpose, files, executable flow, and course connections in plain language. The technical appendix explains the data shapes, TF-IDF arithmetic, dummy prediction, and evidence limits. The final section contains unanswered practice questions and the inspected source references.

<!-- pagebreak -->

## A useful target starts with a clear label

Supervised classification learns from examples that already have a class. The course defines this relationship in Lecture 5, PDF page 2 [S3]. For Orchestra, the proposed attributes come from query text, and the class is the first action. The annotation protocol gives each class a meaning before any classifier comparison begins.

The proposed four labels are:

- `document_retrieval` means reading an identified document or passage. "Summarize the cancellation clause in the attached contract" is an example.
- `knowledge_lookup` means looking up an item in an identified structured source. "Find product A17's warranty period in the product catalog" is an example.
- `calculation` means computing a requested numeric answer whose inputs are already supplied. "What is 12 times 8?" is an example.
- `direct_answer` means explaining or rewriting without a requested calculation or external lookup. "Explain why a fraction can be less than one" is an example.

These are our proposed operational definitions in `docs/data-and-evaluation.md`. The course lists actions as examples. It does not mandate our exact strings or all our boundary rules [S1].

Some requests cannot receive a defensible label under these assumptions. "What is the warranty?" does not identify the item or source. The v1 protocol holds such examples for clarification. Guessing a label would introduce annotation noise before the model sees any text.

The router sees query text. It does not see hidden report contents or an unrecorded conversation. A label must follow from the inputs available to the model. This constraint helps us distinguish difficult language from missing information.

The smoke script uses `simple` and `complex` as artificial fixture labels. Those words test library behavior. They are not a two-class version of the four-action study. Changing the label names alone would not create a research dataset or establish routing quality.

A later milestone will define rows with stable IDs, paraphrase groups, provenance, and annotation rationales. Related paraphrases must stay in the same partition so that near-copies do not make unseen evaluation easier. M0 creates no such rows or splits.

<!-- pagebreak -->

## The repository separates preparation from experiments

The repository's entry point is `README.md`. Its setup commands recreate the Python environment and run the existing check. The roadmap states milestone goals. The project plan explains the research scope. The data protocol records proposed labels and evaluation decisions. Those documents organize future work without pretending that the experiment exists.

Three environment files have distinct jobs. `.python-version` selects Python 3.12.13. `pyproject.toml` declares dependencies and development tooling. `uv.lock` records resolved packages, versions, and distribution hashes. `uv sync --locked` uses this recorded resolution instead of silently generating a different one.

A lockfile reduces one source of variation. It does not prove that every operating system behaves identically. The learning log records recreation on the same macOS arm64 host. Cross-platform behavior remains unverified.

`scripts/smoke.py` is the executable preparation. The script imports scikit-learn, constructs tiny text fixtures, computes TF-IDF features, checks their shape and sparsity, and fits a dummy classifier. The script prints a success message and runtime versions. It writes no model artifact, dataset, prediction file, or score table.

Our code owns the fixture texts, call order, and assertions. scikit-learn owns tokenization, TF-IDF, and `DummyClassifier`. SciPy owns the sparse-matrix machinery. Using a library still requires us to explain its inputs, outputs, assumptions, and fitted state. We do not claim to have authored those algorithms' internals.

`docs/repo-guide.md` gives the file-by-file walkthrough. `docs/learning-log.md` records checks and your actual learning responses. A passing command establishes implementation evidence. Only your attempted explanation can establish understanding.

The editable source of this guide belongs in `docs/study-guides/m0-preparation.md`. Its PDF belongs in the agreed external folder, `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/`. Course PDFs remain outside Git. Later editions should identify their source commit and checksum in the guide index.

Keeping preparation small matters for the oral exam. A single readable script lets you trace every operation. Reusable application modules become useful when data validation, training, or evaluation introduces behavior that needs them.

<!-- pagebreak -->

## Trace the actual smoke script

The training texts are "What is the capital of Denmark?", "Explain how rain forms.", and "What is the capital of France?" Their toy labels are `simple`, `complex`, and `simple`. The held-out texts are "Explain quasar formation." and "What is the capital of Sweden?"

The script first creates `TfidfVectorizer()` with default settings. `fit_transform(train_queries)` learns a vocabulary and term weights from the three training texts. The same call produces one numerical row per training text.

Next, `transform(held_out_queries)` uses the vocabulary and weights already fitted. This call does not add words or recompute training statistics. A held-out query can use only the columns learned from training.

Follow "Explain quasar formation." through these operations. Default tokenization lowercases the text and identifies `explain`, `quasar`, and `formation`. Only `explain` occurs in the fitted vocabulary. The other two words contribute no column. After normalization, the numerical row has one nonzero entry, with value 1, in the `explain` column.

The script checks that `quasar` is absent from `vectorizer.vocabulary_`. This assertion demonstrates one visible instance of training-only fitting. It does not prove that every future preprocessing step or dataset partition will avoid leakage.

The dummy classifier then fits on the training feature matrix and toy labels. There are two `simple` labels and one `complex` label. With `strategy="most_frequent"`, the fitted classifier selects `simple` for every prediction. The text features do not determine its choice.

Both held-out predictions are therefore `simple`. The literal assertion checks this exact behavior. A pass does not mean the model recognizes a quasar, knows a capital city, or selects a useful first action.

The script never supplies held-out ground-truth labels to a scoring function. There is no accuracy or F1 result to report. Its success message describes an environment check, which is the appropriate interpretation of these artificial fixtures.

<!-- pagebreak -->

## Course principles explain the preparation choices

Lecture 5, PDF pages 2, 4, and 5 [S3], separates learning a model from applying the model to unseen records. The smoke script follows this call order with `fit_transform` on training text and `transform` on held-out text. The future study needs meaningful annotated examples and a protected evaluation protocol in addition to this call order.

The lecture's generalization objective explains why fitting a representation on all text first would change the evaluation question. The fitted representation would already incorporate information about the held-out collection. The vocabulary assertion makes this issue concrete. Training-only preprocessing is our implementation choice that supports the course's unseen-record principle.

Lecture 2, PDF pages 32 and 33 [S2], distinguishes feature extraction from feature selection. Extraction maps input into a new representation. Selection keeps some existing features. TF-IDF converts raw query text into weighted term columns. That is a representation choice for our study. These inspected slides do not prescribe TF-IDF by name.

Lecture 2, PDF page 31 [S2], warns that more features do not automatically improve learning accuracy. A larger vocabulary or more n-grams may retain useful distinctions, but it may also increase dimension and data requirements. The toy script establishes that sparse features work. It provides no evidence that adding features improves routing.

Lecture 6, PDF pages 57 and 58 [S4], shows that bag-of-words representations lose word order. Default unigram TF-IDF has the same limitation. Queries with the same word counts can have the same features despite different order. This matters when action order or negation changes the desired route.

Lecture 5, PDF pages 52 through 54 [S3], introduces underfitting, overfitting, and noise. The dummy classifier ignores text, so it cannot learn distinctions between different query meanings. It provides a simple comparison reference. No training or test error has been measured here, so this guide does not diagnose an observed underfitting result.

These connections are explanations of how course principles motivate the implementation. A lecture citation is not evidence that our eventual classifier generalizes. That evidence requires actual experiment results with documented data and evaluation decisions.

<!-- pagebreak -->

## What M0 can contribute to your report

M0 supplies the research question, proposed target, preparation decisions, and reproducible environment description. You can use the guide to outline the introduction and methods sections. Write the final account in your own words and update every method claim to match the implementation that actually ran.

`CourseProjects.pdf`, page 15 [S1], calls for classifier and representation comparisons, confidence analysis, and error analysis. The report therefore needs more than a working prediction command. It needs results that support comparisons and explain where the approaches fail.

`ProjectRreportInstructions.pdf`, page 1 [S5], requires a research report in your own words, a description of the dataset and models, useful visualizations, 5 to 12 pages, and IEEE conference two-column format. It gives December 6, 2026 as the deadline for report and code. This study guide is a learning document, not the final IEEE report.

A defensible preparation statement is that the repository contains a locked environment and a smoke script with sparse-feature, vocabulary-isolation, and literal dummy-prediction assertions. The learning log records historical successful execution. The guide index records the current delivery's evidence and edition identity.

M0 cannot support a claim about routing accuracy, macro-F1, probability calibration, confidence thresholds, model superiority, speed of a research pipeline, or robustness on real requests. It also cannot support a claim that Altan has mastered the material. Those outcomes need separate evidence.

Later guides should preserve run IDs, configurations, split manifests, selected tables, plots, and limitations. A result should remain traceable to the data and code that produced it. This makes it possible to defend the report rather than remember an unsupported number.

January oral preparation should reuse the actual project. When you explain a principle, connect it to a file, operation, or measured result. When a method is only planned, say so. Questions about model selection, confidence, and errors become concrete after those milestones produce results.

M0 remains in progress until your introductory checkpoint response is recorded. Administrative course confirmation is outside the agreed agent work. The guide and its verification establish delivery while the learning checkpoint remains a separate step.

<!-- pagebreak -->

## Technical appendix: the numerical data shape

Text begins as Python lists of strings. `train_queries` contains three strings, `train_labels` contains three class strings, and `held_out_queries` contains two strings. Each training row must correspond to one label at the same list position.

The fitted vocabulary has 11 columns in the following order:

```text
capital, denmark, explain, forms, france, how,
is, of, rain, the, what
```

These names come from a direct inspection of `TfidfVectorizer().fit_transform` on the script's exact fixtures. The inspection used the project's locked environment on October 8, 2026. It is a numerical walkthrough check, not a research experiment.

The training feature matrix has shape `(3, 11)` and 16 stored nonzero entries. The held-out matrix has shape `(2, 11)` and 6 stored nonzero entries. A row means one query. A column means one fitted term. A value means that term's normalized TF-IDF weight in that query.

Sparse storage records nonzero entries rather than a full table of zeros. Many query-vocabulary combinations have value zero. Sparse storage can reduce storage cost for that pattern. These tiny matrices do not measure a meaningful resource saving for the eventual dataset.

For the second held-out query, `sweden` is unknown. The known terms are `what`, `is`, `the`, `capital`, and `of`. Their fitted IDF weights are equal because each occurs in the same two training documents. After L2 normalization, each of those five columns has value approximately `0.447214`, which is `1 / sqrt(5)`.

The first held-out row has just `explain=1`. The second has five values of approximately `0.447214`. All other columns are zero. No `quasar`, `formation`, or `sweden` column exists.

An all-unknown query would produce an all-zero feature row under these defaults. The current script does not test that boundary. A future trained router must document how it handles weak or missing representation information. The present dummy would still choose its most frequent fitted class.

<!-- pagebreak -->

## Technical appendix: TF-IDF and the fitted state

TF-IDF combines a term's frequency within a document with a weight based on how often the term occurs across fitted documents. Here a document means one query string. The default vectorizer uses raw term counts, smoothed inverse document frequency, and L2 normalization.

For term `t`, the smoothed weight is:

```text
idf(t) = log((1 + n) / (1 + df(t))) + 1
raw_weight(t, d) = count(t, d) * idf(t)
normalized_weight(t, d) = raw_weight(t, d) / L2_norm(d)
```

`n` is the number of training documents. `df(t)` counts training documents containing the term, once per document. The logarithm is natural. The L2 norm is the square root of the sum of squared raw weights in the row. Zero rows remain zero.

There are three training documents. `capital` occurs in two, so its IDF is `log(4/3) + 1`, approximately `1.287682`. `explain` occurs in one, so its IDF is `log(4/2) + 1`, approximately `1.693147`. A term occurring in fewer fitted documents receives a larger IDF weight.

In "Explain quasar formation.", the only recognized term has raw weight `1.693147`. The L2 norm is also `1.693147`. Division gives a normalized `explain` weight of 1. The model still receives no information about the two unknown terms.

`fit_transform` learns `vocabulary_` and the IDF statistics, then represents the training text. `transform` reuses that state. Fitting on held-out text would change the vocabulary and document-frequency counts. That would alter the representation even without changing any class labels.

Default tokenization lowercases text, accepts word tokens of at least two characters, and uses unigrams. The script supplies no stop-word list and no sublinear term-frequency option. These settings explain why common words such as `the` and `of` remain in the vocabulary.

TF-IDF weights do not encode truth, action order, or a calibrated probability. L2 normalization scales a feature row. It does not calibrate classifier confidence. Specific TF-IDF choices come from scikit-learn behavior and the project design, not a mandate in the inspected lecture pages.

<!-- pagebreak -->

## Technical appendix: the dummy and the checks

For each class `c`, the most-frequent dummy counts training labels and chooses a class with the greatest count. For these fixtures, `count(simple)=2` and `count(complex)=1`. There is a unique most frequent class, so tie behavior is irrelevant to the observed prediction.

```text
chosen_class = argmax_c count_train(c)
prediction(query) = chosen_class
expected held-out predictions = ["simple", "simple"]
```

The classifier accepts the numerical feature matrix through the estimator API. With this strategy, the learned prediction rule does not use the feature values to distinguish queries. A real baseline comparison later asks whether a text-sensitive model improves on this frequency-only reference under the same evaluation protocol.

Each existing assertion has a narrow meaning:

- `issparse` confirms sparse matrices for both fixture collections.
- The row-count assertion checks alignment between training rows and labels.
- The held-out shape assertion checks two rows and the same fitted column count.
- `nnz > 0` checks that each matrix has at least one nonzero entry. It does not check every row individually.
- The vocabulary assertion checks that the held-out-only word `quasar` did not enter the fitted vocabulary.
- The prediction assertion checks the exact two most-frequent dummy outputs.

The lead reran the README checks on October 8, 2026. Python 3.12.13 was already installed. Locked sync resolved 9 packages and checked 8. The smoke assertions passed with Python 3.12.13 and scikit-learn 1.9.1. Ruff reported all checks passed and 11 files already formatted. `git diff --check` exited with code 0. These are preparation checks, not research results.

The README smoke command is `uv run --locked python scripts/smoke.py`. The script prints `PASS: environment-smoke-only` only after the assertions succeed. Python's optimized mode can disable `assert` statements. The documented command uses ordinary execution and includes no optimization flag.

There is no separate unit-test suite at M0. The smoke script is a preparation check. Meaningful future behavioral tests belong at data-validation and experiment seams when those behaviors exist. Lint and formatting improve consistency, but neither measures routing quality.

<!-- pagebreak -->

## Your introductory checkpoint

Attempt these questions before asking for a worked answer. Use your own words. If a term is unclear, name the term so the next explanation can address it. No response or understanding status has been generated on your behalf.

1. A user asks, "Find invoice 42's total in the billing database, then divide it by three." Under the proposed contract, what is the first action? Explain which information is available before that action and what happens afterward.
2. Suppose we replace the held-out texts with "Explain nebula motion." and "What is the capital of Norway?" while keeping the original fitted vectorizer and dummy classifier. Which terms contribute features in each query? Explain the dummy's predictions and what those predictions tell us about semantic understanding.
3. An examiner says, "Your script passed, so your report can claim that the trained router generalizes to unseen requests." Which part of the statement has evidence at M0? Explain the additional data and evaluation evidence needed for the broader claim, and connect your answer to a course principle.

Your actual attempts and the resulting feedback belong in `docs/learning-log.md`. Existing gaps remain visible until a response supplies evidence to change them. After later milestones, oral practice should include actual confusion matrices, model settings, feature examples, and confidence results.

## Inspected sources

All numbers below are one-based PDF page numbers. The files are local course sources under `/Users/altanesmer/Desktop/SM1/AI/`. Relevant pages were extracted with pypdf for this edition on October 8, 2026. Source fingerprints are recorded in the PDF export manifest.

- [S1] `CourseProjects.pdf`, page 15. Project 13 classification scope, classifier and representation comparisons, confidence and error analysis, and optional tool integration.
- [S2] `Lecture2-Data Preprocessing and Feature Engineering.pdf`, pages 31, 32, and 33. Dimension, feature extraction, and feature selection. Pages 2 and 4 were also inspected for preprocessing context.
- [S3] `Lecture5-FundamentalClassificationAlgorithms.pdf`, pages 2, 4, and 5. Supervised classification and training versus testing. Pages 52, 53, and 54. Underfitting, overfitting, and noise.
- [S4] `Lecture6-ArtificialNeuralNetworks.pdf`, pages 57 and 58. Bag-of-words representation and lost word order.
- [S5] `ProjectRreportInstructions.pdf`, page 1. Report requirements and December 6, 2026 report-and-code deadline.

Implementation references are the baseline `scripts/smoke.py`, the pinned dependency resolution in `uv.lock`, and `docs/repo-guide.md`. Project decisions are defined in `docs/data-and-evaluation.md`, `docs/project-plan.md`, and the accepted `docs/m0-plan.md`. Lecture connections support those choices without turning our exact methods into course requirements.
