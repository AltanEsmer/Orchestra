"""Exercise the real CLI on artificial data, including restored reproduction."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LABELS = ("document_retrieval", "knowledge_lookup", "calculation", "direct_answer")


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def write_rows(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row) + "\n" for row in rows), encoding="utf-8")


def fixture_rows(groups):
    return [
        {
            "query_id": f"fixture-{label}-{group}-{variant}",
            "group_id": f"fixture-{label}-{group}",
            "text": f"Artificial {label} scenario {group} wording {variant}",
            "label": label,
            "status": "accepted",
            "source_id": "fixture",
            "rationale": "Artificial software fixture, never research data.",
            "annotator_ids": ["fixture-author"],
            "annotation_version": "fixture-v1",
        }
        for label in LABELS
        for group in range(groups)
        for variant in range(2)
    ]


def verify(out):
    out = out.resolve()
    if not out.is_relative_to(ROOT / "work"):
        raise ValueError(
            "fixture output must be inside the ignored repository work/ directory"
        )
    out.mkdir(parents=True)
    env = dict(os.environ)
    for name in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
    ):
        env[name] = "1"
    transcript = []

    def run(args, expected=0, cwd=ROOT):
        done = subprocess.run(
            args, cwd=cwd, env=env, text=True, capture_output=True, check=False
        )
        transcript.append(
            {
                "args": [str(a) for a in args],
                "exit_code": done.returncode,
                "stdout": done.stdout,
                "stderr": done.stderr,
            }
        )
        write_json(out / "transcript.json", transcript)
        if done.returncode != expected:
            raise RuntimeError(
                f"{args} returned {done.returncode}: {done.stdout}\n{done.stderr}"
            )
        return done

    cli = [sys.executable, "-m", "orchestra"]
    sources = out / "sources.json"
    write_json(
        sources,
        {
            "fixture": {
                "author": "software fixture",
                "created": "2026-10-22",
                "license": "Artificial test fixture only",
            }
        },
    )
    brief = out / "collection-brief.md"
    brief.write_text(
        "Artificial fixture collection fixed before predictions. No research claims.\n",
        encoding="utf-8",
    )
    configs = {}
    for stage, groups in (("m2", 15), ("m3", 50)):
        rows = fixture_rows(groups)
        dataset, reviews = out / f"{stage}.jsonl", out / f"{stage}-reviews.jsonl"
        write_rows(dataset, rows)
        write_rows(
            reviews,
            [
                {
                    "query_id": r["query_id"],
                    "original_label": r["label"],
                    "review_label": r["label"],
                    "reviewer_id": "fixture-reviewer",
                    "review_date": "2026-10-22",
                    "review_kind": "second_human",
                    "resolved_label": r["label"],
                }
                for r in rows
            ],
        )
        config = json.loads((ROOT / f"configs/{stage}.json").read_text())
        config.update(
            {
                "dataset": str(dataset),
                "sources": str(sources),
                "split_manifest": str(out / "splits" / f"{stage}.json"),
                "train": str(out / stage / "train.jsonl"),
                "validation": str(out / stage / "validation.jsonl"),
                "sealed_test": str(out / "sealed" / f"{stage}.jsonl"),
                "results_dir": str(out / "results"),
            }
        )
        if stage == "m3":
            config["parent_dataset"] = configs["m2"]["dataset"]
            config["parent_manifest"] = configs["m2"]["split_manifest"]
        config_path = out / f"{stage}-config.json"
        prepared = out / f"{stage}-prepared.json"
        write_json(config_path, config)
        run(
            cli
            + [
                "status",
                "--dataset",
                str(dataset),
                "--sources",
                str(sources),
                "--review",
                str(reviews),
            ]
        )
        run(
            cli
            + [
                "prepare-study",
                "--config",
                str(config_path),
                "--review",
                str(reviews),
                "--collection-brief",
                str(brief),
                "--out",
                str(prepared),
            ]
        )
        configs[stage] = json.loads(prepared.read_text())
        for suffix in ("a", "b"):
            run(
                [
                    str(ROOT / "scripts/run_experiment.sh"),
                    "--config",
                    str(prepared),
                    "--run-id",
                    f"{stage}-{suffix}",
                ]
            )
        run(
            cli
            + [
                "compare",
                "--left",
                str(out / f"results/{stage}-a"),
                "--right",
                str(out / f"results/{stage}-b"),
            ]
        )
    run(
        cli
        + [
            "prepare-review",
            "--dataset",
            str(out / "m2.jsonl"),
            "--sources",
            str(sources),
            "--out",
            str(out / "blind-review"),
        ]
    )
    m3 = out / "results/m3-a"
    selection, confidence, frozen, final = (
        out / name for name in ("selection.json", "confidence", "freeze.json", "final")
    )
    run(cli + ["select", "--run", str(m3), "--out", str(selection)])
    run(
        cli
        + [
            "report",
            "--run",
            str(m3),
            "--selection",
            str(selection),
            "--train",
            configs["m3"]["train"],
            "--validation",
            configs["m3"]["validation"],
        ]
    )
    sealed = Path(configs["m3"]["sealed_test"])
    hidden = sealed.with_suffix(".hidden")
    sealed.rename(hidden)
    try:
        run(
            cli
            + [
                "confidence",
                "--run",
                str(m3),
                "--selection",
                str(selection),
                "--out",
                str(confidence),
                "--fixture",
            ]
        )
        run(cli + ["freeze", "--confidence", str(confidence), "--out", str(frozen)])
    finally:
        hidden.rename(sealed)
    final_command = cli + ["final-test", "--freeze", str(frozen), "--out", str(final)]
    run(final_command)
    run(final_command)
    run(
        cli
        + ["final-test", "--freeze", str(frozen), "--out", str(out / "changed-final")],
        expected=1,
    )
    run(
        cli
        + [
            "figures",
            "--run",
            str(m3),
            "--selection",
            str(selection),
            "--train",
            configs["m3"]["train"],
            "--validation",
            configs["m3"]["validation"],
            "--confidence",
            str(confidence),
            "--final",
            str(final),
            "--out",
            str(out / "figures"),
            "--fixture",
        ]
    )
    code_files = [
        "pyproject.toml",
        "uv.lock",
        ".python-version",
        "scripts/run_experiment.sh",
    ]
    code_files += [
        str(p.relative_to(ROOT)) for p in sorted((ROOT / "src/orchestra").glob("*.py"))
    ]
    data_files = [
        str(p.relative_to(ROOT))
        for p in sorted(out.rglob("*"))
        if p.is_file() and p.name != "transcript.json"
    ]
    allowlist = out / "archive-files.json"
    write_json(allowlist, code_files + data_files)
    archive, restored = out / "fixture.zip", out / "restored"
    run(
        cli
        + [
            "archive",
            "--root",
            str(ROOT),
            "--files",
            str(allowlist),
            "--out",
            str(archive),
        ]
    )
    run(cli + ["restore", "--archive", str(archive), "--out", str(restored)])
    restored_config = dict(configs["m3"])
    for key, value in restored_config.items():
        if isinstance(value, str) and value.startswith(str(ROOT) + os.sep):
            restored_config[key] = str(restored / Path(value).relative_to(ROOT))
    restored_config["results_dir"] = str(restored / "rerun-results")
    rerun_config = restored / "rerun.json"
    write_json(rerun_config, restored_config)
    run(["uv", "sync", "--locked"], cwd=restored)
    run(
        [
            str(restored / "scripts/run_experiment.sh"),
            "--config",
            str(rerun_config),
            "--run-id",
            "restored-m3",
        ],
        cwd=restored,
    )
    run(
        cli
        + [
            "compare",
            "--left",
            str(m3),
            "--right",
            str(restored / "rerun-results/restored-m3"),
        ]
    )
    write_json(
        out / "acceptance.json",
        {
            "fixture_only": True,
            "passed": True,
            "commands": len(transcript),
            "checks": [
                "M1 readiness",
                "blind review",
                "M2 and M3 reproduction",
                "confidence without sealed file",
                "freeze",
                "single final test and retry",
                "scientific figures",
                "verified archive",
                "clean restored environment and predictions",
            ],
        },
    )
    print(f"PASS: artificial workflow, {len(transcript)} commands; evidence in {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    verify(args.out)
