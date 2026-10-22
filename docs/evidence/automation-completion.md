# Automation completion evidence — October 22, 2026

This delivery implements the remaining independent software for issues #4–#11. Every data-bearing acceptance check uses clearly identified artificial fixtures. There are still zero research rows and no research metrics. Human annotations, permission, report authorship, learning responses, and submission receipts are not supplied by tooling.

## Integrated foundation

[PR #16](https://github.com/AltanEsmer/Orchestra/pull/16) merged as `d66698838b8f405b638e868daa0bebe2142528b7`. Its final repair commit is `f973d92121a5073ed39193e1b9117d258c08c6c0`. The exact archived repair commit passed 153 unit tests, smoke, lint, format, and the M2/M3 fixture workflow. The repair binds materialized contents to the frozen split, refuses destructive path aliases, and permits reproduction after relocating parent paths.

## Completion tooling

- Readiness status, blind review worksheets, and immutable prepared study configs with permission/review/collection-brief hashes.
- Reproduction of saved raw scores before grouped training-only sigmoid calibration; probability, reliability, and coverage diagnostics; checked validation interpretations before a research freeze.
- Frozen source/dependency/artifact identities and a canonical final-test receipt per split. A POSIX lock excludes concurrent runs; failed or interrupted identical requests can resume with preserved attempt history and atomic receipt updates.
- Scientific SVG/PNG figures with exact source JSON, hashes, and inherited artificial-data labeling.
- A compiled IEEE report source template containing prompts, not findings.
- Explicit local archive allowlists, checksum/path validation, executable-mode restoration, clean-environment reproduction, and GitHub CI.

## Acceptance evidence

The reproducible command is `uv run --locked python scripts/verify_workflow.py --out work/<new-directory>`. Its outputs include `acceptance.json` and the complete command transcript. It creates 120/400 artificial rows and records artificial review evidence only inside the ignored fixture tree.

The integrated workflow passed all 24 command checks: M1 readiness and blind worksheet; prepared M2 and M3 splits; two runs of each and reproduction comparison; selection/report; confidence and freeze with the sealed test file temporarily absent; final evaluation with exact-repeat verification and changed-output refusal; scientific figure export; archive creation and restoration; locked installation in the restored environment; and restored M3 prediction/metric comparison.

The first integrated archive attempt exposed an overly broad secret-header detector that rejected the archive module's own source. That detector now recognizes actual PEM header lines. A regression uses a valid archive, alters one payload while retaining manifest/modes, and asserts checksum refusal before restoration.

The IEEE template compiled successfully in the Codex document compiler. Class balance, validation comparison, reliability, and coverage exports were visually inspected. Final research pagination, figures, and report content remain unverified until their inputs exist.

Final local checks on the integrated source:

| Check | Observed result |
| --- | --- |
| `sh scripts/check.sh` | Exit 0: locked setup; smoke PASS; 201 tests in 19.122s, OK; Ruff lint PASS; 47 files already formatted; diff whitespace PASS. |
| `scripts/verify_workflow.py --out work/poteto/automation-completion/integration-final` | Exit 0; all 24 real CLI checks PASS, including clean restored reproduction. |
| Local Markdown links | 121 links and anchors resolve across 27 files. |
| Focused recovery checks | 19 confidence tests include interrupted retry, active-run exclusion, stale receipt recovery, and blocked-parent preflight. |
| Figure checks | 10 tests; inherited fixture labeling and verified research evidence. Final coverage plot visually checked after grouping coincident threshold labels. |
| Archive checks | 11 tests, including an altered valid archive rejected specifically by checksum. |
| Independent reviews | Spec re-review PASS for repaired mechanisms; Standards found no remaining correctness issue. The final redundant comment was removed. Exact-head shipping review and remote CI are recorded on the PR. |

Reviewers used the available GPT-6.1 model family. These were independent roles, not a cross-family review. Scratch transcripts and detailed review reports are retained under ignored `work/poteto/automation-completion/`; the repository contains the rerunnable verification commands and this concise record.

## Limits and manual handoff

The final-test receipt is a local audit control, not protection against deliberately deleting records or modifying code. Recovery uses POSIX locks and currently supports macOS/Linux. An archive is local-only; publication needs the actual dataset permission. Secrets and PDFs are excluded; retain the final report and external milestone study PDFs separately. The model outputs an action label and never executes that action.

Milestone PDFs requiring actual data/results, the research archive, research conclusions, final report pagination, oral readiness, and submission remain dependent on human work. Optional embeddings, GPU experiments, deployment, and tool execution remain outside scope. The [manual guide](../manual-steps.md) gives the sequence; the first action is one original English query plus the first action and rationale. No learning status changed.
