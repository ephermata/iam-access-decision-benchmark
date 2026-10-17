#!/usr/bin/env bash
# Run every model runner, then score each predictions file.
# API keys come from the environment (see .env.example). Laya runs locally.
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Jev ==="
if [ -n "${TYPESAFE_API_KEY:-}" ]; then
  python3 runners/run_jev.py --model jev-latest --out predictions_jev.jsonl
  python3 eval.py --cases cases.jsonl --predictions predictions_jev.jsonl \
    --out report_jev.md
else
  echo "SKIP: TYPESAFE_API_KEY not set"
fi

echo "=== Sage (Levanto) ==="
if [ -n "${LEVANTO_API_KEY:-}" ]; then
  python3 runners/run_sage.py --out predictions_sage.jsonl
  python3 eval.py --cases cases.jsonl --predictions predictions_sage.jsonl \
    --out report_sage.md
else
  echo "SKIP: LEVANTO_API_KEY not set"
fi

echo "=== Laya (local, open weights) ==="
python3 runners/run_laya.py --out predictions_laya.jsonl
python3 eval.py --cases cases.jsonl --predictions predictions_laya.jsonl \
  --out report_laya.md

echo "done."
