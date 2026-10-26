# Pilot review and annotation guide v1

On October 26, 2026, Altan supplied the final eight boundary decisions and the shared-request-template rule. The agent applied his decisions and froze guide v1 after the recorded pilot review. This completes pilot annotation, not the 120-row M1 milestone. The pilot is human-authored through agent-directed exercises, with one human annotator and disclosed AI checks.

## Rule and actual decisions

A group is a shared request template: the same user goal solved by the same procedure, whatever the scenario. Sharing a label or arithmetic operation is insufficient. Conservative template families reduce independent group counts and can contain different first-action labels.

| Case | Actual human decision |
| --- | --- |
| q0039 and g002 | Keep separate. Checklist actions preserve required steps; a summary selects and shortens. |
| q0035 | Join g008’s named-document content extraction. g029 retired. |
| q0013 | Join g004’s concept explanations. g010 retired. |
| q0022, q0030, q0038 | Keep brainstorming, storytelling, and social-message goals separate. |
| q0036 | Join g003’s key-based lookup, separate from g016’s condition filter. g030 retired. |
| q0017 and q0021 | Keep allocation and averaging separate. |
| q0025 and g005 | Keep geometry and amount-per-unit scaling separate, regardless of the group cap. |
| q0001 | Keep percentage discount as its own template; future related discount requests join it. |

Earlier human decisions and the two practice exclusions remain preserved in the [learning log](../learning-log.md). q0014 was adapted from teaching material. q0037 was the fifth related member of the amount-per-unit family and remains practice-only under the four-row research cap. q0033’s current-water clarification retains its calculation label. No original query or first-action label was rewritten.

## Accepted pilot, not an M1 release

| Label | Accepted rows | Groups containing that label | M1 rows needed | M1 groups needed |
| --- | ---: | ---: | ---: | ---: |
| calculation | 9 | 6 | 30 | 15 |
| document_retrieval | 9 | 5 | 30 | 15 |
| knowledge_lookup | 10 | 4 | 30 | 15 |
| direct_answer | 10 | 7 | 30 | 15 |

There are 38 accepted pilot rows across 19 shared request templates. Per-class group counts overlap in mixed-label families and must not be summed as independent groups. All 38 have actual AI review entries; the only retained flagged row has its actual human adjudication. AI consistency is 38/38 for the retained subset and 40/40 historically; it is not correctness or independent human agreement. Zero legacy human-review entries exist.

The local `data/raw/pilot-v0.jsonl` path is retained for existing CLI callers, but its current rows explicitly carry `annotation_version: guide-v1` and `status: accepted`. The matching `data/raw/reviews-v1.jsonl` is unchanged. The filename does not determine the guide version. No `data/processed/m1-v1.jsonl` release or research split was created. Historical forty-ID snapshots, original worksheet, exact decisions, and before/after artifacts stay ignored locally. The October 25 audit is a dated snapshot; later group decisions are separate audit entries.

The final batch changes only three group IDs plus the guide version and acceptance metadata. Keep-separate decisions do not alter IDs. Original texts, first-action labels, rationales, sources, and annotators are preserved. `work/poteto/pilot-guide-v1/` stores the final human message with Markdown emphasis removed, normalized decisions, prior pilot/review bytes, hashes, CLI outputs, and checks. Formatting normalization is disclosed rather than presented as a byte-exact message export.

Current accepted pilot SHA-256: `314365de4c1807517a7a027bbb8b7d1aa992000f18dbb58e73059c5ce7d22a44`.

Matching review ledger SHA-256: `29e5cbd1248672c06ea59f1ba536c7a4d822bc78a5ccab14c5e348550daa60c2`.

## Remaining work and interpretation limits

The actual validator passes 38 rows. `orchestra status` exits 1 as expected with only size/coverage blockers: 120 accepted rows total, 30 per class, and 15 groups per class. There are no pending pilot ambiguities or grouping questions. M1 stays open. The next work is licensed source adoption and compatible expansion under guide v1; the thirty public shortlist candidates are still proposals. No training, validation metric, or final test exists.

The shared word “handbook” in summary/checklist cases is recorded for future validation error analysis as a possible word-level cue. No effect or error has been observed. Keep wording intact and do not inspect the sealed test to tune families or cues. Source/style confounding and the small authored pilot remain limitations.

Verification: `sh scripts/check.sh` passed all 208 tests in 17.129 seconds, the environment smoke check, Ruff lint, formatting for 52 files, and whitespace checks. The desktop LaTeX compiler successfully compiled the updated report prompt. No application code, dependency, or schema changed. New tests were not added for recorded annotation decisions. The methods preview source is current; the full M1 PDF edition is not yet exported and remains an outstanding milestone deliverable.

Independent Spec and Standards reviewers returned PASS after stale current-state paragraphs were corrected. Spec verified the actual local data, preservation rules, final decisions, and coverage-only blockers. Standards checked 134 relative Markdown link targets, current/historical distinctions, and whitespace. Review used agents from the same GPT family and does not constitute independent human annotation.
