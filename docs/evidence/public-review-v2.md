# Guide-v2 import: labels and blind AI check

On October 26, 2026, Altan replied "Approve all proposed labels in the review worksheet." The 90 [import candidates](public-import-v2.md) took the agent's proposed labels as primary labels under annotator A1. Each rationale ends with "Agent proposal approved by A1 on 2026-10-26." These are agent-proposed, human-confirmed labels. Approving proposals risks anchoring: Altan saw the agent's answer before deciding, and the 27 worksheet flags were shown to him at the same time.

## Blind AI check

A fresh subagent got only the guide sections on labels and grouping, the Dolly attachment paragraph, and the 90 queries, shuffled with `random.Random(2026)` under new IDs b001–b090. Each query had its text and an attached-passage yes/no, nothing more. The subagent saw no label, rationale, group, source, or chat history.

The reviewer was `claude-opus-5-5`, not the `gpt-6.1-sol` that the [pilot check](pilot-ai-review.md) used. It is the same model family as the agent that proposed the labels, so its agreement is a consistency check, not independent validation, and certainly not human agreement.

| Result | Rows |
| --- | ---: |
| AI label matches the primary label | 90 of 90 |
| AI judgment clear / ambiguous / exclude | 76 / 14 / 0 |
| Clear and unflagged, accepted | 35 |
| Ambiguous or flagged, pending Altan's adjudication | 55 |

Clear, unflagged matches keep the primary label and become `accepted`. Under the [AI-assisted method](ai-assisted-review.md), every other row needs Altan's decision, even when the label agrees.

The combined file now holds 73 accepted rows (38 pilot, 35 new) and 55 `needs_review`. The validator passes all 128 rows. The readiness check fails as expected, on the 55 pending adjudications and on class counts.

## The 55 pending rows

The local `data/raw/import-v2/adjudication-worksheet.md` lists each row with its flags and the agent's recommendation. The recommendations are not decisions.

| Category | Rows | Agent recommendation |
| --- | ---: | --- |
| Informational flag | 39 | Keep label and group. The flags note a shared template (allowed across groups in v2), wording to keep ("without quoting", "them"), drafting rather than sending, or a lookup before a calculation. |
| Stable fact, no named source | 7 | Keep `direct_answer` under the guide's default rule (q0117–q0121, q0128, q0130). |
| Record ID, source not named | 4 | Keep `knowledge_lookup`. A record ID can only be answered from a stored record (q0066, q0067, q0070, q0084). |
| Live or sensitive record | 3 | Keep `knowledge_lookup`. The IDs are synthetic benchmark text, and the router does not run the lookup (q0065, q0068, q0069). Excluding all three leaves lookup at 29 rows. |
| Near-duplicate in another group | 2 | Merge under guide v2 rule 1: q0098 into g101 (both cosine similarity of two five-number vectors) and q0076 into g081 (same "include only those … whose names are listed in the columns" frame). Labels unchanged. |

If every recommendation is accepted, the projected counts are calculation 32 rows/31 groups, document retrieval 31/30, lookup 32/25, and direct answer 33/30.

## Adjudication

Altan replied "Accept recommendations for all 55 flagged rows in the adjudication worksheet." Each of the 55 ledger entries now records `human_adjudication` by A1 on 2026-10-26, with the category rationale and "Agent recommendation accepted by A1 on 2026-10-26." No label changed and nothing was excluded. q0098 moved to g101 and q0076 to g081. Accepting recommendations in one reply carries the same anchoring risk as the label approval.

| Label | Rows | Groups | Largest source |
| --- | ---: | ---: | --- |
| calculation | 32 | 31 | 72% BFCL |
| document_retrieval | 31 | 30 | 71% Dolly |
| knowledge_lookup | 32 | 25 | 69% BFCL |
| direct_answer | 33 | 30 | 70% No Robots |

All 128 rows are accepted, in 108 groups (largest group four rows). `validate_dataset.py --ready` with `reviews-v2.jsonl` passes: "M1 readiness checks passed (128 accepted rows, 128 reviewed)". No two rows in different groups reach 0.5 token overlap. Every class has two sources, none above 75 percent. Merges changed no request type, so the projected request-type spread (largest 39 percent) still holds. All 128 ledger entries are AI checks, so the readiness pass reports AI consistency (128 of 128), not human agreement.

After adjudication: `data/raw/m1-v2.jsonl` SHA-256 `3e02b6fa8a7c1987a44a6a9ae1c118bac768be16ad05c58d2948880b87633b2e`; `data/raw/reviews-v2.jsonl` SHA-256 `5c449ce1f234490f351e1be7b1843346f46d9c1466136a0b14d5ddb6eb6c2de8`. `apply_adjudication.py` checks the data, ledger, proposal, and worksheet hashes before writing, and `adjudication-2026-10-26.json` keeps the exact reply.

## Freeze

Altan replied "Freeze the M1 release as data/processed/m1-v1.jsonl with the reviews-v2 ledger." The agent copied `data/raw/m1-v2.jsonl` byte for byte to `data/processed/m1-v1.jsonl` and made it and `data/raw/reviews-v2.jsonl` read-only. Readiness on the frozen file with that ledger passes: "M1 readiness checks passed (128 accepted rows, 128 reviewed)".

| Frozen input | SHA-256 |
| --- | --- |
| `data/processed/m1-v1.jsonl` | `3e02b6fa8a7c1987a44a6a9ae1c118bac768be16ad05c58d2948880b87633b2e` |
| `data/raw/reviews-v2.jsonl` | `5c449ce1f234490f351e1be7b1843346f46d9c1466136a0b14d5ddb6eb6c2de8` |
| `data/manifests/sources.json` | `67cfe73fa3517a87175ebc24f14fdbaeb2566023d1e21f58fc10b6d32c7f7420` |
| `docs/annotation-guide.md` (guide v2) | `dd78162cbf9dcbdaaa68f4ad0bd654aec8d1ea181fb453362d9ab1dcdcc8ba55` |

Groups and labels are now fixed. Any later change needs a new release name. Dolly passages stay in `data/raw/import-v2/attachments.jsonl`. They are not router input and not part of the release file. No split exists and no model has run.

## Local evidence

Everything here is in ignored `work/poteto/public-import/` or `data/raw/`.

| File | SHA-256 |
| --- | --- |
| `approval-2026-10-26.json` (exact message, annotator, worksheet hash) | worksheet `a4735e07…7902` |
| `ai-blind.jsonl` | `f61897ec8c3ded3a2a75b79c0708106a6d817195db842fe38c2998954e203114` |
| `review-task.txt` | `c546947c96d8363c4780ee20799bf3d03fe0c2bb0b7a6567cf863a67d9f9271a` |
| `ai-decisions.jsonl` | `bb018572dd98a4485ae94c3219a3eb0e56d29184570451abb727d0881b2791d2` |
| `data/raw/m1-v2.jsonl` after ingestion | `45c85d18c0f0b911bee97f6ed6ea4a2eda8e656e8ee04844cbdd196f7c99fe25` |
| `data/raw/reviews-v2.jsonl` (38 pilot + 90 new AI entries) | `afec567b2cb0cf033175acd64b448cde6615da3b6e0d333817a1e49f769ca5ed` |
| `adjudication-proposal.json` | `f911fea59004c97b4e3a4a8c8ff8ff43d72ac9804677a4c9132ce7bb50100331` |
| `data/raw/import-v2/adjudication-worksheet.md` | `e621c49799af116d457bef25551152bb5f6ba576b09dd7ae405dcce2f2735941` |

`ingest_ai.py` checks the data, blind-input, and task hashes. It refuses to overwrite an existing `reviews-v2.jsonl` and checks that each blind ID appears once with matching text. Nothing is frozen and no split exists. No model has run.
