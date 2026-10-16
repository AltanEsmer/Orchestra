# Orchestra

Orchestra is course project 13, **Learning to Route Queries in AI Systems**. The study will compare classifiers and text representations for choosing a query's first action, then analyze confidence and errors.

Current milestone is M1, the annotation pilot. The repository contains a project plan, data/evaluation protocol, draft [annotation guide](docs/annotation-guide.md), dataset validator, learning routine, and a verified Python environment smoke check. There is no research dataset, trained router, or experiment result yet. Tool integration is optional and deferred.

The [M1 to M3 implementation plan](docs/m1-m3-plan.md) defines the proposed data, baseline, and comparison work. Its [methods preview](docs/study-guides/m1-m3-methods-preview.md) supports the exam, presentation, and report. This is a planning delivery. Implementation waits for Altan's separate approval after the documentation PR merges.

## Set up and check the environment

Use [uv](https://docs.astral.sh/uv/getting-started/installation/) and run these commands from the repository root. The checked setup used uv 0.11.29 and Python 3.12.13. `.python-version` pins Python, and `uv.lock` pins package versions and distribution hashes. Setup needs network access when Python or packages are not cached.

```sh
uv python install 3.12.13
uv sync --locked
uv run --locked python scripts/smoke.py
uv run --locked python -m unittest discover -s tests
uv run --locked ruff check .
uv run --locked ruff format --check .
git diff --check
```

The smoke check prints `PASS: environment-smoke-only` followed by the checks performed and runtime versions. It tests sparse TF-IDF, training-only vocabulary, and expected dummy-classifier predictions on artificial fixtures. It does not measure routing accuracy. The unit tests check the dataset validator on small literal rows. Exact evidence is in the [learning log](docs/learning-log.md#preparation-evidence-october-7-2026).

Check annotated rows with `uv run --locked python scripts/validate_dataset.py <file.jsonl>`; the [annotation guide](docs/annotation-guide.md) explains the format. Training, experiment evaluation, and report generation are planned work. No runnable commands for those capabilities exist yet. No API key or GPU is needed for the current check.

## Start the study

- Track milestones, completion evidence, and next actions in the [roadmap](ROADMAP.md).
- Read the [architecture](architecture.md) for the current smoke check and proposed routing workflow.
- Read the [project plan](docs/project-plan.md) for scope, decisions, the report outline, and the ordered first work session.
- Use the [data and evaluation protocol](docs/data-and-evaluation.md) for labels, annotation, leakage controls, the experiment matrix, and confidence analysis.
- Follow the [repository walkthrough](docs/repo-guide.md) to explain each file and trace today's check versus the proposed prediction flow.
- Maintain the [learning log](docs/learning-log.md) for evidence, teach-back questions, and knowledge gaps.
- Use the [milestone study guides](docs/study-guides/README.md) for implementation explanations, course connections, report evidence, and oral preparation. PDFs are saved outside the repository in `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/`.
- Consult [course sources](docs/course-sources.md) for file locations and verified page references. Course PDFs are not redistributed here.
- Agents must follow [AGENTS.md](AGENTS.md).

The report and code deadline is **December 6, 2026**. The report must be 5–12 pages in IEEE conference two-column format and use Altan's own words. Altan handles course administration. At his request, course-rule confirmation is not an agent task or milestone gate. The study guides support his January 2027 oral preparation without claiming that the supplied PDFs verify an exam date.

Repository preparation and student understanding are tracked separately. Routing and split terminology **needs practice** after the first question caused confusion. The other topics remain **not yet reviewed**. The learning log records the response and next exercise.
