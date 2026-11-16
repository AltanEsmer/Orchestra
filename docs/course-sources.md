# Course sources

The course files remain outside Git. On Altan's machine their directory is `/Users/altanesmer/Desktop/SM1/AI/`. In the original checkout this is the parent directory. Managed worktrees are elsewhere, so use the absolute source location there. Redistribution permission has not been established. A new contributor must obtain the files through the course.

All page references below are PDF page numbers, counted from one. Source review occurred on October 7, 2026. The two primary requirement pages were extracted and visually inspected. Relevant lecture pages were checked for the topic mapping.

| Source file | Pages | Verified requirement or connection |
| --- | --- | --- |
| `CourseProjects.pdf` | 15 | Project 13 requires classification, classifier and feature comparisons, confidence and error analysis. Listed actions are examples. Tool integration is optional. |
| `ProjectRreportInstructions.pdf` | 1 | Own-word research report describing data and models, useful exploratory graphs, 5–12 pages, IEEE conference two-column format, report submission through itslearning. Report and code deadline is December 6, 2026. |
| `Lecture2-Data Preprocessing and Feature Engineering.pdf` | 2, 4, 18; 7–8; 26–28; 31–33; 68 | Cleaning, scientific questions, sampling/privacy, exploration, transformation, feature extraction versus selection, and data quality. Supports annotation checks and representation choices. |
| `Lecture5-FundamentalClassificationAlgorithms.pdf` | 2, 4–5; 52–57; 64, 67–72; 76–80; 86, 88–89 | Supervised classification, unseen testing, overfitting, model simplicity, Bayes/naive Bayes, SVM margins, regularization, multiclass methods. Supports the bounded classifier comparison. |
| `Lecture6-ArtificialNeuralNetworks.pdf` | 8; 57–58; 78–79 | Neuron/logistic analogy, bag of words and lost order, neural training cost and interpretability. Supports a simple baseline before an optional frozen encoder. |
| `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` | 6, 10–12, 14; 18, 28–29, 31–32, 35–36, 38–39; 47; 52–54, 56–61; 68–69; 80–81 | Tree strengths and weaknesses, bagging and random forests, boosting and XGBoost, train/validation/test roles, confusion-matrix metrics, class imbalance, hyperparameters. Supports the M3.5 tree families and validation-only selection; reviewed November 3, 2026. |
| `Lecture4-LinearModelsforRegression.pdf` | 60–65; 67 | Ridge/LASSO, bias–variance, cross-validation for hyperparameters. These are supporting concepts; regression is not the routing target. |
| `Lecture3-Clustering.pdf` | 2–3; 43; 58 | Clustering and ambiguity, validation, silhouette. Optional exploration only. Clustering does not replace supervised classification. |

TF-IDF, pretrained sentence embeddings, calibration, macro-F1, and classifier confusion matrices are project method choices. Do not claim these specific techniques were mandated by the inspected lectures. Lecture 3's page 50 discusses precision, recall, and F-measure for clustering.

The report instructions do not establish oral-exam format, AI-use policy, a submission time, or the code-upload mechanism. On October 8, 2026, Altan removed confirmation of these details from agent work and milestone gates. He owns course administration. This decision changes the workflow, not what the PDFs establish.

## Ongoing lecture review

Altan will add lecture slides to `/Users/altanesmer/Desktop/SM1/AI/`. During each milestone, inspect the relevant available files and record filenames, one-based PDF pages, review date, and SHA-256 hashes in its study guide. Refresh affected explanations if a source changes. Do not copy course PDFs into Git or the generated guides. Paraphrase concepts and cite the source rather than reproducing slides. Unavailable topics remain labeled as project choices or external methods until a verified course connection exists.

On November 3, 2026, the M4 guide added Lecture 5 p. 80 (soft margin), Lecture 7 p. 47 (cross-validation against overfitting) and p. 53 (an independent test set), and noted Lecture 7 pp. 58 to 61 (ROC and AUC) as seen but unused. `UTF-8''Lecture8-Hadoop%20Fundamentals%20and%20MapReduce.pdf`, SHA-256 `997b6d2d5e9114951b0d05713f49d79c98e4f2a074fe2e8dc73bf2f5f31d3098`, was new since November 2. A text search of all 106 pages found no confidence, calibration or error-analysis content, so it is not relevant to M4. Its pages were not rendered to look for image-only content.

On November 10, 2026, the M6 guide re-extracted its cited pages and recomputed the hashes of the course files in the folder. The cited files match the hashes recorded in earlier guide manifests, and no lecture file is newer than Lecture 8. The guide cites Lecture 7 p. 54 (the leakage diagram, image only, rendered and viewed) for the three-set structure. Its validation arm reads "biased towards the test set", which looks like a slip, so it is not cited for that wording. Lecture 7 p. 52 calls the validation error an unbiased estimate; the guide treats that as a contrast with the project's optimistic selected validation score. A text search of Lectures 1 to 8 found no page on reproducibility, seeds, locked environments, calibration, TF-IDF or macro-averaging. These remain project choices or external methods.

The supplied download `UTF-8''Project%20Rreport%20Instructions.pdf` was checked on October 8 and is byte-identical to the report-instructions copy below. January 2027 is Altan's oral-preparation target; the supplied instructions contain no oral date.

## Source fingerprints

These SHA-256 hashes identify the inspected copies. Recompute with `shasum -a 256` when files change.

| File | SHA-256 |
| --- | --- |
| `CourseProjects.pdf` | `d4e98da373cbdcd62f804d2cd0f957bbaa53294205762ba6d1dc04b26b74fdca` |
| `ProjectRreportInstructions.pdf` | `00ab8140f009f52fd9f552daa61ade6f628bdd1125096d62c54e07f06e1519a5` |

## External implementation references

The following official references were checked on October 7, 2026. Library behavior for experiments must match the version in `uv.lock`.

- [uv project workflow](https://docs.astral.sh/uv/guides/projects/) explains environment synchronization and lockfiles.
- [scikit-learn leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html) supports training-only preprocessing and pipelines.
- [scikit-learn text features](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) documents count and TF-IDF representations.
- [scikit-learn calibration](https://scikit-learn.org/stable/modules/calibration.html) distinguishes classifier outputs from calibrated confidence.

These references support implementation choices. They do not create additional course requirements.

## M7 source review, November 13, 2026

The course folder still contains Lectures 1 through 8, with no newer lecture. The agent re-extracted `CourseProjects.pdf` p. 15 and `ProjectRreportInstructions.pdf` p. 1 and inspected both rendered pages. The requirements remain classification, classifier/feature comparison, confidence/error analysis, and an own-word IEEE two-column report of 5–12 pages, due December 6. Tool integration remains optional.

For the M7 guide, the agent re-extracted Lecture 7 pp. 52–54 and 56–57 and Lecture 6 pp. 57–58. It inspected the image-only leakage diagram on Lecture 7 p. 54 and the confusion matrix on p. 56. The earlier caveat about p. 54's validation caption remains. M7 cites p. 53 for independent testing and p. 57 for precision, recall and F1, and Lecture 6 pp. 57–58 for lost word order. Checksums, bundles, replay and package freezing are project engineering choices. The M7 guide records full source hashes. No course PDF enters the package or Git.
