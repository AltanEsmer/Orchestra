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

## First human adjudication, October 25, 2026

Altan clarified: "I meant 60 litres currently inside the tank." The q0033 ledger entry now records A1’s actual dated adjudication retaining `calculation`: the starting quantity and amount used are supplied. The original text, label, rationale, group, AI evidence, and historical flag are preserved. The other thirty-nine ledger entries are unchanged. The ignored `work/poteto/ai-assisted-review/q0033-adjudication-2026-10-25.json` retains the full reply and ledger hashes before and after this decision.

One flagged case, q0014’s similarity to a teaching example, remains without adjudication. All forty draft rows remain `needs_review` until guide and grouping decisions are complete; accepted count is still zero. The next question concerns whether q0014 was adapted from that example or written independently.

## Teaching-example origin confirmed, October 25, 2026

Altan stated: "I adapted it from the teaching example. Record that and guide me through what we should do with it next." This confirms q0014’s origin. The exact reply and unchanged dataset/ledger hashes are retained in ignored `work/poteto/ai-assisted-review/q0014-provenance-2026-10-25.json`. The annotation guide reserves teaching examples for practice; the learning log already excludes their paraphrases from the study. Recommended treatment is exclusion from research, retaining the original record for practice and provenance.

Altan has confirmed origin, but has not yet explicitly chosen exclusion. q0014 therefore remains pending with null human adjudication and resolution. No query, original label, group, or AI evidence changed. After the actual treatment decision, grouping review remains before guide v1 and acceptance.

## Teaching-example exclusion recorded, October 25, 2026

Altan explicitly requested exclusion of q0014 from research and retention for practice. Its row now has `excluded` status with the reason; its original query, label, group, source, and guide version are retained. The original complete row, including its original routing rationale, is preserved in ignored `work/poteto/ai-assisted-review/q0014-exclusion-2026-10-25.json` with the exact reply and before/after dataset and ledger hashes. Its ledger retains both original and AI labels, and records A1’s dated exclusion with a null adjudicated/resolved label. The other thirty-nine dataset and review entries are unchanged.

Both individual flags have actual human adjudications. There are 39 pending candidates, one excluded practice record, and zero accepted rows. Grouping remains provisional. First shared-group review is g002: the return-policy and safety-rule handbook summaries; retaining one template family is proposed, awaiting Altan’s answer. No source adoption, guide freeze, or model run occurred.

## First group confirmed, October 25, 2026

Altan kept q0002 and q0007 in g002 because they share the same template with different handbooks and topics. The exact reply, member IDs, date, and current dataset/ledger hashes are retained in ignored `work/poteto/ai-assisted-review/g002-group-decision-2026-10-25.json`. Existing membership already implements that decision; dataset and label-review ledger bytes are unchanged. Group decisions are recorded separately from first-action label adjudications.

The next shared group is g004, q0004 and q0008, both explaining a difference in simple terms. Its review is pending. Confirming g002 does not freeze all groups, accept rows, or establish a complete leakage audit.

## Difference-explanation group confirmed, October 25, 2026

Altan kept q0004 and q0008 together in g004 because they use the same “explain the difference” template with different topics. The exact reply, member IDs, date, and unchanged dataset/ledger hashes are retained in ignored `work/poteto/ai-assisted-review/g004-group-decision-2026-10-25.json`. No dataset or label-review ledger rewrite was needed. g002 and g004 have actual human group decisions. Next is g005’s ticket-cost, track-distance, and flour-quantity requests; its treatment and remaining cross-group checks are pending. Counts remain 39 pending, one excluded, zero accepted.

## Amount-per-unit group confirmed, October 25, 2026

Altan kept q0005, q0012, and q0029 together in g005 because they share an amount-per-unit times number-of-units pattern in different situations. The exact reply, member IDs, date, and unchanged dataset/ledger hashes are retained in ignored `work/poteto/ai-assisted-review/g005-group-decision-2026-10-25.json`. Existing membership already matches, so no dataset or label-review ledger rewrite was needed. g002, g004, and g005 have actual human group decisions. Next is g007’s politeness and shortening requests; its treatment and cross-group checks remain pending. Counts remain 39 pending, one excluded, zero accepted.

## Provided-sentence rewriting group confirmed, October 25, 2026

Altan kept q0009 and q0018 together in g007 because both rewrite a supplied sentence, despite different transformations. The exact reply, member IDs, date, and unchanged dataset/ledger hashes are retained in ignored `work/poteto/ai-assisted-review/g007-group-decision-2026-10-25.json`. Existing membership already matches; dataset and label-review ledger bytes are unchanged. This is a conservative family decision within rewriting, not a rule to group all direct answers. Confirmed shared groups are g002, g004, g005, and g007. Next is g015, the last currently multi-row group; singleton and cross-group similarity checks remain pending. Counts remain 39 pending, one excluded, zero accepted.

## Two-document comparison group confirmed, October 25, 2026

Altan kept q0019 and q0031 together in g015 because both compare information from two documents on different topics. The exact reply, member IDs, date, and unchanged dataset/ledger hashes are retained in ignored `work/poteto/ai-assisted-review/g015-group-decision-2026-10-25.json`. Existing membership already matches. All five existing multi-row groups now have actual human keep-together decisions; dataset and label-review ledger bytes remain unchanged.

The cross-group audit starts with q0003/g003, q0011/g009, and q0016/g013. These each request a field from an identified structured record; a shared family is proposed for human review, not yet applied. Other cross-group checks and guide v1 remain open. Counts remain 39 pending, one excluded, zero accepted; no research split or model run exists.

## Single-record lookup families merged, October 25, 2026

Altan explicitly merged q0003, q0011, and q0016 because each asks for one piece of information from a specific catalog/database record. They now share g003. Only q0011 and q0016 changed group IDs; g009 and g013 are retired, with their previous mapping, exact reply, and before/after hashes preserved in ignored `work/poteto/ai-assisted-review/g003-merge-decision-2026-10-25.json`. All other fields and rows, plus the entire label-review ledger, are unchanged. No split exists to be moved. There are now 32 provisional groups including the excluded practice record’s group; this is not an independent-group acceptance count.

Next is q0024/g020 versus q0040/g034: ordering a book list versus selecting the earliest booking. That decision and remaining cross-group checks are pending. Counts remain 39 pending, one excluded, zero accepted.

## Record-ordering families merged, October 25, 2026

Altan kept q0024 and q0040 together because both order records by a field, despite returning a sorted list versus one earliest record. They now share g020. Only q0040 changed group ID; g034 is retired. The exact reply, previous mapping, and before/after hashes are retained in ignored `work/poteto/ai-assisted-review/g020-merge-decision-2026-10-25.json`. All other dataset fields and rows and the entire label-review ledger are unchanged. There are now 31 provisional groups including the excluded practice group, not 31 accepted independent groups.

Next is q0020/g016 versus q0032/g026, listing records matching a condition versus counting matching records. Its decision and remaining cross-group checks are pending. Counts remain 39 pending, one excluded, zero accepted; no research split or experiment exists.

## Record-filtering families merged, October 25, 2026

Altan merged q0020 and q0032 because both filter records by a condition, despite listing versus counting matches. They now share g016; only q0032 changed group ID, and g026 is retired. The exact reply, prior mapping, and before/after hashes are retained in ignored `work/poteto/ai-assisted-review/g016-merge-decision-2026-10-25.json`. All other dataset fields and rows and the complete label-review ledger are unchanged. There are 30 provisional groups including the excluded practice group, not 30 accepted independent groups.

Altan requested an explanation of the review’s purpose. Grouping controls related-template overlap between splits; first-action labels remain a separate decision. These are conservative family choices, not proof of exact duplication. Next is q0023/g019 versus q0026/g022: translation from a missing document versus translation of supplied text. Their differing labels are preserved; no grouping decision is inferred. Counts remain 39 pending, one excluded, zero accepted.

## Translation family merged across labels, October 25, 2026

Altan merged q0023 and q0026 because both request translation despite different source dependencies. They now share g019; only q0026 changed group ID, and g022 is retired. The exact reply, prior mapping, and before/after hashes are retained in ignored `work/poteto/ai-assisted-review/g019-merge-decision-2026-10-25.json`. All other fields/rows and the label-review ledger are unchanged. q0023 remains `document_retrieval`; q0026 remains `direct_answer`. Both already have review entries, as required for later mixed-label-group acceptance. This records grouping, not another label adjudication. There are 29 provisional groups including the excluded practice group, not 29 accepted independent groups.

Next is q0034’s supplied-word sorting versus g020’s record ordering. That decision and remaining cross-group checks are pending. Counts remain 39 pending, one excluded, zero accepted; no research split or experiment exists.

## Supplied-word sorting added to ordering family, October 25, 2026

Altan added q0034 to g020 because it also sorts items despite receiving its words directly. g020 now contains q0024, q0034, and q0040. Only q0034 changed group ID; g028 is retired. Its `direct_answer` label and the others’ `knowledge_lookup` labels are preserved. All three have AI review entries. The exact reply, prior mapping, and before/after hashes are retained in ignored `work/poteto/ai-assisted-review/g020-add-q0034-decision-2026-10-25.json`. Other dataset fields/rows and the full label-review ledger are unchanged. There are 28 provisional groups including the excluded practice group, not 28 accepted independent groups.

Next is q0010/g008 versus q0027/g023: specific guidance from named camp documents. Their grouping and other cross-group checks remain pending. Counts remain 39 pending, one excluded, zero accepted; no split or experiment exists.

## Document-guidance families merged, October 25, 2026

Altan merged q0010 and q0027 because both ask for specific guidance from a named document about things to bring. They now share g008; only q0027 changed group ID, and g023 is retired. The exact reply, previous mapping, and before/after hashes are retained in ignored `work/poteto/ai-assisted-review/g008-merge-decision-2026-10-25.json`. Other fields/rows and the full label-review ledger are unchanged. There are 27 provisional groups including the excluded practice group, not 27 accepted independent groups.

Next is q0006’s lookup-before-cost request versus g005’s amount-per-unit family. Its decision is pending; g005 has three rows and the cap is four. The q0037 conversion relation must also be resolved before freezing groups; a cap cannot justify putting related variants into separate split families. Counts remain 39 pending, one excluded, zero accepted; no research split or experiment exists.

## Lookup-before-cost added to amount-per-unit family, October 25, 2026

Altan added q0006 to g005 because it shares the price-times-quantity pattern despite requiring lookup first. g005 now contains q0005, q0006, q0012, and q0029, reaching the four-row cap. Only q0006 changed group ID; g006 is retired. Its `knowledge_lookup` label and the others’ calculation labels are preserved. All four have AI review entries. The exact reply, previous mapping, and before/after hashes are retained in ignored `work/poteto/ai-assisted-review/g005-add-q0006-decision-2026-10-25.json`. Other fields/rows and the entire review ledger are unchanged. There are 26 provisional groups including the excluded practice group, not 26 accepted independent groups.

Next is q0037’s explicit unit conversion versus this family. Semantic relatedness must be decided independently of the cap. If related, excess-row handling needs an explicit decision before a structurally valid merge; do not invent separate families to fit the cap. Counts remain 39 pending, one excluded, zero accepted; no split or experiment exists.

## Fifth amount-per-unit family member confirmed, October 25, 2026

Altan confirmed q0037 belongs to g005’s family because it also multiplies an amount by a per-unit factor. The exact reply, all five family IDs, date, and unchanged dataset/ledger hashes are retained in ignored `work/poteto/ai-assisted-review/g005-q0037-family-decision-2026-10-25.json`. The semantic relationship is recorded; the JSONL merge is pending resolution of the existing four-row cap. The stored g031 mapping is temporary and unresolved, not a claim of independence. Neither a release nor a split may use it as a separate family.

The proposed treatment retains the four existing study candidates and archives the later q0037 for practice, chosen by collection order before model evaluation. Actual exclusion remains a human decision; none is fabricated. The current validator counts all rows per group, so simply adding a fifth excluded row to g005 would fail. After a decision, preserve the complete original row/review and family history in the audit archive while materializing only four members in the study collection. No cap change or automatic row removal occurred. Dataset and review-ledger bytes remain unchanged; counts are still 39 pending, one excluded, zero accepted.

## Unit-conversion practice exclusion recorded, October 25, 2026

Altan explicitly excluded q0037 from research and retained it for practice. The local audit files `data/raw/pilot-audit-2026-10-25.jsonl` and `data/raw/reviews-audit-2026-10-25.jsonl` preserve all forty IDs and actual label-review evidence. q0037 belongs to g005 in that audit, with an actual A1 exclusion; g031 is retired. Both q0014 and q0037 are retained for practice. The audit has a five-member semantic family intentionally and is not a study dataset to pass to the four-row-cap validator.

The existing research pilot and matching ledger paths now contain only the remaining 38 candidates/reviews, all pending, with zero accepted. Their retained records are unchanged. g005 has four research members; no related variants were split to evade the cap. The exact reply, original q0037 record, audit paths/hashes, and before/after research hashes are retained in ignored `work/poteto/ai-assisted-review/q0037-exclusion-2026-10-25.json`. The full AI pass remains forty checks as historical evidence; the research subset has thirty-eight matching checks. There are 24 provisional research groups, distinct from the full audit’s families.

Next is q0028’s lighter-tent comparison versus g020’s ordering/selection family. That decision and remaining checks are pending; no guide freeze, accepted release, split, or experiment occurred.

## Lighter-tent selection added to ordering family, October 25, 2026

Altan added q0028 to g020 because choosing the lighter tent orders items by a field and selects one. g020 now contains q0024, q0028, q0034, and q0040, reaching the four-row cap. Only q0028 changed group ID; g024 is retired. All original labels and other row fields remain intact, including the direct-answer member q0034; all four members have review entries. The exact reply, prior mapping, and before/after hashes are retained in ignored `work/poteto/ai-assisted-review/g020-add-q0028-decision-2026-10-25.json`. Other rows and the review ledger are unchanged. The prior forty-row audit remains a dated snapshot; the decision record preserves this later change. There are now 23 provisional research groups, not 23 accepted independent groups.

Next is q0015’s elapsed lesson time versus q0033’s remaining water. Their family relationship remains for human review; a shared arithmetic operation alone does not establish paraphrase identity. Counts remain 38 pending research candidates, two practice-only exclusions in the audit history, and zero accepted; no split or experiment exists.

## Difference-calculation families merged, October 25, 2026

Altan merged q0015 and q0033 because both calculate a difference from supplied values, despite time versus water contexts. They now share g012. Only q0033 changed group ID; g027 is retired. Both calculation labels and q0033’s earlier current-contents adjudication are preserved. The exact reply, prior mapping, and before/after hashes are retained in ignored `work/poteto/ai-assisted-review/g012-merge-decision-2026-10-25.json`. Other fields/rows and the complete review ledger are unchanged. There are 22 provisional research groups, not 22 accepted independent groups.

Next is a short understanding checkpoint on the effect of placing close group variants across training and test. It does not replace remaining boundary checks or freeze guide v1. Counts remain 38 pending research candidates, two practice-only exclusions retained in the audit history, and zero accepted; no split or experiment exists.

## Grouping-purpose checkpoint answered, October 25, 2026

Altan correctly explained that a model seeing a similar pattern during training could obtain an inflated test score that does not show performance on genuinely new requests. The exact response and current data/ledger hashes are retained in ignored `work/poteto/ai-assisted-review/grouping-teachback-2026-10-25.json`; the learning log records the limited demonstrated topic. No group, label, review, or acceptance status changed. Next boundary is q0039’s handbook checklist transformation versus g002’s summaries. Remaining checks and guide v1 are open; there are 38 pending research candidates and zero accepted.

## Final pilot boundaries and guide v1, October 26, 2026

Altan supplied the shared-request-template rule and all eight remaining boundary decisions. The agent moved q0035 to g008, q0013 to g004, and q0036 to g003, retaining the other specified families separately. Original labels and texts remain unchanged. Guide v1 is frozen, and 38 eligible pilot rows are accepted after genuine review. The [pilot acceptance record](pilot-guide-v1.md) records hashes, all final decisions, 19 template families, class/group counts, exclusions, and actual CLI blockers. This supersedes earlier pending counts in the dated entries above. The 120-row M1 gate remains unmet; no baseline ran.
