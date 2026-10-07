# Working on Orchestra

Orchestra is course project 13, Learning to Route Queries in AI Systems. Keep changes small enough for Altan to explain at the oral exam.

## Read before changing files

Read [README.md](README.md) and [docs/project-plan.md](docs/project-plan.md) for scope and the current milestone. Before changing data, features, models, metrics, or confidence handling, read [docs/data-and-evaluation.md](docs/data-and-evaluation.md). Verify course claims against [docs/course-sources.md](docs/course-sources.md).

Read [docs/repo-guide.md](docs/repo-guide.md) before explaining or changing implementation. Use relevant existing agentic engineering skills. Explain a proposed dependency, abstraction, or modeling equation and its purpose before adding it. Preserve the preparation scope until a subsequent task authorizes model development.

## Deliver a verifiable change

- Verify `git remote -v` identifies `AltanEsmer/Orchestra` before committing, pushing, or opening a PR. Preserve unrelated work.
- Keep one behavior or contract per commit. Use imperative Conventional Commit messages. Prefer a focused failing test, the smallest implementation, boundary coverage when useful, then evidence documentation. Avoid tests that merely restate implementation.
- Run the affected checks and the README smoke/lint commands before handoff. Report actual outputs. Label unrun commands, planned experiments, and expected metrics as unverified. Never fabricate measurements.
- Update the plan for consequential decisions, the data protocol for schema or evaluation changes, the walkthrough for authored files, and the learning log for every meaningful change. Keep course PDFs, secrets, and unapproved data out of Git.
- If delegation is authorized, use `gpt-6.1-sol` with low reasoning for workers and high reasoning for reviewers. Prefer named worker/reviewer roles. Give writers disjoint files or worktrees. The lead reviews the diff and explains the integrated result.
- Handoffs list commit hashes, checks, acceptance evidence, and unresolved limitations. PRs link the issue or ADR, explain risk and verification, and disclose schema, security, privacy, or deployment impacts. Include screenshots when UI changes need them.

## Teach alongside implementation

Follow the handoff and status routine in [docs/learning-log.md](docs/learning-log.md). Explain the change plainly, trace one concrete query, and give two or three teach-back questions or a small exercise. During practice, let Altan attempt an answer before revealing the worked explanation.

Update learning status from Altan's actual responses only. Passing tests and written explanations establish implementation evidence, not student understanding. Keep unanswered topics visible and revisit them at the plan's milestone checkpoints.
