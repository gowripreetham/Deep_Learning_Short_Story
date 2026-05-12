# Submission checklist — work through this top-to-bottom

This is the exact set of steps to take everything in this folder from local files to a fully submitted assignment. It assumes you have a GitHub, Medium, SlideShare/LinkedIn, and YouTube account.

---

## 1. Sanity-check the repo locally

- [ ] `article/article.md` opens and renders correctly in your editor.
- [ ] `slides/reliable_responsible_foundation_models.pptx` opens in PowerPoint / Keynote / Google Slides without errors.
- [ ] `slides/reliable_responsible_foundation_models.pdf` displays cleanly.
- [ ] `figures/` contains 7 SVG and 7 PNG diagrams.
- [ ] `autoresearch/results/summary.json` exists, with overall + by-category numbers.
- [ ] `autoresearch/results/hallucination_by_category.png` displays correctly.
- [ ] `paper/2602.08145v1.pdf` is the original survey.

## 2. Push the public GitHub repo

- [ ] Create a new **public** repo on github.com — suggested name: `reliable-responsible-foundation-models-shortstory`.
- [ ] In this folder, run:

```bash
git init
git add .
git commit -m "Short-story review of Yang et al. 2025/2026 — initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo-name>.git
git push -u origin main
```

- [ ] Confirm in your browser that anyone (in incognito) can view the repo.
- [ ] Note the repo URL: `https://github.com/<you>/<repo>`

## 3. Publish the Medium article

- [ ] Sign in at https://medium.com.
- [ ] Click your profile → "Write".
- [ ] Paste the contents of `article/article.md` into the editor.
- [ ] Replace each `![...](../figures/XX.svg)` reference by uploading the matching PNG from `figures/` (Medium handles PNG/JPG, sometimes balks on SVG).
- [ ] Title: "Reliable and Responsible Foundation Models: A Field Map of the Nine Open Problems"
- [ ] Subtitle: "A practitioner's tour through Yang et al.'s 2025/2026 TMLR survey"
- [ ] Tags: `Machine Learning`, `LLM`, `AI Safety`, `Foundation Models`, `Paper Review`
- [ ] Click **Publish**.
- [ ] Copy the published URL.
- [ ] Open `README.md`, replace `<TODO: paste your Medium URL here>` with the URL.

## 4. Publish the slide deck

Easiest: upload to **SlideShare** (the rubric mentions it explicitly).

- [ ] Sign in at https://www.slideshare.net.
- [ ] Click "Upload" → upload `slides/reliable_responsible_foundation_models.pptx`.
- [ ] Title and description: copy the article's title and intro.
- [ ] Set visibility to **Public**.
- [ ] Copy the SlideShare URL.
- [ ] Replace `<TODO: paste your SlideShare URL here>` in `README.md`.

(Alternatives if SlideShare fails: speakerdeck.com, or upload as a Google Slides public link.)

## 5. Record + upload the video

Follow `video/recording_checklist.md`:

- [ ] Record 18–20 minute walkthrough using `video/video_script.md` and the slides.
- [ ] Export as MP4 (1080p H.264).
- [ ] Upload to YouTube as **Public**.
- [ ] Title: "Reliable & Responsible Foundation Models — short-story review (Yang et al., TMLR 2025)"
- [ ] Description: paste the block in `video/recording_checklist.md`.
- [ ] Copy the YouTube URL.
- [ ] Edit `video/youtube_link.txt` and paste the URL.
- [ ] Replace `<TODO: paste your YouTube URL here>` in `README.md`.

## 6. Final commit + push

```bash
git add README.md video/youtube_link.txt
git commit -m "Add Medium, SlideShare, and YouTube links"
git push
```

## 7. Submit on Canvas

- [ ] Go to the assignment page.
- [ ] Submission type: "Submitting a website url".
- [ ] URL: your public GitHub repo URL.
- [ ] Also paste the same URL into the class spreadsheet, per the assignment.

---

## What the rubric checks

| Rubric item | Where it lives in the repo |
|---|---|
| Survey paper from 2025/2026 in a top venue | `paper/2602.08145v1.pdf` (TMLR 10/2025) |
| Original-prose summary, not copy-paste | `article/article.md`, `slides/`, `video/video_script.md` |
| Many figures and illustrations | `figures/01–07.{svg,png}` |
| Reproduction with results | `autoresearch/` (configs, code, results, plot, notebook) |
| Public GitHub repo | confirmed in step 2 |
| Slide deck | `slides/*.pptx` and `*.pdf` |
| Medium article | step 3 link |
| SlideShare deck | step 4 link |
| YouTube walkthrough video | step 5 link |
| Proper README | `README.md` (you're reading the workflow side; the README is the entry point) |
| Paper cited in the article | citation block at the end of `article/article.md` |
