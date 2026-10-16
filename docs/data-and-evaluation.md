# Data and evaluation protocol

This is the proposed v1 protocol. No research dataset, trained router, or experimental score exists yet. The tiny examples in `scripts/smoke.py` are environment fixtures and must never enter the study.

The October 16 [M1 to M3 plan](m1-m3-plan.md) specifies the proposed implementation of this protocol. Its refinements below are planning decisions. They add no dataset, schema implementation, fitted model, or measured outcome. Implementation requires Altan's separate approval after the documentation PR merges.

## Prediction contract

Predict the first action required to answer a self-contained English query. Assume that the system has a named-document retriever, a structured knowledge lookup, and a calculator. The router sees only query text. It receives no hidden document content or conversation history. A model prediction is an action label, not an answer and not a complete tool sequence.

| Label | Positive definition and example | Negative example | Boundary example and rule |
| --- | --- | --- | --- |
| `document_retrieval` | Read an identified document or passage. "Summarize the cancellation clause in the attached contract." | "What is 12 times 8?" is calculation. | "Calculate the increase using the figures in the attached report." Retrieve the report first. |
| `knowledge_lookup` | Look up a specific fact or record in an identified structured catalog or knowledge base. "Find product A17's warranty period in the product catalog." | "Summarize the attached warranty PDF." requires document retrieval. | "What is the warranty?" lacks a source and item. Hold it for clarification. |
| `calculation` | Compute a numeric answer when the inputs already appear in the query. "What is 18 percent of 250?" | "Explain what a percentage means." is direct answering. | "Find today's exchange rate and convert 100 euros." requires unavailable live information. Exclude from v1. |
| `direct_answer` | Explain, rewrite, or answer without retrieving external facts or performing a requested calculation. "Explain why a fraction can be less than one." | "Look up invoice 42 in the billing database." is knowledge lookup. | "Explain how to multiply 12 by 8 without computing it." asks for an explanation. "Compute 12 times 8." asks for calculation. |

Source references are legitimate routing signals, but avoid making one trigger word perfectly identify a label. Include varied wording and hard negatives across labels. Preserve numbers and negation. Do not strip words such as "not" or replace all numbers before testing their effect.

For multi-action requests, label the earliest necessary dependency. Retrieval before calculation is a valid first-action case. If two independent actions have no uniquely justified order, mark the query `needs_review`. If context or tool availability is missing, do the same. Resolve it through re-annotation or exclude it with a reason. `needs_review` is annotation metadata, not a fifth target label or a confidence fallback. Keep excluded and out-of-scope examples in a separate challenge set with their counts. Do not silently force them into one of the four classes.

## Data sources and annotation

Start with human-authored scenarios using fictional documents, catalogs, and records. Do not ingest personal queries, private course submissions, or real customer records. Record Altan's authorship and intended dataset license before releasing rows. The repository's MIT code license does not automatically license third-party data or course PDFs.

Candidate extensions are published intent-classification datasets and public tool-routing benchmarks. Neither is approved yet. Intent labels may not map to the first-action contract. Before use, record the exact source URL, download date, version or hash, original license, permitted redistribution, and mapping rationale. Reject a source whose license or mapping cannot be established. Do not scrape a dataset merely to reach the target size.

If an LLM generates candidates later, record provider, model/revision, prompt, parameters, generation date, and human edits. Budget approval precedes paid generation; Altan owns course-rule compliance without an agent confirmation gate. Human review is mandatory. Synthetic data can encode generator vocabulary, clean label cues, and unrealistic balance. It cannot establish performance on real traffic. All variants of one generated scenario belong to one group, even when produced by different prompts.

Use a 40-query pilot, initially 10 queries per label. Aim for 120 accepted rows for the first slice and 400 for the main study, roughly 100 per class. These are targets, not observed counts. Target at least two independently written scenarios for every boundary in the table. Cap each paraphrase family at four rows so a few templates cannot dominate.

Altan labels every query with a rationale. Ask a second human to independently annotate at least 20 percent, stratified by proposed class, plus all ambiguous rows. Record pre-adjudication agreement and disagreements before resolving them. If no second annotator is available, record single-annotator bias and perform a delayed blind self-review. Agent agreement is not independent human annotation. Freeze the guide only after unclear pilot boundaries have been resolved.

## Planned row format and validation

Each JSONL row has the following fields. `scripts/validate_dataset.py` enforces this schema; the [annotation guide](annotation-guide.md) gives the pilot conventions.

| Field | Meaning |
| --- | --- |
| `query_id` | Stable unique string, such as `q0001`. |
| `group_id` | Shared scenario, template, or paraphrase family, assigned before splitting. |
| `text` | Nonempty query without an embedded gold-label hint. |
| `label` | One of the four labels for accepted rows, or null while unresolved. |
| `status` | `accepted`, `needs_review`, or `excluded`. |
| `source_id` | Reference to a provenance manifest containing author/source, license, date, and generation details if applicable. |
| `rationale` | Why the first action is required, or the exclusion reason. |
| `annotator_ids` | Pseudonymous annotator identifiers, without contact information. |
| `annotation_version` | Version of the label guide used. |

The validator rejects duplicate IDs, empty text, unknown labels, accepted rows with null labels, missing author or creation date in provenance, and absent group IDs. It also rejects exact duplicates after whitespace/case normalization and groups above four rows. A missing license is not a structural error, so an unresolved draft validates while permission is pending. The summary reports the dataset SHA-256, status, class, and group counts, word-length minimum/median/maximum, source mix, group-size distribution, and excluded rows with reasons, and lists groups whose accepted rows carry different labels for review. Near-duplicate inspection and merging related groups remain manual. Only accepted rows enter the supervised splits.

### Review ledger and readiness

Review evidence is a JSONL ledger with one object per reviewed row and exactly these fields: `query_id`, `original_label`, `review_label`, `reviewer_id`, `review_date` (ISO `YYYY-MM-DD`), `review_kind` (`second_human` or `delayed_self`), and `resolved_label`. `original_label` and `review_label` must be one of the four labels. `resolved_label` must also be a label, or null when the row was excluded after review. A `second_human` reviewer must not appear in that row's `annotator_ids`. `query_id` must exist in the dataset and appear once. Save `original_label` and `review_label` before discussion; `resolved_label` records the adjudicated result.

`--review LEDGER` validates the ledger and prints agreement: reviewed rows whose `original_label` equals `review_label`, divided by reviewed rows, with matching and reviewed counts per `review_kind`. It also prints the ledger SHA-256. Report the sampling method alongside the denominator.

`--ready` (requires `--review`) adds the M1 acceptance checks and exits 1 if any fails: at least 120 accepted rows; at least 30 accepted rows and 15 distinct groups per class; no `needs_review` row; a nonempty license for every source used by accepted rows; per class at least ceil(0.2 x accepted rows of that class) reviewed rows; a nonempty ledger; every accepted row in a mixed-label group has a ledger entry; and every ledger `resolved_label` equals the dataset label of that accepted row, or is null for an excluded row. These checks establish counts, permission records, and ledger consistency. They do not judge whether any label is semantically correct. The ledger has no ambiguity marker, so confirm by hand that every ambiguous or `needs_review`-origin row was reviewed.

## Split responsibilities and leakage controls

Create one group-aware, approximately stratified 60/20/20 train/validation/test split with seed 42. Assign whole groups, then record actual row and class proportions. The implementation must reject overlap and missing classes. If a class has too few independent groups, collect more data or reduce the taxonomy before freezing the study. Do not break groups just to hit exact percentages.

Persist query IDs and group IDs in a versioned split manifest. Keep the same split for every model and representation. Training fits vocabulary, IDF weights, scaling, model coefficients, and training-fold calibration. Validation selects hyperparameters, models, and any fallback threshold. The sealed test estimates final performance after those choices are frozen. Do not inspect test text or mistakes while tuning. Final test error analysis comes after the freeze and cannot feed another reported selection on the same test.

For M2, the planned allocator sorts query IDs and uses five shuffled `StratifiedGroupKFold` folds with seed 42. Combine held-out folds 0 through 2 as training, fold 3 as validation, and fold 4 as test. Validate achieved class coverage and proportions rather than assuming exact stratification. The implementation is `python -m orchestra split --config configs/m2.json`. It refuses unresolved `needs_review` rows and any class with fewer than five groups, takes each fold's own held-out indices (never the overlapping training indices), and raises if a partition lacks a class instead of searching seeds. The manifest records manifest version, dataset hash, seed, algorithm, fold-to-partition map, scikit-learn version, class order, query IDs per partition, group IDs, actual counts, and proportions. It is written once, and a later run that would produce different bytes is refused. `check_split` rejects stale hashes, duplicate membership, missing or extra IDs, group overlap, group mappings that disagree with the rows, unresolved rows, missing classes, and malformed manifests. The command materializes train and validation files separately from a sealed test file and prints counts only. Sealing is a workflow boundary, not encryption. The algorithm has run only on an artificial fixture (see `docs/evidence/m2-splits.md`), not on research data.

For M3, preserve every original row hash, label, group ID, and partition. Allocate only new independent groups with the same procedure and append them to a child manifest that records its parent hash. Never resplit all 400 rows, because M2 validation has already influenced development. Put new variants of old scenarios in the challenge collection. Review new groups against all previous families before allocation. If old annotations require correction, record a successor protocol and exposure history instead of overwriting M2 evidence. Keep every exposed group out of any replacement test set.

Freeze the expansion's collection brief before M2 error inspection. Collect new test candidates under that brief, rather than targeting observed model failures. Sealing restricts model-development access. It cannot undo exposure during human authoring or annotation, which must be disclosed. The planned runner reads separately materialized training and validation inputs and does not open test content. The splitter may inspect rows to allocate them and report aggregate counts.

Use a scikit-learn pipeline so training-only transforms also hold inside cross-validation. Calibration uses three group-aware training folds with every class represented, supplied as explicit index pairs. It must never fit on the final test or the validation rows used for selection. If there are too few groups per class for those folds, postpone calibration and report the data shortage. These choices follow scikit-learn's [leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html).

## Bounded experiment matrix

The mandatory comparison uses the following 14 configurations on the fixed split. No unbounded search is planned. Record all configurations, including unsuccessful ones.

| ID | Representation | Classifier | Candidate settings | Count |
| --- | --- | --- | --- | --- |
| B0 | No text information | `DummyClassifier(strategy="most_frequent")` | Training majority. | 1 |
| B1 | Word counts, unigrams | Multinomial naive Bayes | `alpha=1.0`. | 1 |
| L1 | Word counts, unigrams | Logistic regression | `C` in 0.1, 1, 10. | 3 |
| L2 | Word TF-IDF, unigrams | Logistic regression | `C` in 0.1, 1, 10. | 3 |
| S1 | Word TF-IDF, unigrams | Linear SVM | `C` in 0.1, 1, 10. | 3 |
| L3 | Word TF-IDF, unigrams and bigrams | Logistic regression | `C` in 0.1, 1, 10. | 3 |

Use lowercase word tokenization, no stop-word removal, `min_df=1`, and a 10,000-feature cap initially. Record all library defaults in the resolved configuration. TF-IDF uses its documented normalization and IDF settings. Keep model regularization and solver settings explicit in the future implementation. Raise logistic-regression iteration limits only when convergence warnings require it and record the change. B1 gives a course-aligned probabilistic baseline. L1 versus L2 holds the classifier fixed to compare weighting. L2 versus S1 compares linear classifiers on the same representation. L2 versus L3 tests short phrases. The [feature extraction guide](https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction) documents these representations.

The implementation plan proposes word token pattern `(?u)\b\w+\b` to retain single-character digits and words. Preserve the original text and negation. This representation still loses punctuation and does not faithfully encode signed or decimal numbers. The plan fixes TF-IDF normalization, solver settings, bounded convergence retries, and score types before any comparison. All of these remain unmeasured proposals.

Add one frozen sentence-embedding representation plus logistic regression at the same three C values only after a resource check. The candidate family is a small English sentence-transformer encoder. Before downloading, choose its exact model ID, immutable revision, license, dimension, maximum input length, pooling, and normalization. Cache by model revision and query hash. No fine-tuning is planned. This adds three configurations, for a maximum of 17. If the resource gate fails, the count-versus-TF-IDF comparison still satisfies the representation requirement. Neural representations extend Lecture 6; the specific pretrained encoder is external work, not lecture content.

Select by validation macro-F1. Break ties within 0.01 by lower complexity, then prediction latency, recording the rule before comparing. Report each family's validation selection. Freeze the selected systems for one final test pass so classifier and feature comparisons remain visible. Do not choose a new winner by test score. Seeds 7 and 21 are optional training/validation-only stability checks with the original test groups held fixed.

For M3, make that tie rule deterministic. Within each family, form the candidates within 0.01 of its best validation macro-F1 and prefer the smallest C. For an optional overall choice among tied family winners, use the declared simplicity order B0, B1, L1, L2, S1, L3. This is an explanatory and computational preference, not a theorem about model complexity. Use median prediction latency only if earlier keys tie, then configuration ID. Preserve per-family selections and matched-C comparisons regardless of the overall choice.

## Metrics, confidence, and errors

Report accuracy as secondary context and macro-F1 as the main metric. For each class, precision is TP/(TP+FP), recall is TP/(TP+FN), and F1 is 2PR/(P+R). Macro-F1 averages class F1 equally. Include class support, use zero for undefined scores, and flag missing predicted classes. Save confusion matrices as raw counts and row-normalized proportions. Plot class balance and query lengths before interpreting performance.

SVM decision margins are scores, not probabilities. Logistic-regression and naive-Bayes probability outputs are not automatically calibrated. For the selected logistic model, compare its raw probabilities with sigmoid calibration fitted through the training-only grouped folds. Evaluate multiclass log loss, multiclass Brier score defined as the mean sum of squared probability errors across classes, and a five-bin top-label reliability diagram. Report bin counts. ECE is a descriptive, bin-sensitive summary, not proof of calibration. The [calibration guide](https://scikit-learn.org/stable/modules/calibration.html) explains why calibration fitting needs independent predictions.

An optional abstention policy uses the highest calibrated class probability. Evaluate thresholds 0.0, 0.5, 0.6, 0.7, 0.8, and 0.9 on validation. Prefer maximum coverage among thresholds with at least 0.90 accepted-query accuracy; this is a design target, not a promised result. If none qualifies, report that no threshold met the target. Report accuracy-versus-coverage and accepted counts, plus per-class coverage. Define coverage as accepted/total, and selective accuracy as correct accepted/accepted. If no queries are accepted, accuracy is undefined. Freeze a threshold before the test pass. Fallback means request clarification or human review; no fallback tool is implemented here.

Inspect at least 20 validation errors across predicted and true classes, or all if fewer exist. Separate annotation ambiguity, missing context, vocabulary mismatch, negation, multi-action dependencies, and out-of-scope inputs. Retain correct examples for comparison. After the test freeze, present representative test mistakes with expected action, prediction, score type, and a reasoned interpretation. Label interpretations as hypotheses. If uncertainty intervals are reported, resample entire groups, not individual paraphrases, and disclose the number of independent groups.

## Reproducibility and resource budget

Every future run records the Git SHA and dirty status, Python and uv versions, lockfile hash, OS/CPU, dataset and annotation versions, raw-file hashes, split manifest hash, random seeds, resolved model/feature configuration, library/model versions, and start/end time. Save predictions, metrics, confusion matrices, and timing under `results/<run-id>/`. Store enough metadata to recreate each plot. Never treat an untracked notebook state as an experiment definition.

The current setup needs package downloads, one CPU, and no credentials. The planned sparse comparison targets a laptop with 8 GB RAM. The embedding gate allows one model download up to 500 MB and a 15-minute CPU pilot on 120 rows, with no paid API. These are proposed caps, not measured usage. Record runtime and peak memory before accepting the extension. Ask before paid services or larger compute commitments. Add visualization or embedding dependencies only when a committed experiment needs them.

On October 16, Altan reported that SDU will provide 10 GPU hours. The required M1 through M3 sparse study reserves that allocation and uses the CPU. No SDU access or hardware has been verified. The [compute plan](m1-m3-plan.md#measure-resources-before-using-the-gpu-allocation) gives a conditional optional-embedding budget and the access information needed only if measured CPU limits justify using SDU. No GPU job or model download is authorized by this planning change.

Keep raw downloads, processed data, models, local results, caches, `.env*`, and course PDFs out of Git. Commit small cleared fixtures, source/license manifests, split/configuration versions, and selected anonymized report evidence deliberately. Ignored results need an explicit backup or course submission archive containing the manifests and files required for reproduction. Record the archive location and checksum in the final handoff. Never load untrusted pickle/joblib artifacts. No secrets or API keys are required for the present scaffold.
