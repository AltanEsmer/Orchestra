# Orchestra

Orchestra is course project 13, **Learning to Route Queries in AI Systems**. The study will compare classifiers and text representations for choosing a query's first action, then analyze confidence and errors.

M1–M3 are complete in the GitHub tracker. M1 froze 128 accepted rows and M2 reproduced its baselines. On October 28, [M3](docs/evidence/m3-research-run.md) froze 400 rows, extended the split to 242 training/79 validation/79 sealed test, and reproduced all 14 configurations including an archive restore. Validation-only selection chose L1-C10, macro-F1 0.925. M3 opened no test; its 79 test rows stayed sealed inside the M3.5 test, which M4 opened once on November 3. The labels include human-adopted AI judgments, not independent human agreement.

[M3.5](docs/m3-5-plan.md) was added October 31 after supervisor feedback: expand with public data to **at least 2,000 accepted rows in a near-balanced design** (set November 1 after source discovery, replacing the original 2,500 minimum and 4,000 aim; see [option B](docs/evidence/m3-5-option-b-supply.md)), and compare **Decision Tree, Random Forest, XGBoost, and TypeSafe AI Jev** alongside the existing methods. The [roadmap](ROADMAP.md) holds dates, issues, and completion gates. On November 2 the four new methods were [implemented and tested on fixtures](docs/evidence/m3-5-classifiers.md), and the [M3.5 release](docs/evidence/m3-5-dataset.md) `m3-5-v1` was frozen: 3,145 accepted rows (retrieval 1,000, direct 1,000, calculation 651, lookup 494), AI-labeled with Altan adjudicating disagreements, after Altan raised the size to up to 1,000 per class. The [first M3.5 run](docs/evidence/m3-5-research-run.md) fitted the 26 local configurations: the best local validation macro-F1 is L3-C10 at 0.952. With Altan's TypeSafe key, the [27-configuration run](docs/evidence/m3-5-full-run.md) added Jev at 0.975, and the frozen rules select Jev on validation. The M4 commands accept that decision set, Jev included. On November 3 the [M3.5 study guide](docs/study-guides/m3-5-data-and-methods.md) was delivered, Altan accepted M3.5, and the [M4 final test](docs/evidence/m4-final-test.md) ran once: Jev, the frozen selection, scores 0.964 test macro-F1. The same day every Jev and L3-C10 test mistake was [interpreted as a hypothesis](docs/evidence/m4-final-test.md#test-mistakes-interpreted-after-the-freeze) and the [M4 study guide](docs/study-guides/m4-confidence-errors.md) was delivered. M4 is done: Altan answered its practice questions on November 5, and on November 6 he reviewed the flagged test labels and kept them all. Altan accepted M4 on November 6, and M5 is in progress. The [six-page IEEE manuscript and evidence map](report/README.md) are ready for Altan’s revision in his own words.

The [M1 to M3 implementation plan](docs/m1-m3-plan.md) defines the proposed data, baseline, and comparison work. Its [methods preview](docs/study-guides/m1-m3-methods-preview.md) supports the exam, presentation, and report. Altan approved implementation on October 16. The five units are built and tested on fixtures. Their M1–M3 research evidence is recorded; M3.5 adds a separately planned extension.

## Set up and check the environment

Use [uv](https://docs.astral.sh/uv/getting-started/installation/) and run these commands from the repository root. The checked setup used uv 0.11.7 and Python 3.12.13. `.python-version` pins Python, and `uv.lock` pins package versions and distribution hashes. Setup needs network access when Python or packages are not cached. On macOS, XGBoost also needs the OpenMP runtime: run `brew install libomp` once (Linux and Windows use the self-contained `xgboost-cpu` build).

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

Continue with the [M3.5 plan](docs/m3-5-plan.md); the earlier [manual sequence](docs/manual-steps.md) documents M1–M3 intake and review. The agent can operate the commands. `uv run --locked python -m orchestra status` checks the configured data readiness; it does not certify the new M3.5 requirements. `prepare-study` enforces readiness, records collection/review hashes, and calculates the parent hash before splitting. Later commands cover `confidence`, `freeze`, `final-test`, `figures`, `archive`, and `restore`.

Run `sh scripts/check.sh` for the complete software checks. Run `uv run --locked python scripts/verify_workflow.py --out work/fixture-proof` with a new output path for the artificial CLI workflow and clean restored reproduction. The workflow creates no research evidence. GitHub Actions runs both checks on pull requests and main.

Use `scripts/run_experiment.sh --config data/processed/m2-prepared.json --run-id m2-a` after `prepare-study` writes that prepared configuration and split. The launcher sets all four timing thread variables to `1` before starting the existing runner. It resolves relative paths from the repository root. No GPU is needed, and only the optional Jev collection needs an API key.

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
