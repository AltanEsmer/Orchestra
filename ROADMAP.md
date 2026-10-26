# Roadmap

Last updated: October 26, 2026. This is the primary progress tracker for course project 13. Preparation was delivered through [issue #1](https://github.com/AltanEsmer/Orchestra/issues/1); the milestone issues below track the remaining work. The [project plan](docs/project-plan.md) owns scope and decision rationale; [architecture](architecture.md) owns component responsibilities. The [learning log](docs/learning-log.md) tracks understanding separately.

## Current position

Preparation was reviewed and merged in [PR #2](https://github.com/AltanEsmer/Orchestra/pull/2) on October 7, 2026, as [`08cce7b`](https://github.com/AltanEsmer/Orchestra/commit/08cce7b). Issue #1 is closed. The locked environment and smoke check have passed. M0 now delivers a course-linked study PDF and an introductory learning checkpoint under the [accepted plan](docs/m0-plan.md). Altan removed course confirmation as a gate on October 8. On October 16 Altan closed issue #3, so M0 is closed by his decision. The introductory learning response was never recorded; it moves into M1 as an open learning gap rather than counting as answered. M1 now has forty human-authored pilot candidates, ten per action, and Altan's explicit study-use and sharing permission. A blind AI pass matched all forty original labels; it is consistency evidence, not independent human review. Altan selected single-human annotation with disclosed AI checks on October 24. Guide v1 and pilot review are complete: 38 accepted pilot rows across 19 request templates, plus two practice-only exclusions. No 120-row M1 release, trained router, experimental metric, or submitted report exists yet.

Statuses mean **not started**, **in progress**, **in review**, **done**, or **blocked**. “Done” requires the stated completion evidence. A blocked item records what must change and who can resolve it. Dates are targets, not evidence of completion.

The October 16 [M1 to M3 plan](docs/m1-m3-plan.md) is a documentation-only delivery, accompanied by an [exam, presentation, and report methods preview](docs/study-guides/m1-m3-methods-preview.md). Altan authorized creating and merging the planning PR, then stopping for implementation approval. He gave that approval on October 16 after PR #15 merged. The five delivery units are now implemented as tooling and tested on artificial fixtures only. M2 and M3 are blocked on accepted M1 data. The original forty labels and permission are recorded; pilot review and grouping are complete, while expansion to the accepted M1 release remains outstanding. No research split, run, or metric exists.

## Automation handoff, October 22

PR #16 is merged as `d666988`. The remaining tooling now includes readiness and blind-review preparation, frozen study configs, confidence/calibration, validation interpretation checks, final-test receipts, scientific figures, a compiling IEEE report template, verified local archives, clean reproduction, and CI. [Completion evidence](docs/evidence/automation-completion.md) distinguishes artificial checks from research results. [The manual guide](docs/manual-steps.md) now continues with review decisions; the forty-query collection and permission steps are complete. The agent operates the commands as human evidence arrives.

All currently independent software work is implemented. Actual research execution remains dependent on accepted, reviewed data. Public human-authored supplements are being assessed to reduce further manual writing. M1–M8 stay open because their acceptance conditions include data, research results, writing, learning, or submission. Passing fixture checks does not close them. The October 18 M1 target has passed. The October 25 M2 target has also passed because M1 is unfinished. The dates below remain original targets; rebaseline them after pilot adjudication and dataset readiness, rather than claiming an unsupported completion date.

## Completion estimate, October 26

Overall completion is **approximately 35%**. This is a planning estimate of deliverables, not a measured percentage of code, elapsed time, model quality, or course marks. Fixed weights below yield 34%, rounded to the nearest five percentage points. A template earns limited preparation credit; it does not count as written research findings.

| Workstream | Weight | Estimated completion | Evidence |
| --- | ---: | ---: | --- |
| Study design and planned software | 25% | 100% | Defined protocol; implemented tooling; 208 tests and artificial end-to-end workflow evidence. |
| Data preparation and acceptance | 25% | 30% | Guide v2; 38 accepted pilot rows in 23 scenario/source groups; two exclusions; public sources still await adoption and annotation. |
| Research experiments | 20% | 0% | No research split, trained model, validation run, or final test. |
| Results, confidence, and error interpretation | 10% | 0% | No measured research results to interpret. |
| Final report | 15% | 10% | Compiling IEEE template and evidence outline; no authored final manuscript or results. |
| Research reproduction, oral rehearsal, and submission | 5% | 0% | Fixture reproduction exists; research archive, rehearsal, and submission evidence do not. |

## Current data path

Retain Altan's forty pilot queries and original labels. Assess public supplements before asking for more authored queries. The bounded samples establish potential sources, not enough accepted rows to fill M1:

| Source | Screened | Provisional contribution | Remaining condition |
| --- | ---: | --- | --- |
| [Berkeley BFCL](docs/evidence/bfcl-compatibility.md) | 40 | 14 distinct texts: 11 calculation, 2 lookup, 1 direct answer | Remap from function calls to first actions; deduplicate and review. |
| [No Robots](docs/evidence/public-direct-answer.md) | 20 | 13 direct-answer texts | CC BY-NC 4.0 notices; review wording, rights, and groups. |
| [Dolly](docs/evidence/public-document-retrieval.md) | 20 | 3 conditional document-reading texts | Preserve original linked passages outside classifier input; CC BY-SA 3.0 notices; review mapping. |

These convenience samples are not corpus proportions. An ignored local shortlist preserves all thirty provisional public texts, including three conditional Dolly records with separately linked original passages. Cross-source exact-text checking found seventy distinct texts when combined with the forty-query pilot: 21 calculation, 12 lookup, 24 direct answer, and 13 document retrieval. Distinct text is not an independent scenario group. These are inspected candidates, not seventy accepted or test-unseen rows.

No public source is yet in the accepted dataset. Do not combine source licenses under the repository's MIT license. Prevent source style from becoming a shortcut for the label; record source-by-class counts and report any confounding that remains. Guide review precedes bulk expansion, so the current shortlist does not claim to finish the 120-row collection.

The [blind AI pilot check](docs/evidence/pilot-ai-review.md) preserved all original labels and found 40/40 label matches. Altan asked about AI review instead of another person. Altan explicitly chose single-human annotation with disclosed AI checks. AI entries use their own `ai_assisted` kind and evidence hashes, separate from human agreement. Clear matches retain the original human label; flagged cases and disagreements need an actual human adjudication, including a decision to keep the original label. Guide v1 and pilot boundary/group review are complete; accepted-data expansion follows under that fixed rule.

On October 26, Altan completed the [pilot review and guide-v1 decisions](docs/evidence/pilot-guide-v1.md). A group is a shared request template: the same user goal solved by the same procedure, whatever the scenario. Broader families reduce independent group counts. There are 38 accepted rows across 19 templates: calculation 9 rows/6 groups, document retrieval 9/5, lookup 10/4, and direct answer 10/7. Mixed-label groups overlap those counts. q0014 and q0037 remain practice-only in the audit history. All individual pilot flags and grouping questions are resolved; no 120-row M1 release exists. Altan correctly explained grouping-related score optimism; other leakage controls remain to practice. Next is licensed public-source expansion and genuine review of new labels. “Handbook” is a prospective validation error-analysis cue, not an observed effect.

The October 26 [expansion screen](docs/evidence/public-expansion-screen.md) judged 80 seeded Dolly records and every read-only BFCL SQL record by request template. Most fall into existing families that are full or nearly full. If every proposal were accepted, document retrieval would reach about 24 rows/8 groups and lookup about 16 rows/6 groups, both short of 30/15. Nothing was imported.

Altan then asked for simpler, less strict rules with high quality kept. [Guide v2](docs/evidence/guide-v2.md) groups rows by shared variation, source or named setting, situation, or public record instead of request template, and adds batch checks: near-duplicates, no request type above 40 percent of a class, and at least two sources per class with none above 75 percent. The pilot became 23 groups (calculation 9, document retrieval 8, lookup 7, direct answer 7) with labels and text unchanged. Under v2, Dolly alone covers the document-retrieval group gap. Lookup still needs request types beyond BFCL's condition filters, and calculation and direct answer need about 10 and 6 more screened rows.

Altan approved the regrouping and the Dolly attachment adapter, and adopted Dolly, BFCL, and No Robots. The [guide-v2 import](docs/evidence/public-import-v2.md) adds 90 `needs_review` candidates: 22 document, 22 lookup, 23 calculation, and 23 direct answer. If every proposal is accepted, each class reaches 30–33 rows and 26–32 groups and passes the batch checks. Altan approved all proposed labels. A blind AI check agreed on 90 of 90 ([review record](docs/evidence/public-review-v2.md)): Altan then adjudicated the 55 flagged rows by accepting the recommendations. All 128 rows are accepted, each class has 31–33 rows and 25–31 groups, and the readiness check passes. Altan froze it on October 26 as `data/processed/m1-v1.jsonl` with the `reviews-v2.jsonl` ledger. M2 baselines are next.

The next sequence is licensed candidate expansion to the first 120-row target, baselines, the main comparison targeting 400 rows, confidence and final test, then report and reproduction. Keep the existing four labels and query-only prediction contract. Dataset discovery has not changed the research question.

## Milestones

Dates use Europe/Copenhagen. December 6 is the course submission date; earlier dates are project targets. Altan handles submission timing and course administration.

| ID | Target date | Milestone | Issue | Status | Completion evidence or remaining gate |
| --- | --- | --- | --- | --- | --- |
| M0 | October 11, 2026 | Preparation and course-linked study guide | [#3](https://github.com/AltanEsmer/Orchestra/issues/3) | Done | Closed by Altan on October 16. Environment and planning merged in PR #2; M0 PDF delivered, checked, and snapshotted. Exception: no learning response was recorded, so the checkpoint carries into M1 unanswered. |
| M1 | October 18 | Annotation pilot and first dataset | [#4](https://github.com/AltanEsmer/Orchestra/issues/4) | In progress | Forty authored candidates and permission recorded; blind AI check complete; free-source samples inspected. Guide v1 review complete; guide v2 regrouped 38 accepted pilot rows into 23 scenario/source groups. Adopt compatible sources and reach 120 rows with provenance, 30 rows and 15 groups per class. Record disagreements and exclusions. |
| M2 | October 25 | First reproducible baseline | [#5](https://github.com/AltanEsmer/Orchestra/issues/5) | Blocked | Split, run, and compare commands exist and pass on fixtures. Blocked on accepted M1 data (Altan). After M1: validate rows and splits; run dummy and TF-IDF logistic regression twice with identical split membership and predictions. Save validation metrics and provenance. |
| M3 | November 8 | Main classifier and representation comparison | [#6](https://github.com/AltanEsmer/Orchestra/issues/6) | Blocked | Extend, 14-configuration run, select, and report commands exist and pass on fixtures. Blocked on M2 evidence and the 400-row collection (Altan). After M2: freeze the main dataset, target 400 accepted queries, and complete the 14 required configurations. Save all outcomes and validation selections. |
| M4 | November 15 | Confidence, errors, and final test | [#7](https://github.com/AltanEsmer/Orchestra/issues/7) | Blocked | Tooling verified on artificial fixtures. Requires actual M3 evidence. After M3: complete calibration and validation error analysis; freeze selected systems and any fallback threshold, then evaluate the sealed test. Save confidence and error evidence. |
| M5 | November 22 | Report draft | [#8](https://github.com/AltanEsmer/Orchestra/issues/8) | Blocked | IEEE template compiles and figure export works; actual results and Altan’s own writing remain. After M4: write a 5–12 page IEEE two-column draft with traceable figures, methods, results, and limitations in Altan's own words. |
| M6 | November 29 | Clean reproduction and oral rehearsal | [#9](https://github.com/AltanEsmer/Orchestra/issues/9) | Blocked | Artificial archive restored and reproduced in a clean environment; research archive and oral responses remain. After M5: reproduce the study from a clean environment and archive; record a rehearsal using actual queries, predictions, and figures. Carry knowledge gaps forward. |
| M7 | December 4 | Submission freeze | [#10](https://github.com/AltanEsmer/Orchestra/issues/10) | Not started | After M6: verify final report, citations, code, archive checksum, submission instructions, and remaining high-priority knowledge gaps. |
| M8 | December 6 | Submission | [#11](https://github.com/AltanEsmer/Orchestra/issues/11) | Not started | After M7: submit report through itslearning and code through the confirmed method. Record receipt or equivalent submission evidence. |

The [first-slice acceptance condition](docs/project-plan.md#first-vertical-slice) defines M2 in more detail. Dataset sizes are collection targets, not observed counts. Optional embeddings and tool integration are outside the required milestone path.

Every milestone also requires its updated [study PDF](docs/study-guides/README.md), with source and verification evidence, and a recorded learning attempt connecting course concepts to the project. A delivered guide and an actual student response are separate evidence. Unresolved learning gaps remain visible. After M8, continue oral preparation through January 2027 using the frozen study and newly relevant lectures; this is Altan's target, not a verified exam date.

## Milestones in plain language

| Milestone | What you do | Objective by the end |
| --- | --- | --- |
| M0 — Get ready | Check the setup and use the study guide to explain what the project does and how the preparation works. | A working starting repository, a verified course-linked PDF, and a recorded learning checkpoint with any gaps visible. |
| M1 — Prepare examples | Write questions and review the first action each one needs. | A clear labeling guide and 120 accepted, traceable examples ready for the first baseline. |
| M2 — Build the first classifier | Train a simple question classifier and compare it with a model that always guesses the most common class. | Both baselines run twice with the same splits and predictions, and their validation results are saved. |
| M3 — Compare approaches | Try different ways to represent questions and different classifiers on the same data. | A frozen dataset targeting 400 examples, all 14 required experiment outcomes, and choices justified by validation results. |
| M4 — Check trust and mistakes | Study confidence and errors, freeze the choices, then evaluate unseen test examples. | Honest evidence of final performance, when confidence is useful, and which mistakes remain. |
| M5 — Explain the study | Write the methods, results, and limitations in your own words. | A complete 5–12 page IEEE two-column draft whose figures and conclusions link to saved evidence. |
| M6 — Rerun and rehearse | Reproduce the study from a clean environment and practice explaining it with real examples. | A verified reproduction, an archived study, and a rehearsal record showing remaining knowledge gaps. |
| M7 — Make it ready to hand in | Check the final report, citations, code, archive, and submission steps. | A verified final package with a recorded version/checksum and remaining learning gaps. |
| M8 — Hand it in | Submit the report and code through the confirmed channels. | Recorded receipts or equivalent proof identifying exactly what was submitted. |

For example, “What is 18 percent of 250?” needs `calculation` as its first action. M1 records that label, M2 learns to predict it, M3 compares approaches, and M4 checks predictions and confidence on unseen examples. M5–M8 explain, reproduce, finalize, and submit the study. The entire command flow is tested with artificial data; accepted research data is still absent.

## Preparation checklist

- [x] Verify project 13 and report requirements against the supplied course PDFs.
- [x] Add and verify the locked Python environment and smoke check.
- [x] Document scope, label rules, data collection, splits, experiments, and confidence analysis.
- [x] Add the repository walkthrough, agent instructions, and honest learning record.
- [x] Add the architecture overview and this progress tracker.
- [x] Complete PR review and integration through PR #2 and merge commit `08cce7b`.
- [ ] Complete the introductory learning checkpoint; the first response requested clarification. M0 closed on October 16 without a recorded response, so this item carries into M1.
- [x] Save the approved milestone-PDF plan and remove course confirmation as an agent gate.
- [x] Deliver and verify the M0 lesson and technical appendix in the chosen study folder; see the [edition evidence](docs/study-guides/README.md#edition-evidence).

## Next actions and open decisions

Altan owns course administration, annotation decisions, and the report. Agent work proceeds within his approved scope. Implementation of the [M1 to M3 delivery units](docs/m1-m3-plan.md#deliver-the-work-in-five-units) was approved on October 16 and the tooling is built; the remaining gates are human data evidence. Use the plan's local data paths instead of the draft guide's unignored pilot path.

| Action or decision | Owner | Evidence needed |
| --- | --- | --- |
| Answer the carried-forward M0 checkpoint questions. | Altan | An actual response recorded in the learning log. |
| Refresh study guides as each milestone develops. | Agent and Altan | Current PDF, inspected lecture sources, report evidence, and recorded oral-practice feedback. |
| Introduce routing with one everyday query before further practice. | Agent and Altan | Altan's actual response in the learning log. |
| Retain permission and source-specific notices. | Agent | Altan's exact permission is recorded for q0001–q0040. Public-source licenses remain separate and must be included before adoption. |
| Run the M1 readiness check on the accepted 120 rows and review ledger. | Altan, then agent | `scripts/validate_dataset.py <rows> --review <ledger> --ready` printing PASS, saved in `docs/evidence/m1-data.md`. |
| Expand the reviewed pilot using compatible public sources under guide v2. | Agent, with Altan’s genuine annotation decisions | Pilot review is complete: 38 accepted rows/23 groups, two practice-only exclusions. Apply the v2 batch checks for near-duplicates, request-type spread, and source mix. Reach the M1 row and group targets before a release. |
| Apply guide-v1 boundaries to new candidates. | Agent and Altan | Pilot boundaries are resolved. Record genuine decisions for any new flagged cases; preserve original labels and full queries locally. |
| Retain actual review evidence during expansion. | Agent and Altan | Pilot adjudications are complete. New AI checks require actual provenance and genuine human decisions when flagged; never pool AI consistency with human agreement. |

## Evidence ledger

| Date | Delivered evidence | What it establishes |
| --- | --- | --- |
| October 7, 2026 | [`7e37f68`](https://github.com/AltanEsmer/Orchestra/commit/7e37f68) | Locked environment and executable smoke assertions. |
| October 7, 2026 | [`c3fef0e`](https://github.com/AltanEsmer/Orchestra/commit/c3fef0e) and [preparation checks](docs/learning-log.md#preparation-evidence-october-7-2026) | Course-grounded plan, evaluation protocol, walkthrough, learning record, and passing preparation checks. |
| October 7, 2026 | [PR #2](https://github.com/AltanEsmer/Orchestra/pull/2) and [tracking update](docs/learning-log.md#architecture-and-roadmap-october-7-2026) | Architecture and milestone tracking added to the preparation branch. |
| October 7, 2026 | [`08cce7b`](https://github.com/AltanEsmer/Orchestra/commit/08cce7b) | PR #2 reviewed and merged; issue #1 closed. Learning and course-rule gates remain open. |
| October 8, 2026 | [Milestone issues #3–#11](https://github.com/AltanEsmer/Orchestra/issues?q=is%3Aissue+%22%5BM%22) and [tracking update](docs/learning-log.md#milestone-issues-and-roadmap-rename-october-8-2026) | One issue per milestone, with objectives, dependencies, and completion criteria; roadmap renamed to `ROADMAP.md` and local references updated. No research milestone is claimed complete. |
| October 8, 2026 | [M0 delivery plan](docs/m0-plan.md) and [study-guide edition](docs/study-guides/README.md#edition-evidence) | Course confirmation removed by Altan; M0 PDF delivered with code and lecture connections; M0-M8 issue learning checkpoints updated. Actual learning response remains pending. |
| October 16, 2026 | Issue #3 closed by Altan; dated snapshot `M0-preparation-2026-10-16.pdf` (SHA-256 `3c321a3b…1ce07`, identical to the October 8 edition) | M0 closed by owner decision. The learning checkpoint was not answered and carries into M1. |
| October 16, 2026 | Branch `claude/m1-annotation-start`: annotation guide v0, source manifest, and dataset validator with unit tests | M1 tooling ready for the pilot. No query rows exist yet. |
| October 16, 2026 | [PR #14](https://github.com/AltanEsmer/Orchestra/pull/14), merged as `48abda0` | M1 preparation integrated into main. Data collection and acceptance remain unfinished. |
| October 16, 2026 | [M1 to M3 plan](docs/m1-m3-plan.md), [methods preview](docs/study-guides/m1-m3-methods-preview.md), and [planning evidence](docs/evidence/m1-m3-planning.md) | Proposed implementation, data-growth safeguards, study-document workflow, and CPU/GPU resource decisions. No implementation approval, new research data, or experiment result is implied. |
| October 16, 2026 | Branch `claude/m1-m3-implementation` (`c48d60e` to the lead docs commit) and [tooling log](docs/learning-log.md#m1-to-m3-tooling-october-16-2026) | P1 to P5 tooling with 148 passing tests and fixture-only evidence. No research data, split, run, or metric. M1 to M3 remain open. |
| October 23, 2026 | Forty actual pilot responses and scoped permission recorded in [learning log](docs/learning-log.md) and source manifest | Authorship and permission evidence; review and acceptance remain unfinished. |
| October 24, 2026 | [BFCL](docs/evidence/bfcl-compatibility.md), [No Robots](docs/evidence/public-direct-answer.md), [Dolly](docs/evidence/public-document-retrieval.md), and [blind AI check](docs/evidence/pilot-ai-review.md) | Complementary-source compatibility and AI consistency evidence; no human-review substitution or research result. |
| October 24, 2026 | Altan chose single-human annotation with disclosed AI checks | Method change supersedes the earlier pending choice. Dedicated AI evidence and actual human adjudications are required; AI agreement is never reported as independent human review. |
| October 26, 2026 | [Guide v2](docs/evidence/guide-v2.md) | Scenario/source grouping and batch quality checks replace request-template groups; 38 pilot rows regrouped into 23 groups, labels unchanged. |
| October 26, 2026 | [Guide-v1 pilot acceptance](docs/evidence/pilot-guide-v1.md) and actual human decisions | 38 accepted pilot rows across 19 shared request templates; two practice-only exclusions. No remaining pilot group questions; M1 coverage and source adoption remain open. |

## Maintaining progress

When work starts, change its status to “in progress.” When review is required, use “in review” until review finishes. Mark a milestone “done” only after linking its completion evidence: a commit, accepted dataset manifest, saved run, reviewed report, or submission receipt.

Update the date and evidence ledger with each milestone change, and reconcile the linked issue's checklists and open/closed state with that evidence. Creating an issue does not complete its milestone. For a blocker, record its cause, owner, and next action. If a target date changes, record why. Keep milestone dates and statuses here instead of duplicating them in other documents. Learning statuses change only from Altan's actual responses in the learning log.

Course-rule confirmation is no longer a milestone gate. Earlier ledger entries describe the requirements at the time; the October 8 accepted plan supersedes that administrative requirement.
