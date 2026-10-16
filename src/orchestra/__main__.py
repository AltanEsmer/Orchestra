import argparse
import json
from pathlib import Path

from orchestra.data import file_sha256, read_jsonl, validate
from orchestra.splits import check_split, make_split, materialize


def split(args):
    with open(args.config, encoding="utf-8") as file:
        config = json.load(file)
    rows, errors = read_jsonl(config["dataset"])
    with open(config["sources"], encoding="utf-8") as file:
        errors += validate(rows, json.load(file))
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"FAIL: {len(errors)} errors; dataset is not structurally valid")
        return 1
    digest = file_sha256(config["dataset"])
    try:
        manifest = make_split(rows, digest, config["seed"])
    except ValueError as error:
        print(f"ERROR: {error}")
        return 1

    text = json.dumps(manifest, indent=2) + "\n"
    path = Path(config["split_manifest"])
    if path.exists() and path.read_text(encoding="utf-8") != text:
        print(f"ERROR: {path} exists and differs; manifests are immutable")
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

    written = json.loads(path.read_text(encoding="utf-8"))
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


def main(argv=None):
    parser = argparse.ArgumentParser(prog="orchestra")
    commands = parser.add_subparsers(dest="command", required=True)
    split_parser = commands.add_parser("split", help="create the persisted split")
    split_parser.add_argument("--config", required=True)
    split_parser.set_defaults(run=split)
    args = parser.parse_args(argv)
    return args.run(args)


if __name__ == "__main__":
    raise SystemExit(main())
