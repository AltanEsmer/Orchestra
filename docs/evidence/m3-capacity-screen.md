# M3 capacity screen

Screened October 26, 2026, after the M2 run, against the source mix and 400-row target in the [collection brief](../collection-brief.md). This is a capacity estimate. No row was imported, labelled, or accepted. Every eligibility verdict below is an agent screening proposal (Claude Opus 5.5), not a human label.

## Finding

Three classes can reach about 100 rows within the brief's mix. Lookup cannot. After the 40 percent request-type limit, BFCL supplies 32 to 43 new lookup rows, and the AI drafts add 11. That leaves **14 to 25 lookup rows** with no screened source. Calculation's second source, GSM8K, is unscreened because no GSM8K file has been downloaded. The brief leaves both decisions to Altan.

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
| Calculation | 32 (23 BFCL, 9 Altan) | 68 | 52 | BFCL: about 156 | 16 | GSM8K: unscreened | unknown |
| Knowledge lookup | 32 (22 BFCL, 10 Altan) | 68 | 53 | BFCL: 32–43 | 25–36 | AI drafts: 11 | **14–25** |

Lookup's ranges come from 12 borderline BFCL rows. The low end excludes them and the high end includes them. The shortfall assumes every usable draft is accepted after Altan's labelling and the AI check. Any rejection widens it.

## How each source was measured

Filters in `pools.py` narrow what was judged. They do not decide labels. Small pools were judged in full. Large pools were judged on a seeded sample of 30 (`random.Random(42)`). The estimate is the number of distinct texts in the pool times the sampled share, with a 95 percent Wilson interval.

| Pool | Filter | Distinct texts | Judged | Eligible | Estimate (95% interval) |
| --- | --- | ---: | ---: | ---: | --- |
| No Robots, direct categories | Generation, Brainstorm, Open QA, Rewrite, Classify, Coding; single turn | 374 | 30 | 30 | 374 (331–374) |
| Dolly, no-passage categories | open QA, brainstorming, creative writing; empty context | 6,138 | 30 | 29 | about 5,900 (5,114–6,101) |
| Dolly, passage categories | closed QA, information extraction, summarization; nonempty context | 4,340 | 30 | 13 | about 1,900 (1,188–2,638) |
| No Robots, passage categories | Summarize, Closed QA, Extract; single turn | 47 | 47 | 35 | 35, exhaustive |
| BFCL, calculation | math-like function name in the cached files | 292 | 30 | 16 | about 156 (105–203) |
| BFCL, lookup | named structured source or record ID in the user text, or a read-only SQL `SELECT` | 193 of 214 records | 214 | 37 firm, 12 borderline | 32 firm, 43 with borderline, after caps |
| AI drafts, lookup | proposed lookup label | 20 | 20 | 15 | 11 after the shared type cap |

Notes on the judgments:

- **Dolly passage rows.** Most failures ask a bare question ("When did Alia Bhatt get her first leading role?") that names no passage. The adapter hides the passage from the router, so the text alone points to a direct answer, not retrieval. The earlier screen used the same rule.
- **No Robots passage rows.** The passage is inline in the prompt, not a separate field. A row counts when its instruction refers to the text ("Summarize this article", "Use the following passage") and the passage can be split off at a clear boundary. One counted row puts the instruction after the passage. Rows that only ask a question with no reference to the text failed.
- **BFCL calculation.** Weather, home searches, contact lookups, and formulas with missing inputs failed. The cached `chatable` file repeats `simple` records, which is why its 323 records hold only 292 distinct texts. Many finance and physics rows are small variations of each other and will share groups. With about 156 eligible rows against a need of 52, grouping does not bind.
- **BFCL lookup.** Most of the 214 candidates are writes (server setup, orders, bookings, payments), live data (weather, flight status, Amazon prices), real external databases (IMDB, a county property registry), or chatable copies. The 37 firm rows form 20 groups. Sixteen ask about one person, Adriel, and form one group capped at four. Six near-identical API-token requests form another. 33 of the 37 are keyed-record lookups. M1 already has 12 keyed-record lookups, so at most 28 more fit under the 40-row limit, which leaves 32. Most give a record ID without naming the database, the same flag 4 accepted M1 lookups carry. That is a source-style cue risk. The 12 borderline rows are stored sensor readings, file listings, and settings checks. Each could count as live telemetry or a file system listing rather than a structured lookup. Altan decides those during labelling.
- **SQL rows.** All four remaining read-only SQL rows query the `employees` or `customers` table, which already have M1 groups. None is eligible.
- **AI drafts.** Five lookup drafts reuse a name from an M1 group (Willow, Cedar, Elm, Birch, Oak), so guide v2 joins them to it. Four of the remaining 15 are keyed-record lookups. If BFCL fills the keyed-record limit, those four do not fit. Drafts that share a name (Alder, Fern) share a group.

## GSM8K

GSM8K's license and pinned revision are now in `data/manifests/sources.json`:

- License: MIT, stated in the [dataset card at revision `740312ad`](https://huggingface.co/datasets/openai/gsm8k/blob/740312add88f781978c0658806c59bc2815b9866/README.md) and in the LICENSE of [openai/grade-school-math](https://github.com/openai/grade-school-math/blob/3101c7d5072418e28b9008a6636bde82a006892c/LICENSE) (Copyright 2021 OpenAI). This confirms the brief's "MIT, to be confirmed".
- Revision: `740312add88f781978c0658806c59bc2815b9866`, read from the Hugging Face API on October 26.
- Size from the card: 7,473 training and 1,319 test questions in the `main` configuration.

Calculation needs 16 GSM8K rows. The card describes grade-school word problems that supply their numbers, which suggests most questions qualify. That is a guess until the questions are read. Screening needs one download, which Altan has not yet approved:

| File | Source | Size | Upstream SHA-256 |
| --- | --- | ---: | --- |
| `main/test-00000-of-00001.parquet` | huggingface.co/datasets/openai/gsm8k at `740312ad` | 419,088 bytes | `ee7b8da9…4e59` |
| `main/train-00000-of-00001.parquet` | same | 2,306,545 bytes | `ea82612e…19d` |

The test file alone holds 1,319 questions, far more than 16. The files include each worked solution and final answer. The import would keep only the `question` field.

## Decisions for Altan

1. **Lookup shortfall of 14–25 rows.** The brief already names Altan-authored queries as lookup's second source, so you could write them. Otherwise, choose a top-up such as screening more BFCL files (the parallel and irrelevance sets are not cached locally), more AI drafts, a lower lookup target, or another source. Avoid keyed-record lookups. That type is at its 40-row limit.
2. **The 12 borderline BFCL lookups.** Do stored sensor readings, file listings, and settings checks count as structured lookup?
3. **GSM8K download.** Approve downloading the 419,088-byte test parquet above to screen calculation's second source.

## Exposure and limits

- The agent read about 400 candidate texts during this screen. Collection must disclose that exposure, as for the M1 import.
- No filter or judgment used the M2 validation errors. The agent read Altan's error hypotheses in the learning log only after every judgment was fixed in `judge.py`, while drafting these docs.
- Eligibility is one agent's reading of the guide. Altan's labels and the blind AI check decide acceptance. Sampled pools carry sampling error, shown by the intervals. Only the No Robots passage, BFCL lookup, and AI draft pools were judged in full.
- Only locally cached files at their pinned revisions were screened: BFCL `simple`, `exec_simple`, `multiple`, `live_simple`, `live_multiple`, `chatable`, `sql`; the No Robots test split (500 rows); all of Dolly. The No Robots training split was not screened, and the screen did not need it.

## Reproduce

The ignored directory `work/poteto/m3-capacity/` holds the tools. Run both from the repository root with `python3 -I`. `pools.py` checks the SHA-256 of M1, the import provenance, and every source file, then writes the pools and seeded samples. `judge.py` holds every verdict, asserts one verdict per judged line, and writes `capacity.json`.

| File | SHA-256 |
| --- | --- |
| `pools.py` | `f3c4f0b58a8d2cc83829c55803f486185154a9ac4bb02a93714a6e552106e663` |
| `judge.py` | `e423353b8e0e7d8bc9fbcf13de6395bbb55f2f4d1c12bc7a66e47acab5305abd` |
| `pools.json` | `8075c2537f80acd5e1c2896efe6798f41dbef28fc699258d4d47283e88aab234` |
| `capacity.json` | `27afee0a70bd5345f6c83532a3afda98af50b3c38f77ece25f01ff5e525271c2` |
