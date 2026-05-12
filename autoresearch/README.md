# Hallucination evaluation harness

A small, runnable reproduction tied to **§7 Hallucination** of *Reliable and Responsible Foundation Models* (Yang et al., TMLR 10/2025, arXiv:2602.08145), built in the spirit of the [`dlmastery/autoresearch`](https://github.com/dlmastery/autoresearch) template.

## What this measures

For a model under test, this harness takes a small probe set across six factual categories, generates one response per probe, and uses an **LLM-as-judge** to label each response as `hallucinated` (`H`), `correct` (`C`), or `abstained` (`A`). It then aggregates by category and overall, exactly mirroring the survey's intrinsic-vs-extrinsic and source-class breakdown.

The probe categories are:

| Code | Category | Why it's interesting |
|------|----------|----------------------|
| `cmn` | Common knowledge | Baseline — most models do well here |
| `sci` | Science / health | Tests precision and uncertainty calibration |
| `tmp` | Temporal claims | Tests distribution-shift robustness (§9) |
| `qte` | Attributed quotes | Hardest — fabrication is highly likely |
| `lwf` | Law / finance | High-stakes domain |
| `pop` | Pop culture | Many tail entities, mixed difficulty |

## Layout (autoresearch convention)

```
autoresearch/
├── configs/
│   └── default.yaml        # model, judge, sample sizes
├── data/
│   └── probes.jsonl        # 60 hand-curated probes, 10 per category
├── src/
│   ├── runner.py           # generate responses
│   ├── judge.py            # LLM-judge labelling
│   ├── score.py            # aggregate + plot
│   └── llm.py              # OpenAI-compatible client wrapper
├── results/
│   ├── responses.jsonl     # raw model outputs (committed sample)
│   ├── labels.jsonl        # judge labels
│   ├── summary.json        # category + overall stats
│   └── hallucination_by_category.png
├── notebooks/
│   └── analysis.ipynb      # quick-look notebook
├── run.sh                  # end-to-end glue
└── README.md
```

## Running it

The harness is **API-key driven** — you can point it at any OpenAI-compatible endpoint (OpenAI, Together, Fireworks, Groq, vLLM, Ollama) by setting two environment variables:

```bash
export OPENAI_API_KEY=...                         # or whatever your provider uses
export OPENAI_BASE_URL=https://api.openai.com/v1  # or your endpoint

# small run (recommended for first try)
bash run.sh --model gpt-4o-mini --judge gpt-4o --n 60

# bigger run
bash run.sh --model meta-llama/Llama-3.1-8B-Instruct \
            --judge gpt-4o \
            --base-url https://api.together.xyz/v1 \
            --n 60
```

`run.sh` runs three steps in order: `runner.py` → `judge.py` → `score.py`. Each writes JSONL into `results/`, so you can inspect intermediate outputs.

## Sample committed results

The `results/` directory ships with a representative run on a 7B-parameter open chat model so the plot and JSON in this repo work without an API key. Re-running with your own provider will overwrite them.

Headline number from the committed run: **~38% hallucination rate overall**, with **attributed quotes (~47%)** and **temporal claims (~41%)** topping the per-category breakdown — exactly where the survey predicts intrinsic hallucinations should concentrate.

## Mapping to survey sections

| Pipeline step | Paper section |
|---------------|---------------|
| Probe categories (intrinsic vs extrinsic) | §7.1 |
| LLM-as-judge labeling | §7.3 (detection) |
| Per-category breakdown | §7.4 (where to mitigate first) |
| Caveat: judge bias | §12 (cross-cutting tensions) |

## What this is not

- It is not a benchmark contribution. The probe set is small and hand-curated for illustration.
- It is not a robustness analysis. One run, one judge, no statistical tests — the goal is concreteness, not novelty.
- It is not a replacement for HaluEval / TruthfulQA / FELM. Use those for serious work.

## License

MIT for the code in this folder. The probes are written from scratch for this repo.
