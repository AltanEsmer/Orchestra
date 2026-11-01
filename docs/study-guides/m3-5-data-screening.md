# M3.5: finding usable public queries

Interim screening edition - October 31, 2026. This is a data-discovery lesson, not the completed M3.5 model-comparison guide.

## What changed

The supervisor asked for a larger research dataset. Altan set a preferred total of 4,000 accepted queries and a minimum of 2,500. We started from 400, with 100 per action. That means finding, reviewing and accepting another 3,600 or 2,100 rows. The accepted count is still 400 after this screening step.

Public sources contain many kinds of tasks. We need queries that fit Orchestra's question: which action must happen first? A dataset with thousands of questions may contribute few examples of that action. Source categories and function definitions cannot supply information that the router does not receive.

## Four different counts

- Source rows: everything in an upstream dataset, including answers, repeated scenarios and incompatible tasks.
- Screening candidates: unchanged requests that an AI screen provisionally judges compatible with the annotation guide.
- Accepted rows: examples whose provenance, labels, review and batch checks have actually passed.
- Independent groups: scenarios or sources that do not overlap across the training, validation and test partitions. Ten paraphrases do not automatically give ten independent examples.

## What the fresh samples show

The existing-source screen made 240 decisions. It found 151 provisional successes, not 151 accepted rows. Direct-answer samples passed 27/30 for Dolly and 27/30 for No Robots train. Passage samples passed 13/20 for Dolly closed QA, 7/20 for extraction and 1/20 for summarization. No Robots passage prompts passed 38/60 after separating the instruction and screening parent overlap. Remaining GSM8K questions passed 30/30, while BFCL's remaining calculation-filtered sample passed 8/30.

The new-source investigation screened ToolACE, SQL-create-context and Glaive. It found some provisional lookup and calculation examples but unresolved grouping and request-type concentration. The official xLAM data download was gated, so it has no measured yield. ToolACE and Glaive contain generated language; a public dataset is not necessarily a human-authored dataset. Exact counts, revisions, filters and exclusions live in the evidence notes.

<!-- pagebreak -->

## Why we cannot simply take the first 4,000

The current rules limit each scenario group to four rows, each source to 75% of a class, and each request type to 40% of a class. These limits protect against a model learning a few repeated patterns or recognizing the source instead of the first action. They do not prove that all source shortcuts are gone.

GSM8K illustrates the difference between supply and useful variety. Its sampled questions are numerical word problems. At 1,000 calculation rows, only 400 can have that request type. Sixteen existing GSM8K rows already use those slots, so at most 384 new word problems fit. At least 516 of the 900 new calculation rows must come from other request types. More word-problem datasets alone do not solve this constraint.

Lookup has a different difficulty. Many public questions need a database schema or earlier dialogue to identify the source. Those hidden fields are not router input. Adding "in the database" to a question would change its wording and potentially introduce a label cue. We keep the input contract and record the incompatibility instead.

## Trace one teaching query

"Calculate the increase using the figures in the attached report" is a document-retrieval request first. The query identifies the report, and the calculation depends on reading its figures. The router receives the request, not the attachment contents or expected action. The attachment is preserved separately. This example comes from the teaching protocol and is not a new research row.

If a public record merely asks a bare fact question, a hidden passage does not automatically make it retrieval. We assess the wording that the model will actually see. The No Robots adapter retains an exact instruction substring and records the separated passage; it does not invent a source reference.

## What the software establishes

The screening scripts pin input hashes, record deterministic seed-42 sample orders and save every AI verdict and exclusion reason. They compare candidate text computationally with the parent release and preserve all parent artifacts. The comparison is a conservative discovery filter; manual grouping still has to resolve related scenarios and common wording. The screening scripts do not train classifiers, accept labels, measure routing quality or open the sealed-test file for model development.

<!-- pagebreak -->

## Course connection and research limitations

Lecture 2, "Data Preprocessing and Feature Engineering", PDF page 8, asks how data were sampled, which data are relevant, and whether privacy issues exist before moving to modeling. The screen follows that sequence: establish relevant data and its limits before running more classifiers. The lecture does not mandate our four labels, numerical targets or quota percentages; those are project choices.

The lecture page was extracted and visually checked on October 31, 2026. File SHA-256: e7bfec9a9a52954c038e58a84f680e76648efa582ef79acafe2a3bfaa582217f. No course slide is reproduced in this guide.

The reported row-yield ranges describe a sampled pool under a simple binomial model. Related templates violate the idea that every row provides independent evidence. Therefore those ranges are not confidence intervals for accepted independent groups, and they cannot guarantee either target size. Public-data selection also changes the population relative to real user traffic. AI screening judgments and eventual AI checks are not independent human annotation agreement.

## Next evidence to obtain

- Audit source/scenario groups and collisions with all parent groups, then calculate cumulative source and request-type quotas. Lookup diversity is still a key unresolved gate.
- Record a concrete source/adapter decision and a new M3.5 collection brief before bulk import. Preserve the old hash-bound brief.
- Time the prepared 12-query human pilot with real labels and rationales. It has blank human fields and separate AI proposals. Its deliberately balanced selection is not a population-yield estimate.
- Keep the 2,500 minimum and 4,000 aim visible. Do not replace missing evidence with synthetic padding, invented human decisions or new test exposure.

## Practice before reading an answer

1. Why can a source with 60,000 rows still provide too few lookup examples for this project?
2. Why is a 30/30 screening result not proof that 1,000 accepted, independent examples are available?
3. Explain why the report example requires retrieval first, despite beginning with "Calculate".

These questions are unanswered. No learning status changes until Altan makes an actual attempt.

## Evidence to use in the report

The editable records are docs/evidence/m3-5-capacity-screen.md and docs/evidence/m3-5-lookup-screen.md. They contain primary-source links, pinned revisions, sample counts, judgments, local evidence paths and explicit limits. The supporting data and audit scripts remain in ignored work/m3-5-screen/. The source manifest and frozen M3 release are unchanged. This screening edition does not claim that M3.5 collection or the expanded classifier comparison is complete.
