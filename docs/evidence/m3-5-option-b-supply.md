# M3.5 option B lookup supply

November 1, 2026, following the [source discovery](m3-5-source-discovery.md). Altan asked what it would take to reach at least 2,000 accepted rows and chose option B, a near-balanced design. This note records that decision and the two screens it prompted. It is AI screening only. No source was adopted, row imported, label recorded, split changed or model run. Accepted rows remain **400**.

## Decision

Calculation, retrieval and direct-answer supply was inferred sufficient for 500 to 600 rows per class. Lookup is the only constraint. The options compared, with lookup sizes inferred from AI screening before human review:

| Option | Lookup rows | Each other class | Ratio | Approvals needed |
| --- | ---: | ---: | ---: | --- |
| A. Balanced | 500 | 500 | 1.0 | Attached tables, personal stores, and about 70 more lookups |
| **B. Near-balanced (chosen)** | about 430 | about 523 | 1.2 | Attached tables, personal stores, a stated imbalance |
| C. Attached tables only | about 360 | about 546 | 1.5 | Attached tables, imbalance |
| D. Personal stores only | about 215 | about 595 | 2.8 | Personal stores, imbalance |
| E. No scope change | about 130 | about 623 | 4.8 | Imbalance |

Lookup sizes respect the 40% request-type cap. Without DataBench, keyed records exceed 40% before other supply runs out, which is why options D and E fall so low.

Altan chose **B** on November 1. It means:

- **Size.** Lookup keeps as many rows as pass review, up to 500. The other three classes share the rest of 2,000 equally. If reviewed lookup falls below **350**, Altan decides again. Starting from 400, every option needs about 1,600 newly accepted rows.
- **Attached tables.** A public question that refers to its own table generically ("in the dataset") may keep the original table as an attachment outside router text, as Dolly passages do. Its first action is `knowledge_lookup`. A question with no table reference stays excluded. Each table forms one group, capped at four rows.
- **Personal stores.** A query that reads the user's own calendar, email, contacts, lists, bills or transactions names a structured store. One store kind is one group across all sources. Crowd-written public utterances qualify; real users' personal queries remain excluded. Live status requests stay excluded. After the tool-pool screen below, Altan extended the rule to the user's own accounts in third-party services, such as CI workflows, link campaigns or an exchange account.
- **Still open.** AQuA-RAT, CAMEL and TheoremQA provenance, and any authored lookup supplement.

The hash-bound v2 guide is unchanged. The versioned M3.5 collection brief will carry both rules. Macro-F1 stays the primary metric. It weights classes equally, so a 1.2-to-1 split changes per-class support but not the weighting of the headline score. With a 20% test partition, lookup would hold about 86 test rows.

## DataBench under the attached-table rule

[DataBench](https://huggingface.co/datasets/cardiffnlp/databench/tree/e75d53add267d2f9cfa32efd65ad77f0807adfad) (`e75d53a`, MIT, human-written questions over 80 tables) was earlier estimated only by regex. This screen judged a sample under the new rule.

The pool is every DataBench question whose unchanged text matched the discovery lane's generic-reference regex (301) plus its nine named-pattern hits, which were all generic on inspection: **310 questions over 69 tables**. The contract was saved before judging. A `random.Random(42)` shuffle fixed the order, and the first 30 were judged.

| Measure | Result |
| --- | --- |
| Eligible lookups | **29 of 30** (Wilson 95% 83.3% to 99.4%), measured |
| Held | 1: "properties listed" may mean real-estate listings rather than the table |
| Types | ordering-selection 11, existence-check 7, distinct-values 5, lookup-then-aggregate 2, category-counts 2, threshold-check 1, condition-filter 1 |
| Largest table in sample | 4 rows, exactly at the group cap |
| Rows after the four-per-table cap | 213 if every pool row passed; **about 209** at the sample rate (193 to 212 across the interval), inferred |

The earlier regex figure now has a judged basis. All 29 are non-keyed, so DataBench supplies exactly the types the audit found missing. The type mix stays well under the 40% cap at about 430 lookup rows.

## Further tool pools

A worker subagent screened two already-downloaded pools from the [lookup diversity](m3-5-lookup-diversity.md) investigation under the new rules. Contracts were saved before judging. Both pools continue saved seed-42 orders. Glaive was skipped because its focused pool yielded 0 of 120 on October 31.

- **ToolAlpaca, positions 121 to 240** of the focused order (937 rows).
- **ToolACE broad remainder.** The 1,279 broad-filter hits outside the 222 focused rows judged before, kept in saved order, first 120 judged.

| Pool | Judged | Eligible (Wilson 95%) | Keyed / non-keyed | Retained after duplicates and caps | Of which non-personal |
| --- | ---: | --- | --- | ---: | ---: |
| ToolAlpaca | 120 | 22 (12.4% to 26.2%) | 16 / 6 | 18 | 5 |
| ToolACE remainder | 120 | 23 (13.1% to 27.1%) | 20 / 3 | 20 | 13 (11 keyed) |

These counts are measured from the worker's verdicts. Three ToolAlpaca rows were near-duplicates of dataset-by-ID rows already in the inventory. Four rows fell into personal store kinds that are already full (email, bank). No row matched the parent release.

The lead spot-checked all 18 non-personal retained rows and holds seven. One bundles upcoming matches, which is live data. Five depend on third-party services or registries (Whois history, firmware security, a media catalogue, a patent register) that the October 31 screen held for tool scope. One gives a user ID with no identifiable source. That leaves **11 non-personal rows**, nearly all keyed.

The other 20 retained rows read the user's own accounts in third-party services, such as CI workflows, link-shortener campaigns, webhooks and crypto balances. The worker counts them as new personal store kinds. Altan decided on November 1 that these accounts count. Eleven of the 20 sit in firmly new kinds such as playlists, webhooks and CI pipelines. The other nine are borderline and may merge with existing kinds at review, for example an exchange account with the full bank-account group or followers with contacts. They enter the arithmetic as **11 to 20**.

Remainders are inferred from the sample rates. ToolACE's other 1,159 rows could hold about 126 non-personal rows (75 to 205) by the worker's verdicts, or about 77 after the lead's 11-of-18 rate. ToolAlpaca's other 697 rows hold about 29 (12 to 65), with no non-keyed rows in this sample.

## Lookup arithmetic for option B

| Component | Rows | Keyed / non-keyed | Basis |
| --- | ---: | --- | --- |
| Parent release | 100 | 40 / 60 | Accepted, measured |
| Integrated inventory | 46 | 35 / 11 | AI-screened, October 31 |
| DataBench | about 209 (193 to 212) | 0 / all | Judged sample, capped, inferred |
| Personal stores from CLINC150 and MASSIVE | 68 to 72 | about 18 / about 52 | Store kinds times four, inferred |
| Tool corpora from the discovery | 0 to 7 | 0 / up to 7 | Chained to other requests, likely to fail review |
| Today's tool-pool screen | 22 to 31 | mostly keyed | 11 non-personal after lead holds, plus 11 to 20 account rows, measured |
| **Total lookup class** | **about 430 to 470** | keyed about 25% | Before human review |

At the midpoint, about 450 lookup rows leave about 517 rows for each other class. Every request type stays under 40%. Keyed records sit near 25%, and ordering-selection, the largest DataBench type, near 20%. DataBench, the largest single source, would hold about 46% of the class, under the 75% cap.

Human review will remove some rows. If review kept 80% of each new source, which is a guess, lookup would land near 365 to 395, above the 350 floor. Option A's 500 remains a stretch goal. Judging about 300 more rows of the ToolACE remainder could plausibly add 15 to 50 non-personal rows, mostly keyed (inferred from the sample's Wilson range). With accounts counted, new service kinds there could add more, four rows per kind; the worker guessed 30 to 100 account rows across the whole unjudged remainder. The keyed cap allows about 75 more before it binds at 500.

## Risks

- **Label cues.** Most DataBench rows end with "in the dataset", and personal-store rows say "my". Either could become a lookup shortcut. The collection brief must look for retrieval and direct-answer rows that also mention a dataset or the user's own items, and validation errors should be read by source.
- **One judge.** All verdicts come from one model family with no second judgment. The repository's preferred worker model was unavailable. The worker and lead already disagree on 7 of 18 non-personal tool rows.
- **Account reads.** Counting third-party accounts assumes the router can reach the user's connected services. Some account reads, such as exchange balances or open positions, change continuously and may fail the live-data rule at review.
- **Generated tool text.** ToolACE and ToolAlpaca are generated corpora, and many kept rows bundle several lookups or use placeholder IDs such as 12345. Their wording may differ from human-written DataBench and CLINC150 text.
- **Attachments.** DataBench tables were not downloaded. Adoption needs the original tables at the pinned revision, kept outside router text. Datasets 066 to 080 come from the SemEval test release; the card states no test-only restriction, but the origin is disclosed.
- **Review load.** About 1,600 new rows need human review. The prepared timing pilot has not run, so the hours are unknown.

## Reproduction

All query text, contracts, orders and verdicts stay ignored under `work/m3-5-groups/option-b/`. From the repository root:

```bash
python3 -I work/m3-5-groups/option-b/databench/build.py "$PWD" "$PWD/work/m3-5-groups/option-b/databench"
```

```bash
python3 -I work/m3-5-groups/option-b/databench/judge.py "$PWD/work/m3-5-groups/option-b/databench"
```

`build.py` rewrites the contract, order and sample deterministically from the saved discovery pool. `judge.py` holds the recorded AI verdicts and writes `verdicts.jsonl` and `summary.json` with file hashes. A rerun of both scripts reproduced all five outputs byte for byte.

The tool-pool screen lives in `work/m3-5-groups/option-b/keyed/`: three contracts, the saved ToolACE remainder order, `verdicts.jsonl` (240 rows, null human labels, no adoption), `summary.json`, `notes.md`, `hashes.json` and the worker's scripts. `lead-review.json` lists the seven lead holds and their reasons.
