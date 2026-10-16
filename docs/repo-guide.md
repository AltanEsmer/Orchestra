# Repository walkthrough

This guide distinguishes the executable preparation from the planned routing experiment. Start with the [README commands](../README.md), then read the script alongside this explanation.

## Authored files and their roles

| File | Purpose, input, and output |
| --- | --- |
| `README.md` | Entry point with executable setup/check commands and links to the project documents. |
| `architecture.md` | Current and proposed components, query flow, library responsibilities, and storage boundaries. |
| `ROADMAP.md` | Primary milestone tracker with target dates, statuses, completion gates, linked GitHub issues, owners, and evidence. Includes plain-language milestone objectives. |
| `AGENTS.md` | Repository workflow and explanation obligations for agents. |
| `pyproject.toml` | Declares the Python range, pinned ML dependency, development tooling, and the pinned `setuptools==84.0.0` build requirement that makes `src/orchestra/` an editable package under `uv sync --locked`. |
| `.python-version` | Selects Python 3.12.13 so a newer system Python does not silently change the runtime. |
| `uv.lock` | Generated dependency resolution, versions, sources, and distribution hashes. uv uses it during locked setup. It is tracked evidence, not handwritten model logic. |
| `scripts/smoke.py` | Executable environment assertions on tiny artificial query lists. It prints a success label and runtime versions. It writes no research results. |
| `scripts/validate_dataset.py` | Thin CLI adapter over `orchestra.data`. Reads an annotated JSONL file and the source manifest, prints every schema or provenance error, then prints a summary (dataset hash, status, label, and group counts, word lengths, source mix, group sizes, exclusions). With `--review LEDGER` it validates the review ledger and reports agreement. With `--ready` it also enforces the M1 acceptance requirements (counts, permission, review coverage, ledger/dataset agreement). Exit code 1 means the file is not valid or not ready. It does not judge whether a label is correct. |
| `src/orchestra/__init__.py` | Marks the installable package. Empty. |
| `src/orchestra/data.py` | Shared dataset logic moved unchanged from the script: constants, `read_jsonl`, `validate`, `validate_reviews`, `agreement`, `readiness`, `file_sha256`, `summarize`. Pure functions on rows. |
| `src/orchestra/splits.py` | `make_split` (five-fold `StratifiedGroupKFold`, folds 0-2 train, 3 validation, 4 test, refuses unresolved rows or too few groups), `check_split` (returns every violation of a manifest against the rows), and `materialize` (writes the three partition JSONL files). Manifests carry `row_sha256`, a SHA-256 of each accepted row's canonical `{text, label, group_id}`, so later steps can prove old content is unchanged. `extend_split` builds an M3 child manifest: parent memberships stay put, only new independent groups are allocated by the same private allocator, and it refuses a changed or missing old row, a new row in a parent group, `needs_review` rows, and fewer than five new groups per class. `check_extension` validates the parent and the child with `check_split`, reports moved or dropped parent IDs, then rebuilds the expected child with `extend_split` and reports any difference (reused parent groups, hand-moved new groups, wrong lineage hashes or new-group counts). Rows are passed explicitly. |
| `src/orchestra/__main__.py` | `python -m orchestra` entry point with `argparse` subcommands. `split --config PATH` validates the dataset, writes the immutable split manifest, re-checks it, writes train, validation, and sealed test files, and prints counts and proportions only. `run --config PATH --run-id ID` fits the configured baselines and writes `results/<run-id>/`; `compare --left DIR --right DIR` checks two runs reproduce (exit 0 PASS, 1 FAIL). `extend --config PATH` verifies the parent dataset file against the parent manifest's dataset hash and the parent manifest file against the config's `parent_manifest_sha256` (refuses when null or different), builds and re-checks the child manifest, writes the three M3 files, and prints counts, proportions, and new-group counts only. |
| `src/orchestra/experiment.py` | P3 runner. `FAMILIES` is a table from family id (`B0`, `L2`) to a pipeline builder, its one convergence-retry limit, and its score type; a new family is one more entry. `run` reads only the train and validation files and the split manifest (it never opens the sealed test file or the full dataset file), refuses an empty configuration list, query IDs that differ from the manifest, or an existing run directory, fits each configuration on train text and labels, predicts validation, and writes the artifact files with `manifest.json` last. `compare` verifies both manifests and hashes, then reports differences in config (path-valued fields ignored; input hashes in provenance establish identity), outcomes, ordered predictions (scores within 1e-10), metrics and confusion; timings and timestamps are ignored. It also fails for the same directory or run ID, any outcome that is not `ok`, empty or mismatched predictions, and non-finite scores. A run directory without `manifest.json` is partial. B0 shares the TF-IDF step only for pipeline shape: its fitted vectorizer is unused by the dummy and its predictions ignore text. |
| `configs/m2.json` | Paths and seed for the M2 split and a `configurations` list (`B0`; `L2` with `C=1`; IDs `B0`, `L2-C1`). The test file sits under `data/processed/sealed/` so training code can be pointed at train and validation only. |
| `configs/m3.json` | Paths and seed for the M3 extension. `configurations` is empty until P5 fills it; `run` on it before then has nothing to fit. |
| `docs/evidence/m3-extension.md` | P4 evidence: real `extend` output on an artificial fixture (fixture-only numbers) and the gates still open. |
| `tests/test_splits.py` | Behavioral tests on a generated artificial fixture: whole groups with mixed labels, order independence, fold-to-partition mapping, every `check_split` rejection, extension tests (frozen parent memberships, changed or missing old rows, reused groups, cross-partition families, stale hashes), and the `split` and `extend` CLIs end to end. |
| `tests/test_experiment.py` | Behavioral tests on a generated artificial fixture: dummy majority predictions, held-out vocabulary isolation, literal metrics and confusion counts, score-column order, convergence retry, manifest hashes, tamper and overwrite refusal, missing sealed file, and the two-process reproduction path through the real CLI. |
| `docs/evidence/m2-baselines.md` | P3 evidence: real `run` and `compare` output on an artificial fixture (fixture-only numbers) and the gates still open. |
| `docs/evidence/m2-splits.md` | P2 evidence: setuptools pin, real `split` output on an artificial fixture, and the gates that remain open. |
| `tests/test_validate_dataset.py` | Unit tests that call the validator with small literal rows and check the exact errors and counts, including readiness rejections and ledger agreement. |
| `docs/annotation-guide.md` | Draft v0 procedure for choosing a first action, writing and grouping queries, the pilot row conventions, the review method, and decisions Altan must make before v1. |
| `data/manifests/sources.json` | Provenance manifest. Each `source_id` used by a row names its author, license, and creation date. The license is `null` until Altan chooses one. |
| `.gitignore` | Preserves the initial Python exclusions and adds local data, models, results, secrets, course PDF, and scratch exclusions. It does not protect already tracked files. |
| `LICENSE` | Existing MIT license for repository material. It does not grant rights to external course content or data. |
| `docs/evidence/m1-data.md` | Tooling evidence for P1: real CLI output on an artificial fixture, and the human gates still open. |
| `docs/project-plan.md` | Scope, decision rationale, report evidence map, first-session checklist, and a link to milestone tracking. |
| `docs/m0-plan.md` | Accepted M0 scope, ordered delivery, checks, and the separate student-response gate. |
| `docs/m1-m3-plan.md` | Proposed five-unit implementation sequence for M1 through M3, acceptance checks, split extension, resources, documentation, and the explicit approval boundary. |
| `docs/study-guides/m1-m3-methods-preview.md` | Explanation of the proposed methods for exam, presentation, and report support. Contains no results or claimed student responses. |
| `docs/evidence/m1-m3-planning.md` | Actual planning checks, review evidence, workflow adaptations, and remaining implementation limits. |
| `docs/evidence/m1-m3-decisions.tsv` | Dated planning decisions with evidence pointers. Planned choices are labeled separately from verified checks. |
| `docs/study-guides/README.md` | PDF location, edition evidence, refresh procedure, and coverage planned for each milestone. |
| `docs/study-guides/m0-preparation.md` | Editable M0 lesson and technical appendix explaining the current script and its course connections. |
| `docs/data-and-evaluation.md` | Proposed first-action labels, row schema, annotation/split protocol, experiments, confidence, and reproducibility. |
| `docs/course-sources.md` | Source locations, exact course page mapping, and requirement fingerprints. |
| `docs/repo-guide.md` | This living explanation of authored files and data flow. |
| `docs/learning-log.md` | Change explanations, actual verification, questions, and evidence-based understanding status. |

The smoke script checks the environment. Behavioral tests for project code live under `tests/` and run with `uv run --locked python -m unittest discover -s tests`. The shared validation code lives in `src/orchestra/data.py`; `scripts/validate_dataset.py` keeps the documented command line. New files must be added to this guide when created.

## The executable flow today

uv reads `.python-version`, `pyproject.toml`, and `uv.lock`, then creates the ignored `.venv/` environment. The smoke script imports scikit-learn and its numerical dependencies from that environment.

The script fits a TF-IDF vectorizer on toy training text. It transforms a separate held-out query using the already learned vocabulary. The checks verify a sparse, nonempty feature matrix and ensure the held-out-only word `quasar` never enters that vocabulary. Fitting learns the representation's vocabulary and IDF statistics; transforming uses them without learning new words.

The dummy classifier learns the most frequent toy label and predicts it for every held-out query. Its labels are fixture labels, not the proposed four routing actions. A prediction of `simple` proves only that fit/predict executes as expected. It does not establish semantic understanding or routing quality.

Our code owns fixture selection, call order, and assertions. scikit-learn owns tokenization, TF-IDF, and the dummy estimator. NumPy/SciPy own numerical arrays and sparse matrix operations. Altan needs to explain those concepts and their inputs/outputs, but this repository does not implement library internals.

## The planned research flow

Consider "Calculate the increase using the figures in the attached report." Its proposed first action is `document_retrieval`, because the numbers must be read before any calculation. Annotation records that rationale and a group ID shared by related paraphrases.

The validator now checks the row's fields and provenance. Only rows whose status is `accepted` after annotation review will enter the splits. A persisted split assigns its whole group to one partition. If the row belongs to validation, the fitted training pipeline transforms it and predicts one of the four actions. The evaluation compares that prediction with the annotated first action. A confidence policy may later abstain. No document is actually retrieved in the initial study.

This flow is not executable yet. The first implementation session in the [plan](project-plan.md#first-work-session-after-preparation) defines the next steps and its completion condition.

## Proposed layout as the study grows

The following directories are planned, not empty packages created in advance.

| Path | Intended content and Git policy |
| --- | --- |
| `src/orchestra/` | Reusable validation and split code now; training and evaluation modules arrive with later units. Track authored modules. |
| `tests/` and `tests/fixtures/` | Focused behavioral checks and small cleared fixtures. Track both. |
| `data/raw/`, `data/processed/` | Local acquired and derived rows. Ignored. Preserve source/license manifests separately. |
| `data/manifests/`, `data/splits/` | Proposed tracked provenance and stable split-ID manifests after privacy review. |
| `configs/` | Tracked experiment configurations; `m2.json` exists. |
| `results/<run-id>/` | Ignored full metrics, predictions, timing, and configuration copies. Archive for reproducibility. |
| `models/` | Ignored fitted artifacts. Load only trusted locally produced files. |
| `docs/evidence/` | Deliberately selected, cleared small tables and figures that support the report. |
| `work/` | Ignored agent scratch notes, not required to run the project. |

No runtime credential, paid API, external dataset, or pretrained model is needed for today's smoke check. Setup downloads Python or packages when missing. Future artifact retention and resource limits are defined in the [protocol](data-and-evaluation.md#reproducibility-and-resource-budget).
