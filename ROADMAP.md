# Roadmap

Last updated: October 8, 2026. This is the primary progress tracker for course project 13. Preparation was delivered through [issue #1](https://github.com/AltanEsmer/Orchestra/issues/1); the milestone issues below track the remaining work. The [project plan](docs/project-plan.md) owns scope and decision rationale; [architecture](architecture.md) owns component responsibilities. The [learning log](docs/learning-log.md) tracks understanding separately.

## Current position

Preparation was reviewed and merged in [PR #2](https://github.com/AltanEsmer/Orchestra/pull/2) on October 7, 2026, as [`08cce7b`](https://github.com/AltanEsmer/Orchestra/commit/08cce7b). Issue #1 is closed. The locked environment and smoke check have passed. M0 remains open for the learning checkpoint and course-rule confirmation. No research dataset, trained router, experimental metric, or submitted report exists yet.

Statuses mean **not started**, **in progress**, **in review**, **done**, or **blocked**. “Done” requires the stated completion evidence. A blocked item records what must change and who can resolve it. Dates are targets, not evidence of completion.

## Milestones

Dates use Europe/Copenhagen. December 6 is the course submission date; earlier dates are project targets. The portal cutoff time still needs confirmation.

| ID | Target date | Milestone | Issue | Status | Completion evidence or remaining gate |
| --- | --- | --- | --- | --- | --- |
| M0 | October 11, 2026 | Preparation and course-rule confirmation | [#3](https://github.com/AltanEsmer/Orchestra/issues/3) | In progress | Environment and planning reviewed and merged in PR #2. Learning checkpoint and staff confirmation remain open. |
| M1 | October 18 | Annotation pilot and first dataset | [#4](https://github.com/AltanEsmer/Orchestra/issues/4) | Not started | After M0: review 40 pilot queries, freeze guide v1, and accept 120 rows with provenance and group IDs. Record disagreements and exclusions. |
| M2 | October 25 | First reproducible baseline | [#5](https://github.com/AltanEsmer/Orchestra/issues/5) | Not started | After M1: validate rows and splits; run dummy and TF-IDF logistic regression twice with identical split membership and predictions. Save validation metrics and provenance. |
| M3 | November 8 | Main classifier and representation comparison | [#6](https://github.com/AltanEsmer/Orchestra/issues/6) | Not started | After M2: freeze the main dataset, target 400 accepted queries, and complete the 14 required configurations. Save all outcomes and validation selections. |
| M4 | November 15 | Confidence, errors, and final test | [#7](https://github.com/AltanEsmer/Orchestra/issues/7) | Not started | After M3: complete calibration and validation error analysis; freeze selected systems and any fallback threshold, then evaluate the sealed test. Save confidence and error evidence. |
| M5 | November 22 | Report draft | [#8](https://github.com/AltanEsmer/Orchestra/issues/8) | Not started | After M4: write a 5–12 page IEEE two-column draft with traceable figures, methods, results, and limitations in Altan's own words. |
| M6 | November 29 | Clean reproduction and oral rehearsal | [#9](https://github.com/AltanEsmer/Orchestra/issues/9) | Not started | After M5: reproduce the study from a clean environment and archive; record a rehearsal using actual queries, predictions, and figures. Carry knowledge gaps forward. |
| M7 | December 4 | Submission freeze | [#10](https://github.com/AltanEsmer/Orchestra/issues/10) | Not started | After M6: verify final report, citations, code, archive checksum, submission instructions, and remaining high-priority knowledge gaps. |
| M8 | December 6 | Submission | [#11](https://github.com/AltanEsmer/Orchestra/issues/11) | Not started | After M7: submit report through itslearning and code through the confirmed method. Record receipt or equivalent submission evidence. |

The [first-slice acceptance condition](docs/project-plan.md#first-vertical-slice) defines M2 in more detail. Dataset sizes are collection targets, not observed counts. Optional embeddings and tool integration are outside the required milestone path.

## Milestones in plain language

| Milestone | What you do | Objective by the end |
| --- | --- | --- |
| M0 — Get ready | Check the setup, understand what the project does, and confirm the course rules. | A working starting repository, confirmed rules, and a recorded learning checkpoint with any gaps visible. |
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
- [ ] Complete the introductory learning checkpoint; the first response requested clarification.
- [ ] Confirm AI-use rules, disclosure requirements, oral-exam format, code submission, and portal cutoff with course staff.

## Next actions and open decisions

Altan owns course confirmation, annotation decisions, and the report. Implementation can be agent-assisted under the confirmed course rules. New implementation work starts with the [ordered first-session checklist](docs/project-plan.md#first-work-session-after-preparation).

| Action or decision | Owner | Evidence needed |
| --- | --- | --- |
| Complete the remaining M0 gates in issue #3. | Altan | Dated course-rule confirmation and an actual introductory learning response; PR #2 is already merged. |
| Confirm course rules and submission details. | Altan, with course staff | Dated staff response or official announcement in the course-source record. |
| Introduce routing with one everyday query before further practice. | Agent and Altan | Altan's actual response in the learning log. |
| Start the 40-query annotation pilot. | Altan | Versioned rows, provenance, rationales, and reviewed boundary cases. |
| Arrange a second human annotation review or document the delayed self-review alternative. | Altan | Recorded review method and disagreements before guide freeze. |

## Evidence ledger

| Date | Delivered evidence | What it establishes |
| --- | --- | --- |
| October 7, 2026 | [`7e37f68`](https://github.com/AltanEsmer/Orchestra/commit/7e37f68) | Locked environment and executable smoke assertions. |
| October 7, 2026 | [`c3fef0e`](https://github.com/AltanEsmer/Orchestra/commit/c3fef0e) and [preparation checks](docs/learning-log.md#preparation-evidence-october-7-2026) | Course-grounded plan, evaluation protocol, walkthrough, learning record, and passing preparation checks. |
| October 7, 2026 | [PR #2](https://github.com/AltanEsmer/Orchestra/pull/2) and [tracking update](docs/learning-log.md#architecture-and-roadmap-october-7-2026) | Architecture and milestone tracking added to the preparation branch. |
| October 7, 2026 | [`08cce7b`](https://github.com/AltanEsmer/Orchestra/commit/08cce7b) | PR #2 reviewed and merged; issue #1 closed. Learning and course-rule gates remain open. |
| October 8, 2026 | [Milestone issues #3–#11](https://github.com/AltanEsmer/Orchestra/issues?q=is%3Aissue+%22%5BM%22) and [tracking update](docs/learning-log.md#milestone-issues-and-roadmap-rename-october-8-2026) | One issue per milestone, with objectives, dependencies, and completion criteria; roadmap renamed to `ROADMAP.md` and local references updated. No research milestone is claimed complete. |

## Maintaining progress

When work starts, change its status to “in progress.” When review is required, use “in review” until review finishes. Mark a milestone “done” only after linking its completion evidence: a commit, accepted dataset manifest, saved run, reviewed report, or submission receipt.

Update the date and evidence ledger with each milestone change, and reconcile the linked issue's checklists and open/closed state with that evidence. Creating an issue does not complete its milestone. For a blocker, record its cause, owner, and next action. If a target date changes, record why. Keep milestone dates and statuses here instead of duplicating them in other documents. Learning statuses change only from Altan's actual responses in the learning log.
