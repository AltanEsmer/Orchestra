# M0 delivery plan

Approved direction: October 8, 2026. Implements [issue #3](https://github.com/AltanEsmer/Orchestra/issues/3) with Altan's revised scope. The objective is to complete Orchestra and defend the project through the December report and January oral exam preparation, connecting implementation choices to course concepts.

## Agreed scope

- Remove course-rule confirmation as an agent task and milestone gate. Altan owns these administrative details. This decision does not claim that the supplied PDFs establish unspecified rules.
- Read relevant lecture slides from `/Users/altanesmer/Desktop/SM1/AI/` at each milestone. Record the inspected filename, PDF page number, and source revision. New slides are incorporated when milestone work resumes, not by a background monitor.
- Keep editable guide text in `docs/study-guides/`. Export milestone PDFs to `/Users/altanesmer/Desktop/SM1/AI/Orchestra-study/`, outside Git.
- Give every milestone a plain-language lesson and technical appendix. Cover the purpose, implemented files, one concrete query, course concepts, choices, actual checks, limitations, report evidence, and oral questions.
- Update the relevant guide after meaningful changes. Maintain a stable current PDF and a dated snapshot when the milestone closes. Record a checksum and the source commit for each delivered edition.
- Keep the final report a separate synthesis in Altan's own words. Continue oral practice through January 2027 using actual results and recorded learning gaps. The month is Altan's stated preparation target, not a date verified from the supplied PDFs.
- Preserve the existing model-development boundary. M0 introduces no research dataset, model, experiment, or tool execution.

## Ordered delivery and acceptance

1. Save this plan before authoring the M0 guide. Update the roadmap, project plan, and current administrative wording to match the accepted direction.
2. Recheck the existing smoke script and course mappings. Run the README setup, smoke, and lint commands. Preserve actual output and distinguish these checks from research evidence.
3. Write `docs/study-guides/m0-preparation.md`. Explain first-action routing before vocabulary or split terminology. Trace the actual toy input through TF-IDF and the dummy classifier. Explain which behavior belongs to our script and which belongs to scikit-learn.
4. Export `M0-preparation.pdf` to the chosen folder. Inspect every rendered page for legibility and layout, and verify that its content matches the editable source. Keep generation tools outside the project's runtime dependency set.
5. Review standards and the accepted specification independently. Fix findings, record evidence in the learning log and guide index, and commit coherent changes on the current branch. Reconcile issue #3 with the revised scope and observed evidence.
6. Present a short introductory checkpoint. Record only Altan's actual answers and feedback. Keep M0 in progress until that response is recorded; a completed guide establishes delivery, not student understanding. Gaps may remain visible after the checkpoint.

The agent can complete steps 1-5 now. Step 6 needs Altan's participation and is not replaced by generated answers. No course-confirmation response is required.

## Workflow choices

The Poteto Feature playbook is adapted to a documentation and PDF artifact change. The existing repository walkthrough supplies the implementation explanation. Architect is skipped because no application boundary or model design changes. TDD is skipped because no runtime behavior changes; existing smoke assertions, source checks, Markdown links, and rendered PDF inspection are the meaningful checks. The two-axis review uses the starting commit `0350a8e7cfa080b236caeb999e6eff3853c54f28` as its fixed point and this document plus Altan's request as the specification. No new issue-tracker setup is needed because issue #3 is known. A PR is deferred; the Implement request calls for a commit on the current branch.

Throughput checkpoint:

- Blocking first steps: verify the remote and clean starting state, read the project guidance, and save the accepted plan.
- Independent workstreams: the lead owns the roadmap and supporting documents; a worker owns the M0 guide and PDF export.
- Shared mutable state: writers have disjoint files. Git staging, commits, issue edits, and final evidence updates belong to the lead.
- Smallest safe decomposition: one guide author and independent standards/specification reviewers. No application implementation or competing architecture is needed.
