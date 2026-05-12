"""Aggregate judge labels into per-category and overall stats; plot."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import yaml

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402


def load_config(cfg_path: str) -> dict:
    with open(cfg_path) as f:
        return yaml.safe_load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/default.yaml")
    ap.add_argument("--in", dest="in_path", default="results/labels.jsonl")
    ap.add_argument("--out-summary", default="results/summary.json")
    ap.add_argument("--out-plot", default="results/hallucination_by_category.png")
    args = ap.parse_args()

    cfg = load_config(args.config)
    cats = cfg["categories"]

    rows = []
    with open(args.in_path) as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))

    by_cat: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        by_cat[r["category"]][r["label"]] += 1

    summary = {"by_category": {}, "overall": {}}
    overall = Counter()
    for cat, name in cats.items():
        c = by_cat[cat]
        n = sum(c.values()) or 1
        summary["by_category"][cat] = {
            "name": name,
            "n": sum(c.values()),
            "hallucinated": c["H"],
            "correct": c["C"],
            "abstained": c["A"],
            "hallucination_rate": round(c["H"] / n, 3),
        }
        overall.update(c)

    n = sum(overall.values()) or 1
    summary["overall"] = {
        "n": sum(overall.values()),
        "hallucinated": overall["H"],
        "correct": overall["C"],
        "abstained": overall["A"],
        "hallucination_rate": round(overall["H"] / n, 3),
    }

    Path(args.out_summary).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_summary, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"[score] wrote {args.out_summary}")

    # Plot
    cat_codes = list(cats.keys())
    cat_names = [cats[c] for c in cat_codes]
    rates = [summary["by_category"][c]["hallucination_rate"] * 100 for c in cat_codes]
    overall_pct = summary["overall"]["hallucination_rate"] * 100

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(cat_names, rates, color=[
        "#1d4ed8" if r < overall_pct + 2 else "#b91c1c" for r in rates
    ])
    ax.axhline(overall_pct, color="#374151", linestyle="--", linewidth=1)
    ax.text(len(cat_names) - 0.5, overall_pct + 1.5,
            f"overall {overall_pct:.0f}%", ha="right", fontsize=10, color="#374151")
    ax.set_ylabel("hallucination rate (%)")
    ax.set_ylim(0, max(60, max(rates) + 10))
    ax.set_title(
        f"Hallucination rate by category — model: {rows[0].get('model','?')}, n={summary['overall']['n']}"
    )
    for b, r in zip(bars, rates):
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.7,
                f"{r:.0f}%", ha="center", fontsize=10, fontweight="bold")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(args.out_plot, dpi=140)
    print(f"[score] wrote {args.out_plot}")

    # Console summary
    print(f"\n=== overall ===")
    print(f"  n={summary['overall']['n']}  "
          f"H={summary['overall']['hallucinated']}  "
          f"C={summary['overall']['correct']}  "
          f"A={summary['overall']['abstained']}  "
          f"rate={overall_pct:.1f}%")
    print("=== by category ===")
    for c in cat_codes:
        s = summary["by_category"][c]
        print(f"  {c:>3}  {s['name']:<22}  "
              f"H={s['hallucinated']:>2}  C={s['correct']:>2}  A={s['abstained']:>2}  "
              f"rate={s['hallucination_rate']*100:.1f}%")


if __name__ == "__main__":
    main()
