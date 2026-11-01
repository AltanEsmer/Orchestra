# M3.5: groups and quotas

Interim audit edition - October 31, 2026. Accepted data remain 400 rows in 360 groups. The target is at least 2,500 accepted queries, preferably 4,000. This guide records a screening step, not a completed release or model comparison.

## What the audit found

The combined working inventory contains 99 provisional calculation rows in 69 proposed groups and 46 provisional lookup rows in 37 proposed groups. It includes retained earlier candidates and new sources. These groups are hypotheses pending semantic and human review; distinct strings and a clean duplicate check do not prove independent evidence.

The new investigation made 773 formal screening decisions: 462 focused lookup requests, 220 numerical-source records and 91 additional Dolly/No Robots requests. Some overlap earlier records. Math Stack Exchange adds independently posted mathematical questions with per-post attribution and revisions. ToolAlpaca adds public generated tool-use requests. A small published calculation benchmark contributes existing synthetic prompts, with repeated templates grouped. Source adoption and adapters remain unresolved. No new examples were generated or accepted.

## The quota arithmetic

At 2,500 total, the balanced plan needs 625 rows per class, so 525 additional rows per class. At most 250 can have one request type and at most 468 can come from one source. With a four-row group cap, each class needs at least 132 new groups. At 4,000 total, the corresponding figures are 1,000 per class, 900 additional rows, 400 per request type, 750 per source and at least 225 new groups per class.

The existing lookup class already has 40 keyed-record requests. At 625 rows, only 210 more keyed requests fit. Therefore at least 315 new lookup requests must be other types. The integrated inventory contains only 11 of those, leaving 304 still to establish. For 1,000 per class, the remaining non-keyed gap is 529.

The existing calculation class has 16 word problems. At 625 rows, only 234 more fit. At least 291 additional calculations must be other types. The integrated inventory provides 57, leaving 234 still to establish. For 1,000 per class, the remaining non-word-problem gap is 459. These are gaps in measured candidate inventory, not proof that suitable public data do not exist elsewhere.

## Why a larger pending batch can fail

All 46 pending lookup candidates cannot simply be added to the current 100. They include 35 keyed requests, producing 75 keyed rows out of 146, or 51.4%. That exceeds 40%. All 11 non-keyed candidates plus seven keyed ones would give 47 out of 118, or 39.8%, which passes the type arithmetic. This is an illustrative subset, not an accepted batch or a recommendation to stop at 118.

<!-- pagebreak -->

## Grouping needs interpretation

Repeated BMI questions, movie-ID requests and arithmetic templates can create many rows from few scenarios. Exact duplicates collapse; related variants share a group; groups already in the parent release cannot receive new extension rows. The audit keeps every match and reason.

Token overlap is only a flag. Two requests can use the same placeholder number while asking about different things, such as a session and a manager record. The audit rejected that false match. Conversely, a paraphrase may evade a word-overlap threshold. Numerical token sets can also lose operators and over-merge distinct mathematical tasks. The conservative groups remain reviewable; the audit does not silently change guide v2 into grouping all examples by request type.

## Trace a query

Teaching example: "Find the records priced below 500 in the named catalogue." The first action is knowledge lookup. The number is a filter condition; it is not enough to compute the answer without reading the catalogue. The query must identify its source under the current contract. A hidden schema or tool description cannot supply that missing information to the router. This teaching example is not a research row.

## Evidence and limits

The actual parent source/type counts were reconstructed from frozen row IDs and original provenance, not an import report's earlier projection. Parent text was compared computationally without printing it; no model errors or sealed partition file were inspected. The release, review ledger, split, source manifest, old collection brief, annotation guide and dependency files remain unchanged.

The numerical-source investigation stopped counting MATH after finding a documented rights dispute, and excluded MathOdyssey because its author restricts data to testing. Public accessibility alone is not a source-adoption decision. The individual source notes retain primary links, license and revision evidence, excluded leads and generated-origin disclosure.

This follows Lecture 2, Data Preprocessing and Feature Engineering, PDF page 8: inspect sampling and relevance before modeling. The page was extracted and visually checked for this M3.5 work on October 31. Its file hash is e7bfec9a9a52954c038e58a84f680e76648efa582ef79acafe2a3bfaa582217f. The numerical caps and four labels are project choices, not lecture requirements.

## Next work and practice

Continue named-source filters, membership, aggregation and duplicate-record lookup inventory; investigate varied finite probability, geometry and numerical-integration questions. Resolve held source scope and adapters before freezing the new collection brief. Time the existing blank-label human pilot; AI screening speed is not human review throughput. Neither target is demonstrated yet, and the minimum has not been lowered.

1. Why can a batch with several sources still fail the request-type cap?
2. Why does a shared number such as 12345 not prove two requests belong to the same group?
3. Why is the catalogue example lookup rather than calculation?

These questions remain unanswered. Implementation evidence does not change Altan's learning status. Full evidence is in docs/evidence/m3-5-group-quota-audit.md, m3-5-lookup-diversity.md and m3-5-calculation-diversity.md. Raw queries, attribution, scripts, decisions and hashes stay in ignored work/m3-5-groups/.
