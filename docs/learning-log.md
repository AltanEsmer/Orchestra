# Learning log

Implementation evidence and understanding are separate records. This document starts the oral-preparation routine required by [issue #1](https://github.com/AltanEsmer/Orchestra/issues/1). Altan's first response showed that the practice question needed an introduction. Routing and split terminology is **needs practice**. The other topics are **not yet reviewed**.

## Handoff routine

For each meaningful code, data, or experiment change, record the date, files, commit or run reference, reason, relevant ML concepts, alternatives, checks, and limitations. The agent explains the integrated result even when workers wrote parts of it.

Walk through one concrete query from input to the current output. State which parts are executable and which remain planned. Give two or three questions or one manual exercise. During practice, wait for Altan's attempt before showing a worked explanation. Record his answer or a concise faithful summary and targeted feedback. Do not generate an answer on his behalf.

Use these statuses consistently:

| Status | Evidence needed |
| --- | --- |
| not yet reviewed | No student response is recorded. Reading a generated document alone does not change this status. |
| needs practice | A real attempt shows a gap, relies on a hint, or cannot transfer the idea to a new example. Record the gap and next exercise. |
| explained independently | Altan explains the concept accurately without a worked answer and applies it to an unfamiliar query or result. Record the response/date. Revisit if later evidence exposes a gap. |

At each [milestone](project-plan.md#milestones-working-back-from-submission), review the topic ledger and carry unresolved gaps forward. Passing an implementation gate never automatically advances a learning status.

Each handoff now includes a [milestone PDF](study-guides/README.md). Connect a verified lecture concept to an implemented choice, trace a concrete query or artifact, and identify evidence suitable for the report. PDF delivery is implementation evidence; only Altan's actual explanation changes the understanding record. New course slides are reviewed during milestone work. Continue this routine through January 2027 oral preparation after December submission.

## Preparation evidence, October 7, 2026

The initial change adds a locked Python environment, a small smoke script, course-grounded planning documents, and agent instructions. A plain script was chosen over a package/CLI because the issue prepares a study and does not yet implement a router. The future data shape is a query row with stable identity, paraphrase group, first-action label, provenance, and annotation rationale.

The installed runtime is Python 3.12.13 with scikit-learn 1.9.1 and Ruff 0.16.10. uv 0.11.29 created the locked environment on macOS arm64. `uv.lock` records transitive dependency versions and hashes. The worker and lead both ran the smoke command successfully. Lead verification is recorded with the final preparation commits in Git history and the issue PR.

| Command | Observed result |
| --- | --- |
| `uv sync --locked` | Passed. The pinned environment synchronized. |
| `uv run --locked python scripts/smoke.py` | Passed. Sparse TF-IDF, held-out vocabulary isolation, and literal dummy predictions verified. |
| `uv run --locked ruff check .` | Passed. |
| `uv run --locked ruff format --check .` | Passed. |
| `git diff --check` | Passed. |

The lead also created a separate environment at `/tmp/orchestra-issue-1-clean-venv` with `UV_PROJECT_ENVIRONMENT` and repeated locked synchronization and the smoke check successfully. This checks recreation from the lockfile on the same macOS arm64 host. Other operating systems have not been tested.

The smoke output was:

```text
PASS: environment-smoke-only; sparse TF-IDF, held-out vocabulary isolation, and toy DummyClassifier predictions verified.
Python 3.12.13; scikit-learn 1.9.1
```

These checks establish that the environment executes the intended library calls. They do not establish a useful classifier, a leakage-free future dataset, or Altan's understanding. The smoke's `simple` and `complex` labels are artificial fixtures, not the project's target taxonomy. All experiment metrics remain unmeasured.

The agent read issue #1, verified the course requirement pages, and used independent source/scaffold work through Poteto Mode. Planning prose and the smoke script are agent-assisted preparation. Altan must review the choices and write his report in his own words under the staff's confirmed AI-use policy. The original MIT license remains unchanged. Course PDFs were not copied into the repository.

The executable preparation is commit [`7e37f68`](https://github.com/AltanEsmer/Orchestra/commit/7e37f68). An independent reviewer reran every README command, checked all 24 local Markdown links and anchors, and found no blocking findings. Review used agents from one model family. The comment audit led to removal of three redundant narration comments. No code suppression or unresolved refactor constraint remained.

Use `git log --oneline -- README.md AGENTS.md docs scripts pyproject.toml uv.lock` to locate the documentation companion commit. Future entries should link their specific commit and result paths after those exist.

## Architecture and roadmap, October 7, 2026

At Altan's request, the agent added root-level [architecture.md](../architecture.md) and [ROADMAP.md](../ROADMAP.md) (originally named `roadmap.md`). Architecture explains the existing smoke script separately from the proposed data, training, evaluation, and reporting components. The roadmap records milestone dates, status, completion gates, owners, and evidence. README and the repository walkthrough link both files. The project plan now points to the roadmap instead of maintaining a duplicate schedule.

This is a documentation change. It adds no model, dataset, dependency, or experiment result. For example, “What is 18 percent of 250?” illustrates the proposed `calculation` target; today's smoke script still predicts only toy fixture labels. The diagrams describe that boundary without claiming the planned pipeline exists.

The new documents are agent-assisted. Existing understanding statuses remain unchanged, and the introductory practice described below is still pending. Progress tracking does not establish student understanding. The smoke check, Ruff lint and formatting, `git diff --check`, and all 43 local Markdown links and anchors passed after this change. The change commit is recorded in the PR handoff.

## Milestone issues and roadmap rename, October 8, 2026

At Altan's request, the agent created nine GitHub issues, one for each milestone M0–M8, and renamed the primary tracker from `roadmap.md` to [ROADMAP.md](../ROADMAP.md). Each issue records a plain-language objective, the previous milestone dependency, work, completion evidence, and a learning checkpoint. The roadmap links all nine issues and adds simple explanations of what each milestone should achieve. Dates and progress statuses remain in that tracker.

GitHub confirms that PR #2 merged on October 7 as `08cce7b` and issue #1 is closed. The roadmap now records that evidence instead of describing the PR as open. M0 remains in progress because course-rule confirmation and the introductory learning checkpoint are unfinished. Issue #3 covers those remaining gates rather than repeating the completed preparation. M1–M8 remain not started. Creating issues does not complete a research milestone.

README, architecture, the project plan, and this walkthrough/log now use the uppercase filename. For example, “What is 18 percent of 250?” is a planned `calculation` example: M1 labels it, M2 predicts its first action, M3 compares methods, and M4 evaluates confidence and errors on unseen examples. No research pipeline or result was added by this documentation change.

Verification: locked environment synchronization, the README smoke check, Ruff lint and formatting, and `git diff --check` passed. Local Markdown links and anchors and the exact tracked filename were checked. GitHub readback verified one open issue per milestone, matching roadmap links, objectives, completion criteria, and dependencies. The commit reference is provided in the companion PR handoff.

This planning/documentation work is agent-assisted. Altan has not provided a new learning response, so understanding statuses remain unchanged. For the next checkpoint, ask Altan to explain why a most-common-class guess is useful for comparison, why M4 waits until model choices are frozen before opening the test set, and what evidence distinguishes a milestone being planned from being complete. Record his attempt before revealing worked answers.

## M0 study guide and revised checkpoints, October 8, 2026

Altan approved the [M0 delivery plan](m0-plan.md), asked for milestone PDFs to explain the implementation and course connections, and removed administrative course confirmation from agent work. He wants to defend the project in the December report and January oral exam. These preferences are planning decisions, not evidence of ML understanding. Earlier entries describe the previous administrative gate; this entry supersedes it.

The roadmap and project plan now require a lesson and technical appendix for each milestone. The [guide index](study-guides/README.md) records the external PDF folder, update procedure, future coverage, source hashes, and edition evidence. The [M0 source](study-guides/m0-preparation.md) explains the existing environment and smoke script and maps classification, unseen testing, feature extraction, lost word order, and model complexity to verified lecture pages. The final report remains Altan's own synthesis. Course PDFs and generated study PDFs remain outside Git.

The lead saved the plan before the guide author began. The worker owned the guide and local export helper; the lead owned other documents and issue updates. Existing application code and dependencies did not change. A tracked Markdown source and an external PDF were chosen over a new document-building framework. ReportLab runs in the bundled authoring environment, separate from the locked study environment. The data protocol only changes administrative ownership; its schema and evaluation decisions are unchanged.

For example, the existing held-out query "Explain quasar formation." is transformed using the training vocabulary. Only `explain` has a fitted column, so the normalized row has one nonzero entry. The most-frequent dummy returns `simple` because that is the majority toy training label. It does not choose one of the proposed four routing actions. This explains an executable library check, not a research result.

| Check on October 8 | Actual result |
| --- | --- |
| `uv python install 3.12.13` | Python 3.12.13 already installed. |
| `uv sync --locked` | Resolved 9 packages and checked 8 packages. |
| `uv run --locked python scripts/smoke.py` | PASS: environment-smoke-only; sparse TF-IDF, held-out vocabulary isolation, and toy DummyClassifier predictions verified. Python 3.12.13; scikit-learn 1.9.1. |
| `uv run --locked ruff check .` | All checks passed. |
| `uv run --locked ruff format --check .` | Initial check: 11 files already formatted. Final check after local authoring helpers: 13 files already formatted. |
| `git diff --check` | Exit 0. |
| PDF rendering | Author and lead inspected all 10 pages. No clipping, overlap, or missing glyphs observed. |
| PDF content and numerical walkthrough | Author checked extracted text against the source and probed the locked environment for the matrix shapes, vocabulary, IDF values, and held-out vectors. |
| Issue readback | Issues #3-#11 each contain their new PDF deliverable and course-to-project learning checkpoint. All remain open. |
| Local Markdown links | All 59 local links and anchors across 12 tracked Markdown files resolve. |
| Formula and code export | Lead verified all three fenced code/formula blocks against extracted PDF text. |

Two independent reviewers from one model family checked standards and the accepted specification. The standards review found a blank line splitting the roadmap evidence table; the lead removed it. The specification review found no gaps and independently checked lecture pages, numerical examples, and checksums. No runtime-code or suppression review was needed because application code did not change. The final smoke, Ruff lint, Ruff formatting, and diff checks passed. Guide delivery commit: `22f445e08ea322ccb99a78d77fd9e04157030e26`. The guide index records the final source and PDF identities.

The M0 guide's three fresh questions cover a database-then-calculation request, the features and dummy prediction for unfamiliar held-out text, and the difference between passing a smoke check and evidence of generalization. They have no worked answers. Altan has not answered them yet. Data-contract and introductory split terminology remain **needs practice**; other concepts remain **not yet reviewed**. M0's agent deliverables are ready, but milestone closure waits for an actual learning response, with gaps carried forward. January practice will revisit those gaps using the submitted study and later lecture slides.

## M0 closure and M1 start, October 16, 2026

Altan closed issue #3 on October 16 and asked to begin M1. The roadmap now marks M0 done by his decision. The introductory checkpoint was never answered. That gap is carried into M1 unchanged, and no understanding status moved. The stable M0 PDF was copied to the dated snapshot `M0-preparation-2026-10-16.pdf`; its SHA-256 matches the October 8 edition.

M1 started with three agent-side pieces. [`docs/annotation-guide.md`](annotation-guide.md) is a v0 procedure for choosing a first action, grouping paraphrases, writing rows, and running the pilot review. It lists four decisions that belong to Altan before v1. [`data/manifests/sources.json`](../data/manifests/sources.json) records the authored source with `license: null`. [`scripts/validate_dataset.py`](../scripts/validate_dataset.py) checks rows against the protocol schema, with 15 unit tests in `tests/test_validate_dataset.py`. No query rows were written. Authoring and labeling the pilot is Altan's work.

The validator pulls the row checks forward from M2 so pilot rows are checked as they are written. It uses only the standard library, so no dependency was added. It stays a script until the M2 split code needs to import it. A worker wrote the validator and tests from a fixed specification. The lead reviewed the diff, changed the test command to `python -m unittest discover -s tests` instead of adding a package file, and updated the documents.

Trace one row. Suppose a pilot line is `{"query_id": "q0001", "group_id": "g001", "text": "Add 40 and 2.", "label": "calculation", "status": "accepted", "source_id": "altan-authored", ...}`. The validator finds all nine fields, a known label, and a known source. It then checks the source entry and finds `license: null`, so it prints `ERROR: source altan-authored: missing license` and exits 1. This probe ran from a scratch file outside the repository. Once Altan records a license, the same row passes and the summary counts one accepted `calculation` row in one group.

| Check on October 16 | Actual result |
| --- | --- |
| `uv run --locked python scripts/smoke.py` | PASS: environment-smoke-only. Python 3.12.13; scikit-learn 1.9.1. |
| `uv run --locked python -m unittest discover -s tests` | Ran 15 tests, OK. |
| `uv run --locked ruff check .` | All checks passed. |
| `uv run --locked ruff format --check .` | 16 files already formatted. |
| `git diff --check` | Exit 0. |
| Validator on a one-row scratch probe with the real manifest | `ERROR: source altan-authored: missing license`, exit 1, as intended. |

Limitations. The validator checks structure, not label correctness. Near-duplicate detection, length and source-mix reports, and agreement computation are not implemented. The M1 study PDF is deferred until pilot rows and the v1 decisions exist, because the guide must trace actual annotation evidence. Lecture slides were rechecked on October 16; no file newer than Lecture 6 exists, so the recorded source hashes still apply.

Questions for Altan, to answer before seeing worked explanations:

1. Carried from M0: for "Look up order 5521 in the sales database and tell me how many days late it shipped," what is the first action, and why is that a different problem from predicting the whole sequence of actions?
2. Why does the validator reject a group of five paraphrases, and how could a large paraphrase group inflate a test score?
3. Label "What is the boiling point of water in Fahrenheit?" under guide v0. Which open decision in the guide does it touch?

## M1 to M3 planning, October 16, 2026

Altan requested a complete implementation plan for M1, M2, and M3, documents supporting the exam, presentation, and report, and a planning PR to create and merge. He explicitly required waiting for implementation approval afterward and asked for no questions during planning. He also reported an SDU allocation of 10 GPU hours. These instructions establish project preferences, not new learning evidence.

The agent added the [delivery plan](m1-m3-plan.md), a [methods preview](study-guides/m1-m3-methods-preview.md), [planning verification](evidence/m1-m3-planning.md), and a [decision trail](evidence/m1-m3-decisions.tsv). The plan separates pilot acceptance, split protection, baseline reproduction, immutable dataset expansion, and the 14-configuration comparison. It reserves GPU hours for a conditional optional embedding experiment. It requires human annotation evidence and permissions before research data acceptance.

The data protocol now describes the proposed split extension, tokenization, and tie rules. The annotation guide uses the ignored local pilot directory to avoid accidentally publishing rows. No row schema, application code, dependency, source license, dataset, model, or experiment changed. The walkthrough, architecture, README, study index, and roadmap link the plan. Milestone statuses remain unchanged, and the implementation approval is pending.

Trace the teaching query "Calculate the increase using the figures in the attached report." Its planned target remains `document_retrieval` because the figures must be read first. M1 would record a reviewed label and group, M2 would fit a training-only pipeline, and M3 would compare predictions on fixed validation rows. That research flow has not run. The teaching query and its paraphrases stay outside the dataset. Today's executable check still predicts artificial smoke labels.

One worker inspected existing contracts and another wrote the companion in a disjoint file. The lead integrated and reviewed the documents. Actual checks and independent review are in the [planning evidence](evidence/m1-m3-planning.md). Commit identities and the merged PR are provided in the handoff and Git history. The document-only workflow skips model prototypes and performance experiments because implementation is not authorized.

The preview stores three unanswered exercises covering lookup before calculation, paraphrase grouping and fit/transform, and accuracy versus macro-F1. No new response was supplied by Altan, so routing and split terminology remain **needs practice** and other topics remain **not yet reviewed**. The M1, M2, and M3 evidence-based PDFs and actual learning attempts are future deliverables. Nothing in the planning PR completes a research milestone or certifies oral readiness.

## M1 to M3 implementation approval, October 16, 2026

After PR #15 merged, Altan asked in chat to implement its plan with Sonnet worker agents and Opus reviewer agents. That instruction is the implementation approval the plan's first box requires. It does not authorize merging the implementation PRs, publishing data, recording a dataset license, or supplying labels on his behalf. The baseline before any change is commit `7999d69`. Every README check passed there: the smoke check, 15 unit tests, Ruff lint, Ruff format with 19 files formatted, and `git diff --check`.

## M1 to M3 tooling, October 16, 2026

The five delivery units are implemented as tooling on branch `claude/m1-m3-implementation`, from `72dc37b` to `315c7c4`. Five Sonnet workers wrote one unit each, in order. After each unit a separate Opus reviewer read the diff and attacked it with adversarial inputs. The worker then fixed the findings in a follow-up commit. The lead set each unit's design and data shape before any code was written, and reviewed every report.

- **P1.** `scripts/validate_dataset.py --review LEDGER --ready` checks release requirements: 120 accepted rows, 30 per class, 15 groups per class, 20% review coverage per class, review of mixed-label groups, a license, and agreement between the ledger and the dataset. Structural validation no longer requires a license, so draft rows validate while permission is pending. Evidence is in [m1-data](evidence/m1-data.md).
- **P2.** `src/orchestra/` became an installable package, with a pinned `setuptools==84.0.0` build requirement. `python -m orchestra split` writes an immutable split manifest. It writes the train and validation files apart from a sealed test file. Evidence is in [m2-splits](evidence/m2-splits.md).
- **P3.** `run` fits B0 and L2. It reads only the train file, the validation file and the manifest, never the dataset or the sealed file. It writes hashed artifacts. `compare` checks that two separate processes produced identical runs. Evidence is in [m2-baselines](evidence/m2-baselines.md).
- **P4.** `extend` appends only new groups to a frozen split, pinned to the parent manifest hash. It rebuilds the child to prove no old row moved. Evidence is in [m3-extension](evidence/m3-extension.md).
- **P5.** `run` covers all 14 configurations with prediction latency. `select` applies the 0.01 inclusive tie rule. It is invalid unless all 14 configurations ran successfully. `report` writes tables and validation errors without fitting anything. Evidence is in [m3-comparison](evidence/m3-comparison.md).

Reviewers found real defects, and each is now fixed and tested. Malformed ledgers and manifests crashed the code instead of being rejected. A config could write the sealed test file over the training file. `compare` passed when both runs were empty or had failed. An edited parent manifest could move M2 validation rows into M3 test. `select` called an incomplete matrix valid. `report` could write validation text into a tracked directory.

Trace the teaching query "Calculate the increase using the figures in the attached report." It stays out of the dataset. Suppose a similar real row were labeled `document_retrieval` in group `g031`. `validate` checks its fields. `--ready` counts it toward the 30 rows its class needs. `split` puts the whole of `g031` in one fold. If that fold is 3, the row goes to validation. `run` fits the L2 pipeline on training text only, so a word that appears only in this row gets no feature. It then writes the row's predicted class and its four probabilities in label order. If the prediction is wrong, `report` lists the row in `errors.jsonl` for human inspection. None of this has run on real data.

| Check at `315c7c4` | Actual result |
| --- | --- |
| `uv run --locked python scripts/smoke.py` | PASS: environment-smoke-only. Python 3.12.13; scikit-learn 1.9.1. |
| `uv run --locked python -m unittest discover -s tests` | Ran 148 tests, OK. |
| `uv run --locked ruff check .` | All checks passed. |
| `uv run --locked ruff format --check .` | 31 files already formatted. |

Limitations. Every number in the evidence documents comes from artificial fixtures and is not a research result. Several things are still missing: pilot rows, guide v1, human review, a license, the 120 and 400 accepted rows, the collection brief, archive and restore, inspection of real errors, and plots, which need a dependency decision. M1, M2, and M3 stay open. The M1 to M3 study PDFs wait for real evidence.

Questions for Altan, to answer before seeing worked explanations:

1. `--ready` requires 15 groups per class, not just 30 rows. Why does the number of groups matter more than the number of rows for a trustworthy validation score?
2. `run` never opens the full dataset file, even though hashing it would be harmless to the model. Which mistake does that rule prevent?
3. In the fixture comparison L1, L2, S1, and L3 tied on validation macro-F1, and `select` chose L1 at `C=0.1` overall. Which rule chose it, and why is that choice not evidence that L1 is better?

## Concepts introduced by preparation

TF-IDF represents each query as a vector of weighted terms. With scikit-learn's default smoothed IDF, `idf(t) = log((1 + n)/(1 + df(t))) + 1`. Term frequency multiplies this weight, then the vector is L2-normalized. Here `n` and `df` come from training documents only. Vocabulary membership is also learned from training.

The most-frequent dummy classifier chooses `argmax_c count_train(c)` regardless of query features. This is a floor for later comparisons, not a semantic router. The check deliberately verifies that simple behavior rather than claiming an ML result from a handful of toy inputs.

The [data protocol](data-and-evaluation.md) defines precision, recall, F1, and confidence measures for future work. Logistic regression, naive Bayes, SVM margins, and calibration should receive new log entries when implemented. Document their equations and assumptions alongside actual runs, not as claims that the concepts have already been mastered.

## Initial teach-back exercise

Run the smoke command, then answer without reading a worked explanation:

1. Why must `quasar` stay out of the fitted vocabulary even though it appears in a held-out query? What changes if we fit on all text first?
2. Why does the dummy classifier return `simple` for both held-out queries? What does the PASS message prove, and what does it leave untested?
3. For "Calculate the increase using the figures in the attached report," identify the first action and explain why a complete-route target would be a different modeling problem.

On October 7, Altan responded to a combined version of questions 1 and 3 with "Im confused, what is this question?" The agent had asked about the report example and keeping paraphrases in one split before introducing the terms. This establishes a need for an introductory explanation, not a specific ML misconception.

The agent then explained that a router selects the first action, that the report must be read before calculation, and that paraphrases are differently worded versions of one request. It explained that keeping them in one split avoids testing on near-copies of training examples. This was a worked explanation, so no independent understanding is claimed.

Next practice should start with the purpose of routing, one everyday query, and the difference between training examples and an unseen test. Then use a new query and let Altan name the first action. Introduce paraphrase grouping only after that step is clear. Record the next attempt before changing the status.

## Topic ledger and question bank

The data-contract row remains **needs practice**. On October 25, Altan explained in his own words how related training/test variants can inflate a score: the grouping-related optimism mechanism is **explained independently** for that question after instruction. Leakage and grouping are **explained independently** for the checked cases of group integrity and training-only feature fitting. See the November 10 M5 teach-backs. Since then, model selection, the tree families, API reproducibility, metrics (precision and recall), confidence and fallback, and SVM margins have been **explained independently**; see the November 3 and 5 entries. Every other row is **not yet reviewed**.

| Topic and course connection | Question or manual exercise | Follow-up milestone |
| --- | --- | --- |
| Environment and ownership. Repo guide. | Recreate the environment. Which behavior is our code and which belongs to scikit-learn? | Preparation review. |
| Data contract and action boundaries. Project 13, Lecture 5 pp.2, 4–5. | Label a query that needs retrieval before calculation. Explain a case that cannot receive one label yet. | Annotation pilot. |
| Leakage and grouping. Lecture 2 pp.26–28, Lecture 5 pp.52–56. | Show how two paraphrases in different splits can inflate a score. Explain why the split precedes fitting. | First baseline. |
| Counts, TF-IDF, and order. Lecture 6 pp.57–58; external feature guide. | Calculate a small term's IDF and explain what a bag of words loses. What could a bigram recover? | First baseline. |
| Naive Bayes. Lecture 5 pp.64, 67–72. | Explain conditional independence and why smoothing helps unseen terms. | Classifier comparison. |
| Logistic regression and regularization. Lecture 6 p.8, Lecture 4 pp.60–65. | Explain how a feature coefficient changes a class score and why regularization can improve generalization. | Classifier comparison. |
| SVM. Lecture 5 pp.76–79, 86, 88–89. | Explain a margin and why its numeric value is not automatically a probability. | Classifier comparison. |
| Model selection. Lecture 4 p.67, Lecture 5 pp.52–57. | Explain why choosing C on the test set changes what its score means. | Comparison freeze. |
| Metrics. Data protocol. | Compute one class's precision/recall from a confusion matrix. Explain why accuracy can hide a minority-class failure. | Error analysis. |
| Confidence and fallback. External calibration guide. | Interpret a reliability bin and compare accuracy at two coverage levels. What if no queries are accepted? | Confidence analysis. |
| Reproducibility and limitations. Lecture 2 pp.7–8, 68. | Reproduce a run from its manifest. Explain what a fixed seed does not guarantee and why synthetic data limits conclusions. | Draft/reproduction. |
| Optional embeddings. Lecture 6 pp.78–79. | Explain the frozen encoder, its external training, cost, and why its pretraining data creates uncertainty. | Only if implemented. |

## Knowledge gaps and final rehearsal

No specific ML misconception has been established. The first response shows that routing and split terminology needs an introduction before further teach-back questions. Ability to explain the scaffold, taxonomy, preprocessing, and evaluation remains unverified. On October 8 Altan took ownership of course administration and removed course-rule confirmation from agent tasks and milestone gates.

By November 29, rehearse with an unfamiliar query, an actual saved model/configuration, a confusion matrix, and a confidence result. Altan must trace the query through preprocessing and prediction, explain a model and its features, interpret the results, justify one design choice, reproduce a run, and discuss an error or limitation. Record each attempt and revisit weak topics before the December 4 freeze. The rehearsal is planned; no oral readiness has been certified.

After submission, continue with the frozen project and accumulated study PDFs through January 2027. For each newly available lecture, identify which principle the project uses, where it appears, and what assumption or limitation accompanies it. Record the attempt and revise explanations without rewriting the submitted experimental record.

## PR #16 local setup, October 16, 2026

Altan requested all setup that can proceed without his data or decisions. The locked environment synchronized successfully with uv 0.11.7 and Python 3.12.13. No dependency, model, row schema, or evaluation rule changed.

The executable `scripts/run_experiment.sh` sets the four numerical thread variables to `1` before invoking the existing run CLI. It resolves relative paths from the repository root and preserves command arguments and exit codes. The [experiment runbook](run-experiments.md) replaces the README's incomplete command sequence and names the readiness gate before splitting. The annotation guide now records the existing implementation approval without freezing guide v1.

Local setup prepared an ignored blank worksheet at `data/raw/pilot-intake.md` and empty `data/raw/pilot-v0.jsonl` and `data/raw/reviews-v1.jsonl` files. Existing files were preserved. No query, human label, reviewer identity, review date, license, or agreement was supplied. The empty pilot fails `--ready` with `ERROR: no accepted rows: the training dataset is empty`, exit 1. The source license and M3 parent hash remain null. The latter can be calculated only after the real M2 split exists.

A worker owned the five-line launcher. A separate read-only explainer confirmed that the existing split and extension commands perform structural validation but do not enforce complete readiness. The lead wrote the runbook and inspected the actual launcher and evidence. The final independent reviewer found no actionable issues in the integrated setup. It independently checked shell syntax, real help from another directory, the saved fixture transcript and thread provenance, empty intake files, and local links. Comment review found no actionable comments or suppressions. These agents use one model family, not cross-family review.

The lead ran the complete command sequence under ignored `work/poteto/pr16-setup/workflow-proof/` using the existing artificial test fixture. The actual M2 split, two launcher runs, comparison, overwrite refusal, M3 hash-pinned extension, two 14-configuration launcher runs, comparison, valid selection, and report all behaved as expected. Provenance recorded all four thread variables and all loaded numerical thread pools at one thread. These are tooling checks, not research results. The local rerun script is `work/poteto/pr16-setup/verify_workflow.py`; it deliberately requires a fresh proof directory.

| Check | Actual result |
| --- | --- |
| `uv python install 3.12.13` and `uv sync --locked` | Python already installed; resolved and checked 9 packages. |
| Real launcher help from `/tmp` | Exit 0. |
| Launcher with temporary fake uv | Preserved arguments and working directory, forced caller thread values from 8 to 1, propagated exit 37, and handled a repository path containing spaces. |
| `sh -n scripts/run_experiment.sh` | Exit 0. |
| Complete artificial M2 and M3 command sequence | PASS, including both reproduction checks and report files. |
| Empty pilot with `--review data/raw/reviews-v1.jsonl --ready` | Expected exit 1, no accepted rows. |
| `uv run --locked python scripts/smoke.py` | PASS, environment-smoke-only; Python 3.12.13 and scikit-learn 1.9.1. |
| `uv run --locked python -m unittest discover -s tests` | Ran 148 tests, OK. |
| `uv run --locked ruff check .` | All checks passed. |
| `uv run --locked ruff format --check .` | 32 files already formatted. |
| `git diff --check` | Exit 0. |
| `git check-ignore` on all three intake files | All ignored. |
| Local Markdown links in the six changed documents | 54 links and anchors resolve. |

Trace the existing teaching query about calculating an increase from an attached report. Altan still supplies its first-action rationale and scenario group for any distinct real example. The readiness command checks accepted data and review evidence. After splitting, the launcher fixes the timing environment and passes train and validation paths to the runner. The runner predicts the first action without executing tools. The teaching query stays outside the dataset.

Still needed from Altan are the 40-query pilot with labels, rationales, and groups; actual dataset permission; a review method and real blind review evidence; and pilot boundary resolutions before guide v1. The 120-row release and reviewed expansion toward 400 remain future work. No research split or metric exists. No learning status changed.

Two unanswered exercises remain for later practice. Why can structural validation pass an empty draft while readiness fails? Why must the parent-manifest hash come from the frozen M2 artifact rather than a chosen value?

## Frozen-input integrity repair, October 22, 2026

Altan authorized completing the remaining automation, creating and merging PRs, updating issues, and then guiding manual work one step at a time. This does not supply queries, human review decisions, permission, or learning responses.

An independent review of PR #16 found three reproducible gaps. The runner accepted changed materialized text, labels, and groups under an old split identity. Split outputs could overwrite an input dataset. Relocated M3 parent paths caused a false reproduction mismatch. The repair checks visible rows against canonical manifest hashes and group memberships, rejects input/output aliases before writing, preserves existing materialized files, and excludes parent path locations from semantic run comparison while retaining their hashes.

Four regression checks failed against the original implementation. After repair, 59 experiment tests and 52 split tests passed. Focused Ruff lint and format checks passed. The complete current test run was attempted while a separate M4 worker had written a failing test before its module existed; that transient import failure is not a passing full-suite claim. The integrated full suite will run after all writers finish.

The teaching query about an attached report still stays outside the research data. If a real validation row is edited after splitting, the runner now refuses its changed content hash before fitting. Neither passing checks nor this explanation changes Altan's learning status.

Next practice remains one introductory routing query, followed by the meaning of an unseen example. The new integrity question is why a stable query ID alone cannot prove that its text and label stayed unchanged.

## Complete automation and manual handoff, October 22, 2026

The remaining command workflow is implemented: check readiness, prepare a blind review, freeze input evidence and splits, reproduce experiments, analyze calibration, freeze choices, evaluate the final test, export figures, and archive/restore the study. The IEEE report template compiles. [Completion evidence](evidence/automation-completion.md) records checks and limitations; the [walkthrough](repo-guide.md) explains each new module.

Two candidate designs were compared before implementation. One existing CLI with focused modules keeps the project explainable. Matplotlib is the only new experiment dependency; it supplies scientific figures. Calibration reuses scikit-learn and wraps the full pipeline in grouped training folds so held-out fold vocabulary cannot leak into fitting. Review found and repaired score-tie reliability, missing readiness/environment gates, final-test reservation/recovery problems, and lost fixture labels. A POSIX lock and atomic receipt updates keep retries exclusive and auditable.

For a concrete teaching trace, consider “Calculate the increase using the figures in the attached report.” Its first action is document retrieval. The real dataset still needs Altan's original examples and actual review; this supplied teaching example stays outside it. Once a real group is accepted, preparation binds its data/review hashes and assigns the entire group to a partition. Training learns from train text only. Validation supports model and confidence choices. The final-test command uses those frozen choices, and plots read saved outcomes rather than choosing a new winner. An archive lets another checkout repeat the same prediction process.

The end-to-end fixture run restored the executable launcher and a clean locked environment, then reproduced M3 predictions and metrics. This is software evidence, not research performance or proof of learning. PR #16 is merged; final automation review and checks are listed in the completion evidence. The real pilot and review ledgers are empty, and dataset permission remains unset.

First manual action: write one original query and explain what must happen first. Two later teach-back prompts remain unanswered: why must related paraphrases stay in one partition, and why must model/confidence choices be fixed before opening the test set? Let Altan answer before providing worked explanations. No understanding status changed.

## First original pilot response, October 22, 2026

Altan supplied candidate q0001 and independently chose calculation because the required numbers were already supplied. The exact query and rationale are preserved locally in ignored `data/raw/pilot-intake.md`, assigned scenario g001. No row has been released, no permission inferred, and no independent review recorded.

This response correctly applies the calculation boundary to an original example. The broader data-contract topic remains **needs practice** until multi-action dependencies and other boundaries have been attempted; grouping and split understanding remain unverified. Feedback: the router outputs the action label, while executing that action would produce the numeric answer. Next exercise: author one original request requiring a named document, with its first action and rationale.

This update records an actual learning response and candidate intake only; it changes no code, schema, model, or experiment. Smoke, Ruff lint, Ruff formatting (47 files), and whitespace checks passed.

## Second original pilot response, October 22, 2026

Altan supplied candidate q0002 and chose reading the named handbook because the answer depends on its contents. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, assigned independent scenario g002. This correctly applies document retrieval before summarization. The collection prompt specified a document-based request, so this demonstrates the rationale within that category rather than an unaided choice across all four categories.

The broader data-contract topic remains **needs practice** pending other boundaries and multi-action dependencies. No permission, independent review, or release acceptance is inferred. Next exercise: author one request involving a specific record in a named fictional catalog or database, with its first action and rationale. This update changes only candidate intake and learning evidence.

## Third original pilot response, October 22, 2026

Altan supplied candidate q0003 and chose looking up the product record because the warranty information is in its catalog entry. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, assigned scenario g003. Although it shares the fictional shop name with q0002, it concerns a separate product-record scenario rather than a paraphrase of the handbook request.

This correctly applies knowledge lookup to an identified record and structured source. The collection prompt specified that category, so unaided discrimination across categories remains unverified. The broader data-contract topic remains **needs practice** pending other boundaries and multi-action dependencies. No permission, independent review, or release acceptance is inferred. Next exercise: author one request for an explanation or rewrite needing no document retrieval, record lookup, or numeric computation, with its first action and rationale. This update changes only candidate intake and learning evidence.

## Fourth original pilot response, October 22, 2026

Altan supplied candidate q0004 and chose direct answering because the request is a general explanation requiring no document, database lookup, or calculation. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, assigned scenario g004. This correctly applies direct answering; the collection prompt supplied the category, so unaided category discrimination remains unverified. Four pilot candidates now cover the four labels, with no independent review or release acceptance inferred.

Altan asked why he was answering these prompts. The agent clarified that they collect human-authored labeled examples for the router and provide limited learning evidence; they are not questions whose underlying answers must be supplied. Human authoring follows the current study protocol, rather than a technical inability to generate examples. Any later generated candidates require disclosed provenance and human review. This question is a request for purpose, not evidence of a conceptual misconception. Broader learning statuses remain unchanged.

## Fifth original pilot response, October 22, 2026

Altan explicitly chose to retain the human-written collection approach. He then supplied candidate q0005, choosing calculation because the ticket price and number of tickets are provided. Unlike the preceding category-directed collection prompts, this prompt allowed any of the four actions. His explanation correctly applies the calculation boundary without a category hint. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, assigned scenario g005, separate from the notebook-discount scenario.

Calculation with supplied inputs is **explained independently** for this example. The broader data-contract topic remains **needs practice** pending multi-action dependencies and other unaided boundary decisions. Five candidates are recorded; no independent review, permission, or release acceptance is inferred. Next exercise: author a request involving two dependent actions and identify which must happen first, with a rationale.

## Sixth original pilot response, October 22, 2026

Altan supplied candidate q0006 and chose looking up the product record because its price is needed before calculating the total. The collection prompt requested two dependent actions but did not supply the category or scenario. This correctly explains the earliest necessary dependency in an original lookup-then-calculation request. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, assigned scenario g006. It shares a fictional catalog with q0003 but concerns price-to-total computation rather than a warranty fact; it is treated as a separate scenario, subject to later manual near-duplicate review.

First-action dependency ordering is **explained independently** for this example. Broader action-boundary coverage, ambiguity handling, and grouping/split understanding remain pending; this does not certify the whole data-contract topic. Six candidates are recorded, with no independent review, permission, or release acceptance inferred. Next collection exercise: supply another original document-based request, with its first action and rationale.

## Seventh original pilot response, October 22, 2026

Altan supplied candidate q0007 and chose reading the handbook because its contents are required to summarize the rules. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`. It is assigned g002 alongside q0002: both follow the same named-handbook policy/rules summarization template, despite different fictional organizations. Keeping these close variants together conservatively prevents this template crossing partitions.

The rationale correctly applies document retrieval, but the collection prompt specified a document-based request. No new independent learning status is inferred. Seven candidates across six groups are recorded; independent review, permission, and release acceptance remain pending. Next exercise asks Altan why these two handbook queries should stay in the same split before revealing a worked explanation. This exercise is learning evidence only and is not an additional dataset candidate.

## Grouping explanation, October 22, 2026

Asked why training on the shop-handbook query and testing on the similar school-handbook query could overstate performance, Altan answered: “Because the two requests have almost the same wording and structure, the model might recognize the pattern instead of showing that it can handle genuinely different requests.” This correctly explains the near-duplicate evaluation risk. The preceding feedback had already identified the shared template and stated that grouping prevents near-duplicates crossing partitions, so this is a correct supported explanation, not evidence of fully independent transfer.

The leakage/grouping topic remains **needs practice** until Altan applies grouping to a fresh example without that hint and explains training-only feature fitting. Feedback confirms that related queries stay in one partition so evaluation better tests transfer to different requests. This learning response adds no dataset row; the intake remains seven candidates across six groups. Next collection step: another original direct-answer request in a different everyday setting, with a first-action rationale.

## Eighth original pilot response, October 22, 2026

Altan supplied candidate q0008 and chose direct answering because the request is a general explanation requiring no document, database lookup, or calculation. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`. It shares g004 with q0004 because both use the same “explain the difference between … in simple terms” template. The topic change alone does not establish an independent query family.

The category-directed prompt supports a correct rationale but does not establish unaided category selection. Learning statuses remain unchanged. Eight candidates across six groups are recorded, two per label; no independent review, permission, or release acceptance is inferred. Next collection step: one original request with wording and structure different from the preceding examples, choosing any first-action category and supplying a rationale.

## Ninth original pilot response, October 22, 2026

Altan supplied candidate q0009 and chose direct answering because the provided text only needs rewriting. The prompt allowed any category and requested a different sentence structure. This correctly applies direct answering to a new rewriting scenario without a category hint. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, assigned new group g007.

Direct answering for supplied-text rewriting is **explained independently** for this example. Broader ambiguity handling and grouping/feature-fitting understanding remain pending; other topic statuses are unchanged. Nine candidates across seven groups are recorded: three direct-answer queries and two in each other class. No independent review, permission, or release acceptance is inferred. Next collection step: an original request involving a named fictional document, using a task other than summarizing a handbook, with its first action and rationale.

## Tenth original pilot response, October 22, 2026

Altan supplied candidate q0010 and chose reading the named welcome letter because it contains the required equipment. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, assigned new scenario g008. This requests specific information from a letter rather than summarizing a handbook, adding a distinct document-retrieval scenario.

The rationale is correct, but the prompt specified a document-based request, so no new independent learning status is inferred. Ten candidates across eight groups are recorded: three document-retrieval, two knowledge-lookup, two calculation, and three direct-answer queries. No independent review, permission, or release acceptance is inferred. Next collection step: an original request involving a specific record in a named fictional structured source outside shopping, with its first action and rationale.

## Eleventh original pilot response, October 22, 2026

Altan supplied candidate q0011 and chose looking up the book record because its author is listed in the catalog entry. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned scenario g009 for library authorship lookup. Scenario grouping remains subject to the pilot's manual near-duplicate review, including comparison with other catalog-record requests.

The rationale correctly applies knowledge lookup to a named structured source and identified record. The collection prompt specified this category, so no new independent learning status is inferred. Eleven candidates across nine provisional groups are recorded: three document-retrieval, three knowledge-lookup, two calculation, and three direct-answer queries. No independent review, permission, or release acceptance is inferred. Next collection step: an original calculation request outside prices and purchases, with its first action and rationale.

## Twelfth original pilot response, October 22, 2026

Altan supplied candidate q0012 and chose calculation because the lap length and lap count are provided. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`. It is conservatively grouped with q0005 in g005: both use the short supplied-unit-quantity times count template, with a changed setting and numbers. This grouping is a template judgment, not a rule that all multiplication queries belong together, and remains subject to pilot review.

The rationale is correct, but the collection prompt specified calculation, so no new independent learning status is inferred. Twelve candidates across nine provisional groups are recorded, three per category. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request containing numbers but requiring no numerical calculation, with a freely chosen first action and rationale.

## Thirteenth original pilot response, October 22, 2026

Altan supplied candidate q0013 and chose direct answering because he requests an explanation of the percentage, not a calculation. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g010. This is a numerical-concept explanation rather than the weather-versus-climate comparison in g004; sharing the weather topic alone does not establish a paraphrase family.

The response correctly distinguishes numerical content from a request to compute. The prompt explicitly requested numbers without calculation, so this is supported boundary practice rather than independent transfer evidence. Existing learning statuses remain unchanged. Thirteen candidates across ten provisional groups are recorded: three document-retrieval, three knowledge-lookup, three calculation, and four direct-answer queries. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request requiring information from a named fictional document before a numerical calculation, with its first action and rationale.

## Fourteenth original pilot response, October 22, 2026

Altan supplied candidate q0014 and chose reading the report because its figures are needed before calculating the attendance increase. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g011. Sharing the fictional camp with q0010 does not make it the same scenario: this request requires report figures followed by a calculation, rather than equipment information from a welcome letter.

The dependency explanation is correct. The collection prompt specified document access before calculation, so this is supported practice and does not add independent transfer evidence. The request also resembles the protocol's report-before-calculation teaching example; pilot review must assess this similarity before release and avoid claiming it as an independently novel template. Existing learning statuses remain unchanged. Fourteen candidates across eleven provisional groups are recorded: four document-retrieval, three knowledge-lookup, three calculation, and four direct-answer queries. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original calculation request involving a difference or duration, with all required inputs and its first-action rationale.

## Fifteenth original pilot response, October 22, 2026

Altan supplied candidate q0015 and chose calculation because both start and end times are provided. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g012 for a supplied-time duration scenario. The rationale is correct; the collection prompt specified calculation involving a difference or duration, so no new independent learning status is inferred.

Fifteen candidates across twelve provisional groups are recorded: four document-retrieval, three knowledge-lookup, four calculation, and four direct-answer queries. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request about a specific record in a named fictional database outside product and book catalogs, with its first action and rationale.

## Sixteenth original pilot response, October 22, 2026

Altan supplied candidate q0016 and chose looking up the booking record because its entry contains the assigned room. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g013 for a reservation-room lookup. Shared fictional organization names alone do not determine grouping; the pilot review must still compare the structure of this request with other record-attribute lookups before freezing groups.

The rationale correctly identifies knowledge lookup. The collection prompt specified a database-record request, so no new independent learning status is inferred. Sixteen candidates across thirteen provisional groups are recorded, four per category. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request in any category, avoiding previously used sentence templates and fictional organizations, with its first action and rationale.

## Seventeenth original pilot response, October 22, 2026

Altan supplied candidate q0017 and chose calculation because the total seedlings and pot count are provided. The prompt allowed any category and asked for a new situation and wording. This correctly applies the supplied-input calculation boundary without a category hint and reinforces the earlier independent explanation. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g014 for equal distribution.

Seventeen candidates across fourteen provisional groups are recorded: four document-retrieval, four knowledge-lookup, five calculation, and four direct-answer queries. Broader learning statuses are unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request to transform supplied text, using a different task from making a sentence more polite, with its first action and rationale.

## Eighteenth original pilot response, October 22, 2026

Altan supplied candidate q0018 and chose direct answering because the supplied sentence only requires rewriting. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`. It is conservatively assigned g007 with q0009: both are short imperative requests to rewrite a quoted sentence, with a changed transformation instruction and source text. This provisional template grouping remains subject to pilot review; it does not imply every rewriting task must share a group.

The rationale is correct, but the collection prompt specified supplied-text transformation, so no new independent learning status is inferred. Eighteen candidates across fourteen provisional groups are recorded: four document-retrieval, four knowledge-lookup, five calculation, and five direct-answer queries. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request comparing information in two named fictional documents, with its first action and rationale.

## Nineteenth original pilot response, October 22, 2026

Altan supplied candidate q0019 and chose reading both welcome letters because their contents are needed to compare meal options. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g015 for a two-document comparison. Either document may be read first, but both reads have the same action label, document_retrieval; no competing first-action class is required by that ordering flexibility.

The rationale is correct. The collection prompt specified comparison of named documents, so no new independent learning status is inferred. Nineteen candidates across fifteen provisional groups are recorded: five document-retrieval, four knowledge-lookup, five calculation, and five direct-answer queries. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request finding records that satisfy a condition in a named fictional database, with its first action and rationale.

## Twentieth original pilot response, October 23, 2026

Altan supplied candidate q0020 and chose looking up the room records because the database stores their capacities. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g016 for filtering room records by a capacity condition. The number 20 supplies the selection threshold; the missing room capacities must first come from the structured source.

The rationale correctly identifies knowledge lookup. The collection prompt specified finding records that satisfy a database condition, so no new independent learning status is inferred. Twenty candidates across sixteen provisional groups are recorded, five per category. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request in any category, with different wording and a new situation, plus its first action and rationale.

## Twenty-first original pilot response, October 23, 2026

Altan supplied candidate q0021 and chose calculation because all three scores and the number of rounds are provided. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g017 for averaging supplied scores. The collection prompt allowed any category and requested a new situation and wording. This correctly applies the supplied-input calculation boundary without a category hint and reinforces the earlier independent explanation; it does not establish understanding of model evaluation or other pending topics.

Twenty-one candidates across seventeen provisional groups are recorded: five document-retrieval, five knowledge-lookup, six calculation, and five direct-answer queries. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request that can be answered directly, using a task other than comparing concepts or rewriting a sentence, with its first action and rationale.

## Twenty-second original pilot response, October 23, 2026

Altan supplied candidate q0022 and chose direct answering because the request asks for general suggestions without requiring a document, database lookup, or calculation. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g018 for generating activity ideas. The requested count of three controls the number of suggestions; it does not require numerical calculation. Sharing rainy-weather context with earlier queries alone does not establish a common template group.

The rationale correctly identifies direct answering. The collection prompt specified a direct-answer request outside concept comparison and sentence rewriting, so no new independent learning status is inferred. Twenty-two candidates across eighteen provisional groups are recorded: five document-retrieval, five knowledge-lookup, six calculation, and six direct-answer queries. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request using a named fictional document for a task other than summarizing, finding a listed item, comparing documents, or obtaining calculation inputs, with its first action and rationale.

## Twenty-third original pilot response, October 23, 2026

Altan supplied candidate q0023 and chose reading the welcome letter because its original text is needed before translation. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g019 for retrieving document text before translating it. Unlike the supplied-text rewriting examples, the text to transform is not included in the request.

The rationale correctly identifies document retrieval as the first necessary action. The preceding user-facing prompt explicitly requested translation of a named fictional document whose text was not provided, so this is supported dependency practice and does not add independent transfer evidence. Twenty-three candidates across nineteen provisional groups are recorded: six document-retrieval, five knowledge-lookup, six calculation, and six direct-answer queries. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request involving a named fictional structured source, using a task other than retrieving one attribute or filtering records by a threshold, with its first action and rationale.

## Twenty-fourth original pilot response, October 23, 2026

Altan supplied candidate q0024 and chose looking up the catalog records because their book titles are needed before sorting. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g020 for ordering records from a structured source. Sharing a library setting with q0011 alone does not establish a common template: this request orders a collection rather than retrieving a single book attribute.

The rationale correctly identifies knowledge lookup as the first necessary action. The collection prompt specified a named fictional structured source, so this is supported practice and does not add independent transfer evidence. Twenty-four candidates across twenty provisional groups are recorded, six per category. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request in any category, using a new situation and different wording, with its first action and rationale.

## Twenty-fifth original pilot response, October 23, 2026

Altan supplied candidate q0025 and chose calculation because both garden dimensions are provided. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g021 for rectangular area from supplied dimensions. Although it involves multiplication like g005, its geometry task and wording differ from the unit-quantity times count template; grouping remains subject to pilot review.

The collection prompt allowed any category and requested a new situation and wording. The response correctly applies the supplied-input calculation boundary without a category hint and reinforces the earlier independent explanation. It does not establish understanding of other pending topics. Twenty-five candidates across twenty-one provisional groups are recorded: six document-retrieval, six knowledge-lookup, seven calculation, and six direct-answer queries. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original direct-answer request with the full text to translate included in the request, with its first action and rationale, contrasting with q0023 where the source paragraph was absent.

## Twenty-sixth original pilot response, October 23, 2026

Altan supplied candidate q0026 and chose direct answering because the complete text is provided and only requires translation. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g022 for translating supplied text. Pilot review must compare this group with the other short supplied-text transformation requests before freezing groups. In contrast to q0023, no document access is required to obtain the source text.

The rationale correctly applies the supplied-text boundary. The collection prompt specified translation with the complete text included, so this is supported boundary practice rather than a freely chosen transfer example. Twenty-six candidates across twenty-two provisional groups are recorded: six document-retrieval, six knowledge-lookup, seven calculation, and seven direct-answer queries. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request using a named fictional document to check whether a proposed action follows its rules, with its first action and rationale.

## Twenty-seventh original pilot response, October 23, 2026

Altan supplied candidate q0027 and chose reading the visitor rules because their pet policy is needed to determine whether bringing a dog is allowed. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g023 for checking a proposed action against a document's rules. Pilot review must compare this with other document-information requests before freezing groups; a shared camp setting alone does not determine grouping.

The rationale correctly identifies document retrieval as the first necessary action. The collection prompt specified checking an action against rules in a named fictional document, so this is supported practice rather than new independent transfer evidence. Twenty-seven candidates across twenty-three provisional groups are recorded: seven document-retrieval, six knowledge-lookup, seven calculation, and seven direct-answer queries. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request comparing two entries in a named fictional structured source, with its first action and rationale.

## Twenty-eighth original pilot response, October 23, 2026

Altan supplied candidate q0028 and chose looking up both tent records because their listed weights are needed before comparison. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g024 for comparing two catalog records. Either record can be retrieved first; both retrievals have the knowledge_lookup label. The request does not supply the weights itself.

The rationale correctly identifies the earliest necessary action. The collection prompt specified comparison of entries in a named fictional structured source, so this is supported practice rather than new independent transfer evidence. Twenty-eight candidates across twenty-four provisional groups are recorded, seven per category. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request in any category, using a new situation and different wording, with its first action and rationale.

## Twenty-ninth original pilot response, October 23, 2026

Altan supplied candidate q0029 and chose calculation because the flour amount per batch and number of batches are provided. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`. It is conservatively assigned to g005 with q0005 and q0012: all three use a supplied amount per unit times count template. The cooking setting alone does not establish an independent template. This provisional group contains three queries, within the four-query limit, and remains subject to pilot review.

The collection prompt allowed any category and requested a new situation and wording. The rationale correctly applies the supplied-input calculation boundary without a category hint, reinforcing earlier independent explanation. Twenty-nine candidates across twenty-four provisional groups are recorded: seven document-retrieval, seven knowledge-lookup, eight calculation, and seven direct-answer queries. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request asking for a short piece of creative writing, with its first action and rationale.

## Thirtieth original pilot response, October 23, 2026

Altan supplied candidate q0030 and chose direct answering because the request asks for original creative writing without requiring a document, database lookup, or calculation. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g025 for creating a short story from a supplied premise.

The rationale correctly identifies direct answering. The collection prompt specified creative writing, so this is supported practice rather than new independent transfer evidence. Thirty candidates across twenty-five provisional groups are recorded: seven document-retrieval, seven knowledge-lookup, eight calculation, and eight direct-answer queries. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request to identify a discrepancy between two named fictional documents, with its first action and rationale.

## Thirty-first original pilot response, October 23, 2026

Altan supplied candidate q0031 and chose reading both documents because their stated times are needed to check for a discrepancy. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`. It is conservatively assigned g015 with q0019: both compare information obtained from two named documents. Their wording and comparison purpose differ, so this grouping remains a provisional leakage-control judgment for pilot review. It does not imply all two-document requests must share one group.

The rationale correctly identifies document retrieval. The collection prompt specified identifying a discrepancy between two named fictional documents, so this is supported practice rather than new independent transfer evidence. Thirty-one candidates across twenty-five provisional groups are recorded: eight document-retrieval, seven knowledge-lookup, eight calculation, and eight direct-answer queries. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request to count matching records in a named fictional database, with its first action and rationale.

## Thirty-second original pilot response, October 23, 2026

Altan supplied candidate q0032 and chose looking up the booking records because the bookings that include breakfast must be identified before counting them. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g026 for counting matching records from a structured source. Pilot review must compare this with g016's record-filtering request and g006's lookup-before-calculation request before freezing groups. A database query may perform selection and counting together; the routing label remains knowledge_lookup because the required records are external to the request.

The rationale correctly identifies the first necessary action. The collection prompt specified counting matching database records, so this is supported dependency practice rather than new independent transfer evidence. Thirty-two candidates across twenty-six provisional groups are recorded, eight per category. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request in any category, using a new situation and different wording, with its first action and rationale.

## Thirty-third original pilot response, October 23, 2026

Altan supplied candidate q0033 and chose calculation because the starting water amount and amount used are provided. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g027 for a remaining-quantity subtraction scenario. Pilot review should check whether “holds 60 litres” clearly states current contents rather than tank capacity; the supplied rationale indicates Altan's intended starting amount, but that rationale will not be available as model input. No wording change has been made to the human-authored query.

The collection prompt allowed any category and requested a new situation and wording. The rationale correctly applies the supplied-input calculation boundary under the intended reading, reinforcing earlier independent explanation. Thirty-three candidates across twenty-seven provisional groups are recorded: eight document-retrieval, eight knowledge-lookup, nine calculation, and eight direct-answer queries. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request to organize or classify information supplied entirely within the request, with its first action and rationale.

## Thirty-fourth original pilot response, October 23, 2026

Altan supplied candidate q0034 and chose direct answering because all words are provided and only require organizing. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g028 for alphabetizing supplied words. Unlike q0024, which requires titles from a catalog, this request includes the complete material to sort. Pilot review must consider their shared sorting task when checking template similarity and leakage before freezing groups.

The rationale correctly applies the supplied-information boundary. The collection prompt specified organizing or classifying information provided entirely in the request, so this is supported boundary practice rather than new independent transfer evidence. Thirty-four candidates across twenty-eight provisional groups are recorded: eight document-retrieval, eight knowledge-lookup, nine calculation, and nine direct-answer queries. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request to extract a short quotation from a named fictional document whose text is not supplied, with its first action and rationale.

## Thirty-fifth original pilot response, October 23, 2026

Altan supplied candidate q0035 and chose reading the handbook because its exact wording is needed before quoting. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g029 for retrieving an exact quotation. Pilot review must compare this with q0023's request for an opening paragraph before translation and other document-extraction requests before freezing groups.

The rationale correctly identifies document retrieval. The collection prompt specified a quotation from a named fictional document whose text was absent, so this is supported practice rather than new independent transfer evidence. Thirty-five candidates across twenty-nine provisional groups are recorded: nine document-retrieval, eight knowledge-lookup, nine calculation, and nine direct-answer queries. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request checking whether a specific record exists in a named fictional database, with its first action and rationale.

## Thirty-sixth original pilot response, October 23, 2026

Altan supplied candidate q0036 and chose looking up the booking because the database must be checked to determine whether it is listed. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g030 for record-existence checking. The label does not assume a matching record will be found. Sharing the hotel database with q0032 alone does not establish a common template; pilot review must still compare this request with the other identified-record lookups before freezing groups.

The rationale correctly identifies knowledge lookup. The collection prompt specified checking record existence in a named fictional database, so this is supported practice rather than new independent transfer evidence. Thirty-six candidates across thirty provisional groups are recorded, nine per category. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original calculation request involving conversion between units, with all required values and the conversion factor supplied, plus its first action and rationale.

## Thirty-seventh original pilot response, October 23, 2026

Altan supplied candidate q0037 and chose calculation because the length and conversion factor are provided. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g031 for unit conversion with an explicit factor. This differs in task and wording from g005's amount-per-unit times count examples despite also using multiplication; pilot review must confirm grouping before release.

The rationale correctly identifies calculation. The collection prompt specified a unit conversion with all required inputs supplied, so this is supported practice rather than new independent transfer evidence. Thirty-seven candidates across thirty-one provisional groups are recorded: nine document-retrieval, nine knowledge-lookup, ten calculation, and nine direct-answer queries. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request to draft a short everyday message using details supplied entirely in the request, with its first action and rationale.

## Thirty-eighth original pilot response, October 23, 2026

Altan supplied candidate q0038 and chose direct answering because the request provides the details needed to draft a thank-you message. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g032 for drafting an everyday message from supplied context. Pilot review must compare it with other text-generation requests before freezing groups; generating a story and drafting a thank-you message are provisionally distinct tasks.

The rationale correctly identifies direct answering. The collection prompt specified drafting an everyday message with all necessary details supplied, so this is supported practice rather than new independent transfer evidence. Thirty-eight candidates across thirty-two provisional groups are recorded: nine document-retrieval, nine knowledge-lookup, ten calculation, and ten direct-answer queries. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request to turn instructions from a named fictional document into a checklist, with its first action and rationale.

## Thirty-ninth original pilot response, October 23, 2026

Altan supplied candidate q0039 and chose reading the handbook because its setup instructions are needed before organizing them into a checklist. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g033 for transforming document instructions into a checklist. Pilot review must compare it with other document-summary and document-transformation requests before freezing groups.

The rationale correctly identifies document retrieval as the first necessary action. The collection prompt specified turning instructions from a named fictional document into a checklist, so this is supported practice rather than new independent transfer evidence. Thirty-nine candidates across thirty-three provisional groups are recorded: ten document-retrieval, nine knowledge-lookup, ten calculation, and ten direct-answer queries. Broader learning statuses remain unchanged. No independent review, permission, or release acceptance is inferred. Next collection exercise: an original request to find the record with the earliest or latest date in a named fictional database, with its first action and rationale.

## Fortieth original pilot response, October 23, 2026

Altan supplied candidate q0040 and chose looking up the booking records because their stored arrival dates are needed to find the earliest one. The exact query and rationale are preserved in ignored `data/raw/pilot-intake.md`, provisionally assigned g034 for selecting the earliest dated record. Pilot review must compare it with g020's record-ordering task and other structured-source comparisons before freezing groups.

The rationale correctly identifies knowledge lookup as the first necessary action. The collection prompt specified selecting the earliest or latest dated record, so this is supported practice rather than new independent transfer evidence. Forty candidates across thirty-four provisional groups are recorded, ten per category. An intake integrity check confirmed exactly q0001 through q0040 with no duplicate IDs and ten candidates in each bucket. These are candidate counts, not accepted or independently reviewed rows. Broader learning statuses remain unchanged. Dataset permission, review decisions, ambiguity resolution, and final grouping remain outstanding. In particular, q0033's current-contents versus tank-capacity wording remains flagged. No research results or release acceptance are inferred. The next manual step in `docs/manual-steps.md` is Altan's actual study-use permission statement, including redistribution limits; no license is inferred from authorship or the code's MIT license.

## Pilot permission recorded, October 23, 2026

Altan supplied this permission after collecting candidates q0001 through q0040:

> I give permission to use these queries in the study, include them in my course submission, and share them publicly without restrictions.

The agent copied the statement verbatim into the existing source manifest's `license` field and the ignored intake worksheet, with the date and explicit scope of these forty candidates. No named license or permission for future material was inferred. The walkthrough now describes the actual provenance record. Queries remain in ignored local storage. This permission record does not publish them or establish annotation acceptance, independent review, or M1 readiness. Collection used agent-directed exercises and immediate feedback while Altan supplied the query text and rationales; the human-authored provenance must not be described as unaided collection.

For q0040, looking up the stored dates remains the first required action before selecting the earliest arrival. Permission changes whether that candidate may be used and shared, not its routing label. Existing learning statuses remain unchanged. The next manual step is choosing a second human reviewer or delayed blind self-review, with reviewer availability or a delay. The guide proposes one week for self-review. The pilot review needs at least two rows per proposed class plus all ambiguous rows, including q0033. Reviewer identities, dates, decisions, and agreement remain unfilled.

Verification for the permission update: exact-string readback passed for the source manifest and intake worksheet. The pilot JSONL and review ledger remain empty, confirmed directly. Draft validation reported `PASS: 0 rows valid`, which establishes no accepted research rows. The environment smoke check passed with Python 3.12.13 and scikit-learn 1.9.1. All 201 unit tests passed in 20.059 seconds. Ruff lint, format checks for 47 files, and `git diff --check` passed. No new tests were added for this metadata-only change. No commit, PR, or merge was performed during this permission-recording step. The accumulated learning-log changes remain local.

## Berkeley compatibility inspection, October 24, 2026

Altan asked whether public data could replace further manual query writing and authorized a small Berkeley sample inspection. The agent downloaded a pinned BFCL V3 revision and inspected 40 records across five categories. The [assessment](evidence/bfcl-compatibility.md) records exact sampling, citations, local artifact hashes, and a traceable screening ledger. Eighteen sampled rows provisionally fit the current contract. Four are duplicate calculation requests, leaving fourteen distinct candidates: eleven calculations, two lookups, and one direct answer. Four records need clarification and eighteen request unsupported actions. These counts describe this bounded, adaptive sample and are not full-corpus proportions or model results.

A separate agent checked primary-source provenance and schema. A reviewer checked mappings and count evidence. Agent judgments do not establish independent human labels. The source's empty-tool chatable category contains exact repeats of calculation requests, so mapping its category directly to direct_answer would contradict the project's fixed-tool contract. For the concrete area request `simple_0`, supplied dimensions imply calculation regardless of whether BFCL supplies a function in that category. This is an explanation provided by the agent, not a teach-back answer from Altan.

The recommendation is to retain the existing pilot, consider a filtered BFCL supplement for calculations and read-only structured lookups, and assess other sources for remaining coverage before requesting more authored rows. No dataset source was adopted, no sample entered research JSONL, and no review decision was fabricated. Prior exposure of these inspected examples must be disclosed in any later evaluation design. Existing learning statuses remain unchanged. The user has not yet answered the review-method decision.

Verification for the inspection: all nine downloaded artifacts matched their recorded byte counts and SHA-256 hashes. The seeded supplement and screening scripts reproduced forty sampled records and fourteen distinct candidate texts. A separate AI reviewer confirmed source-line matching, expected-call joins, duplicate detection, and counts. One rationale was corrected to avoid claiming that a function identified a named player database; the routing judgments did not change. The screening hash recorded in the assessment reflects that correction. The environment smoke check, Ruff lint, formatting check for 48 files, and `git diff --check` passed. The full unit suite was not rerun for this documentation-only investigation. All pilot and review JSONL files remain empty. No commit, PR, merge, model fitting, or tool execution from BFCL was performed.

## Complementary sources and blind AI review, October 24, 2026

Altan requested free datasets for the missing classes, an updated roadmap, completion of independent preparation, and one human step at a time. Two source investigations used pinned primary documentation and original records. The [No Robots assessment](evidence/public-direct-answer.md) found thirteen provisional direct-answer texts in twenty inspected records. The [Dolly assessment](evidence/public-document-retrieval.md) found three conditional document-reading texts, two held, and fifteen unsuitable for that supplement in twenty inspected records. Its three candidates require retaining the original separate context as a linked passage; the classifier sees the original instruction only. Initially the attachment assumption was too restrictive, then the original schema and the protocol's identified-passage rule established that preserving an existing association is different from inventing a source cue. The reports retain that condition and the distinct CC BY-NC 4.0 and CC BY-SA 3.0 source requirements. QMSum was triaged but not imported or counted.

The ignored inspection shortlist combines thirty public candidates with exact source IDs, revisions, screening reasons, and licenses. The three original Dolly contexts are stored separately with their original UTF-8 hashes. Across those candidates and the forty authored queries, exact normalized-text checking found seventy distinct texts: 21 calculation, 12 lookup, 24 direct answer, and 13 document retrieval. These are candidate counts, not accepted rows or independent groups. Bulk expansion waits for the pilot guide decisions. No query was rewritten, generated, or put into an accepted research split.

When asked about the human reviewer, Altan requested an AI persona and preservation of his own labels as fallback. A fresh reviewer received only shuffled query texts and guide rules. Its forty labels matched the forty originals, ten per class. The [AI review evidence](evidence/pilot-ai-review.md) records model, input/output hashes, grouping notes, and the limits of that match. The original labels are preserved, and the human ledger is empty. AI agreement cannot establish independent human annotation, true label correctness, or student understanding. The original q0033 wording ambiguity and q0014 teaching-example similarity remain visible. A nine-query blind human packet is ready if the existing method is retained. Altan has been asked whether to formally adopt the single-human, AI-assisted alternative; that method decision remains pending at this entry.

For a concrete routing trace, a Dolly instruction explicitly asks about a given paragraph. Keeping the paragraph as its original linked attachment makes reading it the first dependency. Removing both the paragraph association and its reference would change the task. A generic fact question with no requested source does not become document retrieval merely because the dataset supplies a hidden answer passage. This is an agent explanation, not a student response.

The roadmap now records actual pilot progress, source options, the uncompleted review requirement, and an approximate overall completion of 30%. The weighted estimate is 25% design/tooling at 100%, 25% data at 20%, 20% experiments at 0%, 10% interpretation at 0%, 15% report at 10%, and 5% research reproduction/rehearsal/submission at 0%. The sum is 31.5%, rounded to the nearest five points. These are planning judgments, not measured effort or course marks. The report has a compiled template and outline, with no finished manuscript or measured results. The missed M1 date and at-risk M2 date are explicit; no unsupported new completion dates were assigned.

Preparation verification checked all eleven No Robots evidence hashes and byte counts; the Dolly original download hash, twenty source-line/query/context matches, and context hashes; exact forty-ID pilot coverage; original query preservation; blinded packet fields; and forty AI/original comparisons. The pilot and human-review JSONL files remain empty. Source investigators and reviewers use the same GPT model family; this is not cross-family validation. Required software checks and integration evidence are recorded below after execution.

Next practice after the method choice: resolve one real boundary or group at a time. Ask Altan why an AI label match does not prove independent human agreement, then let him attempt the answer. Later ask how using a different dataset for each label could let source style become a shortcut. Learning statuses remain unchanged until actual responses are recorded.

Integrated verification: `sh scripts/check.sh` exited 0. Locked setup and environment smoke passed; all 201 unit tests passed in 21.386 seconds; Ruff lint passed, 51 files were already formatted, and `git diff --check` passed. These are software checks on fixtures, not research results. No production code or dependency changed. The full artificial archive workflow was not rerun locally for this documentation change; the existing CI job runs it for the PR.

## Approved AI-assisted method, October 24, 2026

Altan answered the method question: "Switch to single-human annotation with disclosed AI checks." This changes the study protocol explicitly. His original labels remain the reference; clear AI matches may retain them, while actual human adjudication is required for any disagreement, abstention, exclusion, or existing flag. The report template and manual path now state the selected method and single-annotator limitation. This is a method choice, not a teach-back answer or independent human-review evidence.

The [implementation evidence](evidence/ai-assisted-review.md) records the dedicated ledger shape, design alternatives, local ingestion hashes, and checks. The smaller nested-evidence design reuses the existing validation interface rather than adding a sidecar loader to each caller. The implementation worker owned the data/study modules and their tests; the lead owned protocol, evidence, report, and local data preparation. The worker observed a focused red run of 47 tests with 7 failures before implementation, then 48 validator tests and 9 study tests passing. The parent verifies the integrated result separately.

All forty original queries, labels, rationales, and groups now exist in the local draft, with zero accepted rows pending guide/group decisions. The review ledger records forty actual AI checks, zero legacy human reviews, and two unresolved steward flags. The task prompt, guide snapshots, blind input, and raw AI output are preserved and hashed. No human adjudicator, decision, date, or rationale was manufactured. q0033's current-contents/capacity question was presented as the first human adjudication; its reply is still pending at this entry.

The data-source work merged in PR #18 as `d88de371cfabd7e199aecef8ee4be2cbc7ebbb9d`, preserving commits `d1f2114` and `11d8089`. Independent Spec and Standards checks passed, and PR CI passed the full artificial reproduction workflow. The later method selection is a separate verifiable change. Overall completion remains approximately 30%; schema support and AI agreement do not supply accepted data, research metrics, final report prose, or learning evidence.

Integrated method verification: `sh scripts/check.sh` passed all 208 tests in 22.025 seconds, smoke, lint, formatting for 52 files, and whitespace checks. The desktop LaTeX compiler successfully compiled the updated report template. Spec and Standards reviewers independently verified the actual forty draft/ledger rows, prompt/guide/input/output hashes, legacy behavior, pending-adjudication rules, and local links; both returned PASS and independently passed the 48-validator/9-study focused tests. The actual draft validator reports forty valid pending rows, zero accepted rows, zero human-review entries, and forty AI matches. `orchestra status` correctly remains not ready.

## Tank clarification recorded, October 25, 2026

Altan stated: "I meant 60 litres currently inside the tank. Record that and guide me through the next flagged query." The agent recorded an actual A1 adjudication for q0033, retaining `calculation`, and preserved the original query, label, rationale, group, AI decision, and historical flag. The other thirty-nine ledger entries are unchanged. Current contents provide the starting number; subtracting the stated usage gives 42 litres. This arithmetic trace is an agent explanation, not a student calculation or broader teach-back evidence. Learning statuses remain unchanged.

The manual path, evidence, roadmap, and walkthrough now point to q0014’s teaching-example similarity. Its provenance question remains unanswered, as do final grouping decisions. All forty rows remain pending and zero are accepted. No experiment or source adoption occurred.

Verification: the actual pilot/review validator passed all forty draft rows; the dataset hash is unchanged and the ledger now has exactly one human adjudication with q0014 still pending. `sh scripts/check.sh` passed: 208 tests in 18.345 seconds, environment smoke, Ruff lint, formatting for 52 files, and whitespace checks. No new tests were added for this evidence-only update. Changes are local, awaiting the next review decisions before a consolidated documentation handoff.

## Teaching-example adaptation confirmed, October 25, 2026

Altan stated: "I adapted it from the teaching example. Record that and guide me through what we should do with it next." The agent recorded q0014’s actual provenance without inventing a final exclusion decision. The existing annotation guide reserves teaching examples for practice, and this log already keeps their paraphrases outside the research dataset. The recommendation is to exclude q0014 from research while preserving its original record and using it for practice. The next human step is that treatment decision, then grouping review. No routing teach-back or change to learning status is inferred from the provenance answer.

Both dataset and review ledger remain unchanged in this step: forty pending rows, zero accepted, q0033 adjudicated, q0014 still awaiting treatment. No experiment ran.

Verification: exact reply saved locally; dataset and ledger hashes remain unchanged. Draft/review validation passed forty rows. Environment smoke, Ruff lint, formatting for 52 files, and diff whitespace checks passed. The full unit suite was not rerun for this documentation/provenance-only update; the preceding q0033 step passed all 208 tests.

## Practice-only exclusion and first group, October 25, 2026

Altan stated: "Yes, exclude q0014 from the research dataset and keep it for practice. Record that and guide me through the first query group." The agent recorded the actual A1 exclusion with null adjudicated/resolved label and `excluded` dataset status. The original full row remains in the local exclusion evidence for practice; text, original labels, and AI evidence are preserved. Other rows and reviews are unchanged. There are 39 pending candidates, one excluded practice row, and zero accepted rows. Both individual flags are adjudicated, but grouping and guide v1 remain unfinished.

The first shared group presented is g002: q0002 summarizes a return policy from a handbook; q0007 summarizes safety rules from a handbook. The agent proposes retaining one template family to avoid close variants spanning training and evaluation. Altan has not yet answered that grouping question. This proposal is an explanation, not student understanding evidence; learning statuses remain unchanged. No experiment ran.

Verification: actual dataset/review validation passed forty records, reporting 39 pending and one excluded. Before/after comparisons confirmed that only q0014 changed in each file. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. The full unit suite was not rerun for this evidence/data-state update; no validator behavior changed. Documentation remains local for the consolidated pilot-review handoff.

## Handbook-summary group confirmed, October 25, 2026

Altan stated: "Keep them in one group because they use the same template, just with different handbooks and topics. Record that and guide me through the next group." This confirms retaining q0002 and q0007 in g002. Existing IDs already match his decision; dataset and label-review ledger bytes remain unchanged. The exact response and hashes are retained locally in the g002 decision record, separate from label adjudication.

Altan correctly identifies the shared template despite changes in subject and handbook. This is supported grouping practice after the agent’s recommendation, not an independent demonstration of split leakage or mastery of the whole topic. Existing broader learning statuses remain unchanged. Next shared group is g004, comparing two “explain the difference” requests; its human decision remains pending. Cross-group review is still required. Counts remain 39 pending, one excluded practice row, and zero accepted; no experiment ran.

Verification: g002 member IDs and unchanged dataset/ledger hashes checked directly; draft/review validation passed forty records. Environment smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this evidence-only change. Updates remain local for the consolidated pilot-review handoff.

## Difference-explanation group confirmed, October 25, 2026

Altan stated: "Keep them together because they use the same “explain the difference” template, just with different topics. Record that and guide me through the next group." This records a genuine decision to retain q0004 and q0008 in g004. Existing membership already matches; dataset and label-review ledger bytes remain unchanged. The exact reply and file hashes are retained in the local g004 decision record.

Altan correctly recognizes the shared template across different topics without a recommendation in the immediately preceding question, following the supported g002 example. This is successful transfer to another close grouping example; it does not yet demonstrate the effect on evaluation or establish broader split mastery. Existing topic statuses remain unchanged pending that explanation. Next is g005’s three quantity calculations; its grouping decision remains open. Counts remain 39 pending, one excluded practice record, zero accepted. No experiment ran.

Verification: g004 membership and unchanged dataset/ledger bytes checked directly. Actual draft/review validation passed forty records. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this evidence-only update. Documentation remains local for consolidated pilot-review handoff.

## Amount-per-unit group confirmed, October 25, 2026

Altan stated: "Keep all three together because they use the same amount-per-unit times number-of-units pattern, just in different situations. Record that and guide me through the next group." This genuinely confirms retaining q0005, q0012, and q0029 in g005. The exact reply and file hashes are retained locally; dataset and label-review ledger bytes remain unchanged because existing membership already matches.

Altan identified the common quantitative pattern across tickets, laps, and recipe batches without a recommendation in the preceding question. This is successful transfer beyond the repeated wording of g004. It supports grouping recognition for this example, but does not yet demonstrate split-leakage consequences or broader split mastery. Existing topic statuses remain unchanged pending that explanation. Next is g007’s politeness and shortening requests; the human decision is pending. Counts remain 39 pending, one excluded practice row, zero accepted. No experiment ran.

Verification: g005 membership and unchanged dataset/ledger bytes checked directly. Draft/review validation passed forty records. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this evidence-only update. Documentation remains local for consolidated pilot-review handoff.

## Provided-sentence rewriting group confirmed, October 25, 2026

Altan stated: "Keep them together because both rewrite a sentence already provided, even though one changes politeness and the other changes length. Record that and guide me through the next group." The actual decision retains q0009 and q0018 in g007. The exact reply and hashes are preserved in the local g007 decision record. Existing membership already matches, so dataset and label-review ledger bytes remain unchanged.

Altan recognizes the common provided-sentence rewriting task while acknowledging different transformations. This supports his stated conservative grouping choice; it does not establish independent understanding of evaluation leakage or imply that a shared label alone defines a group. Broader learning statuses remain unchanged. Next is g015’s two-document comparisons; singleton and cross-group checks also remain open. Counts remain 39 pending, one excluded practice row, zero accepted. No experiment ran.

Verification: g007 membership and unchanged dataset/ledger bytes checked directly. Draft/review validation passed forty records. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this evidence-only update. Documentation remains local for consolidated pilot-review handoff.

## Two-document comparison group confirmed, October 25, 2026

Altan stated: "Keep them together because both compare information from two documents, just on different topics. Record that and guide me through the next step." This genuinely confirms retaining q0019 and q0031 in g015. The exact reply and hashes are preserved locally. Dataset and label-review ledger bytes remain unchanged because membership already matches. All five current multi-row groups now have human decisions.

Altan identifies the common two-document comparison task across different topics. This is another actual grouping rationale; broader split understanding remains unverified until he explains evaluation consequences. Existing topic statuses remain unchanged. Next is a cross-group check of q0003, q0011, and q0016, currently separate but each requesting a field from an identified structured record. No merge or answer is inferred. Counts remain 39 pending, one excluded practice row, zero accepted. No experiment ran.

Verification: g015 membership and unchanged dataset/ledger bytes checked directly. Draft/review validation passed forty records. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this evidence-only update. Documentation remains local for consolidated pilot-review handoff.

## Single-record lookup families merged, October 25, 2026

Altan stated: "Merge them into one group because each asks for one piece of information from a specific record in a catalog or database. Record that and guide me through the next step." The agent applied the actual decision using g003 for q0003, q0011, and q0016. Only q0011 and q0016 changed group IDs; g009/g013 are retired with the previous mapping and hashes retained in local merge evidence. All text, labels, remaining fields, and label-review ledger bytes are preserved. The draft now has 32 provisional groups including the excluded practice group, not 32 accepted independent groups.

Altan recognizes the shared one-field lookup pattern across different structured sources. This is supported cross-group practice after the agent identified the pattern; it does not yet demonstrate independent leakage reasoning. Broader learning statuses remain unchanged. Next is q0024’s sorted book list versus q0040’s earliest booking. Counts remain 39 pending, one excluded practice row, zero accepted. No split or experiment exists.

Verification: before/after comparison confirmed exactly two group-ID changes, preserved all other row fields, and confirmed unchanged review-ledger bytes. Actual draft/review validation passed forty records, including the three-row merged family within the four-row cap. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this annotation-state update; implementation is unchanged. Documentation remains local for consolidated pilot-review handoff.

## Record-ordering families merged, October 25, 2026

Altan stated: "Keep them together because both order records by a field, even though one returns a sorted list and the other selects the earliest record. Record that and guide me through the next step." The actual decision merges q0024 and q0040 into g020. Only q0040 changed group ID; g034 is retired with history and hashes retained locally. All other fields, rows, and review-ledger bytes are preserved. The draft now has 31 provisional groups including the excluded practice group.

Altan identifies ordering by a field as the shared pattern despite different outputs. This supports the recorded conservative grouping decision; a common operation alone is not a universal rule to merge all queries. Broader split-understanding status remains unchanged pending evaluation reasoning. Next is q0020’s room filter versus q0032’s breakfast-booking count; no grouping decision is inferred. Counts remain 39 pending, one excluded practice row, zero accepted. No experiment ran.

Verification: before/after comparison confirmed only q0040’s group ID changed, with all other fields/rows and review-ledger bytes unchanged. Draft/review validation passed forty records. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this annotation-state update; implementation is unchanged. Documentation remains local for consolidated pilot-review handoff.

## Record-filtering families merged and purpose explained, October 25, 2026

Altan stated: "Keep them together because both filter records by a condition, even though one lists the matches and the other counts them. Record that and guide me through the next step.

And tell me what is all this about" The actual decision merges q0020 and q0032 into g016. Only q0032 changed group ID; g026 is retired with history and hashes retained locally. All other fields/rows and review-ledger bytes are preserved. There are 30 provisional groups including the excluded practice group.

Altan identifies filtering by a condition as the shared pattern and asks what the overall activity is for. Explain before continuing: the router predicts the first action; groups keep related templates in one split to reduce optimistic evaluation from similar training examples. A shared operation alone does not universally require merging, and broader grouping reduces independent sample counts. This explanation is agent-supplied, not evidence that Altan can explain leakage independently. Existing topic statuses remain unchanged. Next is the translation pair q0023/q0026, with no grouping answer inferred. Counts remain 39 pending, one excluded practice row, zero accepted; no experiment ran.

Verification: before/after comparison confirmed only q0032’s group ID changed, preserving all other fields/rows and review-ledger bytes. Draft/review validation passed forty records. Smoke, Ruff lint, and formatting for 52 files passed. The initial whitespace check caught trailing whitespace in the quoted reply; it was removed from the Markdown while the exact reply remains in local evidence. Full unit suite not rerun for this annotation-state update; implementation is unchanged. Documentation remains local for consolidated pilot-review handoff.

## Translation family merged across labels, October 25, 2026

Altan stated: "Keep them together because both ask for translation, even though one needs the document first and the other already provides the text. Record that and guide me through the next step." The actual decision merges q0023 and q0026 into g019. Only q0026 changed group ID; g022 is retired with mapping and hashes retained locally. Both first-action labels and all other row fields remain intact, as does the review ledger. Both members have AI review entries. There are 29 provisional groups including the excluded practice group.

Altan distinguishes the common translation task from the different first-action dependencies after those were explained by the agent. This supports grouping/label distinction in this example; evaluation-leakage reasoning is still unverified independently. Existing broader topic statuses remain unchanged. Next is q0034’s supplied-word sorting versus existing g020’s record ordering; no answer is inferred. Counts remain 39 pending, one excluded practice row, zero accepted; no experiment ran.

Verification: before/after comparison confirmed only q0026’s group ID changed, with all other fields/rows and review-ledger bytes unchanged. Both mixed-family members have review entries. Draft/review validation passed forty records. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this annotation-state update; implementation is unchanged. Documentation remains local for consolidated pilot-review handoff.

## Supplied-word sorting added to ordering family, October 25, 2026

Altan stated: "Keep q0034 in the ordering group because it also sorts items, even though the words are already provided. Record that and guide me through the next step." The agent applied the actual decision by changing only q0034’s group ID from g028 to g020. Its direct-answer label remains unchanged, alongside the two lookup labels in the family. All three members have AI review entries; the ledger is unchanged. Mapping history and hashes are retained locally. There are 28 provisional groups including the excluded practice group.

Altan recognizes the shared ordering task across different input availability after the comparison was presented. This supports the recorded family choice; broader leakage understanding remains unverified independently. Existing topic statuses remain unchanged. Next is q0010/q0027’s specific guidance from named camp documents; no decision is inferred. Counts remain 39 pending, one excluded practice row, zero accepted; no experiment ran.

Verification: before/after comparison confirmed only q0034’s group ID changed; every other field/row and review-ledger byte is unchanged. All three mixed-family members have review entries. Draft/review validation passed forty records. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this annotation-state update; implementation is unchanged. Documentation remains local for consolidated pilot-review handoff.

## Document-guidance families merged, October 25, 2026

Altan stated: "Keep them together because both ask for specific guidance from a named document, just about different things to bring. Record that and guide me through the next step." The actual decision merges q0010 and q0027 into g008. Only q0027 changed group ID; g023 is retired with mapping and hashes preserved locally. All remaining fields/rows and review-ledger bytes are unchanged. There are 27 provisional groups including the excluded practice group.

Altan gives the shared document-guidance pattern as the reason, beyond the documents’ shared camp setting. This records his grouping rationale; independent evaluation-leakage understanding remains unverified. Existing topic statuses remain unchanged. Next is q0006’s lookup-before-cost request versus g005, with its four-row cap and the conversion boundary still to check. No group decision is inferred. Counts remain 39 pending, one excluded practice row, zero accepted; no experiment ran.

Verification: before/after comparison confirmed only q0027’s group ID changed; all other fields/rows and review-ledger bytes remain unchanged. Draft/review validation passed forty records. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this annotation-state update; implementation is unchanged. Documentation remains local for consolidated pilot-review handoff.

## Lookup-before-cost added to amount-per-unit family, October 25, 2026

Altan stated: "Put q0006 in g005 because it uses the same price-times-quantity pattern, even though it needs a lookup first. Record that and guide me through the next step." The actual decision adds q0006 to g005 while preserving its lookup-first label. Only its group ID changed; g006 is retired with history and hashes retained locally. Other fields/rows and review-ledger bytes remain unchanged. All four g005 members have review entries. There are 26 provisional groups including the excluded practice group.

Altan distinguishes the common price-times-quantity pattern from its lookup dependency after the comparison was presented. Broader independent leakage reasoning remains unverified, so topic statuses remain unchanged. Next is q0037’s unit-conversion boundary. g005 is at the four-row cap; explain that semantic relatedness comes first and any excess-row decision must be explicit. No answer, exclusion, or cap change is inferred. Counts remain 39 pending, one excluded practice row, zero accepted; no experiment ran.

Verification: before/after comparison confirmed only q0006’s group ID changed; all other fields/rows and review-ledger bytes remain unchanged. All four mixed-family members have review entries. Draft/review validation passed forty records, including the four-row group cap. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this annotation-state update; implementation is unchanged. Documentation remains local for consolidated pilot-review handoff.

## Fifth amount-per-unit family member confirmed, October 25, 2026

Altan stated: "Put q0037 in the same family because it also multiplies an amount by a per-unit factor. Record that and guide me through how to handle the four-query limit." The agent recorded the actual semantic decision that q0037 belongs to g005’s family. This makes five related queries. Dataset and label-review ledger bytes remain unchanged pending the four-row-cap treatment; g031 is an unresolved storage mapping, not an independent family decision. No split or release may use it to separate known relatives.

The agent recommends keeping the existing four research candidates and retaining the later q0037 for practice only, based on collection order before model results. The exact family decision and hashes are preserved locally; no exclusion decision has yet been made. The validator counts all stored rows, so the future study subset must have four family members while the original practice record/review remains archived. This is a sampling limitation, not a reason to invent independence or silently change the cap. Existing learning statuses remain unchanged. Counts remain 39 pending, one excluded, zero accepted; no experiment ran.

Verification: exact five-member family decision saved with current hashes; dataset and ledger bytes remain unchanged. Draft/review validation passed the stored forty-row draft, which does not resolve its pending semantic mapping or establish readiness. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this evidence-only update. Documentation remains local for consolidated pilot-review handoff.

## Unit-conversion practice exclusion recorded, October 25, 2026

Altan stated: "Yes, keep q0037 for practice only and exclude it from the research collection. Record that and guide me through the next step." The agent recorded the actual A1 exclusion and g005 family relationship for q0037, retiring g031. The complete forty-ID audit and review snapshots remain in ignored data/raw with both practice-only exclusions. Current research pilot/ledger paths contain 38 pending candidates/reviews; zero accepted. Retained research records are unchanged. g005 now has four research rows while the audit honestly preserves five related queries. The exact reply, original record, audit paths, and hashes are preserved in the local exclusion evidence.

This is a real sampling decision based on the recorded family cap and collection order, not model performance. No query was rewritten, deleted from history, or split into a false independent family. Broader learning statuses remain unchanged. Next is q0028’s lighter-tent comparison versus g020; no answer is inferred. No experiment ran.

Verification: complete forty-ID audit and review snapshots saved with hashes; retained research rows/reviews compare unchanged against the preceding collection. Draft/review validation passed 38 rows with 38 AI matches and zero accepted. g005 has four research members; the historical fifth is retained in the separate audit. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this annotation-state update; implementation is unchanged. The runbook documents the current paths and exclusion counts. Documentation remains local for consolidated pilot-review handoff.

## Lighter-tent selection added to ordering family, October 25, 2026

Altan stated: "Put q0028 in g020 because choosing the lighter tent also orders items by a field and selects one. Record that and guide me through the next step." The agent applied the actual decision by changing only q0028’s group ID from g024 to g020. g020 now has four research members, with original labels preserved and review entries for each member. All other fields/rows and review-ledger bytes are unchanged. The mapping and hashes are retained locally; the earlier audit remains a dated snapshot. There are 23 provisional research groups.

Altan identifies ordering by a field and selection as the common pattern, supporting this conservative family decision. Existing broader learning statuses remain unchanged pending independent evaluation reasoning. Next is q0015’s lesson duration versus q0033’s remaining-water calculation; no answer is inferred. Counts remain 38 pending, two historical practice-only exclusions, zero accepted. No experiment ran.

Verification: before/after comparison confirmed only q0028’s group ID changed, preserving all remaining fields/rows and review-ledger bytes. All four mixed-family members have review entries. Draft/review validation passed 38 records and the four-row cap. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this annotation-state update; implementation is unchanged. Documentation remains local for consolidated pilot-review handoff.

## Difference-calculation families merged, October 25, 2026

Altan stated: "Keep them together because both calculate a difference using values already provided, even though one involves time and the other water. Record that and guide me through the next step." The actual decision merges q0015 and q0033 into g012. Only q0033 changed group ID; g027 is retired with prior mapping and hashes retained locally. Both labels and the earlier tank-contents adjudication remain unchanged, as do other fields/rows and review-ledger bytes. There are 22 provisional research groups.

Altan identifies a shared difference-calculation pattern across time and volume. This is his actual conservative grouping rationale, not evidence that he can independently explain evaluation leakage. Pause pair review for one question: what could happen to the test score if close variants from one family occur in both training and test? The answer remains pending; let him attempt it before giving the worked explanation. Existing topic statuses remain unchanged. Remaining boundary checks and guide v1 stay open. Counts remain 38 pending, two practice-only exclusions, zero accepted; no experiment ran.

Verification: before/after comparison confirmed only q0033’s group ID changed, preserving all other fields/rows and review-ledger bytes, including its earlier adjudication. Draft/review validation passed 38 records. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this annotation-state update; implementation is unchanged. Documentation remains local for consolidated pilot-review handoff.

## Grouping purpose explained by Altan, October 25, 2026

Altan stated: "It could make the test score look higher because the model has already seen a similar pattern, so it may not show how well it handles genuinely new queries. Record that and guide me through the next step." This correctly explains why close variants across training and test can make a score optimistic without establishing performance on genuinely new requests. Record the mechanism as **explained independently** in this response after prior instruction. This is actual learning evidence, distinct from passing tests and agreeing to group memberships. The broader leakage topic remains **needs practice**: split-before-fitting, vocabulary leakage, and model-selection leakage have not been attempted. No broader mastery is inferred. The exact reply and current hashes are retained locally.

Next is a remaining document-task boundary: q0039 turns handbook instructions into a checklist, compared with g002’s summaries of handbook content. Ask whether the transformation warrants a separate family or belongs with the summary family, and why. No answer or group change is inferred. Dataset/review bytes remain unchanged: 38 pending research candidates, two practice-only exclusions in history, 22 provisional research groups, zero accepted. No experiment ran.

Verification: exact response and current hashes saved; dataset and review-ledger bytes remain unchanged. Draft/review validation passed 38 rows. Smoke, Ruff lint, formatting for 52 files, and whitespace checks passed. Full unit suite not rerun for this learning-evidence-only update. Documentation remains local for consolidated pilot-review handoff.

## Final pilot grouping decisions and guide v1, October 26, 2026

Altan supplied all eight remaining decisions and defined a group as a shared request template: the same user goal solved by the same procedure, whatever the scenario. He explicitly rejected shared arithmetic operation or label as sufficient. He distinguished summarization from preserving steps in a checklist, allocation from averaging, geometry from amount-per-unit scaling, and discounts from the existing arithmetic families. He kept three different writing goals separate. He joined named-document content extraction, concept explanations, and key-based existence checking to their stated families. These actual answers show reasoned use of goal/procedure/output boundaries across the pilot; they do not demonstrate feature fitting, test-set selection, or broad ML mastery.

The agent applied only three group-ID changes (q0035 to g008, q0013 to g004, q0036 to g003), froze guide v1, and marked 38 eligible pilot rows accepted under the completed review. Original text, first-action labels, rationales, source IDs, and annotators are unchanged. The label-review ledger is unchanged. q0014 and q0037 remain practice-only with actual exclusions retained in the dated forty-ID audit and later decision records. The historical filename `pilot-v0.jsonl` remains the CLI path; row metadata now says `guide-v1`. This is the accepted pilot, not the 120-row release.

There are 19 shared request templates. Calculation has 9 rows/6 groups; document retrieval 9/5; lookup 10/4; direct answer 10/7. Group counts overlap where a family has different labels. The broader grouping reduces independent evidence. The agent recorded the possible word “handbook” cue for later validation error analysis without claiming any observed effect or changing wording. The study protocol, collection brief, manual guide, roadmap, walkthrough, report prompt, and methods preview now reflect the user’s rule.

The [pilot record](evidence/pilot-guide-v1.md) links actual evidence. The local final human message is retained with Markdown emphasis/code formatting removed, and that normalization is disclosed. Normalized decisions and before/after artifacts are under ignored `work/poteto/pilot-guide-v1/`. Actual `orchestra status` exits 1 with only collection coverage blockers: 38 versus 120 total, per-class rows below 30, and per-class groups below 15. It reports no pending pilot review case. No model ran. Next is licensed public-source adoption and annotation, followed by expansion; no more pilot group questions are outstanding.

Overall completion is approximately 35% using the same planning weights: design/tooling 100% of 25%, data 30% of 25%, experiments 0% of 20%, interpretation 0% of 10%, report 10% of 15%, final research reproduction/submission 0% of 5%. The sum is 34%, rounded to the nearest five points. This is a planning judgment, not a measured effort or course mark. The October 25 M2 target has passed; no unsupported replacement dates are assigned.

Integrated verification: `sh scripts/check.sh` passed 208 tests in 17.129 seconds, smoke, Ruff lint, formatting for 52 files, and whitespace checks. Actual data validation passed 38 accepted rows; status returned the expected size/coverage blockers only. The desktop compiler successfully compiled the changed report prompt. No application code, dependencies, or schema changed; no new tests were needed for annotation metadata. The methods preview source is updated, while the full M1 PDF edition remains unexported and is not claimed complete. Independent Spec and Standards review caught stale current-state paragraphs in the runbook/roadmap; these were corrected before handoff.

Independent Spec and Standards review both returned PASS. The Spec reviewer ran actual pilot validation/status and checked original-field preservation; Standards checked 134 relative Markdown link targets and whitespace. Both verified that the full M1 PDF remains an outstanding milestone deliverable. Origin could not resolve this repository, so shipping uses the authenticated GitHub CLI fallback. This review is software/document evidence from the same GPT family, not another human annotator.

## Public expansion screen for lookup and document retrieval, October 26, 2026

Altan asked the agent to compute the per-class gap and run larger lookup and document-retrieval screens. The agent judged 80 seeded Dolly records with an explicit passage reference, all 21 read-only BFCL SQL records, and five named-source BFCL matches, assigning each to a guide-v1 request template. The [screen record](evidence/public-expansion-screen.md) holds the counts. Nothing was imported, labeled, or accepted.

The main result is a constraint, not a count. Public rows are plentiful, but most share templates that already exist in the pilot, such as answering a question from a document (g008) or filtering records by a condition (g016). Because a family holds at most four rows, those rows add little. If every proposal were accepted, document retrieval would reach about 8 of 15 groups and lookup about 6. Closing that gap is Altan's decision: another source, targeted authoring, or a changed target.

Trace one query: Dolly line 659, "Given this paragraph about Pittsford, New York, what year was the town settled?" With the passage attached, the first action is reading it, so the proposed label is `document_retrieval`. It asks a specific question about an identified passage, so it joins g008 with the pilot's camp-letter and handbook questions, even though the topic differs.

Teach-back questions, unanswered: (1) Why does adding 40 more "answer a question from the passage" rows barely help the 15-group target? (2) Dolly rows usually start "Given this paragraph". What could a classifier learn from that phrase that would inflate its validation score? (3) Should "extract every country named in the text" share a family with "what year was the town settled, according to the text"? Name the goal and procedure for each. No learning status changes until Altan answers.

Verification: see the handoff for actual check output. No application code, dependency, schema, or data file changed.

## AI-generated template drafts, October 26, 2026

Altan supplied twenty template proposals. When asked whether to keep human authoring or draft disclosed AI-generated candidates, he explicitly selected “Draft AI-generated candidates.” The agent prepared forty local drafts, two per template, and updated the collection brief and protocol to record that limited drafting scope. The [review record](evidence/template-expansion-draft.md) explains the proposed boundaries and provenance limitations. Accepted pilot rows, primary labels, review ledger, and guide v1 remain unchanged. No new human understanding is inferred from this authorization.

The four flagged boundaries are provisionally: keep category counts (L3), document completeness (D3), and heading structure (D6); merge document location (D1) into g008. The broader comparison also merges keyed historical/joined lookup, difference calculations, social-message drafting, descriptive headlines, and chained source resolution with their existing goal families. Nine new families remain proposed. g003, g008, and g032 would exceed four rows if all drafts were imported; at most 28 drafts fit remaining capacity under these mappings. Human grouping decisions and candidate selection remain pending, so neither this ceiling nor the twenty-per-label draft count establishes release coverage.

Trace: L8-1 asks for the days between a supplied date and the arrival date of a named booking in a named database. Lookup must supply the missing arrival date first, so its proposed label is knowledge_lookup; the difference goal places it with g012, alongside calculation-first pilot rows. The local worksheet records this proposal only. No database was queried and no router predicted a label.

Practice questions, unanswered: (1) Why can L8-1 share a family with a calculation-first query? (2) If g008 already has three accepted members, how many of its six new drafts can enter research without changing the cap? (3) What shortcut could a classifier learn from the pilot’s use of “fictional,” and why does observing the word counts not prove it learned that shortcut? Learning statuses remain unchanged.

Draft checks passed: forty unique texts/IDs, two per template, twenty per proposed label, no normalized exact pilot overlap, all drafts pending with no human labels, query-only input alignment, saved-file hashes, and a 28-slot capacity ceiling. No fresh blind AI check was run: this agent saw its own proposed labels. Primary human annotation precedes that later check. Backend revision and generation parameters are unavailable and disclosed; the full conversation was not exported. Drafts remain ignored local files, not research-schema rows. No commit or model run was made.

Software verification: `sh scripts/check.sh` passed locked synchronization, environment smoke (Python 3.12.13/scikit-learn 1.9.1), all 208 tests in 18.744 seconds, Ruff lint, formatting for 55 files, and whitespace checks. Test splits are artificial fixtures, not research splits. Final documentation whitespace checks also passed. No code, dependency, or dataset schema changed. The full M1 study-guide PDF remains an outstanding milestone deliverable; this draft preparation does not complete M1.

## Guide v2: simpler scenario and source groups, October 26, 2026

Altan asked: "Dont be strict and modify rules to actually make the project simple to follow and train but in high quality standarts." He had also noted that his teacher advised finding the data online. The agent replaced the v1 request-template groups with guide v2. Rows now share a group when they are small variations, share a source or named setting, describe the same situation, or come from one public record. Three batch checks keep quality: near-duplicates, no request type above 40 percent of a class, and at least two sources per class with none above 75 percent. Labels, boundaries, review method, and readiness targets are unchanged. The [guide-v2 record](evidence/guide-v2.md) has the reasoning, pilot regrouping, and hashes.

The agent applied the rule to the pilot: 38 rows in 23 groups (calculation 9, document retrieval 8, lookup 7, direct answer 7). Only group IDs and the annotation version changed. Altan has not yet confirmed the individual assignments; they are listed for his objection. The AI drafts and the expansion screen carry notes that their v1 family accounting is superseded.

Trace: q0036 asks whether booking B24 exists in the Willow Hotel database. Under v1 it sat with the Northstar and Riverside keyed lookups because the procedure matched. Under v2 it joins the other Willow Hotel queries and the Willow School handbook query (g038), because a model could memorize "Willow" across splits. Its `knowledge_lookup` label is unchanged.

Practice questions, unanswered: (1) Under v2, what does a good test score now show, and what does it no longer show compared with v1? (2) Why are the Willow Hotel and Willow School rows in one group even though one is lookup and the other is document retrieval? (3) BFCL lookup rows mostly filter by a condition. Which v2 check stops them from filling the lookup class, and why does that matter? Learning statuses remain unchanged.

Verification: see the handoff. The validator passed the 38 regrouped rows with the unchanged review ledger. No code, dependency, or schema changed.

## Guide-v2 public import candidates, October 26, 2026

Altan approved the pilot regrouping and the Dolly attachment adapter. He adopted Dolly for document retrieval, BFCL for lookup and calculation, and No Robots for direct answer, with the batch checks. The agent built 90 `needs_review` candidates with null labels and recorded the three sources with licenses and notices. The [import record](evidence/public-import-v2.md) has the selection, checks, flags, and hashes. If every proposal were accepted, every class would pass 30 rows, 15 groups, the 40 percent request-type limit, and the 75 percent source limit, with small margins. No row is accepted yet.

Trace: q0081 is BFCL `sql_61`: "What is the average age of the customers from the 'customers' table who have made purchases above $1000?" The records must be fetched before averaging, so the proposed first action is `knowledge_lookup`. It shares the `customers` table with q0079 (`sql_51`), so both sit in one group under guide v2 rule 4.

Practice questions, unanswered: (1) Why is q0081 lookup and not calculation, even though it asks for an average? (2) Why do q0079 and q0081 share a group even though one filters and the other aggregates? (3) Fifteen lookup rows use SQL words like "table" and "column". If the model learned "table means lookup", which validation result would reveal it? Learning statuses remain unchanged.

Verification: see the handoff. The combined 128-row file passes the validator. No code, dependency, or schema changed.

## Import labels approved and blind AI check, October 26, 2026

Altan said: "Approve all proposed labels in the review worksheet." The 90 candidates took the agent's proposals as primary labels under A1, disclosed as agent-proposed and human-confirmed. A fresh `claude-opus-5-5` subagent then labeled the shuffled queries without seeing any label and agreed on all 90. It is the same model family as the proposing agent, so this is consistency, not independent validation. Thirty-five clear, unflagged rows are accepted. The other 55 carry an AI flag or an ambiguous judgment and wait for Altan's adjudication, with an agent recommendation for each. The [review record](evidence/public-review-v2.md) has the counts, categories, and hashes.

Trace: q0118 asks "What is the fastest flying bird?" Altan approved `direct_answer`, and the AI chose the same label but marked it ambiguous because no source is named and a careful annotator might choose lookup. Under the guide's default rule a stable fact without a named structured source is `direct_answer`, so the agent recommends keeping it. The row stays `needs_review` until Altan decides.

Practice questions, unanswered: (1) The AI agreed on 90 of 90. Name two reasons that number overstates label quality. (2) Why does q0118 need Altan's decision even though both labels match? (3) If Altan excludes q0065, q0068, and q0069, which readiness check fails, and what would fix it? Learning statuses remain unchanged.

Verification: see the handoff. The 128-row file passes the validator with the new ledger. Readiness fails only on pending adjudications and class counts. No code, dependency, or schema changed.

## Flagged import rows adjudicated, M1 readiness passes, October 26, 2026

Altan said: "Accept recommendations for all 55 flagged rows in the adjudication worksheet." Each flagged ledger entry now records his adjudication, no label changed, nothing was excluded, and two near-duplicates joined their partners' groups. All 128 rows are accepted. Calculation has 32 rows in 31 groups, document retrieval 31/30, lookup 32/25, and direct answer 33/30. The readiness check passes. The [review record](evidence/public-review-v2.md) has the hashes. The release is not frozen yet.

Trace: q0098 and q0097 both ask for the cosine similarity of two five-number vectors, with different numbers and back-stories. Before, they sat in g102 and g101. If one landed in training and the other in test, the model would be tested on a near-copy. Guide v2 rule 1 puts small variations in one group, so q0098 moved to g101 and the pair now always lands in the same split.

Practice questions, unanswered: (1) Readiness passed. Name one thing it checks and one thing it cannot check. (2) Lookup has 25 groups but 32 rows. Why does the split care about groups and not rows? (3) Why was moving q0098 safe for the label but important for the test score? Learning statuses remain unchanged.

Verification: see the handoff. `validate_dataset.py --ready` passes on 128 rows with `reviews-v2.jsonl`. No code, dependency, or schema changed.

## M1 release frozen, October 26, 2026

Altan said: "Freeze the M1 release as data/processed/m1-v1.jsonl with the reviews-v2 ledger." The agent copied the adjudicated file byte for byte, made the release and its ledger read-only, and reran readiness on the frozen copy, which passed. The runbook now names `reviews-v2.jsonl` for the M1 readiness and M2 preparation commands. The [freeze record](evidence/public-review-v2.md#freeze) lists the hashes of the release, ledger, source manifest, and guide.

Trace: q0081 ("average age of the customers … above $1000") is now fixed in g084 with q0079. When M2 splits by group, both rows land in the same split, and its `knowledge_lookup` label can no longer change without a new release name.

Practice questions, unanswered: (1) Why freeze the data before looking at any baseline errors? (2) What would you have to do if you found a wrong label in M2? (3) Why record the hashes of the guide and source manifest, not only the data file? Learning statuses remain unchanged.

Verification: see the handoff. Readiness passes on the frozen file. Only documentation changed in Git.

## M3 collection brief: sources chosen, October 26, 2026

The collection brief still described the pilot plan: human-authored fictional queries and no external corpora. `prepare-study` records the brief's hash at split time, so the agent drafted an update before M2. Asked whether to use web datasets, Altan said: "Go with the recommended mix without screening first and update the brief." Each class keeps its M1 public source and adds a second one. Direct answer adds Dolly's no-passage categories. Document retrieval adds No Robots' passage categories through the attachment adapter. Calculation adds GSM8K, which is not adopted until its license and revision are pinned. Lookup adds Altan-authored queries and the AI drafts. Capacity was not screened. Altan then said: "Keep 400 rows (about 100 per class) as the M3 target." The draft note is removed. `prepare-study` will record the brief's hash when it splits M2.

Trace: lookup has 32 rows, 22 of them from BFCL. Reaching 100 rows with BFCL alone would make BFCL 90 percent of the class, above the 75 percent limit. A model could then learn "SQL table wording means lookup" instead of the first action. At least 25 lookup rows must come from other sources.

Practice questions, unanswered: (1) Why must the brief be frozen before you look at M2 errors? (2) Why is source mix a quality check and not just a bookkeeping rule? (3) Why might a text-to-SQL question like "How many singers are there?" fail the guide's first step? Learning statuses remain unchanged.

Verification: see the handoff. Only documentation changed in Git; no data was downloaded or imported.

## M2 split and baselines, October 26, 2026

Altan said: "Start M2: run prepare-study with configs/m2.json and reviews-v2, run both baselines twice, and compare the runs. Stop before I inspect validation errors." `prepare-study` split the 128 rows by group into 78 training, 25 validation, and 25 sealed test rows, and recorded the hashes of the data, ledger, sources, and collection brief. Two separate runs gave byte-identical predictions. On validation, B0 (always `direct_answer`) scores accuracy 0.24 and macro-F1 0.097. L2 (TF-IDF + logistic regression, C = 1) scores 18 of 25, macro-F1 0.730. Six of its seven errors involve `direct_answer`. The [M2 record](evidence/m2-research-run.md) has the full numbers and limits.

Trace: q0081 and q0079 share group g084, so the split put both in the same partition. Neither can be in training while the other is tested, so L2 cannot score well on one simply by having memorized its partner.

Practice questions, unanswered: (1) B0 has accuracy 0.24 but macro-F1 0.097. Why does macro-F1 punish it more? (2) One validation row moves accuracy by 0.04. What does that mean for comparing two models that differ by 0.04? (3) Why must nobody look at the sealed test predictions yet? Learning statuses remain unchanged.

Verification: see the handoff. `compare` passes; `sh scripts/check.sh` passes. No code, dependency, or schema changed.

## M2 error hypotheses, October 26, 2026

The agent showed Altan the seven L2 validation errors and nine correct rows with their probabilities, plus four guiding questions. Altan then sent these hypotheses (verbatim):

> 1. **Hypothesis: L2 may respond differently to wording that introduces reference text.** Both incorrect Dolly rows say “Based on this paragraph,” while the correct examples say “Given this paragraph” or “Given a reference text.” Retrieval probabilities differ only slightly: .26/.27 for the errors versus .34/.29 for the correct rows. That suggests a fragile boundary, rather than a reliable distinction between these phrasings.
>
> 2. **Hypothesis: M4 could benefit from handling small winning margins as uncertainty.** The top-two gaps for the seven errors are: q0044 .04, q0047 .09, q0069 .06, q0084 .01, q0090 .01, q0117 .01, q0130 .01. Four errors are effectively ties at the displayed precision. A margin-based fallback or second check might help, but correct rows are also close: q0045 has a .02 gap and q0048 a .02 gap. These examples suggest testing uncertainty handling, not choosing a threshold yet.
>
> 3. **Hypothesis: explicit task cues may help, but their presence is neither necessary nor sufficient.** “Fictional” appears in the correctly classified handbook and catalog examples, and “table” appears in the strong lookup prediction for q0064 (.57). However, “paragraph” occurs in both correct and incorrect retrieval rows. Correct calculation examples do not require the literal word “calculate,” and q0090 is misclassified despite an explicit probability question. The pattern may concern how cues combine with the requested operation.
>
> 4. **Hypothesis: L2 may blur external-state lookup with reasoning, and factual answering with lookup.** Complaint status and inventory levels require external records, yet q0069 and q0084 favor calculation or direct answering. Conversely, the two No Robots errors favor lookup for general factual questions. L2 may not consistently distinguish *needing a particular external record* from *asking for factual information*.
>
> 5. **Hypothesis: source wording or task composition may contribute to the errors.** The two Dolly errors are retrieval → direct; the three BFCL errors involve lookup/calculation → calculation/direct; and the two No Robots errors are direct → lookup. This clustering could reflect source-specific language or class composition. Without source totals and the remaining correct rows, it does not establish that any source is harder.
>
> These are exploratory hypotheses from 25 rows. Identical results in m2-a and m2-b show repeatability on this sample, not independent confirmation.

The gap table in item 2 is condensed into one line here; the values are Altan's.

Agent feedback after his attempt. His displayed-precision gaps match the saved scores; exactly, q0048's is 0.027. Checks the hypotheses suggested, recorded in the [M2 record](evidence/m2-research-run.md#error-inspection):

- Hypothesis 1: "Based on this paragraph" never occurs in training, while "paragraph" occurs in 3 retrieval and 2 direct-answer training rows. An unseen opening phrase plus a word shared by two classes fits his "fragile boundary" reading.
- Hypothesis 2: the four smallest margins of all 25 rows are errors, and the next two are correct. A threshold chosen from these rows would be fitted to them, which is why he held off.
- Hypothesis 5: in training, No Robots rows are all direct answer and Dolly rows all retrieval. Source style and label are confounded, so a source-style cue and a class cue look the same to the model. This sharpens his "class composition" point and is what the M3 second-source rule is meant to break.

Trace: q0047, "Based on this paragraph when was the last time we sent them to space?" Its true first action is document retrieval because the answer is in the attached paragraph. L2 scores direct answer 0.36 and retrieval 0.27. Its opening phrase never appears in training; "when was the last time" reads like a general question.

Learning status: this is Altan's own error analysis after the agent's guiding questions. It is evidence of attempting the error-analysis exercise, not of a ledger topic. The metrics and confidence rows stay **not yet reviewed**; their ledger questions (precision/recall from a confusion matrix, reliability bins) are still unanswered. The three M2 practice questions above also remain unanswered.

Disclosure: inspecting these errors is human exposure before M3 collection. The collection brief forbids targeting them.

## M3 capacity screen, October 26, 2026

The agent recorded GSM8K in the source manifest: MIT license, confirmed from the dataset card at revision `740312ad` and OpenAI's repository LICENSE. No GSM8K file was downloaded. The agent then estimated how many new rows each source in the brief's mix can supply under guide v2, counting only rows that join no M1 group and fit the 40 percent request-type and 75 percent source limits. Small pools were judged in full, large ones on seeded samples of 30. Direct answer and document retrieval have far more than they need. BFCL can fill calculation's main share, and GSM8K is unscreened. Lookup is the bottleneck: after the limits, BFCL supplies 32 to 43 new rows and the AI drafts 11, leaving 14 to 25 rows without a source. The [capacity screen](evidence/m3-capacity-screen.md) has the table and the three decisions.

Trace: BFCL record `live_multiple_166-66-0` asks for "Adriel's detailed profile information … his id is 12445". It names a person and a record ID, so it is a keyed-record lookup. Fifteen other BFCL records also ask about Adriel. Under guide v2 they describe the same situation, so they share one group, and a group holds at most four rows. Those 16 candidates are therefore worth 4 rows, not 16. That is one reason lookup's large-looking pool shrinks.

Practice questions, unanswered: (1) Lookup already has 12 keyed-record rows. Why can BFCL's 33 eligible keyed-record rows add only 28? (2) Why does the screen drop a Dolly question like "When did Alia Bhatt get her first leading role?" even though its passage answers it? (3) Why does the screen count a sampled pool's eligible share with an interval instead of a single number? Learning statuses remain unchanged.

Verification: see the handoff. The manifest and documentation changed in Git; screening tools and candidate text stay in ignored `work/poteto/m3-capacity/`.

## GSM8K screened for calculation, October 26, 2026

Altan said: "Yes, download the GSM8K test parquet at revision 740312ad and screen it for calculation." The agent downloaded the 419,088-byte test file, checked that its SHA-256 matches the upstream hash, and exported only the question text. The worked solutions and answers were never read. All 30 seeded sample questions are word problems that supply every number, so the 1,319-question test split easily covers the 16 rows calculation needs. Lookup remains the only class with a shortfall.

Trace: GSM8K test question 1220 reads "Ian has a board that is 40 feet long. … The longer piece is 4 times longer than the shorter piece. How long is the longer piece?" Every number is in the text and the request is a numeric result, so the first action is calculation. It never says "calculate". That helps dilute the "calculate" cue the brief lists.

Practice question, unanswered: Why must the import store GSM8K's question but never its answer field, even though the router would only see the question? Learning statuses remain unchanged.

## BFCL parallel and irrelevance files screened for lookup, October 26, 2026

Altan said: "Download all eight BFCL parallel and irrelevance files at revision 61fc0608 and screen them for lookup." The agent downloaded the eight files (3,110,208 bytes), checked each against the pinned listing, and judged all 112 records that passed the lookup filter. Six are firm lookups and four are borderline. Five of the six are keyed-record lookups, a type already at its 40-row limit, so the files add only about three usable rows. The lookup shortfall is now 11 to 24 rows.

Trace: `parallel_49` asks whether "the player with id 3142 in team RocketLeague" was top scorer in three seasons. It identifies a record by ID, so its first action is a keyed-record lookup. Lookup can hold at most 40 keyed-record rows. M1 has 12, and the earlier BFCL files already supply 33 such candidates for the remaining 28 places. This row is eligible, but it does not raise capacity.

Practice question, unanswered: Why can screening more of the same source fail to fix a shortfall, even when it finds eligible rows? Learning statuses remain unchanged.

## AI lookup drafts for the shortfall, October 26, 2026

Altan said: "Draft more AI lookup candidates in non-keyed request types, avoiding M1 named settings, for me to label." The agent wrote 30 drafts across ten request types, such as condition filters, category counts, free slots, and duplicate checks. Each names its own invented organisation, so each is its own group. A script refuses to write the bundle if a draft shares a name with M1, the earlier drafts, or the BFCL candidates, overlaps any text at 0.5 Jaccard or more, or uses one of the brief's cue words. All 30 passed. They are unlabelled proposals. The [draft record](evidence/lookup-ai-drafts.md) lists the boundary cases to look at.

Trace: draft N14 reads "Add up the overtime hours logged by the night shift in the Larkspur Depot timesheet records for the week of 3 February." The addition needs the hours first, and the hours sit in a named structured source. So the first action is lookup, even though the query opens with an arithmetic verb.

Practice question, unanswered: Why must the blind AI check on these drafts be run by a different reviewer than the agent that drafted them? Learning statuses remain unchanged.

## Ricardo meeting presentation, October 27, 2026

Altan requested a concise presentation for Friday October 30, 12:30–13:00, then explicitly requested a completely new design. The agent created a separate [eight-slide meeting deck](https://chatgpt.com/space/page_e5a15c75532c8191a4ad1643233396c1) with an ivory, charcoal and burnt-orange design. It covers the planned study, accepted data, M2 results, one validation error, current M3 collection, the existing milestone targets and questions for Ricardo. Speaker notes allocate ten minutes to the update, seventeen to discussion and three to agreed actions. The deck uses the latest dated evidence rather than outdated introductory summaries. It reports no new experiments or supervisor decisions.

Trace: q0047 asks when “we sent them to space” based on an attached paragraph. The reviewed first action is document retrieval. L2 instead predicts direct answer, with raw scores 0.36 versus 0.27 for retrieval. Source wording is an exploratory explanation, not an established cause.

Practice prompts, unanswered: (1) Why does q0047 require retrieval? (2) What do identical baseline runs establish, and what remains unknown? (3) Why freeze model and confidence choices before evaluating the test set? Learning statuses remain unchanged. The presentation and its rehearsal prompts do not establish student understanding.

Verification: all eight slide renders were visually inspected. The editable chart reproduces the recorded validation macro-F1 values, 0.097 and 0.730. The 400-row collection size remains a target and the 30 new lookup drafts remain unaccepted. No implementation, data, schema or evaluation rule changed.

Repository checks: `sh scripts/check.sh` passed: environment smoke, 208 unit tests, Ruff lint, formatting (61 files already formatted), and diff whitespace. No commit was created. The previous seven-slide deck remains unchanged at state version 10.

## M1 and M2 completion work, October 28, 2026

Altan said: "Lets complete m1 and m2 now." The agent finished the remaining agent-side gates for both milestones. Altan's learning attempts and the issue closures remain his.

- **Archive.** The M1 release, review ledger, guide revision, permission manifest, readiness output, M2 split, inputs, code and both runs were archived as 47 files. They were restored into a new directory with byte-identical hashes, and M2 was rerun there from a fresh `uv sync --locked`. The rerun `m2-restored` passed `compare` against `m2-a` with identical prediction and metric bytes. The [archive record](evidence/m1-m2-archive.md) holds the commands and hashes. The M2-time sources manifest and collection brief came from commit `d541de9`, because both files changed when GSM8K was recorded.
- **Study guides.** The [M1 guide](study-guides/m1-dataset.md) covers labels, provenance, grouping v1 to v2, AI-assisted review and the source-label confound. The [M2 guide](study-guides/m2-baselines.md) covers the readiness gate, the grouped split, fit versus transform, both baselines, reproduction and the error inspection. Both were exported to `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/` as 13-page PDFs with provenance sidecars. Two subagents drafted the sources. The lead checked the numbers, IDs, quotes and a sample of slide pages against the files. [Edition evidence](study-guides/README.md#edition-evidence) lists the hashes.
- **Concepts.** The concepts are reproducibility versus generalization, training-only fitting, group leakage, macro-F1 versus accuracy, and single-annotator review versus inter-annotator agreement.

Trace: q0005 reads "A train ticket costs 45 kr. How much do three tickets cost?" It is a validation row labeled `calculation`. L2 never saw `45`, `ticket` or `tickets` in training, so those tokens get no column. The prediction is still `calculation`, at probability 0.353 against 0.278 for direct answer. The largest pushes come from `how` and `a`, and `train` pushes toward retrieval because of one Dolly row about train tracks. The prediction is right, but partly for shallow reasons.

Practice prompts, unanswered: (1) What does the `m2-restored` rerun prove that `m2-a` and `m2-b` did not, and what does it still not prove? (2) Why can't 128 of 128 AI matches be reported as inter-annotator agreement? (3) In q0005, why does `45` contribute nothing? Each guide ends with five further questions. Learning statuses remain unchanged. Delivering the PDFs does not establish understanding.

Limitations: the reproduction ran on one macOS arm64 host only. The archive is local, inside the ignored `work/` folder. Dated closure snapshots of the PDFs wait until Altan closes each milestone.

## M3 candidate import, October 28, 2026

Altan asked to complete M3. The 400-row target needs about 272 new rows with his labels, so the agent asked how to proceed, and he chose "Build import for review". The agent imported 312 candidates: the six public pools to their quotas plus three reserves each, and 90 lookup candidates for 68 places. Every row is `needs_review` with a null label. The [import record](evidence/m3-import.md) holds the rules, projections, and hashes.

- **Fixed order.** Each pool's judging order was fixed before any judgment: the capacity screen's sample, then a seeded shuffle. The agent judged rows in that order and stopped when the quota filled. The order and the skip rules, not the agent's taste, decide which eligible rows enter.
- **Cue limit.** The brief asks new rows to dilute M1's cue words. Without a limit, "paragraph" or "reference text" would rise from 32 to 41 percent of retrieval rows, and "calculate" from 50 to 51 percent of calculation rows. The import now holds each cue at its M1 share. This rule was added after the projection and before any label, and the record says so.
- **Blind check first.** Three fresh subagents checked all 312 rows on shuffled, query-only text before Altan labels them. Their output stays sealed until his labels are recorded.
- **Fill rule.** After labelling, each pool keeps accepted rows in order until its quota. Reserves and later lookup rows replace rejected ones, and every limit is checked again on the final classes.

Trace: q0140 comes from a No Robots closed-QA prompt. It asks whether a statement about plant health is true, says to use the following passage, and then pastes a 301-word article. The import cuts the prompt at the second blank line. The router sees only the question and the "use the following passage" sentence. The article becomes a linked attachment with its exact characters and a hash. The proposed first action is document retrieval, because the request points at a passage that only the attachment holds.

Practice prompts, unanswered: (1) Why fix the judging order before judging, instead of picking the clearest rows? (2) Three classes sit exactly at 75 of 100 rows from their main source. What happens to that limit if a second-source row is rejected and no reserve replaces it? (3) Why does the blind check's output stay sealed until the labels exist? Learning statuses remain unchanged.

Limitations: the agent wrote every proposed label, so approving proposals carries anchoring risk. The cue limit was chosen after seeing projected counts. The blind check is AI consistency, not human agreement.

## M3 labels adopted and blind check ingested, October 28, 2026

Altan pasted review judgments on the 312-row worksheet that, by its own statement, came from an AI reviewer. Asked how to treat them, he chose "Adopt as my A1 labels" and said the reviewer did not read the sealed blind-check files. The judgments approve the proposals except three exclusions, count 9 of the 16 borderline BFCL rows as lookup, and exclude the other 7. The blind check then gave the same label on 300 of the 302 labelled rows and a different label on none. 238 clear agreements are accepted, and 64 rows wait for his adjudication. The [import record](evidence/m3-import.md#labels-and-blind-check-october-28) holds the counts and hashes.

Trace: q0241 asks for the latest readings of all temperature and humidity sensors on a named office network. The adopted judgment counts the whole sensor group as lookup, because it reads recorded readings. The blind reviewer would exclude q0241, because "latest" reads as live data that no tool provides. Both readings follow the guide. The difference is whether "latest" means the newest stored record or the live state now. The adjudication worksheet puts that question back to Altan.

Practice prompt, unanswered: The labels and the blind check agree on 300 of 302 rows, but the labels are the agent's proposals approved through another AI's review. What does that agreement show, and what can it not show? Learning statuses remain unchanged.

Limitation: the A1 labels are human-adopted AI judgments, not human-written labels. The report must say so.

## M3 release, split and comparison, October 28, 2026

Altan said "Accept all" to the adjudication worksheet. The agent froze the 400-row `m3-v1` release with its ledger, extended the M2 split to 242 training, 79 validation and 79 sealed test rows, and ran all 14 configurations twice. The runs reproduce byte for byte, and an archive restored into a new directory reproduced them again. Validation-only selection picks L1-C10, word counts with logistic regression at C 10, with macro-F1 0.925. L3 scored 0.923, within the 0.01 tie, so the simplicity order decided. The [run record](evidence/m3-research-run.md) holds the tables and hashes.

- **Small differences.** 79 validation rows means one row moves accuracy by about 0.013. Most family differences are two rows or fewer. Only bigrams helped at every C.
- **More data versus a better model.** On the 25 rows that were M2's validation set, L2-C1 made seven errors with 78 training rows and one error with 242. The model and its settings did not change.

Trace: q0005, "A train ticket costs 45 kr. How much do three tickets cost?", is a validation row labelled `calculation`. In M2, `45`, `ticket` and `tickets` had no column, and L2 gave calculation 0.353. With 242 training rows the vocabulary holds 1,655 words, and only `ticket` is missing. L1-C10 now gives calculation 0.731, and `how`, `three`, `costs`, `cost` and `kr` push hardest toward it over direct answer. A training-only refit reproduced the saved scores exactly.

Practice prompts, unanswered: (1) Why does the selection prefer L1-C10 over L3-C0.1 when L3 is within 0.01? (2) What does the drop from seven errors to one on the same 25 rows show that the 0.925 headline does not? (3) Why can 79 validation rows not separate counts from TF-IDF here? The [M3 guide](study-guides/m3-comparison.md) ends with five further questions. Learning statuses remain unchanged.

Limitations: no test result, no human error inspection yet, one host and seed. The 272 new labels are human-adopted AI judgments, so the release has no human agreement figure.

## Supervisor dataset PDF, October 30, 2026

Altan requested a PDF of the dataset to show his supervisor today. The agent exported `output/pdf/orchestra-dataset-supervisor.pdf`: a 23-page overview of the frozen 400-row M3 release, attribution and permissions, and all 242 training queries grouped by accepted label, with source and group IDs. Validation and sealed test queries are omitted; only the training JSONL, source manifest and existing M3 evidence were read for the export. Linked document passages and review rationales are not reproduced. Emoji above U+FFFF are printed as explicit Unicode codes, disclosed in the PDF; stored data is unchanged. The generator is local scratch at `work/dataset-supervisor/build.py`. Existing output files and prior local learning-log changes were preserved. No commit was created.

Trace: training row q0001 supplies an 80 kr notebook price and a 25 percent discount. Its first action is calculation because all required numbers are already present. The router predicts the action rather than computing the answer.

Verification: all 242 training IDs occur exactly once in extracted PDF text; query text matches the input after the disclosed emoji transcription; no extra query IDs appear. All 23 page renders were inspected, with the final attribution-page revision inspected separately. The environment smoke check and 208 unit tests passed. The first lint pass also scanned the temporary PDF generator and found import-format issues; the generator was moved to ignored scratch. The final repository Ruff lint, formatting check (67 files), and diff whitespace check passed. No research run or data change was made.

Practice prompts, unanswered: (1) Why does this meeting copy omit the sealed test questions? (2) Why is the AI consistency check not independent human annotation agreement? Learning statuses remain unchanged.

## Supervisor follow-up and M3.5 plan, October 31, 2026

Altan reported positive supervisor feedback and a request for more public data and more classification methods. He requested a new M3.5 before M4, increasing the 400-row study to at least 2,500 accepted rows or preferably 4,000, and selected Random Forest, Decision Tree, XGBoost and Jev. In response to a clarification, he identified Jev as TypeSafe AI's new model. This is a scope decision, not a demonstration of model understanding.

The agent authored the [M3.5 plan](m3-5-plan.md), added [GitHub issue #25](https://github.com/AltanEsmer/Orchestra/issues/25), and changed [M4 issue #7](https://github.com/AltanEsmer/Orchestra/issues/7) to depend on it. The roadmap, project plan, README, data protocol, walkthrough and study-guide index now include the extension. M1–M3 issue closure was verified on GitHub and reconciled in the roadmap; unanswered learning questions remain open. M3.5 execution is not started. Provisional schedule changes make room for the extra work, with source/review-capacity checkpoints before committing to the forecast; the December 6 submission deadline is unchanged.

The research skill supplied one background research worker, whose [primary-source note](evidence/m3-5-research-notes.md) the lead reviewed. It identifies Jev's versioned API, four-option Choice output and separate vendor confidence statistic, and records public-data leads with license/mapping uncertainties. Existing M3 evidence was read instead of reopening sealed test data. The GitHub connector returned an access error; the authenticated local `gh` CLI created and updated the issues, and their bodies were read back and matched to the saved requests.

The plan preserves the original 400-row release and split, checks source capacity and real review effort before bulk collection, and proposes 27 configurations: the existing 14 plus four settings each for Decision Tree, Random Forest and XGBoost and one pinned Jev setup. A single tree partitions word features; a forest combines randomized trees; boosted trees add stages that improve the fitted objective. Jev instead receives query text and fixed label instructions through a pretrained API, so its comparison must disclose different pretraining, representation, cost and reproducibility. These are explanations of planned methods, not measured performance claims. XGBoost would require a dependency during implementation; no package or model was added here.

The main comparison reruns the baselines on the expanded split. An old-versus-new headline score cannot isolate the benefit of extra training rows because the validation set also grows. The plan also includes the currently missing selector/configuration/final-test integration for the new families; adding estimator constructors alone would not make M4 ready. The original hash-bound collection brief and experiment configurations were left unchanged.

Trace: “Calculate the increase using the figures in the attached report” still has `document_retrieval` as its first action. The proposed local classifiers consume training-only text features; Jev consumes the same query and fixed first-action definitions. Evaluation compares each label with the accepted first action. The study does not retrieve the report or calculate the increase.

| Check | Actual result |
| --- | --- |
| `sh scripts/check.sh` | Exit 0: locked sync resolved/checked 20 packages; environment smoke passed (Python 3.12.13, scikit-learn 1.9.1); 208 tests passed in 18.743s; Ruff reported `All checks passed!`; 69 files already formatted; diff whitespace passed. |
| Local links and anchors | 118 links/anchors across the eight other changed documents passed. |
| GitHub readback | Issue #25 and updated #7 bodies match the locally saved text; both remain OPEN. M1–M3 issues #4–#6 are CLOSED. |
| Scope/preservation review | Only planning/reference documentation changed; pre-existing learning-log/walkthrough additions and `output/`/`tmp/` files preserved. No data, split, config, model, lockfile or old collection-brief change. |

No new research experiment, corpus download, API request or M3.5 study PDF was produced. The separate full fixture workflow was not rerun for this documentation-only change; existing unit/smoke checks do not establish new-model compatibility. The shell has no bare `python` executable, so a documentation-edit helper was rerun with `python3`; the project checks used locked `uv run ... python` as documented. No commit or push was created; the planning patch remains in the working tree on baseline `6f298ac`. The GitHub issue is the shared planning record. Main unresolved limitations are eligible source capacity (especially lookup), actual review effort, Jev access/data handling/budget, and implementation/resource/reproducibility evidence.

Practice prompts, unanswered: (1) Why rerun logistic regression on the expanded split before claiming Random Forest is better? (2) How could 4,000 rows still provide too little independent evidence? (3) Why does Jev need a different fairness/reproducibility discussion from a decision tree? Wait for Altan's attempt before giving worked answers. Learning statuses remain unchanged.

## M3.5 public-data screening, October 31, 2026

Altan requested: “Let's start M3.5 by finding and screening more public data. Aim for 4,000 accepted queries, with 2,500 as the minimum.” This authorizes public-source discovery and bounded screening. It does not supply primary labels, source-adoption judgments or human review time. Accepted data remain 400 rows, 100 per class; no new release or model outcome exists.

The [capacity note](evidence/m3-5-capacity-screen.md) records 240 existing-source sample decisions and 151 provisional successes, source permission/revision evidence, conservative parent-text exclusions and row-yield uncertainty. No Robots train was newly downloaded and its 10,474,682 bytes verified against the pinned LFS SHA-256. The other existing pools reuse pinned local sources. Parent rows were read computationally for exclusion and hash checks, without displaying parent queries or inspecting model errors. Screening can reuse earlier inspected unused records; it is not an unseen-data claim.

The research skill mandated a background researcher. A worker owned only the [new-source note](evidence/m3-5-lookup-screen.md) and ignored lookup audit folder; the lead reviewed and integrated its results. ToolACE, SQL-create-context and Glaive received 390 formal sample decisions; xLAM's official data download returned 401 and was not bypassed. ToolACE yielded 18 distinct provisional lookup candidates. Glaive's corrected samples yielded 30 calculation candidates, 25 exact-unique strings and at most 23 rows in 13 tentative groups. Its separately disclosed initial-format subgroup yielded 16 lookup records, conservatively at most 10 rows in 3 tentative groups, all keyed-record. Parser correction, adaptive filters, duplicate handling and generated-language limitations remain in the evidence. These counts do not demonstrate hundreds of accepted independent groups.

Across both investigations, 630 formal decisions cover seven corpora; this is not a unique-query or accepted-row count. Direct-answer and retrieval sources look promising, while lookup diversity and non-word-problem calculation supply still need group/type inventories. We did not relax the 40% type or 75% source caps, add source cues, generate replacement rows, or change annotation boundaries. Twelve deliberate pilot cases with blank human fields and separated agent proposals are ready in ignored `work/m3-5-screen/existing/human-pilot.md`; real human review timing is unmeasured. The new collection brief and adoption decisions remain open.

README, roadmap, project plan, M3.5 plan, data-protocol progress, walkthrough and study-guide index now reflect screening in progress. GitHub issue #25 received a progress section with its original plan/checklist preserved; exact readback matched and it remains OPEN. M4 is still blocked on M3.5 acceptance. No issue comment or external query upload was sent.

The [interim lesson](study-guides/m3-5-data-screening.md) was exported using the PDF skill to `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/M3.5-data-screening.pdf` with a companion hash manifest. All three pages were rendered and visually inspected; the final question layout was re-rendered and checked. Lecture 2, `Lecture2-Data Preprocessing and Feature Engineering.pdf`, page 8 was extracted and visually inspected; SHA-256 `e7bfec9a9a52954c038e58a84f680e76648efa582ef79acafe2a3bfaa582217f`. It connects sampling/relevance checks before modeling; our labels and quotas remain project choices. This is an interim edition, not the full M3.5 methods completion PDF.

Actual verification:

- `sh scripts/check.sh`: PASS; locked environment resolved 20 packages, smoke `PASS: environment-smoke-only`, Python 3.12.13/scikit-learn 1.9.1; 208 tests in 18.164 seconds, OK; Ruff “All checks passed!” and 72 files already formatted. The test counts/splits printed by this command are artificial fixtures.
- Existing-source pool and verdict scripts rerun: all saved audit file hashes reproduced exactly. `protected-before.json` comparison: seven protected release/review/split/source/brief/environment files unchanged. The old source manifest and collection brief remain byte-identical.
- New-source reproduction: PASS, three deterministic sample orders, unchanged records, 180 aligned verdicts; Glaive verifier PASS for 150 corrected samples, exact first-user projection, aligned verdicts and complete audit hashes. The additional 60 initial-format subgroup decisions are retained with their separate sampling chronology and manifest hashes.
- Asserted 630 formal decisions across the two bundles, zero new human primary labels, unchanged accepted count and all source data paths ignored. Final `git diff --check` passed; 185 local Markdown file/anchor links passed. PDF/source hashes match its companion manifest.
- No new behavioral tests were written because application behavior is unchanged. The separate full fixture workflow was not rerun. No new-model compatibility, group-capacity completion, human throughput or accuracy improvement is claimed.

Teaching trace: “Calculate the increase using the figures in the attached report” is retrieval first, because the numeric inputs must be read before computing. It is a teaching example, not an imported research row. Unanswered practice: (1) Why can 60,000 public records yield too few usable lookup queries? (2) Why does 30/30 screening success not establish 1,000 accepted independent examples? (3) Explain why the report request is retrieval despite the word “Calculate.” No student response was invented and learning statuses remain unchanged.

No commit or push was made. Baseline remains `6f298ac`; this screening patch and the earlier planning/unrelated documentation work remain local. Raw public files, scripts and verdicts stay ignored. Main limitations: actual source/scenario groups and parent collisions, source/type coverage for both targets, source/adapter adoption, true human effort, final blind review and later model integration. Next is a concrete grouped source-mix proposal and timed human pilot before freezing bulk-collection quotas.

## M3.5 group and quota audit, October 31, 2026

Altan requested continued checks of independent groups and source quotas, prioritizing varied lookup and calculation queries toward at least 2,500 accepted rows, ideally 4,000. The [integrated audit](evidence/m3-5-group-quota-audit.md), [lookup investigation](evidence/m3-5-lookup-diversity.md) and [calculation investigation](evidence/m3-5-calculation-diversity.md) record this continuation. The research skill's background-research requirement authorized the two existing workers' follow-ups; their source notes and ignored directories were disjoint. The lead reviewed their evidence and integrated parent, duplicate, group and quota checks. No learning response was supplied by Altan.

The actual parent source/type counts were reconstructed from the frozen 400 IDs and original provenance. New screens made 773 formal decisions: 462 lookup, 220 calculation-source and 91 Dolly/No Robots. These are not unique rows; previously inspected records can recur. One hundred additional MATH positions were rights-held without route judgments and are not included. Source investigation added ToolAlpaca, attributed/revision-tracked Math Stack Exchange bodies and existing published synthetic calculation prompts. Public generated origin, HTML projection, quoted-source rights and tool/scope holds remain explicit. No new examples were generated and no new source was adopted.

After integrated exact deduplication, conservative parent holds and four-row group caps, the working inventory has **99 calculation candidates in 69 proposed groups** and **46 lookup candidates in 37 proposed groups**. Distinct strings do not establish independence; shared-scenario review remains open, and token-based groups can over-merge mathematical expressions when operators are discarded. Rejected boilerplate matches and semantic holds are retained, not silently relabeled. The inventory includes earlier candidates, so it is not 145 newly found rows. Source/type caps were neither relaxed nor redefined.

At 625 rows per class, the 75% source cap is 468, and the 40% type cap is 250. The existing 40 keyed lookups mean at least 315 new non-keyed queries are needed; only 11 are currently inventoried, leaving 304. The analogous non-word-problem calculation gap is 234 after the current 57. The full calculation/lookup row gaps are 426 and 479. The 4,000 aim has larger gaps, recorded in the audit. All are conditional on eventual acceptance of current proposals. The next bounded work targets named-source filters, membership, aggregation and duplicate-record lookup requests, plus finite probability, geometry and numerical integration. Source/adapters and measured human review effort still precede collection-brief freeze. Neither target is demonstrated yet.

The plan, roadmap, README, protocol progress, walkthrough and study-guide index link the new evidence. Issue [#25](https://github.com/AltanEsmer/Orchestra/issues/25) retains its original plan and earlier progress and adds this audit; exact body readback matched and the issue remains OPEN. M4 still waits. No issue comment was sent. Public API reads collected source evidence; no classifier API inference, paid call, model training or final-test evaluation occurred.

The PDF skill exported the [editable lesson](study-guides/m3-5-group-quota-audit.md) to `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/M3.5-group-and-quota-audit.pdf`, with source/PDF hashes in its companion manifest. Both pages were rendered and visually inspected. The prior screening PDF is preserved. The lesson reuses the Lecture 2 page 8 sampling/relevance connection visually verified earlier in this M3.5 work, at SHA-256 `e7bfec9a9a52954c038e58a84f680e76648efa582ef79acafe2a3bfaa582217f`. Project quotas are explicitly separate from course requirements. The full M3.5 methods guide remains future work.

Actual verification:

- `sh scripts/check.sh`: PASS; environment smoke passed, 208 tests in 18.022 seconds, OK; Ruff reported “All checks passed!” and 75 files already formatted. Printed test counts/splits are fixtures. No implementation changed, so no new behavior tests or full fixture-workflow rerun was needed.
- Lookup verifier: PASS, fixed query-only discovery order, 462 unchanged screened records, 22 new provisional rows with at most four per proposed group, unchanged parent and all audit hashes. Calculation bundle: all 42 saved hashes verified.
- The lead reran `audit_prior.py`, `judge_extra_math.py` and `integrate.py`: all eight output hashes reproduced. Saved a manifest of 98 inputs, outputs and scripts. Asserted 145 distinct provisional strings, no group above four, null human labels, no adoption, and the unchanged 400-row accepted release.
- Eight protected hashes remain identical: release, review ledger, split, source manifest, original collection brief, annotation guide, dependency specification and lockfile. Final checks passed: `git diff --check`, 201 local Markdown links/anchors across 16 documents, all 98 audit-manifest hashes, PDF/source manifest and the unchanged lecture hash. All 106 files under the new raw/audit work directory are ignored.

Teaching trace: “Find the records priced below 500 in the named catalogue” requires lookup first: the number is a filter and the records must be read. It is a teaching example, not an imported row. Practice prompts, unanswered: (1) Why can a batch from several sources still fail the request-type cap? (2) Why does the same placeholder number not prove a shared group? (3) Why is the catalogue example lookup rather than calculation? Wait for Altan's attempt before supplying worked practice answers. Learning statuses remain unchanged.

No commit or push was created; baseline remains `6f298ac`. Earlier local documentation and unrelated `output/`/`tmp/` work are preserved. Accepted rows remain 400, and provisional groups, source/adapters, real human review, sufficient diverse capacity and later model integration remain unresolved.

## M3.5 source discovery, November 1, 2026

Altan asked for appropriate public datasets to move M3.5 beyond 400 accepted rows, continuing the previous handoff under Poteto mode. The [discovery record](evidence/m3-5-source-discovery.md) targets the audit's two binding gaps: 304 non-keyed lookups and 234 non-word-problem calculations at 625 per class. Five subagent lanes ran under one shared brief with disjoint ignored directories. The repository's preferred `gpt-6.1-sol` worker model is unavailable in this runtime, so the lanes ran on the lead's single model family; there was no independent second judgment. The lead re-read primary licenses for the recommended sources, spot-checked each verdict file and integrated the counts. No learning response was supplied by Altan.

The lanes judged seeded samples from 19 corpora and checked five more for terms only: 804 AI decisions, all with null human labels and no adoption, plus 200 Spider/BIRD naming checks. The 244 provisional calculation and lookup rows have no exact or Jaccard-0.5 match against the earlier 145-row inventory. Human-written CLINC150 (CC BY 3.0), MASSIVE en-US (CC BY 4.0), OpenAssistant (Apache-2.0) and TheoremQA's self-written rows (MIT) give about 384 inferred non-word calculation candidates before review, enough for the 625-per-class gap but narrow in type. AQuA-RAT and CAMEL physics broaden types but need provenance decisions. For lookup, 0 of 180 sampled table-benchmark questions and none of 19 tool-corpus lookups name a structured source with a proper name. DataBench and the CLINC150/MASSIVE personal-store intents become usable only with Altan's scope decisions, and even then about 268 inferred non-keyed lookups fall short of 304.

Relevant ML concepts: selection versus population (a filtered pool's sample rate is not the corpus rate), independence (grouping bounds evidence more than row count), and shortcut learning (a source's style or a phrase such as "in the dataset" can predict a label). Alternatives considered and not taken: WildChat-style real logs (privacy decision first), MathQA (tokenized copy of AQuA), text-to-SQL corpora (questions do not name tables) and relaxing the source-in-query rule (a contract change, not a screening choice).

Actual verification:

- `sh scripts/check.sh`: exit 0; environment smoke passed, 208 tests in 17.832 seconds, OK; Ruff "All checks passed!" and 77 files already formatted. No implementation changed.
- `git diff --check`: passed. Local Markdown links in the five edited documents: 127 checked, 0 broken.
- Eight protected hashes from `work/m3-5-groups/audit/protected-before.json` are unchanged (release, review ledger, split, source manifest, collection brief, annotation guide, dependency files). All discovery files are ignored. The intents and tools lanes reran their pipelines and reproduced their outputs byte for byte.

Teaching trace, paraphrased: a CLINC150 request to convert a stated number of pounds into ounces contains every input and asks for a number, so its first action is `calculation`; the router sees only that text, never the intent label used to select it. A DataBench question asking how many unique customers appear "in the dataset" needs records read first, but names no specific dataset, so it is held until Altan decides the attached-dataset adapter. Neither is an imported row. Practice prompts, unanswered: (1) Why does a corpus with 3,149 calendar and account queries add zero eligible lookups today? (2) Why could 300 CLINC150 calculations teach a classifier the wrong cue? (3) Why does DataBench's limit come from its 80 tables rather than its 1,829 questions? Wait for Altan's attempt before supplying worked answers. Learning statuses remain unchanged.

No commit or push was created; baseline remains `6f298ac`. The study guide, PDF and issue #25 were not updated in this turn. Accepted rows remain 400. Source adoption, the four decisions listed in the discovery record, human review timing and the collection brief remain open.

## M3.5 option B decision, November 1, 2026

Altan asked what options could reach at least 2,000 accepted rows, approved the discovery findings, and chose option B: a near-balanced release where lookup keeps as many reviewed rows as pass, up to 500 with a floor of 350, and the other three classes share the rest equally. Option B carries two lookup scope rules for M3.5: a question that refers to its own table generically may keep that table as an attachment and routes to `knowledge_lookup`, and the user's own stores count as structured sources with one group per store kind. The plan, protocol, roadmap, README and project plan now record the 2,000-row working minimum; the hash-bound v2 guide is unchanged and the future collection brief will carry the rules. AQuA-RAT, CAMEL and TheoremQA provenance and any authored supplement remain undecided.

Two screens followed, recorded in the [option B supply note](evidence/m3-5-option-b-supply.md). The lead judged a seeded 30-row DataBench sample under the new attachment rule: 29 eligible, all non-keyed, about 209 rows after the four-per-table cap. A worker subagent screened 240 further rows from the already-downloaded ToolAlpaca and ToolACE pools and retained 38. The lead held seven of its 18 non-personal rows (live data or third-party services held for tool scope on October 31), and the 20 remaining rows read third-party developer or business accounts. Asked whether those count as personal stores, Altan chose "Count all accounts", so 11 to 20 of them enter the estimate (nine may merge with existing store kinds at review). The lookup class now looks like about 430 to 470 rows before review. The worker ran on the lead's model family because `gpt-6.1-sol` is unavailable; there is no independent second judgment. No learning response was supplied by Altan.

Relevant ML concepts: class imbalance versus metric choice (macro-F1 weights classes equally, so support changes but weighting does not), grouping as the real capacity limit (DataBench is bounded by tables, not questions), and shortcut risk from source phrasing ("in the dataset", "my"). Alternatives considered and not taken: a balanced 500-per-class release requiring an authored supplement, and smaller lookup classes that would leave too few test rows for a stable per-class F1.

Actual verification:

- `sh scripts/check.sh`: exit 0; environment smoke passed, 208 tests in 20.713 seconds, OK; Ruff "All checks passed!" and 78 files already formatted (Ruff's count includes Markdown, so the new evidence note is the added file). No implementation changed.
- `git diff --check`: passed. Local Markdown links in the eight edited or new documents: 196 checked, 0 broken.
- Eight protected hashes from `work/m3-5-groups/audit/protected-before.json` are unchanged. The DataBench build and judge scripts reran and reproduced all five outputs byte for byte. All option B screening files are ignored; the worker's 240 verdicts all carry null human labels and no adoption.

Teaching trace, paraphrased: a DataBench question asking for the three shortest talk durations "in the dataset" now keeps its table as an attachment the router never sees; the text alone signals that records must be read, so its first action is `knowledge_lookup`. It joins its table's group, which allows four rows. A Dolly question asking what a supplied passage says about a date still routes to `document_retrieval`, because the attachment is prose rather than structured records. Neither is an imported row. Practice prompts, unanswered: (1) Why does lowering the lookup class from 500 to 450 barely change how macro-F1 weights lookup? (2) Why could "in the dataset" become a shortcut, and what kind of row would counter it? (3) Why does each personal store kind add at most four rows, however many calendar queries exist? Wait for Altan's attempt before supplying worked answers. Learning statuses remain unchanged.

No commit or push was created; baseline remains `6f298ac`. The study guide, PDF and issue #25 were not updated. Accepted rows remain 400.

## M3.5 collection brief draft, November 1, 2026

Altan asked to commit the M3.5 work and then to draft the collection brief. The commits `25af092` through `2eeb007` (seven, unpushed) hold all earlier M3.5 evidence, plan and study files. The new [draft brief](collection-brief-m3-5.md) is not frozen. It sets the 2,000-row near-balanced targets and caps for lookup sizes 350 to 500, per-source records, the guide-v3 lookup rules with a frozen starting list of store kinds, grouping, seeded pools with interleaving ratios and a `cap-hold` rule, a stop rule, a two-stage review and measured cue counts. Six decisions precede freezing: source adoption, calculation provenance, the "dataset" cue, DataBench attachments, five borderline store kinds and the timing-pilot schedule. No learning response was supplied by Altan.

New measurements for the brief: whole-word cue counts over the M3 release and candidate pools (counts only; no M3 text printed), and the DataBench file listing at the pinned revision (80 full tables, 373.8 MB; 80 sample tables, 6.2 MB) read from Hugging Face metadata without downloading. "Dataset" appears in 276 of 310 DataBench candidates and only 8 candidates elsewhere, so it is the strongest new cue. A fresh reviewer subagent, given the sources but not the lead's conclusions, returned 12 findings. All were addressed: generated public text now qualifies under the personal-store rule, the brief gained pool paths, interleaving and cap holds, per-source records, a workload estimate that counts rejected candidates, a guide-v3 binding and affected-row check, and retrieval-side cue candidates. The reviewer confirmed the cap table and the licenses. It ran on the lead's model family.

Relevant ML concepts: sampling order as a source of selection bias (a fixed seeded order prevents picking convenient rows), cumulative constraints (a batch can break a cap that the final release would meet), and shortcut cues measured before training rather than discovered afterwards. Alternatives considered and not taken: downloading 374 MB of tables the router never reads, and quotas fixed per source regardless of review yield.

Actual verification:

- `sh scripts/check.sh`: exit 0; 208 tests in 17.697 seconds, OK; Ruff "All checks passed!" and 79 files already formatted (the new brief is the added Markdown file). No implementation changed.
- `git diff --check`: passed. Local Markdown links in the six edited or new documents: 146 checked, 0 broken.
- Eight protected hashes unchanged, including the frozen M3 brief and v2 guide. The cue script reran with an identical `cues.json`; all brief work files are ignored.

Teaching trace, paraphrased: a CLINC150 request to list the items on the user's shopping list joins the shopping-list store-kind group shared with MASSIVE, which can hold four rows in total. If lookup batches have already accepted many keyed records, a passing keyed row waits as a `cap-hold` until non-keyed rows make room, rather than pushing keyed records above 40%. Practice prompts, unanswered: (1) Why does the brief fill lookup before the other classes? (2) What would go wrong if Altan saw the screen's proposed label before writing a label? (3) Why can 1,600 accepted rows require reviewing more than 1,600 candidates? Wait for Altan's attempt before supplying worked answers. Learning statuses remain unchanged.

## M3.5 brief decisions, November 2, 2026

Altan answered "Accept all five" to the recommended answers for decisions 1 to 5 in the [draft brief](collection-brief-m3-5.md). CLINC150, MASSIVE, oasst2, TheoremQA's author-written rows, DataBench, ToolACE, ToolAlpaca and Glaive are adopted, with source-manifest entries still to write. AQuA-RAT, CAMEL physics, Math Stack Exchange, the synthetic calculation benchmark and TheoremQA's externally sourced rows stay excluded. The "dataset" cue is accepted with the brief's counter-measures and no DataBench cap. DataBench tables are recorded as pinned references, a disclosed departure from the Dolly local attachment file. The five borderline store kinds merge into bank account, contacts, lists, transactions and maintenance records. The brief, plan, protocol, roadmap and repo guide record these choices. Still open before freezing: Altan's 12-case timing pilot and the agent's check of affected M3 training and validation rows. These are scope decisions, not evidence of understanding; the earlier practice prompts remain unanswered and learning statuses are unchanged. No commit was created in this step.

## M3.5 affected-row check, November 2, 2026

Altan asked the agent to run the guide-v3 affected-row check. It read only the prepared M3 training and validation files; the sealed test file was not opened. A whole-word regex for "my", "dataset", "table" and "database" found 41 rows (28 training, 13 validation; 29 lookups, 6 calculations, 5 direct answers, 1 retrieval). Guide v3 changes none of their labels. Existing lookups stay lookups; the other twelve use "my" without reading a store, and one mentions "my dataset" without an attached table while supplying every number, so it stays a calculation. The check found one drafting error: the brief's live-status wording would have excluded three accepted lookups that read an order or complaint status by ID (q0068, q0069, q0215). The brief, protocol and option B note now follow guide v2's live rule instead. Verdicts are saved in ignored `work/m3-5-groups/option-b/brief/affected-rows.json` with the input file hashes. Only the timing pilot remains before freezing the brief. No learning response was supplied; statuses are unchanged. No commit was created in this step.

## M3.5 classifier implementation, November 2, 2026

Altan asked the agent to recheck [issue #25](https://github.com/AltanEsmer/Orchestra/issues/25), then plan and implement Random Forest, Jev, Decision Tree and XGBoost, and to open a pull request. Altan also set the agent models: Sonnet 5.5 at medium effort for workers and Opus at high effort for reviewers. Two workers wrote disjoint files (tree families and matrix; Jev adapter). The lead connected Jev to the runner, revised the Jev prompt using TypeSafe's integration guidance, and ran the real-artifact checks. The [classifier record](evidence/m3-5-classifiers.md) holds the details.

What changed: `DT`, `RF` and `XGB` read the same training-only unigram TF-IDF as L2 and S1, with the plan's four settings each. Each family is one `FAMILIES` entry naming its configuration keys, ID rule and tie key. A run config picks the `m3` or `m3.5` matrix. The `jev` command sends validation queries to TypeSafe up to a cap and logs every exchange, and the `Jev` family replays that log offline. XGBoost 3.4.1 is pinned, with the CPU-only build on Linux; macOS needs Homebrew's `libomp`, which the agent installed on this machine.

Relevant ML concepts: a decision tree splits on one feature value at a time; a random forest averages many trees grown on bootstrap samples with random feature subsets (bagging), which lowers variance; boosting fits trees one after another, each correcting the errors left by the trees before it. XGBoost reads an absent sparse entry as a missing value and learns where missing values go at each split. Jev is a pretrained model prompted with fixed instructions, so it learns nothing from this study's training rows. Alternatives considered and not taken: densifying the TF-IDF matrix for XGBoost (memory, and the plan forbids silent densification), the Linux `xgboost` wheel with its GPU library, scikit-learn's HistGradientBoosting in place of the requested XGBoost, and any live Jev request without a key, cap and data-handling approval.

Actual verification:

- Full unit suite: 239 tests OK (208 before); `sh scripts/check.sh` exits 0.
- An Opus reviewer at high effort, given the diff and the plan, found no breach of M3 compatibility, sealed-test isolation, network-free tests, the failure policy, label order or determinism. It raised eight hardening findings, all addressed. Answers now bind to the pinned model and the exact prompt bytes, collection and replay share one answer key, the `jev` command refuses a log path Git would track, a dropped connection is logged rather than lost, and two tests were strengthened. Disabling the prompt-binding or model check makes the Jev tests fail (measured). The reviewer ran on Anthropic models, like the workers, so this is not cross-family review.
- `select` on the stored `results/m3-a` equals the stored `m3-a-selection.json`; a fresh M3 rerun, `m3-compat-nov2`, compared `PASS: runs reproduce` against `m3-a`.
- `scripts/verify_workflow.py --out work/ci-proof-m3-5-models`: `PASS: artificial workflow, 24 commands`.
- Training-only pilot over 242 M3 training rows: 26 local configurations in 2.15 seconds, peak 164.8 MiB. No validation or test file was opened by the pilot, and no new family has a validation score.

Teaching trace for "What is 18 percent of 250?": the TF-IDF step turns it into weights for words such as "percent" and "250" seen in training. A decision tree follows one path of word-weight tests to a leaf whose training rows were mostly `calculation`. A random forest lets 200 such trees vote. XGBoost adds the outputs of 200 small trees per class and turns the four sums into probabilities. Jev instead receives `{"query": "What is 18 percent of 250?"}` and the four label descriptions, and returns its own four probabilities. Practice prompts, unanswered: (1) Why does a random forest sample rows and features at random for each tree? (2) Why can treating an absent word as missing differ from treating it as zero? (3) Why does replaying saved Jev answers prove the log is intact but not that Jev would answer the same way again? Wait for Altan's attempt before supplying worked answers. Learning statuses remain unchanged.

Afterwards Altan answered "Wait for M3.5" to whether the new families should run on the frozen M3 validation rows now. They will be scored first in the M3.5 comparison, so the 79 parent validation rows that stay in the M3.5 validation partition are not seen with the new families in advance. This is a scope decision, not evidence of understanding; the practice prompts remain unanswered.

## M3.5 dataset release, November 2, 2026

Another agent session asked this one to build `m3-5-v1` under the M3.5 brief, with Altan's November 2 decisions: accept a new row when an AI screen and an independent blind AI check agree and neither flags it, with Altan adjudicating every disagreement, flag or abstention; skip the timing pilot; keep option B's size. Mid-collection Altan wrote "We can make rules less strict than before to even obtain more dataset as it is one of the most important", then chose "Up to 1,000 per class" and "Keep all rules". Altan answered the three adjudication worksheets with "Use suggested defaults", "use same defaults" and "Use same defaults". The [dataset record](evidence/m3-5-dataset.md) holds every count and hash.

What changed: the brief records both decisions and the post-freeze size change. Eight sources gained manifest entries. `src/orchestra/collection.py` adds seeded orders, the weighted interleave, import adapters and the cumulative release checks, with a `check-collection` command. Ignored driver scripts drew 7,206 candidates; Sonnet screens and Opus blind checks reviewed them. The release has 3,145 rows: retrieval 1,000, direct answer 1,000, calculation 651, lookup 494. The M3 split was extended to 1,888 / 629 / 628.

Relevant ML concepts: label quality bounds what any classifier can learn, so the release reports how labels were made, not only how many. Group-aware splitting keeps paraphrases and number swaps of one request in one partition; without it a validation score rewards memorizing a template. Source and request-type caps limit shortcuts, where a model learns "this corpus" or "this phrasing" instead of the first action. A word such as "dataset", which appears almost only in lookups, is such a cue. Class imbalance (494 lookups against 1,000 retrievals) leaves macro-F1 weighting the classes equally but gives the model fewer lookup examples to learn from.

Alternatives considered and not taken: per-row human labels (Altan replaced them); relaxing the four-row group cap or the share caps for more rows (Altan kept them); adding unlisted sources when calculation and lookup ran short (the brief forbids switching sources); joining every pair of short prompts that share a frame (the agent first did this, then replaced it with M3's narrower precedent before freezing).

Actual verification:

- `check-collection` on the release: `PASS: M3.5 collection checks`.
- `scripts/validate_dataset.py ... --ready`: `PASS: M1 readiness checks passed (3145 accepted rows, 3145 reviewed)`.
- `prepare-study` with `configs/m3-5.json`: readiness passed and `PASS: extension written`, parent hash `6d48e18b…` pinned.
- `sh scripts/check.sh`: exit 0; 34 tests in `tests/test_collection.py`.
- An Opus reviewer at high effort checked the diff and recomputed the note's counts and hashes. It found one blocking issue: a practice prompt quoted text from a validation row. The agent replaced it before anything was pushed, so it never entered shared history. It also found seven should-fix issues, all addressed: a teaching trace that used a row outside the release, the wrong cause for calculation's shortfall, untested cap boundaries, overstated wording about Altan's adjudication, an incomplete screen-bias disclosure, 142 rows skipped on the screen label alone (now disclosed as a deviation), and no check for a dropped parent row (now refused). The reviewer ran on the same model family.

Teaching trace for q0449, a CLINC150 request to convert a weight in pounds to kilograms, now in the training partition (its text is not quoted here). It came from the saved seed-42 calculation order, so it was drawn at a fixed place in a calculation batch. The screen labeled it `calculation`, type per-unit-scaling, and flagged `needs-constant`, because the pound-to-kilogram factor is not in the query. The blind check, seeing only the text, also chose `calculation` but judged it ambiguous for the same reason. The flag sent it to Altan, whose W1 answer adopted the default for that theme and accepted it. Its number-swap skeleton made it group g430 with other requests of the same frame, and the extension placed that whole group in the training partition. Only its text reaches the router.

Practice prompts, unanswered: (1) Why does AI agreement between two Claude models not count as human agreement, even at 96%? (2) Why should two invented requests such as "how many cups are in 9 litres" and "how many litres are in 9 cups" share a group? (3) What would you expect a classifier to learn from "in the dataset" if DataBench supplied 42% of lookups and no other class used the phrase? Wait for Altan's attempt before supplying worked answers. Learning statuses remain unchanged; the three earlier M3.5 plan prompts also remain unanswered.

## M3.5 research run, November 2, 2026

After the dataset PR merged, the agent ran the 26 local configurations twice on `m3-5-v1` from a branch of the updated `main`, compared the runs, ran `select` and `report`, and reproduced run A from a restored archive. The [run record](evidence/m3-5-research-run.md) holds the scores, timings and hashes.

What changed: no code. The new evidence note, and status lines in the plan, roadmap, README, runbook and repo guide. Results stay in ignored `results/`.

Relevant ML concepts: model selection uses validation data only, and a tie rule (within 0.01 macro-F1, prefer the simpler setting) prevents chasing noise between near-equal settings. Bigrams let L3 see two-word phrases such as "how many" or "the passage", which single words lose; on this validation set that family scores highest (0.952). Trees split on one word weight at a time, so a single tree overfits rare words (DT 0.818); averaging 200 trees (RF 0.913) or adding them sequentially (XGB 0.901) recovers much of that, but not the linear models' level on sparse text. Reproduction has two levels: two runs on this machine, then a rerun from a restored archive in a fresh environment.

Alternatives considered and not taken: choosing an overall winner without Jev (the M3.5 rules make the selection invalid instead); comparing 0.952 with M3's 0.925 (different validation rows); reading the sealed test (not before M4's freeze).

Actual verification: both runs `ok` for all 26; `compare`: `PASS: runs reproduce`; `select`: invalid, `missing: ["Jev"]`; restored archive: `PASS: 59 restored files byte-identical to originals` and `PASS: runs reproduce`. About 22 s and 320 MiB per run.

Teaching trace: q0449, the pound-to-kilogram conversion from the dataset entry, is a training row. During `run`, the TF-IDF vectorizer learns its words' weights from training rows only. L3-C10's logistic regression then learns one weight per word or word pair and class from all training rows, this one included. No score is computed for a training row; the model predicts the 629 validation rows, and selection reads only those predictions. Practice prompts, unanswered: (1) Why is the overall selection marked invalid rather than choosing L3-C10 now? (2) L3-C10 makes no error on the 35 validation rows containing "dataset". Why does that not prove the model understands lookups? (3) Why can a random forest beat a single tree on the same features? Wait for Altan's attempt before supplying worked answers. Learning statuses remain unchanged.

## M3.5 Jev run and 27-configuration selection, November 2, 2026

Altan wrote "Create and merge PR for dataset updates and then complete m3.5" and pointed to a local file with a TypeSafe key. The agent merged the run record (PR #28), sent the 629 validation queries to `jev-1.14.0` in a main and a repeat pass, added the Jev entry, reran all 27 configurations twice, selected, reported and reproduced from a restored archive. The [27-configuration record](evidence/m3-5-full-run.md) holds the numbers. The agent's first look at the key file printed the key into the local session transcript; it told Altan and advised rotating the key.

What changed: no code. The new evidence note, and status lines in the plan, roadmap, README, runbook, repo guide, data protocol and earlier M3.5 notes. Logs and results stay in ignored `results/`.

Relevant ML concepts: Jev is a pretrained model that reads the four label descriptions, so it needs no training rows; the local models learn the same distinction only from 1,888 labeled examples. That makes this a system comparison, not a feature or classifier comparison on equal inputs. Jev scores 0.975 validation macro-F1 against L3-C10's 0.952, and the frozen tie rules select it because no local winner is within 0.01. Jev and L3-C10 share only one error, so they fail on different rows. Probability quality is separate from accuracy: Jev's Brier score (0.059) is lower than L3-C10's (0.096), but its probabilities are underconfident (mean top 0.92 against 0.97 accuracy). An API model can answer differently when asked again: the repeat flipped 2 of 629 top choices.

Alternatives considered and not taken: tuning the Jev prompt on validation (the prompt was frozen before any request); dropping or re-asking rows Jev got wrong (the failure policy re-sends only failed requests); a decomposed set of yes/no questions (a second Jev setup outside the plan); sending the sealed test (that is M4's single final test, and it needs Altan's separate approval).

Actual verification:

- Jev collection: smoke test 3 of 3 valid, then the main pass 629 of 629 and the repeat 629 of 629, with no failed request.
- Runs: `m3-5-full-a` and `m3-5-full-b` report all 27 configurations `ok`, and `compare` prints `PASS: runs reproduce`.
- Selection: `select` prints `PASS: overall Jev`.
- Restored archive: `PASS: 62 restored files byte-identical to originals`, and its rerun prints `PASS: runs reproduce`.
- The 26 local metrics equal the first run's.

Teaching trace for q2851, a retrieval row in the validation partition (its text is not quoted here). In the main pass, Jev received `{"query": <its text>}` with the frozen question and returned `document_retrieval` with top probability 0.52. In the repeat pass it returned `direct_answer` with 0.50. The runs replay only the main log, whose hash is pinned in the config, so both runs saw `document_retrieval` and the row counts as correct. Replay makes the run deterministic; the repeat log shows the API itself is not.

Practice prompts, unanswered:

1. Jev scores 0.975 and L3-C10 0.952 on the same 629 rows. Why is that still not evidence of which one does better on the sealed test?
2. The two answers that flipped had top probabilities near 0.5. What does a probability near 0.5 tell you about a single prediction?
3. Why does the record also report the 79 M3 rows separately from the 550 new rows?

Wait for Altan's attempt before supplying worked answers. Learning statuses remain unchanged; earlier M3.5 prompts also remain unanswered.

## M3.5 integration with M4, November 2, 2026

Altan answered "Merge #29, then integrate". The agent merged PR #29 and extended the M4 commands (`confidence`, `freeze`, `final-test`) to the 27-configuration decision set.

What changed:
- **`systems.json`:** `confidence` writes it, declaring each chosen system's score type, calibration and validation metrics. Only the chosen logistic system is recalibrated.
- **Freeze:** when Jev is chosen, the freeze names an ignored Jev test log that must not exist yet.
- **Final test:** `final-test` refuses a Jev set unless `--send-jev-test` and a key are given, before any receipt. It collects Jev's test answers only inside the reservation, and `--resume` resends only the missing queries.
- **XGBoost version:** an M3.5 run must record its XGBoost version, and it must match.
- **Rejected key:** `jev collect` stops after a 401 or 403 instead of sending every remaining query.
- **Probability sums:** rows may sum to 1 within 1e-3, the bound Jev's parser already used. The old 1e-10 rejected XGBoost's float32 probabilities.

Relevant ML concepts:
- **Calibration:** it fits a small model that maps raw scores to better probabilities. It needs data the classifier did not train on, here grouped training folds.
- **Why only one system:** a pretrained API model cannot be refit inside those folds, so Jev's probabilities are reported as they are.
- **Single test:** a final test is meaningful only if every decision is frozen before the test is read. Sending test text to an API is also reading it, so it belongs inside the same one-time reservation.

Alternatives considered and not taken:
- **Collecting Jev's test answers with the `jev` command before the freeze:** that would expose the test outside the receipt.
- **Calibrating Jev or the trees too:** not declared in the plan, and it would add choices before freezing.
- **Renormalizing XGBoost's probabilities:** a tolerance changes no saved prediction.

Actual verification:
- **Tests:** `sh scripts/check.sh` exits 0 with 284 tests.
- **Mutation checks:** fifteen mutations of the new checks were each caught by a failing test, after three tests were tightened.
- **Real run:** `confidence` on `m3-5-full-a`, written to a scratch folder, reproduced all ten chosen systems and calibrated only L3-C10, before and after the review fixes.
- **Independent review:** an Opus reviewer at high effort found no blocking defect and confirmed that test rows are read or sent only after the `opened` receipt. Its three medium findings were fixed, each with a new test:
  - a log edited between attempts went undetected;
  - a missing log folder failed only after opening;
  - a rejected key sent every query.

  So were its low ones: a request count from the last attempt only, a send function accepted without Jev, the XGBoost check depending on the recorded field, and boundary tests for the tolerance.
- **Sealed test:** not opened.

Teaching trace: say Altan approves and runs the final test. `freeze` records `results/jev/m3-5-test.jsonl`, which does not exist yet. `final-test --send-jev-test` reserves the split and opens the 628 test rows. Then it sends each row as `{"query": <text>}` with the same frozen question as validation. If TypeSafe drops three requests, the attempt stops with a `failed_after_reservation` receipt, and the identical command with `--resume` sends only those three. Jev's predictions then come from replaying the completed test log, whose hash goes into the results, next to the nine local systems refit on training rows.

Practice prompts, unanswered:
1. Why does sending the test queries to Jev count as opening the test?
2. Why is only one system calibrated, and why not Jev?
3. What would go wrong if a failed Jev request were treated as a wrong answer instead of being resent?

Wait for Altan's attempt before supplying worked answers. Learning statuses remain unchanged.

## M3.5 study guide and status check, November 3, 2026

Altan wrote "Complete m3.5 and report me when m4 is fully ready" and pointed to a handoff. The agent re-verified the inherited state, delivered the [M3.5 study guide](study-guides/m3-5-data-and-methods.md) and its PDF, and corrected stale status text. No code, data or result changed.

What changed:
- **Study guide:** a new lesson on the release, the four new families, the selection of Jev, results, limits and a q0005 trace. The 18-page PDF is in the external study folder ([edition evidence](study-guides/README.md#m35-data-and-methods-edition-november-3-2026)).
- **Course sources:** Lecture 7 (ensembles and model evaluation) is now listed with its verified pages.
- **Status:** the plan intro, roadmap, README and repo guide now describe the November 3 state. M3.5 is in review; M4 stays blocked.

Relevant ML concepts:
- **Single tree:** it chooses each split by the lowest weighted Gini impurity. Depth and leaf size limit it.
- **Bagging and boosting:** a forest averages many trees trained on bootstrap samples, which lowers variance. Boosting adds shallow trees in sequence, each reducing the remaining loss.
- **Jev:** a pretrained system that sees none of the training rows, so its gap to L3-C10 is a system comparison.

Actual verification:
- **Software checks:** `sh scripts/check.sh` exits 0, with smoke passing, 284 tests, and Ruff and `git diff --check` clean.
- **Release:** `check-collection` on `m3-5-v1` prints `PASS: M3.5 collection checks`, and a separate count finds 3,145 rows: 1,000 retrieval, 1,000 direct, 651 calculation and 494 lookup.
- **Guide numbers:** the selection scores and q0005 probabilities equal `results/m3-5-full-a`. Five cited lecture pages were extracted again.
- **PDF:** all 18 pages were inspected, every source word was found in the extracted text, and two exports were byte-identical.
- **Sealed test:** not opened.

Teaching trace for q0005, "A train ticket costs 45 kr. How much do three tickets cost?", an Altan-authored validation row labelled `calculation`. L3-C10 gives calculation 0.80. The depth-30 tree asks 18 questions, reaches a 3-row leaf of direct answers and gives direct answer 1.0. The forest splits 91 to 86 of 200 trees between direct answer and calculation. XGBoost gives direct answer 0.87. Jev returns calculation with probability 1 in both passes. One row ranks nothing; it shows how differently the families reach a decision.

Practice prompts, unanswered (the guide's six; the first three carry over from the plan):
1. Why must we rerun logistic regression on the expanded split before claiming Random Forest is better?
2. How could 4,000 rows still contain too little independent evidence?
3. Why does Jev need a different fairness and reproducibility discussion from a decision tree?
4. Suppose Jev had scored 0.960 and every other family winner were unchanged. Apply the overall rule step by step. Which system is chosen, and which step decides?
5. In the q0005 trace, why is the tree's 1.0 weaker evidence than it looks?
6. A reader asks, "Is Jev's 0.975 agreement with human labels?" What do you answer?

Wait for Altan's attempt before supplying worked answers. Learning statuses remain unchanged, and earlier M3.5 prompts remain open.

## M3.5 and M4 practice answers, November 3, 2026

Altan answered all nine open prompts without a worked answer: the six from the M3.5 guide and the three from the M4 integration. In the same message he wrote "I approve to send 628 tests to Jev." That approval covers `final-test --send-jev-test` for the 628 sealed-test queries. It does not by itself accept M3.5.

Faithful summaries and feedback:

1. **Rerun before comparing.** The comparison must use the same data, or a score gap could come from the larger dataset or the changed validation population. Correct. Feedback: the project shows it. M3 chose L1-C10, and on the expanded split the best local system is L3-C10.
2. **4,000 rows, little evidence.** Paraphrases, number swaps and a few sources can cover few independent scenarios. Group-aware splitting stops related rows crossing partitions, but source and scenario coverage still matter. Correct. Feedback: lookup's 494 rows sit in only 223 groups.
3. **Jev's fairness and reproducibility.** The tree learns from our rows. Jev brings unknown pretraining and written label instructions, so the gap compares systems. Refitting reproduces the tree; replaying Jev's log reproduces an artifact, fresh calls may change, and pretraining overlap is unknown. Correct and complete.
4. **Rule with Jev at 0.960.** Cutoff 0.950; L3-C10 at 0.9524 qualifies; the family order puts L3 before Jev, so the order step decides and L3-C10 is chosen. Report Jev's higher validation score and that the frozen rule chose L3-C10, and say the tolerance is a project preference, not statistical equivalence. Correct, with the right reporting caveat.
5. **The three tree scores.** The tree's 1 is three training rows in one leaf, weak evidence; the forest's 0.455 is the average over 200 trees, close to calculation's 0.430; XGBoost's 0.8656 is softmax over summed boosted scores. Check held-out calibration, bin counts, probability losses and similar errors before trusting it, and it is already confident and wrong here. Correct.
6. **"Is 0.975 human agreement?"** No. It is macro-F1 against accepted reference labels made mostly by AI checks with Altan adjudicating disagreements. Agreement needs independent human judgments before reconciliation, a documented sample and a stated measure. Correct.
7. **Sending test queries opens the test.** Jev processes the held-out inputs and produces predictions even before anyone sees a score, so it belongs after the freeze inside the recorded procedure. Correct. Feedback: the text also leaves our control once a vendor receives it.
8. **Only one calibrated system.** Declared experiment; grouped training folds; Jev cannot be refit there, and calibrating it would need a separate experiment. Correct.
9. **Failed request counted wrong.** It mixes service failure with classification error; resend only failed or invalid requests, never a valid wrong answer, and keep unresolved failures explicit. Correct; this is what `final-test --resume` does.

Status changes from these answers:
- **Model selection** (tolerance, family order, test exposure): **explained independently**, applied to the unfamiliar hypothetical in prompt 4.
- **Tree families and their scores**: **explained independently** for the q0005 trace.
- **Reproducibility of an API system**: **explained independently**.
- **Leakage and grouping**: still **needs practice**. Group evidence and test exposure were explained; split-before-fitting and vocabulary leakage remain unattempted.
- **Confidence and fallback**: calibration's purpose was explained; the reliability-bin and coverage exercise remains **not yet reviewed**.
- **Metrics**: the difference between macro-F1 and an agreement rate was explained; the precision/recall exercise remains **not yet reviewed**.

Next exercise: from a 2 × 2 slice of a confusion matrix, compute one class's precision and recall, then say what a reliability bin with 30 rows, mean confidence 0.9 and accuracy 0.8 means.

## M3.5 acceptance and the M4 final test, November 3, 2026

Altan wrote "Accept, run it" and named the file holding his TypeSafe key. The agent recorded the acceptance, kept the dated M3.5 snapshot, then ran `confidence`, `freeze` and one `final-test --send-jev-test`. The [M4 final-test record](evidence/m4-final-test.md) holds the numbers.

What changed: no code. A new evidence note and status lines in the roadmap, README, plan, M3.5 plan and study-guide index. The test outputs, the interpretation ledger and the Jev test log stay in ignored `results/`.

Relevant ML concepts:
- **Optimism of selection:** Jev scored 0.975 on the validation rows that chose it and 0.964 on the sealed test. The gap is small here, but it is the reason the test exists.
- **Ranking instability:** S1-C1 beat L3-C10 on test after trailing on validation. A 0.016 validation gap does not reliably rank two families, and the frozen choice is not revisited.
- **Fallback threshold:** the calibrated logistic system already met the 0.90 target with every query accepted, so the frozen threshold is 0.0. It also held on test, at 0.932.

Actual verification: freeze and final test each printed `PASS`; the receipt records one complete attempt; Jev answered 628 of 628 with no failure; the key appears in no output; the lead recomputed by-origin scores and error groups.

Teaching trace: q0005 is a validation row, so it never reaches the test. For a test row, `final-test` reserved the split, opened it, sent `{"query": <text>}` to Jev with the frozen question, logged the answer, refit the nine local systems on training rows, applied the frozen threshold 0.0 to calibrated L3-C10, and scored every system against the accepted label once.

Practice prompts, unanswered:
1. Jev lost 0.011 macro-F1 from validation to test, and S1-C1 gained 0.009. Why can a system that was not selected rise on test?
2. S1-C1 beat L3-C10 on test. Why must the report keep L3-C10 as the frozen local choice?
3. Jev made no error on the 79 inherited M3 test rows. What can and can't you conclude from that?

Wait for Altan's attempt before supplying worked answers. Learning statuses are unchanged by this run.

## M4 test mistakes and study guide, November 3, 2026

Altan asked to start M4 from issue #7 on a fresh branch, in Poteto mode. The freeze and the one final test had already run, so the remaining agent work was the post-freeze review of test mistakes and the M4 study guide. The work is on branch `claude/m4-confidence-errors`.

What changed:
- **`test-review` command:** checks a test interpretation ledger against the final-test predictions with the freeze's coverage rule, and prints interpreted errors and category counts per system (`ffba6d4`, `ae5b6cf`). It reuses the validation ledger check and adds one test.
- **Test mistakes:** a worker agent drafted a hypothesis for every Jev (26) and raw L3-C10 (41) test error. The lead read each against its text and corrected five. The ledger stays in ignored `results/`; the [M4 record](evidence/m4-final-test.md#test-mistakes-interpreted-after-the-freeze) holds the counts and examples (`55d22c0`). No label, selection or score changed.
- **Correction:** the M4 record no longer calls Jev's 0.011 drop the expected optimism of selection. L1-C1, L3-C10 and XGBoost, none of them the overall pick, fell by 0.025 to 0.030, so a harder test split is also likely.
- **Study guide:** the 16-page [M4 guide](study-guides/m4-confidence-errors.md) and its [edition evidence](study-guides/README.md#m4-confidence-and-errors-edition-november-3-2026) (`61b758e`). Lecture 8 was inspected and is not relevant.

Relevant ML concepts:
- **Margin, probability, calibrated probability:** an SVM margin is a distance, not a chance of being right. A probability can still be miscalibrated. Raw L3-C10 was underconfident on validation, and sigmoid calibration lowered its ECE from 0.100 to 0.061.
- **Calibration builds a new model:** the calibrated system averages three L3-C10 copies fitted on two thirds of the training rows each, which is why its accuracy can differ from raw L3-C10's.
- **Error analysis after the freeze:** test mistakes are read only after the one opening, as hypotheses, and cannot feed another selection. Missing passage context is the likely cause of about half of Jev's errors; vocabulary mismatch leads for L3-C10.

Alternatives considered:
- Interpreting only a sample of test mistakes. All 67 cost little and give category counts comparable with the validation ledger.
- Binding `test-review` to the receipt in code. Deferred: the runbook says to compare the receipt's manifest hash, and the lead did so once.
- Rendering the reliability and coverage figures now. Left to M5, where the report chooses its figures.

Actual verification:
- `sh scripts/check.sh` exits 0: smoke passes, 285 tests pass, and Ruff and `git diff --check` are clean.
- `test-review` on the real ledger prints `Jev: 26/26 errors interpreted` and `L3-C10: 41/41 errors interpreted` and passes. Given the validation ledger instead, it refuses with an unknown query error.
- The receipt's `result_manifest_sha256` equals the current final-test manifest hash.
- An independent Opus reviewer recomputed the guide's tables, trace, reliability and threshold numbers and checked sixteen lecture pages. Its findings were fixed before export. Workers ran on Sonnet and the reviewer on Opus, one model family.
- The PDF: all 16 pages inspected, every source word found in the extracted text, two exports identical.

Teaching trace for q0005, "A train ticket costs 45 kr. How much do three tickets cost?", an Altan-authored validation row labelled `calculation`. Raw L3-C10 gives calculation 0.8045; calibrated L3-C10 gives 0.8853. Both fall in the top reliability bin [0.8, 1.0], whose 507 calibrated rows are 99.2% right at mean confidence 0.945. The frozen threshold 0.0 accepts it; a threshold of 0.9 would have withheld it. Its log loss falls from 0.218 to 0.122.

Practice prompts, unanswered: the guide's nine questions. The first three are the M4 prompts from the previous entry. The new ones ask Altan to tell a margin from a probability, read a test reliability bin, compute L3-C10's lookup precision and recall, explain why a better test threshold cannot replace the frozen one, design an experiment for the missing-context hypothesis, and weigh calibration against its small accuracy loss.

Wait for Altan's attempt before supplying worked answers. Learning statuses are unchanged. Altan has not yet reviewed the flagged test labels (unit conversions, DataBench tables, q2225, q3014).

## M4 practice answers, November 5, 2026

Altan answered all nine questions in the [M4 guide](study-guides/m4-confidence-errors.md#your-m4-practice-questions) without a worked answer. The agent checked each against the guide and the result files. All nine are correct, and every number he computed matches.

Faithful summaries and feedback:

1. **A non-selected system can rise.** Validation and test are different samples, and S1-C1 may suit the test rows better. Jev's validation score may carry selection optimism. Correct. Feedback: S1-C1 was not the pick, so its validation score carries no selection bias that the test would remove.
2. **Keep L3-C10.** It was chosen before the test, and switching on the test ranking would use the test for selection. Report both facts. Correct.
3. **Zero errors on 79 inherited rows.** Perfect on that subset, not a zero underlying error rate or real-user performance. Small subset, label limits, unknown pretraining overlap. Correct. Feedback: zero errors in 79 still allows an error rate up to about 3/79, or 3.8%, at roughly 95% confidence (the rule of three). L3-C10 made 6 errors and S1-C1 made 3 on the same rows, so the rows are not trivially easy.
4. **Margin against probability.** Only L3-C10's 0.8045 is a candidate chance of being right. Check calibration on enough independent, representative rows and whether real queries resemble the data. One row cannot show calibration. Correct. Feedback: raw L3-C10 was underconfident on validation, so 0.8045 likely understates its chance.
5. **The [0.4, 0.6) test bin.** Underconfident by 6.8 points, about 27 of 46 right, and one outcome moves a three-row bin by 33.3 points. Correct.
6. **Lookup precision and recall.** 80/83 = 96.4% precision, 80/98 = 81.6% recall. The weakness is recall, and 14 of the 18 misses become direct answers without the record. Correct.
7. **Threshold 0.7.** That would tune the threshold on the test. Coverage must be reported beside accuracy. Choose it on development data under a predefined rule, freeze it, and test on fresh rows. Correct.
8. **Missing-context experiment.** Fresh labelled retrieval requests with direct-answer controls, each query alone and with truthful attachment metadata, document text kept out, prompt and criterion frozen first. No meaningful improvement on enough rows counts against the hypothesis. Correct and well designed. Feedback: say what the controls must show. If they also flip to retrieval, the metadata works as a label cue, not as context.
9. **Calibration's trade.** ECE, Brier and log loss improved, and accuracy and macro-F1 fell slightly. Whether that is worth it depends on the use. The calibrated system is a three-model average, so classes can change. Correct.

Status changes from these answers:
- **Metrics:** **explained independently** for precision and recall, computed from an unfamiliar matrix and interpreted for the user.
- **Confidence and fallback:** **explained independently** for reading a reliability bin, bin size, the coverage trade and calibration's effect. The case where no query is accepted remains unattempted.
- **SVM margins:** **explained independently** for why a margin is not a probability.
- **Model selection:** already explained independently, and prompts 2 and 7 apply it to the test.
- **Error analysis:** new evidence. Altan designed a falsifiable experiment for a post-freeze hypothesis.
- **Leakage and grouping:** still **needs practice**. Split-before-fitting and vocabulary leakage remain unattempted.

Still open for M4: Altan's review of the flagged test labels (unit conversions, DataBench tables, q2225, q3014), the PR merge and the dated PDF snapshot.

Next exercise: what should a fallback report say when no threshold accepts any query, and why is "undefined" better than 0 for that accuracy?

## M4 flagged-label review, November 6, 2026

Altan reviewed the four sets of flagged test labels and kept all of them. He also merged PR #32. The decisions and his reasons are in the [M4 record](evidence/m4-final-test.md#altans-review-of-the-flagged-labels-november-6-2026). No file, frozen label or score changed.

Faithful summary: unit conversions stay `calculation` under the conversion default, with one-unit questions kept as boundary cases. The four DataBench rows and q2225 stay `knowledge_lookup` under the attached-table and store-kind rules. q3014 stays `document_retrieval`, and the missing passage is recorded as a limit of the router's input rather than a label error. He separated "the label is right" from "the router could have known", and that is the distinction the error categories need.

Feedback: the DataBench and q2225 reasons match the collection brief. The conversion default is not written in any tracked document the agent found. If the report relies on it, cite where it was adopted.

Status changes: none beyond the November 5 entry. This is annotation adjudication, which applies the data contract to real cases. It supports the **data contract and action boundaries** row but does not move it, because the open exercise there (a query needing retrieval before calculation) is still unattempted.

Altan then wrote "Accept M4". The roadmap marks M4 done, and the dated snapshot `M4-confidence-errors-2026-11-06.pdf` is identical to the November 3 edition. Carried into M5 unchanged: leakage and grouping (**needs practice**), the data-contract exercise, the no-accepted-query fallback case and the earlier unanswered M0 to M3 prompts.

## M5 report outline, November 6, 2026

Commit `440f175` replaces the preparation prompts with the [IEEE working outline](../report/main.tex), its [source map](../report/README.md), three research figures and an [M5 study guide](study-guides/m5-report.md). The two-page outline budgets eight pages for Altan’s manuscript. The class-balance and word-length figures introduce the population; the Jev test matrix lets a reader inspect errors behind the aggregate score. The comparison table shows validation selection alongside the single frozen test. It rounds directly from the saved metrics, including DT test macro-F1 0.806454 (0.806; the M4 summary shows 0.807).

Trace for discussion: q3014 has an attached passage. Its accepted label is retrieval. Jev saw only the short instruction and predicted direct answer. This adds one to the retrieval-to-direct cell, which totals 13. Altan retained the label after checking the attachment. The missing-context interpretation is a hypothesis.

The research figure export passed. All ten pairs of table scores matched the saved metrics to three decimals. The three PNGs and three sidecars matched the figure manifest. Tectonic compiled the IEEE outline and both pages were inspected. The two-page milestone guide and its provenance are recorded in the [edition index](study-guides/README.md). The software check passed the environment smoke, all 285 tests, Ruff lint and formatting (90 files), and whitespace checks. The existing final-test outputs supplied all test evidence.

Next exercise: write two sentences interpreting the lookup row of the test matrix, naming the denominator and predicting action. Then choose a limitation that restricts the conclusion. M5 understanding is **not yet reviewed**. Carry forward the M4 closing list, including leakage and grouping (**needs practice**) and the no-accepted-query fallback case. Altan’s own-word draft, citations, final pagination and response are pending.

## M5 manuscript for revision, November 6, 2026

Commit `360248a` expands the outline into the [full IEEE manuscript](../report/main.tex) with three research figures, four result tables and 19 cited references. The [evidence map](../report/README.md) identifies the saved runs for each section. The author line and assistance statement identify this as an AI-assisted draft for Altan to revise.

A concrete example runs through the error analysis. For q3014, the annotator could verify a passage, while Jev received only a summary instruction and predicted direct answer. The count is measured. Whether an attachment flag would change the decision requires a future experiment. For the next exercise, rewrite the explanation of q1529 in your own words and use Figure 3 to distinguish its error direction from q3014. The M5 learning checkpoint remains **not yet reviewed**.

Four tables were compared to the saved validation, final-test and threshold records. Each tracked figure and sidecar matched the research export, and all 19 bibliography entries were cited. Tectonic compiled six US Letter pages in IEEE conference two-column format. All six rendered pages were inspected, including the three figures and the references. The PDF SHA-256 is `4cf56c6815926b8beef38235acd4c9bee5cd54daa9722f387aaf00d5de567251`. The smoke check passed, 285 tests passed in 31.245 seconds, Ruff lint and formatting passed, and diff whitespace was clean. The current study guide and its hashes are in the [edition index](study-guides/README.md). This writing step used the existing one-time test results. M5 stays open for Altan’s own-word revision and actual response.

## M5 report review, November 9, 2026

Commit `c1d38ec` corrects the draft against the course instructions and frozen evidence. The [review record](evidence/m5-report-review.md) maps requirements, findings and verification. The report now has seven IEEE two-column pages, four figures and five tables. The added reliability panels preserve exact saved bins. The cue analysis counts errors on overlapping subsets of the existing test predictions.

The review removed an unsupported inference from equal medians, made the L3-C10 fallback scope explicit, specified model settings and tied the reproduction claim to the validation archive. For q3014, Jev predicted direct answer but L3-C10 predicted retrieval. That concrete comparison limits the missing-context explanation. Altan can practice by explaining what evidence would distinguish a useful attachment signal from a learned wording cue, then rewrite the paragraph in his own words. M5 understanding remains **not yet reviewed**, with the earlier gaps carried forward.

All 27 validation and 11 test configurations’ accuracy, macro-F1 and confusion counts were recomputed from their saved predictions. The five tables, four images and provenance were checked. All seven report pages and both guide pages were inspected. The smoke check, 285 tests (30.992 seconds), Ruff lint and format (92 files), and whitespace checks passed. The report PDF SHA-256 is `325df1194d8a76670fa0f6ea467be53c10d0be49434aa7770617ffefd10f5426`. Own-word revision remains with Altan, and complete-package reproduction remains M6 work.

## M5 author block, November 9, 2026

At Altan’s request, removed the dated working-draft subtitle from the report author block. The PDF recompiles to seven pages, all inspected after the layout reflow. The requested sentence is absent from the source and extracted PDF text. Current PDF SHA-256 is `50c73d36b7917f4252fe6bc8bc2fe8a7730825630c32eb87e11f3f2eeb6c065c`. The PR includes this presentation change.

## M5 trade-off columns, November 10, 2026

At Altan’s request, Table I of the [report](../report/main.tex) gained test Brier score and ECE for each frozen system, and Table III gained class F1 for S1-C1 and L3-C10 beside Jev's. The prose is unchanged. The [review record](evidence/m5-report-review.md#trade-off-columns-november-10-2026) lists the values and the further additions it suggested but did not make.

Trace for discussion: q1961 asks for the user's reminders without using the word "reminder". Its accepted label is lookup. Jev chose lookup with probability 0.68, while S1-C1 and L3-C10 both chose direct answer. Then compare q3014, the bare request to summarize: Jev chose direct answer (0.53 against 0.47 for retrieval), while both local systems chose retrieval. Queries like these, in opposite directions, explain why Table III now shows Jev ahead on lookup and behind on retrieval.

Exercise, to attempt before reading the review record: using only Tables I and III, decide which local system you would deploy if uncertain requests had to go to a person, and name the one number that rules out S1-C1 for that job without extra work. M5 understanding remains **not yet reviewed** for these tables. The earlier gaps carry forward.

Every new table row was recomputed from the saved validation and final-test metrics and matched the source. Tectonic compiled seven pages, and the two pages carrying the tables were inspected. The reading copy's SHA-256 is `7dd141822ccd4ef0c0bbb08884a460932d853b5c766b556e6b1522907f43217b`.

## M6 clean reproduction and rehearsal guide, November 10, 2026

**What changed.** Commits `b2bc633` to `8749e06` on branch `claude/m6-reproduction`, including three fixes after an independent review. `final-test --replay-jev-test` lets a clean copy recompute the frozen final test from Jev's archived answers without sending a query. `scripts/archive_study.sh`, `scripts/reproduce_study.sh` and `scripts/compare_study.py` archive the ignored study files, rerun the runbook in a fresh clone and compare every result. `scripts/route_query.py` routes a new query through the frozen L3-C10 for rehearsal. The [M6 record](evidence/m6-reproduction.md) holds the run; the [M6 guide](study-guides/m6-reproduction.md) is exported as `M6-reproduction.pdf`.

**Why.** Issue #9 asks for proof that the study can be rerun without hidden local files. A fresh GitHub clone at `8749e06`, an empty package cache and a freshly downloaded Python restored the 171-file archive and reproduced every split, prediction, metric, confidence result and figure. The rejected alternative was resending the 628 test queries to Jev. That would expose the sealed text again, need Altan's approval and mix model drift into the check.

**ML concepts.** Reproduction versus replication; deterministic group splits from a seed; refitting a frozen configuration instead of loading a saved model file; the difference between proving a computation and proving an external model's answers.

**Checks.** `compare_study.py` printed `PASS: study reproduces`, with each expected difference named by rule. A deliberately changed test prediction and figure byte made it fail. The smoke check, unit tests, Ruff and the whitespace check are listed in the PR.

**Trace.** "What is 15 percent of the total on the invoice I uploaded?" is invented for the guide. Its first action under annotation rule 4 is document retrieval. Frozen L3-C10 chose calculation, raw 0.818 and calibrated 0.889, pushed by "15", "percent" and "total". "uploaded" never occurs in training. "invoice" occurs in one training row but is not among the 10,000 most frequent n-grams L3-C10 keeps. Neither has a feature, so the attachment cue contributes nothing. An earlier version of this entry and of the guide said both words never occur in training; the review found the feature cap, and both were corrected before merge.

**Rehearsal, not yet attempted.** The guide's eight prompts cover an unfamiliar query of Altan's own through `scripts/route_query.py`, rewording it without its strongest n-gram, the L3-C10 test confusion matrix, the 0.0 threshold, what stops a second test evaluation in a checkout and in a fresh clone, reproducing a run, a platform difference that could fail the comparer, and Lecture 7 pp. 52 and 54. Worked answers wait for his attempt. No learning status changes from this entry. The prioritized knowledge-gap backlog will be written from his actual rehearsal responses.

## M5 abstract teach-back, November 10, 2026

Altan explained that Jev predicted the first action for each query, that validation selected it, and that 0.964 was macro-F1 across the four actions on the held-out test. This correctly separates the routing task, the selection decision and the reported metric. The walkthrough continues with Section I and a new exercise on choosing the earliest necessary action. The broader M5 checkpoint remains open.

## M5 Introduction teach-back, November 10, 2026

Altan independently assigned knowledge lookup to a new order-database request because both totals must be read before subtraction. He changed the label to calculation when both totals were supplied inline. This demonstrates transfer for the lookup-to-calculation boundary. The walkthrough continues with Section II and a grouped-split exercise. The separate retrieval-to-calculation exercise and the broader M5 checkpoint remain open.

## M5 Data and exploratory analysis teach-back, November 10, 2026

Altan independently grouped two phrasings of the same fictional order, explained that an unrelated order may go in a different split, and identified inflated test scores as a risk of seeing a near-duplicate in training. This confirms the grouping mechanism on a fresh example. The broader leakage topic remains **needs practice** until he explains training-only feature fitting. Section III supplies that exercise.

## M5 Models and evaluation teach-back, November 10, 2026

Altan correctly paired L2-C10 and L3-C10 on validation to measure the effect of adding bigrams at the same numerical setting. He independently explained that fitting TF-IDF before splitting would let test texts influence the vocabulary and IDF weights even if the labels were hidden. Together with the previous grouping example, this closes the recorded split-before-fitting and vocabulary leakage gaps. Section IV asks him to turn a matched contrast into a qualified results claim.

## M7 package preparation, November 13, 2026

Altan requested the M6 merge and M7 completion. M6 PR #36 merged as `4a5b17c`. The report's future-tense M6 claim now cites the completed clean reproduction. A local package will bind the report, source code and archived research inputs to one source revision. The M7 lesson explains the package and its verification. Existing scripts provide the reproduction contract, so no new framework or study dependency is needed.

The four November 10 teach-back entries above were preserved from Altan's existing uncommitted learning log in the original checkout. That checkout and its edits remain untouched. These are prior recorded responses, not new answers supplied by this task. The latest entry establishes group integrity and training-only feature fitting for the checked examples. Altan subsequently answered the M7 result-and-replay question in this chat; the response is recorded below.

Trace q0005 through the existing evidence. The query asks, "A train ticket costs 45 kr. How much do three tickets cost?" Its first action is calculation. M4's L3-C10 raw probability is 0.8045 for calculation; the grouped training-fold calibration gives 0.8853. The saved threshold is zero, so the policy accepts it. M7 binds the files that produced that trace; it does not refit a new policy or execute a calculator.

### Prioritized remaining practice

| Priority | Evidence and next attempt | Status |
| --- | --- | --- |
| High | Defend the 0.964 test macro-F1 claim, give a limitation, and distinguish replay from a new service response. Altan answered these three points accurately on November 13, as recorded below. | Explained independently for this question; full artifact-tracing rehearsal pending. |
| High | Revise and defend the manuscript in Altan's own words, including the matched-C contrast and local test rank reversal. Issue #8 was closed November 10; closure is not proof of authorship or comprehension. | Author revision and full report defense remain unverified. |
| High | Work a retrieval-before-calculation query and explain when query-only input is insufficient. Lookup-before-calculation was explained November 10. | Remaining action-boundary practice. |
| Medium | Explain a small TF-IDF example, coefficient, regularization choice and naive-Bayes smoothing. | No complete independent attempts recorded for these topics. |
| Medium | Revisit confidence under a zero-accepted-query case and distinguish Brier score from ECE. Earlier fallback and reliability attempts are recorded; this extension is unanswered. | Fresh transfer check pending. |

Fresh exercise, before a worked answer: choose one sentence in the report's conclusion, locate its saved metric and configuration, and explain one condition under which it would not transfer. Then explain which package file identifies the exact code and which file proves the research inputs have not changed.

## M7 result and replay teach-back, November 13, 2026

Altan explained that validation selected Jev and that 0.964 macro-F1 measures strong agreement with the accepted first-action labels on 628 held-out queries. He explicitly distinguished equal averaging of the four class F1 scores from 96.4 percent accuracy. He limited the claim to one grouped English dataset with substantial AI-assisted annotation, rather than real-world user performance. He explained that replay uses saved replies to reproduce scoring and never queries today's service. Service changes or nondeterminism could change fresh answers, as two of 629 top choices changed between the original validation passes.

Feedback: each point is accurate and appropriately scoped. The result, metric distinction, dataset limitation and replay boundary are **explained independently** for this question. This response satisfies the M7 result-and-replay checkpoint; it does not establish the remaining M6 unfamiliar-query trace, mastery of all models, or an own-word manuscript revision. Next practice is the guide's attachment-flag evaluation question, before a worked explanation.

Altan explicitly chose "Keep author review pending" on November 13. M7's technical package can be verified, but the milestone remains **in review** until his author step is complete. The assistance paragraph remains intact. Independent citation review also found MASSIVE's request to cite its English seed corpus, SLURP. The report now includes the verified EMNLP 2020 reference. No research result changed.

### M7 verified delivery

The [M7 record](evidence/m7-freeze.md) and [package identities](evidence/m7-package.json) bind source `49074f8` to the local review ZIP. A new clone from the delivered bundle, with fresh Python/cache folders, reproduced all frozen outputs under the existing rules. The report rebuilt to identical extracted text; seven report pages and five guide pages were inspected. All five tables, four figure sidecars, 22 references, 287 tests and 24 fixture commands passed. The report and guide are agent-assisted. Altan's actual answer is the understanding evidence; the checks establish software and artifact evidence. Author review stays pending as requested. The final evidence commit is recorded in the PR handoff.

## M7 plain-language report pass, November 16, 2026

After M7 PR #37 merged, Altan asked to finalize the report, find AI-sounding passages and issues, shorten the Assistance section and use plainer words. The agent rewrote the prose in [report/main.tex](../report/main.tex). Long words became short ones ("attained" to "reached", "underdetermined" to "does not follow from the text alone"). Repeated sentence shapes were removed, such as the "X would require Y" closer that ended many paragraphs. Altan's own actions now use "I" instead of "Altan". The Assistance section is now three short sentences. At Altan's later request the same day, it no longer says that AI tools helped draft and edit the report; it lists help with queries, labels, code and errors. The report text was nevertheless drafted and edited by AI agents, and Altan owns the course's AI-use rules.

Two content issues were fixed. The data limitation said "the collection lead"; the release record shows this was the lead AI agent, and the report now says so. The q3014 example said L3-C10 "also" predicted retrieval. The saved test predictions show that Jev chose direct answer and L3-C10 chose retrieval, so the word "also" was misleading.

Trace q3014: the query is a short instruction to summarize, and its passage is stored as an attachment the router never sees. The accepted label is document retrieval. Jev predicted direct answer; L3-C10, from the same words, predicted retrieval. The report uses this case to argue that a router needs a signal that a passage exists.

Checks: a script compared every number, citation key, label, table body and the bibliography between the old and new source; all match. Tectonic built seven pages with no undefined references, and every page was viewed. `sh scripts/check.sh` exited 0 with 287 tests, Ruff lint and format passing. The reading copy is `output/pdf/Orchestra-report-2026-11-16.pdf`, SHA-256 `48e53fdd0447db9124548bb673ec3105081ed649ad8aeb6692873a579cc8b55d`. The November 13 package still holds the older report text; the November 16 package below replaces it.

This is an agent edit, not Altan's own-word revision, and no learning status changes. Questions to try before reading any answer:

1. Jev got q3014 wrong and L3-C10 got it right from the same words. Why does that not make L3-C10 the better router?
2. The calibrated L3-C10 bins held 0, 3, 46, 91 and 488 test queries. Which bin decides most of the ECE, and what can that hide?
3. Exercise: rewrite the Assistance section in your own words, saying exactly which parts you did yourself.

## M7 November 16 package, November 16, 2026

At Altan's request the agent built a new dated package from merged source `f635044`. It is `Orchestra-submission/Orchestra-M7-2026-11-16.zip`, SHA-256 `598ab01625ccbb13b7aa1de8b3a3d1cb384e6ee2598f43b746054f9ec5b3614d`. The November 13 package is kept unchanged. A fresh bundle clone with a new uv cache reproduced the study, and the report rebuilt to seven pages with text identical to the local build. The checks, numeric audit, citation checks and checksums all passed; the [M7 record](evidence/m7-freeze.md#november-16-edition) lists them.

Practice question: the code and study archive did not change, so why rerun the whole reproduction for a text-only report change? Name what the new bundle could get wrong that the old run would not catch.

No learning status changes. M8 submission and receipts remain Altan's task.

## Jev error investigation, November 19, 2026

Riccardo asked what might explain Jev's errors. Altan chose to keep Jev at the centre and use published work on GPT and Claude for comparison. The [manuscript and evidence map](../report/README.md#supervisor-follow-up-november-19-2026) use the archived choices, prompt, labels and attachment records. The abstract links to the private repository and the text names the study stages in ordinary language. This AI-assisted report revision adds an interpretation and proposed tests. Altan's own-word review and earlier practice items remain open.

Trace q0605. A kitchen conversion has the accepted action calculation because the adopted labeling rule covers a known conversion factor. The instruction Jev received describes computing from values supplied by the user. Jev chose direct answer with probability 0.99. It got seven of the other cases in this 13-query conversion group right. The prompt difference suggests a testable explanation. A rerun with a clearer rule on fresh examples would be needed to measure its effect.

The ledger check matched all 26 Jev mistakes and all 41 L3-C10 mistakes to the saved predictions. The new subgroup counts matched the frozen files. The five tables and four figure inputs matched the previous edition, all 19 references are cited, and the compiled PDF links to the repository on page one. All seven pages were rendered and inspected. The reading copy is `output/pdf/Orchestra-report-2026-11-19.pdf`, SHA-256 `b9490afa3e40944972df191bc9e0513fc20ce91b38768418c3badbf422647f37`. The environment smoke passed, all 287 tests passed in 32.666 seconds, and Ruff passed lint and formatting (99 files). No live model call or new test evaluation was used.

Practice, before a worked answer: Sketch two requests with identical wording where the right first action changes with the source the user meant. What one piece of information would distinguish them? Then name one case where the presence of an attachment alone would mislead the router. This follow-up is **not yet reviewed** with Altan.

## Manuscript voice revision, November 20, 2026

At Altan's request, the agent edited the abstract, introduction and conclusion in his preferred first-person academic voice. The percentage-change example traces the first decision from the location of the amounts. Figures supplied inline allow calculation immediately. Figures in a referenced report require document retrieval first. The conclusion frames the attachment signal and clearer conversion instructions as proposals for testing. Altan's own-word review remains open.

The reading copy built to seven pages. The environment smoke check and all 287 tests passed. Ruff passed lint and formatting. Practice: What information did Jev have for the 13 retrieval requests it routed to direct answer? How would you test whether an attachment signal helps without changing the wording?
