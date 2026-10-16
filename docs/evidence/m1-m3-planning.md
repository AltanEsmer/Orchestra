# M1 to M3 planning evidence

This record covers the documentation-only change on October 16, 2026. It supports the [implementation plan](../m1-m3-plan.md) and [methods preview](../study-guides/m1-m3-methods-preview.md). It reports planning evidence, not experimental results.

## Baseline and authorization

The verified remote is `https://github.com/AltanEsmer/Orchestra.git`. Planning started from main commit `48abda02aaeedd11d0549c6b88beb33bcbb12786`, the merge of PR #14. The original checkout was clean on `claude/m1-annotation-start` and remains untouched. Work used a separate managed worktree and branch `codex/m1-m3-plan`.

Altan requested a plan for completing milestones 1, 2, and 3, supporting explanations for the exam, presentation, and report, and a documentation PR that the agent should merge. He explicitly required waiting for subsequent implementation approval. He requested no questions during this work and reported that SDU would provide 10 GPU hours. These are task instructions, not evidence of data acceptance or ML understanding.

## Decisions supported by inspection

The current code has a row validator and toy environment smoke check. There are no research rows, learned router, or experiment outputs. The validator's 15 existing tests cover structural checks. Schema validation alone accepts an empty input and does not establish the sample counts or human review required for M1. The plan therefore separates schema validation from dataset acceptance.

The draft pilot path `data/annotation/` is not ignored. The plan and annotation guide now use the already ignored `data/raw/` directory. No data file or ignore rule changed.

The 120-row baseline precedes the 400-row comparison. The plan preserves initial membership because M2 validation could otherwise enter a newly shuffled test set. The five-fold allocator and append-only extension remain proposed algorithms, with behavioral verification required during implementation.

Local signature inspection confirmed scikit-learn 1.9.1 exposes `LogisticRegression(penalty='deprecated', ..., l1_ratio=0.0, solver='lbfgs', max_iter=100, ...)`. The plan records explicit settings compatible with that version and requires exporting resolved parameters. No fitted estimator was created by this inspection.

Official scikit-learn documentation for group stratification, leakage, logistic regression, and TF-IDF was checked. References are linked in the plan. The methods preview reuses the repository's verified course-page map. On October 16, hashes of CourseProjects, report instructions, and Lectures 2, 5, and 6 matched the recorded copies. No fresh visual slide review is claimed. The available lecture filenames still end at Lecture 6.

## Workflow and independent review

Poteto's figure-it-out workflow was adapted to one documentation PR with a clear completion condition. The multi-phase-plan playbook's no-implementation boundary applies. Its standing-program template and checker were not used. There is no requested goal, heartbeat, UI rollout, or autonomous implementation program. Training prototypes, ten UI coverage lanes, runtime performance comparisons, and screenshots would not verify this prose-only change and were skipped. Runtime helper installation was unnecessary.

The pinned Poteto dependency check passed with commit `7366ac128bdf95f45e6734f412b49a4031800169`, 68 skills, 187 files, and 95 routes. No skill library, runtime cache, or plugin configuration changed. Origin CLI was present, but `origin repo view` reported that the repository was not found. GitHub CLI is the selected forge.

A worker independently inspected the current contracts and split-expansion risks without edits. A second worker authored only the methods preview. The lead reviewed that file, specified the implementation plan, and reconciled existing documents. Writers had disjoint file ownership. Review uses the repository's named `gpt-6.1-sol` reviewer role and is not cross-family validation. No application comments or suppressions were added, so a separate comment-removal agent was inapplicable. Deslop and technical-writing review apply to the documentation diff.

An independent `gpt-6.1-sol` reviewer inspected the documentation patch and decision trail and reported no blocking correctness or security findings. The reviewer reran the smoke check, all 15 unit tests, Ruff lint, Ruff formatting, and the diff check successfully. That pass used the original checkout's locked environment against files in the planning worktree. The lead's checks below used the fresh worktree environment. The exact committed-head verdict is a remaining pre-merge check recorded with the PR handoff. A full exported chat transcript is not available as a separate review artifact.

## Actual checks

All commands ran from the managed planning worktree. No research experiment ran.

| Command or inspection | Observed outcome |
| --- | --- |
| `uv python install 3.12.13` | Python 3.12.13 already installed. |
| `uv sync --locked` | Created the worktree environment, resolved 9 packages, and installed 8 packages. |
| `uv run --locked python scripts/smoke.py` | `PASS: environment-smoke-only; sparse TF-IDF, held-out vocabulary isolation, and toy DummyClassifier predictions verified.` Python 3.12.13, scikit-learn 1.9.1. |
| `uv run --locked python -m unittest discover -s tests` | Ran 15 tests, `OK`. |
| `uv run --locked ruff check .` | `All checks passed!` |
| `uv run --locked ruff format --check .` | `19 files already formatted`. Includes local authoring helpers; this is not a count of tracked application modules. |
| `git diff --check` | Exit 0. |
| Local Markdown link and anchor check | `PASS: 101 local Markdown links and anchors across 16 files.` |
| Dependency and source scope | No diff in `pyproject.toml`, `uv.lock`, scripts, tests, or `data/`. Only Markdown and a decision TSV are planned for the PR. |

The Markdown check used an ignored one-shot helper at `work/m1-m3-plan/check-docs.py`. It enumerates tracked and unignored new Markdown, resolves relative targets, and checks heading fragments. It does not test remote links. The external course-file fingerprints matched the existing recorded hashes. Reproduction of experimental outputs remains unverified because no experiment exists yet.

## Remaining limits

M1 still needs human labels and review, guide v1, a truthful permission record, and accepted rows. M2 and M3 have no runnable research commands or measurements. The proposed split allocation, CPU limits, and GPU budget have not been tested. Human review can move collection beyond the current roadmap targets, especially with the one-week self-review alternative. Dates are not completion evidence.

The methods preview is delivered as Markdown. The three milestone PDFs require actual milestone evidence and will be exported and inspected during implementation. No dataset, dependency, model, experiment, GPU use, or new student answer is delivered here. The next gate is explicit implementation approval after the planning PR merges.
