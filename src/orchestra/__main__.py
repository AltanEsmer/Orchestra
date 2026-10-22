import argparse
import json
import os
from pathlib import Path

from orchestra import experiment
from orchestra.data import file_sha256, read_jsonl, validate
from orchestra.splits import (
    check_extension,
    check_split,
    extend_split,
    make_split,
    materialize,
)


def guarded(function):
    def command(args):
        try:
            return function(args)
        except OSError as error:
            print(f"ERROR: cannot read {error.filename}: {error.strerror}")
        except json.JSONDecodeError as error:
            print(f"ERROR: invalid JSON: {error}")
        except KeyError as error:
            print(f"ERROR: config is missing {error}")
        except ValueError as error:
            print(f"ERROR: {error}")
        except (TypeError, AttributeError):
            print("ERROR: config values have the wrong type")
        return 1

    return command


def outputs_are_distinct(config, config_path=None):
    train, validation, sealed = (
        Path(config[k]).resolve() for k in ("train", "validation", "sealed_test")
    )
    if len({train, validation, sealed}) < 3 or any(
        d in sealed.parents for d in (train.parent, validation.parent)
    ):
        print(
            "ERROR: train, validation and sealed_test must be distinct files, "
            "and sealed_test must not sit in the train or validation directory"
        )
        return False
    inputs = [
        Path(config[k]).resolve()
        for k in ("dataset", "sources", "parent_dataset", "parent_manifest")
        if k in config
    ]
    if config_path is not None:
        inputs.append(Path(config_path).resolve())
    outputs = [train, validation, sealed, Path(config["split_manifest"]).resolve()]
    for index, output in enumerate(outputs):
        for other in inputs + outputs[index + 1 :]:
            same = output == other or (
                output.exists() and other.exists() and output.samefile(other)
            )
            if same or output in other.parents or other in output.parents:
                print(f"ERROR: input/output paths collide: {output} and {other}")
                return False
    return True


def load_valid(dataset, sources_path):
    """Rows of a structurally valid dataset, or None after printing the errors."""
    rows, errors = read_jsonl(dataset)
    with open(sources_path, encoding="utf-8") as file:
        sources = json.load(file)
    if not isinstance(sources, dict):
        print(f"ERROR: {sources_path}: must be a JSON object")
        return None
    errors += validate(rows, sources)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAIL: {len(errors)} errors; dataset is not structurally valid")
        return None
    return rows


def write_manifest(manifest, path, kind="manifest"):
    text = json.dumps(manifest, indent=2) + "\n"
    path = Path(path)
    if path.exists() and path.read_text(encoding="utf-8") != text:
        print(f"ERROR: {path} exists and differs; {kind}s are immutable")
        return None
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return json.loads(path.read_text(encoding="utf-8"))


def run_split(args):
    with open(args.config, encoding="utf-8") as file:
        config = json.load(file)
    if not outputs_are_distinct(config, args.config):
        return 1
    rows = load_valid(config["dataset"], config["sources"])
    if rows is None:
        return 1
    digest = file_sha256(config["dataset"])
    try:
        manifest = make_split(rows, digest, config["seed"])
    except ValueError as error:
        print(f"ERROR: {error}")
        return 1

    path = Path(config["split_manifest"])
    written = write_manifest(manifest, path)
    if written is None:
        return 1
    errors = check_split(written, rows, digest)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    materialize(
        written, rows, config["train"], config["validation"], config["sealed_test"]
    )
    # Aggregates only: test text never reaches the log.
    print(
        json.dumps(
            {"counts": manifest["counts"], "proportions": manifest["proportions"]},
            indent=2,
        )
    )
    print(f"PASS: split written to {path}")
    return 0


def run_extend(args):
    with open(args.config, encoding="utf-8") as file:
        config = json.load(file)
    if not outputs_are_distinct(config, args.config):
        return 1
    parent_rows = load_valid(config["parent_dataset"], config["sources"])
    rows = load_valid(config["dataset"], config["sources"])
    if parent_rows is None or rows is None:
        return 1
    parent_digest = file_sha256(config["parent_dataset"])
    with open(config["parent_manifest"], encoding="utf-8") as file:
        parent = json.load(file)
    if not isinstance(parent, dict) or parent.get("dataset_sha256") != parent_digest:
        print("ERROR: parent dataset file does not match the parent manifest hash")
        return 1
    parent_manifest_digest = file_sha256(config["parent_manifest"])
    if config["parent_manifest_sha256"] != parent_manifest_digest:
        print(
            "ERROR: parent_manifest_sha256 in the config is missing or does not "
            "match the parent manifest file"
        )
        return 1
    digest = file_sha256(config["dataset"])
    try:
        manifest = extend_split(
            parent,
            parent_rows,
            rows,
            parent_digest,
            parent_manifest_digest,
            digest,
            config["seed"],
        )
    except ValueError as error:
        print(f"ERROR: {error}")
        return 1

    path = Path(config["split_manifest"])
    written = write_manifest(manifest, path)
    if written is None:
        return 1
    errors = check_extension(
        written, parent, parent_rows, rows, digest, parent_manifest_digest
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    materialize(
        written, rows, config["train"], config["validation"], config["sealed_test"]
    )
    print(
        json.dumps(
            {
                "counts": manifest["counts"],
                "proportions": manifest["proportions"],
                "new_groups": manifest["new_groups"],
            },
            indent=2,
        )
    )
    print(f"PASS: extension written to {path}")
    return 0


def run_experiment(args):
    with open(args.config, encoding="utf-8") as file:
        config = json.load(file)
    try:
        out, outcomes = experiment.run(config, args.run_id)
    except FileExistsError as error:
        print(
            f"ERROR: run directory {error.filename} already exists; pick a new run id"
        )
        return 1
    except ValueError as error:
        print(f"ERROR: {error}")
        return 1
    unset = [v for v in experiment.THREAD_VARS if v not in os.environ]
    if unset:
        print(f"WARNING: thread variables not set before start: {', '.join(unset)}")
    for outcome in outcomes:
        print(f"{outcome['id']}: {outcome['status']}")
    if any(o["status"] != "ok" for o in outcomes):
        print(f"FAIL: some configurations did not finish cleanly; see {out}")
        return 1
    print(f"PASS: run written to {out}")
    return 0


def compare(args):
    differences = experiment.compare(args.left, args.right)
    for difference in differences:
        print(f"DIFF: {difference}")
    if differences:
        print("FAIL: runs differ")
        return 1
    print("PASS: runs reproduce")
    return 0


def select(args):
    try:
        selection = experiment.select(args.run_dir)
    except ValueError as error:
        print(f"ERROR: {error}")
        return 1
    if write_manifest(selection, args.out, "selection") is None:
        return 1
    for family, info in selection["families"].items():
        print(f"{family}: {info['chosen']}")
    if not selection["valid"]:
        blocked = ", ".join(selection["blocking"]) or "no configurations"
        print(f"FAIL: selection is not valid; blocked by {blocked}; see {args.out}")
        return 1
    print(f"PASS: overall {selection['overall']['chosen']}; written to {args.out}")
    return 0


def report(args):
    try:
        out, counts, selection = experiment.report(
            args.run_dir, args.selection, args.train, args.validation
        )
    except FileExistsError as error:
        print(f"ERROR: {error.filename} already exists; report needs a new directory")
        return 1
    except ValueError as error:
        print(f"ERROR: {error}")
        return 1
    for configuration, count in counts.items():
        print(f"{configuration}: {count} validation errors")
    if not selection["valid"]:
        reasons = selection["blocking"] + selection["missing"] + selection["unexpected"]
        print(f"INVALID selection: {', '.join(reasons)}; report written to {out}")
        return 1
    print(f"PASS: report written to {out}")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(prog="orchestra")
    commands = parser.add_subparsers(dest="command", required=True)
    split_parser = commands.add_parser("split", help="create the persisted split")
    split_parser.add_argument("--config", required=True)
    split_parser.set_defaults(run=guarded(run_split))
    extend_parser = commands.add_parser(
        "extend", help="append new groups to a frozen split"
    )
    extend_parser.add_argument("--config", required=True)
    extend_parser.set_defaults(run=guarded(run_extend))
    run_parser = commands.add_parser("run", help="fit and evaluate the baselines")
    run_parser.add_argument("--config", required=True)
    run_parser.add_argument("--run-id", required=True)
    run_parser.set_defaults(run=guarded(run_experiment))
    compare_parser = commands.add_parser("compare", help="check two runs reproduce")
    compare_parser.add_argument("--left", required=True)
    compare_parser.add_argument("--right", required=True)
    compare_parser.set_defaults(run=guarded(compare))
    select_parser = commands.add_parser("select", help="freeze per-family selections")
    select_parser.add_argument("--run", dest="run_dir", required=True)
    select_parser.add_argument("--out", required=True)
    select_parser.set_defaults(run=guarded(select))
    report_parser = commands.add_parser("report", help="write the comparison report")
    report_parser.add_argument("--run", dest="run_dir", required=True)
    report_parser.add_argument("--selection", required=True)
    report_parser.add_argument("--train", required=True)
    report_parser.add_argument("--validation", required=True)
    report_parser.set_defaults(run=guarded(report))
    args = parser.parse_args(argv)
    return args.run(args)


if __name__ == "__main__":
    raise SystemExit(main())
