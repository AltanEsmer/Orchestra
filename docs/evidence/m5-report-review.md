# M5 report review, November 9, 2026

The review checked the manuscript against the local course instructions, frozen study artifacts and recorded decisions. The revised PDF has seven IEEE conference two-column pages, four figures, five tables and 20 cited references. Its source is [report/main.tex](../../report/main.tex), with the [evidence map](../../report/README.md) alongside it. The reading copy is `output/pdf/M5-report-draft.pdf` under the repository root, SHA-256 `325df1194d8a76670fa0f6ea467be53c10d0be49434aa7770617ffefd10f5426`.

## Course requirements

| Requirement and source | Review evidence |
| --- | --- |
| Research report describing the data and models, report instructions p. 1 | Sections II and III explain sources, annotation, grouping, representations, configurations and selection. |
| Useful exploratory graphs, report instructions p. 1 | Figures 1 and 2 show class support and query length. Figure 3 visualizes confidence and Figure 4 shows test mistakes. |
| IEEE conference format, two columns, 5–12 pages, report instructions p. 1 | The IEEEtran conference source compiles to seven US Letter pages. All seven rendered pages were inspected. |
| Classifier and representation comparison, CourseProjects p. 15 | Tables I and II report the frozen winners and matched-C contrasts. |
| Confidence and error analysis, CourseProjects p. 15 | Section V, Figure 3 and Table IV explain calibration and selective routing. Section VI, Figure 4 and Table V analyze errors. |
| Own-word report, report instructions p. 1 | Altan’s rewriting and acceptance remain pending. The author line and assistance statement disclose the draft’s provenance. |

The inspected report-instructions PDF has SHA-256 `00ab8140f009f52fd9f552daa61ade6f628bdd1125096d62c54e07f06e1519a5`. CourseProjects has SHA-256 `d4e98da373cbdcd62f804d2cd0f957bbaa53294205762ba6d1dc04b26b74fdca`. Lecture 7 p. 53 was checked for the independence principle. Its revision remains the one recorded in the study guide. The course deadline is December 6, 2026, with report submission through itslearning.

## Corrections and additions

- Equal medians do not establish that query length is a weak predictor. The draft now limits its interpretation to the observed distribution and leaves predictive dependence unmeasured.
- The error discussion now uses Jev’s correct comparison q2291 and discloses that L3-C10 correctly predicted retrieval for q3014. Missing attachment information remains a hypothesis to investigate.
- The model description now specifies the logistic penalty and solver, SVM loss and multiclass strategy, deterministic family preference order, Jev response validity rule and exact prompt location.
- Fallback explicitly applies to calibrated L3-C10. Coverage and selective accuracy are defined with their denominators, and the text describes the simulated review decision. The calibration comparison also changes the underlying ensemble.
- The added reliability figure displays raw L3-C10, calibrated L3-C10 and Jev with counts for all populated bins. Its [renderer](../../report/plot_reliability.py) uses a tracked numeric sidecar. The sidecar records source, renderer and image hashes.
- Table V reports descriptive cue subsets required by the collection audit. It joins the existing test predictions and frozen texts by query ID, verifies the reference labels match, and uses case-insensitive whole-word matching. Every row totals 628 queries, 26 Jev errors and 41 L3-C10 errors. Subsets overlap and differ in class and source mix, so the table supports an association.
- The limitations now disclose candidate exposure during collection, ASCII overlap screening, truncated long-request screens and the DataBench reference-only review. The reproduction section distinguishes the verified validation archive from the complete package that M6 must reproduce.
- The calibration method now cites its official documentation. The CLINC150 citation includes its verified publication details. Source-specific attribution and frozen study references remain in the bibliography.

## Checks and remaining work

The hashes in all three source manifests matched their files. Accuracy, macro-F1 and confusion counts for all 27 validation configurations and all 11 frozen test systems were recomputed from their saved predictions. All four existing tables matched the numeric files. Table V’s counts and errors were recomputed from the joined rows. By-origin results used membership of the actual parent release. The three retained images and sidecars matched the earlier figure export; the new panel values match the saved final-test reliability bins and total 628 per system.

Tectonic compiled the final manuscript without missing glyphs, unresolved citations/references or overfull boxes. Its ordinary underfull spacing warnings were checked visually. All seven pages were inspected, including the final rerender of the changed limitations page. The smoke check passed, 285 tests passed in 30.992 seconds, Ruff lint and formatting passed (92 files), and the diff whitespace check passed. The local verification transcript is in `work/m5-review/`.

The paper is ready for Altan’s revision. M5 acceptance still needs his own account and learning attempt. Complete-package reproduction and archival are assigned to M6. The review used existing predictions and the existing one-time final-test record.
