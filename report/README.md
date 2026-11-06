# M5 report outline

Start in [main.tex](main.tex). Each section gives Altan a writing question, a page allowance and measured evidence. The figures and comparison table are ready to use. Replace the prompts with your own account, check citations and assistance disclosures, then review the compiled manuscript against the 5–12 page IEEE two-column requirement. The draft target is eight pages by November 25. The report and code are due December 6. [Course instructions and page references](../docs/course-sources.md)

## Evidence to use while writing

| Report section | Evidence and how to read it |
| --- | --- |
| Task and data | Use the first-action examples in the [protocol](../docs/data-and-evaluation.md#prediction-contract). For what actually entered the release, use the [release and split counts](../docs/evidence/m3-5-dataset.md), [source manifest](../data/manifests/sources.json) and [collection brief](../docs/collection-brief-m3-5.md). Describe the inherited and newly screened rows separately. |
| Methods | Use the M3.5 [configuration grid](../configs/m3-5.json), [methods guide](../docs/study-guides/m3-5-data-and-methods.md) and [record of the full run](../docs/evidence/m3-5-full-run.md). The local comparison holds the partitions fixed. Jev changes both the system and the information supplied about the task. |
| Results | Table I uses the ten chosen IDs in `results/m3-5-full-a-selection.json`. Read validation macro-F1 from `results/m3-5-full-a/metrics.json` and test macro-F1 from `results/final-test-m3-5/metrics.json`. Use the latter file for per-class precision, recall, F1 and support. The matched-C contrasts and local batch timings are in `results/m3-5-full-a-report/comparison.md`. Jev network timings are in the [collection record](../docs/evidence/m3-5-full-run.md#jev-collection). |
| Confidence and errors | Use `results/m4-5-validation/{reliability,thresholds}.json` for bin counts and the threshold choice. Use `results/final-test-m3-5/{metrics,reliability,thresholds}.json` for frozen outcomes. Read the [M4 test record and label review](../docs/evidence/m4-final-test.md) alongside `results/test-interpretations-m3-5.jsonl` for paraphrased examples and correct comparisons. A missing attachment is a proposed explanation for a measured error. |
| Discussion and reproducibility | Use the [release disclosures](../docs/evidence/m3-5-dataset.md#disclosures-and-limitations), [archive identities](../docs/evidence/m3-5-full-run.md) and [freeze, receipt and final output hashes](../docs/evidence/m4-final-test.md#identities). The 62-file archive restore reproduced validation with cached Jev replies. Cite the run's own provenance, including its dirty working tree, separately from the report commit. M6 covers clean final reproduction. |

Table I rounds directly from the metrics files. For DT-d30-leaf1 the test value is 0.8064543652, or **0.806** to three decimals. The earlier M4 summary prints 0.807.

## Figures in the outline

The images in [figures/](figures/) are copies from the research export. Each named PNG has a matching source sidecar. The full local export retains SVGs, exact numeric inputs in `plot-data.json`, and a checksum for each output in `manifest.json`.

| PNG | Values in plot-data.json | Reading question |
| --- | --- | --- |
| `class-balance.png` | `class_balance`, in `class_order` | How much support does each action have on training and validation? |
| `word-lengths.png` | `word_lengths.train` and `word_lengths.validation` | What might a long tail tell us about the way the router input was assembled? |
| `final-confusion-Jev.png` | `final["confusion.json"]["Jev"]["counts"]` | Which accepted action accounts for the largest group of errors, and what did Jev predict instead? |

From the repository root, reproduce the figures from saved outputs with the following command. Choose a fresh output directory for a repeat export. Only the three PNGs and their sidecars belong in the outline.

```sh
uv run --locked python -m orchestra figures \
  --run results/m3-5-full-a --selection results/m3-5-full-a-selection.json \
  --train data/processed/m3-5/train.jsonl --validation data/processed/m3-5/validation.jsonl \
  --confidence results/m4-5-validation --final results/final-test-m3-5 \
  --out results/m5-figures
```

Compile `main.tex` with IEEEtran in the report directory (for example, `tectonic main.tex`). The tracked images are sufficient for compilation. For practice, use the [M5 study guide](../docs/study-guides/m5-report.md).
