# Annotation guide v1

Status: v2 frozen on October 26, 2026. v2 changes only the grouping rule: Altan asked for simpler, less strict grouping that keeps quality checks, so groups now follow shared scenarios and sources instead of request templates. First-action labels and boundaries are unchanged from v1. The [guide-v2 record](evidence/guide-v2.md) lists the pilot regrouping; the [v1 record](evidence/pilot-guide-v1.md) keeps the earlier decisions. This guide contains no full research query rows.

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

A group holds rows a model could memorize across splits. Put two rows in the same group when any of these is true:

1. **Small variation.** One is a paraphrase of the other, or the same sentence with a few words or numbers swapped.
2. **Same source or setting.** They name or attach the same document, passage, database, catalog, table, or named place or organization (for example, two Willow Hotel database queries, or a Willow Hotel and a Willow School query).
3. **Same situation.** They describe the same specific people, objects, or numbers.
4. **Same public record.** They come from one upstream record, share one attached passage, or query one named table.

Otherwise, keep rows in separate groups. A shared request type, label, keyword, or arithmetic operation alone does not join rows. Groups may mix labels. Keep at most four research rows per group; a related fifth row goes to the practice collection with its reason. Whole groups move together between splits.

### Quality checks for every batch

- **Duplicates.** Reject exact duplicates (the validator does this) and check near-duplicates by hand before assigning groups.
- **Request-type spread.** Note each row's request type (for example, "answer a question from a passage" or "filter records by a condition") in the import worksheet. No single request type should exceed 40 percent of a class's accepted rows.
- **Source mix.** Report rows by source and class. Each class should draw on at least two sources, and no single source should supply more than 75 percent of a class, so that a source's phrasing does not become the label cue.
- **Label review.** The selected AI-assisted method applies unchanged: AI checks of every new row, and Altan's decision on every flag or disagreement.

The v1 request-template families remain in the audit history. An optional analysis can report scores on request types absent from training; it is not a release gate.

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
| `annotation_version` | `guide-v0` during the pilot, `guide-v1`, then `guide-v2` (current). |

Check the file after each writing session:

```sh
uv run --locked python scripts/validate_dataset.py data/raw/pilot-v0.jsonl
```

The validator rejects missing fields, duplicate IDs, empty text, unknown labels, accepted rows without a label, unknown sources, sources without an author or date, exact duplicate text, and groups larger than four. A missing license passes this check and fails the readiness check below. It also prints status, label, and group counts and lists groups with more than one accepted label for review. It does not judge whether a label is correct.

## Pilot review

The forty-query pilot is written and its permission recorded. Altan chose single-human annotation with disclosed AI checks on October 24. Preserve his original label/rationale, present shuffled query-only inputs to the AI reviewer, and record AI provenance separately. Check at least 20 percent per original class plus all ambiguous/mixed-label cases. The completed AI pass covers all forty rows.

Clear agreement with no flags can retain the original label. Ask Altan to adjudicate every disagreement, abstention, exclusion proposal, and previously flagged case. Keeping the original label after disagreement is still an actual human decision that must be recorded. A persona is not a second human; report AI consistency and single-annotator limitations. The pilot boundary decisions are complete under v1, and its groups were reassigned under v2. The previous second-human/delayed-self alternatives remain supported, but are not the selected method.

The legacy human ledger example below applies only when that method is explicitly used. AI rows use the discriminator and extra evidence fields in the [current protocol](data-and-evaluation.md#review-ledger-and-readiness):

```json
{"query_id": "q0001", "original_label": "calculation", "review_label": "direct_answer", "reviewer_id": "r1", "review_date": "2026-10-20", "review_kind": "second_human", "resolved_label": "calculation"}
```

For the legacy example, `review_kind` is `second_human` or `delayed_self`; all seven fields are required. AI entries instead use `ai_assisted`, `ai_evidence`, and `human_adjudication`. A `second_human` reviewer must not be listed in the row's `annotator_ids`. `resolved_label` must match the released dataset label, or be null if the row was excluded after review. Every accepted row in a mixed-label group needs an entry. AI evidence must retain known ambiguity flags. Check by hand that every flagged row has an actual human resolution. Check it with `uv run --locked python scripts/validate_dataset.py DATASET --review LEDGER`, and add `--ready` for the M1 acceptance checks. Human agreement excludes AI entries. AI consistency is reported separately.

Preserve each pre-adjudication label before discussing differences. For each disagreement, note both labels, the resolved label, and whether this guide needs a clearer rule. Record future guide changes under a new version and review affected rows before another release.

## Recorded pilot boundaries

The default direct-answer rule for a stable fact without a named structured source remains unchanged. Public sources require their own permission and mapping records; Altan’s pilot permission covers q0001 through q0040 only. Preserve all original rows, labels, rationales, actual adjudications, and group changes in the local audit history. Keep practice-only rows outside supervised splits.

Flag the shared word “handbook” in the summary/checklist cases for later validation error analysis. This is a prospective word-level cue to inspect, not a measured shortcut or a reason to alter text. Record any observations against actual validation predictions; do not inspect the sealed test to tune wording or groups.
