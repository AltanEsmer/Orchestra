# Annotation guide v2: scenario and source groups

On October 26, 2026, Altan asked for rules that are "not strict", simple to follow, and still high quality. Under v1, a group was a shared request template, and the [expansion screen](public-expansion-screen.md) showed that this let only a few public rows count. Guide v2 changes only the grouping rule and adds batch quality checks. First-action labels, label boundaries, review method, and readiness targets (120 rows, 30 per class, 15 groups per class) are unchanged.

## Rule change

| | v1 (request template) | v2 (scenario or source) |
| --- | --- | --- |
| Rows share a group when | They have the same goal and procedure, whatever the scenario | They are small variations, share a source or named setting, describe the same situation, or come from one public record |
| What the test score measures | New request types | New topics and sources with familiar request types |
| Effect on public data | 50 "answer from the passage" rows count as one group | Each distinct passage or table is its own group |
| Leakage protection | Strong, but blocks M1 | Stops memorizing a shared source, setting, or wording across splits |

To keep quality, v2 adds three batch checks (see the [guide](../annotation-guide.md#quality-checks-for-every-batch)):
- A near-duplicate review.
- Request-type spread: no request type above 40 percent of a class.
- Source mix: at least two sources per class, and no source above 75 percent of a class.

These replace the protection that the stricter grouping gave against a few request types or one source's phrasing dominating a class. An optional unseen-request-type analysis can still report the harder v1 question.

## Pilot regrouping

The agent applied the v2 rule to the 38 accepted rows. Only `group_id` and `annotation_version` (now `guide-v2`) changed; text, labels, rationales, sources, and annotators are byte-identical. Nine v1 groups keep their IDs because their membership did not change (g001, g004, g007, g014, g017, g018, g021, g025, g032). Every changed group got a new ID.

| New group | Rows | Reason |
| --- | --- | --- |
| g034 | q0002, q0003, q0006 | Northstar Shop handbook and catalog |
| g035 | q0007, q0011 | Riverside School and Riverside Library |
| g036 | q0010, q0016 | Pinewood Camp letter and reservations |
| g037 | q0027, q0028 | Cedar Camp and Cedar Outdoors |
| g038 | q0032, q0035, q0036, q0040 | Willow Hotel database and Willow School |
| g039 | q0023, q0024, q0026 | Maple School letter, Maple Library, and the school-welcome translation |
| g040 | q0019, q0020, q0039 | Oak and Birch camp letters, Oak Centre, Birch Club |
| g041 | q0031 | Elm School |
| g042–g044 | q0005, q0012, q0029 | Separate per-unit situations (ticket, track, recipe) |
| g045, g046 | q0015, q0033 | Separate difference situations (lesson, water tank) |
| g047 | q0034 | Word sorting, separate from catalog ordering |

The shared names follow the blind AI pilot reviewer's [original flags](pilot-ai-review.md) (Willow Hotel records, Northstar catalog). They are an agent application of Altan's requested rule, listed here so he can object to any assignment. Splitting by shared name is conservative: Riverside School and Riverside Library share only a word, but a model could still learn it.

| Label | Rows | Groups (v1) | Groups (v2) |
| --- | ---: | ---: | ---: |
| calculation | 9 | 6 | 9 |
| document_retrieval | 9 | 5 | 8 |
| knowledge_lookup | 10 | 4 | 7 |
| direct_answer | 10 | 7 | 7 |

There are 23 groups in total: 14 singletons, four pairs, four triples, and one group of four. Seven groups mix labels; every accepted row already has a review entry. `scripts/validate_dataset.py` with the unchanged review ledger passes all 38 rows.

Before SHA-256: `314365de4c1807517a7a027bbb8b7d1aa992000f18dbb58e73059c5ce7d22a44`. After SHA-256: `047f3c0b0e746b1892f35c82ab28993ecb0180e17d3909e0f8b59b4d84a20eec`. Ledger SHA-256, unchanged: `29e5cbd1248672c06ea59f1ba536c7a4d822bc78a5ccab14c5e348550daa60c2`. The before copy and `regroup.py`, which checks the before hash and refuses to run otherwise, are in ignored `work/poteto/guide-v2/`.

## Public capacity under v2

These are capacity estimates from already screened sources, not accepted rows.

| Label | Pilot rows/groups | Public source under v2 | What still limits it |
| --- | --- | --- | --- |
| document_retrieval | 9 / 8 | Dolly: 1,483 passage-referencing records over 1,399 distinct passages, most in their own group | Request-type spread (question answering at most 40 percent) and the attachment adapter decision |
| knowledge_lookup | 10 / 7 | BFCL SQL: 21 read-only rows over 14 named tables, so 20 usable under the cap | About 15 are condition filters, which exceeds the 40 percent spread. SQL table and column wording is a style cue. Other lookup request types are needed, such as the pending AI drafts. |
| calculation | 9 / 9 | 11 shortlisted BFCL texts. BFCL simple has more math requests, not yet screened. | Screen about 10 more. |
| direct_answer | 10 / 7 | 13 No Robots and 1 BFCL shortlisted. No Robots has more, not yet screened. | Screen about 6 more. |

The 40 AI-drafted candidates in the [template draft record](template-expansion-draft.md) used v1 family accounting. Under v2, that cap table no longer applies. Each draft gets a group from its own scenario or source, and drafts sharing a named setting share a group. They remain unaccepted proposals that need Altan's primary labels and the AI check.

## What this does not change

No source was adopted, no public row imported, no label changed, and no split or model run. The attachment adapter for Dolly, source licenses, and every new label still need Altan's decisions. The report must disclose the v1→v2 change, why it was made, and that the test measures new scenarios rather than new request types.
