# M7: the submission freeze

Study guide edition: November 13, 2026. This lesson explains the final package for Orchestra, course project 13. Package filenames, the final commit, verification outputs and complete hashes belong in the M7 evidence record and package manifest. They identify the delivered edition without making this lesson depend on its own checksum.

## What the freeze means

The research decisions are already frozen. M7 collects the code, report and evidence needed to inspect and reproduce them. It changes no accepted label, model setting, selection rule or reported result. M8 records the actual submission and receipt.

The study contains 3,145 English queries. Training has 1,888, validation has 629 and test has 628. Whole scenario or source-item groups stay in one partition. Validation selected Jev from 26 local configurations and one service condition. Its test macro-F1 is 0.963646, rounded to 0.964 in the report. S1-C1 scores 0.945427 and raw L3-C10 scores 0.927873. The stronger local test score does not replace the validation-selected system.

A final package needs more than the PDF. The report explains the study. The code and lockfile describe its computation. The study archive supplies ignored inputs and saved outputs. The manifest identifies the files that were checked together.

The clean M6 run already reproduced the complete analysis on the same Mac. M7 checks the final delivered edition and records its identity. An exact archive checksum establishes file integrity. A successful rerun establishes agreement with saved computation. Neither establishes that every accepted label is correct.

Source: [M6 reproduction record](../evidence/m6-reproduction.md), [report evidence map](../../report/README.md) and [M4 final test](../evidence/m4-final-test.md).

<!-- pagebreak -->

## What each package file contributes

The Git bundle contains the selected branch and the Git objects needed to clone it without GitHub. Its checkout retains the commit identity used by the reproduction scripts. The source ZIP offers the same authored files for reading, but it has no `.git` directory. Run the reproduction from the bundle clone.

The report PDF is the reading copy. The tracked LaTeX source and four research figures allow another compilation. Tectonic is outside `uv.lock`, so the package records its version separately. PDF build metadata can change the PDF bytes even when extracted text agrees.

The unchanged `orchestra-study-m6.zip` contains 171 payload files and an embedded manifest. Its SHA-256 is `38a3ab56a2641f313cc21394afd02afdce87bdbebf99a9ebecdca410272bdc6b`. It supplies the release, review and interpretation ledgers, cached Jev replies, split files and saved results. Code, source notices and report source come from the code snapshot.

The package README explains the environment and rerun command. The final manifest and checksum list identify the code bundle, source ZIP, report and study archive. Keep those files beside the delivered artifacts. Verify their identities before extracting or cloning them.

For a later correction, preserve this package. Commit the change, rebuild affected artifacts, rerun their checks and create a new dated package with a new manifest and checksums.

The study archive includes query text and held-out rows. A local package does not publish it. Source-specific terms remain in `data/manifests/sources.json` and its linked notices. The package excludes credentials, course PDFs and unrelated scratch files.

For scope, `ProjectRreportInstructions.pdf` p. 1 requires an own-word IEEE conference report of 5–12 pages and code by December 6, 2026. It specifies itslearning for the report. It does not establish a code-upload format or an oral date. Altan owns those administrative details.

<!-- pagebreak -->

## Follow q0005 through the frozen system

q0005 is an Altan-authored validation query already quoted in earlier guides: "A train ticket costs 45 kr. How much do three tickets cost?" Its reference action is calculation because the needed values are present.

L3-C10 uses lowercase unigram and bigram TF-IDF features. The training rows determine its vocabulary and inverse-document-frequency weights. Transforming q0005 uses those fixed choices. Logistic regression combines the feature values with learned class weights and an intercept, then converts the class scores into probabilities.

The saved raw probability for calculation is 0.8045. The calibrated probability is 0.8853. The calibration procedure fits sigmoid mappings using three grouped training folds and averages the fitted classifier–calibrator pairs. Those two values are therefore outputs of different fitted procedures, rather than the same score with a universal correction applied.

The routing helper can refit that frozen local system and reproduce the saved validation trace:

```sh
uv run --locked python scripts/route_query.py \
  "A train ticket costs 45 kr. How much do three tickets cost?"
```

A word can occur in training yet remain outside the retained 10,000 features. The helper reports training-row counts for words outside the vocabulary. In this trace, "ticket" never occurs in training, while "kr" occurs in one training row but is absent from the retained vocabulary. A vocabulary omission alone does not tell you which of those explanations applies.

`Lecture6-ArtificialNeuralNetworks.pdf` pp. 57–58 supports the bag-of-words connection and its loss of order. TF-IDF, the feature cap and this calibration procedure are project method choices. Bigrams retain adjacent pairs, not full sentence structure.

Trace evidence: [M6 guide](m6-reproduction.md) and `results/m4-5-validation/predictions.jsonl`. This lesson quotes no test query.

<!-- pagebreak -->

## What the final claims can say

The report compares agreement with accepted first-action labels on one grouped English collection. It does not measure downstream answers or an assistant's ability to execute the selected tools. `CourseProjects.pdf` p. 15 asks for classifier and feature comparisons, confidence and error analysis. Tool integration is optional.

Macro-F1 gives each action equal weight. That choice makes the smaller lookup class visible, but it does not remove uncertainty from its limited test support. `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` p. 57 covers precision, recall and F1. Averaging F1 equally over these four classes is the project's choice.

The confidence result is narrower than a guarantee of safe routing. Calibrating L3-C10 reduces test log loss from 0.245 to 0.229. Its frozen fallback threshold is zero, so every test query is accepted. The experiment does not measure the success or cost of human review after an abstention.

The M6 reproduction rebuilds local models and recomputes Jev results from cached replies. It does not ask the live service again. Two original validation passes changed two of 629 top choices. The service's future answers remain untested.

The comparison checks split and image bytes, structured results and specifically named provenance differences. Timing is excluded. It used the same Mac, so another platform remains unverified. Labels and adjudications remain trusted inputs. AI-review agreement does not establish independent human agreement.

Lecture 7 p. 53 supports keeping the test independent. Reproduction reads the test after rebuilding the frozen decisions. It does not authorize model revisions based on those results. Receipts are local to a checkout, so discipline still matters across copies.

Altan's November 10 teach-backs demonstrate grouped-split reasoning and training-only fitting. Do not downgrade those recorded responses because new exercises remain. On November 13 he also explained the result, macro-F1 versus accuracy, the dataset limitation and the replay boundary accurately. The full M6 rehearsal, own-word report review and unattempted topics remain open.

<!-- pagebreak -->

## Technical appendix: reproduce the delivered code

The following assumes the package files are in the current directory. Check the package manifest and checksum list first. Use an unused directory for `orchestra-repro`.

```sh
git clone --branch codex/m7-freeze \
  orchestra-code.bundle orchestra-repro
cd orchestra-repro
uv python install 3.12.13
scripts/reproduce_study.sh ../orchestra-study-m6.zip
```

The manifest records the expected commit. Compare it with `git rev-parse HEAD` before the run. The script requires a clean checkout, installs locked packages, restores the archive, rebuilds the analysis and runs the comparer. Expected completion is `PASS: study reproduces`. Read the log at `work/m6-reproduction/reproduce.log` if it fails. Do not change saved results to force a pass.

Setup needs Git, uv, network access for uncached packages and, on macOS, the documented OpenMP runtime. Jev replay needs no API key. Empty cache and Python directories are additional evidence-run settings, not defaults supplied by the script.

### Fresh prompts, unanswered

Attempt these before a worked answer is recorded in the learning log.

1. A classmate proposes adding an attachment flag and reporting its score on the archived test. Design an evaluation for that change and justify which observations the classmate can use at each step.
2. Choose one source or action subgroup for a follow-up collection. Specify what new observations would test transfer beyond the present corpus and which alternative explanation would remain.
3. A rerun matches all predictions but reports a different wall time. Propose an investigation that separates the research conclusion from an operational latency claim.

### Inspected course identities

The lead rechecked the cited pages on November 13, 2026. Page numbers count PDF pages from one. Full filenames appear on the preceding pages.

| Source | Pages | SHA-256 |
| --- | --- | --- |
| CourseProjects.pdf | 15 | `d4e98da373cbdcd62f804d2cd0f957bbaa53294205762ba6d1dc04b26b74fdca` |
| ProjectRreportInstructions.pdf | 1 | `00ab8140f009f52fd9f552daa61ade6f628bdd1125096d62c54e07f06e1519a5` |
| Lecture 7 | 53, 57 | `918f33dc045f3fbbaaae8a33b1a779e9eb7785e8625f1008aa5fc144b49813fd` |
| Lecture 6 | 57–58 | `4096ea75c917389ad65c0322bb1e045fcba82154ecde673f7221da3440b7d94d` |

No new slides beyond the previously recorded Lecture 8 were supplied. Package checks and written explanations establish implementation evidence. Learning status changes only after Altan responds.
