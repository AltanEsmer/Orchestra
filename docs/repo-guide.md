# Repository walkthrough

This guide distinguishes the executable preparation from the planned routing experiment. Start with the [README commands](../README.md), then read the script alongside this explanation.

## Authored files and their roles

| File | Purpose, input, and output |
| --- | --- |
| `README.md` | Entry point with executable setup/check commands and links to the project documents. |
| `AGENTS.md` | Repository workflow and explanation obligations for agents. |
| `pyproject.toml` | Declares the Python range, pinned ML dependency, and development tooling. uv reads it to resolve the environment. |
| `.python-version` | Selects Python 3.12.13 so a newer system Python does not silently change the runtime. |
| `uv.lock` | Generated dependency resolution, versions, sources, and distribution hashes. uv uses it during locked setup. It is tracked evidence, not handwritten model logic. |
| `scripts/smoke.py` | Executable environment assertions on tiny artificial query lists. It prints a success label and runtime versions. It writes no research results. |
| `.gitignore` | Preserves the initial Python exclusions and adds local data, models, results, secrets, course PDF, and scratch exclusions. It does not protect already tracked files. |
| `LICENSE` | Existing MIT license for repository material. It does not grant rights to external course content or data. |
| `docs/project-plan.md` | Scope, milestone dependencies, decision rationale, report evidence map, and first-session checklist. |
| `docs/data-and-evaluation.md` | Proposed first-action labels, row schema, annotation/split protocol, experiments, confidence, and reproducibility. |
| `docs/course-sources.md` | Source locations, exact course page mapping, and requirement fingerprints. |
| `docs/repo-guide.md` | This living explanation of authored files and data flow. |
| `docs/learning-log.md` | Change explanations, actual verification, questions, and evidence-based understanding status. |

There is no separate unit-test suite yet. The smoke script is the meaningful executable environment check for this preparation. Future behavioral tests belong under `tests/` when the baseline introduces a data validator, split generator, or model code. New files must be added to this guide when created.

## The executable flow today

uv reads `.python-version`, `pyproject.toml`, and `uv.lock`, then creates the ignored `.venv/` environment. The smoke script imports scikit-learn and its numerical dependencies from that environment.

The script fits a TF-IDF vectorizer on toy training text. It transforms a separate held-out query using the already learned vocabulary. The checks verify a sparse, nonempty feature matrix and ensure the held-out-only word `quasar` never enters that vocabulary. Fitting learns the representation's vocabulary and IDF statistics; transforming uses them without learning new words.

The dummy classifier learns the most frequent toy label and predicts it for every held-out query. Its labels are fixture labels, not the proposed four routing actions. A prediction of `simple` proves only that fit/predict executes as expected. It does not establish semantic understanding or routing quality.

Our code owns fixture selection, call order, and assertions. scikit-learn owns tokenization, TF-IDF, and the dummy estimator. NumPy/SciPy own numerical arrays and sparse matrix operations. Altan needs to explain those concepts and their inputs/outputs, but this repository does not implement library internals.

## The planned research flow

Consider "Calculate the increase using the figures in the attached report." Its proposed first action is `document_retrieval`, because the numbers must be read before any calculation. Annotation records that rationale and a group ID shared by related paraphrases.

A future validator accepts the row only after annotation review. A persisted split assigns its whole group to one partition. If the row belongs to validation, the fitted training pipeline transforms it and predicts one of the four actions. The evaluation compares that prediction with the annotated first action. A confidence policy may later abstain. No document is actually retrieved in the initial study.

This flow is not executable yet. The first implementation session in the [plan](project-plan.md#first-work-session-after-preparation) defines the next steps and its completion condition.

## Proposed layout as the study grows

The following directories are planned, not empty packages created in advance.

| Path | Intended content and Git policy |
| --- | --- |
| `src/orchestra/` | Add only when reusable validation, training, or evaluation code is needed. Track authored modules. |
| `tests/` and `tests/fixtures/` | Focused behavioral checks and small cleared fixtures. Track both. |
| `data/raw/`, `data/processed/` | Local acquired and derived rows. Ignored. Preserve source/license manifests separately. |
| `data/manifests/`, `data/splits/` | Proposed tracked provenance and stable split-ID manifests after privacy review. |
| `configs/` | Proposed tracked, resolved experiment configurations. |
| `results/<run-id>/` | Ignored full metrics, predictions, timing, and configuration copies. Archive for reproducibility. |
| `models/` | Ignored fitted artifacts. Load only trusted locally produced files. |
| `docs/evidence/` | Deliberately selected, cleared small tables and figures that support the report. |
| `work/` | Ignored agent scratch notes, not required to run the project. |

No runtime credential, paid API, external dataset, or pretrained model is needed for today's smoke check. Setup downloads Python or packages when missing. Future artifact retention and resource limits are defined in the [protocol](data-and-evaluation.md#reproducibility-and-resource-budget).
