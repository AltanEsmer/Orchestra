# M3 comparison tooling evidence (P5)

**Fixture only. No research claim, no accuracy threshold.** Everything below ran on the artificial P4 fixture (48-row parent, 96-row child, source `fixture`, texts such as `artificial fixture text cal-g5-0`) in a scratch directory outside the repository (`<tmp>`). Class labels are trivially recoverable from the generated query IDs, so the high scores say nothing about routing quality. The run shows that the tooling executes, reproduces, selects and reports; it does not show anything about Orchestra data.

Code commit under test: `3a151ee` (`git_dirty: false` in provenance; the live run used a detached `git worktree` of that commit because the main checkout had an unrelated uncommitted edit). Environment: macOS arm64, `cpu_count` 12, scikit-learn 1.9.1. Every command was prefixed with `env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1` so the variables exist before Python starts; `provenance.json` records them under `thread_env` and the loaded native pools under `threadpools` (`threadpoolctl.threadpool_info()`: one OpenMP pool, `libomp` from scikit-learn, `num_threads: 1`).

Correction: the first version of this record (commit `464760c`, run at `cc967fc`) set only three variables, omitted `VECLIB_MAXIMUM_THREADS` (Accelerate on macOS) and captured no thread-pool information, so its claim of single-threaded execution was not fully established. This record replaces it.

## Contracts implemented

- 14 configurations from `configs/m3.json`: `B0`, `B1`, then `L1`, `L2`, `S1`, `L3` at C 0.1, 1, 10. IDs follow `f"{C:g}"`: `L1-C0.1`, `L1-C1`, `L1-C10`. A test asserts the exact list.
- LinearSVC: in scikit-learn 1.9.1 `multi_class` exists with default `"ovr"` and passing it or not raises no warning (checked with `-W error`). It is left implicit; the resolved parameters saved in `config.json` show `multi_class: ovr`, `penalty: l2`, `loss: squared_hinge`, `dual: auto`, `tol: 0.0001`, `max_iter: 1000`, `random_state: 42`. Retry limit 10,000 for the whole S1 family. Scores are `decision_function` margins in LABELS order with `score_type: margin`.
- Latency: after fitting, one warm-up `predict` on the whole validation batch, then 30 timed `predict` calls (`time.perf_counter`); median and nearest-rank p95 (the 29th of 30 sorted values), batch size, and repetitions are saved in `timing.json`. `predict` includes vectorization. `compare` still ignores timing.
- Plots are deferred pending a dependency decision (no matplotlib). The class and length "figures" are the tables in `comparison.md`.
- `report` has no `--out`: it writes `comparison.md` and `errors.jsonl` (the latter holds validation text) to `<run parent>/<run_id>-report/`, a sibling of the run under the ignored `results/`, refusing an existing directory. It takes `--train` as well as `--validation`, because the class-count and length tables need both inputs and both are hash-checked against the run's provenance. `select` is invalid unless the run is exactly the 14 required IDs (`complete_matrix`, `missing`, `unexpected`). `report` on an invalid selection still writes its files, headed `INVALID selection:`, and exits 1. The 0.01 tolerance is inclusive; with one winner per family the overall latency and ID tie-breaks cannot trigger and are kept only because the protocol declares them. It also recomputes the selection from the run and refuses a `selection.json` that differs (other than the `run` path).

## Commands and outputs

`P` below stands for `env OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 uv run --locked python -m orchestra`.

```text
P split   --config <tmp>/split.json       # parent, PASS
P extend  --config <tmp>/m3.json          # PASS: extension written to <tmp>/splits/m3.json
P run --config <tmp>/m3.json --run-id p5-a   # exit 0, separate process
P run --config <tmp>/m3.json --run-id p5-b   # exit 0, separate process
```

Both runs printed `<id>: ok` for all 14 configurations and `PASS: run written to <tmp>/results/p5-x`. No configuration warned, so no convergence retry occurred in the live run (retry paths, including S1 at 10,000 and logistic regression at 1,000, are covered by tests that force a warning). Running with `VECLIB_MAXIMUM_THREADS` unset printed `WARNING: thread variables not set before start: VECLIB_MAXIMUM_THREADS`. Hashes: dataset `005e2508...a8d05f`, split manifest `3f0ae8a8...c64734` (as in the P4 evidence).

```text
$ P compare --left <tmp>/results/p5-a --right <tmp>/results/p5-b
PASS: runs reproduce

$ P select --run <tmp>/results/p5-a --out <tmp>/selection.json
B0: B0
B1: B1
L1: L1-C0.1
L2: L2-C1
S1: S1-C0.1
L3: L3-C1
PASS: overall L1-C0.1; written to <tmp>/selection.json

$ P report --run <tmp>/results/p5-a --selection <tmp>/selection.json \
    --train <tmp>/m3/train.jsonl --validation <tmp>/m3/validation.jsonl
B0: 14 validation errors
B1: 4 validation errors
L1-C0.1: 2 validation errors
L2-C1: 2 validation errors
S1-C0.1: 2 validation errors
L3-C1: 2 validation errors
PASS: report written to <tmp>/results/p5-a-report

(same command again)
ERROR: <tmp>/results/p5-a-report already exists; report needs a new directory
```

After moving the first report aside, a second report produced `comparison.md` and `errors.jsonl` byte-identical (`cmp`) to the first. `comparison.md` sha256 `f51150cdf357b3384e1f2c5fd30c40e42038731e92fbf2ca72aeabb791b0c38c`; `selection.json` sha256 `96a24fdb41c4f9ff3f7c8715d29db2a0ea1044b1d25b2143fe2aff0f95c5113c` (embeds the run path). `errors.jsonl` has 26 rows (14 + 4 + 2 + 2 + 2 + 2), sorted by query ID; texts are in the file only, never printed.

### Selection (valid: true)

Tie sets: B0 {B0}; B1 {B1}; L1 {L1-C0.1, L1-C1, L1-C10}; L2 {L2-C1, L2-C10}; S1 {S1-C0.1, S1-C1, S1-C10}; L3 {L3-C1, L3-C10}. Overall tie set {L1-C0.1, L2-C1, S1-C0.1, L3-C1}; simplicity order gives L1-C0.1. The macro-F1 ties are exact (0.9143 for every non-degenerate configuration) because the fixture is trivially separable, so the overall pick shows the simplicity rule only.

### Validation table (from `comparison.md`; latency is median seconds over the 20-row validation batch)

| Configuration | Status | Accuracy | Macro-F1 | Median latency (s) |
| --- | --- | --- | --- | --- |
| B0 | ok | 0.3000 | 0.1154 | 0.000158 |
| B1 | ok | 0.8000 | 0.7976 | 0.000106 |
| L1-C0.1 | ok | 0.9000 | 0.9143 | 0.000111 |
| L1-C1 | ok | 0.9000 | 0.9143 | 0.000109 |
| L1-C10 | ok | 0.9000 | 0.9143 | 0.000112 |
| L2-C0.1 | ok | 0.5500 | 0.4929 | 0.000203 |
| L2-C1 | ok | 0.9000 | 0.9143 | 0.000199 |
| L2-C10 | ok | 0.9000 | 0.9143 | 0.000198 |
| S1-C0.1 | ok | 0.9000 | 0.9143 | 0.000198 |
| S1-C1 | ok | 0.9000 | 0.9143 | 0.000197 |
| S1-C10 | ok | 0.9000 | 0.9143 | 0.000198 |
| L3-C0.1 | ok | 0.5000 | 0.3864 | 0.000223 |
| L3-C1 | ok | 0.9000 | 0.9143 | 0.000223 |
| L3-C10 | ok | 0.9000 | 0.9143 | 0.000224 |

Matched-C tables (L1 vs L2, L2 vs S1, L2 vs L3), class and length tables, and raw confusion matrices of the six selected configurations are in the same `comparison.md`; each cites run `p5-a` and its source file. The only non-zero matched-C differences are at C=0.1 (L2 is under-fit at the strongest regularization on this tiny fixture).

### Resources (descriptive; one tiny fixture, not a ceiling check)

- Peak process RSS from `timing.json`: 150,044,672 bytes (run a), 150,323,200 bytes (run b), about 143 MiB for all 14 configurations in one process, against the proposed 8 GB ceiling.
- Largest per-configuration fit: 0.0031 s (run a), 0.0020 s (run b); proposed ceiling 15 minutes.
- p95 prediction latency ranged 0.111 to 0.230 ms per 20-row batch in run a.

## Behavior covered by tests (not by this live run)

Failed, unresolved-warning and warned configurations, or a run that is not the 14 required IDs, make `select` write `"valid": false`, list them under `blocking` or `missing`, choose nothing, and exit 1; a gap of 0.011 does not tie while 0.01 does; the overall order picks the simpler family despite worse latency; a failed attempt records the `max_iter` actually tried; a whole family reruns at the retry limit when one member warns; `report` fits nothing (patched `Pipeline.fit` raises), refuses a validation file whose hash differs from provenance, an existing report directory, and a selection that does not match the run.

## Open gates (not satisfied by this tooling)

- The real frozen 400-row dataset and split do not exist; no real comparison has been run.
- A human has not inspected at least 20 validation errors; `errors.jsonl` only provides the list, and the error note is not written.
- Archive and restore of the frozen dataset, split and run is not done.
- Class and length plots are deferred pending a dependency decision; tables stand in.
- M4 work (calibration, thresholds, test evaluation) is untouched; the sealed test file is never opened.
- Timing is one machine, one batch size, one process; it is descriptive only.
