# Public expansion screen: lookup and document retrieval

> **Superseded grouping, October 26.** This screen used the v1 request-template rule. [Guide v2](guide-v2.md) now groups by scenario or source, so the family caps below no longer limit capacity. The per-record labels, risks, and source notes still apply.

Screened October 26, 2026 under annotation guide v1. Research preparation only. No record was imported, rewritten, accepted, or used for training. Every disposition below is an agent screening proposal, not a human label or adjudication.

## Finding

Public rows are not the bottleneck; independent request templates are. Under Altan's shared-request-template rule, the screened Dolly and BFCL records collapse into a few families that mostly already exist in the pilot. Each family holds at most four research rows. Even if every proposal below were accepted, document retrieval would reach about 8 of 15 groups and lookup about 6 of 15. The remaining groups need new templates from another source, targeted authoring, or a changed target. Choosing between those is Altan's decision.

## Gap from the accepted pilot

Counts come from the 38 accepted rows in local `data/raw/pilot-v0.jsonl` (SHA-256 `314365de…2a44`). Group counts overlap across labels in mixed-label families.

| Label | Rows | Groups | Rows needed | Groups needed |
| --- | ---: | ---: | ---: | ---: |
| calculation | 9 | 6 | 21 | 9 |
| document_retrieval | 9 | 5 | 21 | 10 |
| knowledge_lookup | 10 | 4 | 20 | 11 |
| direct_answer | 10 | 7 | 20 | 8 |

At least 82 more accepted rows are needed in total. Each class also needs enough new families: with four rows per family, 30 rows require at least eight families, and the 15-group target is stricter.

## Sources and selection

Both sources were already pinned and hashed in earlier inspections, and their cached files matched those hashes before screening. No new download, account, or dependency was used.

- **Dolly** ([inspection](public-document-retrieval.md), CC BY-SA 3.0). Over all 15,011 records, a fixed regular expression kept instructions that explicitly refer to an attached text, passage, paragraph, or article and have nonempty context. That left 1,483 records. The 20 previously inspected lines were removed, leaving 1,478. From these, 80 were drawn with `random.Random(42)` and judged one by one. The keyword filter can miss records and does not decide labels.
- **BFCL v3** ([inspection](bfcl-compatibility.md), Apache 2.0). All 100 SQL records were checked. The 21 whose reference answer is a read-only `SELECT` were judged, and the 79 writes (create, insert, update, delete) were excluded as outside the read-only lookup action. The cached simple, executable-simple, live-simple, and chatable files were also searched for a named structured source (database, catalog, table, inventory, record, and similar words). Five of those matches were judged.

## Dolly: 80 sampled records, proposed document families

All 80 meet the conditional attachment reading from the earlier inspection: the classifier sees only the original instruction, and the original context is kept separately as the passage to read. Altan has not yet adopted that adapter.

| Proposed family | Sampled records | Rows still allowed under the cap | Note |
| --- | ---: | ---: | --- |
| g008, answer a question from an identified document | 46 | 1 | Already holds 3 pilot rows. |
| g002, summarize or list key points | 10 | 2 | Already holds 2 pilot rows. |
| New: extract every item of a category, formatted | 22 | 4 | Boundary with g008 for Altan: listing all matches versus answering one question. |
| New: edit the passage's own text | 1 (about 5 more in the pool) | 4 | Boundary with g019's translation of document text. |
| New: read figures, then compute | 1 | 4 | Most "how many" cues only ask for a stated number, which is g008. Genuine computations are rare. |

Most sampled rows fall into families that are already full or nearly full. Dolly can add at most about 15 document rows and 3 new families, and only if Altan accepts both new boundaries. That gives 24 rows and 8 groups, against targets of 30 and 15.

## BFCL: read-only lookup candidates

| Proposed family | Records | Rows still allowed under the cap |
| --- | ---: | ---: |
| g003, one field of a keyed record | 4 | 0, already full |
| g016, find or count records matching a condition | 16 | 2 |
| New: retrieve matching records, then aggregate a field (average, total) | 3 | 3 |
| New: check a record against a threshold | 1 | 1 |

Correction, October 26: `sql_15` asks to correct a stored value, which is a write. It is not a keyed lookup and was excluded from the [import](public-import-v2.md). Held: `simple_92` names a real external database (IMDB), and `simple_309` asks for a player's season record without naming a source. At most 6 lookup rows and 2 new families are available, giving 16 rows and 6 groups. The aggregate family needs Altan's confirmation that its first action is lookup and that it is separate from g005's lookup-then-scale request.

## Risks to record before any import

- **Source style as a label cue.** Dolly rows usually say "Given this paragraph" or "reference text", and BFCL SQL rows name tables and columns. A classifier could learn the source's phrasing instead of the first action. Count rows by source and class, and compare that with the pilot's fictional-document wording.
- **Attachment adapter.** Dolly rows count as document retrieval only if the original passage stays attached outside the classifier input. Without that, hold them, as in the earlier inspection.
- **Calculation and direct answer were not part of this step.** Their earlier shortlist entries (11 BFCL calculation texts and 14 direct-answer texts) still need the same template check.

## Reproduce

The local ignored directory `work/poteto/public-expansion/` contains `dolly_screen.py`, which checks the Dolly hash and redraws the sample, and `judge.py`, which holds every per-record family judgment, checks that each sampled line has exactly one judgment, and writes `screen-summary.json`. Run both from the repository root with `python3 -I`. The Dolly sample SHA-256 is `8fab98635033d05496aa7e7120a6ab8223104b7cf9c00795f40c78cd66a580b7`. The recorded judgments are AI proposals, not automatic semantic proof.
