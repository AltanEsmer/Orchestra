# Collection brief for the main comparison

First prepared October 22, 2026. Revised October 26, 2026 after the M1 freeze, before any split or research model errors exist. `prepare-study` records this file's hash before the M2 split. Freeze that copy for the expansion; document later changes before collecting affected rows.
## What M3 adds

The frozen M1 release (`data/processed/m1-v1.jsonl`, 128 rows, 108 groups) keeps its text, labels, group IDs, and split memberships. M3 targets 400 accepted rows, roughly 100 per class. This is a collection target, not a result. If fewer rows are feasible, keep the held-out test and report the shortfall and its uncertainty instead of inventing data. `extend` adds only new, independent groups, at least five per class, and refuses a new row in an existing group.

## Sources

Collect from these sources only. Each needs a `data/manifests/sources.json` entry with license and pinned revision before its rows are imported.

| Source | License | Router input |
| --- | --- | --- |
| Altan-authored | Altan's recorded permission | Query text |
| AI drafts (supplement below) | Generated locally; disclosed | Query text |
| Dolly 15k | CC BY-SA 3.0 | Instruction only; any passage stays a linked attachment outside router input (the approved adapter) |
| BFCL v3 | Apache-2.0 | User text only; no function docs, expected calls, or system messages |
| No Robots | CC BY-NC 4.0 | Prompt text only; in passage categories, the passage is split off as a linked attachment, as for Dolly |
| GSM8K | MIT, confirmed October 26 at revision `740312ad` | Question text only; no worked solution or answer |

On October 26, 2026, Altan chose the recommended per-class mix: "Go with the recommended mix without screening first and update the brief." Each class keeps its M1 public source as the main source and adds a second one so that no source exceeds 75 percent:

| Class | Main source | Second source |
| --- | --- | --- |
| Direct answer | No Robots | Dolly categories without a passage (open QA, brainstorming, creative writing) |
| Document retrieval | Dolly | No Robots passage categories (summarize, extract, closed QA), with the attachment adapter |
| Calculation | BFCL | GSM8K word problems |
| Knowledge lookup | BFCL, remaining read-only lookups | Altan-authored queries and the pending AI drafts |

This choice also extends the attachment adapter to No Robots and selects GSM8K as a new source. GSM8K is adopted once its license and pinned revision are recorded in the source manifest. Both were recorded on October 26 (MIT, from the dataset card and OpenAI's repository LICENSE); no GSM8K file has been downloaded. Capacity was not screened before this choice. If a source cannot fill its share, the agent reports the shortfall and Altan decides the top-up. The agent does not switch sources on its own. Text-to-SQL corpora were not chosen for lookup because their questions usually do not name the database, which the guide marks as missing context. This reason has not been checked by a screen.

Keep public text as written. Do not rewrite it to fit a label; skip it instead. Adding any other public corpus requires Altan's adoption and a recorded change to this brief before its rows are collected. Public rows are not covered by the repository's MIT license, and their attribution must travel with the data.

## Labels, groups, and batch checks

Label by first action under the [annotation guide](annotation-guide.md). Its label boundaries are unchanged from v1. A stable fact without a named source is a direct answer. A record ID implies a structured source. Exclude requests that need live or external information that no tool provides.

Group under guide v2. Rows share a group when they share a small variation, a source or named setting, a specific situation, or one public record. A shared request type alone does not join rows. Compare candidates against existing M1 groups before allocating. A related variant joins its existing group, so it cannot be added in M3; move it to the practice collection with its reason. Keep at most four rows per group.

Every batch passes the guide's checks before acceptance:

- No exact duplicates, and a hand check of pairs that reach 0.5 token overlap across groups.
- No request type above 40 percent of a class.
- At least two sources per class, and no source above 75 percent of a class.

These checks apply to the cumulative M3 dataset, not only to the new rows.

Include varied request styles and wording lengths. M1 class medians run from 14 to 19 words. Cover direct instructions, questions, negation, retrieval-before-calculation dependencies, and the documented action boundaries. Include at least two independently sourced scenarios for each boundary.

## Review

Use the same AI-assisted method as M1:

- Altan records the primary label and rationale for every new row.
- A blind AI check reviews every new row, seeing only the guide, the query text, and whether a passage is attached.
- Clear, unflagged agreements are accepted. Every flag, ambiguous judgment, or disagreement needs Altan's adjudication.

Disclose that AI consistency is not human agreement. Disclose too that approving agent proposals carries an anchoring risk. Record exclusions and unresolved boundaries.

## What not to do

Do not collect, select, or relabel new rows to target mistakes seen in M2 validation errors. Sealing the test files restricts model access only. It cannot undo human exposure during collection, which must be disclosed. Do not change M1 rows or groups; any change needs a new release name.

## Known cues to inspect

These are measured associations in the frozen M1 release. They do not show that a classifier relies on them.

| Cue | Rows containing it |
| --- | --- |
| "fictional" | 19 of 63 retrieval and lookup rows; no others |
| "table" | 14 of 32 lookups; 1 retrieval |
| "database" | 8 of 32 lookups; no others |
| "calculate" | 15 of 32 calculations; 1 lookup |
| "paragraph" or "reference text" | 10 retrieval; 2 direct answer |
| "handbook" | 4 retrieval; no others |

New rows should dilute these associations rather than add to them. Inspect them during validation error analysis. The October 26 pilot decision still applies: checklist transformation stays separate from summarization.

After collection, the agent measures class and group counts, word lengths, source mix, request-type spread, agreement, and exclusions. These observations establish the coverage actually achieved. This brief cannot guarantee natural user language or real-world routing performance.

## Size target

On October 26, 2026, Altan said: "Keep 400 rows (about 100 per class) as the M3 target." It is set before collection so the size cannot be chosen after seeing M2 results. At 100 rows per class, the 75 percent limit allows at most 75 rows from the main source. M1 already has 9–10 Altan-authored rows per class, so each class needs about 15 more from its second source. Lookup is tightest because the [expansion screen](evidence/public-expansion-screen.md) found few read-only BFCL lookups.

## AI candidate drafting supplement, October 26, 2026

Altan asked to "Draft AI-generated candidates" after being offered human authoring or disclosed AI drafting. This allows a local draft supplement. Generated text is not attributed to Altan. Permission, human primary labels and rationales, the AI check, and adjudication still apply before acceptance.

The [template review](evidence/template-expansion-draft.md) records 40 local drafts, two per supplied template. They used v1 family accounting. Under v2, each draft gets a group from its own scenario or source, and drafts that share a named setting share a group. They are proposals, not accepted rows. Keep generation provenance, the request, guide snapshots, and query-only input outside Git. The exact backend revision and generation parameters are unavailable and must not be invented.

Drafted source names are fictional, without requiring the word "fictional" in every query. Vary structured-source and document nouns while keeping enough information to choose an action. Do not target model errors.
