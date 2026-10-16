# Project plan

Orchestra studies course project 13, Learning to Route Queries in AI Systems. This plan prepares the work described in [issue #1](https://github.com/AltanEsmer/Orchestra/issues/1). It does not report experimental findings. The implementation currently verifies the Python environment and validates annotated row structure and provenance.

The October 16 [M1 to M3 delivery plan](m1-m3-plan.md) specifies the next implementation, its acceptance gates, resource limits, and supporting documents. Its planning PR is authorized for merge. Implementation waits for Altan's subsequent approval. The ordered units in that plan refine the first-session outline below without claiming any dataset or trained model exists.

## Research question and scope

How do text representations and classifiers affect first-action routing quality, confidence, and errors on a small, explicitly defined English query dataset?

The unit of prediction is one query with one first-action label. The proposed labels are `document_retrieval`, `knowledge_lookup`, `calculation`, and `direct_answer`. These are project choices, not a mandatory course taxonomy. Their operational meanings, exclusions, and examples live in [data and evaluation](data-and-evaluation.md). Inputs contain the context needed to select an action. There is no conversation history or tool availability inference in the first study.

Required outcomes are a classification formulation, comparisons of classifiers and representations, confidence analysis, and error analysis. The report must describe the data and models in Altan's own words and contain useful exploratory visualizations. Tool execution is optional. Deployment, an assistant UI, multi-step orchestration, live retrieval, model fine-tuning, and production user data are outside the initial scope.

## First vertical slice

The next implementation takes a versioned, labeled JSONL file, checks its schema and annotation status, assigns related queries to the same split, fits a training-only TF-IDF pipeline, and writes validation predictions and metrics. Run a most-frequent dummy classifier before logistic regression. Store query IDs, expected labels, predictions, and available scores so errors can be traced back to the input.

Completion means both baselines run twice from the same committed configuration and produce the same split membership and predictions. Macro-F1, class metrics, and a confusion matrix must be saved with provenance. A low score is a valid result. A target accuracy is not an acceptance condition. Test-set evaluation waits until the experiment and confidence choices are frozen.

## Milestones working back from submission

The [roadmap](../ROADMAP.md#milestones) is the primary tracker for milestone dates, dependencies, statuses, and completion evidence. Its targets lead to the December 6, 2026 submission deadline. Update that tracker when progress or dates change.

Understanding checkpoints remain in the [learning log](learning-log.md#topic-ledger-and-question-bank). At each milestone, review the corresponding topics and carry gaps forward. These checkpoints are part of the work plan, not scheduled notifications.

## Explain and defend each milestone

The objective is to complete the project and defend its methods and findings in the report and oral exam. Altan approved the [M0 delivery plan](m0-plan.md) on October 8, 2026. Course-rule confirmation is removed from agent work and milestone acceptance; Altan owns administration.

Every milestone includes an updated [study guide](study-guides/README.md), exported to `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/`. Keep its editable source in Git. Start with a plain-language lesson, then give implementation details, a concrete query trace, course connections, choices, actual checks, limitations, report evidence, and unanswered oral questions. Update the guide after meaningful changes and retain a dated snapshot at milestone completion.

At each milestone, inspect relevant slides available in `/Users/altanesmer/Desktop/SM1/AI/`. Cite the exact filename and one-based PDF pages, record the inspected revision, and distinguish lecture concepts from project-specific techniques. New slides may add or revise connections, but do not justify retroactive claims that unfinished work exists. Source refresh happens during milestone work, not through a background monitor.

After December submission, use the frozen project, saved results, and guide collection for oral practice through January 2027. Trace unfamiliar queries, explain a course principle and where the project applies it, justify an alternative, and discuss an observed error. Record actual answers and revisit gaps. January is Altan's stated target; no exact exam date is inferred. The final report is a separate synthesis in Altan's own words, not a concatenation of study guides.

## Decisions and rejected alternatives

| Decision | Reason and consequence | Revisit when |
| --- | --- | --- |
| Predict the first action. | A single complete route would require sequence labels and tool execution semantics. First-action classification fits the course task. | After the required comparisons and analysis are complete. |
| Use four action labels and an annotation holdout for ambiguous queries. | This makes action boundaries explicit without teaching the model an incoherent catch-all class. Report exclusion counts. | Pilot agreement exposes a boundary that annotators cannot apply consistently. |
| Begin with human-authored English queries. | No external redistribution or API dependency is needed to start. Authored queries still have synthetic-data limitations. | A licensed, compatible external corpus is verified. |
| Use Python, uv, scikit-learn, and a plain smoke script. | The project needs a reproducible numerical environment. A packaged CLI and service framework add little evidence at this stage. | Reusable training code has actual callers. |
| Compare sparse count and TF-IDF features first. | This guarantees a representation comparison even if pretrained embeddings are infeasible. | The frozen-embedding resource check passes. |
| Use one local CPU and no paid APIs. | The planned sparse models suit a course-sized dataset. | Measured limits justify a documented resource change. |

## Risks and unresolved decisions

The largest scientific risks are annotation shortcuts, overlapping action meanings, paraphrase leakage, a small test set, and synthetic language that fails to resemble real users. The [data protocol](data-and-evaluation.md) addresses each and requires limitations in the report. More models cannot repair unclear labels.

Altan handles oral-exam arrangements, AI-use rules, disclosure, and submission mechanics. The agent does not require administrative answers to proceed with approved work. Before any external data or embedding download, record its license and immutable revision. Dataset size is a collection target, not a guaranteed sample size. If fewer than 400 rows are feasible, keep the held-out test and report uncertainty instead of inventing data or hiding exclusions.

## Report outline and evidence map

Target an eight-page draft within the required 5–12 pages. Use IEEE conference two-column format. The final prose must be Altan's own account of work he can explain.

| Report part | Question or requirement | Planned evidence | Limitations to discuss |
| --- | --- | --- | --- |
| Introduction, about 1 page | Why first-action routing, and what is being predicted? | Action table and one query-to-action example. | Action availability and single-turn English scope. |
| Data and exploratory analysis, about 1.5 pages | What distribution do the labels represent? | Provenance, annotation agreement, class/group counts, query-length and class-balance figures. | Authored language, exclusions, sample size. |
| Methods, about 1.5 pages | What changes across classifier and representation comparisons? | Frozen matrix, split diagram, feature and model equations. | Limited tuning budget and model families. |
| Results, about 1.5 pages | Which choices help, and by how much? | Macro-F1 comparison, per-class table, confusion matrix, timing. | Small samples and seed variation. |
| Confidence and error analysis, about 1.5 pages | Can confidence guide fallback, and what mistakes remain? | Reliability diagram, log loss/Brier score, accuracy-versus-coverage curve, annotated error examples. | Imperfect calibration and domain shift. |
| Discussion and conclusion, about 1 page | What does the evidence support? | Conclusions tied to run IDs, rejected alternatives, reproduction instructions. | No general claim about all AI systems or tool success. |

References and final pagination must fit the course limit. Each result or figure links to a saved run and configuration. Do not write a conclusion before its evidence exists. Keep an agent-assistance record in the learning log. Altan manages the applicable disclosure requirements.

## First work session after preparation

1. Run the [README commands](../README.md) and explain why the dummy classifier ignores query meaning.
2. Read the action definitions. Write 10 independent queries per label for the pilot. Keep related variants under one group ID.
3. Review ambiguous and multi-action examples using the annotation policy. Revise and version the guide before collecting more rows.
4. Grow to 120 accepted queries, at least 30 per label and 15 independent groups per label. Keep enough groups for every split.
5. Implement schema and duplicate checks, then a persisted group-aware split. Verify that groups do not overlap.
6. Implement the dummy and TF-IDF logistic-regression baselines with their saved configuration and validation outputs.
7. Rerun and compare split IDs and predictions. Inspect at least five validation errors, or all errors if fewer exist.
8. Update the walkthrough and learning log, then answer the first-slice teach-back questions. Stop when the vertical-slice completion condition above is met.

Training and evaluation commands are intentionally not published as runnable commands yet.

## Source authority

See [course sources](course-sources.md) for file locations and page-level course mappings. The course PDFs take precedence over this project plan if a discrepancy appears. Confirm later staff announcements separately and record their date and source.
