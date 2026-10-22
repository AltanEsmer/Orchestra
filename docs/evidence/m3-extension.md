# M3 extension tooling evidence (P4)

Everything below ran on an artificial fixture in a temporary directory outside the repository: a 48-row parent (source `fixture`, 4 classes x 6 groups x 2 rows, two mixed-label groups, the P2 fixture) and a 96-row extension that keeps those rows byte-identical and adds 24 new independent groups (4 classes x 6 groups x 2 rows). **No research extension exists.** The numbers describe the fixture, not Orchestra data, and say nothing about routing quality.

## Live run

```text
python -m orchestra split  --config <tmp>/split.json     # parent, PASS
python -m orchestra extend --config <tmp>/extend.json   # config pins parent_manifest_sha256
```

Output of `extend` (exit 0, path shortened to `<tmp>`):

```text
{
  "counts": {
    "train": {"document_retrieval": 12, "knowledge_lookup": 14, "calculation": 16, "direct_answer": 18},
    "validation": {"document_retrieval": 6, "knowledge_lookup": 4, "calculation": 4, "direct_answer": 6},
    "test": {"document_retrieval": 4, "knowledge_lookup": 4, "calculation": 4, "direct_answer": 4}
  },
  "proportions": {"train": 0.625, "validation": 0.2083, "test": 0.1667},
  "new_groups": {
    "by_class": {"document_retrieval": 6, "knowledge_lookup": 6, "calculation": 6, "direct_answer": 8},
    "by_partition": {"train": 15, "validation": 5, "test": 4}
  }
}
PASS: extension written to <tmp>/splits/m3.json
```

(The real output prints each count on its own line; compacted here.) Observations:

- Achieved combined proportions are 62.5 / 20.8 / 16.7, not exactly 60/20/20, because whole groups move together.
- Independent groups: 24 parent plus 24 new, 48 in total. New groups per partition are 15, 5, 4. `direct_answer` shows 8 new groups because two mixed-label groups count once under each label they contain.
- A second identical run printed `PASS` again (byte-identical manifest accepted). Files: train 60 lines, validation 20, sealed test 16 (`wc -l`), 96 in total.
- A direct script check confirmed each parent partition is a subset of the same child partition, and the intersection of parent validation IDs with child test IDs is `set()`: M2 validation did not become M3 test.
- SHA-256: parent dataset `99e9428b75b9e1d5e3cc3ae4313dcf07931b69f99226aa6b915f5415810a94cd`, parent manifest `4448ecc3501b6cfd1fbf941854aefab895ed8e69711eff217ad5bd74ffcb10c4`, child dataset `005e25081e3eb97b3e42ea6dc7e3d4e2f04131f25a3ca89f3ef40bf6b9a8d05f`, child manifest `3f0ae8a8d7b8d07d78aa87111874fe58861c581a1d72239dad779ec8b3c64734`. The child records the first, second, and third as `parent_dataset_sha256`, `parent_manifest_sha256`, and `dataset_sha256`.
- `python -m orchestra run --config <tmp>/extend.json --run-id m3-fixture` (with a B0 and L2 `C=1` configuration list in the temp config) printed `B0: ok`, `L2-C1: ok`, `PASS: run written to <tmp>/results/m3-fixture`.

Refusal when `parent_manifest_sha256` is `null` (exit 1, nothing written):

```text
ERROR: parent_manifest_sha256 in the config is missing or does not match the parent manifest file
```

The pin is what stops a re-recorded parent manifest (for example a whole group moved between partitions with counts recomputed) from being accepted as the parent. `configs/m3.json` ships with `null` until the real M2 manifest hash is recorded. After the refactor the run was repeated from scratch and reproduced the same hashes and counts as above; the child records `parent_manifest_sha256` equal to the parent manifest hash.

Refusal (one old text edited, same new-row set; exit 1; no m3b manifest or files written):

```text
ERROR: doc-g0-0: text, label or group_id differs from the parent; record the correction and build a named successor protocol instead of overwriting
```

## Open gates (not satisfied by this tooling)

- The real 400-row collection under the P1 collection brief does not exist.
- Review of new candidates against all existing scenario families is human work and has not happened.
- New-data collection bias and author exposure must be disclosed when real data is added; passing checks do not remove them.
- Archive and restore of the frozen dataset and common split, as in P1, is not done.
- `configs/m3.json` has `parent_manifest_sha256: null` (fill from the M2 evidence when the real split is frozen) and an empty `configurations` list until P5.
