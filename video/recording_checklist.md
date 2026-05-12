# Recording checklist

## Before you hit record

- [ ] Open `slides/reliable_responsible_foundation_models.pdf` in full-screen presenter mode (or open the `.pptx` and present from slide 1).
- [ ] Open `video/video_script.md` on a second monitor or phone — it's structured one block per slide.
- [ ] Quiet room. Phone on Do Not Disturb. Close Slack/Discord/email.
- [ ] Quick mic test (30 sec) — listen back and confirm no clipping, no fan noise.
- [ ] Camera framing: head and shoulders, eyes ~1/3 from top of frame, lit from the front (window or lamp).

## Tools

| Need | Free option |
|------|-------------|
| Screen + camera recording | OBS Studio (Mac/Windows/Linux), or QuickTime + Photo Booth (Mac) |
| Lightweight edit | iMovie, DaVinci Resolve (free), or CapCut |
| YouTube upload | youtube.com/upload — set visibility to **Public** |

## OBS quick setup

1. Add Source → Display Capture (your slide screen).
2. Add Source → Video Capture Device (webcam) — resize to a small box bottom-right.
3. Add Source → Audio Input Capture (your mic).
4. Settings → Output → Recording → MP4, 1080p, 30fps.
5. Hit `Start Recording`, advance to slide 1, begin reading the script.

## During the take

- Aim for **18–20 minutes** total. The script has time cues (`[t≈MM:SS]`) — glance at them every few slides.
- One take is fine. Stumbles are normal — pause, breathe, re-do the sentence; you can splice it in edit. If you want zero edit, just keep going.
- Move forward through the slides at the marked points. Don't backtrack on screen — if you mis-advance, just narrate "let me go back" and continue.

## After the take

- Trim the dead air at the start and end.
- Export as MP4 (1080p H.264) and place at `video/short_story_walkthrough.mp4` — or upload to YouTube and put the link in `video/youtube_link.txt`.
- Do **not** commit the raw `.mp4` if it's > 100 MB; GitHub will reject it. Either:
  - Use Git LFS, or
  - Upload to YouTube and only commit the link.

## YouTube upload settings

- Title: `Reliable & Responsible Foundation Models — short-story review (Yang et al., TMLR 2025)`
- Visibility: **Public** (the rubric requires it)
- Description (paste this):

```
Short-story review of "Reliable and Responsible Foundation Models: A Comprehensive Survey" (Yang et al., TMLR 10/2025, arXiv:2602.08145).

A practitioner's tour through nine reliability dimensions — bias, alignment, security, privacy, hallucination, uncertainty, distribution shift, explainability, AIGC detection — and how they collide in production systems. Includes a small hallucination-evaluation reproduction in the spirit of the autoresearch template.

Companion artifacts:
- Article: <Medium URL>
- Slides:  <SlideShare URL>
- Code:    <GitHub repo URL>
- Paper:   https://arxiv.org/abs/2602.08145
```

- Tags: `foundation models, LLM, alignment, hallucination, AI safety, machine learning, survey, paper review`
- Category: Education
