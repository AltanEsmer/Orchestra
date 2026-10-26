# Project plan

Orchestra studies course project 13, Learning to Route Queries in AI Systems. This plan prepares the work described in [issue #1](https://github.com/AltanEsmer/Orchestra/issues/1). It does not report experimental findings. The implementation covers the complete planned study workflow and has been verified with artificial fixtures. The reviewed guide-v1 pilot has 38 accepted rows; the 120-row release and actual experiment results remain absent.

The October 16 [M1 to M3 delivery plan](m1-m3-plan.md) specifies the data and comparison gates. Altan approved that implementation on October 16 and authorized the remaining automation and merges on October 22. The [automation plan](automation-plan.md) records the completed tooling scope and its human evidence boundary. No 120-row M1 release or trained research model exists. The accepted pilot is recorded separately.

## Research question and scope

How do text representations and classifiers affect first-action routing quality, confidence, and errors on a small, explicitly defined English query dataset?

The unit of prediction is one query with one first-action label. The proposed labels are `document_retrieval`, `knowledge_lookup`, `calculation`, and `direct_answer`. These are project choices, not a mandatory course taxonomy. Their operational meanings, exclusions, and examples live in [data and evaluation](data-and-evaluation.md). Inputs contain the context needed to select an action. There is no conversation history or tool availability inference in the first study.

Required outcomes are a classification formulation, comparisons of classifiers and representations, confidence analysis, and error analysis. The report must describe the data and models in Altan's own words and contain useful exploratory visualizations. Tool execution is optional. Deployment, an assistant UI, multi-step orchestration, live retrieval, model fine-tuning, and production user data are outside the initial scope.

## First vertical slice

The implemented workflow takes a versioned, labeled JSONL file, checks its schema and annotation status, assigns related queries to the same split, fits a training-only TF-IDF pipeline, and writes validation predictions and metrics. Run a most-frequent dummy classifier before logistic regression. Store query IDs, expected labels, predictions, and available scores so errors can be traced back to the input.

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
| Group by shared scenario or source, not request template (guide v2). | The v1 template rule let only a few public rows count, blocking M1. Scenario/source groups still stop a model from memorizing a shared source across splits; batch checks for request-type spread and source mix guard against a few request types or one source's phrasing dominating. Test scores now measure new topics and sources with familiar request types, not unseen request types. | An optional unseen-request-type analysis shows a large gap worth reporting as a limitation. |
| Use one local CPU and no paid APIs. | The planned sparse models suit a course-sized dataset. | Measured limits justify a documented resource change. |

## Risks and unresolved decisions

On October 24, Altan authorized public-source investigation to reduce further manual writing. [No Robots](evidence/public-direct-answer.md) adds thirteen provisional direct-answer candidates in a twenty-record sample. [Dolly](evidence/public-document-retrieval.md) adds three conditional document-reading candidates in twenty records, provided their original linked passages are retained outside router input. These sources have distinct licenses and need mapping, attribution, and grouping review. A [blind AI pass](evidence/pilot-ai-review.md) matched the original forty labels. Altan subsequently chose single-human annotation with disclosed AI checks. A dedicated AI review kind preserves its provenance, keeps his original labels, and requires human adjudication of flagged cases. The report must disclose single-annotator bias and AI assistance rather than independent human agreement.

The earlier Berkeley Function Calling Leaderboard inspection also aimed to reduce further manual writing. The [inspection](evidence/bfcl-compatibility.md) found 14 distinct provisional candidates in 40 records, mainly calculations, and no document-retrieval candidate in that bounded sample. It recommends a filtered supplement and further source assessment, not an unchanged replacement for all four classes. No public-source import, source adoption, first-action label-contract change, or model run has occurred. The pilot history contains forty human-authored candidates; 38 now qualify under guide v1. Public source annotation remains separate.

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

## Research steps after tooling preparation

1. Use the selected single-human, AI-assisted method, preserving Altan's forty original labels and recorded permission. Keep AI consistency separate from human agreement.
2. Pilot review and guide v1 are complete as of October 26. Guide v2 then regrouped the 38 accepted rows by shared scenario or source (23 groups) at Altan's request. Preserve the rows, two practice-only exclusions, actual human decisions, and the v1 family history.
3. Extend with licensed public human-authored examples where compatible. Preserve original wording and linked source context; review mappings rather than copying upstream task categories.
4. Reach 120 accepted queries, at least 30 per label and 15 independent groups per label. Freeze the expansion brief before viewing baseline errors.
5. Use the existing commands to validate, split by group, and run the dummy and TF-IDF logistic-regression baselines twice.
6. Check identical split membership and predictions. Inspect at least five validation errors, or all if fewer exist.
7. Update the evidence and learning log, then attempt the first-slice teach-back exercise. Continue to the main comparison only after the M2 acceptance evidence exists.

Executable commands are in the [runbook](run-experiments.md). Their research execution waits for accepted data and the recorded human evidence.

The October 26 [AI candidate supplement](evidence/template-expansion-draft.md) prepares forty unaccepted drafts at Altan’s explicit request. Conservative overlap review proposes nine new families and exposes three over-cap families. Human annotation, family adjudication, and cap selection precede import; the draft counts do not close the M1 release gap.

## Source authority

See [course sources](course-sources.md) for file locations and page-level course mappings. The course PDFs take precedence over this project plan if a discrepancy appears. Confirm later staff announcements separately and record their date and source.
