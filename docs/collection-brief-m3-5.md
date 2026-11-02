# Collection brief for M3.5

Draft prepared November 1, 2026. **Not frozen.** Altan answered decisions 1 to 5 on November 2, 2026; the timing pilot and the affected-row check at the end remain before freezing. Once frozen, record this file's hash before importing any row, and document later changes before collecting affected rows. The October 26 [M3 brief](collection-brief.md) stays unchanged and hash-bound. **Guide v3** means the v2 [annotation guide](annotation-guide.md) plus the "Guide v3" section below; the frozen brief's hash binds both. This draft contains no research query rows.

## What M3.5 adds

The frozen M3 release (`data/processed/m3-v1.jsonl`, 400 rows, 360 groups) keeps its text, labels, groups and split memberships. M3.5 extends it to a new release, `m3-5-v1`, under the [M3.5 plan](m3-5-plan.md).

The target is Altan's near-balanced design from November 1 ([option B](evidence/m3-5-option-b-supply.md)): **2,000 accepted rows**. Lookup keeps every reviewed row that passes, up to 500 in total including M3's 100 lookups, with a floor of 350. The other three classes split the rest evenly. A remainder row goes first to direct answer, then to document retrieval. Every case needs 1,600 newly accepted rows.

| Lookup rows | Calculation / retrieval / direct | Lookup source cap / type cap | Other classes' source cap / type cap |
| ---: | --- | --- | --- |
| 350 | 550 / 550 / 550 | 262 / 140 | 412 / 220 |
| 400 | 533 / 533 / 534 | 300 / 160 | 399 or 400 / 213 |
| 450 | 516 / 517 / 517 | 337 / 180 | 387 / 206 |
| 500 | 500 / 500 / 500 | 375 / 200 | 375 / 200 |

Caps are the guide's limits rounded down: no source above 75% of a class, no request type above 40%. These are collection targets, not results. If a class falls short, keep the sealed test and report the shortfall instead of inventing data. Do not silently lower the minimum or start M4.

## Sources

Collect from these sources only. Before import, each needs a `data/manifests/sources.json` entry with the fields the [protocol](data-and-evaluation.md) requires: source URL, download date, revision or hash, license, permitted redistribution and mapping rationale. Keep public text exactly as written; skip a row rather than edit it. Source task or intent labels are never Orchestra labels.

| Source | Revision, license, redistribution | Origin | Router input; main exclusions | Status |
| --- | --- | --- | --- | --- |
| Altan-authored, AI drafts | M3 records | Altan; disclosed local drafts | Query text | Adopted in M3; no new drafts |
| [Dolly 15k](https://huggingface.co/datasets/databricks/databricks-dolly-15k/tree/bdd27f4d94b9c1f951818a7da7fd7aeea5dbff1a) | `bdd27f4`; CC BY-SA 3.0; attribution, share-alike | Databricks employees | Instruction; passage as linked attachment. Exclude passage tasks whose instruction never mentions the passage | Adopted |
| [No Robots](https://huggingface.co/datasets/HuggingFaceH4/no_robots/tree/e6f9a4ac5c37faeb744ba9ecf0473184d7f8105b) | `e6f9a4a`; CC BY-NC 4.0; attribution, non-commercial | Human annotators | First user prompt; passage split off by exact substring. Exclude multi-turn, placeholders, figure-dependent prompts | Adopted |
| [BFCL v3](evidence/bfcl-compatibility.md) | `61fc060`; Apache-2.0 | Benchmark authors | User text only. Exclude live, write and missing-input requests | Adopted; fully screened |
| GSM8K | `740312ad`; MIT | Human-written | Question only; no solution | Adopted |
| [CLINC150](https://github.com/clinc/oos-eval/tree/828f8093932c8fe6ca7936c3d2e52903b1c523de) | `828f809`; CC BY 3.0 Unported; attribution | Crowd workers | Utterance text; intent used only to select pools. Exclude out-of-scope rows and write or live intents | Adopted November 2; manifest entry pending |
| [MASSIVE en-US 1.1](https://github.com/alexa/massive/tree/f966f21846043aabef9b0f974fa7970027f43738) | repo `f966f21`; CC BY 4.0; attribution, cite SLURP | Crowd workers | `utt` only, never `annot_utt`, scenario or worker ID. Exclude social, takeaway, music, news, weather, stock and currency intents | Adopted November 2; manifest entry pending |
| [OpenAssistant oasst2](https://huggingface.co/datasets/OpenAssistant/oasst2/tree/179dd21fc55192153d94adb0e0ce8f69e222bf75) | `179dd21`; Apache-2.0 | Volunteers | First user message only. Exclude prompts with personal details | Adopted November 2; manifest entry pending |
| [TheoremQA](https://huggingface.co/datasets/TIGER-Lab/TheoremQA/tree/a340b1782960a712843aae3ed25f1e013cc008a5), author-written rows | `a340b17`; MIT | The authors | Question only; no answer or theorem | Adopted November 2; manifest entry pending |
| [DataBench](https://huggingface.co/datasets/cardiffnlp/databench/tree/e75d53add267d2f9cfa32efd65ad77f0807adfad) | `e75d53a`; MIT | Human-written; datasets 066 to 080 come from the SemEval 2025 test release | Question only; table as attachment (guide v3). Exclude questions with no table reference, modeling and transformation | Adopted November 2; manifest entry pending |
| [ToolACE](https://huggingface.co/datasets/Team-ACE/ToolACE/tree/6bda777c88d21e5a204703c1ee45597a8fa4f734), [ToolAlpaca](https://github.com/tangqiaoyu/ToolAlpaca/tree/189069998d64a7baf1b4a1c3c4b2e75eb9d05532), [Glaive v2](https://huggingface.co/datasets/glaiveai/glaive-function-calling-v2/tree/e7f4b6456019f5d8bcb991ef0dd67d8ff23221ac) | `6bda777`, `1890699`, `e7f4b64`; Apache-2.0 | Generated | First user turn only; never tool definitions. Exclude live, write and third-party catalogue requests held for tool scope | Adopted November 2; manifest entry pending |
| AQuA-RAT, CAMEL physics, Math Stack Exchange, the synthetic calculation benchmark, TheoremQA's externally sourced rows | See the [discovery](evidence/m3-5-source-discovery.md) and [audit](evidence/m3-5-group-quota-audit.md) | Mixed | Question only | Excluded November 2 |

Excluded: MathQA (tokenized copy of AQuA), MATH, text-to-SQL and table benchmarks other than DataBench, hidden tool-catalog names, and real-user chat logs such as WildChat. Adding any other corpus needs Altan's adoption and a recorded change to this brief.

Known duplicate risks: at least ten number-swap patterns recur in both CLINC150 and MASSIVE; one CLINC150 row swaps numbers in the protocol's own teaching example; one oasst2 row repeats a GSM8K problem; MASSIVE shares utterances with SLURP and HWU64, which are not collected separately; DataBench questions repeat templates within a table; tool rows reuse placeholder IDs such as 12345. Full per-source fields, samples and holds are in the linked evidence notes.

Indicative per-class plan at about 450 lookups. Supply figures are AI screening estimates before human review:

| Class | From M3 | New supply before review | Groups | Main constraint |
| --- | --- | --- | --- | --- |
| Lookup | BFCL 62, AI drafts 28, Altan 10 | DataBench about 209 (inferred); CLINC150/MASSIVE stores 68 to 72 (inferred); ToolACE, ToolAlpaca, Glaive about 70 to 80 (measured screens) | 69 tables; 17 to 18 store kinds plus up to 15 new | Total supply; floor 350 |
| Calculation | BFCL 75, GSM8K 16, Altan 9 | CLINC150 about 168, MASSIVE about 65, oasst2 about 52 (inferred); TheoremQA about 112 (guess); earlier inventory about 49; GSM8K word problems fill the remainder | TheoremQA 70 to 100 (guess); CLINC150/MASSIVE by number-swap pattern | Word problems at most 40%; arithmetic about 161 |
| Retrieval | Dolly 75, No Robots 16, Altan 9 | Dolly closed QA and extraction; No Robots passage prompts about 521 (inferred) | One per passage or scenario | Dolly at most 75%; document questions at most 40% |
| Direct | No Robots 75, Dolly 15, Altan 10 | No Robots and Dolly direct pools, thousands (inferred); CLINC150/MASSIVE direct intents, not yet screened | One per scenario | No Robots at most 75% |

## Guide v3: two lookup rules

Guide v2's label boundaries and grouping stay in force, with two additions for M3.5 rows. New rows record `annotation_version` as `guide-v3`. M3 rows keep their v2 labels; a correction would need a separate release decision.

1. **Attached table.** A question that refers to its own table generically ("in the dataset", "the table") counts as naming a structured source when the original table is kept as an attachment outside router text. If it asks to read, filter, order, count or check records, the first action is `knowledge_lookup`. Without an attachment, the old "missing context" rule applies. An attached prose passage stays `document_retrieval`.
2. **Personal stores.** A query that reads the user's own records in a named kind of store is `knowledge_lookup`. Writes and actions (send, book, delete) are not lookups. As in guide v2, a request is excluded as live only when it needs live or external information that no tool provides, such as a market price or news. A status stored in a record the user can read, like an order's status by ID, stays a lookup, matching accepted M3 rows. Flag unclear cases. Public utterances of any recorded origin qualify (crowd, volunteer or generated, disclosed as such). Real users' personal queries stay excluded.

**Store kinds** are functions, not brands: all calendars are one kind, all CI pipelines another. The starting list is frozen with this brief. It holds the 14 CLINC150 and 5 MASSIVE kinds in the discovery's intents record (shared kinds such as calendars merge, giving 17 or 18), and the tool screen's 10 new kinds: playlists, chat rooms, CI pipelines, code repository, link campaigns, projects, SMS account, webhooks, website analytics and workspace users. On November 2 Altan merged the five borderline kinds into existing ones: brokerage account into bank account, social connections into contacts, saved collections into lists, merchant sales into transactions, and facility maintenance into maintenance records. Altan records any further kind in the review ledger before rows from it are accepted.

**Attachments.** For DataBench, Altan chose references on November 2 rather than downloading the tables. Record each table's pinned path and LFS SHA-256 instead of a local copy. That departs from the Dolly adapter's local attachment file and must be disclosed. The router never reads the table and the study computes no answers. Sizes from the Hugging Face file listing at `e75d53a`, read November 1: 80 full tables, 373.8 MB; 80 sample tables, 6.2 MB.

**Affected M3 rows.** The guide requires reviewing rows a new version could affect. On November 2 the agent checked the 41 M3 training and validation rows that contain "my", "dataset", "table" or "database" (28 training, 13 validation; 29 lookups, 6 calculations, 5 direct answers, 1 retrieval). Guide v3 changes none of their labels. Lookups stay lookups. The other twelve use "my" without reading a store, and one mentions "my dataset" without an attached table while giving every number. The check also found that the draft's live-status wording would have excluded three accepted lookups that read an order or complaint status by ID (q0068, q0069, q0215), so rule 2 now follows guide v2's live rule. Verdicts are in ignored `work/m3-5-groups/option-b/brief/affected-rows.json`. Test rows stay sealed and unchecked; that is a recorded deviation.

## Groups and batch checks

Group under guide v2, with these M3.5 specifics:

- **Each DataBench table is one group.** At most four questions per table.
- **Each store kind is one group across all sources.** CLINC150, MASSIVE and the tool corpora share these groups.
- **Number swaps join across sources**, including the patterns shared by CLINC150 and MASSIVE.
- **Parent overlap.** A candidate that would share a group with an M3 row under guide v2's four rules (variation, named source or setting, situation, public record) is excluded, not given a new group.

Every batch of at most 100 rows passes the cumulative checks before acceptance: no exact duplicates; a hand check of pairs at 0.5 token overlap or more; at most four rows per group; at least two sources per class with none above 75%; no request type above 40%. Each class needs at least five new groups. These checks apply to the cumulative release, not just the batch.

## Pools, order and caps

**Pools.** Each source's candidates come from its saved screening pool and seed-42 order: DataBench in `work/m3-5-groups/option-b/databench/`; ToolACE, ToolAlpaca and Glaive in `work/m3-5-groups/lookup/` and `work/m3-5-groups/option-b/keyed/`; CLINC150, MASSIVE, oasst2 and TheoremQA in `work/m3-5-groups/discovery/`; Dolly, No Robots and GSM8K in `work/m3-5-screen/existing/`. Pools that do not exist yet, the CLINC150/MASSIVE direct intents and the cue candidates below, are built and their orders saved before any of their rows is reviewed. Pool and order hashes are recorded when the brief is frozen.

**Interleaving.** Within a class, fill each batch from the sources in the ratios below, taking the next candidates in each source's order:

- **Lookup.** Every eligible candidate, since supply is below 500. Interleave DataBench, store kinds and tool corpora about 3 : 1 : 1, so keyed records stay under 40%.
- **Calculation.** CLINC150, TheoremQA, MASSIVE, oasst2 and the earlier inventory in proportion to their estimated supply (about 168 : 112 : 65 : 52 : 49). New GSM8K word problems come in only once those run out or are cap-held.
- **Retrieval.** Two Dolly rows per No Robots row. Within Dolly, alternate closed QA with extraction and summarization so document questions stay under 40%.
- **Direct.** Two No Robots rows per Dolly row, plus CLINC150/MASSIVE direct rows as their screen finds them, within group caps.

**Cap holds.** M3 already sits at several limits: keyed lookups (40 of 100), BFCL in calculation (75), Dolly in retrieval (75), No Robots in direct answers (75) and document questions (40). A candidate that passes review but would push a cumulative share over its cap is held as `cap-hold`, neither accepted nor rejected. It returns first when later rows make room. A temporarily over-cap batch is never accepted.

**Stop rule.**

1. **Lookup first.** Work through the lookup pools until 500 lookups are accepted in total or the pools are exhausted. That count fixes the lookup size. Below 350, stop. Altan then chooses among a smaller lookup class (a more imbalanced release), an authored supplement, further sources or a contract change.
2. **Then the other classes**, with targets from the table above. Calculation goes next, then retrieval and direct answer. Stop at the target. If a source is exhausted, continue with the class's other listed sources. If all are exhausted, report the shortfall; the agent does not switch sources on its own.
3. **No targeting.** Do not select, collect or relabel rows to address mistakes seen in M2 or M3 validation errors. Disclose collection exposure; sealing restricts model access only.

## Review

**Timing pilot first.** Run the prepared 12-case pilot (`work/m3-5-screen/existing/human-pilot.md`) before collecting, by November 3 if the schedule holds. The workload is minutes per candidate times candidates reviewed, plus adjudication time. Candidates reviewed exceed the 1,600 accepted rows by the share Altan rejects, which is unknown until the first batch. The pilot's twelve hand-picked cases cannot estimate that yield. Re-estimate after the first batch of 100 and label the estimate inferred. If it does not fit the November 12 target, Altan decides scope or schedule.

**Two stages.** First, the AI screen applies this brief to each pool in order and records eligible, held and excluded candidates, as the discovery screens did. Second, Altan reviews every eligible and held candidate in the same order, using the M3 method:

- Altan records the primary label and rationale for every new row, without seeing the screen's proposed label.
- A blind AI check reviews every new row. It sees guide v3, the query text, and whether a passage or table is attached.
- Clear, unflagged agreements are accepted. Every flag, abstention or disagreement needs Altan's adjudication.

Screening verdicts are not labels. A pool's source still hints at a label; disclose that, along with the facts that AI consistency is not human agreement and that approving agent proposals carries an anchoring risk. Record exclusions and unresolved boundaries.

## Known cues to inspect

Counts by whole-word regex, from `work/m3-5-groups/option-b/brief/cues.py` (results in `cues.json`). They do not show that a classifier relies on them. M3 test rows are counted but never printed.

| Cue | M3 release (100 rows per class) | Candidate pools |
| --- | --- | --- |
| "table" | 14 lookups | No Robots direct 36 of 7,827 |
| "database" | 14 lookups | DataBench 7 of 310 |
| "dataset" | 1 calculation | DataBench 276 of 310; Dolly and No Robots 8 in total |
| "my" | lookup 11, direct 10, calculation 6, retrieval 1 | No Robots direct 1,241 of 7,827; No Robots passage 80 of 823; Dolly direct 181 of 5,797 |

A substring match for "table", which the M1 brief's count may have used, also finds one retrieval and one calculation row. "My" is common in direct-answer requests, so drawing direct rows in proportion should dilute it. "Dataset" is the opposite. About 186 of the roughly 209 DataBench rows would carry it, against at most 8 candidates elsewhere. On November 2 Altan accepted the cue without capping DataBench, with these required responses:

- Judge the eight "dataset" candidates in Dolly and No Robots, and the 80 No Robots passage prompts with "my", and keep any that qualify as retrieval or direct answers.
- Screen CLINC150 and MASSIVE direct-answer intents (definitions, translations, jokes), so those corpora do not supply only calculation and lookup.
- After collection, report cue counts by class. During validation error analysis, report errors on rows with and without each cue, and by source.

After collection, the agent measures class and group counts, word lengths, source mix, request-type spread, agreement and exclusions. This brief cannot guarantee natural user language or real-world routing performance.

## What not to do

Do not change M3 rows, groups or partitions. Do not rewrite public text, append hidden metadata or tool definitions, or use a source's intent or task label as an Orchestra label. Do not open the sealed test. Do not add a synthetic top-up.

## Before freezing

On November 2, Altan answered "Accept all five" to the recommended answers:

1. **Sources.** CLINC150, MASSIVE, oasst2, TheoremQA's author-written rows, DataBench and the three tool corpora are adopted as listed.
2. **Calculation provenance.** AQuA-RAT, CAMEL physics, Math Stack Exchange, the synthetic benchmark and TheoremQA's externally sourced rows stay excluded. Reopening them needs a recorded change to this brief.
3. **The "dataset" cue.** Accepted with the responses above; DataBench is not capped.
4. **DataBench attachments.** Pinned table references, no download.
5. **Borderline store kinds.** All five merge into existing kinds, as listed under guide v3.

Done on November 2: the affected-row check under guide v3 (no label changes; live-status wording aligned with guide v2).

Still open:

6. **Timing pilot.** Altan runs it and confirms the schedule from its result. After approval: record the brief's hash, add the source-manifest entries, then build the import adapters and the M3.5 count and batch checks. None of that implementation exists yet.
