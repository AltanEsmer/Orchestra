# Orchestra

Orchestra is course project 13, **Learning to Route Queries in AI Systems**. The study will compare classifiers and text representations for choosing a query's first action, then analyze confidence and errors.

Current research milestone is M1. Altan completed pilot review on October 26, and guide v2 then replaced the strict request-template grouping with simpler scenario/source groups plus batch quality checks ([guide-v2 record](docs/evidence/guide-v2.md)). The local pilot has 38 accepted human-authored queries in 23 groups, and 90 public candidates from Dolly, BFCL, and No Robots await Altan's labels ([import record](docs/evidence/public-import-v2.md)), with two practice-only exclusions preserved in the audit history. Single-human annotation with disclosed AI checks is the selected method. The [pilot acceptance record](docs/evidence/pilot-guide-v1.md) distinguishes these accepted rows from the unmet 120-row M1 release. No research split, trained router, or experimental result exists. The complete planned software workflow has passed artificial fixtures; tool integration remains optional and deferred.

The [M1 to M3 implementation plan](docs/m1-m3-plan.md) defines the proposed data, baseline, and comparison work. Its [methods preview](docs/study-guides/m1-m3-methods-preview.md) supports the exam, presentation, and report. Altan approved implementation on October 16. The five units are built and tested on fixtures. Their research runs wait for accepted, reviewed, and licensed M1 data.

## Set up and check the environment

Use [uv](https://docs.astral.sh/uv/getting-started/installation/) and run these commands from the repository root. The checked setup used uv 0.11.7 and Python 3.12.13. `.python-version` pins Python, and `uv.lock` pins package versions and distribution hashes. Setup needs network access when Python or packages are not cached.

```sh
uv python install 3.12.13
uv sync --locked
uv run --locked python scripts/smoke.py
uv run --locked python -m unittest discover -s tests
uv run --locked ruff check .
uv run --locked ruff format --check .
git diff --check
```

The smoke check prints `PASS: environment-smoke-only` followed by the checks performed and runtime versions. It tests sparse TF-IDF, training-only vocabulary, and expected dummy-classifier predictions on artificial fixtures. It does not measure routing accuracy. The unit tests cover validation, splitting, experiments, confidence, figures, preparation, and archives using artificial inputs. Exact evidence is in the [learning log](docs/learning-log.md#preparation-evidence-october-7-2026).

Check annotated rows with `uv run --locked python scripts/validate_dataset.py <file.jsonl>`; the [annotation guide](docs/annotation-guide.md) explains the format. Add `--review <ledger.jsonl> --ready` to also check the M1 release requirements.

The [experiment runbook](docs/run-experiments.md) gives the complete preparation-to-archive command sequence. Research runs wait for accepted, reviewed data and a permission record.

Continue the [manual sequence](docs/manual-steps.md) with licensed public-source expansion and review of new labels; pilot grouping, guide v1, authorship, permission, and the AI-assisted method choice are complete. The agent can operate the commands. `uv run --locked python -m orchestra status` reports the current data blocker. `prepare-study` enforces readiness, records collection/review hashes, and calculates the parent hash before splitting. Later commands cover `confidence`, `freeze`, `final-test`, `figures`, `archive`, and `restore`.

Run `sh scripts/check.sh` for the complete software checks. Run `uv run --locked python scripts/verify_workflow.py --out work/fixture-proof` with a new output path for the artificial CLI workflow and clean restored reproduction. The workflow creates no research evidence. GitHub Actions runs both checks on pull requests and main.

Use `scripts/run_experiment.sh --config data/processed/m2-prepared.json --run-id m2-a` after `prepare-study` writes that prepared configuration and split. The launcher sets all four timing thread variables to `1` before starting the existing runner. It resolves relative paths from the repository root. No API key or GPU is needed.

## Start the study

- Track milestones, completion evidence, and next actions in the [roadmap](ROADMAP.md).
- Read the [architecture](architecture.md) for the implemented components and research workflow.
- Read the [project plan](docs/project-plan.md) for scope, decisions, the report outline, and the ordered first work session.
- Use the [data and evaluation protocol](docs/data-and-evaluation.md) for labels, annotation, leakage controls, the experiment matrix, and confidence analysis.
- Follow the [repository walkthrough](docs/repo-guide.md) to explain each file and trace the verified tooling and the research flow awaiting data.
- Maintain the [learning log](docs/learning-log.md) for evidence, teach-back questions, and knowledge gaps.
- Use the [milestone study guides](docs/study-guides/README.md) for implementation explanations, course connections, report evidence, and oral preparation. PDFs are saved outside the repository in `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/`.
- Consult [course sources](docs/course-sources.md) for file locations and verified page references. Course PDFs are not redistributed here.
- Agents must follow [AGENTS.md](AGENTS.md).

The report and code deadline is **December 6, 2026**. The report must be 5–12 pages in IEEE conference two-column format and use Altan's own words. Altan handles course administration. At his request, course-rule confirmation is not an agent task or milestone gate. The study guides support his January 2027 oral preparation without claiming that the supplied PDFs verify an exam date.

Repository preparation and student understanding are tracked separately. Altan explained how related training/test queries can inflate scores. The broader routing and leakage topics still **need practice**. The other topics remain **not yet reviewed**. The learning log records the response and next exercise.
