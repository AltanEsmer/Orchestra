# Annotation guide v1

Status: v1 frozen on October 26, 2026 after Altan’s pilot boundary and group decisions. The [data protocol](data-and-evaluation.md#prediction-contract) defines the first-action labels. The [pilot acceptance record](evidence/pilot-guide-v1.md) records 38 accepted pilot rows, two practice-only exclusions, and the unmet M1 collection requirements. This guide contains no full research query rows.

Follow the [experiment runbook](run-experiments.md) for local paths and readiness commands. Keep historical v0 decisions in the audit history. Future substantive changes require a new guide version and review of affected rows.

## Choose the first action

Read only the query text. Assume a named-document retriever, a structured knowledge lookup, and a calculator exist. Ask these questions in order and stop at the first decisive answer.

1. Can a reader choose an action from the text alone? If the request leaves out which document, item, or source it means, mark it `needs_review` with the reason "missing context". If it needs live or external information that none of the three tools provides, mark it `excluded`.
2. Which actions does the request need? Retrieval applies when the query identifies a document or passage to read. Lookup applies when it identifies a record in a structured source. Calculation applies when it asks for a numeric result. Direct answering applies when it asks for an explanation or rewrite that needs none of the tools.
3. If only one action applies, that action is the label.
4. If several apply, label the one whose output another action needs. Reading a report before calculating from its figures gives `document_retrieval`. If no action must come first, mark the query `needs_review` with the reason "no unique first action".

Record the result in one sentence of the form "First action is X because Y." For an excluded or unresolved query, the rationale gives the reason instead. Never put the label or the rationale into the query text.

## Write and group queries

Write new queries rather than copying the examples in the protocol, so those examples stay available for teaching. Use fictional documents, catalogs, people, and records. Vary wording so one trigger word does not identify a label. Include hard negatives, such as a query that mentions numbers but asks for an explanation. Keep numbers and negations as written.

A group is a **shared request template: the same user goal solved by the same procedure, whatever the scenario**. A shared label, keyword, arithmetic operation, or setting alone does not establish a group. Compare the requested goal, required inputs, procedure, and output. Different first-action dependencies can occur within one family when the core template is shared, as in translation of supplied text versus document text. Preserve each first-action label.

Use this rule for both earlier and future families. Ordering and selection form one recorded family; amount-per-unit scaling forms another. Geometry, equal allocation, averaging, and percentage discounts retain separate templates. Checklist transformation stays separate from summarization because it preserves the required steps as actions rather than selecting and shortening content. Quotation and specific guidance from an identified document share the recorded content-extraction family. Concept explanations include explanations of differences. Key-based record existence and field retrieval share a family; condition-based filtering is separate. Brainstorming, storytelling, and social messages remain separate writing goals.

These conservative families reduce the number of independent groups. Report achieved group counts rather than treating every distinct text as independent. Keep at most four research rows per family. A related fifth query stays in the audit/practice collection with its real family relationship and exclusion reason; do not give it another research group just to evade the cap. Whole research groups move together between splits.

## Row format

Store pilot rows locally in ignored `data/raw/pilot-v0.jsonl`, one JSON object per line. Every row has all nine fields from the [protocol](data-and-evaluation.md#planned-row-format-and-validation). Keep queries out of Git and archive them with hashes when accepted.

| Field | Convention for the pilot |
| --- | --- |
| `query_id` | `q0001`, `q0002`, and so on. Never reuse a retired ID. |
| `group_id` | `g001`, `g002`, and so on, one per scenario. |
| `label` | One of the four labels for `accepted` rows, or `null`. |
| `status` | `accepted`, `needs_review`, or `excluded`. |
| `source_id` | `altan-authored`, defined in `data/manifests/sources.json`. |
| `annotator_ids` | `["A1"]` for Altan. A second annotator becomes `A2`. Contact details never enter the data. |
| `annotation_version` | `guide-v0` during the pilot, then `guide-v1` (current). |

Check the file after each writing session:

```sh
uv run --locked python scripts/validate_dataset.py data/raw/pilot-v0.jsonl
```

The validator rejects missing fields, duplicate IDs, empty text, unknown labels, accepted rows without a label, unknown sources, sources without an author or date, exact duplicate text, and groups larger than four. A missing license passes this check and fails the readiness check below. It also prints status, label, and group counts and lists groups with more than one accepted label for review. It does not judge whether a label is correct.

## Pilot review

The forty-query pilot is written and its permission recorded. Altan chose single-human annotation with disclosed AI checks on October 24. Preserve his original label/rationale, present shuffled query-only inputs to the AI reviewer, and record AI provenance separately. Check at least 20 percent per original class plus all ambiguous/mixed-label cases. The completed AI pass covers all forty rows.

Clear agreement with no flags can retain the original label. Ask Altan to adjudicate every disagreement, abstention, exclusion proposal, and previously flagged case. Keeping the original label after disagreement is still an actual human decision that must be recorded. A persona is not a second human; report AI consistency and single-annotator limitations. The pilot boundary and group decisions are complete under v1. The previous second-human/delayed-self alternatives remain supported, but are not the selected method.

The legacy human ledger example below applies only when that method is explicitly used. AI rows use the discriminator and extra evidence fields in the [current protocol](data-and-evaluation.md#review-ledger-and-readiness):

```json
{"query_id": "q0001", "original_label": "calculation", "review_label": "direct_answer", "reviewer_id": "r1", "review_date": "2026-10-20", "review_kind": "second_human", "resolved_label": "calculation"}
```

For the legacy example, `review_kind` is `second_human` or `delayed_self`; all seven fields are required. AI entries instead use `ai_assisted`, `ai_evidence`, and `human_adjudication`. A `second_human` reviewer must not be listed in the row's `annotator_ids`. `resolved_label` must match the released dataset label, or be null if the row was excluded after review. Every accepted row in a mixed-label group needs an entry. AI evidence must retain known ambiguity flags. Check by hand that every flagged row has an actual human resolution. Check it with `uv run --locked python scripts/validate_dataset.py DATASET --review LEDGER`, and add `--ready` for the M1 acceptance checks. Human agreement excludes AI entries. AI consistency is reported separately.

Preserve each pre-adjudication label before discussing differences. For each disagreement, note both labels, the resolved label, and whether this guide needs a clearer rule. Record future guide changes under a new version and review affected rows before another release.

## Recorded pilot boundaries

The default direct-answer rule for a stable fact without a named structured source remains unchanged. Public sources require their own permission and mapping records; Altan’s pilot permission covers q0001 through q0040 only. Preserve all original rows, labels, rationales, actual adjudications, and group changes in the local audit history. Keep practice-only rows outside supervised splits.

Flag the shared word “handbook” in the summary/checklist cases for later validation error analysis. This is a prospective word-level cue to inspect, not a measured shortcut or a reason to alter text. Record any observations against actual validation predictions; do not inspect the sealed test to tune wording or groups.
