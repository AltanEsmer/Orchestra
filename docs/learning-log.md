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

No specific ML misconception has been established. The first response shows that routing and split terminology needs an introduction before further teach-back questions. Ability to explain the scaffold, taxonomy, preprocessing, and evaluation remains unverified. Course AI-use and oral-exam rules remain unconfirmed administrative questions.

By November 29, rehearse with an unfamiliar query, an actual saved model/configuration, a confusion matrix, and a confidence result. Altan must trace the query through preprocessing and prediction, explain a model and its features, interpret the results, justify one design choice, reproduce a run, and discuss an error or limitation. Record each attempt and revisit weak topics before the December 4 freeze. The rehearsal is planned; no oral readiness has been certified.
