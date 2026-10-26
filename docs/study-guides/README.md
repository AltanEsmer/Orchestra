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
| M4 | Confidence, calibration, errors, test freeze, uncertainty and limitations. Supplies confidence analysis and final findings. |
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

M1 edition: not yet exported. Pilot rows and guide-v1 decisions are now available in the [pilot record](../evidence/pilot-guide-v1.md), and the methods preview includes the October 26 update. The milestone edition still needs the first dataset’s full coverage evidence; M1 is not complete.

Inspected course source revisions for this edition:

| File | SHA-256 |
| --- | --- |
| `CourseProjects.pdf` | `d4e98da373cbdcd62f804d2cd0f957bbaa53294205762ba6d1dc04b26b74fdca` |
| `ProjectRreportInstructions.pdf` | `00ab8140f009f52fd9f552daa61ade6f628bdd1125096d62c54e07f06e1519a5` |
| `Lecture2-Data Preprocessing and Feature Engineering.pdf` | `e7bfec9a9a52954c038e58a84f680e76648efa582ef79acafe2a3bfaa582217f` |
| `Lecture5-FundamentalClassificationAlgorithms.pdf` | `c2995d1963da118c5b8f599a641a15b2c8ec8102aa61a66fee13a29eeb67980d` |
| `Lecture6-ArtificialNeuralNetworks.pdf` | `4096ea75c917389ad65c0322bb1e045fcba82154ecde673f7221da3440b7d94d` |
