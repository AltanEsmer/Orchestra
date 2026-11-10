#!/bin/sh
# Usage: scripts/archive_study.sh STUDY_ROOT OUT.zip
# Archives the ignored M3.5 study inputs and saved outputs from STUDY_ROOT.
# Tracked code and configs come from a Git checkout, not from this archive.
set -eu
[ $# -eq 2 ] || { echo "usage: $0 STUDY_ROOT OUT.zip" >&2; exit 2; }
ROOT="$(CDPATH= cd -- "$1" && pwd)"
OUT="$2"
REPO="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
LIST="${OUT%.zip}.files.json"

(
  cd "$ROOT"
  {
    printf '%s\n' \
      data/processed/m3-v1.jsonl \
      data/processed/m3-5-v1.jsonl data/raw/m3-5-reviews-v1.jsonl \
      data/raw/m3-5-import/types.json data/raw/m3-5-import/pairs.json \
      data/raw/m3-5-import/collection-check.json \
      data/processed/m3-5-prepared.json data/processed/m3-5-prepared-jev.json \
      data/processed/m3-5/train.jsonl data/processed/m3-5/validation.jsonl \
      data/processed/sealed/m3-5-test.jsonl \
      results/jev/m3-5-validation.jsonl results/jev/m3-5-validation-repeat.jsonl \
      results/jev/m3-5-test.jsonl \
      results/validation-interpretations-m3-5.jsonl \
      results/test-interpretations-m3-5.jsonl \
      results/m3-5-full-a-selection.json results/frozen-study-m3-5.json
    find results/m3-5-full-a results/m3-5-full-a-report results/m4-5-validation \
      results/final-test-m3-5 results/m5-figures -type f
    find results/test-receipts -type f -name '*.json'
  } | LC_ALL=C sort | python3 -c 'import json, sys
print(json.dumps([line.strip() for line in sys.stdin if line.strip()], indent=1))'
) > "$LIST"

cd "$REPO"
uv run --locked python -m orchestra archive --root "$ROOT" --files "$LIST" --out "$OUT" \
  > "${OUT%.zip}.manifest.json"
echo "PASS: $(python3 -c 'import json, sys; print(len(json.load(open(sys.argv[1]))))' "$LIST") files archived"
shasum -a 256 "$OUT"
