# M6: clean reproduction and oral rehearsal

Study guide edition: November 10, 2026. The evidence is the [M6 reproduction record](../evidence/m6-reproduction.md). A fresh clone of commit `ad65169` from GitHub restored the study archive `orchestra-study-m6.zip` (SHA-256 `38a3ab56…`) and reran the study from the frozen release to the report figures. Every split, prediction, metric and figure matched the saved originals. The project is course project 13, Learning to Route Queries in AI Systems. This guide follows on from the [M4 guide](m4-confidence-errors.md) and the [M5 writing guide](m5-report.md).

## What you need to defend

M6 asks one question. Could someone else rebuild your results from what you hand in, without your laptop's hidden files? The answer has two parts. The archive keeps the data and saved outputs that Git does not hold. A clean run proves the code and the archive together produce the same numbers again.

You should be able to explain five things. What was archived and why it lives outside Git. What the clean run repeated, step by step. What "the same result" means for each kind of file, and which differences are expected. Why Jev was replayed instead of asked again. What a reproduction cannot prove.

M6 changes no result. The selected system is still Jev, with test macro-F1 0.9636. S1-C1 still scores 0.9454 and L3-C10 0.9279. The reproduction recomputed these numbers from scratch and they matched to every saved digit.

## Reproduction in plain words

Three words get mixed up, so keep them apart.

1. **Integrity.** A restored file has the same bytes as the file you archived. The `restore` command checks every file's SHA-256 against the archive manifest. This proves nothing was lost or changed in storage. It does not prove the files can be recomputed.
2. **Reproduction.** The same code and the same inputs, run again, give the same outputs. This is what M6 tests. It needs the code, the locked environment, the archived inputs and a script that runs the documented commands.
3. **Replication.** New data or a new team reaches the same conclusion. M6 does not do this. A larger or different set of real user queries would be a replication.

A reproduction is only as strong as what it leaves out. If the clean run had quietly read a file from the old checkout, the check would be worthless. That is why the run starts from a fresh clone of GitHub, with an empty package cache and a freshly downloaded Python.

## What was archived and why

Git holds the code, the configurations, the split manifest and the report source. It does not hold the data rows or the results, because `.gitignore` excludes `data/processed/`, `data/raw/` and `results/`. Those files carry query text from public sources and from your own pilot, and some carry the sealed test. They stay local.

`scripts/archive_study.sh` packs 171 files into one ZIP of 5,382,029 bytes. They fall into two groups.

- **Inputs the rerun starts from.** The frozen release `m3-5-v1.jsonl` (3,145 rows), its parent `m3-v1.jsonl`, the review ledger, the request types and close-pair decisions used by `check-collection`, Jev's validation and test answer logs, and the two interpretation ledgers. These are human or API evidence. Code cannot recreate them.
- **Saved outputs to compare against.** The prepared configs, the three split files, run `m3-5-full-a`, its selection and error report, the confidence analysis, the freeze, the final test with its receipt, and the full figure export.

The archive tool refuses PDFs, `.env` files and private keys, so no course slide or secret can enter it. It records each file's hash and permission bits in a manifest inside the ZIP.

## What the clean run did

`scripts/reproduce_study.sh` runs inside the fresh clone. It refuses to start if the checkout has changes or saved results. It then runs the commands from the [experiment runbook](../run-experiments.md) in order.

| Step | Command | What it checks |
| --- | --- | --- |
| 1 | `uv sync --locked`, smoke check | The environment matches `uv.lock`; downloads the 21 locked packages. |
| 2 | `restore` | Every archived file's hash; writes the originals to `work/m6-reproduction/original`. |
| 3 | `validate_dataset.py --ready`, `check-collection` | The release still passes its data gates: 3,145 accepted and reviewed rows. |
| 4 | `prepare-study` | Rebuilds the split from the release and seed 42. The tracked manifest must come out byte-identical. |
| 5 | `run_experiment.sh --run-id m6-repro` | Refits all 26 local configurations and replays Jev's validation log. |
| 6 | `select`, `report` | Validation-only selection and the error list. |
| 7 | `confidence`, `freeze` | Calibration on training folds, threshold choice, and the frozen decision set. |
| 8 | `final-test --replay-jev-test` | The frozen systems on the 628 test rows, Jev from its archived test log. |
| 9 | `test-review`, `figures` | The test-mistake ledger still matches; all figures redrawn. |
| 10 | `report/plot_reliability.py` | The report's reliability panel redrawn from its sidecar. |
| 11 | `compare_study.py` | Every result file against the archived original. |

The whole run took 96.5 seconds of wall time on one CPU thread per process.

## What matched, and what was allowed to differ

`scripts/compare_study.py` compares each original file with its reproduced copy. It uses three rules. Split files and images must be byte-identical. JSON results must have identical content once the folder path and run ID are mapped. The run itself uses the project's own `compare` command, which allows score differences up to 1e-10.

| Check | Files | Result |
| --- | --- | --- |
| Split (train, validation, sealed test) | 3 | Byte-identical |
| Collection check and prepared configs | 3 | Identical |
| Validation run, all 27 configurations | 1 run | Reproduces |
| Selection and validation errors | 2 | Identical |
| Confidence analysis | 8 | Identical |
| Freeze | 1 | Identical decisions; six expected fields differ |
| Final test, Jev included | 7 | Identical |
| Figure data and 78 PNG and SVG images | 79 | Identical, images byte for byte |
| Figure provenance sidecars | 41 | Identical except hashes of timed files |
| Report figures (three PNGs and the reliability bins) | 4 | Identical |

The expected differences all come from time or from the code version. A run writes its start and end time into `provenance.json`, so any file that hashes it changes hash too. The freeze also records its own time, its git commit and the hashes of the source files. Two source files changed after the November 3 freeze, because M4 added `test-review` and M6 added the replay option. The comparer prints each allowed difference with its reason and a count. Anything else fails the check.

A check is only useful if it can fail. Before trusting it, one test prediction was changed in a copy and one byte of one figure was flipped. The comparer reported both files and failed.

## Why Jev was replayed, not asked again

Jev runs on TypeSafe's servers. Asking it the 628 test questions again would send the sealed test text out a second time, which needs your approval. A new model version could also answer differently. On November 2, a repeat of the validation questions flipped 2 of 629 top choices.

So the reproduction separates two questions. Can the project's computation be rebuilt? Yes. The clean run reads Jev's archived answers, parses them, and recomputes every Jev prediction, metric and confusion count. Would Jev give the same answers today? That is not tested. The replay proves the pipeline from answers to results, not the answers themselves.

`final-test --replay-jev-test` reads the archived log at the path the freeze recorded and allows zero requests. If any test answer were missing, the command would fail instead of sending a query. The result records `jev_test_replayed: true`, so nobody can mistake a replay for a new opening. In your original checkout the receipt for this split is already complete, so a replay there with a different output path is refused. The test cannot be opened a second time by accident.

## Trace one artifact: Jev's 0.9636

Follow the headline number from the report back to its inputs.

1. Table I of the report gives Jev test macro-F1 0.964.
2. That is `macro_f1` for `Jev` in `results/final-test-m3-5/metrics.json`, 0.963646 before rounding.
3. The metric is computed from 628 rows of `predictions.jsonl`, one Jev prediction per test query.
4. Each prediction is the top choice in Jev's answer for that query, read from `results/jev/m3-5-test.jsonl` (SHA-256 `bcdb69f2…`, 628 requests).
5. In the clean run, `final-test --replay-jev-test` read the same log, rebuilt all 628 predictions, and wrote the same metrics file content.

The local systems took the harder path. L3-C10 and S1-C1 were refit from the training rows in a new environment, then predicted the test. Their predictions and probabilities matched exactly. That shows the frozen configurations are a complete description of the models. No saved model file was needed.

## Trace one unfamiliar query

`scripts/route_query.py` routes any new text through the frozen logistic system, L3-C10. It refits the frozen configuration and its calibration exactly as the final test did. To check that claim, route q0005, "A train ticket costs 45 kr. How much do three tickets cost?" It returns raw calculation 0.8045 and calibrated 0.8853, the values saved in the M4 confidence analysis. The tool cannot route Jev, because that would send your query to TypeSafe.

Here is a query written for this guide. It is not in the dataset. Route it with `uv run --locked python scripts/route_query.py "What is 15 percent of the total on the invoice I uploaded?"`. The output, with shortened class names, is below.

```text
             retrieval    lookup   calculation    direct
raw             0.0583    0.0860        0.8183    0.0374
calibrated      0.0181    0.0883        0.8887    0.0048
prediction: calculation, raw and calibrated
fallback threshold 0.0: top calibrated 0.8887, route it
strongest n-grams for calculation (TF-IDF x weight):
  '15' +0.6515, 'percent' +0.4338, 'is 15' +0.4267,
  'total' +0.3576, 'of' +0.2640, 'percent of' +0.2334
words never seen in training: invoice, uploaded
```

**The label.** The total is on a supplied document, so the router must read it before any arithmetic. Annotation guide rule 4 gives `document_retrieval` when a document must be read before calculating from its figures. This is my application of the rule to an invented query, not a reviewed dataset row.

**What the model did.** L3-C10 chose calculation with raw probability 0.818. It turns the query into TF-IDF values for its unigrams and bigrams, multiplies each by a learned weight per class, adds an intercept, and turns the four sums into probabilities with softmax. The strongest pushes toward calculation came from "15", "percent" and "total". A positive weight means the feature was associated with calculation in the training rows.

**Why it failed.** The two words that signal a document, "invoice" and "uploaded", never occur in the 1,888 training rows. They have no feature, so they add nothing. The model cannot see the attachment cue at all. In M4 terms this is vocabulary mismatch on a multi-action query.

**What confidence did.** Calibration raised the wrong answer to 0.889. The frozen fallback threshold is 0.0, so nothing would be held back anyway. A confident mistake on an unseen cue is the case no threshold catches.

## Alternatives that were rejected

- **Resend the test to Jev.** Rejected. It exposes the sealed text again, needs your approval and money, and would mix model drift into a reproduction check.
- **Copy the old checkout instead of cloning.** Rejected. A copy carries ignored files and caches, the hidden state the check must rule out.
- **Compare every file byte for byte.** Rejected. Files that record times or absolute paths can never match. The comparer maps paths, then names each remaining difference and its cause.
- **Put the archive in Git.** Rejected. The rows include public-source text under licences and the sealed test, and you have not approved publishing them.
- **Reproduce M1 to M3 as well.** Not done. The report's results come from the M3.5 release and the M4 test. Earlier milestones have their own archive records.

## Limitations

- **Same machine.** The clean run used the same Mac (Apple M4 Pro, macOS 27.0). Another operating system or CPU could change the last digits of some probabilities, especially XGBoost. Not tested.
- **Jev's answers are not re-derived.** See the replay section.
- **Newer code, older results.** The runs being reproduced were made at earlier commits. The clean run used commit `ad65169`. This shows the code you will hand in still produces the reported results. It does not rerun the exact original code.
- **Inputs are trusted.** The labels, the review ledger and the interpretation ledgers are inputs. Reproduction checks the computation built on them, not whether a label is right.
- **Timing is not compared.** Latency columns depend on the machine's load. They are excluded from every comparison.
- **The report PDF.** The report compiled from the clean clone to seven pages with text identical to the current reading copy. Its bytes differ because the PDF embeds a build date and identifier. Tectonic sits outside the locked environment.

## Report evidence

The report's reproducibility paragraph can now say this. A fresh checkout of the submitted code, with the study archive, reran every step from the frozen data release to the figures. All splits, predictions, metrics and figures matched. Jev's answers were replayed from the archived logs and not re-requested. Cite the [M6 record](../evidence/m6-reproduction.md) for the commit, archive hash and command. Write that paragraph in your own words. Do not claim replication, or that Jev would answer the same today.

<!-- pagebreak -->

## Course connections

The lectures cover how to separate data for training, tuning and testing, and how to measure classifiers. They do not cover reproducibility, seeds, locked environments or calibration. Those are project engineering choices. Say so at the exam instead of stretching a slide.

| Course concept | Source | Project use |
| --- | --- | --- |
| Separate training and test data; the test checks the model | `Lecture5-FundamentalClassificationAlgorithms.pdf` pp. 2 and 5 | The split is rebuilt from the release and seed, byte-identical to the tracked manifest. |
| Training, validation and test sets | `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` p. 52 | Selection on validation, one test opening. Compare the slide's wording about the validation error with rehearsal question 8. |
| Validation tunes parameters; the test set stays independent | Lecture 7 p. 54 | Freeze before test; receipt refuses a second evaluation. Cite the diagram's structure. Its validation arm reads "biased towards the test set", which looks like a slip. |
| Keep the test set truly independent | Lecture 7 p. 53 | The reproduction reads the test only after a fresh freeze. |
| Precision, recall and F1 | Lecture 7 p. 57 | Per-class F1 and macro-F1. Macro-averaging over four classes is a project choice; the slide is binary. |
| Confusion matrix, with recall, precision and accuracy | Lecture 7 p. 56 | Confusion matrices for every frozen system, reproduced exactly. |
| Majority classes dominate when classes are imbalanced | Lecture 7 p. 68 | Why macro-F1 and per-class results, not accuracy alone. |
| Bag of words loses order | `Lecture6-ArtificialNeuralNetworks.pdf` p. 57 | TF-IDF features; bigrams keep a little order. TF-IDF itself is not in the lectures. |
| Start with logistic regression, SVM or boosted trees | Lecture 6 p. 79 | The local systems: L3-C10, S1-C1, XGBoost. |
| SVM cost parameter C | Lecture 5 p. 86 | The C grid for S1. The logistic families use a C of their own, which sets regularization strength. |
| Random forest | Lecture 7 p. 14 | RF-dNone-leaf1 among the frozen systems. |
| Project 13 asks for classifiers, representations, confidence and errors | `CourseProjects.pdf` p. 15 | The whole study. Reproduction is not required by the brief. |
| Own-words IEEE report and code due December 6, 2026 | `ProjectRreportInstructions.pdf` p. 1 | The archive and scripts support the code deliverable. No code-submission format is stated. |

<!-- pagebreak -->

## Technical appendix: commands

Build the archive from the checkout that holds the data, then reproduce in a fresh clone.

```sh
DATA=/Users/altanesmer/Desktop/SM1/AI/Orchestra
ZIP=$DATA/work/m6-reproduction/orchestra-study-m6.zip
scripts/archive_study.sh "$DATA" "$ZIP"
git clone https://github.com/AltanEsmer/Orchestra.git clean
cd clean && git checkout ad651696206b3d573dc5607061c2e8b389786725
scripts/reproduce_study.sh "$ZIP"
```

The evidence run set `UV_CACHE_DIR` and `UV_PYTHON_INSTALL_DIR` to new empty folders, so the 21 packages and Python 3.12.13 were downloaded again. The log is `work/m6-reproduction/clean/work/m6-reproduction/reproduce.log`.

## Technical appendix: identities

| Item | Identity |
| --- | --- |
| Clean clone | GitHub `AltanEsmer/Orchestra` at `ad651696206b3d573dc5607061c2e8b389786725`, no changes |
| Archive | `work/m6-reproduction/orchestra-study-m6.zip`, 171 files, SHA-256 `38a3ab56a2641f313cc21394afd02afdce87bdbebf99a9ebecdca410272bdc6b` |
| Environment | uv 0.11.7, Python 3.12.13, `uv.lock` `13bdff21…`, scikit-learn 1.9.1, NumPy 2.5.3, SciPy 1.18.1, XGBoost 3.4.1, Matplotlib 3.11.2 |
| Machine | macOS 27.0 arm64, Apple M4 Pro, 12 cores; four BLAS and OpenMP thread variables set to 1 |
| Data release | `m3-5-v1.jsonl` `be747dda…`; config `configs/m3-5.json` `2b016c63…`; seed 42 |
| Split | manifest `7aacbc49…`; train `dd3308af…`; validation `0e9dc934…`; test `baab0310…` |
| Jev logs | validation `1f68d2f3…`; test `bcdb69f2…`, 628 requests |
| Freeze | original `e71f5b80…`; reproduced `d48f4605…` (time, commit and code hashes differ) |
| Final test manifest | original `9b9b7f21…`; reproduced `68dce2b2…` (provenance times differ) |

Full values are in the [M6 record](../evidence/m6-reproduction.md).

<!-- pagebreak -->

## Your M6 rehearsal

Answer out loud or in writing before reading any worked explanation. Use the real files and commands. The answers will be recorded in the learning log as you give them.

1. **An unfamiliar query.** Write a query of your own that is not in this guide or the dataset. Before running anything, say its first action, whether L3-C10 will get it right, and roughly how confident it will be. Then run `scripts/route_query.py` on it and compare.
2. **Features and a model.** Using the output from question 1, explain how the TF-IDF values and class weights become the four raw probabilities. Then say what calibration changed and what it did not.
3. **A confusion matrix.** Open `results/m5-figures/final-confusion-L3-C10.png`. Name the class with the lowest recall, the class it is most often confused with, and one kind of query that could cause that.
4. **A confidence result.** The frozen fallback threshold is 0.0. Explain what that means for a deployed router. Then propose a different threshold and say which of your own routed queries it would hold back, and at what cost.
5. **A design choice.** Explain why the final test refuses a second evaluation in your checkout, and why the clean-clone replay is not a second opening. Name the rejected alternative and how it could fail.
6. **Reproduce a run.** Walk through what `scripts/reproduce_study.sh` does in order. Say which step would fail first if someone changed one label in the archived release, and why.
7. **An error or limitation.** Name one thing this reproduction cannot prove about Jev and one experiment that would test it.
8. **A course connection.** Lecture 7 p. 52 says the validation error gives an unbiased estimate. Using p. 54, explain why the validation score of the selected system in this project is likely optimistic.

## Inspected sources

All course files were read on November 10, 2026 from `/Users/altanesmer/Desktop/SM1/AI/`. Page numbers are one-based PDF pages. Every cited page was extracted with `pdftotext`; Lecture 7 pp. 54 and 56 were also rendered and viewed. Lectures 1, 2, 3, 4 and 8 were searched for reproducibility, seeds, calibration, TF-IDF and macro-averaging; no page covers them.

| File | Pages cited | SHA-256 |
| --- | --- | --- |
| `CourseProjects.pdf` | 15 | `d4e98da373cbdcd62f804d2cd0f957bbaa53294205762ba6d1dc04b26b74fdca` |
| `ProjectRreportInstructions.pdf` | 1 | `00ab8140f009f52fd9f552daa61ade6f628bdd1125096d62c54e07f06e1519a5` |
| `Lecture5-FundamentalClassificationAlgorithms.pdf` | 2, 5, 86 | `c2995d1963da118c5b8f599a641a15b2c8ec8102aa61a66fee13a29eeb67980d` |
| `Lecture6-ArtificialNeuralNetworks.pdf` | 57, 79 | `4096ea75c917389ad65c0322bb1e045fcba82154ecde673f7221da3440b7d94d` |
| `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` | 14, 52, 53, 54, 56, 57, 68 | `918f33dc045f3fbbaaae8a33b1a779e9eb7785e8625f1008aa5fc144b49813fd` |
