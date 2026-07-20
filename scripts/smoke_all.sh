#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 "$ROOT/evals/run_evals.py"
python3 "$ROOT/evals/run_pipeline_smoke.py"
python3 "$ROOT/subskills/continuity-bridge/evals/run_smoke.py"
python3 "$ROOT/subskills/assist-mode-router/evals/run_smoke.py"
echo ALL_SMOKE_PASS
