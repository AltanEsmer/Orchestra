#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
uv sync --locked
uv run --locked python scripts/smoke.py
uv run --locked python -m unittest discover -s tests
uv run --locked ruff check .
uv run --locked ruff format --check .
git diff --check
