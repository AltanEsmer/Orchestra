# Deliver milestones 1, 2, and 3

This plan defines the next implementation for Altan's routing study. It is a documentation deliverable dated October 16, 2026. The user authorized its PR and merge, then required a stop until separate implementation approval. M1 remains in progress. M2 and M3 remain not started.

Read the [methods preview](study-guides/m1-m3-methods-preview.md) for explanations and report or presentation support. Use the [roadmap](../ROADMAP.md) for dates and status, and the [data protocol](data-and-evaluation.md) for scientific rules. The tooling is implemented in PR #16. Follow the [experiment runbook](run-experiments.md) for current setup and commands. Real data, review, permissions, archives, and research runs remain pending.

## Start only after implementation approval

- [x] Record Altan's explicit implementation approval in the learning log. A merged planning PR does not satisfy this box.
- [x] Re-read the current repository instructions, this plan, and the protocol. Preserve unrelated work and verify the GitHub remote.
- [x] Run every README check before changing code. Record the baseline commit and outputs.
- [ ] Execute the delivery units below in dependency order. End each unit with focused checks and a reviewable commit.
- [ ] Keep human annotation, data permissions, and learning evidence truthful. If required evidence is absent, finish independent tooling with fixtures and record the remaining gate.

Use Poteto's bounded investigation, implementation, and independent review workflow. This is a local study, with no recurring automation or fleet of agents. Give writers disjoint files or worktrees. Use a worker for implementation and a separate reviewer for the resulting patch. Keep detailed Conventional Commits. Later implementation PRs stop at merge-ready unless Altan's implementation approval also authorizes their merge.

## Resolve the data decisions without guessing evidence

Apply these proposed defaults after approval. Record any owner correction before collecting rows. The choices below do not modify the current source manifest or freeze guide v1.

| Decision | Planned approach | Evidence required before acceptance |
| --- | --- | --- |
| General-knowledge facts | Treat stable facts with no requested source as `direct_answer`. Use `knowledge_lookup` only for an identified structured source. Exclude unavailable live-information requests. | Pilot boundary cases and an explicit guide-v1 rule. This settles a proposed policy, not an observed pilot finding. |
| Candidate authoring | Preserve the human-authored primary study. The agent may prepare candidate scenarios after implementation approval, but must mark them as agent-generated and keep them separate until human review. | Altan's actual labels and rationales. Never attribute generated rows to `altan-authored`. Record generation details and human edits if candidates are used. |
| Annotation review | Prefer a second human on at least 20% by class plus all ambiguous rows. Use the existing one-week delayed blind self-review alternative if no second human is available. | Original and review labels, reviewer IDs, dates, agreement before adjudication, resolutions, and bias disclosure. Agent agreement cannot satisfy this gate. |
| Dataset rights | Keep the existing license unset until the owner supplies an actual license or explicit study-use permission. Do not infer it from MIT code licensing or implementation approval. | A nonempty, accurate permission record and any redistribution restriction. No external data acquisition or publication is needed. |
| Storage | Keep full queries and review records local under ignored `data/raw/` and `data/processed/`. Track cleared metadata and hashes. | A restorable archive with its path, file list, and checksum. Do not use the unignored `data/annotation/` path for real rows. |
| Learning | Store fresh exercises in the milestone documents. Do not interrupt this planning task with questions. | Actual later responses. Until then, carry the existing knowledge gaps forward. |

Data permissions and human review are real acceptance gates. They need not prevent code work on clearly labeled fixtures after implementation approval. Such work does not complete M1 or produce valid research results. Keep issue #4 open until its evidence exists. A smaller dataset requires a recorded scope decision, never fabricated rows or silent relaxation of counts.

## Deliver the work in five units

The sequence is P1, P2, P3, P4, then P5. These are local plan IDs, not assigned GitHub PR numbers. P1 completes M1's data work, P2 and P3 deliver M2, and P4 and P5 deliver M3. Each unit includes documentation and evidence for its own change. Study PDFs and the recorded learning attempt remain separate milestone closure requirements.

### P1. Accept the pilot and first dataset

Depends on implementation approval. Tracks [M1 issue #4](https://github.com/AltanEsmer/Orchestra/issues/4).

- [ ] Preserve the current validator entry point. Add separate dataset-readiness checks rather than pretending schema validity establishes scientific readiness.
- [ ] Prepare 40 pilot candidates, initially 10 per label. Include two independent scenarios for each protocol boundary and hard negatives with misleading keywords.
- [ ] Record all unresolved and excluded rows with reasons. Review related scenarios globally before assigning group IDs. Cap a group at four rows.
- [ ] Collect the required human labels and blind review. Save raw decisions before adjudication. Report agreement as matching reviewed labels divided by reviewed rows, with the denominator and sampling method.
- [ ] Resolve pilot ambiguity, freeze guide v1, and relabel affected rows under that version.
- [ ] Grow to 120 accepted rows, at least 30 per class and 15 independent groups per class. Mixed-label groups need a recorded review, not automatic separation into different groups.
- [ ] Freeze a collection brief for the expansion to 400 before inspecting M2 model errors. Specify class and boundary coverage, wording diversity, sources, and grouping rules.
- [ ] Save the dataset hash, source permissions, guide version, review ledger, counts, group sizes, length distribution, source mix, and exclusions. Report the primary dataset and challenge rows separately.
- [ ] Archive the local rows and review evidence. Confirm restoration to a different local directory reproduces the hashes and validation report.

Planned files include additions to `scripts/validate_dataset.py` and its tests, `docs/annotation-guide.md`, cleared `data/manifests/` records, and `docs/evidence/m1-data.md`. Local rows belong in `data/raw/pilot-v0.jsonl` and `data/processed/m1-v1.jsonl`. The current source manifest remains unchanged until permission evidence exists.

Acceptance tests must reject an empty training dataset, insufficient accepted counts, missing classes, missing permissions, or missing review evidence. Preserve structural validation for unresolved drafts. Test readiness separately with small fixtures and explicit count requirements. No test may claim to determine semantic label correctness. A live validator run and human review ledger must agree on the released counts.

### P2. Persist splits and protect the test set

Depends on accepted P1 data for research execution. Fixture-based development may proceed while P1 awaits human evidence. Tracks [M2 issue #5](https://github.com/AltanEsmer/Orchestra/issues/5).

- [ ] Move shared validation into `src/orchestra/data.py` when the splitter becomes its second caller. Keep `scripts/validate_dataset.py` as the documented CLI adapter.
- [ ] Add `src/orchestra/splits.py` for split creation, loading, and validation. Pass rows explicitly and avoid global mutable datasets.
- [ ] Add a minimal installable package when introducing `src/orchestra/`. Use `setuptools.build_meta` with a pinned `setuptools` build requirement and editable installation through `uv sync --locked`. This build dependency makes the shared package importable from a fresh checkout. Select and verify its exact version during P2, then pin it before use. Do not use `sys.path` edits or require a manually set `PYTHONPATH`.
- [ ] Sort by stable query ID. Run `StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)` on accepted rows. Assign held-out folds 0, 1, and 2 to training, fold 3 to validation, and fold 4 to test. Do not use its overlapping training indices as separate partitions.
- [ ] Save one immutable split manifest with query IDs, group IDs, dataset hash, seed, algorithm/version, class order, actual counts, and manifest version. Report approximate 60/20/20 proportions.
- [ ] Reject duplicate membership, missing or extra IDs, group overlap, stale hashes, unresolved rows, or a missing class in any partition. Fail visibly if five folds cannot support the accepted groups. Collect more groups rather than searching seeds for a favorable model score.
- [ ] Materialize training and validation inputs separately from sealed test rows. Training commands must load only those two inputs. Keep test text, predictions, errors, and metrics out of logs and report examples until M4.

Sealing is a workflow boundary, not encryption. The data steward sees rows while authoring and splitting. Record that exposure. Developers may check hashes, membership, and aggregate test class counts but must not inspect test content or tune against its results.

Behavioral tests must exercise whole groups with mixed labels, stable membership after input reordering, changed-data rejection, missing classes, and malformed manifests. A CLI integration test must show that a baseline run succeeds without opening the sealed test file. Include a fixture-only held-out token that cannot enter the fitted vocabulary.

### P3. Run and reproduce the two baselines

Depends on P2 and accepted P1 data. Completes M2's executable study work.

- [ ] Add `src/orchestra/experiment.py` for pipeline construction, fitting, validation evaluation, and artifact writing. Add one small `__main__.py` command entry point using standard-library `argparse`.
- [ ] Use JSON configuration and the current scikit-learn dependency. Add no experiment framework, service, database, or paid API.
- [ ] Run B0, the training-majority dummy, and L2 with `C=1`, the unigram TF-IDF logistic model. Fit only on training text and labels.
- [ ] Keep feature extraction inside the scikit-learn pipeline. Never feed IDs, labels, rationale, source, or annotators into features.
- [ ] Persist validation predictions and score columns with explicit class order and score type. Save fixed-label metrics, raw and normalized confusion matrices, warnings, resolved configuration, provenance, and timings.
- [ ] Run both baselines twice in fresh processes with the same frozen inputs. Compare split membership, ordered predictions, and deterministic metrics exactly. Compare numerical scores with an explicit tolerance of `1e-10` on the same environment. Exclude timestamps and timings from equality checks.
- [ ] Inspect at least five validation errors, or all if fewer exist. Include correct examples for comparison. Keep findings as hypotheses and do not rewrite test data from those observations.
- [ ] Restore the archived input and rerun from a clean locked environment on the same host. Preserve all run IDs and explain any difference.

Expected future command interfaces are shown below. They are specifications, not runnable commands today.

```text
uv run --locked python -m orchestra split --config configs/m2.json
uv run --locked python -m orchestra run --config configs/m2.json --run-id m2-a
uv run --locked python -m orchestra run --config configs/m2.json --run-id m2-b
uv run --locked python -m orchestra compare --left results/m2-a --right results/m2-b
```

Contract tests must cover known dummy predictions, held-out vocabulary isolation, literal confusion-matrix counts, zero predicted support, class-score alignment, artifact hashes, refusal to overwrite an existing run, and the two-process reproduction path. Require outputs from the real CLI, beyond unit tests. Routing accuracy has no acceptance threshold.

### P4. Freeze the expanded dataset without moving old groups

Depends on P3. Tracks [M3 issue #6](https://github.com/AltanEsmer/Orchestra/issues/6).

- [ ] Follow the collection brief frozen in P1 to target 400 accepted rows, roughly 100 per class. Apply the same review and permission rules to additions.
- [ ] Review new candidates against all existing scenario families before allocation. Reject undeclared near-duplicates and family links across partitions.
- [ ] Keep the original 120 rows, text hashes, labels, group IDs, and partition assignments immutable. Add only independent new groups to the main study extension. Store related new variants in the challenge collection instead.
- [ ] Allocate the new groups once with the P2 five-fold procedure, then append their membership to the original manifest. Save the parent dataset and manifest hashes.
- [ ] Verify exact preservation of every old membership and hash. Report achieved combined proportions and independent group counts. Do not freshly split all 400 rows.
- [ ] If an old label or family is found wrong, stop the current version. Record the correction and exposure history. Rebuild a named successor protocol if needed, keeping every exposed group out of a new test set. Never silently overwrite M2 evidence.
- [ ] Freeze the main dataset and common split before the comparison. Archive and restore them as in P1.

Tests must reject moved original IDs, changed old content, changed old labels, missing old rows, cross-partition families, and stale parent hashes. A fixture extension must demonstrate that M2 validation can never become M3 test. Report new-data collection bias and author exposure even when these checks pass.

### P5. Compare the 14 configurations and freeze selections

Depends on P4. Completes M3's executable study work.

- [ ] Extend the same runner with the protocol's fixed matrix. Run B0 once, B1 once, and L1, L2, S1, and L3 at each of `C=0.1, 1, 10`. The total is 14, including fresh B0 and L2 results on the expanded dataset.
- [ ] Use one frozen dataset and split for all runs. Save all outcomes, including errors, warnings, and failed attempts. No failed configuration disappears from the comparison table.
- [ ] Resolve convergence warnings before selection. Record every retry and setting change. If a configuration remains unsuccessful, mark M3 incomplete or document an explicit scope amendment.
- [ ] Compare L1 against L2 for weighting, L2 against S1 for classifier choice, and L2 against L3 for phrase features. Show matched-C comparisons alongside each family's tuned result.
- [ ] Select within each family by validation macro-F1. Form the tie set within 0.01 of the best score, then prefer the smallest C. The smaller C is the predeclared stronger-regularization preference.
- [ ] If an overall selection is useful, apply a fixed simplicity order to its tied family winners. Prefer B0, B1, L1, L2, S1, then L3. This order is a project preference for explanation and computation, not a universal complexity theorem. Use measured median prediction latency only if preceding keys tie, then configuration ID.
- [ ] Save `selection.json` with scores, tie candidates, rules, chosen IDs, dataset/split hashes, and run paths. Freeze one selection per family so M4 preserves all required comparisons.
- [ ] Produce class and length figures, a validation comparison table, confusion matrices, and an error note. Inspect at least 20 validation errors, or all if fewer exist. Trace each table and figure to input runs.
- [ ] Hand off selected systems and untouched test manifests to M4. Calibration, threshold choice, and final test evaluation remain M4 work.

The experiment configuration tests must expand to exactly 14 unique required configurations and select from literal metric fixtures, including ties and failed runs. Integration checks must reproduce a saved comparison from archived validation outputs without fitting a model again.

## Fix the model and artifact contracts before coding

Use only query text as input. The proposed shared word token pattern is `(?u)\b\w+\b`, which retains single-character words and digits. Lowercase, preserve negation, use no stop-word list, set `min_df=1`, `max_df=1.0`, and cap features at 10,000. Word tokenization still drops punctuation and does not fully represent signed or decimal numbers. Record that limitation instead of claiming numerical understanding.

Use counts for B1 and L1. Use TF-IDF with `norm="l2"`, `use_idf=True`, `smooth_idf=True`, and `sublinear_tf=False` for L2, S1, and L3. L3 uses `(1, 2)` n-grams. Other word models use `(1, 1)`.

Logistic regression starts with `solver="lbfgs"`, L2 regularization expressed as `l1_ratio=0.0` in pinned scikit-learn 1.9.1, `tol=1e-4`, `max_iter=100`, an intercept, no class weighting, and seed 42. Avoid the deprecated `penalty` argument. On convergence warnings, raise the limit once to 1,000, preserve the failed attempt, and rerun all configurations in that family with the same limit. Unresolved warnings block valid selection.

Use `MultinomialNB(alpha=1.0, force_alpha=True, fit_prior=True)` for B1. Use `LinearSVC` with L2 penalty, squared-hinge loss, `dual="auto"`, one-vs-rest multiclass handling, `tol=1e-4`, `max_iter=1000`, an intercept, no class weighting, and seed 42. A bounded SVM retry uses 10,000 iterations for its whole family. Save SVM margins as margins. Export every estimator's resolved parameters so omitted library defaults remain inspectable.

Each `results/<run-id>/` directory must contain the resolved configuration, provenance, per-configuration outcomes, ordered validation predictions, metrics, confusion matrices, warnings, and timing. Write a manifest last with hashes of completed files. Mark partial or failed runs explicitly and refuse accidental overwrite. Scores record the estimator's class order. Run provenance includes every field required by the [resource protocol](data-and-evaluation.md#reproducibility-and-resource-budget).

Track selected cleared evidence under `docs/evidence/`. Keep full rows, full runs, and trusted local model artifacts outside Git. Record archive locations and checksums in each milestone evidence document. Check the tracked-file list before pushing so a path mistake cannot publish query rows.

## Measure resources before using the GPU allocation

The required 14 sparse configurations use the local CPU and existing scikit-learn environment. No GPU, SDU credentials, paid API, or pretrained-model download is needed for P1 through P5. Altan reports an available SDU allocation of 10 GPU hours. No access, GPU type, availability, or performance has been verified, and no hours have been consumed by this plan.

Measure training time, process peak memory, and end-to-end prediction latency. Use a fixed validation batch, one warm-up, and 30 repetitions with `time.perf_counter`. Report median and 95th percentile, batch size, hardware, and thread limits. Set numerical-library thread limits to one before Python starts. Timing is descriptive, not a statistical proof of one model's superiority.

Use proposed operational ceilings of 15 minutes per sparse configuration and 8 GB peak process memory. These are unverified stop-and-investigate limits, not predicted usage. Record observed values before changing a limit. Run the same fixed fixture on parent and changed versions when measuring runner regressions. Do not compare timings for unlike workloads or invent a parent result where no runner existed.

Reserve all 10 GPU hours unless the optional frozen-embedding extension is accepted after the required matrix. First use the existing 500 MB download and 15-minute CPU-pilot gate. Pin an encoder revision, permission, pooling, dimension, normalization, and dependencies before downloading. If SDU compute becomes useful, report the measured reason and the needed access details, scheduler commands, storage, GPU type, and quota policy. Never request credentials in a document. A proposed ceiling is one GPU hour for the pilot and two more for cached extraction and reruns, leaving seven unallocated. This proposal is not authorization to spend or a runtime estimate. No fine-tuning is planned.

## Produce the milestone explanations alongside the work

- [ ] Maintain editable sources for `M1-data.pdf`, `M2-baselines.pdf`, and `M3-comparison.pdf` under `docs/study-guides/` as the real work lands.
- [ ] Explain what Altan supplied, what the agent authored, what a library computed, and what the evidence actually establishes. Record model/provider details for any generated candidates.
- [ ] Trace one real training or validation query through the implemented milestone. Keep the preview's teaching example out of the research data and keep test examples sealed.
- [ ] Include decisions and rejected alternatives, implemented files, equations with defined symbols, actual commands/results, limitations, report evidence, and unanswered oral exercises.
- [ ] Refresh the relevant lecture mapping using exact filenames, one-based pages, dates, and hashes. Keep project choices distinct from course requirements.
- [ ] Export each PDF outside Git to the existing study folder. Inspect every rendered page and extracted text. Record source commit/hash, PDF hash, export method, page count, and a dated closure snapshot.
- [ ] Maintain a short presentation outline and claim-to-evidence table in each guide. Label M2 and M3 metrics as validation results. Leave confidence and final-test findings empty until M4.
- [ ] Record Altan's actual later learning response separately. Do not fill it on his behalf or mark understanding from document delivery.

## Verify completion and hand off

For every unit, run focused behavior tests and every [README check](../README.md#set-up-and-check-the-environment). Run the real CLI on the intended artifact, inspect its output files, and record resource use where computation changed. Review the exact patch independently before merging an authorized implementation PR. Keep one behavior per commit and include unit, live execution, and resource evidence where applicable.

Close M1 only with the pilot/review/guide/accepted-data evidence. Close M2 only with identical reruns and archived validation outputs. Close M3 only with frozen expansion, all 14 outcomes, resolved failures, and saved per-family selections. Each also needs its inspected PDF and actual learning attempt under the roadmap, or a separately recorded owner exception. Leave missing gates visible.

Report commit and PR links, exact commands and outcomes, dataset/run/archive identities, remaining limitations, and the next learning exercise. The present planning PR ends after its verified merge. Implementation approval is the next action.

## Rationale and deferred alternatives

The Laziness Protocol keeps one runner, JSON configuration, standard-library CLI parsing, and the existing ML stack. A plugin registry, notebook-only experiment, hosted service, and early GPU training add maintenance without answering the research question.

Sequence Work into Verifiable Units separates data acceptance, split protection, reproduction, dataset expansion, and comparison. This keeps each failure attributable. Prove It Works requires saved artifacts and real executions. Passing schema tests cannot establish a correct label, a completed experiment, or exam readiness.

No training prototype ran while preparing this plan. The splitter is a proposed use of an existing library, and its feasibility must be checked on approved data in P2. The project avoids a custom split optimizer, accuracy promises, automatic human-review claims, and test-driven model selection.

Official references checked on October 16, 2026 support the proposed mechanisms. Group stratification preserves groups but may only approximate class balance, as described in [StratifiedGroupKFold](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.StratifiedGroupKFold.html). Pipeline isolation follows [scikit-learn leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html). Resolved settings must match [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) and [TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html) in the locked version. Local signature inspection confirmed the 1.9.1 logistic penalty deprecation during planning.
