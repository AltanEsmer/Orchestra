# M3.5 dataset release

Started November 2, 2026, under the frozen [M3.5 collection brief](../collection-brief-m3-5.md) and Altan's November 2 decisions 6 and 7 recorded there. This note records the freeze, the collection and the release. The release `m3-5-v1` has **3,145 accepted rows**: the 400 M3 rows and 2,745 new ones. It is AI-labeled with human adjudication of disagreements; AI agreement is not human agreement.

## Freeze, November 2

Altan changed the review protocol and confirmed the size rule on November 2. A new row is accepted when the AI screen's label and an independent blind AI check agree and neither flags it. Altan adjudicates every disagreement, flag or abstention and does not label every row. The 12-case timing pilot was not run, because the change removes per-row human labeling. The release will be disclosed as AI-labeled with human adjudication of disagreements; AI agreement is not human agreement. Lookup takes every reviewed row that passes, up to 500 (floor 350), and the other three classes split the rest to 2,000.

The agent wrote both answers into the brief's Review and "Before freezing" sections, then froze it. Guide v3 is the v2 annotation guide plus the brief's "Guide v3" section, so the two hashes below bind it.

| File | SHA-256 |
| --- | --- |
| `docs/collection-brief-m3-5.md` (frozen) | `5320797319b1206f4e11acae5ec7e16f90ea2500b14e21cc0f882ff80957e50e` |
| `docs/annotation-guide.md` (v2 guide, unchanged) | `dd78162cbf9dcbdaaa68f4ad0bd654aec8d1ea181fb453362d9ab1dcdcc8ba55` |
| `data/processed/m3-v1.jsonl` (parent release) | `4e9425fd65e2572bff1c7fefd9ef21692bf219479818903d4ec33a372fc55bbf` |
| `data/raw/m3-reviews-v1.jsonl` (parent ledger) | `e56b73a22a0e95893fb19efcbde1717ae803fb52ffa0ce668cbceb384a3248e9` |
| `data/splits/m3-split.json` (parent split) | `6d48e18bae6ac319bffecc98c68b6b02c8c4483f68a75eddb63db2a52213225f` |

Existing pools and orders at the freeze, all ignored under `work/`:

| Pool or order | SHA-256 |
| --- | --- |
| `m3-5-groups/option-b/databench/order.jsonl` | `119f64d1d7cb2faa6d48e81d2535ee4f23944f7daf9b28369865586d5ce8eaab` |
| `m3-5-groups/option-b/databench/contract.json` | `a4d270ed8e5cac1cb0258a32c3a71e869c299e07f9a94cf61e29c2a06f45a5a6` |
| `m3-5-groups/discovery/intents/clinc150-lookup-pool.jsonl` | `c4adc41a286c655d9d4fed9341dadc06ad0968e4ffbdbe705074885c9d3051ba` |
| `m3-5-groups/discovery/intents/clinc150-lookup-order.json` | `3d7c1232cd2da34478e367ffadc5adfe86f040632d04905095443cb4d337d0e8` |
| `m3-5-groups/discovery/intents/massive-lookup-pool.jsonl` | `a3e47fc978735ca6ea2965e3918ef796dc89f4805dae27d9e00def88a5eea0c3` |
| `m3-5-groups/discovery/intents/massive-lookup-order.json` | `0e47eeb9e42594a7eb067d93f97ce08f66294da80b9777ef87ac1b5cc321d7b6` |
| `m3-5-groups/lookup/ToolACE-focused-order.jsonl` | `11cce71a19d144fac08e985b1889ddefdaed559926b20ad90deee347eddb3d59` |
| `m3-5-groups/option-b/keyed/ToolACE-remainder-order.jsonl` | `2fabd59fa5b2b78a6fdc2bfd3833eef34e6e606f388a4df7f26b70327eaed4fc` |
| `m3-5-groups/lookup/ToolAlpaca-focused-order.jsonl` | `015970cfcb420939988da76873294a20972ccb5f15c968d518c429d77a35a51c` |
| `m3-5-groups/option-b/keyed/Glaive-skip.json` | `2922c2e89afdaba63b5ecb895a5cd9f55683436ade91758a7578e6cf7f06dc2b` |
| `m3-5-groups/audit/integrated-inventory.jsonl` | `a4fa2da71a8328551a641b091f7f7140cd35871e8c54938d7e3d6b93138ca131` |
| `m3-5-groups/discovery/intents/clinc150-calc-pool.jsonl` | `581f59dbae9f1d63c696b08e14e0846a3f45b9c0b95b2dc7bc7ac4122666842f` |
| `m3-5-groups/discovery/intents/clinc150-calc-order.json` | `0dbae1ef2aad4d901f05f66c8087a94214584241b7cac9cd4219fe39afd7667f` |
| `m3-5-groups/discovery/intents/massive-calc-pool.jsonl` | `f7d79a394bd9a2de86f94623408140a453bd1d491ee076c24102a65d4bd246fc` |
| `m3-5-groups/discovery/intents/massive-calc-order.json` | `ced861c67c81de0f598375b905116053db01a05fbefd30f5fa2768c3ee96e270` |
| `m3-5-groups/discovery/prompts/theoremqa-pool.jsonl` | `b9e4fae5b96b3b2cb303d913fee0dc44bb471b87127debe0ddf639e6d8bc63d5` |
| `m3-5-groups/discovery/prompts/theoremqa-self-order.json` | `ba2486c7ace7a0411bce4b652740ef4c9a847b850c1f798121d79dddcc921f46` |
| `m3-5-groups/discovery/prompts/oasst2-calculation-pool.jsonl` | `6db4b46221276ef0bc4e44bc40cd94fd6cb6507c8cc8d2a6a6b31de4e78d20b6` |
| `m3-5-groups/discovery/prompts/oasst2-calc-focused-order.json` | `b65c50d1ecb1f865d8461c02a7b25467c9de2accbcacbb403be04bb7c0888e5d` |
| `m3-5-screen/existing/gsm8k_test-pool.jsonl` | `7fc84820167874b36a751a6da34f8b68cc605bc1b8e8653c704424b57d56e5df` |
| `m3-5-screen/existing/dolly_closed_qa-pool.jsonl` | `83e74359d4fdf6c1f90afe34cebcb13a8ce978dd921bb171dcd1696964f38691` |
| `m3-5-screen/existing/dolly_information_extraction-pool.jsonl` | `9e56e0303ae314dc6ff9521dd3e65fa673e77a68a563802120d8513505018611` |
| `m3-5-screen/existing/dolly_summarization-pool.jsonl` | `cf35f86ccbd88ab831303dc54965d10d1a13b23e3f5d8d997165b658bd2dc554` |
| `m3-5-screen/existing/no_robots_passage_train-pool.jsonl` | `f8e858d28336c69255e16649b3ebce4421da91608ed389b24ea4d8e6305d4933` |
| `m3-5-screen/existing/no_robots_direct_train-pool.jsonl` | `b0c8d1e5f664d773a2e3bf717eceb246b277ec1fc23dbcdad7a2cfe3ae0b77e6` |
| `m3-5-screen/existing/dolly_direct-pool.jsonl` | `0d62df76f7880f56ec8d413701688d0a3ae5fe24eb92011f4c06966363739c14` |

## Size change after freezing, November 2

After the first adjudication round, Altan asked for more data ("We can make rules less strict than before to even obtain more dataset as it is one of the most important") and then chose "Up to 1,000 per class" and "Keep all rules". The brief's new section "Change after freezing" records it as decision 8, replacing the 2,000 total; every quality rule stays. The amended brief's SHA-256 is `5f881f83df5ed6a96585a3788ca9bd8c568286bba2570bf9bc6b9bdae8163f92`; the frozen version above stays the reference for rows screened before the change.

The `m3-5-screen/existing` pools saved only a seed-42 sample, not a full order. Their full orders keep that sample first and add the rest in a seed-42 shuffle, as the M3 import did; they are built with the two new pools and hashed below before any review. The full hash list, including the samples, is in ignored `work/m3-5-dataset/freeze.json`, written by `work/m3-5-dataset/freeze_hashes.py`.

## New pools and orders

Built by ignored `work/m3-5-dataset/build_orders.py` with the tracked `seeded_order`, before any of their rows was screened. The contract was written first.

| File in `work/m3-5-dataset/orders/` | Rows | SHA-256 |
| --- | ---: | --- |
| `contract.json` | | `8aa13e06c011116a5267f18b5cb890b6682c87fa4324dbbe0d5f278ff6e481d3` |
| `clinc150-direct-pool.jsonl` and order | 748 | `6222942d…dd014dc`, `9c0c35ef…775518b9` |
| `massive-direct-pool.jsonl` and order | 1,229 | `1d35f9ef…ddce4`, `468c87cc…ff221` |
| `cue-order.json` (8 "dataset" and 80 "my" candidates) | 88 | `b22bc484fa364e36c69b95615be703b0723e16cc8c8497ee215872ce5e4261af` |
| Full orders for the seven sample-only pools (GSM8K, Dolly closed QA, extraction, summarization and direct, No Robots passage and direct) | | listed in ignored `orders/hashes.json` |

The direct-intent pools dropped 9 MASSIVE duplicates and 24 rows at token Jaccard 0.5 or more against M3 (2 CLINC150, 22 MASSIVE).

## Collection

Fifty screening batches drew **7,206 candidates** in brief order: lookup 2,706, retrieval 2,350, direct 1,150, calculation 1,000. Claude Sonnet 5.5 workers at medium effort screened them with `work/m3-5-dataset/prompts/screen.md` (`0a73369d…`). Forty-five blind sets, each at most 100 rows of one class, went to separate Claude Opus 5.5 agents at high effort with `prompts/blind.md` (`565ceca7…`) and the guide-v3 excerpt `prompts/guide-v3.md` (`fd39eda5…`). Each blind agent saw only blind IDs, query text and the attachment kind; the ID keys sat in a separate folder.

| Stage | Count |
| --- | ---: |
| Screened: eligible / held / excluded | 3,638 / 332 / 3,236 |
| Blind-checked (every eligible and held row with a listed source) | 3,828 |
| Same label from both checks | 3,676 (96.0%) |
| Blind judgments clear / ambiguous / exclude | 3,228 / 510 / 90 |
| Clear unflagged agreements on eligible rows | 3,094 |
| Sent to Altan: W1 / W2 / W3 | 422 / 301 / 4 |
| Accepted by Altan's answers: W1 / W2 / W3 | 240 / 107 / 0 |

Of the 734 blind-checked rows that were not clear agreements, 727 went to Altan; the other 7 could only have landed in classes that were already full, so they were recorded as target-reached without a decision. Of the 347 rows Altan's answers accepted, 274 entered the release; the rest found their group full, their class full or their type capped, or duplicated an earlier row.

Altan answered each worksheet by theme. W1: "Use suggested defaults", the agent's proposed default per theme. W2: "use same defaults", W3: "Use same defaults". So every adjudication applies a default the agent proposed; Altan did not decide rows one by one, and the anchoring risk is high. Each ledger rationale quotes the theme and Altan's words.

Final state of the 7,206 candidates:

| State | Rows |
| --- | ---: |
| Accepted into the release | 2,745 |
| Excluded by the screen | 3,236 |
| Excluded by Altan's adjudication | 380 |
| Labeled into a class whose listed sources exclude the corpus (for example a tool request labeled direct answer) | 142 |
| Group already full (four rows), after merges | 272 |
| Cap-held at the 40% request-type cap (document questions, word problems) | 282 |
| Class target reached | 130 |
| Router text duplicates an earlier row | 6 |
| Router text overlaps an M3 row at 0.5 or more | 13 |

Lookup ran first and walked every listed lookup pool, including 11 table and store-kind candidates that returned when slots freed. It ended at 483 before the size change and 494 after the last returning rows.

## Release

| Class | Rows (new) | Groups (new) | Sources | Largest request type | Words min / median / max |
| --- | --- | --- | --- | --- | --- |
| Document retrieval | 1,000 (900) | 982 (885) | No Robots 501, Dolly 490, Altan 9 | document question 400 (40.0%) | 2 / 15 / 85 |
| Knowledge lookup | 494 (394) | 223 (145) | DataBench 206, ToolACE 68, BFCL 62, ToolAlpaca 58, CLINC150 48, AI drafts 28, MASSIVE 14, Altan 10 | keyed record 105 (21%) | 5 / 13 / 54 |
| Calculation | 651 (551) | 562 (466) | GSM8K 255, CLINC150 117, TheoremQA 99, BFCL 82, MASSIVE 43, oasst2 37, Altan 9, Glaive 7, Dolly 2 | word problem 260 (39.9%) | 3 / 25 / 102 |
| Direct answer | 1,000 (900) | 960 (863) | No Robots 598, Dolly 267, MASSIVE 69, CLINC150 56, Altan 10 | factual question 245 (25%) | 2 / 15 / 1,026 |

Every class has at least two sources, none above 75%, and no request type above 40%. Lookup and calculation fall short of 1,000: every listed lookup pool was walked, and calculation's remaining supply is GSM8K word problems held by the 40% type cap. Per the brief, the agent reports the shortfall and switched no source.

Annotators: 2,471 new rows name only `ai-screen` (clear agreements); 274 name `ai-screen` and `A1` (Altan adjudicated); the 400 M3 rows keep `A1`. Attachments: 900 local passages (Dolly passages checked against their recorded hashes, No Robots passages split off by exact substring) and 206 pinned DataBench table references (path and LFS SHA-256 at `e75d53a`, from the file listing saved as `databench/tree.json`, `494d98cb…`). Lookup uses 72 store-kind groups; 46 new kinds were recorded under Altan's W1 default, with synonyms merged and listed in `work/m3-5-dataset/apply_w1.py`.

Cue counts by class over the whole release (test rows counted, never printed):

| Cue | Lookup | Calculation | Retrieval | Direct |
| --- | ---: | ---: | ---: | ---: |
| "dataset" | 195 | 1 | 0 | 5 |
| "in the dataset" | 186 | 0 | 0 | 0 |
| "my" | 112 | 13 | 12 | 101 |
| "table" | 15 | 5 | 2 | 3 |
| "database" | 30 | 0 | 0 | 0 |

"Dataset" remains almost a lookup-only cue, as Altan accepted on November 2: the cue search found five direct and no retrieval rows that use it. Error analysis must report rows with and without each cue.

## Groups and the close-pair hand check

Deterministic keys come first: a DataBench table, a Dolly passage hash, a number-swap skeleton, an earlier-inventory group. The screen proposed store kinds and template frames. The lead agent then decided all 1,673 new pairs at token Jaccard 0.5 or more among every candidate that could still be accepted, recorded in `work/m3-5-dataset/pairs.json` (`f0d0eed6…`). The decisions come from one written rule set with listed exceptions (`decide_all_pairs.py`), set after the agent read the pairs that attachment, label or source does not settle; this is a rule-based check, not a reading of every pair. 1,252 of these pairs remain among the accepted new rows, and `check-collection` confirms each is in one group or decided.

- **Join (381 pairs):** CLINC150 and MASSIVE template requests of the same kind; number swaps and problem templates in calculation across sources (for example TheoremQA seatings and Stirling-number variants); listed paraphrase or same-situation pairs; tool requests that differ in an ID.
- **Separate (1,292 pairs):** different first actions (44); different attached passages or tables (1,056, of which 874 are DataBench questions on different tables); CLINC150 or MASSIVE requests of different kinds (76); human-written prompts that share only a frame, following M3's precedent (107); and 9 listed frame-only or different-store pairs.

The joins became 161 group merges (`aliases.json`, `2107f812…`). A first round had joined human-written frame-only pairs too; the agent replaced it with this rule set before the freeze, and the first round is kept as `pairs-round1.json`. No pair needed Altan.

The parent-overlap check computed exact matches and Jaccard against all 400 M3 rows without printing them. It excluded 13 candidates at acceptance; 6 more duplicated an earlier row. They arise because the router sees only a passage row's short instruction, while the pools had been deduplicated on the full prompt with its passage. Store-kind overlap was read only on M3 training and validation lookups: some read a personal order, transactions or projects, but guide v2 kept those as separate groups because none names a shared source, so no new store row was excluded on that ground.

## Split

`python -m orchestra prepare-study --config configs/m3-5.json --review data/raw/m3-5-reviews-v1.jsonl --collection-brief docs/collection-brief-m3-5.md --out data/processed/m3-5-prepared.json` passed readiness and extended the M3 split from its pinned hash `6d48e18b…`. It allocated the 2,359 new groups alone with seed 42: 1,413 train, 473 validation, 473 test.

| Partition | Rows | Retrieval | Lookup | Calculation | Direct | Groups |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Train | 1,888 | 601 | 296 | 390 | 601 | 1,628 |
| Validation | 629 | 199 | 100 | 130 | 200 | 545 |
| Test (sealed) | 628 | 200 | 98 | 131 | 199 | 546 |

Proportions 0.600 / 0.200 / 0.200. Every M3 row keeps its partition.

## Checks

- `python -m orchestra check-collection --dataset data/processed/m3-5-v1.jsonl --parent data/processed/m3-v1.jsonl --types data/raw/m3-5-import/types.json --pairs data/raw/m3-5-import/pairs.json --out data/raw/m3-5-import/collection-check.json` printed `PASS: M3.5 collection checks`.
- `scripts/validate_dataset.py data/processed/m3-5-v1.jsonl --review data/raw/m3-5-reviews-v1.jsonl --ready` printed `PASS: M1 readiness checks passed (3145 accepted rows, 3145 reviewed)`. Its `ai_consistency` of 3,143 of 3,145 counts accepted rows only, after disagreements were adjudicated, so it is not an agreement rate; use the 96.0% above.
- All 50 screen outputs and 45 blind outputs passed `pipeline.py verify` (cids, keys, allowed values, exact passage splits).

## Disclosures and limitations

- **AI labels.** New rows are AI-labeled. Both checks are Claude models, so shared-model bias remains. Only the blind check was source-blind: the screen saw each row's source, stream, the class it was drawn for, any upstream intent, and per-stream label guidance. Altan adjudicated by adopting agent-proposed theme defaults.
- **Rows excluded on the screen label alone.** 142 rows (oasst2 70, ToolACE 59, ToolAlpaca 12, TheoremQA 1) were labeled into a class whose listed sources exclude their corpus and were skipped without a blind check or Altan. 19 of them were held, and the brief sends held rows to Altan; 18 of those were labeled direct answer and 1 calculation. This is a deviation from the brief.
- **Length cue.** Direct-answer rows keep supplied text inline (up to 1,026 words), while retrieval rows lose their passage to the attachment (up to 85 words). Query length could become a shortcut; error analysis should report it.
- **Tokenizer.** The overlap tokenizer keeps only ASCII letters, digits and apostrophes, as in the discovery lanes, so close pairs in accented or non-Latin text can be missed.
- **Size change after freezing.** Decision 8 replaced the 2,000 total after lookup was walked; the classes end unequal (494 to 1,000).
- **Screening shortcuts.** Screens were templated and fast. Two tool screens (L11, L17) judged long multi-part requests from their first 300 to 400 characters; 18 L11 exclusions rest on that.
- **Shared scratch folder.** Early parallel agents shared one scratch folder and overwrote each other's helper scripts; one stray verdict file appeared and was replaced by its owner. All outputs then matched their own agents' counts and stream label mixes. Later agents used separate folders. Several blind agents listed their own input folder before reading, which showed only a task file, never a key.
- **Exposure.** The lead agent read candidate texts while checking screens and pairs. No selection used M2 or M3 validation errors.
- **Attachments.** DataBench tables were not downloaded; their Kaggle-derived terms are unreviewed. No table content enters the study.
- **Not checked.** No human read every accepted row. Semantic label errors remain possible, especially where the source hints at a label.

## Local files

All ignored. `data/processed/m3-5-v1.jsonl` `be747dda8fd9f7c2ee432fa4ab29d6577607212b4d5a678d82205fef3386b2a8`; `data/raw/m3-5-reviews-v1.jsonl` `326d63b5ce02514751ccfd57edc751dbc1c684ad1187827bd2728f5026cba51f`; `data/raw/m3-5-import/attachments.jsonl` `1dec7804…`, `provenance.jsonl` `71434785…`, `skipped.jsonl` `61211edd…`, `types.json` `9c9ecede…`, `pairs.json` `6d976d4c…`, `collection-check.json` `e5403b28…`; `work/m3-5-dataset/adjudications.jsonl` `0029af67…`; `data/processed/m3-5-prepared.json` `352cb7f7…`. Tracked: `data/splits/m3-5-split.json` `7aacbc497dd462e56a5fbcb3b5546c056ed4f835e35d0cf61334f17ce3a45e10`.

The driver is `work/m3-5-dataset/pipeline.py` (draw, blind sets, verification, the acceptance derivation and worksheets) with `release.py`, `apply_w1.py`, `apply_w2.py` and `decide_all_pairs.py`. `release.py` refuses to overwrite and refuses while any row awaits a decision.
