# M5 | From a prediction to a report claim

## Read one cell before writing the paragraph

Start with the confusion matrix in the report outline. Read along the retrieval row. Of 200 test queries labeled retrieval, Jev sent 187 to retrieval and 13 to direct answer. The row answers a question a single macro-F1 score cannot: when this system misses a document request, which action does it choose?

Follow one of the 13. In q3014 a short request to summarize has a passage attached. Annotation considers the whole request and assigns retrieval. The router receives the instruction without the passage or its attachment metadata. Jev chooses direct answer. Altan verified the attachment hash and retained the retrieval label on November 6. The saved prediction establishes the disagreement. A future experiment that supplies an attachment indicator could test the missing-context explanation.

## Write from three different records

- Data and methods. Start with the achieved release and the split, then describe what each model sees. The class-balance and word-length plots describe only training and validation. Most local comparisons vary an estimator or word representation. Jev also introduces pretraining and written action definitions.
- Results. Report the selection from the 629 validation rows first. The 0.023 macro-F1 gap between Jev and L3-C10 exceeded the frozen 0.01 tolerance. Present the 628-row test as the estimate after that decision. S1 scoring above L3-C10 there is worth explaining because it shows how the local ordering varied.
- Confidence and limits. Discuss the separate L3-C10 calibration experiment. Inspect a reliability bin and its count before generalizing from its mean. Distinguish the effect of raising a threshold on coverage from its effect on the accuracy of accepted queries. When interpreting the test scores, identify the population and the label review process.

<!-- pagebreak -->

## Technical appendix | Trace the artifacts

The outline is in report/main.tex. The adjacent report/README.md maps every section and figure to a run or recorded decision. The figure exporter checked the manifests for the validation run, confidence analysis and final test. Each selected image retains its source sidecar. The full local figure directory contains exact numeric inputs. No new scoring is needed to write a caption.

For q3014, follow results/final-test-m3-5/predictions.jsonl to the cell in confusion.json and the matching row of results/test-interpretations-m3-5.jsonl. Then read the November 6 adjudication in docs/evidence/m4-final-test.md. Keep the measured count, the author's decision, and the proposed explanation separate when drafting.

## Course connection checked November 6, 2026

`CourseProjects.pdf`, p. 15, asks for classifier and representation comparisons, confidence and errors. `ProjectRreportInstructions.pdf`, p. 1, asks for a research report in your own words, useful exploratory graphs, 5–12 pages and two-column IEEE conference format. The eight-page allocation and three-figure selection are working choices for this draft. Hashes of both inspected PDFs appear in docs/course-sources.md.

`UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf`, p. 53, asks whether testing remains independent of training. In Orchestra, groups stay together across splits, the selection used validation, and the test was opened once after freezing. The slide motivates independence. The 0.01 tolerance and one-opening receipt are project choices. Inspected lecture SHA-256: 918f33dc045f3fbbaaae8a33b1a779e9eb7785e8625f1008aa5fc144b49813fd.

## Practice for the draft

1. Pick the lookup row in the test confusion matrix. Write a caption that gives its denominator and says what happened to the missed requests.
2. At the same regularization setting, what evidence would justify saying that adding bigrams helped? How would you qualify that sentence across settings?
3. Pick a confidence threshold for a service with expensive human review. Which two validation quantities would you report together, and what assumption would you need to check in that service?

Record your attempt before consulting a worked explanation. The full own-word manuscript, final citations, pagination check and learning checkpoint remain open.
