import argparse
import json

from orchestra.data import (
    M1_REQUIREMENTS,
    agreement,
    file_sha256,
    read_jsonl,
    readiness,
    summarize,
    validate,
    validate_reviews,
)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate the annotated query dataset."
    )
    parser.add_argument("dataset")
    parser.add_argument("--sources", default="data/manifests/sources.json")
    parser.add_argument("--review", help="review ledger JSONL")
    parser.add_argument(
        "--ready", action="store_true", help="also check M1 readiness (needs --review)"
    )
    args = parser.parse_args(argv)
    if args.ready and not args.review:
        parser.error("--ready requires --review")

    try:
        rows, errors = read_jsonl(args.dataset)
        reviews, review_errors = read_jsonl(args.review) if args.review else ([], [])
        errors += review_errors
        digest = file_sha256(args.dataset)
        with open(args.sources, encoding="utf-8") as file:
            sources = json.load(file)
    except OSError as error:
        print(f"ERROR: cannot read {error.filename}: {error.strerror}")
        return 1
    except json.JSONDecodeError:
        print(f"ERROR: {args.sources}: not valid JSON")
        return 1
    if not isinstance(sources, dict):
        print(f"ERROR: {args.sources}: must be a JSON object")
        return 1

    errors += validate(rows, sources)
    if args.review:
        errors += validate_reviews(reviews, rows)
    if args.ready and not errors:
        errors += readiness(rows, sources, reviews, M1_REQUIREMENTS)
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        print(f"FAIL: {len(errors)} errors")
        return 1
    summary = summarize(rows, digest)
    if args.review:
        summary["agreement"] = agreement(reviews)
        summary["ledger_sha256"] = file_sha256(args.review)
    print(json.dumps(summary, indent=2))
    if args.ready:
        accepted = summary["status"]["accepted"]
        print(
            f"PASS: M1 readiness checks passed ({accepted} accepted rows, "
            f"{len(reviews)} reviewed)"
        )
    else:
        print(f"PASS: {len(rows)} rows valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
