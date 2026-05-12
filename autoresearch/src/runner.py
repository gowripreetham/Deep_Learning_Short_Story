"""Generate model responses for every probe in the dataset."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from llm import LLM, LLMConfig  # noqa: E402


def load_config(cfg_path: str) -> dict:
    with open(cfg_path) as f:
        return yaml.safe_load(f)


def load_probes(path: str, n: int | None = None) -> list[dict]:
    items = []
    with open(path) as f:
        for line in f:
            if line.strip():
                items.append(json.loads(line))
    if n is not None:
        items = items[:n]
    return items


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--model", help="override model_under_test.name")
    ap.add_argument("--base-url", help="override model_under_test.base_url")
    ap.add_argument("--n", type=int, help="override run.n_probes")
    ap.add_argument("--out", default="results/responses.jsonl")
    args = ap.parse_args()

    cfg = load_config(args.config)
    if args.model:
        cfg["model_under_test"]["name"] = args.model
    if args.base_url:
        cfg["model_under_test"]["base_url"] = args.base_url
    if args.n:
        cfg["run"]["n_probes"] = args.n

    mut = cfg["model_under_test"]
    llm = LLM(LLMConfig(
        name=mut["name"],
        base_url=mut["base_url"],
        temperature=mut.get("temperature", 0.0),
        max_tokens=mut.get("max_tokens", 256),
    ))

    probes = load_probes(cfg["run"]["data_path"], cfg["run"]["n_probes"])
    os.makedirs(os.path.dirname(args.out), exist_ok=True)

    print(f"[runner] {len(probes)} probes against {mut['name']}")
    with open(args.out, "w") as f:
        for i, p in enumerate(probes, 1):
            try:
                resp = llm.complete(mut["system_prompt"], p["question"])
            except Exception as e:  # noqa: BLE001
                resp = f"[ERROR: {e}]"
            row = {
                "id": p["id"],
                "category": p["category"],
                "question": p["question"],
                "reference": p["reference"],
                "response": resp,
                "model": mut["name"],
            }
            f.write(json.dumps(row) + "\n")
            print(f"  [{i:02d}/{len(probes)}] {p['id']}: {resp[:80]}")

    print(f"[runner] wrote {args.out}")


if __name__ == "__main__":
    main()
