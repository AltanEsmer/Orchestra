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

The data-contract row remains **needs practice**. On October 25, Altan explained in his own words how related training/test variants can inflate a score: the grouping-related optimism mechanism is **explained independently** for that question after instruction. The broader leakage/grouping topic remains **needs practice** until split-before-fitting and other leakage controls are attempted. Every other row is **not yet reviewed**. Prioritize the first three rows for the next session.

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
