# Annotation guide v0

Status: draft for the M1 pilot, prepared on October 16, 2026. Altan freezes v1 after the 40-query pilot review. The [data protocol](data-and-evaluation.md#prediction-contract) defines the labels and remains authoritative if this guide disagrees with it. This guide turns those definitions into a repeatable procedure. It contains no dataset rows.

The October 16 [M1 to M3 plan](m1-m3-plan.md#resolve-the-data-decisions-without-guessing-evidence) proposes answers to the open workflow decisions without claiming pilot evidence. Implementation was approved on October 16. Keep v0 until the required review and permissions exist. Follow the [experiment runbook](run-experiments.md) for the local intake worksheet, readiness gate, and commands. Store actual rows under ignored `data/raw/`, because `data/annotation/` is not ignored.

## Choose the first action

Read only the query text. Assume a named-document retriever, a structured knowledge lookup, and a calculator exist. Ask these questions in order and stop at the first decisive answer.

1. Can a reader choose an action from the text alone? If the request leaves out which document, item, or source it means, mark it `needs_review` with the reason "missing context". If it needs live or external information that none of the three tools provides, mark it `excluded`.
2. Which actions does the request need? Retrieval applies when the query identifies a document or passage to read. Lookup applies when it identifies a record in a structured source. Calculation applies when it asks for a numeric result. Direct answering applies when it asks for an explanation or rewrite that needs none of the tools.
3. If only one action applies, that action is the label.
4. If several apply, label the one whose output another action needs. Reading a report before calculating from its figures gives `document_retrieval`. If no action must come first, mark the query `needs_review` with the reason "no unique first action".

Record the result in one sentence of the form "First action is X because Y." For an excluded or unresolved query, the rationale gives the reason instead. Never put the label or the rationale into the query text.

## Write and group queries

Write new queries rather than copying the examples in the protocol, so those examples stay available for teaching. Use fictional documents, catalogs, people, and records. Vary wording so one trigger word does not identify a label. Include hard negatives, such as a query that mentions numbers but asks for an explanation. Keep numbers and negations as written.

A group is one scenario. Paraphrases and small variants of the same request share a `group_id`, even when they were written on different days. Keep at most four rows per group. Groups move between splits as a whole, so a group that is too large removes data from evaluation.

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
| `annotation_version` | `guide-v0` during the pilot, then `guide-v1`. |

Check the file after each writing session:

```sh
uv run --locked python scripts/validate_dataset.py data/raw/pilot-v0.jsonl
```

The validator rejects missing fields, duplicate IDs, empty text, unknown labels, accepted rows without a label, unknown sources, sources without an author or date, exact duplicate text, and groups larger than four. A missing license passes this check and fails the readiness check below. It also prints status, label, and group counts and lists groups with more than one accepted label for review. It does not judge whether a label is correct.

## Pilot review

The forty-query pilot is written and its permission recorded. Altan chose single-human annotation with disclosed AI checks on October 24. Preserve his original label/rationale, present shuffled query-only inputs to the AI reviewer, and record AI provenance separately. Check at least 20 percent per original class plus all ambiguous/mixed-label cases. The completed AI pass covers all forty rows.

Clear agreement with no flags can retain the original label. Ask Altan to adjudicate every disagreement, abstention, exclusion proposal, and previously flagged case. Keeping the original label after disagreement is still an actual human decision that must be recorded. A persona is not a second human; report AI consistency and single-annotator limitations. Freeze v1 after boundary and group decisions. The previous second-human/delayed-self alternatives remain supported, but are not the selected method.

The legacy human ledger example below applies only when that method is explicitly used. AI rows use the discriminator and extra evidence fields in the [current protocol](data-and-evaluation.md#review-ledger-and-readiness):

```json
{"query_id": "q0001", "original_label": "calculation", "review_label": "direct_answer", "reviewer_id": "r1", "review_date": "2026-10-20", "review_kind": "second_human", "resolved_label": "calculation"}
```

For the legacy example, `review_kind` is `second_human` or `delayed_self`; all seven fields are required. AI entries instead use `ai_assisted`, `ai_evidence`, and `human_adjudication`. A `second_human` reviewer must not be listed in the row's `annotator_ids`. `resolved_label` must match the released dataset label, or be null if the row was excluded after review. Every accepted row in a mixed-label group needs an entry. AI evidence must retain known ambiguity flags. Check by hand that every flagged row has an actual human resolution. Check it with `uv run --locked python scripts/validate_dataset.py DATASET --review LEDGER`, and add `--ready` for the M1 acceptance checks. Human agreement excludes AI entries. AI consistency is reported separately.

Preserve each pre-adjudication label before discussing differences. For each disagreement, note both labels, the resolved label, and whether this guide needs a clearer rule. Revise this guide, then freeze it as v1 and relabel affected rows.

## Decisions for Altan before v1

| Decision | Why it matters |
| --- | --- |
| Does a general-knowledge fact such as a country's capital count as `direct_answer` or need `knowledge_lookup`? | The protocol limits lookup to an identified structured source, so these queries currently fall under `direct_answer`. The pilot should test whether that rule is easy to apply. |
| Which flagged cases and groups need resolution? | The single-human, AI-assisted method is selected. Record actual human decisions and disclose single-annotator bias. |
| Which license applies to additional sources? | Altan's exact permission for q0001–q0040 is recorded. Public examples retain their own notices and restrictions; the pilot permission does not cover them. |
| How are full rows retained? | Keep queries, original labels, and review evidence in ignored local storage; retain hashes and the eventual verified study archive. No raw-data publication is part of this preparation. |
