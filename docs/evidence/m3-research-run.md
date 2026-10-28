# M3 research run

Run on October 28, 2026, after Altan said "Accept all" to the M3 adjudication worksheet. This record covers the frozen main dataset, the grouped split, and the 14 required configurations. Every score here is on validation. The sealed test file was written by `prepare-study` and never opened. Validation text stays out of Git, so no query is quoted.

## Main dataset

Altan's adjudication accepted the 64 pending rows and the one group change, and kept his 7 disputed exclusions. `release.py --write` then applied the fill rule fixed in the [import record](m3-import.md#fill-rule-fixed-before-labels).

| Class | Rows | Groups | Main source | Second source | Altan-authored |
| --- | ---: | ---: | --- | --- | ---: |
| Document retrieval | 100 | 97 | Dolly 75 | No Robots 16 | 9 |
| Knowledge lookup | 100 | 78 | BFCL 62 | AI drafts 28 | 10 |
| Calculation | 100 | 96 | BFCL 75 | GSM8K 16 | 9 |
| Direct answer | 100 | 97 | No Robots 75 | Dolly 15 | 10 |

The 400 rows sit in 360 groups. No group has more than four rows, and the seven mixed-label groups are M1's. Retrieval used two reserves, for the excluded q0134 and q0174. Thirty accepted rows are not in the release, because their pool quota was full or the keyed-record limit was reached. They stay in the local candidate file.

Every class meets the 40 percent request-type limit and the 75 percent source limit at exactly 100 rows. The largest request types are document question (40), keyed record (40), physics formula (16), and creative writing (27). Each brief cue is at or below its M1 share, as in the import projection.

`scripts/validate_dataset.py data/processed/m3-v1.jsonl --review data/raw/m3-reviews-v1.jsonl --ready` printed `PASS: M1 readiness checks passed (400 accepted rows, 400 reviewed)`. The ledger holds the 128 M1 entries and 272 new ones. AI consistency is 399 of 400. The exception is q0241, which the blind reviewer would have excluded and Altan kept. Both files were made read-only.

**What the labels are.** M1's labels are Altan's own, or agent proposals he approved. M3's 272 new labels are agent proposals that Altan approved by adopting an AI reviewer's judgments. The 400-row release therefore has no independent human agreement figure. The report must say so.

## Grouped split

`prepare-study` validated the release and ledger, recorded the collection brief hash, and called `extend` with the actual M2 manifest hash. Every M2 row kept its partition. New rows were allocated as whole groups.

| Partition | Rows | Groups | New groups | Retrieval | Lookup | Calculation | Direct answer |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Train | 242 | 215 | 151 | 61 | 60 | 60 | 61 |
| Validation | 79 | 72 | 50 | 19 | 21 | 19 | 20 |
| Sealed test | 79 | 73 | 51 | 20 | 19 | 21 | 19 |

The proportions are 60.5, 19.75, and 19.75 percent. The split manifest is committed as `data/splits/m3-split.json`.

## Runs

The runs used commit `92cbd09` from a clean detached worktree, so provenance records `git_dirty: false`. The main checkout held an unrelated uncommitted learning-log entry. The data and results paths point to the main checkout. Thread variables were set to 1 before Python started.

```text
uv run --locked python -m orchestra prepare-study --config configs/m3.json --review data/raw/m3-reviews-v1.jsonl --collection-brief docs/collection-brief.md --out data/processed/m3-prepared.json
scripts/run_experiment.sh --config data/processed/m3-prepared.json --run-id m3-a
scripts/run_experiment.sh --config data/processed/m3-prepared.json --run-id m3-b
python -m orchestra compare --left results/m3-a --right results/m3-b
python -m orchestra select --run results/m3-a --out results/m3-a-selection.json
python -m orchestra report --run results/m3-a --selection results/m3-a-selection.json --train data/processed/m3/train.jsonl --validation data/processed/m3/validation.jsonl
```

Both runs printed `ok` for all 14 configurations. No configuration warned, so no convergence retry ran. `compare` printed `PASS: runs reproduce`. The predictions (`7bac6631…98fa`) and metrics (`036679a7…c367`) are byte-identical across `m3-a` and `m3-b`. `select` and `report` exited 0.

## Validation results

79 validation rows. One row moves accuracy by about 0.013.

| Configuration | Accuracy | Macro-F1 | Median latency, 79-row batch |
| --- | ---: | ---: | ---: |
| B0 | 0.253 | 0.101 | 0.54 ms |
| B1 | 0.886 | 0.883 | 0.48 ms |
| L1-C0.1 | 0.899 | 0.901 | 0.50 ms |
| L1-C1 | 0.911 | 0.912 | 0.51 ms |
| **L1-C10** | **0.924** | **0.925** | 0.50 ms |
| L2-C0.1 | 0.899 | 0.898 | 0.59 ms |
| L2-C1 | 0.911 | 0.910 | 0.59 ms |
| L2-C10 | 0.899 | 0.897 | 0.58 ms |
| S1-C0.1 | 0.911 | 0.910 | 0.59 ms |
| S1-C1 | 0.886 | 0.883 | 0.59 ms |
| S1-C10 | 0.886 | 0.883 | 0.59 ms |
| L3-C0.1 | 0.924 | 0.923 | 0.97 ms |
| L3-C1 | 0.924 | 0.923 | 0.95 ms |
| L3-C10 | 0.924 | 0.923 | 0.97 ms |

**Selection.** Each family keeps its best configuration and any within 0.01 of it, then takes the smallest C. The choices are B0, B1, L1-C10, L2-C1, S1-C0.1, and L3-C0.1. L3 tied at all three C values. Overall, L1-C10 (0.925) and L3-C0.1 (0.923) are within 0.01. The pre-recorded simplicity order then picks **L1-C10**, word counts with logistic regression. The rule was fixed before any M3 score existed.

**Matched comparisons**, second family minus first, in macro-F1:

| Comparison | C 0.1 | C 1 | C 10 |
| --- | ---: | ---: | ---: |
| Counts to TF-IDF (L1 to L2) | -0.003 | -0.002 | -0.028 |
| Logistic regression to linear SVM (L2 to S1) | +0.012 | -0.027 | -0.014 |
| Unigrams to unigrams and bigrams (L2 to L3) | +0.025 | +0.013 | +0.026 |

Every difference is about two validation rows or fewer. The signs are consistent only for bigrams, which helped at every C. No interval or significance test was computed, so none of these differences is established. Counts and TF-IDF are indistinguishable here except at C 10. The SVM's sign depends on C.

**Selected confusion, L1-C10** (rows true, columns predicted):

| | Retrieval | Lookup | Calculation | Direct |
| --- | ---: | ---: | ---: | ---: |
| Retrieval | 17 | 0 | 0 | 2 |
| Lookup | 1 | 19 | 0 | 1 |
| Calculation | 0 | 0 | 19 | 0 |
| Direct | 0 | 1 | 1 | 18 |

Per-class F1 is 0.919 retrieval, 0.927 lookup, 0.974 calculation, and 0.878 direct answer. Every class is predicted. Of its six errors, four are No Robots rows, one is BFCL, and one is an AI draft.

## M2 rows inside M3 validation

The M3 validation set holds the 25 M2 validation rows plus 54 new ones. The agent split the saved predictions to separate the effect of more training data from the effect of a different validation set. This analysis was not pre-registered.

| Configuration | M2 rows (25), errors | M2 rows, macro-F1 | New rows (54), errors | New rows, macro-F1 |
| --- | ---: | ---: | ---: | ---: |
| L2-C1 in M2 (78 training rows) | 7 | 0.730 | n/a | n/a |
| L2-C1 in M3 (242 training rows) | 1 | 0.962 | 6 | 0.887 |
| L1-C10 in M3 | 0 | 1.000 | 6 | 0.890 |

On the same 25 rows, L2-C1 went from seven errors to one. The rows and the model settings did not change, so the gain comes from the larger training set. Altan inspected those seven M2 errors, and M3 collection followed fixed orders that did not use them. L1, L2, S1, and L3 all score lower on the new rows than on the M2 rows, while B1 scores about the same on both. Why is not established. The new rows are longer and come from more sources, which is one hypothesis.

## Class balance and length

Medians in words, from `comparison.md`:

| Class | Train rows | Train median | Validation rows | Validation median |
| --- | ---: | ---: | ---: | ---: |
| Retrieval | 61 | 14 | 19 | 15 |
| Lookup | 60 | 17.5 | 21 | 19 |
| Calculation | 60 | 22 | 19 | 28 |
| Direct answer | 61 | 16 | 20 | 21 |

Classes are balanced to within two rows in every partition. Direct answer has the longest tail, up to 246 words, because it includes rewrite requests with supplied text. Plots are still deferred pending a dependency decision, so these tables stand in for them.

## Resources

Peak process RSS was 161,808,384 bytes for all 14 configurations in one process. The slowest fit, L3-C10, took 0.023 s. Median prediction latency for the 79-row batch ranged from 0.48 to 0.97 ms. These are descriptive figures from one machine, macOS arm64 with 12 CPUs, scikit-learn 1.9.1, NumPy 2.5.3, and SciPy 1.18.1.

## Archive and restored rerun

`work/m3-archive/run.sh` mirrors the [M2 archive](m1-m2-archive.md). It refuses to run if tracked code, configs, splits, manifests, the brief, or the guide have uncommitted changes. It runs the readiness gate and asserts the four hashes `prepare-study` recorded. Then it archives 56 files: the code, lockfile, configs, M1 and M3 releases and ledgers, both split manifests, the prepared config, the train, validation and sealed test files, import provenance and attachments, both runs, the selection, and the report. It restores them into a new directory, compares every file hash, reruns M3 there from a fresh `uv sync --locked`, and compares the rerun with `m3-a`.

```text
PASS: archived M3 inputs match the hashes recorded by prepare-study
PASS: 56 restored files byte-identical to originals
PASS: runs reproduce
```

`restore` printed `"verified": true`. The archive `work/m3-archive/m3-release.zip` (387,602 bytes) has SHA-256 `81e73da8292c50ab68cf140e44d6070b4ac1643aaa038feae671f66a30b36d8c`. The rerun `m3-restored` has the same prediction and metric hashes as `m3-a`. The sealed test file was copied as bytes and never opened. The zip stays local, on this host, in the ignored `work/` folder.

## Not established

- **Test performance.** The sealed test file was never opened. M4 evaluates it once, after the systems and any confidence threshold are frozen.
- **Error inspection.** The protocol asks a human to inspect at least 20 validation errors across predicted and true classes. `errors.jsonl` lists them locally, and that inspection belongs to M4.
- **Differences between families.** 79 rows cannot separate configurations two rows apart. A grouped resampling interval was not computed.
- **Human agreement.** The new labels are human-adopted AI judgments, and the release has only AI consistency.
- **Source cues.** Sources still align with classes: GSM8K appears only in calculation, and the AI drafts only in lookup. BFCL spans calculation and lookup, and Dolly and No Robots each span retrieval and direct answer, which dilutes the M1 confound but does not remove it.
- **Generality.** One host, one seed, one split. The runs reproduce byte for byte. That shows determinism, not generalization.

## Local files

| File | SHA-256 |
| --- | --- |
| `data/processed/m3-v1.jsonl` (read-only) | `4e9425fd65e2572bff1c7fefd9ef21692bf219479818903d4ec33a372fc55bbf` |
| `data/raw/m3-reviews-v1.jsonl` (read-only) | `e56b73a22a0e95893fb19efcbde1717ae803fb52ffa0ce668cbceb384a3248e9` |
| `data/splits/m3-split.json` (committed) | `6d48e18bae6ac319bffecc98c68b6b02c8c4483f68a75eddb63db2a52213225f` |
| `data/processed/m3-prepared.json` | `b19fccf5565eb1673f034678e682751f7e8993c6e85501c6ad95e7bca6754ecc` |
| `data/processed/m3/train.jsonl` | `5b6b6254028e910c73db7c9588ddff8d1a4a7598aed25140adb275086289d3dd` |
| `data/processed/m3/validation.jsonl` | `5cdda69c02ce8c90fe45a16348fb53d3c84e7efa048d72891129b086149756b6` |
| `docs/collection-brief.md`, as recorded by `prepare-study` | `d9238b34b573438c648ebd90cd4bc8564b2a6698ccba7b26ee8d0726d5105233` |
| `results/m3-a/predictions.jsonl`, equal to `m3-b` | `7bac66319eee0fdaa929d8838bf42a8f1a68907df55c66117c81bd94541598fa` |
| `results/m3-a/metrics.json`, equal to `m3-b` | `036679a7f1e769b2f0514e22cd8f5c55dc0c256012767c8630bb29728a9cc367` |

The adjudication decision is in `work/poteto/m3-import/adjudication-2026-10-28.json`, and `apply_adjudication.py` refuses to run unless the candidates, ledger, proposal, and worksheet match the reviewed versions.
