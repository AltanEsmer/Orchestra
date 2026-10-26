# Guide-v2 public import candidates

> **Update, October 26.** Altan approved all proposed labels. The blind AI check agreed on 90 of 90, 35 rows are accepted, and 55 flagged rows await his adjudication. See the [review record](public-review-v2.md).

Prepared October 26, 2026, after Altan approved the guide-v2 pilot regrouping and the Dolly attachment adapter, and asked to import Dolly for document retrieval, BFCL for lookup and calculation, and No Robots for direct answer. This is a candidate import, not a release. All 90 new rows are `needs_review` with a null label. The agent's proposed label for each row sits in a local worksheet until Altan records his own.

## What was imported

| Source | Rows | Proposed label | Selection |
| --- | ---: | --- | --- |
| Dolly 15k (CC BY-SA 3.0) | 22 | document_retrieval | From the seeded 80-record [screen](public-expansion-screen.md), the first records in source-line order of each request type: 9 passage questions, 6 summaries, 7 list extractions. |
| BFCL v3 (Apache 2.0) | 22 | knowledge_lookup | Read-only SQL `SELECT` records and keyed lookups from the simple, multiple, and live files, balanced so no request type exceeds 40 percent. |
| BFCL v3 | 23 | calculation | The 11 earlier shortlisted texts plus 12 judged from a seeded sample of math requests, with every input supplied. |
| No Robots (CC BY-NC 4.0) | 23 | direct_answer | The 13 earlier shortlisted prompts plus 10 judged from a seeded sample of short single-turn test prompts. |

The classifier input is only the user's original text. For Dolly, the original passage is stored as a linked attachment outside router input (the approved adapter). BFCL function documentation, expected calls, and system messages are not input. No text was rewritten.

The three sources are now in `data/manifests/sources.json` with author, date, license, notices, URL, revision, and Altan's adoption date. Adapted Dolly rows stay CC BY-SA 3.0 and No Robots rows CC BY-NC 4.0. Neither is covered by the repository MIT license.

Two BFCL files (`BFCL_v3_multiple.json`, `BFCL_v3_live_multiple.json`) were newly downloaded from the same pinned revision to find enough non-filter lookups. SHA-256: `aef16815…9b2a` and `af252072…0cee`. No Robots was read from the already pinned test parquet with a throwaway `pyarrow` environment; no project dependency changed.

## Batch checks, projected if every proposal were accepted

| Label | Rows | Groups | Largest request type | Largest source |
| --- | ---: | ---: | --- | --- |
| calculation | 32 | 32 | 16% (geometry, statistics) | 72% BFCL |
| document_retrieval | 31 | 30 | 39% (passage question) | 71% Dolly |
| knowledge_lookup | 32 | 26 | 38% (keyed record, condition filter) | 69% BFCL |
| direct_answer | 33 | 30 | 18% (brainstorm) | 70% No Robots |

Every class meets 30 rows, 15 groups, the 40 percent request-type limit, and the 75 percent single-source limit. Each class has two sources. The margins are small: each class can lose only 1–3 rows to rejection before it needs a top-up. Groups follow guide v2. Each Dolly passage and each named BFCL table is its own group. `students` and `customers` each hold two rows. One near-duplicate pair (two chemical-element table filters with the same sentence frame) was put in one group. No other pair reaches 0.5 token overlap across groups.

The combined local file `data/raw/m1-v2.jsonl` (38 accepted pilot rows plus 90 candidates) passes `scripts/validate_dataset.py` (128 rows). Readiness still fails until the candidates have labels and review entries, which is expected.

## Flags for Altan's review

27 rows carry a flag in the worksheet:
- 15 BFCL SQL rows use table and column wording that may act as a source cue.
- 5 No Robots rows ask stable facts with no named source, so they are proposed as direct_answer under the existing rule.
- 4 lookups give a record ID (order, complaint, case, event) without naming the database.
- 2 BFCL rows dropped an upstream system message.
- 1 Dolly question uses "them", which only the passage resolves.
- 1 lookup uses a real external database (SNP ID).

One correction to the earlier screen: `sql_15` asks to correct a value in a table. It is a write, not a read-only lookup, so it was excluded here and replaced by another keyed lookup.

## Local files and next steps

Ignored local files, from `work/poteto/public-import/import_v2.py`, which checks every source hash before building:

| File | SHA-256 |
| --- | --- |
| `data/raw/m1-v2.jsonl` | `7593e2d2144260b700f0b9aad768c40bd8b4209dacd2f72669893f7dffe99bca` |
| `data/raw/import-v2/provenance.jsonl` | `8a37355aba6999cef4647dea0cb634c49ab4723b66696b9006765bc71ca2a072` |
| `data/raw/import-v2/attachments.jsonl` | `5831d75f300ab60dfd70ce8588a411880c23d1b80feb4b55013dfa288b94e7ad` |
| `data/raw/import-v2/batch-report.json` | `32b0070725cd9504b92aa9a797996ac04f1a49694bb749db83f8a9cf29814fdf` |
| `data/raw/import-v2/review-worksheet.md` | `a4735e0710c8e9032ff5aa69bd353b1ff22f0c2f8cc399d95d4003e378027902` |

Provenance records the upstream file, ID or line, text and passage hashes, the proposed label and its origin, request type, group key, flags, and that the agent saw each row during screening.

Next steps:
1. Altan labels the worksheet rows ("approve all" plus exceptions). His answers become the primary labels under annotator A1. Proposals he approves are disclosed as agent-proposed and human-confirmed, which carries anchoring risk.
2. A blind AI check runs on query-only, shuffled input.
3. Altan adjudicates every disagreement or flag.
4. The readiness check runs, and the release is frozen as `data/processed/m1-v1.jsonl`.

No row is accepted, no split exists, and no model ran.
