# M6 clean reproduction, November 10, 2026

On November 10, 2026, a fresh clone of the project from GitHub, plus one local study archive, reran the M3.5 and M4 study from the frozen release to the report figures. Every split, prediction, metric, confidence result and figure matched the saved originals. The remaining differences are times, commit and code hashes, and hashes of files that record times. Each is listed below with its cause. Jev's answers were replayed from the archived logs; no query was sent to TypeSafe. This is research reproduction evidence for [issue #9](https://github.com/AltanEsmer/Orchestra/issues/9). It does not establish Altan's understanding, which the oral rehearsal records separately.

## What changed in the code

- `final-test --replay-jev-test` (commit `b2bc633`). The frozen decision set includes Jev, so the final test could only obtain Jev's test answers by sending the sealed queries again. The new option reads the archived log at the frozen path with a request budget of zero. A missing answer fails instead of sending, and the output provenance records `jev_test_replayed: true`. In a checkout whose receipt for this split is complete, a replay to another output path is still refused. Commit `ff53b10`, after review, records `jev_replay` in the receipt so a failed replay cannot be resumed as a send. A unit test covers the refusal, a partial log, the refused mode switch and a byte-identical replay.
- `scripts/archive_study.sh`, `scripts/reproduce_study.sh` and `scripts/compare_study.py` (commit `ad65169`, tightened in `8749e06` after review). They archive the ignored inputs and outputs, rerun the documented commands in a clean clone, and compare the results.
- `scripts/route_query.py` (commit `b6e0024`, corrected in `652426b`). It routes a new query through the frozen logistic system for oral practice. A unit test shows that routing a saved test text reproduces its saved raw and calibrated probabilities. The first version labelled every word outside the model's vocabulary "never seen in training". L3-C10 keeps only the 10,000 most frequent n-grams, so a training word can still be missing. The corrected tool reports each such word with its training-row count.

## Archive

`scripts/archive_study.sh /Users/altanesmer/Desktop/SM1/AI/Orchestra ../Orchestra/work/m6-reproduction/orchestra-study-m6.zip`, run from the M6 worktree beside the original checkout, archived 171 files. That first version resolved a relative output path from the caller's directory and then changed directory; both coincided here. Commit `8749e06` resolves the path first. A rebuild with the fixed script from another directory listed the same 171 files in the same order; its ZIP bytes differ only because ZIP entries store file times, so the archive below stays the recorded one.

| Item | Value |
| --- | --- |
| Location | `/Users/altanesmer/Desktop/SM1/AI/Orchestra/work/m6-reproduction/orchestra-study-m6.zip` (ignored, local only) |
| Size and SHA-256 | 5,382,029 bytes, `38a3ab56a2641f313cc21394afd02afdce87bdbebf99a9ebecdca410272bdc6b` |
| File list and manifest | `orchestra-study-m6.files.json` and `orchestra-study-m6.manifest.json` beside the ZIP |
| Inputs | `m3-v1.jsonl`, `m3-5-v1.jsonl`, `m3-5-reviews-v1.jsonl`, `types.json`, `pairs.json`, Jev validation, repeat and test logs, validation and test interpretation ledgers |
| Saved outputs | prepared configs, split files, run `m3-5-full-a` with selection and report, `m4-5-validation`, the freeze, `final-test-m3-5`, the test receipt, `m5-figures` |

The archive contains query text, including the 628 sealed test rows. It stays on this machine. Publishing or submitting it needs Altan's decision and the source licences.

## Clean environment

`git clone https://github.com/AltanEsmer/Orchestra.git` into `work/m6-reproduction/clean`, checked out at `8749e06f6b8c201707fae275b46f507e5ccd7cc8`, the final code commit of this branch. `git status --porcelain --ignored` was empty before the run. `UV_CACHE_DIR` and `UV_PYTHON_INSTALL_DIR` pointed at new empty folders, so `uv python install 3.12.13` downloaded Python into the new folder and `uv sync --locked` downloaded all 21 locked packages. The install command also reported that it could not replace an existing `python3.12` shim in `~/.local/bin`; the clone's `.venv` reports its base interpreter in the new folder, so the shim was not used.

| Item | Value |
| --- | --- |
| Tools | uv 0.11.7 (Homebrew); Python 3.12.13; `uv.lock` `13bdff21661cf0a421c5ba00c3e1c7ad4e08c0247924e620d8c74f7d44f61929` |
| Libraries | scikit-learn 1.9.1, NumPy 2.5.3, SciPy 1.18.1, XGBoost 3.4.1, Matplotlib 3.11.2 |
| Machine | macOS 27.0 arm64, Apple M4 Pro, 12 cores; `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `VECLIB_MAXIMUM_THREADS` set to 1 |
| Command | `scripts/reproduce_study.sh /Users/altanesmer/Desktop/SM1/AI/Orchestra/work/m6-reproduction/orchestra-study-m6.zip` |
| Wall time | 96.4 s, including the package downloads |
| Log | `work/m6-reproduction/clean/work/m6-reproduction/reproduce.log`, 323 lines |

## Study identities

| Item | SHA-256 |
| --- | --- |
| Release `data/processed/m3-5-v1.jsonl` | `be747dda8fd9f7c2ee432fa4ab29d6577607212b4d5a678d82205fef3386b2a8` |
| Template `configs/m3-5.json`, seed 42 | `2b016c6355a6913b55db78197b9f51cd2de8cdf320548505b824d7a0828d3e8c` |
| Split manifest `data/splits/m3-5-split.json` | `7aacbc497dd462e56a5fbcb3b5546c056ed4f835e35d0cf61334f17ce3a45e10` |
| Train, validation, sealed test | `dd3308af151e44ac242b639d6e4ba7e304156f6a26e93a3ff853e4cb5dc12bca`, `0e9dc93459342ccf173ab921136ce3bb30670519ccc33f4f92d3c98e7e888691`, `baab0310b51c940d8a7a3e805ceeeb8f865b175429dcb7ab3c06cdb3685a7ab5` |
| Jev validation log, test log | `1f68d2f3534c2d5649f80f2caabef0eda2ddd6a37f28390b59858e0dc566f839`, `bcdb69f2db765309d2504ff5ee2c1bdcb3e85b035644c0988f10d11bc935a105` (628 requests) |
| Freeze, original and reproduced | `e71f5b80e1f85f3d548772a4e3b93ec2ed0af0e1cd0b35964669b729cd2a6284`, `736c86642646cb204aff788348f93007ff818a104c7b017dee2cc2776e7bd269` |
| Final-test manifest, original and reproduced | `9b9b7f2103e325dabbfd53177f5bba2bba6da5e13ea488f3cb1ae1dee664b94a`, `9c3de520ed5225b7c48241427f393ec713dbeb08564235cf04c3fcb0b8dc9e3a` |

## Commands and their output

The script ran these commands in order. Each printed `PASS`.

- `validate_dataset.py --ready`: M1 readiness checks passed, 3,145 accepted rows, 3,145 reviewed.
- `check-collection`: M3.5 collection checks passed.
- `prepare-study`: wrote the extension; the tracked split manifest was rewritten byte-identically, which the immutable writer requires.
- `run_experiment.sh --run-id m6-repro`: all 27 configurations, Jev replayed from its validation log.
- `select`: overall Jev. `report`: Jev 17, L3-C10 29 validation errors, as in M4.
- `confidence`, `freeze` with the archived validation interpretations and the Jev test-log path.
- `final-test --replay-jev-test`: Jev 0.963646, S1-C1 0.945427, L3-C10 0.927873 test macro-F1.
- `test-review`: Jev 26 of 26 and L3-C10 41 of 41 errors interpreted, each with one correct comparison.
- `figures`, then `report/plot_reliability.py` followed by `git diff --exit-code -- report/figures`, which found no change.

## Comparison

`scripts/compare_study.py` printed the following, unedited.

```text
PASS: split, 3 files
PASS: collection check, 1 files
PASS: prepared configs, 2 files
PASS: validation run, 1 files
PASS: selection, 1 files
PASS: validation errors, 1 files
PASS: confidence, 8 files
EXPECTED: freeze: 1 x /confidence_manifest_sha256: hashes a file that records run times
EXPECTED: freeze: 1 x /config/code_hashes/*/src/orchestra/__main__.py: changed after the freeze
EXPECTED: freeze: 1 x /config/code_hashes/*/src/orchestra/confidence.py: changed after the freeze
EXPECTED: freeze: 1 x /config/hashes/*/results/{run}-selection.json: hashes a file that records run times
EXPECTED: freeze: 1 x /config/hashes/*/results/{run}/manifest.json: hashes a file that records run times
EXPECTED: freeze: 1 x /frozen_utc: time of the rerun
EXPECTED: freeze: 1 x /git_sha: commit of the rerun
PASS: freeze, 1 files
PASS: final test, 7 files
PASS: figure data, 1 files
PASS: figure images, 78 files
EXPECTED: figure provenance: 40 x /sources/confidence/manifest.json: hashes a file that records run times
EXPECTED: figure provenance: 40 x /sources/final/manifest.json: hashes a file that records run times
EXPECTED: figure provenance: 40 x /sources/run/manifest.json: hashes a file that records run times
EXPECTED: figure provenance: 40 x /sources/selection.json: hashes a file that records run times
EXPECTED: figure provenance: 40 x /files/*: hashes the figure provenance files above
PASS: figure provenance, 41 files
PASS: report figures and figure set
PASS: study reproduces
```

Byte checks cover the three split files and all 78 PNG and SVG figures. JSON checks compare full parsed content after mapping the original folder to the clone and run ID `m3-5-full-a` to `m6-repro`. The validation run uses the project's `compare`, which allows probability differences up to 1e-10. The two changed source files are `src/orchestra/__main__.py` and `src/orchestra/confidence.py`, changed after the freeze by commits `ffba6d4` and `ae5b6cf` (test review) and `b2bc633` and `ff53b10` (replay). A change to any other recorded code file or to `uv.lock` would fail the check. The last line also confirms that the reproduced figure folder holds no file the original lacks. `comparison.md` in the run report is not compared: its 27 table rows differ only in the latency column.

**The gate can fail.** In the evidence clone, one test prediction in `final-test-m3-5/predictions.jsonl` was changed to another class and one byte of `word-lengths.png` was flipped. The comparer printed `DIFF` for both files and for the report figure copied from the second, then `FAIL: reproduction differs`, and exited with status 1. After both files were restored it printed `PASS: study reproduces` with status 0. The output is kept in `work/m6-reproduction/clean/work/m6-reproduction/tamper-check.log`.

## Report and routing checks

- **Report.** Tectonic 0.17.0, outside the locked environment, compiled `report/main.tex` from the clean clone to seven pages. `pdftotext -layout` output is identical to that of the current reading copy `output/pdf/M5-report-draft.pdf` (`7dd14182…`). The PDF bytes differ because the file embeds build metadata. `git status` in the clone stayed empty.
- **Routing tool.** `scripts/route_query.py` on q0005, an Altan-authored validation row, returned raw L3-C10 calculation 0.8045 and calibrated 0.8853. These equal the saved `results/m4-5-validation/predictions.jsonl` values traced in the M4 guide. It reports "ticket" as never in training and "kr" as in one training row but dropped by the feature cap.
- **Earlier run.** The same reproduction at commit `ad65169`, before the review fixes, also printed `PASS: study reproduces`. That clone is kept in `work/m6-reproduction/clean-ad65169`.

## Limitations

- The clean run used the same Mac. Another platform could change low-order digits. Not tested.
- Jev's answers were replayed, not requested again. This proves the computation from answers to results, not that Jev would answer the same way today. On November 2 a repeat changed 2 of 629 validation top choices.
- The reproduction ran current code (`8749e06`), not the exact commits of the original runs. It shows the code to be submitted reproduces the reported results.
- Labels, review decisions and interpretation ledgers are inputs. The reproduction does not check that they are right.
- Latency and timing are excluded from every comparison.
- Only the M3.5 and M4 study behind the report is covered. M1 to M3 have their own archive records.
- Receipts live in each checkout's ignored `results/`. The clean clone's replay read the sealed test rows and wrote its own receipt there. It changed no decision, because the freeze was rebuilt from validation before the test was read and matched the original, but the receipt guard itself is per checkout. Protocol discipline, not code, keeps a copy from being used to try new decisions on the test.
- The script does not create the fresh package cache and Python folder; the evidence run set `UV_CACHE_DIR` and `UV_PYTHON_INSTALL_DIR` by hand.
