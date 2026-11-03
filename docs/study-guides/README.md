# Milestone study guides

These guides help Altan explain what Orchestra implements, why each choice was made, and how course concepts apply. They supply traceable material for the December report and practice for the January oral exam. They do not establish understanding without Altan's own responses.

The [M1 to M3 methods preview](m1-m3-methods-preview.md) explains the proposed study before implementation. It accompanies the [delivery plan](../m1-m3-plan.md), with report and presentation evidence to collect and unanswered practice prompts. It is historical Markdown planning material, not a delivered M1, M2, or M3 PDF or a completion record. Implementation is now covered by the [repository walkthrough](../repo-guide.md), [automation evidence](../evidence/automation-completion.md), and [manual guide](../manual-steps.md); those do not establish student understanding.

## Files and editions

Keep editable Markdown sources in this directory. Export PDFs to `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/`. Course slides stay in `/Users/altanesmer/Desktop/SM1/AI/` and outside Git. Generated study PDFs also remain outside Git.

Use a stable filename such as `M0-preparation.pdf` for the current edition. At milestone closure, retain `M0-preparation-YYYY-MM-DD.pdf`; add a revision suffix if a same-day snapshot already exists. Do not overwrite a closed-milestone snapshot. Record the PDF checksum, source checksum, source commit, export date, and validation here. Archive these external PDFs with the final project materials. The Markdown is sufficient to reauthor an edition if a local PDF is lost; identical PDF bytes are not guaranteed.

## Update a guide

1. Read the milestone's actual changes and saved evidence. Inspect relevant lecture files currently available in the course folder.
2. Update the lesson and technical appendix. Explain one input through the current implementation. Mark planned behavior and unmeasured results explicitly.
3. Map each course concept to an actual code choice, result, limitation, or explicitly planned later milestone. Cite exact source filenames and one-based PDF pages; record the source hashes and review date.
4. Add report evidence and fresh oral questions. Wait for Altan's attempt before giving worked answers to those practice questions. Record feedback and status in the [learning log](../learning-log.md).
5. Export the source with the PDF workflow. The Codex bundled authoring runtime provides ReportLab and PDF inspection tools; it is separate from Orchestra's locked experiment environment. No PDF dependency is added to `pyproject.toml`.
6. Inspect every rendered page and extracted text. Check code, equations, tables, page breaks, citations, and source-to-PDF completeness. Record edition evidence below. Update the stable PDF after meaningful work; preserve the dated edition when closing the milestone.

## Coverage across milestones

The [roadmap](../../ROADMAP.md) owns dates and statuses. Each milestone's existing acceptance criteria also require its updated PDF and a recorded learning attempt with remaining gaps visible.

| Milestone | Guide focus and report use |
| --- | --- |
| M0 | Project contract, environment, TF-IDF smoke flow, library ownership, evidence limits. Supplies introductory scope and reproducibility context. |
| M1 | Labels, provenance, ambiguous examples, annotation review, class and group distribution. Supplies the data section. |
| M2 | Validator, group splits, dummy and logistic baselines, fit versus transform, saved runs. Supplies methods and initial validation evidence. |
| M3 | Classifier assumptions, count versus TF-IDF, regularization, controlled comparisons, selection. Supplies the main methods and comparison results. |
| M3.5 | Public-data scale and source quality; single trees, bagged forests, boosted trees and Jev; matched-split comparison, costs and reproducibility. [M3.5 data and methods](m3-5-data-and-methods.md), exported as `M3.5-data-and-methods.pdf` on November 3, 2026. |
| M4 | Confidence, calibration, errors, test freeze, uncertainty and limitations. Supplies confidence analysis and final findings. [M4 confidence and errors](m4-confidence-errors.md), exported as `M4-confidence-errors.pdf` on November 3, 2026. |
| M5 | Claim-to-evidence map, figures, sources, methods and limitations in the report. Supports Altan's own synthesis. |
| M6 | Clean reproduction and recorded oral attempts using real project artifacts. Explains reproducibility and remaining gaps. |
| M7 | Frozen package, versions, checksums and evidence supporting final claims. Records what is ready for submission. |
| M8 | Submitted artifact identities and receipts. Records exactly what was submitted. |

After submission, add dated practice entries to the learning log through January 2027. Refresh the guides for newly relevant lectures and explanations without silently changing the submitted study or its findings.

## Edition evidence

M0 edition exported on October 8, 2026. The guide is delivered; the introductory learning response remains pending, so this is not a closed-milestone snapshot.

- Editable source: [M0 preparation](m0-preparation.md).
- PDF: `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/M0-preparation.pdf`, 10 pages.
- Baseline implementation commit: `0350a8e7cfa080b236caeb999e6eff3853c54f28`. Guide source commit: `22f445e08ea322ccb99a78d77fd9e04157030e26`.
- Source SHA-256: `91c27e80834cd01632de2efd0bc7d20027072b4d09eb1d512f3c810e68455684`.
- PDF SHA-256: `3c321a3b3be63f638fe9a16455926be78662b60e776cf0dccfb661a2b841ce07`.
- Provenance sidecar: `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/M0-preparation.manifest.json`.
- Verification: all 10 rendered pages inspected by the author and lead; the source text was checked against PDF text extraction. The author checked the numerical walkthrough in the locked project environment. Two consecutive exports produced identical hashes.
- Authoring: Codex bundled ReportLab, with a local one-shot exporter at ignored `work/m0-pdf/export.py`. This helper is a convenience for this checkout, not an experiment dependency or a prerequisite for understanding the source. Future editions can be exported from the tracked Markdown through the PDF workflow.

Closure snapshot: Altan closed M0 on October 16, 2026. The stable PDF was copied to `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/M0-preparation-2026-10-16.pdf` with SHA-256 `3c321a3b3be63f638fe9a16455926be78662b60e776cf0dccfb661a2b841ce07`, identical to the October 8 edition. The learning checkpoint was not answered before closure and carries into M1.

M1 and M2 editions exported on October 28, 2026. Both guides are delivered. Altan's learning attempts on their checkpoints are still pending, so neither is a closed-milestone snapshot yet.

| Edition | Source | PDF, 13 pages each | Source SHA-256 | PDF SHA-256 |
| --- | --- | --- | --- | --- |
| M1 | [M1 dataset](m1-dataset.md) | `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/M1-dataset.pdf` | `82e8ed8c805e8a3d82fd585c7ec57e7868c9ea3e59aaadcd7f5b2ef5bafa0834` | `57d822a0ba45d49716c3c2313d3f0bccd4669de5be69668dd75ca7775f73f6bc` |
| M2 | [M2 baselines](m2-baselines.md) | `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/M2-baselines.pdf` | `1d1289bef6ecfc02902eb31ad0adc50c1e9d450287890ffad763d404ac6dd552` | `a07f6c921ba1f6f6c54ce9d00b2ee008bdda87253485756abebc4d1feba71016` |

- Provenance sidecars sit beside each PDF as `M1-dataset.manifest.json` and `M2-baselines.manifest.json`. They record the source and PDF hashes, the page count, the repository commit at export (`07263b4`) and the hash of every cited course PDF.
- Drafting: two agent subagents each drafted one source from the tracked evidence and the local data. The lead checked the cited numbers, group IDs, quoted learning-log phrases and a sample of slide pages against the files.
- Trace check: the M2 guide's q0005 trace comes from a refit of the exact L2 configuration on the training file. All 25 refit predictions and all 100 probabilities equal the saved `m2-a` values.
- Verification: the lead inspected all 26 rendered pages. A scripted check confirmed that every word and every full hash in each source appears in the extracted PDF text. Code-fence language tags are not rendered. Two consecutive exports produced identical hashes.
- Authoring: the export used ReportLab 5.1.0 and pypdf 6.21.3 in a throwaway `uv run --no-project` environment, through the ignored local exporter `work/study-pdf/export.py`. No PDF dependency was added to `pyproject.toml`.
- Data exposure: both guides quote only Altan-authored rows, which his permission covers for public sharing. The M1 trace row q0036 is a training row and the M2 trace row q0005 is a validation row. No sealed test text appears.

M3 edition exported on October 28, 2026. It is delivered. Altan's learning attempt on its checkpoint is pending, so it is not a closed-milestone snapshot yet.

| Edition | Source | PDF, 16 pages | Source SHA-256 | PDF SHA-256 |
| --- | --- | --- | --- | --- |
| M3 | [M3 comparison](m3-comparison.md) | `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/M3-comparison.pdf` | `660d58f2241a966a764af6a7bf25c5f3cea99e1476405517522bdf5378056e37` | `7840a3e0e7f11b3c03215c041f3b84a43c23dbbacfb49d9dc9381f1760641451` |

- The sidecar `M3-comparison.manifest.json` records the repository commit at export (`9d909a3`) and the hash of every cited course PDF.
- Drafting: an agent subagent drafted the source from the tracked M3 evidence, the code and `comparison.md`, and verified each lecture page it cites with `pdftotext` and rendered images. The lead checked every number against the run record, the F1 fractions and trace sums by hand, the code settings and selection rule against `experiment.py`, the protocol quote, and two cited lecture pages.
- Trace check: the q0005 numbers come from a training-only refit of L1-C10, L2-C1 and B1, whose probabilities equal the saved `m3-a` values.
- Verification: the lead inspected all 16 rendered pages and removed two page breaks that had left near-empty pages. A scripted check found every source word in the extracted text, except tokens that the extractor splits: 64-character hashes that wrap inside table cells, filenames that break at `%20`, and the `C 1` column header. With line breaks removed, each of those appears intact. Code-fence tags are not rendered. Two consecutive exports produced identical hashes.
- Data exposure: the guide quotes only q0005, an Altan-authored validation row the M2 guide already quotes. No other query text and no sealed test text appears.
- The M3 edition also cites `UTF-8''Lecture1-Introduction%20to%20Big%20Data%20Analytics.pdf`, SHA-256 `9f16e0d8d8fc24ca12a4c93e4cca3fcdb26bec5f8a6c80cece83e2ed0ed8e1ee`, which no earlier edition cites.

Inspected course source revisions for the M0 edition. The M1 and M2 editions also cite the two files added below, which were first inspected on October 28, 2026:

| File | SHA-256 |
| --- | --- |
| `CourseProjects.pdf` | `d4e98da373cbdcd62f804d2cd0f957bbaa53294205762ba6d1dc04b26b74fdca` |
| `ProjectRreportInstructions.pdf` | `00ab8140f009f52fd9f552daa61ade6f628bdd1125096d62c54e07f06e1519a5` |
| `Lecture2-Data Preprocessing and Feature Engineering.pdf` | `e7bfec9a9a52954c038e58a84f680e76648efa582ef79acafe2a3bfaa582217f` |
| `Lecture5-FundamentalClassificationAlgorithms.pdf` | `c2995d1963da118c5b8f599a641a15b2c8ec8102aa61a66fee13a29eeb67980d` |
| `Lecture6-ArtificialNeuralNetworks.pdf` | `4096ea75c917389ad65c0322bb1e045fcba82154ecde673f7221da3440b7d94d` |
| `Lecture4-LinearModelsforRegression.pdf` | `8a58746abec856b9168dbca3bd64b446297425570cc78e8c3b378c358d4315cc` |
| `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` | `918f33dc045f3fbbaaae8a33b1a779e9eb7785e8625f1008aa5fc144b49813fd` |

## M3.5 interim screening edition, October 31, 2026

The [editable screening lesson](m3-5-data-screening.md) accompanies the first public-data screen. `M3.5-data-screening.pdf` and its hash manifest are saved in the external study folder. All three pages were rendered and visually checked, with the final question layout rechecked. Lecture 2 PDF page 8 was extracted and visually verified at the hash recorded in the source. This interim edition does not complete the planned `M3.5-data-and-methods.pdf`, data release or model comparison. The evidence remains screening proposals; 400 rows are accepted.

## M3.5 interim group and quota audit, October 31, 2026

The [editable audit lesson](m3-5-group-quota-audit.md) records the follow-up independent-group checks, source/type quotas and remaining diversity gaps. `M3.5-group-and-quota-audit.pdf` and its companion source/PDF hash manifest are in the external study folder. Both pages were rendered and visually checked. The lesson retains the verified Lecture 2 page 8 connection and explicitly separates project caps from course requirements. The earlier screening edition is preserved. This is interim evidence, with 400 accepted rows and all learning questions unanswered; the full methods edition remains future work.

## M3.5 data and methods edition, November 3, 2026

The edition is delivered. Altan answered its practice prompts and accepted M3.5 on November 3, 2026. The closure snapshot `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/M3.5-data-and-methods-2026-11-03.pdf` has SHA-256 `ba8f3a95ab2edf6ebeda9ac85432adaa4fe9edab9a29bf2a47f23c9fd500b494`, identical to the edition.

| Edition | Source | PDF, 18 pages | Source SHA-256 | PDF SHA-256 |
| --- | --- | --- | --- | --- |
| M3.5 | [M3.5 data and methods](m3-5-data-and-methods.md) | `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/M3.5-data-and-methods.pdf` | `c6f3e77b49083226f70dc12b7776a562cb230ec716c89fefc67ce0a66694242b` | `ba8f3a95ab2edf6ebeda9ac85432adaa4fe9edab9a29bf2a47f23c9fd500b494` |

- The sidecar `M3.5-data-and-methods.manifest.json` records the repository commit at export (`2a6baf5`) and the hash of every cited course PDF. All five cited course files are present, and their hashes equal the earlier editions' records.
- Drafting: a Sonnet subagent drafted the source from the M3.5 evidence records, the code and the saved `m3-5-full-a` run, and extracted every lecture page it cites with `pdftotext`. The lead compared the selection scores, family winners and q0005 probabilities with `metrics.json` and `predictions.jsonl`, extracted five cited lecture pages again (Lecture 5 pp. 38 and 50, Lecture 7 pp. 11, 32 and 68), and corrected three statements: the figures dependency, pure forest leaves, and Lecture 7's course-source listing.
- Trace check: the q0005 probabilities for L3-C10, DT-d30-leaf1, RF-dNone-leaf1 and XGB-d6-lr0.05 come from training-only refits that equal the saved values, with a maximum difference of 0.0. Jev's answer is read from the two validation logs.
- Verification: the lead inspected all 18 rendered pages and removed a two-word overflow page. A scripted check found every source word in the extracted text, apart from the unrendered `pagebreak` marker. Two consecutive exports produced identical hashes.
- Authoring: ReportLab 5.1.0 and pypdf 6.21.3 in a throwaway `uv run --no-project` environment, through the ignored exporter `work/study-pdf/export.py`.
- Data exposure: the guide quotes only q0005, the Altan-authored validation row that the M2 and M3 guides already quote. No sealed test text appears.
- The edition first cites Lecture 7 pages 6, 10 to 12, 14, 18, 28, 29, 31, 32, 35, 36, 38, 39, 52, 54, 56, 57, 68, 69, 80 and 81, now listed in the [course sources](../course-sources.md).

## M4 confidence and errors edition, November 3, 2026

The edition is delivered. Altan's attempt at its nine practice questions is pending, so it is not a closed-milestone snapshot yet.

| Edition | Source | PDF, 16 pages | Source SHA-256 | PDF SHA-256 |
| --- | --- | --- | --- | --- |
| M4 | [M4 confidence and errors](m4-confidence-errors.md) | `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/M4-confidence-errors.pdf` | `7e2f888c5b25d24ee1125aaf03b0aedf335a2a6eb7d3d9426f890d9f297a1b5c` | `943f3aff4d6e909aa9d4ea3ff2ad6622e2e5842ec2cef238bc057afa3526f77e` |

- The sidecar `M4-confidence-errors.manifest.json` records the repository commit at export (`61b758e`) and the hash of every cited course PDF. All six cited course files are present; the five already cited by earlier editions keep their recorded hashes.
- Drafting: a Sonnet subagent drafted the source from the M4 evidence record, `confidence.py` and the saved `m4-5-validation` and `final-test-m3-5` artifacts, extracting every cited lecture page with `pdftotext`. The lead filled the test-mistakes section from the reviewed [test ledger](../evidence/m4-final-test.md#test-mistakes-interpreted-after-the-freeze), checked the reliability bins, thresholds and fold claims against the files and the code, re-extracted five cited pages (CourseProjects p. 15, report instructions p. 1, Lecture 5 p. 56, Lecture 7 pp. 52 and 57), and corrected the calibration mechanism, Jev's replay and two practice questions whose answers were printed in the guide.
- Review: an independent Opus reviewer recomputed the tables, confusion matrices, reliability and threshold numbers, q0005 trace, fold sizes and by-origin scores, checked sixteen cited lecture pages, and found no five-word sequence of test text in tracked files. Its findings led to these corrections: one overconfident bin, a selection-optimism claim the evidence cannot isolate, hypotheses stated as facts, and practice questions 3 and 6 to 9, whose answers the text still gave. Answer sentences were removed and questions 7 and 8 replaced with transfer questions.
- Trace check: the q0005 raw and calibrated L3-C10 probabilities are read from `results/m4-5-validation/predictions.jsonl`; its losses were recomputed by hand and by the reviewer.
- Verification: the lead inspected all 16 rendered pages and added two page breaks so no heading ends a page. A scripted check found every source word in the extracted text. Two consecutive exports produced identical hashes.
- Authoring: ReportLab 5.1.0 and pypdf 6.21.3 in a throwaway `uv run --no-project` environment, through the ignored exporter `work/study-pdf/export.py`.
- Data exposure: the guide quotes only q0005, the Altan-authored validation row that earlier guides quote. Test mistakes are described by ID and paraphrase; no test text appears.
- The edition first cites Lecture 5 p. 80, Lecture 7 pp. 47, 53 and 58 to 61, and Lecture 8, now listed in the [course sources](../course-sources.md).
