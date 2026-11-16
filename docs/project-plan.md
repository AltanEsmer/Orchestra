# Project plan

Orchestra studies course project 13, Learning to Route Queries in AI Systems. This plan develops the work described in [issue #1](https://github.com/AltanEsmer/Orchestra/issues/1). M1 froze 128 accepted rows, M2 reproduced its baselines, and [M3](evidence/m3-research-run.md) compared 14 configurations on 400 rows. [M3.5](m3-5-plan.md), requested after Altan's supervisor meeting, froze the [`m3-5-v1` release](evidence/m3-5-dataset.md) on November 2: 3,145 accepted rows split 1,888 / 629 / 628. The [27-configuration run](evidence/m3-5-full-run.md) selects TypeSafe Jev on validation, macro-F1 0.975 against 0.952 for L3-C10. On November 3 Altan accepted M3.5 and approved the test send, and the [M4 final test](evidence/m4-final-test.md) ran once: Jev scores 0.964 test macro-F1. Its [test mistakes](evidence/m4-final-test.md#test-mistakes-interpreted-after-the-freeze) are interpreted as hypotheses, the [M4 study guide](study-guides/m4-confidence-errors.md) is delivered, and Altan completed the M4 learning attempt on November 5, kept the flagged labels and accepted M4 on November 6. M5 began the same day.

The October 16 [M1 to M3 delivery plan](m1-m3-plan.md) records the original data and comparison gates. Altan approved that implementation on October 16 and authorized the remaining automation and merges on October 22. The [automation plan](automation-plan.md) records that tooling scope and its human evidence boundary. M3.5 extended it prospectively with the larger release, four new method families and their M4 integration.

Historical, October 31 to November 1. Public-source screening started on October 31 at Altan’s request. The [capacity screen](evidence/m3-5-capacity-screen.md) records fixed samples, exclusions and unresolved group/review capacity. On November 1 Altan replaced the original 2,500 minimum and 4,000 aim with a near-balanced 2,000-row working minimum, lookup between 350 and 500 rows ([option B](evidence/m3-5-option-b-supply.md)); accepted data remain 400. No new collection brief is frozen and no classifier is trained in this screening step.

Historical, October 31. The subsequent [group and quota audit](evidence/m3-5-group-quota-audit.md) reconstructs actual parent source/type counts and integrates 99 provisional calculation and 46 provisional lookup rows. Proposed groups still require semantic review. The balanced minimum requires at least 304 more non-keyed lookup and 234 more non-word-problem calculation candidates beyond this inventory, even if all current proposals become accepted. Continue those strata and resolve source/adapter holds before the collection-brief decision. The November 2 release supersedes this inventory.

## Research question and scope

How do text representations and classifiers affect first-action routing quality, confidence, and errors on a small, explicitly defined English query dataset?

The unit of prediction is one query with one first-action label. The proposed labels are `document_retrieval`, `knowledge_lookup`, `calculation`, and `direct_answer`. These are project choices, not a mandatory course taxonomy. Their operational meanings, exclusions, and examples live in [data and evaluation](data-and-evaluation.md). Inputs contain the context needed to select an action. There is no conversation history or tool availability inference in the first study.

Required outcomes are a classification formulation, comparisons of classifiers and representations, confidence analysis, and error analysis. The report must describe the data and models in Altan's own words and contain useful exploratory visualizations. Tool execution is optional. Deployment, an assistant UI, multi-step orchestration, live retrieval, model fine-tuning, and production user data are outside the initial scope.

## First vertical slice

The implemented workflow takes a versioned, labeled JSONL file, checks its schema and annotation status, assigns related queries to the same split, fits a training-only TF-IDF pipeline, and writes validation predictions and metrics. Run a most-frequent dummy classifier before logistic regression. Store query IDs, expected labels, predictions, and available scores so errors can be traced back to the input.

Completion means both baselines run twice from the same committed configuration and produce the same split membership and predictions. Macro-F1, class metrics, and a confusion matrix must be saved with provenance. A low score is a valid result. A target accuracy is not an acceptance condition. Test-set evaluation waits until the experiment and confidence choices are frozen.

## Milestones working back from submission

The [roadmap](../ROADMAP.md#milestones) is the primary tracker for milestone dates, dependencies, statuses, and completion evidence. Its targets lead to the December 6, 2026 submission deadline. Update that tracker when progress or dates change.

On October 31 Altan requested M3.5 before M4: expand the 400-row study with compatible public data to **at least 2,500 accepted rows, aiming for 4,000**, and add **Decision Tree, Random Forest, XGBoost, and TypeSafe AI Jev**. On November 1 Altan lowered the minimum to a near-balanced 2,000 rows after source discovery showed too few compliant lookups. Rerun the existing 14 configurations on the same expanded split. The [M3.5 plan](m3-5-plan.md) defines source/review capacity gates, a bounded matrix, Jev's distinct API comparison, split preservation, and the required M4 integration. M4 waits for this evidence. The supplied supervisor email motivates broader research; the four selected methods and numerical minimum are Altan's requested scope, not claims about the original course PDFs.

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
| Add M3.5 before confidence and final testing. | Larger, reviewed public-data coverage and three tree families plus Jev broaden the research. Preserve M3 and rerun its baselines on the new split. | Capacity or review evidence shows the minimum cannot be met before the deadline. |
| Treat Jev as a separate pretrained API condition. | It takes query text and label instructions instead of fitting the same TF-IDF features. Record access, costs, model/prompt versions, data handling and pretraining-overlap limits. | Concrete API feasibility and budget decision before execution. |
| Reproduce the study by replaying Jev's archived answers, not by asking Jev again (M6, November 10). | Resending the 628 test queries would expose the sealed text a second time, need Altan's approval and mix model drift into a reproduction check. The replay proves the computation from answers to results, not that Jev would answer the same today. | Altan approves a fresh Jev run to measure answer drift, or the Jev model version changes before submission. |

## Risks and unresolved decisions

The October 24–26 source investigations below are historical. The M3.5 release `m3-5-v1` now exists, and Jev access was verified with Altan's key on November 2. Jev requests cover validation only; test queries reach TypeSafe only after Altan's explicit approval, through `final-test --send-jev-test`.

On October 24, Altan authorized public-source investigation to reduce further manual writing. [No Robots](evidence/public-direct-answer.md) adds thirteen provisional direct-answer candidates in a twenty-record sample. [Dolly](evidence/public-document-retrieval.md) adds three conditional document-reading candidates in twenty records, provided their original linked passages are retained outside router input. These sources have distinct licenses and need mapping, attribution, and grouping review. A [blind AI pass](evidence/pilot-ai-review.md) matched the original forty labels. Altan subsequently chose single-human annotation with disclosed AI checks. A dedicated AI review kind preserves its provenance, keeps his original labels, and requires human adjudication of flagged cases. The report must disclose single-annotator bias and AI assistance rather than independent human agreement.

The earlier Berkeley Function Calling Leaderboard inspection also aimed to reduce further manual writing. The [inspection](evidence/bfcl-compatibility.md) found 14 distinct provisional candidates in 40 records, mainly calculations, and no document-retrieval candidate in that bounded sample. It recommends a filtered supplement and further source assessment, not an unchanged replacement for all four classes. No public-source import, source adoption, first-action label-contract change, or model run has occurred. The pilot history contains forty human-authored candidates; 38 now qualify under guide v1. Public source annotation remains separate.

The largest scientific risks are annotation shortcuts, overlapping action meanings, paraphrase leakage, a small test set, and synthetic language that fails to resemble real users. The [data protocol](data-and-evaluation.md) addresses each and requires limitations in the report. More models cannot repair unclear labels.

Altan handles oral-exam arrangements, AI-use rules, disclosure, and submission mechanics. The agent does not require administrative answers to proceed with approved work. Before any external data or embedding download, record its license and immutable revision. M3's 400-row target was achieved. M3.5 required at least 2,000 accepted rows after Altan's November 1 decision; `m3-5-v1` holds 3,145. Advance to M4 only after Altan accepts M3.5. Keep the held-out test sealed and report exclusions and uncertainty honestly.

## Report outline and evidence map

The November 6 [full M5 draft](../report/main.tex) expanded the outline into six IEEE two-column pages, within the required 5–12 pages. The [November 9 review](evidence/m5-report-review.md) adds the reliability figure and cue analysis, bringing the manuscript to seven pages. The [evidence map](../report/README.md) links four figures and five tables to the frozen study. The initial eight-page budget served as a planning target. Altan now revises the account in his own words and checks the revised pagination.

| Report part | Question or requirement | Planned evidence | Limitations to discuss |
| --- | --- | --- | --- |
| Introduction, about 1 page | Why first-action routing, and what is being predicted? | Action table and one query-to-action example. | Action availability and single-turn English scope. |
| Data and exploratory analysis, about 1.5 pages | What distribution do the labels represent? | Provenance, annotation agreement, class/group counts, query-length and class-balance figures. | Authored language, exclusions, sample size. |
| Methods, about 1.5 pages | What changes across classifier and representation comparisons? | Frozen matrix, split diagram, feature and model equations. | Limited tuning budget and model families. |
| Results, about 1.5 pages | Which choices help, and by how much? | Macro-F1 comparison, per-class table, confusion matrix, timing. Saved: validation comparison `results/m3-5-full-a` ([record](evidence/m3-5-full-run.md)); one sealed-test pass `results/final-test-m3-5` with metrics, confusion matrices and by-origin scores ([record](evidence/m4-final-test.md)). | Small samples and seed variation; one test split and one opening; S1-C1 outranked the frozen L3-C10 on test. |
| Confidence and error analysis, about 1.5 pages | Can confidence guide fallback, and what mistakes remain? | Reliability diagram, log loss/Brier score, accuracy-versus-coverage curve, annotated error examples. Saved: validation reliability bins, thresholds and probability losses in `results/m4-5-validation`; test reliability, thresholds, Brier and ECE in `results/final-test-m3-5`; interpreted validation and test errors in `results/validation-interpretations-m3-5.jsonl` and `results/test-interpretations-m3-5.jsonl` ([record](evidence/m4-final-test.md#test-mistakes-interpreted-after-the-freeze)). The draft uses the saved bin counts and a threshold table for confidence, plus the selected system’s test confusion matrix for errors. | Imperfect calibration and domain shift; ECE depends on the bins; error categories are one reader's hypotheses; withheld passages may cause about half of Jev's errors. |
| Discussion and conclusion, about 1 page | What does the evidence support? | Conclusions tied to run IDs, rejected alternatives, reproduction instructions. | No general claim about all AI systems or tool success. |

References and final pagination must fit the course limit. Each result or figure links to a saved run and configuration. Do not write a conclusion before its evidence exists. Keep an agent-assistance record in the learning log. Altan manages the applicable disclosure requirements.

## Research steps after tooling preparation

The sequence below records the original M1/M2 work, now completed in the linked evidence. Continue with the five stages in the [M3.5 plan](m3-5-plan.md), then M4; do not repeat collection or overwrite frozen artifacts from these earlier steps.

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

## M7 package decision, November 13, 2026

Altan requested merging M6 PR #36 and finishing M7. PR #36 merged as `4a5b17c7343f065c429b9c13ec1af3ce94438d6a` after an independent exact-head review. M7 packages the existing frozen study and corrects the report's obsolete reproduction paragraph. It adds no model, data, metric, calibration rule, or experiment.

The local package pairs a self-contained Git bundle and a source ZIP with the report PDF, the unchanged M6 study ZIP, source-specific license records, checksums, and reproduction instructions. The bundle preserves the Git metadata required by `reproduce_study.sh`; the source ZIP is convenient for inspection. A manifest names the exact source commit. The final evidence commit can follow that source commit without changing the frozen scientific files. Verify the bundle by cloning it into an empty directory and running the complete reproduction with archived Jev replies. Never resend queries for this check.

The package remains local because the study ZIP includes query text. M8 submission remains Altan's task. The report retains its assistance disclosure and own-word revision requirement. Unanswered rehearsal questions stay visible; producing the package does not count as a student answer. The [M7 guide](study-guides/m7-freeze.md) explains the freeze and later correction procedure.
