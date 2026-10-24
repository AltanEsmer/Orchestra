# Pilot AI consistency check

On October 24, 2026, Altan requested an AI reviewer with a persona while keeping his own labels as the fallback. A fresh `gpt-6.1-sol` reviewer with high reasoning received only the four-action guide and forty shuffled queries. Its instruction was to act as a skeptical annotation reviewer. It did not receive the original labels, rationales, groups, or chat history. This is a separate AI pass within the same model family, not an independent human annotation or cross-model-family validation.

## Observed result

All forty AI labels matched Altan's original labels: ten matches in each class. The reviewer marked all forty clear and found no exact duplicate text. This establishes consistency under the shared guide. It does not measure router accuracy, prove the labels correct, or demonstrate generalization. The original collection used agent-directed exercises and immediate feedback, which may also contribute to agreement.

The original labels and rationales remain unchanged in ignored `data/raw/pilot-intake.md` and the separate steward snapshot. At the initial check, the research ledger was empty. After the method choice, forty explicitly typed AI entries were recorded alongside the forty draft pilot rows; zero human-review entries or accepted research rows were invented. See the [method implementation](ai-assisted-review.md). Altan selected single-human annotation with disclosed AI checks later on October 24. The protocol and validator now support the dedicated `ai_assisted` kind, separate AI evidence, and actual human adjudications. The earlier forty matches remain AI consistency, never independent human agreement.

## Open adjudication and grouping work

The earlier q0033 flag remains open despite AI agreement: "holds 60 litres" can describe current contents or capacity. q0014 still needs review for similarity to a teaching example. Keep these checks visible instead of treating an AI vote as adjudication.

The blind reviewer independently flagged possible shared templates or sources: explanation pairs, per-unit multiplication requests, the Willow Hotel records, Northstar catalog requests, and pairs of document comparisons. These are grouping questions, not proven duplicates. Current provisional groups stay unchanged until their collection history and near-duplicate relationships are reviewed. Grouping limits leakage when related examples would otherwise enter both training and evaluation.

The manual-review packet samples two original labels per class using seed 42, then adds q0014 and q0033. One flagged row was already sampled, leaving nine queries. Its ordering is shuffled and its query file contains no original label or rationale. It was prepared for either legacy human method; no reviewer, date, or decision was invented. The later selected method uses the completed AI check and human adjudication of flagged cases. If Altan chooses delayed self-review, allow a full week after his last exposure to the selected labels and record the actual dates. Displaying the original answers again can invalidate that delay.

## Local evidence

All full queries and decisions remain under ignored `work/poteto/complementary/pilot-review/`.

| Artifact | Purpose |
| --- | --- |
| `prepare.py` | Extract the forty actual worksheet rows without rewriting them; reproduce the two blind packets and steward snapshot. |
| `ai-blind.jsonl` | Forty shuffled query IDs and exact texts only. SHA-256 `5ee0123f720f7450874b11fd0fc9d110e175d4b4cb0e322aff02bbf321d34441`. |
| `ai-decisions.jsonl` | Separate AI labels and rationales. SHA-256 `38975c4419f261270cc00b9458a120fecb2e7e2688e0294a3572f4ff658c4c81`. |
| `comparison.json` | Exact-ID comparison after the blind pass; forty matches and zero human review decisions. |
| `human-blind.jsonl` | Nine query IDs and texts only, ready if a human review method is selected. |
| `steward.json` | Original labels, rationales, provisional groups, worksheet hash, and sampling details. Keep hidden from a blind reviewer. |
| `notes.md` | AI grouping observations and boundary interpretations. |

Verification checked exact coverage of q0001 through q0040, byte-preserved query strings, ten original labels per class, blind packet fields, all forty comparisons, and empty research/review files at that initial checkpoint. The later ingestion state is recorded in the method implementation evidence. No training, guide freeze, or research result follows from this pass.
