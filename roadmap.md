# Roadmap

Last updated: October 7, 2026. This is the primary progress tracker for course project 13 and [issue #1](https://github.com/AltanEsmer/Orchestra/issues/1). The [project plan](docs/project-plan.md) owns scope and decision rationale; [architecture](architecture.md) owns component responsibilities. The [learning log](docs/learning-log.md) tracks understanding separately.

## Current position

Preparation is implemented in [PR #2](https://github.com/AltanEsmer/Orchestra/pull/2), which is open for review. The locked environment and smoke check have passed. No research dataset, trained router, experimental metric, or submitted report exists yet.

Statuses mean **not started**, **in progress**, **in review**, **done**, or **blocked**. “Done” requires the stated completion evidence. A blocked item records what must change and who can resolve it. Dates are targets, not evidence of completion.

## Milestones

Dates use Europe/Copenhagen. December 6 is the course submission date; earlier dates are project targets. The portal cutoff time still needs confirmation.

| ID | Target date | Milestone | Status | Completion evidence or remaining gate |
| --- | --- | --- | --- | --- |
| M0 | October 11, 2026 | Preparation and course-rule confirmation | In review | Environment and planning delivered in PR #2. Review, learning checkpoint, and staff confirmation remain open. |
| M1 | October 18 | Annotation pilot and first dataset | Not started | After M0: review 40 pilot queries, freeze guide v1, and accept 120 rows with provenance and group IDs. Record disagreements and exclusions. |
| M2 | October 25 | First reproducible baseline | Not started | After M1: validate rows and splits; run dummy and TF-IDF logistic regression twice with identical split membership and predictions. Save validation metrics and provenance. |
| M3 | November 8 | Main classifier and representation comparison | Not started | After M2: freeze the main dataset, target 400 accepted queries, and complete the 14 required configurations. Save all outcomes and validation selections. |
| M4 | November 15 | Confidence, errors, and final test | Not started | After M3: complete calibration and validation error analysis; freeze selected systems and any fallback threshold, then evaluate the sealed test. Save confidence and error evidence. |
| M5 | November 22 | Report draft | Not started | After M4: write a 5–12 page IEEE two-column draft with traceable figures, methods, results, and limitations in Altan's own words. |
| M6 | November 29 | Clean reproduction and oral rehearsal | Not started | After M5: reproduce the study from a clean environment and archive; record a rehearsal using actual queries, predictions, and figures. Carry knowledge gaps forward. |
| M7 | December 4 | Submission freeze | Not started | After M6: verify final report, citations, code, archive checksum, submission instructions, and remaining high-priority knowledge gaps. |
| M8 | December 6 | Submission | Not started | After M7: submit report through itslearning and code through the confirmed method. Record receipt or equivalent submission evidence. |

The [first-slice acceptance condition](docs/project-plan.md#first-vertical-slice) defines M2 in more detail. Dataset sizes are collection targets, not observed counts. Optional embeddings and tool integration are outside the required milestone path.

## Preparation checklist

- [x] Verify project 13 and report requirements against the supplied course PDFs.
- [x] Add and verify the locked Python environment and smoke check.
- [x] Document scope, label rules, data collection, splits, experiments, and confidence analysis.
- [x] Add the repository walkthrough, agent instructions, and honest learning record.
- [x] Add the architecture overview and this progress tracker.
- [ ] Complete PR review and integration.
- [ ] Complete the introductory learning checkpoint; the first response requested clarification.
- [ ] Confirm AI-use rules, disclosure requirements, oral-exam format, code submission, and portal cutoff with course staff.

## Next actions and open decisions

Altan owns course confirmation, annotation decisions, and the report. Implementation can be agent-assisted under the confirmed course rules. New implementation work starts with the [ordered first-session checklist](docs/project-plan.md#first-work-session-after-preparation).

| Action or decision | Owner | Evidence needed |
| --- | --- | --- |
| Review preparation and resolve PR #2. | Altan | Review outcome and integration reference. |
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

## Maintaining progress

When work starts, change its status to “in progress.” When review is required, use “in review” until review finishes. Mark a milestone “done” only after linking its completion evidence: a commit, accepted dataset manifest, saved run, reviewed report, or submission receipt.

Update the date and evidence ledger with each milestone change. For a blocker, record its cause, owner, and next action. If a target date changes, record why. Keep milestone dates and statuses here instead of duplicating them in other documents. Learning statuses change only from Altan's actual responses in the learning log.
