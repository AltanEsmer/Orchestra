import argparse
import json
import os
from pathlib import Path

from orchestra import experiment, jev
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


def study_status(args):
    from orchestra.study import status

    result = status(args.dataset, args.sources, args.review)
    print(json.dumps(result, indent=2))
    return 0 if result["ready"] else 1


def prepare_review(args):
    from orchestra.study import prepare_review

    out = prepare_review(args.dataset, args.sources, args.out, args.seed, args.extra_id)
    print(f"PASS: blind review worksheet written to {out / 'reviewer.jsonl'}")
    print("Keep steward.json hidden until independent labels are recorded.")
    return 0


def analyze_confidence(args):
    from orchestra.confidence import analyze, load_artifacts

    out = analyze(args.run_dir, args.selection, args.out, fixture=args.fixture)
    outcome = load_artifacts(out)["outcomes.json"]
    if outcome["status"] != "ok":
        print(f"BLOCKED: calibration {outcome['status']}; evidence written to {out}")
        return 1
    print(f"PASS: validation confidence written to {out}")
    return 0


def freeze_study(args):
    from orchestra.confidence import freeze

    freeze(
        args.confidence,
        args.out,
        error_review=args.error_review,
        jev_test_log=args.jev_test_log,
    )
    print(f"PASS: final-test decisions frozen at {args.out}")
    return 0


def final_test(args):
    from orchestra.confidence import final_test

    send = None
    if args.send_jev_test:
        key = os.environ.get(jev.KEY_VARIABLE)
        if not key:
            print(f"ERROR: {jev.KEY_VARIABLE} is not set")
            return 1

        def send(body):
            return jev.post(body, key)

    out = final_test(args.freeze, args.out, resume=args.resume, jev_send=send)
    print(f"PASS: frozen final-test evidence at {out}")
    return 0


def review_test(args):
    from orchestra.confidence import review_test

    summary = review_test(args.final_test, args.interpretations)
    for configuration, entry in sorted(summary.items()):
        categories = ", ".join(
            f"{name} {count}" for name, count in sorted(entry["categories"].items())
        )
        print(
            f"{configuration}: {entry['interpreted']}/{entry['errors']} errors "
            f"interpreted, {entry['correct']} correct comparison; {categories}"
        )
    print("PASS: test interpretations match the final-test predictions")
    return 0


def render_figures(args):
    from orchestra.figures import render

    out = render(
        args.run_dir,
        args.selection,
        args.train,
        args.validation,
        args.out,
        confidence_dir=args.confidence,
        final_dir=args.final,
        fixture=args.fixture,
    )
    print(f"PASS: figures and source values written to {out}")
    return 0


def archive_study(args):
    from orchestra.archive import create_archive

    paths = json.loads(Path(args.files).read_text(encoding="utf-8"))
    if not isinstance(paths, list) or not all(isinstance(p, str) for p in paths):
        raise ValueError("archive files must be a JSON list of relative file paths")
    print(json.dumps(create_archive(args.root, paths, args.out), indent=2))
    return 0


def restore_archive(args):
    from orchestra.archive import verify_archive

    print(json.dumps(verify_archive(args.archive, args.out), indent=2))
    return 0


def check_collection(args):
    from orchestra.collection import check_release

    rows, errors = read_jsonl(args.dataset)
    parent, parent_errors = read_jsonl(args.parent)
    if errors or parent_errors:
        raise ValueError("; ".join(errors + parent_errors))
    types = json.loads(Path(args.types).read_text(encoding="utf-8"))
    pairs = json.loads(Path(args.pairs).read_text(encoding="utf-8"))
    accepted = [r for r in rows if r["status"] == "accepted"]
    parent_ids = {r["query_id"] for r in parent}
    report = check_release(accepted, parent_ids, types, pairs)
    report["dataset_sha256"] = file_sha256(args.dataset)
    report["parent_sha256"] = file_sha256(args.parent)
    with open(args.out, "x", encoding="utf-8") as file:
        file.write(json.dumps(report, indent=2) + "\n")
    for label, counts in report["by_class"].items():
        print(
            f"{label}: {counts['rows']} rows ({counts['new_rows']} new), "
            f"{counts['groups']} groups ({counts['new_groups']} new)"
        )
    print(f"close new pairs: {len(report['close_pairs'])}")
    for error in report["errors"]:
        print(f"ERROR: {error}")
    if report["errors"]:
        print(f"FAIL: {len(report['errors'])} collection check errors")
        return 1
    print("PASS: M3.5 collection checks")
    return 0


def prepare_study(args):
    from orchestra.study import prepare

    out = prepare(args.config, args.review, args.collection_brief, args.out)
    print(f"PASS: ready data split using prepared config {out}")
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
    jev_parser = commands.add_parser("jev", help="collect Jev answers for validation")
    jev_parser.add_argument("--config", required=True)
    jev_parser.add_argument("--log", required=True)
    jev_parser.add_argument("--max-requests", type=int, required=True)
    jev_parser.add_argument("--dry-run", action="store_true")
    jev_parser.set_defaults(run=guarded(jev.run_jev))
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
    status_parser = commands.add_parser(
        "status", help="show M1 data blockers and next action"
    )
    status_parser.add_argument("--dataset", default="data/raw/pilot-v0.jsonl")
    status_parser.add_argument("--sources", default="data/manifests/sources.json")
    status_parser.add_argument("--review", default="data/raw/reviews-v1.jsonl")
    status_parser.set_defaults(run=guarded(study_status))
    review_parser = commands.add_parser(
        "prepare-review", help="prepare a blind human review worksheet"
    )
    review_parser.add_argument("--dataset", required=True)
    review_parser.add_argument("--sources", default="data/manifests/sources.json")
    review_parser.add_argument("--out", required=True)
    review_parser.add_argument("--seed", type=int, default=42)
    review_parser.add_argument("--extra-id", action="append", default=[])
    review_parser.set_defaults(run=guarded(prepare_review))
    confidence_parser = commands.add_parser(
        "confidence", help="analyze training-only calibration on validation"
    )
    confidence_parser.add_argument("--run", dest="run_dir", required=True)
    confidence_parser.add_argument("--selection", required=True)
    confidence_parser.add_argument("--out", required=True)
    confidence_parser.add_argument(
        "--fixture",
        action="store_true",
        help="explicit artificial tooling verification",
    )
    confidence_parser.set_defaults(run=guarded(analyze_confidence))
    freeze_parser = commands.add_parser(
        "freeze", help="freeze decisions before opening the test set"
    )
    freeze_parser.add_argument("--confidence", required=True)
    freeze_parser.add_argument("--out", required=True)
    freeze_parser.add_argument(
        "--error-review", help="completed validation interpretation ledger for research"
    )
    freeze_parser.add_argument(
        "--jev-test-log",
        help="ignored path where final-test will log Jev's test answers",
    )
    freeze_parser.set_defaults(run=guarded(freeze_study))
    final_parser = commands.add_parser(
        "final-test", help="evaluate frozen systems once per split"
    )
    final_parser.add_argument("--freeze", required=True)
    final_parser.add_argument("--out", required=True)
    final_parser.add_argument(
        "--resume",
        action="store_true",
        help="retry the identical failed frozen request",
    )
    final_parser.add_argument(
        "--send-jev-test",
        action="store_true",
        help="send the sealed test queries to TypeSafe Jev (needs TYPESAFE_API_KEY)",
    )
    final_parser.set_defaults(run=guarded(final_test))
    test_review_parser = commands.add_parser(
        "test-review", help="check post-freeze test error interpretations"
    )
    test_review_parser.add_argument("--final-test", required=True)
    test_review_parser.add_argument("--interpretations", required=True)
    test_review_parser.set_defaults(run=guarded(review_test))
    figures_parser = commands.add_parser(
        "figures", help="render figures from saved evidence"
    )
    figures_parser.add_argument("--run", dest="run_dir", required=True)
    figures_parser.add_argument("--selection", required=True)
    figures_parser.add_argument("--train", required=True)
    figures_parser.add_argument("--validation", required=True)
    figures_parser.add_argument("--out", required=True)
    figures_parser.add_argument("--confidence")
    figures_parser.add_argument("--final")
    figures_parser.add_argument("--fixture", action="store_true")
    figures_parser.set_defaults(run=guarded(render_figures))
    archive_parser = commands.add_parser(
        "archive", help="create an explicit local-only backup"
    )
    archive_parser.add_argument("--root", default=".")
    archive_parser.add_argument(
        "--files", required=True, help="JSON array of relative file paths"
    )
    archive_parser.add_argument("--out", required=True)
    archive_parser.set_defaults(run=guarded(archive_study))
    restore_parser = commands.add_parser(
        "restore", help="verify a backup before restoring into a new directory"
    )
    restore_parser.add_argument("--archive", required=True)
    restore_parser.add_argument("--out", required=True)
    restore_parser.set_defaults(run=guarded(restore_archive))
    collection_parser = commands.add_parser(
        "check-collection", help="run the M3.5 cumulative count and batch checks"
    )
    collection_parser.add_argument("--dataset", required=True)
    collection_parser.add_argument("--parent", required=True)
    collection_parser.add_argument(
        "--types", required=True, help="JSON object of query ID to request type"
    )
    collection_parser.add_argument(
        "--pairs", required=True, help="JSON list of close-pair hand checks"
    )
    collection_parser.add_argument("--out", required=True, help="new report file")
    collection_parser.set_defaults(run=guarded(check_collection))
    prepare_parser = commands.add_parser(
        "prepare-study", help="check readiness and freeze inputs before splitting"
    )
    prepare_parser.add_argument("--config", required=True)
    prepare_parser.add_argument("--review", required=True)
    prepare_parser.add_argument("--collection-brief", required=True)
    prepare_parser.add_argument(
        "--out", required=True, help="new local prepared config"
    )
    prepare_parser.set_defaults(run=guarded(prepare_study))
    args = parser.parse_args(argv)
    return args.run(args)


if __name__ == "__main__":
    raise SystemExit(main())
