# Single-human annotation with AI checks

On October 24, 2026, Altan selected: "Switch to single-human annotation with disclosed AI checks." This supersedes the earlier second-human/delayed-self requirement for the current study. His original labels remain the reference. The report must describe one human annotator, agent-assisted collection, and AI consistency checks. A persona is not another human annotator.

## Review contract

The existing ledger gains the `ai_assisted` discriminator. Legacy human entries retain their seven-field schema. AI entries add two fields:

- `ai_evidence` records model, task-prompt/guide manifest hash, blind-input hash, raw-output hash, judgment, and recorded flags.
- `human_adjudication` is null until needed, or records an actual original annotator's ID, date, label or explicit exclusion, and rationale.

Clear, unflagged AI matches retain the original human label. Every disagreement, abstention, exclusion proposal, or existing flag requires an actual human decision. Choosing the original label after a disagreement is still an adjudication. Unresolved AI records have a null resolution and fail readiness, including records prematurely marked excluded. The 120-row, 30-per-class, 15-groups-per-class, permission, and 20%-review-coverage requirements remain.

Human agreement excludes AI entries. An AI ledger adds separate `ai_consistency` counts, including abstentions as nonmatches. The validator rejects malformed evidence, missing fields, invalid dates/hashes, AI reviewer identities presented as original annotators, and unsupported adjudicator identities. These structural checks cannot establish that a claim is truthful. Actual prompt/input/output artifacts must be retained and checked during ingestion.

Two small designs were considered: shared run metadata in a separate manifest, or a discriminated ledger row with nested evidence. The nested form reuses the existing validator, status, and preparation interfaces. It repeats a few hashes but avoids a new file-loading interface across every caller. Local full artifacts remain separate; the ledger carries their hashes.

## Actual pilot ingestion

The forty original worksheet strings, labels, rationales, and provisional groups were copied into ignored `data/raw/pilot-v0.jsonl` without rewriting. All forty have `needs_review` status pending guide and grouping decisions, so accepted-row count remains zero. This status does not mean the AI found forty ambiguous queries. The AI matched all forty labels; the steward retained two specific unresolved flags, q0014 and q0033.

`data/raw/reviews-v1.jsonl` now holds forty `ai_assisted` entries. Thirty-eight unflagged matches retain the original label without a newly invented human adjudication. The two flagged entries have null resolution. No `second_human` or `delayed_self` decision is present. Human replies will be appended to the evidence and applied only to the relevant record.

Ignored `work/poteto/ai-assisted-review/` retains the exact delegated task text, the guide snapshots from commit `1bb6bc7` used during the blind pass, a prompt manifest, and ingestion evidence. The prompt manifest describes the supplied task and referenced guides; it does not claim to capture hidden system instructions. The original shuffled inputs and AI outputs remain under `work/poteto/complementary/pilot-review/`.

The ingestion script checked the preserved worksheet hash, identical forty-ID coverage, exact original query strings, and AI output associations before writing. It refuses to overwrite a nonempty pilot or ledger, preserving later human decisions. The initial draft hash is `b14892e35da118f6500fb9e59c76ce7090526afdb083c3716d1676186c131edb`; the initial AI ledger hash is `c2c9f80afbae4cab25066636db8dae7f9022aefe1cc48ede95e99bab76c5ce7a`. These identify the pre-adjudication snapshot, not any later human decisions.

## Verification

Focused regression tests failed before implementation and passed afterward. They cover the distinct AI schema, missing/malformed evidence, reviewer identities, abstentions, flagged matches, disagreements that attempt to default without human input, actual adjudication/exclusion, mixed human/AI metrics, and the 120-row readiness path through the CLI with artificial records. Legacy human fixtures still pass.

The actual local draft validator reports `PASS: 40 rows valid`, zero accepted rows, zero human reviews, and forty matching AI checks. This is a draft/evidence check, not M1 readiness or routing performance. The next real human action is one flagged-case decision, followed by remaining boundary and grouping decisions. No model training or final report findings have been produced.

Integrated checks passed: all 208 tests in 22.025 seconds, environment smoke, Ruff lint, formatting for 52 files, and whitespace checks. The desktop compiler successfully compiled the updated IEEE template. Two independent reviewers verified the actual artifact hashes/associations and ran the focused 48-validator/9-study test sets; both returned PASS. No research experiment was run.
