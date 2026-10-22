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

The data-contract and leakage/grouping rows currently have status **needs practice**, limited to the introductory terminology discussed above. Every other row is **not yet reviewed**. Prioritize the first three rows for the next session.

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
