# M1: the first dataset and how its labels were made

Study guide edition: October 28, 2026. Data release: `data/processed/m1-v1.jsonl`, frozen on October 26, 2026 and recorded in commit `33d6f62`. Dataset SHA-256 `3e02b6fa8a7c1987a44a6a9ae1c118bac768be16ad05c58d2948880b87633b2e`. Review ledger `data/raw/reviews-v2.jsonl`, SHA-256 `5c449ce1f234490f351e1be7b1843346f46d9c1466136a0b14d5ddb6eb6c2de8`. The project is course project 13, Learning to Route Queries in AI Systems.

## What you need to defend

M1 produced the labeled examples that every later milestone learns from and is scored on. The release holds 128 accepted English queries. Each row has one first-action label, a written rationale, a group, a source, and a review record. Project 13 asks for a classification formulation in `CourseProjects.pdf`, PDF page 15 [S1]. M1 supplies the classes and records that make that formulation concrete.

You need to explain four things. First, what each label means and why some queries receive no label. Second, where each row came from and what permission covers it. Third, how groups were defined and why the rule changed. Fourth, who decided each label and what the review evidence can and cannot show.

The release is small and deliberately balanced. Every class has between 31 and 33 rows. The rows come from four sources, and three of those sources each feed only one or two labels. That pattern is the most important limitation to carry into M2 and M3.

This guide supports the data section of your December report and your January oral preparation. Reading it does not establish that you can explain the dataset unaided. The checkpoint at the end asks new questions. Your own answers are the evidence.

## What this edition contains

The first eight sections explain labels, provenance, grouping, review, distributions, one traced query, course connections, and report use. The technical appendix shows the row and ledger formats, the readiness check, and how the counts were computed. The final section holds unanswered practice questions and the inspected sources.

<!-- pagebreak -->

## Four labels and a holdout

The router predicts the first action needed to answer a self-contained query. It sees only the query text. It assumes three tools exist: a named-document retriever, a structured knowledge lookup, and a calculator. These definitions live in `docs/data-and-evaluation.md` and `docs/annotation-guide.md`.

- `document_retrieval` means reading an identified document or passage first.
- `knowledge_lookup` means looking up a specific record in an identified structured source first.
- `calculation` means computing a numeric answer whose inputs already appear in the query.
- `direct_answer` means explaining, rewriting, or answering without retrieval, lookup, or a requested calculation.

The annotation guide orders the decision. First ask whether the text alone allows a choice. Then list the actions the request needs. If several apply, label the one whose output another action needs. Reading a report before calculating from its figures is therefore `document_retrieval`.

Some queries should get no label. A request that omits which document or record it means is marked `needs_review` with the reason "missing context". A request that needs live information none of the three tools provides is marked `excluded`. Neither status is a fifth class. They keep incoherent examples out of training instead of forcing them into one of four boxes.

The frozen release contains no `needs_review` rows and no excluded rows. The holdout was applied earlier. During the pilot, two queries became practice-only. q0014 was adapted from a teaching example, so it would have repeated material the guide reserves for practice. q0037 was a fifth member of an amount-per-unit family under the template grouping that became guide v1, and a group may hold at most four research rows. Both remain in the dated audit history, outside the study.

Public sources were screened under the same rules before import. The BFCL inspection set aside database writes and requests needing live services. Those screened-out records never entered the release file.

The four labels and the holdout statuses are project choices. The course names example actions such as document retrieval, knowledge-base search, calculation, and direct answering [S1]. It does not prescribe our exact label strings, boundary rules, or holdout procedure.

<!-- pagebreak -->

## Where every row came from

Every row carries a `source_id` that points to an entry in `data/manifests/sources.json`. Each entry records an author, a creation date, and a license or permission. The readiness check refuses any accepted row whose source lacks a license.

| Source | Rows | Labels it supplies | License or permission |
| --- | ---: | --- | --- |
| `altan-authored` | 38 | All four | Altan's written permission, dated October 23, 2026, for q0001 through q0040 |
| `bfcl-v3` | 45 | 23 calculation, 22 lookup | Apache-2.0 |
| `dolly-15k` | 22 | 22 document retrieval | CC BY-SA 3.0 |
| `no-robots` | 23 | 23 direct answer | CC BY-NC 4.0 |

The 38 authored rows come from 40 pilot candidates written on October 22 and 23. Collection used agent-directed exercises with immediate feedback. Many prompts named the category to write, so these rows are human-written but agent-guided. Your permission statement covers study use, course submission, and public sharing of those forty queries only. It does not extend to public sources or later drafts.

Each public source is pinned to an exact upstream revision. Only the user's own text is router input. For BFCL, function documentation, expected calls, and system messages are left out. For Dolly, the original reference passage is stored as a linked attachment outside router input. You adopted that attachment adapter on October 26. No public text was rewritten to fit a label.

The licenses differ, and the repository's MIT code license covers none of the data. Dolly-derived rows keep CC BY-SA 3.0 obligations. No Robots rows are non-commercial only. Their attribution must travel with the data.

None of these sources is real user traffic. The authored rows describe fictional schools, hotels, and catalogs. Dolly and No Robots are instructed human writing, and BFCL is a function-calling benchmark. The dataset supports claims about these sources, not about how real users phrase requests.

<!-- pagebreak -->

## Groups: from request templates to scenarios and sources

A group holds rows that a model could memorize across splits. Whole groups move together when M2 divides the data. If two near-copies sat in training and test, the test score would partly measure recall of the training row. You explained this mechanism yourself on October 25, as recorded in the learning log.

Guide v1, frozen on October 26, defined a group as a shared request template: the same user goal solved by the same procedure, whatever the scenario. You made those pilot decisions. For example, you kept summarization separate from turning a handbook into a checklist. The 38 accepted pilot rows formed 19 templates.

That rule blocked M1. The public expansion screen showed that most public rows matched templates already in the pilot, such as answering a question from a passage. Such rows would join an existing family, and a family holds at most four rows, so they added little. Document retrieval could reach about 8 of the 15 required groups, and lookup about 6.

Guide v2 changed only the grouping rule. Two rows now share a group when any of these holds:

1. One is a small variation of the other.
2. They name the same source or named setting, such as one database or one fictional organization.
3. They describe the same specific situation.
4. They come from one public record, passage, or named table.

A shared request type, label, keyword, or arithmetic operation alone no longer joins rows. Groups may mix labels. Labels, boundaries, review method, and the readiness targets did not change.

The project plan records the trade-off. Under v1, a test score would show how the router handles new request types. Under v2, it shows how the router handles new topics and sources with familiar request types. The report must disclose this change and the v1 history.

v2 added three batch checks to replace some of the lost protection. Near-duplicates are checked by hand. No request type may exceed 40 percent of a class. Each class needs at least two sources, and no source may exceed 75 percent of a class. These thresholds are project choices. You approved the pilot regrouping on October 26.

<!-- pagebreak -->

## Who decided each label

On October 24, you chose single-human annotation with disclosed AI checks. You are annotator `A1` on all 128 rows. Your labels are the reference. An AI reviewer then labeled the same queries blind, and every flag or disagreement needed your dated decision.

The pilot and the import were reviewed differently.

- **Pilot, 38 rows.** You wrote each label and rationale. A `gpt-6.1-sol` reviewer saw only the guide and shuffled query text. It matched all forty original labels. An earlier flag on q0033's "holds 60 litres" wording stayed open despite the match. You clarified on October 25 that this meant the water currently inside the tank, so `calculation` stayed.
- **Import, 90 rows.** The agent proposed labels. On October 26 you approved all proposals in one reply. A fresh `claude-opus-5-5` reviewer then labeled the shuffled queries under new IDs, with no label, source, or group visible. It matched all 90. It marked 14 ambiguous, and 55 rows had a flag or ambiguous judgment. You accepted the agent's recommendation for all 55 in one reply.

The ledger now holds 128 `ai_assisted` entries and 56 dated adjudications by A1. The validator reports AI consistency of 128 of 128. It reports human agreement as zero reviewed rows, because no second human or delayed self-review exists.

AI consistency is not inter-annotator agreement. An inter-annotator figure needs two independent human judgments of the same rows. Here the second judgment came from a model reading the same guide. For the import, the reviewer was from the same model family as the agent that proposed the labels. You saw the agent's proposals and flags before deciding, which creates anchoring risk. The pilot collection also used immediate feedback. Each of these can make agreement look higher than independent annotation would.

What the check does show is narrower. Under the shared written guide, a blind reader reached the same first action on every row. Flags exposed real ambiguity, such as q0033, and each received a human decision. The report should state single-annotator bias, AI assistance, and the anchoring risk plainly.

<!-- pagebreak -->

## What the release looks like

| Label | Rows | Groups containing it | Main source share | Median words |
| --- | ---: | ---: | --- | ---: |
| `calculation` | 32 | 31 | BFCL 23 of 32 | 18.5 |
| `document_retrieval` | 31 | 30 | Dolly 22 of 31 | 14 |
| `knowledge_lookup` | 32 | 25 | BFCL 22 of 32 | 19 |
| `direct_answer` | 33 | 30 | No Robots 23 of 33 | 14 |

There are 108 groups. Ninety-four hold one row, nine hold two, four hold three, and one holds four. Seven groups mix labels: g034 through g040. All seven contain only authored rows that share fictional names such as Willow or Maple. Per-class group counts sum to 116 because a mixed group counts once for each of its labels.

Lookup has the fewest independent groups. Its 32 rows sit in 25 groups. Several authored lookups share named settings, and BFCL rows that query the same named table share a group. Fewer groups means less independent evidence about that class.

Query length ranges from 4 to 77 words, with a median of 16. Length also differs by source. Authored rows have a median of 13 words, Dolly 17, BFCL 22, and No Robots 24.

The source pattern is a confound. Every No Robots row is `direct_answer`. Every Dolly row is `document_retrieval`. BFCL supplies only `calculation` and `knowledge_lookup`. Only the authored rows cover all four labels, and they are about 30 percent of each class. Within the release, source style and label cannot be fully separated.

This matters for M2 and M3. A classifier could score well by recognizing how a source writes, such as passage phrasing or SQL table wording, rather than which action comes first. The 75 percent limit bounds the association but cannot remove it. Some cue words are measurable now. "Fictional" appears in 19 rows, all authored retrieval or lookup rows. "Database" appears in 8 rows, all lookups. These are associations in the data, not evidence that any model uses them. The M3 collection brief adds a second source per class to dilute them.

<!-- pagebreak -->

## Trace one query: q0036

The text is "Does booking B24 exist in the fictional Willow Hotel database?" You wrote it on October 23 in response to an exercise asking for a record-existence check in a named fictional database. The prompt chose the category. The wording and rationale are yours.

Apply the decision order. The query names a structured source, the Willow Hotel database, and a record, booking B24. Nothing is missing. Only one action is needed: check whether that record is stored. The label is `knowledge_lookup`. The label does not assume B24 will be found. The router chooses the first action, and the lookup would run afterward.

Your rationale reads: "First action: look up the record, because I need to check the database to see whether that booking is listed." It names the action and the reason, as the guide requires.

The group changed twice without changing the label. At intake it sat alone in a provisional group for existence checks. Under guide v1 you joined it to g003, the key-based lookup family, and kept it apart from condition filters. Under guide v2 it moved to g038. q0032 and q0040 query the same Willow Hotel database. q0035 quotes a Willow School handbook and is `document_retrieval`. A model could learn "Willow" across splits, so v2 keeps all four together in one mixed-label group.

The source is `altan-authored`, covered by your October 23 permission. Its ledger entry records the blind `gpt-6.1-sol` review on October 24. The reviewer chose `knowledge_lookup`, judged it clear, and raised no flag. A clear, unflagged match keeps the original label without a new adjudication. The resolved label is `knowledge_lookup`, matching the release.

Readiness needs this entry because every row in a mixed-label group must have one, and its resolved label must equal the dataset label. Both hold.

Notice what the trace leaves open. The words "fictional" and "database" appear in this query. Both appear only in retrieval or lookup rows in M1. A correct prediction on q0036 would not show whether a model used the source and record, or just those words. Whole group g038 moves into one M2 partition. The M2 guide covers the split and the baseline results.

<!-- pagebreak -->

## Course principles behind the data choices

Lecture 5, PDF page 2 [S3], defines classification over records whose attributes include one class attribute, with the goal of labeling unseen records. In M1, a record is one row, the query text supplies the attributes, and the first-action label is the class. Page 5 adds that the test set must be separate from the training set [S3]. Lecture 7, PDF page 53 [S4], warns to ensure the test set is truly independent of the training set. Near-copies and shared named settings undermine that independence. Grouping applies the principle; the v2 rules and four-row cap are project choices.

Lecture 2, PDF page 3 [S2], lists incomplete, noisy, inconsistent, and duplicate data. Each has an M1 counterpart. A query that omits its source is incomplete for routing, so it is held out. A wrong label is noise, so every label receives a blind check. Sources with different styles risk inconsistency, so all rows share one schema and pass the source-mix check. The validator rejects exact duplicates, and near-duplicates are checked by hand.

Lecture 2, PDF page 19 [S2], notes that a record is usually ignored when its class label is missing. The holdout follows similar logic for queries without a defensible label. The slide concerns missing values in general; `needs_review` and `excluded` are our design.

Lecture 2, PDF page 20 [S2], lists combined computer and human inspection for suspicious values. The AI-assisted review has this shape: the model flags, a human decides. The slide does not prescribe AI reviewers or our ledger.

Lecture 2, PDF pages 26 and 27 [S2], describe integrating multiple sources, with conflicting representations and redundancy. Page 8 asks how data were sampled and whether privacy issues exist. M1 integrates four pinned sources into one schema. Its public rows came from ordered, seeded, or purposive selections, not random samples of each corpus. The authored rows use fictional settings.

Lecture 5, PDF pages 54 and 55 [S3], show overfitting caused by noise points and by regions with too few examples. These motivate label review and the minimums of 30 rows and 15 groups per class. The minimums are project targets.

Lecture 7, PDF pages 68 and 69 [S4], explain that classifiers tend to favour a majority class and learn better from a balanced distribution. M1 has 31 to 33 rows per class. That balance was a collection target, not a property of real traffic.

Lecture 2, PDF page 68 [S2], summarizes the milestone: quality modeling depends on quality data. A citation explains why a check exists. It does not show that our labels are correct.

<!-- pagebreak -->

## What M1 can contribute to your report

`ProjectRreportInstructions.pdf`, page 1 [S5], asks for a report in your own words describing the dataset and models, with exploratory graphs. M1 supplies most of the data section. The project plan gives that section about 1.5 pages.

Useful material includes:

- A provenance table with sources, licenses, row counts, and the labels each source supplies.
- Class and group counts, with the group-size distribution.
- A class-balance figure and a query-length figure by class and by source. This guide records no such research figure; the counts here are their inputs.
- The annotation method: single human annotator, blind AI consistency check, and dated adjudication of every flag.
- The v1 to v2 grouping change, its reason, and what the test score now measures.
- The two practice-only exclusions and why they were excluded.
- The source-label confound and the measured cue words.

A defensible data statement is this. The release has 128 accepted rows in 108 groups from four sources, labeled by one human annotator. A blind AI check agreed on all 128 labels, and all 56 flagged or ambiguous cases received a dated human decision. Readiness passes on the frozen file.

`CourseProjects.pdf`, page 15 [S1], requires comparisons, confidence analysis, and error analysis. Those come from M2 to M4. M1's role is to make their inputs traceable.

## What M1 cannot support

- **No model quality claim.** M1 trained nothing. It cannot support any accuracy, macro-F1, or confidence statement.
- **No human agreement statistic.** No second human or delayed self-review exists. Do not report 128 of 128 as annotator agreement.
- **No claim of real-user representativeness.** The rows are authored fictional scenarios and instructed or benchmark text, selected to meet class targets.
- **No claim of label correctness.** Readiness checks counts, permissions, and ledger consistency. It cannot judge meaning.
- **No claim that you have mastered M1.** Your learning log shows specific explained examples and many unanswered questions. This guide changes neither.

<!-- pagebreak -->

## Technical appendix: the row and the ledger entry

Each row in the release has nine fields. This is q0036 as frozen:

```json
{"query_id": "q0036", "group_id": "g038",
 "text": "Does booking B24 exist in the fictional Willow Hotel database?",
 "label": "knowledge_lookup", "status": "accepted",
 "source_id": "altan-authored",
 "rationale": "First action: look up the record, because I need to check
   the database to see whether that booking is listed.",
 "annotator_ids": ["A1"], "annotation_version": "guide-v2"}
```

The rationale is wrapped here for width. In the file it is one string. All 128 rows have `status: accepted`, `annotator_ids: ["A1"]`, and `annotation_version: guide-v2`.

Its ledger entry, with hashes shortened for this page:

```json
{"query_id": "q0036",
 "original_label": "knowledge_lookup",
 "review_label": "knowledge_lookup",
 "reviewer_id": "ai:gpt-6.1-sol-blind-2026-10-24",
 "review_date": "2026-10-24", "review_kind": "ai_assisted",
 "resolved_label": "knowledge_lookup",
 "ai_evidence": {"model": "gpt-6.1-sol",
   "prompt_sha256": "fe8b6bde...", "input_sha256": "5ee0123f...",
   "output_sha256": "38975c44...", "judgment": "clear", "flags": []},
 "human_adjudication": null}
```

`original_label` is your label, saved before review. `review_label` is the AI's blind label. `resolved_label` is the final result. A clear match with no flags may resolve to the original label with `human_adjudication` left null. Any flag, ambiguity, disagreement, or proposed exclusion requires an adjudication object with your ID, a date, a label, and a rationale.

q0033 shows the other path. The AI also chose `calculation` and judged it clear, but the entry's `flags` list records the "60 litres" wording question. A flag requires a decision, so the entry holds your October 25 adjudication, which keeps `calculation` and states that the tank's current contents were supplied.

Across the ledger, 38 entries come from `gpt-6.1-sol` and 90 from `claude-opus-5-5`. The AI judged 114 rows clear and 14 ambiguous. Fifty-six entries carry an A1 adjudication: q0033 plus the 55 flagged or ambiguous import rows. The `input_sha256` and `output_sha256` fields identify the preserved blind input and raw AI output files. A hash-shaped string alone does not prove those files are authentic. The ingestion scripts checked the files themselves.

<!-- pagebreak -->

## Technical appendix: readiness and the counts

The readiness command validates structure, the ledger, and the M1 acceptance targets:

```sh
uv run --locked python scripts/validate_dataset.py \
  data/processed/m1-v1.jsonl --sources data/manifests/sources.json \
  --review data/raw/reviews-v2.jsonl --ready
```

Run on October 28, 2026 for this edition, it ended with `PASS: M1 readiness checks passed (128 accepted rows, 128 reviewed)`. Its summary reported `ai_consistency` of 128 matching out of 128 reviewed, human agreement with zero reviewed rows, and an empty excluded list.

Readiness requires at least 120 accepted rows, 30 per class, and 15 groups per class. It requires no `needs_review` row, a license for every source used, and no AI entry awaiting adjudication. Per class, at least `ceil(0.2 x rows)` rows must be reviewed; for 32 calculation rows that is 7, and all 32 were. Every row in a mixed-label group needs a ledger entry, and every resolved label must equal the dataset label.

The group arithmetic checks itself. Group sizes are `{1: 94, 2: 9, 3: 4, 4: 1}`, so `94 + 2*9 + 3*4 + 4 = 128` rows sit in `94 + 9 + 4 + 1 = 108` groups. A group counts once per label it contains. Six mixed groups hold two labels and g039 holds three, adding `6*1 + 1*2 = 8`. That gives `31 + 30 + 25 + 30 = 116 = 108 + 8`.

The source-mix check divides a source's rows in a class by the class total:

```text
calculation:         BFCL      23 / 32 = 0.72
document_retrieval:  Dolly     22 / 31 = 0.71
knowledge_lookup:    BFCL      22 / 32 = 0.69
direct_answer:       No Robots 23 / 33 = 0.70
```

Every share is below 0.75, and every class has exactly two sources. The margins are small. Removing two or three authored rows from any class would break the limit. Multi-row groups come from two sources only: nine authored groups and five BFCL pairs. Every Dolly and No Robots row is a singleton.

The freeze record also lists the guide-v2 hash, `dd78162c…8ba55`, and the source manifest hash, `67cfe73f…f7420`. The manifest later gained a GSM8K entry for M3, so its current hash differs. The release uses only the four M1 entries. Freezing fixes groups and labels; a later correction needs a new release name.

<!-- pagebreak -->

## Your M1 checkpoint

Attempt these before asking for a worked answer. Use your own words. No answer has been written on your behalf.

1. In M3, a No Robots prompt asks to summarize an attached passage and is labeled `document_retrieval`. Suppose a classifier trained on M1 alone had learned that No Robots phrasing means `direct_answer`. What would it predict for this row, and why do such rows help separate source from label?
2. An examiner asks for your inter-annotator agreement. What can you truthfully report from the ledger? What would you need to collect to answer the question as asked?
3. Write one new query that should receive none of the four labels. Say whether it is `needs_review` or `excluded`, and why. Explain what would go wrong if it were labeled `direct_answer` instead.
4. Authored rows have a median of 13 words and No Robots rows 24. How could query length act as a shortcut? Which report figure would reveal it?
5. q0037 became practice-only under the template grouping that became guide v1, because its amount-per-unit family already had four research rows. Guide v2 later split that family into separate per-unit situations. Could q0037 now have its own group? What would you check first, and what would adding it to a frozen release require?

The M0 introductory checkpoint is still unanswered and carries forward. Several earlier M1 practice questions in the learning log are also unanswered. Your attempts and feedback belong in `docs/learning-log.md`. Learning statuses change only from those attempts.

## Inspected sources

All numbers are one-based PDF page numbers. The files are local course sources under `/Users/altanesmer/Desktop/SM1/AI/`. Pages were extracted with `pdftotext` and read for this edition on October 28, 2026.

- [S1] `CourseProjects.pdf`, page 15. Project 13: classification of queries into actions such as document retrieval, knowledge-base search, calculation, or direct answering; classifier and representation comparisons; confidence and error analysis.
- [S2] `Lecture2-Data Preprocessing and Feature Engineering.pdf`, pages 3, 8, 19, 20, 26, 27, and 68. Dirty data, data questions and sampling, missing class labels, noise and combined human inspection, multi-source integration and redundancy, and the data-quality summary.
- [S3] `Lecture5-FundamentalClassificationAlgorithms.pdf`, pages 2, 5, 54, and 55. Classification definition, separate training and test sets, overfitting due to noise and to insufficient examples.
- [S4] `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf`, pages 53, 68, and 69. Independence of test and training sets; imbalanced data and balanced class distributions.
- [S5] `ProjectRreportInstructions.pdf`, page 1. Own-words report describing the data and models, exploratory graphs, 5 to 12 pages, IEEE two-column format, December 6, 2026 deadline.

| File | SHA-256 |
| --- | --- |
| `CourseProjects.pdf` | `d4e98da373cbdcd62f804d2cd0f957bbaa53294205762ba6d1dc04b26b74fdca` |
| `Lecture2-Data Preprocessing and Feature Engineering.pdf` | `e7bfec9a9a52954c038e58a84f680e76648efa582ef79acafe2a3bfaa582217f` |
| `Lecture5-FundamentalClassificationAlgorithms.pdf` | `c2995d1963da118c5b8f599a641a15b2c8ec8102aa61a66fee13a29eeb67980d` |
| `UTF-8''Lecture7-Ensemble%20Methods%20and%20Model%20Evaluations.pdf` | `918f33dc045f3fbbaaae8a33b1a779e9eb7785e8625f1008aa5fc144b49813fd` |
| `ProjectRreportInstructions.pdf` | `00ab8140f009f52fd9f552daa61ade6f628bdd1125096d62c54e07f06e1519a5` |

Project decisions come from `docs/data-and-evaluation.md`, `docs/annotation-guide.md`, `docs/project-plan.md`, and `docs/collection-brief.md`. Evidence comes from `docs/evidence/pilot-ai-review.md`, `docs/evidence/ai-assisted-review.md`, `docs/evidence/pilot-guide-v1.md`, `docs/evidence/guide-v2.md`, `docs/evidence/public-import-v2.md`, and `docs/evidence/public-review-v2.md`. Lecture connections explain these choices. They do not make our labels, groups, or review method course requirements.
