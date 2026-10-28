# M1 and M2 input archive and restored rerun

On October 28, 2026, Altan asked to complete M1 and M2. Both milestones still lacked a verified archive of their inputs. This record covers the M1 archive step in the [runbook](../run-experiments.md#release-the-first-dataset) and the remaining M2 archive and restore gate in the [roadmap](../../ROADMAP.md#milestones).

## What the archive holds

The archive holds 47 files. Their paths are repository-relative.

- **M1 release.** It holds `data/processed/m1-v1.jsonl`, the `reviews-v2` ledger, `docs/annotation-guide.md` as the guide revision, and the current `data/manifests/sources.json` permission manifest. It also holds the readiness output, which printed "PASS: M1 readiness checks passed (128 accepted rows, 128 reviewed)".
- **M2 inputs at M2 time.** The sources manifest and collection brief changed after M2, in commits `afd6ee6` and `7cf7473`, when GSM8K was recorded. Their versions from commit `d541de9` are archived under `work/m2-archive/at-m2/`. A scripted check confirmed that they match the hashes `prepare-study` recorded, `67cfe73f…` and `bbfa7ead…`.
- **M2 split and runs.** It holds `configs/m2.json`, the prepared config, the split manifest, the train, validation and sealed test files, and every file of `results/m2-a` and `results/m2-b`.
- **Code.** It holds `src/orchestra`, the runner, the validator, `pyproject.toml`, `uv.lock` and `.python-version` at commit `07263b4`.

The sealed test file was copied as bytes. Nobody opened or evaluated it.

## Commands and results

`work/m2-archive/run.sh` performs the whole sequence and can be rerun. Its directory is ignored by Git. In order, the script does the following:

1. Refuses to run if tracked code, configs, splits or manifests have uncommitted changes.
2. Runs the readiness gate and saves its output.
3. Extracts the M2-time manifest and brief, then asserts all four hashes recorded by `prepare-study`.
4. Runs `orchestra archive` and then `orchestra restore` into a new directory.
5. Compares the SHA-256 of every restored file with its original.
6. Rewrites the prepared config's absolute paths to the restored directory, runs `uv sync --locked` there, and reruns M2 as `m2-restored`.
7. Compares `m2-restored` with `m2-a`.

Actual output, October 28, 2026:

```text
PASS: archived M2 inputs match the hashes recorded by prepare-study
PASS: 47 restored files byte-identical to originals
B0: ok
L2-C1: ok
PASS: runs reproduce
```

| Artifact | SHA-256 |
| --- | --- |
| `work/m2-archive/m2-inputs.zip` | `253f110335b5327b3a256d52452be3b484fe0614de0ffe3c9321944a4b529d0b` |
| `m2-restored` predictions, equal to `m2-a` | `6064c0b106ce97a1fe85012dac4861001e6c8e4fbdec6d4c8b6bf76be8d5174d` |
| `m2-restored` metrics, equal to `m2-a` | `1690ecd372d57552671ff23db6129b7b48888276c9ba0c9a7eb9f23bbb59ceb4` |

`restore` verified every member hash and printed `"verified": true`. The rerun's provenance differs from `m2-a` only in the run ID, timestamps, git commit and thread-pool details.

## Limits

- **One host.** The archive was made, restored and rerun on the same macOS arm64 machine. It shows that the saved inputs and locked environment reproduce M2 from a fresh directory. It does not show cross-platform reproduction.
- **Local only.** The zip sits in the ignored `work/` folder of this checkout. A copy to separate storage is still Altan's call. The archive manifest states that dataset redistribution permission is a separate decision.
- **Current manifest for M1.** The M1 entry is today's `sources.json`, which adds GSM8K. The M2-time copy that `prepare-study` hashed is also in the archive.
