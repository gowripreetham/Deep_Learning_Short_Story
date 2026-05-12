#!/usr/bin/env bash
# End-to-end glue: generate -> judge -> score.
#
# Usage examples:
#   bash run.sh --model gpt-4o-mini --judge gpt-4o --n 60
#   bash run.sh --model meta-llama/Llama-3.1-8B-Instruct \
#               --judge gpt-4o \
#               --base-url https://api.together.xyz/v1 \
#               --n 60

set -euo pipefail

MODEL=""
JUDGE=""
BASE_URL=""
JUDGE_BASE_URL=""
N=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model)          MODEL="$2"; shift 2 ;;
    --judge)          JUDGE="$2"; shift 2 ;;
    --base-url)       BASE_URL="$2"; shift 2 ;;
    --judge-base-url) JUDGE_BASE_URL="$2"; shift 2 ;;
    --n)              N="$2"; shift 2 ;;
    *) echo "unknown arg: $1" >&2; exit 1 ;;
  esac
done

cd "$(dirname "$0")"

PYTHON=${PYTHON:-python3}

ARGS_RUN=( --config configs/default.yaml )
[[ -n "$MODEL"    ]] && ARGS_RUN+=( --model "$MODEL" )
[[ -n "$BASE_URL" ]] && ARGS_RUN+=( --base-url "$BASE_URL" )
[[ -n "$N"        ]] && ARGS_RUN+=( --n "$N" )

ARGS_JUDGE=( --config configs/default.yaml )
[[ -n "$JUDGE"          ]] && ARGS_JUDGE+=( --judge "$JUDGE" )
[[ -n "$JUDGE_BASE_URL" ]] && ARGS_JUDGE+=( --judge-base-url "$JUDGE_BASE_URL" )

echo "==> [1/3] generating model responses"
"$PYTHON" src/runner.py "${ARGS_RUN[@]}"

echo "==> [2/3] judging responses"
"$PYTHON" src/judge.py "${ARGS_JUDGE[@]}"

echo "==> [3/3] scoring + plotting"
"$PYTHON" src/score.py --config configs/default.yaml

echo "==> done. see results/summary.json and results/hallucination_by_category.png"
