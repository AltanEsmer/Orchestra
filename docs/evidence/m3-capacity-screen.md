# M3 capacity screen

Screened October 26, 2026, after the M2 run, against the source mix and 400-row target in the [collection brief](../collection-brief.md). This is a capacity estimate. No row was imported, labelled, or accepted. Every eligibility verdict below is an agent screening proposal (Claude Opus 5.5), not a human label.

## Finding

Three classes can reach about 100 rows within the brief's mix. Lookup cannot. After the 40 percent request-type limit, BFCL supplies 33 to 46 new lookup rows, and the AI drafts add 11. That leaves **11 to 24 lookup rows** with no screened source. The brief leaves that decision to Altan. Screening eight more BFCL files at Altan's request reduced the shortfall by about three rows, because most of their lookups are keyed-record lookups and that type is already at its limit. Calculation's second source, GSM8K, was screened after Altan approved the download, and it covers the 16 rows calculation needs.

## What eligible means

A candidate counts only if it could enter M3 under guide v2:

- Its text is new. Exact text matches with M1 rows, and texts reaching 0.5 token overlap (Jaccard) with any M1 row, were dropped. This is the brief's near-duplicate threshold.
- It joins no M1 group. Dolly rows sharing an M1 passage, BFCL rows querying an M1 table or function set, and AI drafts reusing an M1 named setting were dropped.
- Its first action fits the class under the annotation guide. The text names its document or source, needs no live or external data, and is a single-turn user request.
- Its group stays within four rows, and its request type stays within 40 rows of the class.

The cumulative checks count the frozen M1 rows (`data/processed/m1-v1.jsonl`, SHA-256 `3e02b6fa…3b2e`). At 100 rows per class, one source supplies at most 75. For each class the table subtracts M1's rows from that 75 to get the main source's room, and the second source must cover the rest.

## Per-class capacity

| Class | M1 rows | New rows for 100 | Main source room under 75% | Main source supply | Second source needs | Second source supply | Shortfall |
| --- | ---: | ---: | ---: | --- | ---: | --- | ---: |
| Direct answer | 33 (23 No Robots, 10 Altan) | 67 | 52 | No Robots: about 374 | 15 | Dolly no-passage: about 5,900 | 0 |
| Document retrieval | 31 (22 Dolly, 9 Altan) | 69 | 53 | Dolly: about 1,900 | 16 | No Robots passage: 35 | 0 |
| Calculation | 32 (23 BFCL, 9 Altan) | 68 | 52 | BFCL: about 156 | 16 | GSM8K test split: about 1,300 | 0 |
| Knowledge lookup | 32 (22 BFCL, 10 Altan) | 68 | 53 | BFCL: 33–46 | 22–35 | AI drafts: 11 | **11–24** |

Lookup's ranges come from 16 borderline BFCL rows. The low end excludes them and the high end includes them. The shortfall assumes every usable draft is accepted after Altan's labelling and the AI check. Any rejection widens it.

## How each source was measured

Filters in `pools.py` narrow what was judged. They do not decide labels. Small pools were judged in full. Large pools were judged on a seeded sample of 30 (`random.Random(42)`). The estimate is the number of distinct texts in the pool times the sampled share, with a 95 percent Wilson interval.

| Pool | Filter | Distinct texts | Judged | Eligible | Estimate (95% interval) |
| --- | --- | ---: | ---: | ---: | --- |
| No Robots, direct categories | Generation, Brainstorm, Open QA, Rewrite, Classify, Coding; single turn | 374 | 30 | 30 | 374 (331–374) |
| Dolly, no-passage categories | open QA, brainstorming, creative writing; empty context | 6,138 | 30 | 29 | about 5,900 (5,114–6,101) |
| Dolly, passage categories | closed QA, information extraction, summarization; nonempty context | 4,340 | 30 | 13 | about 1,900 (1,188–2,638) |
| No Robots, passage categories | Summarize, Closed QA, Extract; single turn | 47 | 47 | 35 | 35, exhaustive |
| BFCL, calculation | math-like function name in the cached files | 292 | 30 | 16 | about 156 (105–203) |
| BFCL, lookup | named structured source or record ID in the user text, or a read-only SQL `SELECT` | 193 of 214 records | 214 | 37 firm, 12 borderline | see the combined row |
| BFCL parallel and irrelevance files, lookup | same filter, skipping texts already in the row above | 109 of 112 records | 112 | 6 firm, 4 borderline | see the combined row |
| BFCL lookup, combined | both rows above | | 326 | 43 firm, 16 borderline | 33 firm, 46 with borderline, after caps |
| AI drafts, lookup | proposed lookup label | 20 | 20 | 15 | 11 after the shared type cap |
| GSM8K test split, calculation | every question | 1,319 | 30 | 30 | about 1,300 (1,169–1,319) |

Notes on the judgments:

- **Dolly passage rows.** Most failures ask a bare question ("When did Alia Bhatt get her first leading role?") that names no passage. The adapter hides the passage from the router, so the text alone points to a direct answer, not retrieval. The earlier screen used the same rule.
- **No Robots passage rows.** The passage is inline in the prompt, not a separate field. A row counts when its instruction refers to the text ("Summarize this article", "Use the following passage") and the passage can be split off at a clear boundary. One counted row puts the instruction after the passage. Rows that only ask a question with no reference to the text failed.
- **BFCL calculation.** Weather, home searches, contact lookups, and formulas with missing inputs failed. The cached `chatable` file repeats `simple` records, which is why its 323 records hold only 292 distinct texts. Many finance and physics rows are small variations of each other and will share groups. With about 156 eligible rows against a need of 52, grouping does not bind.
- **BFCL lookup.** Most of the 214 candidates are writes (server setup, orders, bookings, payments), live data (weather, flight status, Amazon prices), real external databases (IMDB, a county property registry), or chatable copies. The 37 firm rows form 20 groups. Sixteen ask about one person, Adriel, and form one group capped at four. Six near-identical API-token requests form another. 33 of the 37 are keyed-record lookups. M1 already has 12 keyed-record lookups, so at most 28 more fit under the 40-row limit, which leaves 32. Most give a record ID without naming the database, the same flag 4 accepted M1 lookups carry. That is a source-style cue risk. The 12 borderline rows are stored sensor readings, file listings, and settings checks. Each could count as live telemetry or a file system listing rather than a structured lookup. Altan decides those during labelling.
- **BFCL parallel and irrelevance files.** Altan said: "Download all eight BFCL parallel and irrelevance files at revision 61fc0608 and screen them for lookup." Of 1,644 records, 51 were multi-turn or carried a system message, and 112 passed the lookup filter. Most are orders, bookings, account logins, arithmetic, external APIs (VirusTotal, Amazon, a census database), multi-task requests with no unique first action, or prompts missing context ("his profile?"). Six are firm lookups. Five are keyed-record lookups (a player ID, a DNA ID, an employee, an order, an advisory ID), which the type limit already excludes. One, a transaction history followed by a total, is lookup-then-aggregate and adds a row. "Where is my order #123" describes the same order as an earlier BFCL candidate, so it shares that group. The four borderline rows are an SNP lookup in a real external database (as one accepted M1 row), court records, a library catalog request whose later tasks fell outside the view, and stored system anomalies.
- **SQL rows.** All four remaining read-only SQL rows query the `employees` or `customers` table, which already have M1 groups. None is eligible.
- **GSM8K.** All 30 sampled questions supply every number and ask for one numeric result. None needs a source or live data. Few say "calculate", which dilutes the cue the brief lists. Several reuse first names (three mention a Steve) in unrelated situations, which do not join groups under guide v2. None reached 0.5 token overlap with an M1 row.
- **AI drafts.** Five lookup drafts reuse a name from an M1 group (Willow, Cedar, Elm, Birch, Oak), so guide v2 joins them to it. Four of the remaining 15 are keyed-record lookups. If BFCL fills the keyed-record limit, those four do not fit. Drafts that share a name (Alder, Fern) share a group.

## GSM8K

GSM8K's license and pinned revision are now in `data/manifests/sources.json`:

- License: MIT, stated in the [dataset card at revision `740312ad`](https://huggingface.co/datasets/openai/gsm8k/blob/740312add88f781978c0658806c59bc2815b9866/README.md) and in the LICENSE of [openai/grade-school-math](https://github.com/openai/grade-school-math/blob/3101c7d5072418e28b9008a6636bde82a006892c/LICENSE) (Copyright 2021 OpenAI). This confirms the brief's "MIT, to be confirmed".
- Revision: `740312add88f781978c0658806c59bc2815b9866`, read from the Hugging Face API on October 26.
- Size from the card: 7,473 training and 1,319 test questions in the `main` configuration.

Altan said: "Yes, download the GSM8K test parquet at revision 740312ad and screen it for calculation." The agent downloaded `main/test-00000-of-00001.parquet` (419,088 bytes) into ignored `work/poteto/gsm8k-download/`. Its SHA-256, `ee7b8da9e381df27b9e3f7758a159ab2bdaa4dbaa910546cbbc47e0cb44e4f59`, matches the upstream LFS hash and is now the manifest's `file_sha256`. The training file (2,306,545 bytes) was not downloaded.

The parquet also holds each worked solution and final answer. `export_gsm8k.py` checks the hash and writes only the `question` column, with row indexes, to ignored `gsm8k-test-questions.jsonl` (SHA-256 `490d5595…9e0b`). It ran in a throwaway `uv run --no-project --with pyarrow` environment, so no project dependency changed. The screen never read a solution or answer.

## Decisions for Altan

1. **Lookup shortfall of 11–24 rows.** The brief already names Altan-authored queries as lookup's second source, so you could write them. Otherwise, choose a top-up such as more AI drafts, a lower lookup target, or another source. The BFCL parallel and irrelevance files are now screened. Avoid keyed-record lookups. That type is at its 40-row limit.
2. **The 16 borderline BFCL lookups.** Do stored sensor readings and anomalies, file listings, settings checks, real external records (SNP, court records), and a library catalog request count as structured lookup?

GSM8K needs no further decision for capacity. Its rows still need Altan's labels and the AI check.

## Exposure and limits

- The agent read about 540 candidate texts during this screen. Collection must disclose that exposure, as for the M1 import.
- No filter or judgment used the M2 validation errors. The agent read Altan's error hypotheses in the learning log only after every judgment was fixed in `judge.py`, while drafting these docs.
- Eligibility is one agent's reading of the guide. Altan's labels and the blind AI check decide acceptance. Sampled pools carry sampling error, shown by the intervals. Only the No Robots passage, both BFCL lookup, and AI draft pools were judged in full. The GSM8K sample is unanimous, so its interval mainly reflects the sample size.
- Only local files at their pinned revisions were screened: BFCL `simple`, `exec_simple`, `multiple`, `live_simple`, `live_multiple`, `chatable`, `sql`, and the eight parallel and irrelevance files listed below; the No Robots test split (500 rows); all of Dolly; the GSM8K test split. The No Robots training split was not screened, and the screen did not need it.

## Reproduce

The ignored directory `work/poteto/m3-capacity/` holds the tools. Run `export_gsm8k.py` once as described above, then the other two from the repository root with `python3 -I`. `pools.py` checks the SHA-256 of M1, the import provenance, and every source file, then writes the pools and seeded samples. `judge.py` holds every verdict, asserts one verdict per judged line, and writes `capacity.json`.

| File | SHA-256 |
| --- | --- |
| `export_gsm8k.py` | `e0d111d39b7eaeb8e71c3da8b725222933bf1cfb9aa7c78ee429f2a9c6041fb4` |
| `pools.py` | `dfcaa1d8752316cf7b28e89ee805d1afd8ad1775f2ba9bf6490448425232eebe` |
| `judge.py` | `6d4cb5db668dde6f6d6f74c669b1af66cf961757733664e9495b44eaf73857ca` |
| `pools.json` | `0dca84fd762d70a79a8296ec4c1db3d62a7564f6fcf1575f97819c2391386c0f` |
| `capacity.json` | `85fa3514bae6943ba945700f2425a960f45b7c234d6b30387a5f2fd22ca8a4ac` |

Adding GSM8K, then the BFCL parallel and irrelevance pool, as the last pools left the earlier seeded samples byte-identical; the agent compared them before and after each change.

The eight BFCL files were downloaded into ignored `work/poteto/bfcl-download-m3/` from revision `61fc0608cfd831fcfbbaa676ebdfef0ed963eeda`. Each file's size and git blob ID match the Hugging Face API listing. `pools.py` pins their SHA-256:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `BFCL_v3_parallel.json` | 172,094 | `fad375d6…1c3c` |
| `BFCL_v3_parallel_multiple.json` | 347,080 | `8863ea84…0579` |
| `BFCL_v3_exec_parallel.json` | 56,281 | `67826cdd…153d` |
| `BFCL_v3_exec_parallel_multiple.json` | 73,943 | `e3134c94…977d` |
| `BFCL_v3_live_parallel.json` | 15,649 | `6c26e9fd…a421` |
| `BFCL_v3_live_parallel_multiple.json` | 82,332 | `21d4b931…6e79` |
| `BFCL_v3_irrelevance.json` | 160,114 | `975f51c5…8690` |
| `BFCL_v3_live_irrelevance.json` | 2,202,715 | `0d259e1c…1338` |
