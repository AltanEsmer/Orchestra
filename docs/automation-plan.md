# Complete the tooling before collecting research data

Altan authorized this work on October 22, 2026, including PR creation, merge, issue updates, and one-step manual guidance. The acceptance boundary is executable, verified tooling for the required study. Dataset authorship, permissions, human review, final report authorship, learning responses, and submission remain separate evidence.

## Design and delivery

Two independent designs compared extending the existing CLI with adding a separate study driver. The independent judge scored both 22/25. The implementation keeps `python -m orchestra` and adds focused confidence, study preparation, archive, and figure modules. It adopts raw-model reproduction before calibration and a repository-wide final-test receipt keyed by the split hash. A generic workflow engine would add state without answering another research question.

The data shapes are existing JSONL rows and split manifests, hash-bound confidence artifacts, an immutable freeze, and a final-test receipt with explicit attempts. `study_evidence` records hashes only after the existing readiness checks pass. It lets later confidence work verify provenance without reopening the full dataset. Artificial confidence work requires `--fixture` and records that status in its artifacts.

Matplotlib 3.11.2 supplies axes, legends, heatmaps, and reproducible SVG/PNG exports. It is pinned in the experiment environment. Calibration uses the existing scikit-learn dependency. Sigmoid calibration wraps the full feature/model pipeline in three grouped training folds. This applies the existing protocol; it adds no new modeling equation or search grid.

## Verification units

1. Repair frozen-input and output-path integrity in PR #16. Verify the original defects and the complete M2/M3 CLI workflow.
2. Implement readiness, blind review, prepared configs, and verified local archives. Preserve executable modes on restoration.
3. Implement probability diagnostics, training-only calibration, frozen interpretation evidence, and one final-test decision set per split.
4. Render saved scientific evidence and prepare an IEEE report source template.
5. Run `scripts/verify_workflow.py` on explicit artificial fixtures. Restore a backup, install a clean locked environment, and reproduce M3 predictions and metrics.
6. Run the README checks and independent Standards/Spec reviews. Merge only the reviewed head, then reconcile issues with remaining human evidence.

## Scope and tradeoffs

The final-test receipt prevents accidental repeated selection in this checkout. It is an auditable workflow control, not protection against deliberately modifying code or deleting records. An exact failed or interrupted request can resume with its history preserved. A standard-library POSIX file lock excludes concurrent evaluation; atomic receipt writes preserve crash recovery. This local workflow supports macOS and Linux. A changed decision set cannot reuse the live research split.

Archives are explicitly local-only and use a list of regular files. They exclude secrets and PDFs. Submit the final report separately and retain the external study PDFs separately. Permission to back up local data does not imply permission to publish it.

The report template can compile now. Research figures, conclusions, milestone PDFs with real query traces, the real-data reproduction archive, and final pagination wait for accepted data and Altan's report. Fixture checks never close those milestone requirements.

The Laziness Protocol chose one CLI and reused existing models. Model the Domain chose immutable artifact identities and explicit receipt states. Prove It Works required restored execution, rather than accepting an archive checksum alone. Sequence Work into Verifiable Units kept the integrity repair separate from completion tooling.
