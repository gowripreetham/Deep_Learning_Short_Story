"""LLM-as-judge labelling — H / C / A per probe-response pair."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm import LLM, LLMConfig  # noqa: E402


JUDGE_TEMPLATE = """You are a strict factuality judge.

Question:
{question}

Reference answer (ground truth):
{reference}

Model response:
{response}

{rubric}

Respond with EXACTLY one character: H, C, or A. No explanation.
"""


def load_config(cfg_path: str) -> dict:
    with open(cfg_path) as f:
        return yaml.safe_load(f)


def parse_label(raw: str) -> str:
    """Be lenient: take the first valid character we see."""
    raw = raw.strip().upper()
    for ch in raw:
        if ch in {"H", "C", "A"}:
            return ch
    return "A"  # if the judge couldn't decide, treat as abstention


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--in", dest="in_path", default="results/responses.jsonl")
    ap.add_argument("--out", default="results/labels.jsonl")
    ap.add_argument("--judge", help="override judge.name")
    ap.add_argument("--judge-base-url", help="override judge.base_url")
    args = ap.parse_args()

    cfg = load_config(args.config)
    if args.judge:
        cfg["judge"]["name"] = args.judge
    if args.judge_base_url:
        cfg["judge"]["base_url"] = args.judge_base_url

    j = cfg["judge"]
    judge_llm = LLM(LLMConfig(
        name=j["name"],
        base_url=j["base_url"],
        temperature=j.get("temperature", 0.0),
        max_tokens=j.get("max_tokens", 64),
    ))

    rows = []
    with open(args.in_path) as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    print(f"[judge] judging {len(rows)} responses with {j['name']}")
    with open(args.out, "w") as out:
        for i, r in enumerate(rows, 1):
            prompt = JUDGE_TEMPLATE.format(
                question=r["question"],
                reference=r["reference"],
                response=r["response"],
                rubric=j["rubric"],
            )
            try:
                raw = judge_llm.complete(
                    "You are a precise classifier. Output one character only.",
                    prompt,
                )
            except Exception as e:  # noqa: BLE001
                raw = "A"  # treat error as abstention
                print(f"  [{i:02d}] judge error on {r['id']}: {e}")
            label = parse_label(raw)
            out.write(json.dumps({**r, "label": label, "judge_raw": raw}) + "\n")
            print(f"  [{i:02d}/{len(rows)}] {r['id']}: {label}")

    print(f"[judge] wrote {args.out}")


if __name__ == "__main__":
    main()
