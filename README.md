# Reliable & Responsible Foundation Models — short-story review

A graduate "short story" (paper review) of:

> **Yang, X., Han, J., Bommasani, R., Luo, J., Qu, W., Zhou, W., Bibi, A., Wang, X., Yoon, J., Stengel-Eskin, E., et al. (2025).** *Reliable and Responsible Foundation Models: A Comprehensive Survey.* **Transactions on Machine Learning Research, 10/2025.** arXiv:[2602.08145](https://arxiv.org/abs/2602.08145).

This repository contains every deliverable for the assignment in one public place: an original Medium article, a slide deck, a recorded walkthrough video, a runnable mini-reproduction (`autoresearch/`), original diagrams, and the source paper.

---

## Quick links

| Deliverable | Location |
|-------------|----------|
| Medium article (final published version) | **https://gowripreetam.medium.com/reliable-and-responsible-foundation-models-a-field-map-of-the-nine-open-problems-98eaba1c9db5** |
| Local article markdown (source) | [`article/article.md`](article/article.md) |
| Slide deck — `.pptx` | [`slides/reliable_responsible_foundation_models.pptx`](slides/reliable_responsible_foundation_models.pptx) |
| Slide deck — `.pdf` | [`slides/reliable_responsible_foundation_models.pdf`](slides/reliable_responsible_foundation_models.pdf) |
| SlideShare upload | **https://www.slideshare.net/slideshow/comprehensive-survey-on-reliable-and-responsible-foundation-models-challenges-and-trade-offs/287479450** |
| YouTube walkthrough video (15–25 min) | **https://youtu.be/uG_AHkDILo4** |
| Video script + recording checklist | [`video/`](video/) |
| Reproduction harness (autoresearch template) | [`autoresearch/`](autoresearch/) |
| Reproduction summary | [`autoresearch/results/summary.json`](autoresearch/results/summary.json) |
| Reproduction plot | [`autoresearch/results/hallucination_by_category.png`](autoresearch/results/hallucination_by_category.png) |
| Original diagrams (SVG + PNG) | [`figures/`](figures/) |
| Source paper (PDF) | [`paper/2602.08145v1.pdf`](paper/2602.08145v1.pdf) |

---

## What's in the article (TL;DR)

The paper is a 168-page survey of **nine reliability and responsibility dimensions** for foundation models (bias, alignment, security, privacy, hallucination, uncertainty, distribution shift, explainability, AIGC detection) across **four model classes** (LLMs, MLLMs, image generators, video generators). Its central contribution is a **cross-cutting analysis** (§12) of how those dimensions interact — adversarial training hurts fairness, RAG patches hallucinations but pushes the burden to the retriever, etc.

My short-story review:

1. Summarizes each chapter in original prose, with one figure per dimension.
2. Synthesizes the cross-cutting tensions the paper makes explicit.
3. Flags three areas I think are thinner than their 2026 importance (agentic safety, long-context regimes, reasoning models).
4. Includes a small runnable reproduction tied to **§7 Hallucination**.

---

## Repository layout

```
.
├── README.md                    ← this file
├── article/
│   └── article.md               ← ~4,000-word Medium article (publish from this)
├── slides/
│   ├── build_slides.js          ← pptxgenjs source for the deck
│   ├── reliable_responsible_foundation_models.pptx
│   └── reliable_responsible_foundation_models.pdf
├── video/
│   ├── video_script.md          ← slide-by-slide narration, 18–20 min
│   ├── recording_checklist.md   ← OBS / YouTube setup notes
│   ├── short_story_walkthrough.mp4    (created locally; not committed if >100MB)
│   └── youtube_link.txt         ← paste your final YouTube URL here
├── autoresearch/                ← runnable hallucination evaluation harness
│   ├── README.md
│   ├── configs/default.yaml
│   ├── data/probes.jsonl        ← 60 hand-curated probes, 6 categories
│   ├── src/
│   │   ├── llm.py               ← OpenAI-compatible client wrapper
│   │   ├── runner.py            ← generate model responses
│   │   ├── judge.py             ← LLM-as-judge labelling
│   │   └── score.py             ← aggregate + plot
│   ├── results/                 ← committed sample run on 7B chat model
│   │   ├── responses.jsonl
│   │   ├── labels.jsonl
│   │   ├── summary.json
│   │   └── hallucination_by_category.png
│   ├── notebooks/analysis.ipynb
│   ├── requirements.txt
│   └── run.sh                   ← end-to-end glue
├── figures/                     ← original SVG + rasterized PNG diagrams
│   ├── 01_overview_wheel.{svg,png}
│   ├── 02_bias_taxonomy.{svg,png}
│   ├── 03_alignment_pipeline.{svg,png}
│   ├── 04_security_threat.{svg,png}
│   ├── 05_hallucination_taxonomy.{svg,png}
│   ├── 06_synergies.{svg,png}
│   └── 07_results_bar.png
└── paper/
    └── 2602.08145v1.pdf         ← original survey
```

---

## Reproducing the experiment

```bash
cd autoresearch
pip install -r requirements.txt

# point at any OpenAI-compatible endpoint
export OPENAI_API_KEY=sk-...
export OPENAI_BASE_URL=https://api.openai.com/v1   # or your provider

# 60-probe run (default)
bash run.sh --model gpt-4o-mini --judge gpt-4o
```

Outputs land in `autoresearch/results/`. The committed sample run is on a 7B-parameter open chat model and reports an overall hallucination rate of 35%, with attributed quotes (50%) and temporal claims / law / finance (40%) topping the per-category breakdown — consistent with the paper's intrinsic-vs-extrinsic predictions.

See [`autoresearch/README.md`](autoresearch/README.md) for full details.

---

## Building the slide deck and article from source

```bash
# Slide deck
cd slides
npm install pptxgenjs
node build_slides.js
soffice --headless --convert-to pdf reliable_responsible_foundation_models.pptx

# Diagrams (regenerate PNGs from the SVG sources)
cd ../figures
python -c "import cairosvg, glob; [cairosvg.svg2png(url=f, write_to=f.replace('.svg','.png'), output_width=1800) for f in glob.glob('*.svg')]"
```

The Medium article in `article/article.md` is plain markdown with relative image paths into `figures/`. To publish on Medium, paste the markdown into the Medium editor; image upload is manual.

---

## Submitting

This assignment requires **public** access to: the GitHub repo (this directory), the Medium article, the SlideShare deck, and the YouTube video. Update the **Quick links** table above with all four URLs once each is published.

```bash
# create a new public repo on github.com first, then:
git init
git add .
git commit -m "Short-story review of Yang et al. 2025/2026"
git branch -M main
git remote add origin https://github.com/<your-username>/reliable-responsible-foundation-models-shortstory.git
git push -u origin main
```

If your local recorded video is >100 MB, do **not** commit it to git — upload to YouTube and put only the link in `video/youtube_link.txt`. Or use Git LFS.

---

## Reference

Yang, X., Han, J., Bommasani, R., Luo, J., Qu, W., Zhou, W., Bibi, A., Wang, X., Yoon, J., Stengel-Eskin, E., et al. (2025). *Reliable and Responsible Foundation Models: A Comprehensive Survey.* Transactions on Machine Learning Research, 10/2025. arXiv:2602.08145. [arxiv.org/abs/2602.08145](https://arxiv.org/abs/2602.08145).

---

## License

Code (`autoresearch/`, `slides/build_slides.js`) is MIT. The original survey PDF in `paper/` is the property of its authors and is included here for reference under fair-use research provisions; please cite the paper in any derived work. Original diagrams in `figures/` are released under CC BY 4.0.
