# Orchestra report

The [editable IEEE manuscript](main.tex) compiles to seven pages, including four research figures, five results tables and references. The current local reading copy is `output/pdf/Orchestra-report-2026-11-23-research.pdf`. The November 16 submission ZIP contains the earlier edition. Use the evidence map below to revise the prose in your own words and verify the claims you keep. The course allows 5–12 pages. The M5 draft target is November 25 and the report and code are due December 6. [Course instructions and page references](../docs/course-sources.md)

## Evidence to use while writing

The abstract links to the public [Orchestra repository](https://github.com/AltanEsmer/Orchestra). Readers can trace the paper through the [dataset release](../docs/evidence/m3-5-dataset.md), [source manifest](../data/manifests/sources.json), [validation run](../docs/evidence/m3-5-full-run.md), [final test and label review](../docs/evidence/m4-final-test.md) and [clean reproduction](../docs/evidence/m6-reproduction.md).

| Report section | Evidence and how to read it |
| --- | --- |
| Task and data | Use the first-action examples in the [protocol](../docs/data-and-evaluation.md#prediction-contract). For what actually entered the release, use the [release and split counts](../docs/evidence/m3-5-dataset.md), [source manifest](../data/manifests/sources.json) and [collection brief](../docs/collection-brief-m3-5.md). Describe the inherited and newly screened rows separately. |
| Methods | Use the M3.5 [configuration grid](../configs/m3-5.json), [methods guide](../docs/study-guides/m3-5-data-and-methods.md) and [record of the full run](../docs/evidence/m3-5-full-run.md). The local comparison holds the partitions fixed. Jev changes both the system and the information supplied about the task. |
| Results | Table I uses the ten chosen IDs in `results/m3-5-full-a-selection.json`. Read validation macro-F1 from `results/m3-5-full-a/metrics.json` and test macro-F1, accuracy, `brier` and `ece` (five bins, native probabilities, null for S1's margins) from `results/final-test-m3-5/metrics.json`. Use the latter file for per-class precision, recall, F1 and support. Table II gives the matched-C contrasts. Table III uses the selected Jev test entry, with class F1 for `S1-C1` and `L3-C10` from the same file. The contrasts and local batch timings are in `results/m3-5-full-a-report/comparison.md`. Jev network timings are in the [collection record](../docs/evidence/m3-5-full-run.md#jev-collection). |
| Confidence and errors | Use `results/m4-5-validation/{reliability,thresholds}.json` for bin counts and the threshold choice in Table IV. Use `results/final-test-m3-5/{metrics,reliability,thresholds}.json` for frozen outcomes. Read the [M4 test record and label review](../docs/evidence/m4-final-test.md) alongside `results/test-interpretations-m3-5.jsonl` for paraphrased examples and correct comparisons. A missing attachment is a proposed explanation for a measured error. |
| Discussion | Section VII compares published GPT and Claude results, explains why the expansion lacks an irrelevant-attachment control, and gives the workload for reviewing model disagreements. The [research note](../docs/evidence/jev-routing-error-research.md) records the counts, the published comparisons and a proposed test using pairs of requests. |
| Limitations and reproducibility | Use the [release disclosures](../docs/evidence/m3-5-dataset.md#disclosures-and-limitations), [archive identities](../docs/evidence/m3-5-full-run.md) and [freeze, receipt and final output hashes](../docs/evidence/m4-final-test.md#identities). The 62-file archive restore reproduced validation with cached Jev replies. Cite the run's own provenance, including its dirty working tree, separately from the report commit. The [M6 record](../docs/evidence/m6-reproduction.md) documents the completed clean reproduction of the full 171-file study archive, including confidence, the freeze, final-test replay and figures. Distinguish this from the earlier validation-only archive. |

Table I rounds directly from the metrics files. For DT-d30-leaf1 the test value is 0.8064543652, or **0.806** to three decimals. The earlier M4 summary prints 0.807.

Table V was calculated on November 9 by joining the frozen release to saved test predictions on query ID, validating matching accepted labels, and matching each cue with a case-insensitive whole-word regular expression. These descriptive subsets overlap and differ in source and action mix. [Review record](../docs/evidence/m5-report-review.md)

## Figures in the draft

Three images in [figures/](figures/) are copies from the research export. The reliability panels render three selected systems from the saved final-test bins. Each named PNG has a matching source sidecar. The full local export retains SVGs, exact numeric inputs in `plot-data.json`, and a checksum for each output in `manifest.json`.

| PNG | Values in plot-data.json | Reading question |
| --- | --- | --- |
| `class-balance.png` | `class_balance`, in `class_order` | How much support does each action have on training and validation? |
| `word-lengths.png` | `word_lengths.train` and `word_lengths.validation` | What might a long tail tell us about the way the router input was assembled? |
| `test-reliability.png` | Saved test bins for L3-C10, calibrated L3-C10 and Jev in its sidecar | How do bin sizes limit the calibration claim? |
| `final-confusion-Jev.png` | `final["confusion.json"]["Jev"]["counts"]` | Which accepted action accounts for the largest group of errors, and what did Jev predict instead? |

From the repository root, reproduce the figures from saved outputs with the following command. Choose a fresh output directory for a repeat export. The draft uses three PNGs from this export. The additional reliability panel uses its retained numeric sidecar as described below.

```sh
uv run --locked python -m orchestra figures \
  --run results/m3-5-full-a --selection results/m3-5-full-a-selection.json \
  --train data/processed/m3-5/train.jsonl --validation data/processed/m3-5/validation.jsonl \
  --confidence results/m4-5-validation --final results/final-test-m3-5 \
  --out results/m5-figures
```

Compile `main.tex` with IEEEtran in the report directory (for example, `tectonic main.tex`). The tracked images are sufficient for compilation. For practice, use the [M5 study guide](../docs/study-guides/m5-report.md).

Rebuild the reliability panels from the tracked numeric sidecar with `uv run --locked python report/plot_reliability.py` from the repository root. The sidecar records exact bin values, source hashes, renderer hash and output hash.

## M7 package review

The manuscript now cites the completed M6 reproduction. The final package manifest and M7 evidence record identify the code commit, report PDF and archive checksums. The Git bundle provides a checkout for the reproduction script; the source ZIP provides readable source without Git history. Use the bundle clone for the clean rerun. The study archive contains local query text and remains outside Git.

The report remains supplied for Altan's own-word review. Package verification does not establish that review or complete the unanswered oral rehearsal. Actual submission and its receipt belong to M8.

## Plain-language pass, November 16, 2026

At Altan's request the prose was rewritten in plainer words, with repeated AI-style sentence patterns removed and a shorter Assistance section. At his request the Assistance section no longer mentions AI help drafting and editing the report, although AI agents did draft and edit it. Altan's own actions are now written in the first person. "The collection lead" now reads "the lead AI agent", as in the release disclosure. The q3014 example no longer says L3-C10 "also" predicted retrieval: the saved test predictions show Jev chose direct answer and L3-C10 chose retrieval. A script compared the old and new source: every number, citation key, label, table body and the bibliography are unchanged. The PDF is still seven pages. The November 13 M7 package holds the earlier report text. The [November 16 package](../docs/evidence/m7-freeze.md#november-16-edition) contains this version.

## Supervisor follow-up, November 19, 2026

Section VI uses the archived four-choice responses and the error review completed after the test was opened. To check the three counts, run `uv run --locked python -m orchestra test-review --final-test results/final-test-m3-5 --interpretations results/test-interpretations-m3-5.jsonl`. The ledger assigns one hypothesis to each error. The eight ambiguous cases comprise six calculation-to-direct conversions and two lookup-to-retrieval table questions. The five wording cases comprise three inline passages sent to retrieval and two mathematical results sent to direct answer.

To check the additional counts from the local study archive, join `results/final-test-m3-5/predictions.jsonl` to `data/processed/m3-5-v1.jsonl` on query ID and verify the accepted labels match. Use the Jev and raw L3-C10 predictions from the same split.

| Question | Selection and result |
| --- | --- |
| Did the missing passage signal always lead to a mistake? | Select accepted retrieval rows with a `kind=passage` entry in `data/raw/m3-5-import/attachments.jsonl`. This covers 180 test retrievals from the expansion. Jev got 167 right. L3-C10 correctly routed 10 of the remaining 13. |
| Did Jev consistently miss conversions? | Select calculation rows with source `clinc150` and type `per-unit-scaling` in `data/raw/m3-5-import/types.json`. Jev got 7 of 13 right. The other six have the adopted standard-factor decision in the release rationale. Compare that decision with the calculation criterion in [the original prompt](../src/orchestra/jev.py). |

[Lu et al.](https://aclanthology.org/2025.findings-naacl.65/) provide the ToolSandbox example in Figure 3 and the GPT-4o and Claude 3 Opus similarity scores in Table 5. [Zhang et al.](https://proceedings.iclr.cc/paper_files/paper/2025/hash/97e2df4bb8b2f1913657344a693166a2-Abstract-Conference.html) evaluate clarification on open-domain questions. The report proposes testing attachment information, clearer rules and clarification on fresh groups. Their effects on Orchestra are unmeasured.
