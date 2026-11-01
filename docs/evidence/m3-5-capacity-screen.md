# M3.5 public-data capacity screen

October 31, 2026. Altan authorized finding and screening more public data, aiming for **4,000 accepted queries with 2,500 as the minimum**. M3.5 is now in progress. The frozen release still contains **400 accepted rows, 100 per class**. This work adds screening evidence, not accepted rows, a collection release, or model results.

**Direct-answer and document-retrieval capacity looks promising; lookup and calculation diversity remain unresolved.** Source size is not usable capacity. New-source results, including unsuccessful leads, are in the [lookup investigation](m3-5-lookup-screen.md). The minimum and preferred targets remain unchanged. No full collection brief or source quota is frozen while the joint capacity gate is unresolved. Across the existing-source and new-source screens, 630 formal sample decisions were recorded over seven corpora; overlapping selections and duplicate strings mean this is not 630 unique queries. The xLAM lead was access-gated and contributes zero sampled rows.

## Existing sources: measured fresh samples

Reused the exact Dolly file, GSM8K question-only export and remaining BFCL calculation pool from the earlier screen. Downloaded the previously unused **No Robots training split**, at the already documented repository revision. This expands screening beyond the earlier test-only inspection; it does not silently amend the old collection brief's import scope.

| Source | Revision and permission evidence | Input used |
| --- | --- | --- |
| [Dolly, author card](https://huggingface.co/datasets/databricks/databricks-dolly-15k/blob/bdd27f4d94b9c1f951818a7da7fd7aeea5dbff1a/README.md) | `bdd27f4d94b9c1f951818a7da7fd7aeea5dbff1a`; CC BY-SA 3.0, employee-written instructions; retain Databricks/Wikipedia attribution and applicable share-alike terms. | Instruction only; existing linked-passage adapter for explicit passage requests. |
| [No Robots, author card](https://huggingface.co/datasets/HuggingFaceH4/no_robots/blob/e6f9a4ac5c37faeb744ba9ecf0473184d7f8105b/README.md) | `e6f9a4ac5c37faeb744ba9ecf0473184d7f8105b`; CC BY-NC 4.0, human-written; non-commercial use and attribution. Newly downloaded train file: 9,500 rows, 10,474,682 bytes; SHA-256 verified against upstream LFS metadata. | Single user/assistant conversation only; user prompt, never the answer. Passage requests require an exact instruction substring and retained original attachment. |
| [GSM8K, pinned card](https://huggingface.co/datasets/openai/gsm8k/blob/740312add88f781978c0658806c59bc2815b9866/README.md) | `740312add88f781978c0658806c59bc2815b9866`; MIT, human-created problems; retain OpenAI notice. Existing test questions only; no new train download. | Question column only; no solution or numeric answer inspected. |
| [BFCL source record](m3-capacity-screen.md) | Existing adopted revision `61fc0608cfd831fcfbbaa676ebdfef0ed963eeda`, Apache-2.0. Reused historical math-function-filtered pool with its upstream lineage. | User text only for fresh judgments; upstream function-name filtering makes this a selected pool, not a representative BFCL sample. |

The repository MIT license does not replace these source terms. Retain attachments and attribution separately if adopted into the next release. ToolACE and Glaive are public generated-language sources, unlike the human-written sources above; public availability does not establish natural traffic or independent human authorship. See the linked new-source note for its precise provenance limits.

Before judgment, `screen.py` builds pools in source order, removes used upstream records, normalized exact duplicates, exact reused Dolly passages, and texts with token-set Jaccard overlap at least 0.5 with a parent query. It draws each sample with a fresh `random.Random(42).sample` call. No Robots excludes 795 conversations with a non-single-turn role sequence. The sample sizes were fixed at 20 per Dolly passage category, 60 No Robots passage prompts and 30 for each other pool.

Unused source records can have appeared in earlier screening; unused does not mean previously unseen. This is a **conservative discovery filter**, not the guide's final manual near-duplicate grouping decision. It can discard independent queries with common wording. Parent data are read computationally for exclusion/hash checks; parent query text, sealed files and model errors were not displayed for this screen. No new row is selected to repair a known model error.

| Filtered pool | Available texts before judgment | Sampled | Provisionally eligible | Estimated row yield, 95% Wilson range |
| --- | ---: | ---: | ---: | --- |
| Dolly closed QA with passage | 1,702 | 20 | 13 | 1,106; 737–1,394 |
| Dolly information extraction with passage | 1,359 | 20 | 7 | 476; 246–771 |
| Dolly summarization with passage | 1,116 | 20 | 1 | 56; 10–264 |
| Dolly direct categories, no passage | 5,797 | 30 | 27 | 5,217; 4,312–5,596 |
| No Robots train, direct categories | 7,827 | 30 | 27 | 7,044; 5,822–7,556 |
| No Robots train, passage categories | 823 | 60 | 38 | 521; 417–612 |
| GSM8K remaining test questions | 1,303 | 30 | 30 | 1,303; 1,155–1,303 |
| BFCL remaining calculation-filtered texts | 224 | 30 | 8 | 60; 32–100 |

There are **240 fresh screening decisions and 151 provisional successes in these eight samples**. These are AI judgments. No human annotation agreement, accepted count or independent-group count follows from them. The ranges multiply a row-level binomial Wilson interval by the filtered pool size; they describe screening uncertainty under an approximate row-sampling model. They are **not** acceptance forecasts or group-aware uncertainty intervals. Correlated templates, conservative filtering, final grouping, human disagreement, licenses and cumulative caps can lower usable supply substantially. Do not add category interval endpoints as a joint confidence interval.

For No Robots, 41/60 initially identify a usable instruction/passsage boundary. Three more are held because the separated instruction reaches the parent-overlap threshold, leaving 38. All retained instruction strings are exact substrings; no source cue is inserted. The sample includes instructions after the passage and before it. Full prompt attachment overlap and semantic parent grouping remain to be checked across the full pool. Displayed passage excerpts were sufficient to locate boundaries; this was not a full content/rights audit of every linked article.

Why rows fail matters. Many Dolly questions never mention the linked passage: the upstream task name cannot supply that missing signal. No Robots includes bare fact questions, unfilled placeholders, figure dependencies and table/document boundary cases. Some direct prompts depend on unknown personal history or current information. BFCL's math-function filter also returns weather, property search, execution and missing-input requests. These are not silently relabeled to fill a quota.

## What this means for 2,500 and 4,000

Each class needs **525 additional accepted rows for 625/class**, or **900 for 1,000/class**. Keep the four-row group cap, 40% request-type cap and 75% source cap. Distinct texts and source rows do not establish distinct groups.

| Class | Capacity conclusion | Next evidence needed |
| --- | --- | --- |
| Direct answer | Two large, diverse provisional pools; no obvious raw supply shortage. Neither is a certified independent-group inventory. | Freeze source/type quotas; check parent/shared scenarios, cross-source duplicates and real review yield. |
| Document retrieval | Dolly plus No Robots looks plausible. No Robots would need at least 132 new accepted rows at 625/class or 225 at 1,000/class if Dolly supplies its full permitted share; the new sample suggests room before final grouping. | Audit extraction offsets, attached-source identity, topical groups and type balance. The Dolly summary stratum has low yield; No Robots summaries may help. |
| Calculation | GSM8K has ample questions, but all 30 sampled requests have the existing `word-problem` type. More GSM8K or SVAMP word problems cannot by themselves satisfy variety. | A large second pool of independently grouped numerical tasks beyond word problems, with fixed type definitions. New-source screening is investigating this. |
| Knowledge lookup | Existing BFCL was already tight. New ToolACE candidates are mostly keyed-record requests; see the separate measured screen. SQL-create-context fails query-only grounding in its lookup sample. | Additional source and request-type coverage; group/parent checks and source adoption. Do not add database names to otherwise incompatible queries. |

For calculation, the existing 16 GSM8K rows already occupy word-problem slots. That leaves at most **234 new word problems** at 625/class, or **384 at 1,000/class**, before accounting for any other source's word problems. Thus at least 291 or 516 of the new calculation rows must be other types. Even treating all 224 remaining BFCL-filtered texts as usable would not fill that gap; only 8/30 passed this fresh sample. This is a bound on the screened existing calculation pools, not proof that all public data are insufficient. Subdividing word problems after seeing this bottleneck merely to escape the cap would change the protocol and is not done here.

The No Robots estimates cannot be interpreted as a guaranteed 4,000-row release, and a larger direct-answer class cannot silently compensate for an unexamined lookup shortage. No accepted source/type/group allocation has yet demonstrated either balanced target. Source sampling and annotation exposure will be disclosed with any future split.

## Review capacity and concrete next work

Prepared an ignored **12-case human timing pilot**, three proposed cases per action, shuffled with seed 42. Its primary-label and rationale fields are null; proposals are in a separate file. It includes adopted-source examples and three unadopted ToolACE screening cases. Its selection is deliberate, so it cannot estimate population acceptance yield. Time Altan's active labeling/adjudication effort, then use a larger representative batch to estimate rejections and grouping work. AI elapsed time is not human throughput.

1. Continue the targeted group/type inventory for varied calculations and non-keyed lookups. The completed Glaive follow-up found 30 provisional calculation candidates, at most 23 after tentative group caps, plus a narrow lookup subgroup capped at ten rows in three tentative groups. It did not establish the required hundreds of independent cases. Retain failed leads and generated-origin disclosure.
2. Resolve licenses/adapters and audit grouped capacity, parent collisions and cumulative types for a proposed source mix. Preserve the original `docs/collection-brief.md`; prepare a separate M3.5 brief only when the mix is defensible.
3. Review the concrete source/adapter proposal and time the human pilot. Record actual decisions; then freeze quotas and stop rule before bulk import and model comparison. A failure to establish the 2,500 minimum requires an explicit scope decision, not padding or silent relaxation.

The pilot files are `work/m3-5-screen/existing/human-pilot.md`, `human-pilot.jsonl` and the separate `human-pilot-proposals.jsonl`. No blind acceptance check is claimed from the screening agent that already saw these proposals. Source adoption, blind review and human adjudication remain future acceptance steps.

## Reproduction and preservation

All raw data, sample text, scripts and row verdicts remain ignored under `work/m3-5-screen/`. The existing-source bundle contains `download.json`, `screen.py`, `judge.py`, eight `*-pool.jsonl` and `*-sample.jsonl` files, `pool-summary.json`, `verdicts.jsonl`, `capacity.json`, a blank human pilot and `hashes.json`. New-source evidence has its own manifest and reproduction script. No source manifest or accepted dataset was edited.

Run from the repository root:

```sh
uv run --no-project --with pyarrow python work/m3-5-screen/existing/screen.py
python3 -I work/m3-5-screen/existing/judge.py
python3 work/m3-5-screen/lookup/reproduce_samples.py
python3 work/m3-5-screen/lookup/glaive_verify.py
```

PyArrow is a throwaway parsing dependency, not a change to `pyproject.toml` or `uv.lock`. It reads the public Parquet schema; answers are not printed or used for route judgments. `protected-before.json` records the M3 release/review/split, source manifest, old collection brief and environment hashes for before/after preservation checks. The old data release and sealed-test partition remain unchanged. Existing-source audit manifest SHA-256: `3c1525de6d75a296d0198f3eaad820183fabb749c493f44d250258d11d9fa33e`. Commands and actual final check results are recorded in the learning log; no training, API inference or final-test execution occurred.
