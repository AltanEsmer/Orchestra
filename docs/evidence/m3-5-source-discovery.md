# M3.5 new-source discovery for the lookup and calculation gaps

November 1, 2026, continuing the [group and quota audit](m3-5-group-quota-audit.md). Altan asked for appropriate public datasets to grow the release from 400 rows toward 2,500 (minimum) and 4,000 (preferred). The audit's binding gaps at 625 per class are **304 non-keyed lookups** and **234 non-word-problem calculations**; retrieval and direct-answer supply is not the constraint. This is AI screening only. No source was adopted, row imported, label recorded, split changed or model run. Accepted rows remain **400**.

**Calculation looks reachable at 625 per class from human-written, permissively licensed sources. Lookup does not, under the current contract.** No screened corpus names many distinct structured sources in its unchanged queries. Lookup supply appears only behind two scope decisions Altan has not made, and even if both are approved, the strict count falls short of 304 (inferred). The 1,000-per-class lookup target is not supported by any evidence found.

## Method

Five discovery lanes ran in parallel under one shared brief (`work/m3-5-groups/discovery/BRIEF.md`): human intent corpora, open human prompts, tool-use corpora, table and data-analysis benchmarks, and exam-style or synthetic mathematics. Every lane verified licenses from primary cards, LICENSE files or papers, pinned revisions, saved its filter contract before building pools, removed normalized duplicates and texts at token-set Jaccard 0.5 or more against the 400 parent rows (computed, never printed), saved a `random.Random(42)` order and then judged the first 30 per pool. Where a main pool was empty or uninformative, a second stratum received its own saved contract and order before judgment. Router text is the unchanged original query field; no title, option, tool definition, answer or source name was appended. Previously screened sources were not repeated: Dolly, No Robots, GSM8K, all BFCL v3 files, ToolACE, Glaive, ToolAlpaca, sql-create-context, Math Stack Exchange and the published calculation benchmark. MATH and MathOdyssey stay excluded.

The lanes judged samples from **19 corpora** and checked five more for access and terms only. They recorded **804 formal screening decisions** plus 200 table-naming checks on Spider and BIRD. All 804 have null human labels and no adoption. The 244 provisional calculation and lookup rows have no exact or Jaccard-0.5 match against the 145-row integrated inventory. One query string appears in two lanes. Counts below are measured unless marked inferred or guess. Pool estimates multiply a Wilson interval by pool size and are screening ranges, not acceptance forecasts.

Lead verification re-read primary licenses for CLINC150, DataBench, AQuA-RAT and both CAMEL sets, spot-checked each lane's verdict file and re-counted all verdicts. The lane screens were made by subagents on a single model family; there was no independent second judgment.

## Calculation sources

| Source, revision | License and origin | Pool | Eligible non-word / 30 | Types seen | Capacity after four-row cap | Verdict |
| --- | --- | ---: | ---: | --- | --- | --- |
| [CLINC150](https://github.com/clinc/oos-eval/tree/828f8093932c8fe6ca7936c3d2e52903b1c523de), `828f809` | CC BY 3.0 Unported LICENSE file; Mechanical Turk workers | 207 (`calculator`, `measurement_conversion`) | 28 | arithmetic 17, unit conversion 9, percent 2 | about 168 (142-177), inferred | Recommended |
| MASSIVE en-US 1.1 ([repo](https://github.com/alexa/massive/tree/f966f21846043aabef9b0f974fa7970027f43738)) | CC BY 4.0; crowdsourced, same utterances as SLURP and HWU64 | 123 (`qa_maths`, `datetime_convert`) | 18 | arithmetic 15, percent 2, conversion 1 | about 65 (46-81), inferred | Recommended, small |
| [OpenAssistant oasst2](https://huggingface.co/datasets/OpenAssistant/oasst2/tree/179dd21fc55192153d94adb0e0ce8f69e222bf75), `179dd21` | Apache-2.0 card; volunteer-written | 173 (focused stratum) | 9 | percent/finance, arithmetic, number theory | about 52 (29-83), inferred | Recommended, small |
| [TheoremQA](https://huggingface.co/datasets/TIGER-Lab/TheoremQA/tree/a340b1782960a712843aae3ed25f1e013cc008a5), `a340b17`, `self`-source rows | MIT; expert-written subset | 146 | 22 | mostly combinatorics, algebra/calculus | about 112 rows, 70-100 groups (guess) | Recommended, narrow |
| [AQuA-RAT](https://github.com/google-deepmind/AQuA/tree/26b64ed1f22208c6742f47df547dfd65088ec30d), `26b64ed` | Apache-2.0; crowd rewrites of GMAT/GRE-style seeds from prep websites | 28,839 | 24 (+3 word problems) | arithmetic, number theory, percent, geometry, physics, probability, ratio | 90-375 scenario families (rough inference) | Decision needed |
| [CAMEL physics](https://huggingface.co/datasets/camel-ai/physics/tree/a7a962cb4da69bc7c9d1a41231066cffc5eec93d), `a7a962c` | CC BY-NC 4.0; GPT-4 generated | 5,954 | 19 | physics formula | about 248 subtopic groups; type cap binds first | Decision needed |
| [DeepMind mathematics](https://github.com/google-deepmind/mathematics_dataset/tree/427f45075f84b8b9774950196ad63867ca20ffb3), `427f450`, via unofficial mirror | Apache-2.0; programmatic templates | 112.7M rows, 60 drawn | 19 | arithmetic, number theory, algebra | 108 to about 400 rows by template count, inferred | Limited |

**Rejected or blocked for calculation.** MathQA: 83.2% of rows are exact token matches to AQuA and every row is lowercased and tokenized, so it fails unchanged wording; use it only as a category index into AQuA. CAMEL math: 11/30 with frequent near-duplicates inside subtopics. TheoremQA's 608 rows citing textbooks, websites or exams such as SOA and Putnam: the authors' MIT grant cannot clear third-party question text, the same issue as MATH, and most physics and finance supply sits there. OASST main pool: 2 of 30 non-word rows.

CLINC150's paraphrase seeds and scenario prompts are not released, so its number-swap grouping is a lower bound on true merging. Ten number-swap patterns ("what is # times #", square roots) recur in both CLINC150 and MASSIVE and must join across sources. One CLINC row is a number swap of the protocol's own "18 percent of 250" example; it is flagged, not counted twice. One OASST candidate repeats the widely cited GSM8K tennis-ball problem and needs a cross-source hold against the adopted GSM8K source.

## Lookup sources

| Source, revision | License and origin | Pool | Eligible / 30 | Why it fails or stalls | Verdict |
| --- | --- | ---: | ---: | --- | --- |
| [DataBench](https://huggingface.co/datasets/cardiffnlp/databench/tree/e75d53add267d2f9cfa32efd65ad77f0807adfad), `e75d53a` | MIT; human-written questions over 80 tables | 1,829 | 1 keyed | Questions say "in the dataset" or nothing. About 301 generic rows over 69 datasets, 209 after the cap (regex inference, unjudged) | Needs adapter decision |
| CLINC150 read-record intents | CC BY 3.0; human | 3,149 | 0 | 29 of 30 read the user's own calendar, list, bill or transactions | Needs scope decision |
| MASSIVE en-US query intents | CC BY 4.0; human | 2,046 | 0 | 25 of 30 read the user's own calendar, email, contacts or lists | Needs scope decision |
| StableToolBench (`aa4ed9f`), Hermes FC v1 (`dae3e1d`), Seal-Tools (`ce753ec`), API-Bank (`faf7546`) | Apache-2.0 or MIT; mostly generated | 40 to 1,053 | 0-7 per stratum; 7 non-keyed in total | The catalog name sits in the hidden tool definition. All seven proper catalog names found in queries come chained to live, write or unrelated requests | Reject |
| InfiAgent-DABench, TableBench, QRData | CC BY-NC 4.0 or Apache-2.0; mostly generated | 257-492 | 0 | 0 of 90 sampled questions name their table | Reject |
| Spider (`0c35091`), BIRD dev (`3c11fb1`) | CC BY-SA 4.0 | 7,987 and 1,533 | 1 keyed each | 0 of 100 per sample name a table or database (Wilson upper bound 3.7%); six named-table questions exist in all of Spider | Reject |
| OASST2 lookup pool | Apache-2.0; human | 69 | 0 | Volunteers prompting a tool-less assistant never name a store | Reject |

Across the table lane, **0 of 180** sampled questions name a dataset, table or database. Across the tool lane, none of 19 provisional lookups names a catalog with a proper name. This is the structural reason lookup is scarce: public corpora either hide the source in metadata or attach it without mentioning it, while Orchestra's contract requires the query text to identify it.

**Access-blocked.** xLAM-60k (CC BY 4.0, generated) is behind an automatic click-through gate that only Altan can accept. APIGen-MT-5k is ungated but CC BY-NC 4.0 and covers only two settings (retail, airline), so at most eight rows. The ToolBench parent release is on Google Drive or Tsinghua Cloud with an unmeasured size and a research-and-education-only line.

**Real-user chat logs.** WildChat (ODC-BY, ungated), Chatbot Arena (gated; prompts CC BY 4.0, outputs CC BY-NC 4.0) and LMSYS-Chat-1M (gated custom agreement, no redistribution) were checked for terms only and not downloaded. WildChat contains hashed IPs, coarse location and request headers. The protocol's "Do not ingest personal queries" rule applies; any use needs an explicit scope and privacy decision before even a screening download.

## What this means for the targets

| Gap | Need | Candidate supply before human review | Reading |
| --- | ---: | --- | --- |
| Non-word calculations at 625/class | 234 | CLINC150 + MASSIVE about 220 (175-245) + OASST about 52 + TheoremQA `self` about 112 = **about 384**, inferred | Reachable from human-written sources, if review yield holds |
| Same at 1,000/class | 459 | About 384, inferred | About 75 short; needs AQuA-RAT or CAMEL physics |
| Non-keyed lookups at 625/class | 304 | DataBench about 209 (adapter) + personal stores about 52 non-keyed under strict grouping (scope) + tools about 7 = **about 268**, inferred | Short even if both decisions are yes |
| Same at 1,000/class | 529 | About 268, inferred | Not supported |

Type spread stays within caps at 625: about 154 new arithmetic rows plus seven existing gives about 161, under the 250 per-type ceiling (inferred). The human-written calculation supply is narrow, though. Physics, geometry and probability remain thin without AQuA-RAT or CAMEL physics. The personal-store figure uses the strict reading, one group per store kind. The lenient reading, grouping only date and number swaps, would give thousands of rows, but crowd paraphrases of shared prompts and the near-universal "my" make that implausible as independent evidence.

## Decisions for Altan

1. **Personal stores.** Does "my calendar", "my emails" or "my shopping list" identify a structured knowledge base for `knowledge_lookup`? If yes, does each store kind form one shared setting under guide v2? This opens CLINC150 and MASSIVE lookup pools. Three CLINC holds ask for an approval or processing status and may also fail the live-data rule.
2. **Attached-dataset adapter.** May a question that says "in the dataset" keep its original table as an attachment outside router text, as Dolly passages do? If so, is the first action `knowledge_lookup` (structured data) or `document_retrieval` (attached file)? This decides DataBench.
3. **Provenance tolerances.** Accept or reject AQuA-RAT's exam-prep seed provenance, CAMEL's non-commercial GPT-4-generated text, and whether TheoremQA's externally sourced rows get a rights review or stay excluded.
4. **If lookup still falls short.** Choose an explicitly imbalanced release, an authored lookup supplement under the existing AI-draft supplement with human review, or a prediction-contract change. The audit already anticipated this decision before bulk collection.

## Risks to carry into adoption

- **Style shortcuts.** CLINC150 and MASSIVE rows are lowercase, unpunctuated voice-assistant text. If only their calculation rows enter, style can predict the label. Draw direct-answer rows (for example definition or factual intents) from the same corpora, or report source-by-class performance.
- **Trigger phrase.** If DataBench supplies most non-keyed lookups, "in the dataset" could nearly identify `knowledge_lookup`. The protocol asks for hard negatives across labels; this would need retrieval or direct-answer rows that also mention a dataset.
- **Hidden grouping.** CLINC150 seeds, scenarios and worker IDs are unreleased; AQuA replicas change only values; CAMEL subtopics contain near-duplicates. All three can overstate independent groups.
- **Unverified mirror.** DeepMind rows came from an unofficial mirror whose fidelity to the official release is unverified.

## Reproduction

Raw downloads, contracts, pools, seed-42 orders, verdicts, summaries, scripts and per-lane hash manifests are ignored under `work/m3-5-groups/discovery/{intents,prompts,tools,tables,mathsets}/`, each with `notes.md`, `download.json` and `hashes.json`. The intents and tools lanes reran their pipelines and reproduced every pool, order and verdict file byte for byte. Live API reads are not byte-stable reruns; use the saved snapshots. No tracked file, accepted dataset, split, source manifest or collection brief was changed by the lanes.
