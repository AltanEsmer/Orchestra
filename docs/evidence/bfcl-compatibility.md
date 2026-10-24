# Berkeley dataset compatibility inspection

Observed on October 24, 2026. This is a source-compatibility investigation, not a research dataset release or model evaluation. The user authorized inspecting a small Berkeley sample to assess whether it could replace further manual query writing.

## Recommendation

Use filtered BFCL records as a potential supplement. This inspection does not support replacing the entire four-class collection with BFCL unchanged. Of 40 inspected records, 18 provisionally fit Orchestra's current prediction contract. Four are exact duplicates, leaving 14 distinct candidates: 11 calculation requests, two structured lookups, and one direct answer. No clear document-retrieval candidate occurred in this sample. These are agent screening judgments awaiting human review, not accepted labels or estimates of the full corpus's composition.

Keep the existing forty human-authored pilot candidates. Assess additional public sources for document retrieval and direct answering before asking Altan to write the remaining study collection. A broader, reproducible filter over BFCL's read-only lookup and calculation records could reduce authoring work. It cannot remove the need to verify the mapping into Orchestra's labels or guarantee enough independent groups per class.

## Source and sampling

The official [dataset card](https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard/blob/61fc0608cfd831fcfbbaa676ebdfef0ed963eeda/README.md) declares Apache 2.0 and describes function-call evaluation with questions and function documentation. The inspected Hugging Face revision is `61fc0608cfd831fcfbbaa676ebdfef0ed963eeda`. Its `BFCL_v3_*` files are the inspected version, not the V4 suite described by the [current leaderboard](https://gorilla.cs.berkeley.edu/leaderboard.html). No account or payment was needed for these downloads.

The five categories were simple, executable-simple, chatable, SQL, and live-simple. First inspect the first four records of each file. After that pass exposed category mismatches, inspect four further positions from each file, selected with Python's `random.Random(42)` without replacement from positions after the first four. The file order is the order just listed. The supplemental pass was chosen after seeing the first pass, so the combined sample is an adaptive, purposive compatibility check. It is not a representative random sample of BFCL. No multi-turn, parallel, or other uninspected category is covered by the numerical findings below.

Downloaded artifacts include the five source files, three available answer files, and the pinned card, totaling 949,779 bytes. Paths, exact source URLs, revision, access date, sizes, and SHA-256 hashes are saved in ignored `work/poteto/bfcl-inspection/download-manifest.json`. The full local records remain outside Git.

## Observed screening results

| Screening outcome | Records before exact deduplication | Distinct candidate texts |
| --- | ---: | ---: |
| Provisional calculation | 15 | 11 |
| Provisional knowledge lookup | 2 | 2 |
| Provisional direct answer | 1 | 1 |
| Provisional document retrieval | 0 | 0 |
| Needs clarification or missing inputs | 4 | Not counted as candidates |
| Outside current tool scope | 18 | Not counted as candidates |
| Total inspected | 40 | 14 candidate texts |

Candidate text is normalized only for duplicate inspection by collapsing whitespace and case. This does not replace manual paraphrase and group review. Closely related probability, vector-similarity, or geometry requests may share a scenario family despite having different text.

The results can be traced to these pinned source files:

- [Simple](https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard/blob/61fc0608cfd831fcfbbaa676ebdfef0ed963eeda/BFCL_v3_simple.json) includes `simple_0`, a supplied-dimension area request that maps provisionally to calculation. Other sampled rows ask for an unsupported prediction or a hotel booking.
- [Executable-simple](https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard/blob/61fc0608cfd831fcfbbaa676ebdfef0ed963eeda/BFCL_v3_exec_simple.json) includes numerical requests with supplied inputs. `exec_simple_32` asks for a company-symbol identity without naming a source. Under Orchestra's current stable-general-knowledge rule, its proposed label is direct answering even though BFCL expects a lookup function. This boundary particularly needs human confirmation.
- [Chatable](https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard/blob/61fc0608cfd831fcfbbaa676ebdfef0ed963eeda/BFCL_v3_chatable.json) has an empty function field. Its first four requests exactly repeat the first four simple-file calculation requests. Empty tool availability does not mean direct answering under Orchestra's fixed calculator assumption. This proves category names cannot be used as our gold labels.
- [SQL](https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard/blob/61fc0608cfd831fcfbbaa676ebdfef0ed963eeda/BFCL_v3_sql.json) includes two sampled SELECT requests identifying a table and record. Both provisionally map to knowledge lookup. The six other sampled SQL requests create, insert, or update data, which Orchestra's read-only lookup action does not cover.
- [Live-simple](https://huggingface.co/datasets/gorilla-llm/Berkeley-Function-Calling-Leaderboard/blob/61fc0608cfd831fcfbbaa676ebdfef0ed963eeda/BFCL_v3_live_simple.json) includes live services, orders, and current information outside the defined tools. `live_simple_0-0-0` describes a user ID without identifying its database in the query. Its function documentation supplies database context, which the current query-only router would not see.

The other held records are `simple_331`, which omits an identified player source, and chatable lines 178 and 193, which respectively omit a case-information source and the elevation data needed for a landscape slope. No held record was forced into a class.

## Conditions before any study import

BFCL answers are function calls or parameter-reference objects, not Orchestra first-action labels. Reference objects were read as data, never evaluated or executed. The [official evaluator](https://github.com/ShishirPatil/gorilla/blob/6ea57973c7a6097fd7c5915698c54c17c5b1b6c8/berkeley-function-call-leaderboard/bfcl_eval/eval_checker/eval_runner.py) reads `ground_truth` separately. The query, tools, and expected call can support screening, but only self-contained user text belongs in Orchestra's model input. Tool names, arguments, answer references, source-category names, and inferred labels must not be appended as input hints. A sampled live record also includes a separate system message, illustrating a context risk when flattening messages.

The [official V2 collection account](https://gorilla.cs.berkeley.edu/blogs/12_bfcl_v2_live.html) describes contributed queries, deduplication, filtering, and modifications. Do not call the entire dataset human-authored, unchanged, or a sample of real production traffic. Do not assume distinct IDs are independent scenario groups. Retain the pinned upstream IDs, source hashes, mapping rationale, source-specific license attribution, and all exclusions in any future import. The manifest permission for Altan's forty authored rows does not apply to Berkeley material.

Before import, document the source decision and unchanged four-class contract, check the license notices for selected artifacts, deduplicate against the pilot and across BFCL files, assign scenario families before splitting, and collect the existing protocol's human review evidence. Database writes, bookings, unsupported live requests, and tool-dependent missing context must not be silently relabeled to meet class quotas. A second agent's agreement is software-assisted screening evidence, not an independent human annotation.

If the inspected records are used later, disclose their prior exposure during this compatibility assessment. Allocate inspected development examples without claiming they were unseen test material. Freeze any later collection criteria before inspecting model errors. There is no research split or trained model now.

## Reproduce and verify the inspection

The ignored directory `work/poteto/bfcl-inspection/` contains:

- `inspect_sample.py`, which downloads the pinned files and extracts the first 20 records.
- `supplement_sample.py`, which reconstructs the additional seeded positions and complete 40-record sample.
- `screen_sample.py`, which preserves the agent's per-record judgments and reproduces counts and duplicates. Its labels are recorded judgments, not an automatic proof of semantic correctness.
- `source-notes.md`, the separate primary-source investigation.
- `sample-40.jsonl`, `screening-40.jsonl`, and `screening-summary.json`, the exact local evidence.

The 40-record sample SHA-256 is `767016f649033dd15e1e111767a30cf38d3819f468a6d310948e2ba91c1a1e86`. The screening ledger SHA-256 is `074faa37147cc5783c7e2eef4a65af896024918fd063fedfd77b808e02e4f072`. Re-running the local supplement and screening scripts reproduced the sample and aggregate counts. Source-file hashes were checked against the download manifest. No row was imported, rewritten, accepted, split, or used for training. The original pilot worksheet, empty pilot JSONL, and empty human-review ledger remain unchanged by this investigation.
