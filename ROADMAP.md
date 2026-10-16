# Roadmap

Last updated: October 16, 2026. This is the primary progress tracker for course project 13. Preparation was delivered through [issue #1](https://github.com/AltanEsmer/Orchestra/issues/1); the milestone issues below track the remaining work. The [project plan](docs/project-plan.md) owns scope and decision rationale; [architecture](architecture.md) owns component responsibilities. The [learning log](docs/learning-log.md) tracks understanding separately.

## Current position

Preparation was reviewed and merged in [PR #2](https://github.com/AltanEsmer/Orchestra/pull/2) on October 7, 2026, as [`08cce7b`](https://github.com/AltanEsmer/Orchestra/commit/08cce7b). Issue #1 is closed. The locked environment and smoke check have passed. M0 now delivers a course-linked study PDF and an introductory learning checkpoint under the [accepted plan](docs/m0-plan.md). Altan removed course confirmation as a gate on October 8. On October 16 Altan closed issue #3, so M0 is closed by his decision. The introductory learning response was never recorded; it moves into M1 as an open learning gap rather than counting as answered. M1 has started with agent-side tooling: a draft annotation guide, a provenance manifest, and a row validator. Query writing and annotation decisions belong to Altan and have not started. No research dataset, trained router, experimental metric, or submitted report exists yet.

Statuses mean **not started**, **in progress**, **in review**, **done**, or **blocked**. “Done” requires the stated completion evidence. A blocked item records what must change and who can resolve it. Dates are targets, not evidence of completion.

The October 16 [M1 to M3 plan](docs/m1-m3-plan.md) is a documentation-only delivery, accompanied by an [exam, presentation, and report methods preview](docs/study-guides/m1-m3-methods-preview.md). Altan authorized creating and merging the planning PR, then stopping for implementation approval. That approval is pending. Milestone statuses and human-review requirements remain unchanged.

## Milestones

Dates use Europe/Copenhagen. December 6 is the course submission date; earlier dates are project targets. Altan handles submission timing and course administration.

| ID | Target date | Milestone | Issue | Status | Completion evidence or remaining gate |
| --- | --- | --- | --- | --- | --- |
| M0 | October 11, 2026 | Preparation and course-linked study guide | [#3](https://github.com/AltanEsmer/Orchestra/issues/3) | Done | Closed by Altan on October 16. Environment and planning merged in PR #2; M0 PDF delivered, checked, and snapshotted. Exception: no learning response was recorded, so the checkpoint carries into M1 unanswered. |
| M1 | October 18 | Annotation pilot and first dataset | [#4](https://github.com/AltanEsmer/Orchestra/issues/4) | In progress | After M0: review 40 pilot queries, freeze guide v1, and accept 120 rows with provenance and group IDs. Record disagreements and exclusions. |
| M2 | October 25 | First reproducible baseline | [#5](https://github.com/AltanEsmer/Orchestra/issues/5) | Not started | After M1: validate rows and splits; run dummy and TF-IDF logistic regression twice with identical split membership and predictions. Save validation metrics and provenance. |
| M3 | November 8 | Main classifier and representation comparison | [#6](https://github.com/AltanEsmer/Orchestra/issues/6) | Not started | After M2: freeze the main dataset, target 400 accepted queries, and complete the 14 required configurations. Save all outcomes and validation selections. |
| M4 | November 15 | Confidence, errors, and final test | [#7](https://github.com/AltanEsmer/Orchestra/issues/7) | Not started | After M3: complete calibration and validation error analysis; freeze selected systems and any fallback threshold, then evaluate the sealed test. Save confidence and error evidence. |
| M5 | November 22 | Report draft | [#8](https://github.com/AltanEsmer/Orchestra/issues/8) | Not started | After M4: write a 5–12 page IEEE two-column draft with traceable figures, methods, results, and limitations in Altan's own words. |
| M6 | November 29 | Clean reproduction and oral rehearsal | [#9](https://github.com/AltanEsmer/Orchestra/issues/9) | Not started | After M5: reproduce the study from a clean environment and archive; record a rehearsal using actual queries, predictions, and figures. Carry knowledge gaps forward. |
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

For example, “What is 18 percent of 250?” needs `calculation` as its first action. M1 records that label, M2 learns to predict it, M3 compares approaches, and M4 checks predictions and confidence on unseen examples. M5–M8 explain, reproduce, finalize, and submit the study. Today's smoke script still uses toy labels; this research flow is planned.

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

Altan owns course administration, annotation decisions, and the report. Agent work proceeds within his approved scope. After separate implementation approval, follow the [M1 to M3 delivery units](docs/m1-m3-plan.md#deliver-the-work-in-five-units). Use the plan's local data paths instead of the draft guide's unignored pilot path.

| Action or decision | Owner | Evidence needed |
| --- | --- | --- |
| Answer the carried-forward M0 checkpoint questions. | Altan | An actual response recorded in the learning log. |
| Refresh study guides as each milestone develops. | Agent and Altan | Current PDF, inspected lecture sources, report evidence, and recorded oral-practice feedback. |
| Introduce routing with one everyday query before further practice. | Agent and Altan | Altan's actual response in the learning log. |
| Approve implementation after the planning PR merges. | Altan | Explicit subsequent approval recorded in the learning log. |
| Write and review the 40-query pilot using the [annotation guide](docs/annotation-guide.md). | Altan, with disclosed agent candidate assistance if used | Local `data/raw/pilot-v0.jsonl` passing the validator, with actual human rationales and reviewed boundary cases. No rows exist yet. |
| Decide the open guide questions: general-knowledge facts, review method, data license, and tracking of rows. | Altan | Decisions recorded in the annotation guide before v1. |
| Arrange a second human annotation review or document the delayed self-review alternative. | Altan | Recorded review method and disagreements before guide freeze. |

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

## Maintaining progress

When work starts, change its status to “in progress.” When review is required, use “in review” until review finishes. Mark a milestone “done” only after linking its completion evidence: a commit, accepted dataset manifest, saved run, reviewed report, or submission receipt.

Update the date and evidence ledger with each milestone change, and reconcile the linked issue's checklists and open/closed state with that evidence. Creating an issue does not complete its milestone. For a blocker, record its cause, owner, and next action. If a target date changes, record why. Keep milestone dates and statuses here instead of duplicating them in other documents. Learning statuses change only from Altan's actual responses in the learning log.

Course-rule confirmation is no longer a milestone gate. Earlier ledger entries describe the requirements at the time; the October 8 accepted plan supersedes that administrative requirement.
