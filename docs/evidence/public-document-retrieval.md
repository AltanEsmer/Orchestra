# Public document-retrieval supplement: compatibility inspection

Inspected October 24, 2026. Research preparation only. The existing forty human pilot candidates remain intact. No records were imported, rewritten, accepted, or used for training. These are agent screening judgments, not independent human annotations.

## Finding and source triage

Dolly is the stronger candidate for a bounded inspection, but the result supports a conditional filtered supplement: **3 conditional candidates, 2 held, and 15 excluded from the document supplement among 20 inspected instructions**. Categories alone do not map to Orchestra actions. No estimate of corpus-wide yield follows from this ordered sample.

| Source | Primary evidence and decision |
| --- | --- |
| Databricks Dolly 15k | Human-authored instructions, separate reference context, public download, explicit dataset license. Inspect original instructions in `closed_qa` and `summarization`; never concatenate context or insert a document cue. [Pinned card](https://huggingface.co/datasets/databricks/databricks-dolly-15k/blob/bdd27f4d94b9c1f951818a7da7fd7aeea5dbff1a/README.md). |
| QMSum | Human-annotated query-based meeting summaries. Repository queries depend on a paired meeting transcript; its documented examples include generic meeting requests and topic/person questions. Lower priority for a router without hidden meeting context. Repository MIT notice exists, but original transcript rights were not separately established in this inspection; no blanket clearance asserted. [Pinned README](https://github.com/Yale-LILY/QMSum/blob/83d7768c1f2b4dfeb091385d3dc7e239b8e5bb7e/README.md), [license](https://github.com/Yale-LILY/QMSum/blob/83d7768c1f2b4dfeb091385d3dc7e239b8e5bb7e/LICENSE), [authors' paper](https://aclanthology.org/2021.naacl-main.472/). No QMSum records screened or counted. |

Dolly contributors were employees instructed against generative AI; reference passages came from Wikipedia for relevant tasks. This is instructed human writing, not observed user traffic. Individual contributor identities and Wikipedia page/revision identifiers are not supplied per record in the inspected four-field schema. The provider reports creation in March–April 2023 by more than 5,000 employees. [Databricks announcement](https://www.databricks.com/blog/2023/04/12/dolly-first-open-commercially-viable-instruction-tuned-llm).

## Reproducible bounded sample

The public, unauthenticated [original JSONL](https://huggingface.co/datasets/databricks/databricks-dolly-15k/resolve/bdd27f4d94b9c1f951818a7da7fd7aeea5dbff1a/databricks-dolly-15k.jsonl) was downloaded at immutable revision `bdd27f4d94b9c1f951818a7da7fd7aeea5dbff1a`. Its 13,085,339 bytes have SHA-256 `2df9083338b4abd6bceb5635764dab5d833b393b55759dffb0959b6fcbf794ec`. Parsing yielded 15,011 records; filtering category exactly to `closed_qa` or `summarization` yielded 2,961. Select the first twenty eligible records in original file order, retaining one-based original line numbers. This is a convenience sample, not random sampling and not an exhaustive search. The remainder was not semantically inspected.

Local evidence is ignored under `work/poteto/complementary/document/`. `sample-originals.jsonl` retains all original fields, including separate instruction/context/response. `screening-ledger.jsonl` retains original query and context separately, source category, provisional disposition, reason, and absent human review. `screen.py` reproduces the selection and the recorded manual judgments; it is not an automatic semantic annotator. Run `python3 work/poteto/complementary/document/screen.py`.

| Disposition | Original line numbers | Reason |
| --- | --- | --- |
| Conditional candidate: 3 | 7, 56, 85 | Original instruction explicitly invokes a reference text or paragraph. Retain the associated original context as an accessible attached passage; reading it is then the first required action. Without that preserved association, hold these rows. |
| Held: 2 | 41, 60 | Requests refer to the text, with reparations or Key Lime Pie as the topic, but do not clearly identify a particular passage. Human review must decide whether that is sufficient attachment reference under the existing guide. |
| Excluded from document supplement: 15 | 1, 5, 12, 19, 37, 49, 50, 66, 67, 71, 73, 76, 78, 80, 82 | No explicit document/passage reference in the original instruction. A factual topic or the source's QA/summarization category does not identify a document. Other Orchestra labels were not assigned. |

The three conditional candidates need a **preserved-attachment adapter**, not unchanged plug-in import. For each source record, classifier input remains exactly `instruction`; its original `context` becomes the associated accessible passage outside classifier input. The original schema already separates these fields, and the card explicitly identifies `context` as reference text. No query prefix, new document name, Wikipedia title, generated context, or answer is inserted. This is a proposed representation of an existing instruction–passage association, not an implemented retriever or accepted dataset.

This fits the existing contract's identified-passage and attached-document cases: a unique global document identifier is not required to infer that a query asking about its given paragraph must first read that paragraph. Line 7 explicitly invokes reference text about Lollapalooza; line 56 invokes its given paragraph when asking about Kia Stinger speed; line 85 invokes its given Billie Eilish paragraph. The attachment association supplies the exact passage, while the original query alone supplies the routing cue. Treating these as freestanding text after discarding their original context would instead warrant holding them. The fifteen bare questions remain excluded even with context present: an attachment must not silently create a source cue absent from the instruction. The two less explicit text references remain held pending human adjudication.

Original context hashes below are SHA-256 of the JSON-decoded `context` string encoded as UTF-8, without whitespace normalization; the full JSONL hash above additionally protects original serialization.

| Source line | Original context SHA-256 |
| --- | --- |
| 7 | `8ff3ae609ac3b759ee80689fef94543d5decb876931656dac7fcc2f9f2980fee` |
| 56 | `45e06c18aeaf2c49c61c4591063ea54723a09efe79fc4a31e2aa81d022760080` |
| 85 | `07a59bebf9ae98594697b85435fd6b279c165b72619d25ed5abe670ab6a7e42f` |

These are agent-proposed mappings conditional on the adapter and human review, not accepted labels or independent review evidence. No protocol modification is needed to express a retained attached passage, but any later adoption must document that representation explicitly and verify it is preserved.

The sample-originals SHA-256 is `16406cbb7cc7cba0f62ca51598975d03e94f32fd9d15bac628f2c78913360854`; ledger SHA-256 is `7f75871ca5ee828f1284d7828630d914945274b3e48e3f9bc23d7220a876d3fc`. There are twenty distinct original instructions in this selection. Related-source/paraphrase grouping has not been established; later adoption must inspect related passages and prevent source families crossing splits.

## License and provenance conditions

Dolly's card declares **CC BY-SA 3.0 Unported**, including Wikipedia material. Preserve its notices: **Copyright (2023) Databricks, Inc.** and **Copyright © Wikipedia editors and contributors.** Credit the dataset title, provider, source link, license, retained notices, and any changes. Missing per-row Wikipedia provenance remains a limitation; do not invent article revisions. [Pinned attribution section](https://huggingface.co/datasets/databricks/databricks-dolly-15k/blob/bdd27f4d94b9c1f951818a7da7fd7aeea5dbff1a/README.md).

The license permits sharing and adaptation, including commercial use, subject to attribution and applicable ShareAlike requirements. Distributed adaptations need the same or permitted compatible license; retain license links and avoid additional restrictions. Treat any distributed adapted data as CC BY-SA material rather than assuming Orchestra's MIT code license covers it. This does not establish a license requirement for learned model weights. [CC deed](https://creativecommons.org/licenses/by-sa/3.0/), [controlling legal code](https://creativecommons.org/licenses/by-sa/3.0/legalcode).

QMSum's saved repository notice is MIT, copyright 2021 Yale-LILY: copies or substantial portions retain the copyright and permission notice; the warranty disclaimer also remains in the saved original. Its hash is `8308d90c6321345cbd4adc8b479ddbece28ddbdca44f3f0b9bf033c3999a4a80`. This repository notice does not independently establish every upstream meeting transcript's rights.

No paid service, account, new dependency, schema change, source adoption, label change, or model experiment was needed. This inspection leaves source diversity, grouping, attribution completeness, human mapping review, and eventual sampling policy unresolved. A useful teach-back question is why a QA record with hidden reference context cannot automatically receive `document_retrieval` when its instruction only asks a general factual question.
