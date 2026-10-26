# Template expansion draft, October 26, 2026

Altan supplied twenty template proposals and then explicitly selected “Draft AI-generated candidates.” The agent wrote two drafts per template. All 40 remain `needs_review`, with proposed first-action labels and families only. They are stored in ignored `data/raw/template-expansion-ai-2026-10-26/`, not imported into the study schema or attributed to A1. The accepted pilot and label ledger are unchanged. No model, split, source adoption, or human annotation occurred.

## Proposed boundaries

Apply goal, procedure, and output across labels, not merely the number or order of tools. These are conservative agent proposals for human review, not new frozen-guide decisions.

| Templates | Proposed family | Reason |
| --- | --- | --- |
| L1, L2, D9 | g003 | Return a keyed field or event attribute. Joining records, using history, or reading the key first does not by itself change that goal. A broader historical-trend task would need separate assessment. |
| L3 | New category counts | Partition records and count each category rather than return one filtered set/count. |
| L4 | New distinct values | Enumerate a field’s unique values, without per-category counts. |
| L5 | g015 | Compare corresponding facts across two sources, as in the existing timetable/letter comparison. |
| L6 | New free interval | Derive an unoccupied interval of a specified duration within a given window. |
| L7 | New duplicate records | Compare record pairs against explicit identity criteria. |
| L8 | g012 | Lookup precedes the existing difference-calculation goal. |
| L9, D10 | g032 | Draft social messages from source facts; source access changes the first action. |
| L10, D1, D7 | g008 | Answer a specific document question, including location; resolving a source pointer does not establish a separate goal. |
| D2 | New internal contradictions | Search one document for incompatible assertions, instead of comparing specified facts in two sources. Revisit this boundary with g015 during human review. |
| D3 | New document completeness | Check every supplied requirement and report evidence or an omission. |
| D4 | New document quiz | Create assessment questions with supported answers. |
| D5 | g002 | A descriptive headline compresses the document’s main content. |
| D6 | New document structure | Preserve the heading hierarchy rather than select key content. |
| D8 | New document classification | Assign the document to one of an explicit set of categories. |

For the four flagged proposals: retain L3, D3, and D6 provisionally; merge D1 into g008. Other overlaps matter too. This yields nine proposed new families (four lookup, five document), not twenty. An existing family may gain a new label, but it still shares its four-row cap across labels. Public aggregate, threshold, extraction, and read-then-calculate proposals also need comparison against the actual pilot templates before group totals can be claimed. The submitted 16/17 group projection is therefore not established.

## Cap accounting

| Family | Accepted pilot | Draft additions | Combined |
| --- | ---: | ---: | ---: |
| g003 | 4 | 6 | 10 |
| g008 | 3 | 6 | 9 |
| g032 | 1 | 4 | 5 |
| g012 | 2 | 2 | 4 |
| g015 | 2 | 2 | 4 |
| g002 | 2 | 2 | 4 |
| Each of nine new proposed families | 0 | 2 | 2 |

Under these proposals, at most 28 of the 40 drafts fit the remaining slots: none of six g003 drafts, one of six g008 drafts, three of four g032 drafts, and all other drafts. This is a capacity ceiling, not acceptance or a selection decision. Preserve every candidate and its actual family relationship; do not invent independent IDs to bypass the cap. Human adjudication and sampling decisions are pending.

## Provenance and checks

The local bundle contains the supplied request, generation-context snapshots, `candidates.md`, `candidates.jsonl`, `query-only.jsonl`, `cap-report.json`, and `provenance.json`. IDs such as L1-1 are draft IDs, not permanent research IDs. The provenance identifies OpenAI/Codex and the available GPT-6 session identity; exact backend revision and parameters are not exposed. The full conversation is not exported, so prompt reconstruction is incomplete. Human edits at generation: none. Human annotation and permission for eventual research use remain pending.

All names and sources are invented; no linked real document was retrieved or fabricated as evidence. The drafts deliberately make dependencies explicit and vary source nouns. They omit the word “fictional” from the query itself while declaring fictional scope in the worksheet. Pilot inspection found that word in 10/10 lookup and 9/9 document rows, and 0/9 calculation and 0/10 direct-answer rows. This association is real; no model has been tested for reliance on it.

Structural checks cover forty unique texts and IDs, two per template, twenty proposed rows per label, no exact overlap with the pilot, query-only alignment, provenance hashes, and the combined family caps. They cannot establish semantic independence or correct labels. No fresh blind AI review was performed: the drafting agent already saw its proposed labels. Query-only input is prepared for a later review after human primary annotation. See the learning log for actual software-check results.
