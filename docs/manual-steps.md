# Continue the study one step at a time

The agent operates the commands in the [runbook](run-experiments.md). Altan supplies genuine annotation decisions, interpretations, writing, and learning responses.

## Current next step, October 26

Pilot review is complete. Guide v2, adopted at Altan’s request for simpler rules, groups rows by shared variation, source or named setting, situation, or public record, and adds batch checks for near-duplicates, request-type spread, and source mix ([guide-v2 record](evidence/guide-v2.md)). The [pilot acceptance record](evidence/pilot-guide-v1.md) lists actual decisions, counts, hashes, exclusions, and remaining M1 requirements.

There are 38 accepted pilot rows in 23 groups. q0014 and q0037 remain practice-only in the local audit history. Single-human annotation with disclosed AI checks remains the selected method; AI consistency is not independent human agreement. The current pilot filename retains `pilot-v0`, but every accepted row carries `guide-v2`.

No pilot group questions remain. Next, the agent prepares the licensed public-source expansion using BFCL, No Robots, and Dolly assessments. Altan then reviews proposed first-action mappings and any new ambiguous cases. Source screening alone does not adopt a source or supply human labels. Do not ask for more handwritten batches before checking these supplements.

The October 26 [expansion screen](evidence/public-expansion-screen.md) finds plenty of public rows but few new request templates. Even if every proposal were accepted, document retrieval would reach about 8 groups and lookup about 6, short of 15. Guide v2 removes that bottleneck. Altan approved the regrouping and the Dolly attachment adapter and adopted the three sources. The [import record](evidence/public-import-v2.md) lists 90 candidates.

Altan approved all 90 proposed labels. The blind AI check agreed on every label; 35 clear rows are accepted and 55 rows carry an AI flag or an ambiguous judgment ([review record](evidence/public-review-v2.md)).

Altan accepted the recommendations for all 55 flagged rows. All 128 rows are accepted and the readiness check passes.

Altan froze the release as read-only `data/processed/m1-v1.jsonl` with the `reviews-v2.jsonl` ledger ([freeze record](evidence/public-review-v2.md#freeze)).

The [collection brief](collection-brief.md) now records Altan's M3 source mix and the 400-row target. It is final for M2.

M2 ran on October 26. The grouped split has 78 training, 25 validation, and 25 sealed test rows. Both baselines ran twice and reproduce exactly. On validation, B0 scores macro-F1 0.097 and L2 scores 0.730 ([M2 record](evidence/m2-research-run.md)).

Altan inspected the seven L2 errors and recorded five hypotheses ([error inspection](evidence/m2-research-run.md#error-inspection)). That exposure must be disclosed, and M3 rows must not target those errors.

The agent recorded GSM8K's license (MIT) and pinned revision and screened each source's capacity ([capacity screen](evidence/m3-capacity-screen.md)). Direct answer and document retrieval can reach about 100 rows within the mix. With your approval, the agent downloaded the GSM8K test file and screened it. Calculation can now reach about 100 rows as well. At your request the agent also downloaded and screened eight BFCL parallel and irrelevance files; they added about three lookup rows. Lookup is 11 to 24 rows short even if all 11 usable AI drafts are accepted.

At your request the agent drafted 30 AI lookup candidates in request types other than keyed-record lookups ([draft record](evidence/lookup-ai-drafts.md)). Accepting 11 to 24 of them would close the lookup gap.

**Next:** label the 30 drafts in the local `data/raw/lookup-drafts-ai-2026-10-26/worksheet.md`, with your own label and rationale for each, or an exclusion. Decide whether the 16 borderline BFCL rows count as lookup. Then the agent imports candidates, you label them, the blind AI check runs, and you adjudicate flags. The M1 and M2 study PDFs are ready; attempt their checkpoint questions, then close issues #4 and #5 when you are satisfied.

Reach at least 120 accepted rows, 30 per label, and 15 groups per label before a study release or baseline. The current pilot falls short of all those coverage targets. Its accepted status does not permit bypassing readiness.

## Completed human evidence

- Forty human-authored requests and original labels collected through agent-directed exercises; actual sharing permission recorded.
- Single-human annotation with disclosed AI checks selected, with forty historical AI checks and genuine human adjudications.
- Tank-contents ambiguity clarified; teaching-derived and excess-family examples excluded for practice.
- Existing families and cross-group boundaries reviewed; guide v1 rule and eight final decisions supplied by Altan.
- Altan explained how close training/test variants can inflate a score. Other leakage controls still need practice.

Full dated responses remain in the [learning log](learning-log.md); local raw records and decision artifacts remain outside Git.

## Subsequent steps

1. Adopt compatible licensed sources with original wording, contexts, attribution, guide-v2 groups, and the batch quality checks. Review new labels under the selected AI-assisted method.
2. Validate the 120-row release and freeze the expansion brief before baseline error inspection. The agent runs the two baselines twice and checks reproduced splits and predictions.
3. Extend toward 400 rows and run all 14 comparisons without moving previously frozen groups.
4. Discuss actual validation errors and confidence findings. Freeze model/confidence choices before the final test; generate measured figures.
5. Write the report in your own words. The agent checks provenance, references, formatting, and research reproduction.
6. Attempt oral questions and record actual answers. Submit through course channels and retain receipts.

Candidate counts, accepted rows, M1 readiness, and demonstrated understanding are different kinds of evidence.
