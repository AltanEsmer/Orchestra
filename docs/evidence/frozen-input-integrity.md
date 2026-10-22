# Frozen-input integrity repair

October 22, 2026. Review baseline `df7f9ef6858b91faec38574c1561e04069ce2ba6`.

The independent reviewer reproduced changed materialized training content passing under the original manifest, a split output truncating its input dataset, and a restored M3 run failing comparison only because its parent paths changed. The repair binds visible rows to frozen canonical hashes, validates partition/group invariants without test reads, protects input paths, and preserves materialized outputs. Parent paths are locations, while parent hashes remain semantic inputs.

Four focused regression tests failed against the original HEAD. The corrected implementation passed 59 experiment tests and 52 split tests. Ruff check and format passed on the five affected Python files. These checks use artificial fixtures and establish software behavior only.

Reproduce with:

```sh
uv run --locked python -m unittest discover -s tests -p 'test_experiment.py'
uv run --locked python -m unittest discover -s tests -p 'test_splits.py'
```

No research rows, permissions, review decisions, or metrics were supplied.
