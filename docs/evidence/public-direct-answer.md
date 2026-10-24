# Public direct-answer source inspection

Inspected October 24, 2026. **Recommend a filtered No Robots supplement for human review:** 13 distinct provisional direct-answer candidates, 4 held, and 3 excluded in a fixed 20-record screen. These are useful-candidate counts from an ordered convenience sample, not corpus prevalence, accepted annotations, or evidence of router performance. No study rows were imported, no examples generated or rewritten, and no training or protocol change occurred.

## Source, rights, and provenance

[HuggingFaceH4/no_robots](https://huggingface.co/datasets/HuggingFaceH4/no_robots/blob/e6f9a4ac5c37faeb744ba9ecf0473184d7f8105b/README.md), revision `e6f9a4ac5c37faeb744ba9ecf0473184d7f8105b`, describes 10,000 English instructions/demonstrations created by skilled human annotators, mostly single-turn. This is the publisher's provenance statement, not independent verification or naturally occurring traffic. The card leaves collection, annotator identities, and sensitive-information details unspecified. Its categories describe instruction tasks, not Orchestra routes.

The exact license is **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**. Free unauthenticated download succeeded. Noncommercial study use fits the stated grant; commercial use requires separate permission. On sharing, retain supplied creator/copyright/license/disclaimer notices, link the source and license, and identify modifications. Do not imply endorsement or add legal/technical restrictions incompatible with the grant. The license does not establish privacy rights or rights the licensor does not hold. See the [official legal code, sections 1–3](https://creativecommons.org/licenses/by-nc/4.0/legalcode.en). The dataset remains separately licensed from Orchestra's MIT code.

Attribution to retain: **No Robots (2023), Nazneen Rajani, Lewis Tunstall, Edward Beeching, Nathan Lambert, Alexander M. Rush, and Thomas Wolf; Hugging Face; https://huggingface.co/datasets/HuggingFaceH4/no_robots; CC BY-NC 4.0, https://creativecommons.org/licenses/by-nc/4.0/**. Record revision and describe extraction/filtering when sharing derived data. The card supplies that author/title citation; its full original citation and license text are preserved locally. This is a source permission assessment, not source adoption or a guarantee about embedded third-party excerpts.

A reserve alternative is [Databricks Dolly 15k](https://huggingface.co/datasets/databricks/databricks-dolly-15k/blob/bdd27f4d94b9c1f951818a7da7fd7aeea5dbff1a/README.md), pinned at `bdd27f4d94b9c1f951818a7da7fd7aeea5dbff1a`. Its card reports employee-written English prompts, explicit instructions against generative AI, and some Wikipedia context. Its exact notice is **Copyright (2023) Databricks, Inc.** and CC BY-SA 3.0, allowing academic/commercial use with attribution and ShareAlike obligations for adaptations. Retain its Databricks source/license notice and Wikipedia notices where applicable; consult the [official CC BY-SA 3.0 legal code](https://creativecommons.org/licenses/by-sa/3.0/legalcode). Only its metadata/card were examined here: no downloaded row screen or usable-count claim. No Robots currently has the stronger local compatibility evidence.

## Fixed sample and query isolation

Downloaded the original `data/test-00000-of-00001.parquet` (500 source rows, 570,905 bytes) at the pinned No Robots revision. Selected **zero-based rows 0–19**, in file order, before category or text filtering. The source's test designation is unrelated to a future Orchestra split. The complete shard was downloaded to preserve exact original bytes; only 20 rows were screened. No upstream labels or assistant responses were used to decide the routes.

Extraction uses the first message only when its role is `user` and its content exactly equals `prompt`. All 17 eligible records preserve the original user text byte-for-byte as UTF-8 string content, including literal escape sequences. The other 3 begin with system personas; their prompt fields must never become classifier inputs. `query-only-sample.jsonl` contains provenance IDs plus `text`; **only `text` would be a model input**. Assistant replies, categories, personas, IDs, rationales, and screening decisions stay outside it. `original-sample.jsonl` retains original records solely for auditing.

The local ledger records every sampled source index, full prompt ID, exact eligible input, input hash, screening rationale, revision, and source path. No upstream category is automatically mapped to a route. Stable general-knowledge questions follow the current annotation guide's direct-answer interpretation; their factual answers were not validated. Numeric output-length/count constraints do not request arithmetic answers.

| Source row indices | Provisional result | Reason |
| --- | --- | --- |
| 1, 2, 4, 7, 8, 9, 10, 11, 14, 15, 16, 17, 19 | 13 direct-answer candidates | Self-contained creative writing, advice, classification, or general knowledge; no named external source, live requirement, or numeric computation. |
| 3 | 1 held | “Other” presupposes an unstated previous set. |
| 6, 18 | 2 held | Inline passage rewrite/summary: human review must resolve the passage-reading boundary and excerpt provenance. No passage was removed to make the query appear self-contained. |
| 12 | 1 held | Named personal relationship: fiction/consent is not established by the source card. |
| 0, 5, 13 | 3 excluded | System personas and multi-turn chat, incompatible with direct use of the source prompt as a standalone user query. |

There are 13 distinct provisional texts after whitespace/case normalization. This does not establish independent scenario groups or absence of paraphrases across the corpus. None is an accepted Orchestra label. Human review, source manifest approval, privacy/embedded-rights checks, scenario grouping, and the existing M1 review/readiness requirements still apply. Broad topical overlap and instruction-writer style remain limitations; sampling other source positions could produce a different yield. The narrow sample cannot fill the entire direct-answer target or establish coverage of explanations and hard boundaries.

## Local evidence and reproduction

All downloaded rows and derived queries remain under ignored `work/poteto/complementary/direct/`; only this report is intended for tracking. `git check-ignore work/poteto/complementary/direct/test.parquet` confirmed exclusion. `manifest.json` records hashes and byte sizes for source/card/license/API files, extraction and screening scripts, sample and ledger. Key SHA-256 values:

| File | SHA-256 |
| --- | --- |
| `test.parquet` | `60707b2636a46e37bb0c1e9ca263a18553f430317b7a53c691676d6a492fc0f2` |
| `README.md` | `22b642520e082ba1a6c4a93047bd5946aeca099763c6f2d11b59d91e61e79186` |
| `LICENSE-CC-BY-NC-4.0.txt` | `41003d4a74749c0220e33dd415042164b5a1093ed401f36277234f772d22d3d0` |
| `original-sample.jsonl` | `9f1a4c6086b27e268c8bc59c52d6f0751f4f910755d061a5596ff547dd16819c` |
| `query-only-sample.jsonl` | `d8ea900dc58962647579ed1b324b96d6f8eed357b966d9fdf72fac6119426392` |
| `screening-ledger.jsonl` | `20828a69835d142c100781b1ebf7aa2e9a6235b3aa7ef4c277a2de22033d6dae` |

Download URL: [original pinned parquet](https://huggingface.co/datasets/HuggingFaceH4/no_robots/resolve/e6f9a4ac5c37faeb744ba9ecf0473184d7f8105b/data/test-00000-of-00001.parquet). To recreate local derivatives from that file, run:

```sh
uv run --no-project --with pyarrow==26.0.0 python work/poteto/complementary/direct/extract.py
python3 work/poteto/complementary/direct/screen.py
```

PyArrow 26.0.0 was used transiently outside project dependencies to read the original format; no dependency or lockfile changed. Screening is an agent-authored compatibility assessment, not independent human annotation. Hash checks and count verification establish reproducibility of this screen only.
