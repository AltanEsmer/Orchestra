# Collection brief for M3.5

Draft prepared November 1, 2026. **Frozen November 2, 2026**, after Altan answered decisions 1 to 7 at the end. Its SHA-256 and guide v3's are recorded in the [M3.5 dataset record](evidence/m3-5-dataset.md) before any row is imported. Document later changes before collecting affected rows. The October 26 [M3 brief](collection-brief.md) stays unchanged and hash-bound. **Guide v3** means the v2 [annotation guide](annotation-guide.md) plus the "Guide v3" section below; the frozen brief's hash binds both. This draft contains no research query rows.

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

Token overlap is token-set Jaccard over `re.findall(r"[a-z0-9']+", text.casefold())`, as in the discovery lanes. The lead agent hand-checks every new pair at 0.5 or more and records whether the rows share a group; a pair it cannot settle goes to Altan. The parent-overlap check reads M3 training and validation rows. Sealed test rows enter only computed checks (exact match and Jaccard), never printed, as in the affected-row check.

## Pools, order and caps

**Pools.** Each source's candidates come from its saved screening pool and seed-42 order: DataBench in `work/m3-5-groups/option-b/databench/`; ToolACE, ToolAlpaca and Glaive in `work/m3-5-groups/lookup/` and `work/m3-5-groups/option-b/keyed/`; CLINC150, MASSIVE, oasst2 and TheoremQA in `work/m3-5-groups/discovery/`; Dolly, No Robots and GSM8K in `work/m3-5-screen/existing/`. Pools that do not exist yet, the CLINC150/MASSIVE direct intents and the cue candidates below, are built and their orders saved before any of their rows is reviewed. Pool and order hashes are recorded when the brief is frozen, and for the two new pools when they are built.

The two new pools follow the discovery lanes' contract: unchanged text, normalized exact duplicates dropped, token-set Jaccard 0.5 or more against any M3 row dropped (computed, never printed), then a `random.Random(42)` order.

- **Direct intents.** CLINC150 `definition`, `translate`, `tell_joke`, `fun_fact` and `spelling` (train, val and test splits; out-of-scope splits excluded), and MASSIVE en-US `qa_definition`, `general_joke` and `qa_factoid`. Each corpus keeps its own order; the stream alternates them.
- **Cue candidates.** The eight "dataset" rows in the Dolly and No Robots pools and the 80 No Robots passage prompts with "my", by the regexes in `cues.py`. Accepted rows count toward their class and source as usual.

Store-kind candidates alternate the CLINC150 and MASSIVE lookup orders. Tool candidates rotate ToolACE (its focused order, then the remainder order), ToolAlpaca's focused order and the six Glaive lookups of the earlier inventory; Glaive's focused pool stays skipped (0 of 120 on October 31). The calculation "earlier inventory" is the 49 provisional rows of `work/m3-5-groups/audit/integrated-inventory.jsonl` from adopted sources (GSM8K 30, Glaive 10, BFCL 7, Dolly 2), in inventory order; its Math Stack Exchange and synthetic-benchmark rows stay excluded. A candidate already reached through another pool is skipped as a duplicate.

**Interleaving.** Within a class, fill each batch from the sources in the ratios below, taking the next candidates in each source's order:

- **Lookup.** Every eligible candidate, since supply is below 500. Interleave DataBench, store kinds and tool corpora about 3 : 1 : 1, so keyed records stay under 40%.
- **Calculation.** CLINC150, TheoremQA, MASSIVE, oasst2 and the earlier inventory in proportion to their estimated supply (about 168 : 112 : 65 : 52 : 49). New GSM8K word problems come in only once those run out or are cap-held.
- **Retrieval.** Two Dolly rows per No Robots row. Within Dolly, alternate closed QA with extraction and summarization so document questions stay under 40%.
- **Direct.** Two No Robots rows per Dolly row, plus CLINC150/MASSIVE direct rows as their screen finds them, within group caps. The direct-intent stream is drawn at one candidate per Dolly candidate.

Ratios are applied to candidates drawn for screening, by a deterministic smooth weighted round robin. A batch is at most 100 eligible or held candidates of one class sent together to the blind check.

**Cap holds.** M3 already sits at several limits: keyed lookups (40 of 100), BFCL in calculation (75), Dolly in retrieval (75), No Robots in direct answers (75) and document questions (40). A candidate that passes review but would push a cumulative share over its cap is held as `cap-hold`, neither accepted nor rejected. It returns first when later rows make room. A temporarily over-cap batch is never accepted. A candidate whose group already holds four accepted or pending rows is skipped as `group-full`, before screening when its group is known in advance (a table, an intent's store kind, a number-swap skeleton); it returns in order if one of those rows fails review.

**Stop rule.**

1. **Lookup first.** Work through the lookup pools until 500 lookups are accepted in total or the pools are exhausted. That count fixes the lookup size. Below 350, stop. Altan then chooses among a smaller lookup class (a more imbalanced release), an authored supplement, further sources or a contract change.
2. **Then the other classes**, with targets from the table above. Calculation goes next, then retrieval and direct answer. Stop at the target. If a source is exhausted, continue with the class's other listed sources. If all are exhausted, report the shortfall; the agent does not switch sources on its own.
3. **No targeting.** Do not select, collect or relabel rows to address mistakes seen in M2 or M3 validation errors. Disclose collection exposure; sealing restricts model access only.

## Review

**Protocol change, November 2.** Before freezing, Altan replaced per-row human labeling. A new row is accepted when the AI screen's label and an independent blind AI check agree and neither flags it. Altan adjudicates every disagreement, flag or abstention. Altan does not label every row. The 12-case timing pilot is not run, because the change removes per-row human labeling; Altan's workload is the adjudications.

**Two stages.**

1. **Screen.** A Claude Sonnet 5.5 worker at medium effort applies this brief to each pool in order. It records eligible, held and excluded candidates. For each eligible or held candidate it proposes a label, request type, group key and one-sentence rationale. Its exclusions are recorded with reasons and counted; they get no further review.
2. **Blind check.** A separate Claude Opus 5.5 agent at high effort reviews every eligible and held candidate. It sees guide v3, the query text and whether a passage or table is attached. It never sees the source, pool, screen label or rationale.

A candidate is accepted when the screen marked it eligible, both labels agree, the blind check judged it clear and neither flagged it, and the batch passes the cumulative checks and cap holds above. Every disagreement, flag, hold or abstention goes to Altan with both labels and rationales. Only Altan's actual answers are recorded.

In the review ledger, `original_label` is the screen's label and `review_label` the blind check's. A new row's `annotator_ids` name the screen (`ai-screen`), plus `A1` where Altan adjudicated. The screen's model, prompt, input and output hashes go in the import provenance.

Screening verdicts are not labels. Disclose that the release is AI-labeled with human adjudication of disagreements. AI agreement is not human agreement: both checks come from one model family, so shared-model bias remains. A pool's source still hints at a label, and Altan sees the screen's proposal when adjudicating, which carries an anchoring risk. Record exclusions and unresolved boundaries.

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

Altan's further answers on November 2:

6. **Review protocol.** Accept a new row when the AI screen's label and an independent blind AI check agree and neither flags it. Altan adjudicates every disagreement, flag or abstention and does not label every row. The timing pilot is not run, because this change removes per-row human labeling. Disclose the release as AI-labeled with human adjudication of disagreements; AI agreement is not human agreement.
7. **Size.** Keep option B as written: lookup takes every reviewed row that passes, up to 500 (floor 350), and the other three classes split the rest to 2,000 in total, per the target table and stop rule. Do not collect past the targets.

With these answers the brief is frozen. Next: record its hash, add the source-manifest entries, then build the new pools, the import adapters and the M3.5 count and batch checks.

## Change after freezing, November 2

The frozen brief's SHA-256 was `5320797319b1206f4e11acae5ec7e16f90ea2500b14e21cc0f882ff80957e50e`. After Altan adjudicated the first worksheet, lookup stood at 483 accepted rows with all its pools screened. Altan then wrote: "We can make rules less strict than before to even obtain more dataset as it is one of the most important." Asked which rules, Altan chose **"Up to 1,000 per class"** and **"Keep all rules"**.

8. **Size, replacing decision 7.** Every class takes each reviewed row that passes, up to 1,000 rows in total including M3's 100, until its listed sources run out. This replaces the 2,000 total, the target table and step 2 of the stop rule's targets. Lookup keeps its floor of 350. The four-row group cap, the 75% source and 40% request-type caps, the guide v3 boundaries, the sources, the interleaving and the review protocol all stay as frozen. Rows are still drawn in pool order, and no new source, AI draft or synthetic row is added. Classes may end unequal; report actual counts.

The agent recorded this section before drawing any row that the old targets would have stopped. Rows screened earlier under the 2,000 design keep their decisions.
