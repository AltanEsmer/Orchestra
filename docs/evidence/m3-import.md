# M3 candidate import

Prepared October 28, 2026. Altan asked to complete M3. Its dataset gate needs about 272 new rows that carry his labels, so the agent asked how to proceed. He chose "Build import for review". This is a candidate import, not a release. All 312 new rows are `needs_review` with a null label. The agent's proposed label for each row sits in a local worksheet until Altan records his own.

## What was imported

The sources and mix follow the [collection brief](../collection-brief.md). The supply estimates come from the [capacity screen](m3-capacity-screen.md).

| Class | Source | Quota | Reserve | Pool positions walked | Eligible in the walk |
| --- | --- | ---: | ---: | ---: | ---: |
| Document retrieval | Dolly passage categories | 53 | 3 | 180 | 71 |
| Document retrieval | No Robots passage categories | 16 | 3 | 22 | 19 |
| Calculation | BFCL | 52 | 3 | 122 | 57 |
| Calculation | GSM8K test split | 16 | 3 | 19 | 19 |
| Direct answer | No Robots direct categories | 52 | 3 | 55 | 55 |
| Direct answer | Dolly categories without a passage | 15 | 3 | 19 | 18 |

Knowledge lookup has 90 candidates for 68 places: 33 firm BFCL rows, 16 borderline BFCL rows, 11 template drafts, and the 30 N drafts. The lookup fill rule below decides which of them enter the release.

In total the worksheet holds 75 retrieval, 74 calculation, 73 direct-answer, and 90 lookup rows. 75 rows carry a passage as a linked attachment.

## How rows were chosen

`order.py` fixed each pool's order before any judgment. The capacity screen's judged sample comes first, then the rest of the pool in a seeded shuffle. It rebuilds each pool with the screen's filters and asserts the screen's pool sizes. The agent judged rows in that order and stopped once a pool's quota and three reserves were filled. A script assertion confirms that every earlier screen verdict stands.

Eligibility follows the annotation guide:

- **Retrieval.** The instruction must refer to its passage ("this article", "the given text"). The router never sees the passage, so a bare question fails, as in the screen.
- **Calculation.** The request asks for one numeric result and supplies every input. Standard constants such as gravity are allowed and flagged. Live rates, lookups, and unstated formula constants fail.
- **Direct answer.** The request needs writing or stable knowledge. Text supplied inside the query is allowed.
- **Lookup.** The capacity screen's verdicts apply unchanged.

No Robots passage prompts hold the passage inline. The import splits it off at the first blank line after the instruction. Two rows split at the second blank line, and one splits after the line "This is the article:". The instruction becomes the query. The passage keeps its exact characters and becomes a linked attachment. This is the adapter Altan adopted for Dolly, which the brief extends to No Robots.

A row was skipped when it:

- repeats an earlier text or its exact words,
- reaches 0.5 token overlap with an M1 row,
- would push its group above four rows,
- would push its request type above 40, or its main source above 75, of the class's 100 rows, or
- would push a cue word from the brief above its M1 share.

The brief asks new rows to dilute M1's cue associations. Without a limit, "paragraph" or "reference text" would rise from 10 of 31 retrieval rows to 41 of 100, and "calculate" from 16 of 32 calculation rows to 51 of 100. The cue limit holds each cue at its M1 share, which is 32 and 50 of 100. The agent added this limit after seeing those projected counts and before any label existed. It skipped 15 Dolly rows and 2 BFCL rows.

## Fill rule, fixed before labels

After Altan's labels and adjudication:

- In retrieval, calculation, and direct answer, each pool keeps its accepted rows in pool order until its quota fills. Reserves replace rejected rows in the same order.
- Lookup keeps accepted rows in fill order until the class reaches 100. Firm BFCL rows come first, one row per group in each round, then borderline BFCL rows, then template drafts, then N drafts by ID. A row that would break a limit is passed over.
- Every limit is checked again on the final class. If a class ends below 100 rows, the 40 and 75 percent limits apply to its actual size, and the shortfall is reported, not filled with new data.

Rows that labelling or the fill leaves out stay in the local candidate file with their reason. They do not enter the release.

## Projected release if every proposal is accepted

| Class | Rows | Groups | New groups | Largest request type | Largest source |
| --- | ---: | ---: | ---: | --- | --- |
| Document retrieval | 100 | 97 | 67 | 39% document question | 75% Dolly |
| Calculation | 100 | 96 | 65 | 16% physics formula, 16% word problem | 75% BFCL |
| Direct answer | 100 | 97 | 67 | 27% creative writing | 75% No Robots |
| Lookup, borderline rows excluded | 100 | 82 | 57 | 40% keyed record | 55% BFCL |
| Lookup, borderline rows counted | 100 | 76 | 51 | 40% keyed record | 68% BFCL |

These are projections, not results. Three classes sit exactly at the 75 percent source limit, and lookup sits exactly at the 40 percent keyed-record limit. The reserves and the final limit check exist for that reason. Each class has at least two sources and far more than five new groups, which `extend` requires.

Cue counts after the fill, against M1:

| Cue | Class | M1 | Projected |
| --- | --- | ---: | ---: |
| "paragraph" or "reference text" | retrieval | 10 of 31 | 32 of 100 |
| "fictional" | retrieval | 9 of 31 | 9 of 100 |
| "handbook" | retrieval | 4 of 31 | 4 of 100 |
| "calculate" | calculation | 16 of 32 | 50 of 100 |
| "table" | lookup | 13 of 32 | 14 of 100 |
| "database" | lookup | 8 of 32 | 14 of 100 |
| "fictional" | lookup | 10 of 32 | 10 of 100 |

Median query length rises from 18.5 to 23 words in calculation and from 14 to 17 in direct answer, because GSM8K and the longer BFCL requests are word problems. Retrieval moves from 14 to 15 words and lookup stays near 19.

## Hand checks

- **Overlap from 0.4 to 0.5.** 17 pairs in different groups fall in this range. One pair asks for the GCD and the LCM of the same numbers, 12 and 18. That is the same situation under guide v2, so the pair shares a group. The other pairs share only a sentence frame, such as "From the passage provided, extract …" or two future-value questions with different amounts. The guide does not join rows for that.
- **Shared capitalised names.** 71 names appear in more than one group. Most are sentence words or generic place nouns. Two BFCL rows that request the same `employee.fetch_data` fields now share a group, and so do two DNA-sequence lookups on the same unnamed database. The other names refer to different people or places, for example three unrelated Georges.
- **No cross-group pair reaches 0.5** after grouping.
- **Upstream repetition.** Reviewer part 1 noticed one No Robots rewrite prompt that pastes its passage twice. The upstream prompt is identical, so the import kept it as written and flagged it.
- `scripts/validate_dataset.py data/raw/m3-candidates.jsonl` printed `PASS: 440 rows valid` (128 frozen M1 rows and 312 candidates).

## Skipped rows

44 rows were skipped:

- 23 keyed-record BFCL lookups over the 40-row type limit. 14 of them are further Adriel requests.
- 17 rows over a cue share, as above.
- 1 sensor row over the four-row group limit.
- 2 duplicates. One API-token request repeats another exactly, and one differs only by a full stop.
- The borderline SNP row. It asks the same SNP-type question as M1 row q0067 on the same unnamed source, so it would join M1 group g074, which `extend` refuses.

## Source manifest

`data/manifests/sources.json` gains an `ai-drafts` entry for the 41 AI drafts. It records the drafting agent, the date, the two local bundles, and that the text is AI-generated and never attributed to Altan. Altan asked for the drafts on October 26. His approval of the worksheet confirms the entry.

## Blind AI check

Three fresh Claude Opus 5.5 subagents each checked 104 shuffled rows. Each saw only the annotation guide, the data protocol's prediction contract and attachment paragraph, and query-only text with an attachment flag. None saw a proposed label, request type, source, or flag. A script confirmed 312 decisions, each blind ID exactly once, with valid keys, labels, and judgments. The check ran before Altan's labels, which the M1 import did not do. Its output stays sealed in local files until his labels are recorded, so it cannot anchor them. Agreement has not been computed.

While part 2 ran, a rerun of the builder rewrote the three input files with identical bytes, which their hashes confirm. The builder now refuses to touch existing blind inputs.

## Exposure

The agent read about 560 more candidate texts during this import, on top of about 540 in the capacity screen. Before this import it had also read Altan's M2 validation-error hypotheses and validation row q0005, while writing the M2 study guide. No selection rule uses M2 errors. Fixed orders and fixed rules limit the agent's choices, but the agent also wrote every proposed label, request type, and flag. Approving those proposals carries anchoring risk, as the brief discloses.

## Decisions for Altan

1. Label the worksheet rows. "approve all" plus exceptions works, for example `q0200: exclude, needs live data`.
2. Say whether the 16 borderline BFCL rows count as lookup. They include stored sensor data, file listings, settings checks, court records, and a catalogue request that also reserves a book.
3. Confirm the 41 AI drafts and the `ai-drafts` source entry, or exclude drafts you reject.

## After the labels

The agent ingests the sealed AI decisions and accepts clear agreements. It lists every flag, ambiguity, and disagreement for Altan's adjudication. Then it applies the fill rule and runs the readiness check. It freezes `data/processed/m3-v1.jsonl` with `data/raw/m3-reviews-v1.jsonl` and follows the [runbook's M3 commands](../run-experiments.md#extend-the-dataset-and-run-m3). Those are `prepare-study`, two runs of the 14 configurations, `compare`, `select`, and `report`. The M3 study guide follows from those results.

## Local files

All candidate text stays in ignored files. `work/poteto/m3-import/import_m3.py` checks the M1 release, Dolly, No Robots, and draft hashes before building.

| File | SHA-256 |
| --- | --- |
| `work/poteto/m3-import/order.py` | `a371e39569ecae8bf8a458d7fac8b6ff504f5a3aad5a80376fe81cc72782af3e` |
| `work/poteto/m3-import/import_m3.py` | `e4f626a60e7b7337cce211ecbbc2f7cdba371fcd2cd859f688450ecf3ddeba8a` |
| `data/raw/m3-candidates.jsonl` | `4deb66547d65316c944832b0ad86abc5729f4c60e21d81acebd74c855526285d` |
| `data/raw/m3-import/provenance.jsonl` | `73a86203b1ed67ad55a690e660bb4cf40bb8b95a8e616bb87fd8006892f31773` |
| `data/raw/m3-import/attachments.jsonl` | `d02cec53ab367e08966c62fe616a382b90188222ddf9a948dc1bdacdf3ac42d7` |
| `data/raw/m3-import/batch-report.json` | `719ada646dd3f4765ea0ac238da97a49bc460f9ce65717eb4433de84435c5597` |
| `data/raw/m3-import/skipped.jsonl` | `09074e44b182f4a79ee3011c36e76625953aa833d41e240790a34b2f97537daa` |
| `data/raw/m3-import/review-worksheet.md` | `11be38394950cf34fef37167198413599809fee8146af3d6b236a2235ab36524` |
| `work/poteto/m3-import/blind/steward.json` | `d779db3bf73e9cb1fac9644aabd02579d01fdcc65e22852c5036e8bc22429a22` |

Blind check files, in `work/poteto/m3-import/blind/`:

| Part | Task prompt | Query-only input | Decisions |
| --- | --- | --- | --- |
| 1 | `1d0ac056…67ca` | `ca1b95e3…0977` | `fa68070b…d6be` |
| 2 | `009d7bc2…299b` | `ddbd5e4b…48c2` | `ad12ae54…c6d6` |
| 3 | `95baadca…4640` | `08d2a181…2db0` | `2a569ad9…1fe9` |

Provenance records each row's upstream file and ID or line, pool position, text and passage hashes, proposed label, request type, fill role and rank, flags, and exposure.

No row is accepted, no M3 split exists, and no M3 model ran.
