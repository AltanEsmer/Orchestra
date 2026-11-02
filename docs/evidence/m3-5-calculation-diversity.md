# M3.5 calculation diversity screen

October 31, 2026. **Math Stack Exchange provides 12 provisional calculation rows in eight tentative scenario groups across 120 screened posts.** A separate public synthetic sample gives 96 numeric candidates but only 64 rows after provisional template grouping and the four-row cap. Neither establishes hundreds of independent new calculations. MATH has a documented rights dispute and contributes **zero cleared capacity**. Accepted research data remain unchanged.

This is source screening, not adoption, import, Altan's primary annotation, a blind acceptance check, or model evidence. No inference API, answer endpoint, credential, model artifact or sealed prediction was accessed. Parent query text was compared computationally without displaying it. Full question text and attribution remain ignored under work/m3-5-groups/calculation/.

## Independently posted questions

Used the official [Stack Exchange advanced-search API](https://api.stackexchange.com/docs/advanced-search) without a key. Two bounded responses were saved before their respective judgments:

| Snapshot | Fixed selection before judgment | Response bytes and SHA-256 |
| --- | --- | --- |
| Broad discovery | site=math, q=calculate, sort=creation, descending, page size 100; shuffle returned positions with random.Random(42), inspect first 60. | 454,845; 076b0c4c02e4ccfb4707b191e2ee9c2e12556f88198d03ff797ee3f300f4af76 |
| Adaptive numerical follow-up | After broad low yield: title=remainder, sort=votes, descending, page size 100; fresh seed-42 shuffle, inspect first 60. | 196,076; c48ad9919d344ba6578d6342a0a0264a61b059d0f28661b40dd8e70bab4b5c2b |

The follow-up deliberately enriches number theory and popular older posts. Neither sample is representative of all Math Stack Exchange. Source filtering and ordering precede seeded sampling; do not pool their rates as a population estimate. Question-ID lists, complete orders and response bytes freeze this snapshot; rerunning live queries can change it.

Only the original question **body** is router text. HTML tags are removed and entities decoded while textual order and mathematical notation are retained. Titles, tags and author metadata remain provenance. No title is appended to repair missing body context. This HTML-to-text projection needs an explicit adapter decision before adoption. No post was shortened into a convenient numerical exercise. No answer records were requested; question bodies themselves sometimes include attempted solutions or already-known results, which often cause explanation/verification exclusions.

[Stack Exchange's licensing policy](https://stackoverflow.com/help/licensing) assigns CC BY-SA 2.5, 3.0 or 4.0 by contribution date and points to revision timelines for the applicable license. The broad sample returned 57 explicit 4.0 licenses and three missing licenses; the remainder sample returned 17 explicit 4.0, 36 explicit 3.0, three explicit 2.5 and four missing. Missing-license rows are not counted. User posting is not proof of exclusively human authorship: some bodies disclose AI assistance. Quoted textbook/contest material needs separate rights review; platform metadata cannot license rights a poster did not hold.

Every sampled row records post ID, author object/profile link, URL, creation and available last-edit timestamps, returned license, body/text hashes, verdict, type, tentative group and rationale. All 12 kept candidates additionally have latest returned revision GUID/number and an attribution bundle. Three API requests consumed three quota units (299, 298 and 297 remaining); none returned backoff. No answer endpoint or large dump was used.

## Observed route and group inventory

| Sample | Inspected | Provisional calculation | Needs review | Excluded from calculation | Tentative candidate groups | Maximum sample rows after group cap |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Broad posts | 60 | 2 | 11 | 47 | 2 | 2 |
| Remainder follow-up | 60 | 10 | 9 | 41 | 6 | 10 |
| Public synthetic supplement | 100 | 96 | 0 | 4 | 25 | 64 |

All are AI screening judgments. Exclusion from calculation can include valid explanation queries, but this screen accepts no other class. A numeric example inside a proof, algorithm, citation or explanation request is insufficient. Symbolic parameterized remainders, proof requests, unsupported diagrams and missing numeric data are excluded or held. One otherwise numeric remainder candidate is held because the per-post license is absent.

The two broad candidates are [expected sample maximum](https://math.stackexchange.com/questions/5150832) (probability-statistics) and [triangle angle determination](https://math.stackexchange.com/questions/5148168) (geometry). Both supply their setup in the body. The latter includes an image, but the altitude, angle and point constraints are stated in text; its request for a geometric worked solution remains a human boundary check.

The ten follow-up candidates map to the existing number-theory type after body inspection, not merely because of a tag/title:

| Tentative scenario group | Question IDs | Candidate rows | Group reasoning |
| --- | --- | ---: | --- |
| Repunit remainder | 1611471 | 1 | Fixed repeated-digit length and divisor. |
| Sum of powers modulo an integer | 3490156, 279333, 391859 | 3 | Conservatively merge related two-power expression scenarios with numeric changes. |
| Single power modulo an integer | 116103, 1345259, 1635506 | 3 | Conservatively merge repeated exponent/remainder scenarios; changed values do not establish independence. |
| Simultaneous congruences | 778854 | 1 | Fully numeric system; general solution notation needs human confirmation under numeric-result rule. |
| Fibonacci remainder | 344716 | 1 | Recurrence and requested numeric index/modulus supplied. |
| Polynomial value from coefficient constraints | 2111675 | 1 | Numeric value at specified argument with complete constraints. |

These eight combined groups are provisional. Same post/revision always stays one group. Sharing an operation alone does not merge genuinely different scenarios; power families above are conservative small-variation clusters. Source-wide matching can still merge/exclude them. Different author or question ID alone does not establish independence.

Normalized exact matching and token-set Jaccard overlap at least 0.5 against all 400 parent rows found **zero exact and zero threshold collisions in both 60-post samples**. Parent text and sealed partition were not printed. Lexical checks cannot certify semantic independence or detect diagram/source reuse. No candidate was selected from model errors.

## Public synthetic supplement

The [author repository](https://github.com/janwan2003/llm-calculation-benchmark/tree/c43e41b3a02c8f0ee02477a7b55746150ed05051) explicitly distinguishes 399 programmatically generated prompts from 101 translated Polish competition problems and says MIT covers code and the synthetic portion. Only existing synthetic records entered sampling; competition records were excluded before prompt inspection. This is published generated data, not natural traffic or newly generated top-up. No generator/model was run.

Pinned revision: c43e41b3a02c8f0ee02477a7b55746150ed05051. JSON: 195,134 bytes, SHA-256 62c4b42b17b3602ce5625f07de937ff11ec49350c79e13468458e5b70d98a9bf; license SHA-256 f6d51c83a75e002b7f7c40887021947cd3f1f1dc8032f7128bf9cb3f70656dcf. Judgments use unchanged prompt only, never the source answer field.

A seed-42 shuffled first-100 order was saved before judgment. Ninety-six ask numerical outputs; four ask symbolic simplify/factor/expand. Operation templates, paraphrases and numeric swaps are grouped together, including integer/decimal/fraction variants of one arithmetic operation. Twenty-five provisional clusters leave at most 64 sample rows: 17 word problems and 47 other calculations. This is a bounded inventory under conservative grouping, not a certified full-corpus upper bound. Some conversion/probability clusters cover genuinely different situations and need refinement; extra groups must have scenario evidence.

Capped sample types: arithmetic 17, algebra/calculus 12, percent/finance 7, probability/statistics 5, average 3, per-unit scaling 2, physics formula 1 and word problems 17. Parent comparisons found zero exact/threshold collisions in all 399 prompt projections. Wording variations of one template do not create independent scenarios.

## Blocked leads

The [current Hendrycks README](https://github.com/hendrycks/math/blob/985bdc1696e88e8643f081a0ff4719da39f2ae2a/README.md) links qwedsacf/competition_math. Its API reported ungated access at revision e839825f9ec5c6cfa585c654a59610969ec13993 and its card declares MIT. Its linked Parquet was downloaded (4,848,345 bytes; SHA-256 2325458edc03d786939ee9e1e5795efb9e2480247b6e1ed2c51f41bea7369c6a), projected using problem only, and a seed-42 first-100 order saved.

A subsequent check found the [AoPS complaint in Hugging Face's own takedown repository](https://huggingface.co/datasets/huggingface-legal/takedown-notices/blob/6be1fd145590de35cc6c3788a146dcf6a806382a/2025/2025-01-02-AoPS.md), alleging unauthorized MATH reuse and requesting removal of copies. Processing stopped; no alternate copy was sought and no continued route/group capacity judgment was made. All 100 positions have rights-blocked audit records. Ungated access, author linkage and MIT metadata do not resolve the dispute. **Count zero cleared MATH rows** pending authoritative resolution; no question text is committed.

[MathOdyssey's pinned author README](https://github.com/protagolabs/odyssey-math/blob/fe9e83df06111728e1b06ddaee0a60837c07d6c9/README.md) restricts dataset use to testing and prohibits training use; original question/image rights remain with authors. Repository MIT is not blanket data permission. No Odyssey data file was acquired/counted. DeepMind's [mathematics generator](https://github.com/google-deepmind/mathematics_dataset) remains a published synthetic lead, but was not downloaded/screened.

## Consequence for capacity

At 625/class, at most 234 additional word problems fit after the existing 16; at 1,000/class, at most 384 fit. At least 291 or 516 new calculations must therefore be other types. Independently posted questions currently contribute **12 provisional non-word-problem rows in eight groups**, with number theory 10, geometry 1 and probability/statistics 1. Even counting all 47 capped synthetic non-word-problem sample rows, this investigation establishes at most **59 provisional non-word-problem sample candidates**, leaving at least **232 or 457** to establish elsewhere before counting other sources.

These are sample-inventory gaps, not proof that the public site lacks enough material. No extrapolation from API first pages, synthetic headline size or disputed MATH rows is justified. Source adoption, complete grouping, licenses and human review can reduce yield. Existing number-theory rows (9) plus these ten remain below the 40% class cap. Check source mix jointly: no source above floor(0.75 × 625)=468 or 750/1,000.

Next useful step is a predeclared bounded inventory spanning geometry, finite probability, explicit numeric integrals and arithmetic, with body-only criteria and duplicate-link/quoted-source review. Freeze collection quotas after combining capacity and actual human review evidence. This note authorizes no adoption or bulk collection.

## Local evidence and checks

The ignored bundle contains source/API snapshots and download metadata, problem/prompt projections, complete seeded orders, 220 formal route verdicts (120 posts plus 100 synthetic prompts), separate 100-position MATH rights hold, candidate-attribution.jsonl, candidate revision metadata, summary.json, scripts and hashes.json. The projection and judge scripts ran successfully against saved bytes. Live API reacquisition is not byte-stable. sample.py used temporary PyArrow for the initial MATH projection before the hold; do not rerun that blocked-source screen as a capacity step. No project dependency, source manifest or accepted dataset changed.
