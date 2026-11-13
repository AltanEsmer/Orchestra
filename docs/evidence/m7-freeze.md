# M7 submission package verification, November 13, 2026

M7's technical deliverables are complete. The milestone stays **in review** because Altan explicitly chose "Keep author review pending" on November 13. His actual result-and-replay explanation passed the bounded learning checkpoint and is recorded in the [learning log](../learning-log.md#m7-result-and-replay-teach-back-november-13-2026). The full M6 rehearsal and other knowledge gaps remain visible. Nothing has been submitted or uploaded. This record supports [issue #10](https://github.com/AltanEsmer/Orchestra/issues/10).

## Frozen identities

The package is `/Users/altanesmer/Desktop/SM1/AI/Orchestra-submission/Orchestra-M7-2026-11-13.zip`, 7,899,146 bytes. Its SHA-256 is `8f0576edb96411f419ae1ba66e698a83df230c767303d0064fcae1d755e6108f`. A `.zip.sha256` file beside it verifies the outer ZIP. The unpacked review copy is `Orchestra-submission/2026-11-13-m7/`. The [machine-readable record](m7-package.json) preserves this identity and the package manifest.

The exact source revision is `49074f8534c376b2168563e806d1f277e0df7043`. The self-contained bundle has branch `codex/m7-freeze` at that revision. `git bundle verify` passed and reported complete history. The source ZIP's 127 tracked files were compared byte for byte with that commit. Both contain the lockfile, source manifest, licenses, report source and tracked figures. The later documentation-only evidence commit records the verified package without changing its code, report or guide. Its current roadmap supersedes the historical tracker inside the frozen source snapshot.

M6 [PR #36](https://github.com/AltanEsmer/Orchestra/pull/36) merged as `4a5b17c7343f065c429b9c13ec1af3ce94438d6a`. The independent reviewer verified head `9d9d3d78fa1a4801befded268af61ce29775d8c9`, base `47ab65aec3ab05930454e5189554ece19059f5f0`, and stable patch ID `e0dd926a8adbb18addafeec572108b719a6ba170`. The lead rechecked these identities and green CI immediately before merging. Detailed commits were preserved.

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| `Orchestra-report.pdf` | 296,391 | `4fb5b1c0e747af8db6b0df522f3671d39bc1da1c32edf1dabec10a69cc52db40` |
| `orchestra-code.bundle` | 1,227,760 | `0e6fb962198b997f8288ac07ad4937cac34ffac7ef26e973785131147f33ce93` |
| `orchestra-source.zip` | 1,049,052 | `a44609f3a974f45403f50e68b5eeb829f19e6603168f6610ebc7049df4e829b8` |
| `orchestra-study-m6.zip` | 5,382,029 | `38a3ab56a2641f313cc21394afd02afdce87bdbebf99a9ebecdca410272bdc6b` |
| `M7-freeze.pdf` | 12,812 | `f324d51a7c15e00895c70785d07af07ef97a220f74c1f7bffd61749efb2bc4eb` |

The package also contains the archive file list and manifest, the M7 guide provenance sidecar, a reproduction README, verification logs and optional local audit scripts. `SHA256SUMS` covers all other package files, including `manifest.json`. All 20 entries passed. The study archive is the unchanged M6 ZIP, with 171 payload files and its embedded manifest. Query text remains local. No credentials, course PDFs, unapproved new data, or download caches were added. The original checkout's uncommitted notes and outputs were preserved.

## Actual verification

| Check | Observed result |
| --- | --- |
| `sh scripts/check.sh` | Locked setup and smoke passed; 287 tests passed in 51.681 seconds; Ruff lint passed; 98 files formatted; whitespace passed. Final lint and format recheck also passed, with 99 files reported. |
| `verify_workflow.py --out work/m7-freeze/fixture-proof` | `PASS: artificial workflow, 24 commands`. These remain fixtures, not research evidence. |
| Bundle restore | Cloned the delivered bundle into `work/m7-freeze/clean`; HEAD equals the source revision; tracked status clean before and after reproduction. |
| Clean setup | Python 3.12.13 downloaded into a new task-local folder; uv used a new empty cache; locked dependencies synchronized. The task-local shim is outside PATH, but `.venv` uses the new interpreter. |
| `scripts/reproduce_study.sh` with the packaged study ZIP | `PASS: study reproduces`. Every split, prediction, metric, confidence decision and figure matched under the existing comparison rules. Jev replies were replayed; no service request occurred. |
| Report rebuild | Tectonic 0.17.0 compiled the corrected source to seven US Letter IEEE two-column pages. Rebuilding from the bundle clone gave identical `pdftotext -layout` output. Every final rendered page was inspected. Only underfull box warnings remained; no clipping or missing references observed. |
| Independent numeric audit | Recomputed accuracy, macro-F1 and confusion counts from saved predictions for 27 validation and 11 test configurations; all five tables and four figure sidecars/source hashes passed. |
| Citation audit | All 22 entries are cited. Five private repository citations matched their pinned Git objects through authenticated GitHub reads. External primary sources were checked for identity and relevant content. |
| M7 guide | Five pages, all inspected. Every source line/table cell appears in extracted text after markup/whitespace normalization. No missing course source. Stable PDF plus dated review snapshot retained. |
| Package | Bundle verified; source ZIP matched all tracked bytes; all package checksums passed. |

The full rerun log is `work/m7-freeze/clean/work/m6-reproduction/reproduce.log`. It is also included under `verification/` in the package. The run compares three split files, the 27-configuration validation run, selection, error records, eight confidence files, rebuilt freeze, seven final-test files, figure data, 78 images and 41 figure provenance files. Expected differences are the named time, commit and code-hash rules and hashes of timed files from M6. Timings are excluded.

The report audit scripts and hashed input records remain at `work/m7-freeze/audit/` in the M7 worktree. Packaged copies preserve the audit, with their local absolute-path limitation stated in `verification/README.md`. Portable reproduction uses the existing script. The repository is private, so unauthenticated citation URLs return 404; authenticated content was verified. Live upstream cards were checked without revalidating every frozen upstream revision.

## Report corrections and course review

The old manuscript described complete reproduction as unfinished M6 work. It now cites the completed run and distinguishes replayed replies from fresh service behavior. The bibliography no longer labels a moving stable documentation URL as version-specific. Independent review found MASSIVE's request to cite its SLURP seed corpus; the report now includes the verified EMNLP 2020 citation. Results, figures, labels, selection and confidence handling did not change.

The lead rechecked the course requirement pages and relevant Lecture 6/7 pages, with no lecture newer than Lecture 8 present. Exact pages and hashes are in the [guide](../study-guides/m7-freeze.md) and [course source record](../course-sources.md#m7-source-review-november-13-2026). The report retains the assistance paragraph and explicit own-word revision status.

## Remaining limits and later changes

- Altan's own-word report review is pending by his explicit instruction. M7 is in review, not administratively complete. M8 submission and receipts are untouched.
- The result/replay answer is recorded evidence of understanding for that question. It does not complete the unfamiliar-query M6 rehearsal or establish every model concept. The prioritized backlog is in the learning log.
- Reproduction used the same Mac and cached Jev replies. It does not establish live service stability, cross-platform equality, label correctness or real-user transfer.
- Preserve this package. A correction requires a new commit, affected checks, rebuilt artifacts and a new dated package with new hashes. Do not silently replace this edition.

Poteto's **Prove It Works** principle led to a clone from the actual delivered bundle and a complete research rerun. **Sequence Work into Verifiable Units** led to the independent M6 merge verdict, the source freeze, then this evidence-only follow-up. Review used gpt-6.1-sol at high reasoning, with implementation assistance from the same model family at low reasoning. No cross-family review is claimed.
