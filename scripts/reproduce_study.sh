#!/bin/sh
# Usage: scripts/reproduce_study.sh ARCHIVE.zip
# Run inside a fresh clone. Restores the study archive, reruns the documented
# M3.5 and M4 commands from the archived inputs only, and compares every saved
# split, prediction, metric and figure with the archived originals.
# Jev's validation and test answers are replayed from the archived logs; no
# query is sent to TypeSafe.
set -eu
[ $# -eq 1 ] || { echo "usage: $0 ARCHIVE.zip" >&2; exit 2; }
ARCHIVE="$(CDPATH= cd -- "$(dirname -- "$1")" && pwd)/$(basename -- "$1")"
cd "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
OUT=work/m6-reproduction
ORIGINAL="$OUT/original"
test -z "$(git status --porcelain --ignored | grep -v '^!! \.venv/$')" ||
  { echo "ERROR: checkout has changes or ignored files; use a fresh clone" >&2; exit 1; }
test ! -e "$OUT" || { echo "ERROR: $OUT exists; use a fresh clone" >&2; exit 1; }
test ! -e results/m3-5-full-a || { echo "ERROR: saved results present" >&2; exit 1; }
mkdir -p "$OUT"
exec 3>&1 > "$OUT/reproduce.log" 2>&1
trap 'tail -n 40 "$OUT/reproduce.log" >&3' EXIT
set -x
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1

git rev-parse HEAD
uv --version
uv sync --locked
uv run --locked python -c 'import sys; from orchestra.data import file_sha256
for path in sys.argv[1:]: print(file_sha256(path), path)' "$ARCHIVE" uv.lock
uv run --locked python scripts/smoke.py
uv run --locked python -m orchestra restore --archive "$ARCHIVE" --out "$ORIGINAL" \
  > "$OUT/restore.json"

for input in \
  data/processed/m3-v1.jsonl data/processed/m3-5-v1.jsonl \
  data/raw/m3-5-reviews-v1.jsonl data/raw/m3-5-import/types.json \
  data/raw/m3-5-import/pairs.json results/jev/m3-5-validation.jsonl \
  results/validation-interpretations-m3-5.jsonl \
  results/test-interpretations-m3-5.jsonl; do
  mkdir -p "$(dirname -- "$input")"
  cp "$ORIGINAL/$input" "$input"
done

uv run --locked python scripts/validate_dataset.py data/processed/m3-5-v1.jsonl \
  --review data/raw/m3-5-reviews-v1.jsonl --ready
uv run --locked python -m orchestra check-collection --dataset data/processed/m3-5-v1.jsonl \
  --parent data/processed/m3-v1.jsonl --types data/raw/m3-5-import/types.json \
  --pairs data/raw/m3-5-import/pairs.json --out data/raw/m3-5-import/collection-check.json
uv run --locked python -m orchestra prepare-study --config configs/m3-5.json \
  --review data/raw/m3-5-reviews-v1.jsonl --collection-brief docs/collection-brief-m3-5.md \
  --out data/processed/m3-5-prepared.json
uv run --locked python - <<'PY'
import json
from pathlib import Path

from orchestra.data import file_sha256

log = "results/jev/m3-5-validation.jsonl"
config = json.loads(Path("data/processed/m3-5-prepared.json").read_text())
config["configurations"].append(
    {"family": "Jev", "responses": log, "responses_sha256": file_sha256(log)}
)
Path("data/processed/m3-5-prepared-jev.json").write_text(json.dumps(config, indent=2) + "\n")
PY

scripts/run_experiment.sh --config data/processed/m3-5-prepared-jev.json --run-id m6-repro
uv run --locked python -m orchestra select --run results/m6-repro \
  --out results/m6-repro-selection.json
uv run --locked python -m orchestra report --run results/m6-repro \
  --selection results/m6-repro-selection.json \
  --train data/processed/m3-5/train.jsonl --validation data/processed/m3-5/validation.jsonl
uv run --locked python -m orchestra confidence --run results/m6-repro \
  --selection results/m6-repro-selection.json --out results/m4-5-validation
uv run --locked python -m orchestra freeze --confidence results/m4-5-validation \
  --error-review results/validation-interpretations-m3-5.jsonl \
  --jev-test-log results/jev/m3-5-test.jsonl --out results/frozen-study-m3-5.json
cp "$ORIGINAL/results/jev/m3-5-test.jsonl" results/jev/m3-5-test.jsonl
uv run --locked python -m orchestra final-test --freeze results/frozen-study-m3-5.json \
  --out results/final-test-m3-5 --replay-jev-test
uv run --locked python -m orchestra test-review --final-test results/final-test-m3-5 \
  --interpretations results/test-interpretations-m3-5.jsonl
uv run --locked python -m orchestra figures --run results/m6-repro \
  --selection results/m6-repro-selection.json \
  --train data/processed/m3-5/train.jsonl --validation data/processed/m3-5/validation.jsonl \
  --confidence results/m4-5-validation --final results/final-test-m3-5 \
  --out results/m5-figures
uv run --locked python report/plot_reliability.py
git diff --exit-code -- report/figures
uv run --locked python scripts/compare_study.py --original "$ORIGINAL" --reproduced . \
  --run-id m6-repro
