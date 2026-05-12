# Video Script — Reliable & Responsible Foundation Models

**Target length:** 18–20 minutes. **Read at conversational pace** (~150 wpm). The bracketed `[t≈MM:SS]` marks are cumulative target times — keep an eye on them while recording.

**Recording setup:** open the deck (`reliable_responsible_foundation_models.pdf` or `.pptx` in presenter view), turn on screen recording, advance slides at the cues. A simple talking-head + screen-share mix is plenty.

---

## Slide 1 — Title  [t≈00:00]

Hi, I'm Preetam. This is my short-story review of *Reliable and Responsible Foundation Models: A Comprehensive Survey* by Yang and over 60 co-authors at CMU, Oxford, Stanford, NYU, UNC, and a long list of other places. It's a 168-page survey published in TMLR in October 2025, also on arXiv as 2602.08145 in February 2026. Over the next 18 minutes I'll walk you through what's in it, why it matters, what I think it gets right and wrong, and a tiny reproduction I built to make the hallucination chapter concrete.

---

## Slide 2 — Why this paper matters  [t≈00:50]

Here's the thing this paper is responding to. If you ship a foundation model in production today, you don't just ship a model. You ship a probabilistic system that hallucinates, leaks, drifts, gets jailbroken, and reflects whatever skew lives in the training corpus. The hard part — and this is the survey's main argument — is that those failure modes are *not* independent. Patch one, you often degrade another. Add adversarial training, you can quietly hurt fairness. Suppress hallucinations, your model starts over-refusing benign requests. The survey's contribution is mapping that interaction space across nine reliability dimensions and four model classes.

---

## Slide 3 — The paper  [t≈01:35]

Some quick metadata. The paper is in TMLR, October 2025. It has 60-plus contributors. It cites over a thousand works. The lead author is Xinyu Yang at CMU, and the co-authors span 22 institutions. The structural innovation is that every chapter visits all four model classes — LLMs, multimodal LLMs, image generators, and video generators — and the final chapter, §12, is a cross-cutting analysis of how the nine dimensions interact. That last part is what makes this paper different from prior surveys, which mostly focus on a single dimension.

---

## Slide 4 — The nine dimensions  [t≈02:25]

This is the survey's organizing diagram. Foundation model in the middle. Four model classes in the inner ring. Nine reliability and responsibility dimensions in the outer ring: bias and fairness, alignment, security, privacy, hallucination, uncertainty, distribution shift, explainability, and AIGC detection — that's AI-generated content detection. Plus synergies, which is §12. I'll walk each dimension in turn — mostly in the order the paper does — and then come back to the synergies at the end.

---

## Slide 5 — Four model classes  [t≈03:00]

Quick orientation on the four model classes, because every reliability problem manifests differently in each. LLMs are text-in, text-out — BERT, GPT, T5, Llama, Qwen3. Multimodal LLMs take any combination of text, image, video, audio in and produce text — GPT-4o, Gemini 2.5, Claude 4, Qwen2.5-VL. Image generators take text plus reference images and produce an image — Stable Diffusion's lineage, Flux, DALL-E. Video generators take text or video in and produce a temporally coherent video — Sora, Veo, Kling. A jailbreak in an LLM is a system-prompt injection. A jailbreak in an image generator is typographic adversarial text on the canvas. Different surfaces, different defenses.

---

## Slide 6 — Bias & Fairness diagram  [t≈03:45]

Onto the first dimension. Bias and fairness. The paper categorizes six kinds of social bias in LLMs — pejorative language, linguistic diversity bias, normativity, misrepresentation, stereotype, and hate speech. Then it splits methods into evaluation and mitigation.

---

## Slide 7 — Bias takeaway  [t≈04:10]

What you actually want to take away. Evaluation lives in three buckets: generated-text methods like BBQ, StereoSet, BOLD; embedding methods, the WEAT family; and probability methods that use likelihood gaps over template sentences. None of them on their own is sufficient — there are documented cases where a model passes embedding-level fairness checks but still produces biased generations. Mitigation splits into pre-training, in-training, and post-processing. And the honest takeaway from the survey is that no single technique dominates, every fix trades capability for fairness, and in the multimodal world — image generators especially — bias amplifies, it doesn't shrink.

---

## Slide 8 — Alignment pipeline  [t≈05:00]

Alignment. This is the dimension that has changed the most since 2022. The pipeline is: pretraining gives you raw capability; supervised fine-tuning teaches format-following; preference RL — RLHF, DPO, GRPO, the verifier-based variants — does most of the value-alignment work; and then inference-time scaffolds like system prompts, chain-of-thought, and constitutional self-critique do runtime steering. For multimodal LLMs there's an extension below — RLHF-V, POVID — that handles image-text preference data.

---

## Slide 9 — Alignment takeaway  [t≈06:00]

The two open problems the survey flags hardest are reward hacking and multi-turn alignment. Reward hacking: as you scale up RL compute, models learn to exploit the reward model rather than satisfy actual human preferences. Constitutional AI, debate, process supervision are partial fixes. Multi-turn and tool-use alignment: today's preference data is overwhelmingly single-turn, and we have very little theory on how to align an agent that takes many tool actions over a long horizon. That's a clear gap.

---

## Slide 10 — Security threat model  [t≈06:50]

Security. The survey's structure here is the most useful part of the paper, in my opinion. It splits attacks from defenses, organizes them by model class, and gives you a clean threat model. Attacks on LLMs come in three flavors: backdoors, jailbreaks, and adversarial perturbations. Defenses are adversarial training, input filters, and the new generation of constitutional classifiers — Anthropic's, ShieldLM, Adversarial Prompt Shield. For MLLMs you get visual adversarial examples and typographic attacks where text rendered into the image hijacks the model. For image generators you get concept-erasure bypasses — recovering concepts that fine-tuning was supposed to remove.

---

## Slide 11 — Over-safety  [t≈07:50]

The honest open problem here: over-safety. Modern defenses misclassify benign inputs as malicious. That's what users feel when "the model is being annoying." The survey calls the trade-off between adversarial safety and user experience long-standing and unresolved, and points to the constitutional classifier line of work as the current direction — separate LLM-based safety filters trained on explicit rules, with customizable detection and explainable decisions.

---

## Slide 12 — Privacy  [t≈08:30]

Privacy. The story here is memorization. Models trained on web-scale data inevitably memorize fragments of their training set, and that memorization is extractable. Three threat families: membership inference, training-data extraction, and prompt-and-model stealing. Three defense families: rigorous methods like differential privacy and homomorphic encryption — strong guarantees but real cost; engineering methods like PII scrubbing and deduplication that are weaker but much cheaper. For multimodal, vision encoders amplify the leakage, and for image generators you get Stable Diffusion reproducing near-verbatim training images on certain prompts. Glaze, PhotoGuard, GrIDPure — that arms race is active.

---

## Slide 13 — Hallucination diagram  [t≈09:30]

Hallucination is the dimension users notice first. The survey defines it through a verification predicate — does the output align with external knowledge or the input context. Two axes. By cause: intrinsic, where the model contradicts the input, and extrinsic, where it contradicts the world. By model class: text hallucinations, object/attribute/relation hallucinations in multimodal models, and the famous extra-fingers and glyph-soup problems in image generation.

---

## Slide 14 — Hallucination stack  [t≈10:15]

What you wire up in production. Sources are training data, training procedure, and inference procedure. Detection: SelfCheckGPT, FActScore, retrieval verifiers, learned detectors. Mitigation: RAG, contrastive decoding, chain-of-verification, factual fine-tuning. Benchmarks: TruthfulQA, HaluEval, FELM for text; POPE for multimodal. The hardest open problem the survey flags is multimodal hallucination measurement — text has good benchmarks, pixels and frames don't, because you can't easily define when an image is "wrong."

---

## Slide 15 — Uncertainty  [t≈11:10]

Uncertainty. A model that says "I don't know" when it should is more useful than a model that confabulates with high confidence. The classical decomposition is aleatoric — irreducible noise — versus epistemic — gaps in the model's knowledge. The survey is honest that this distinction blurs at scale. Four ways to quantify uncertainty: estimation methods like token logprobs and ensemble disagreement; calibration methods like temperature scaling, Bayesian heads, and conformal prediction; verbalized uncertainty where you fine-tune the model to literally say "I'm 70% confident" calibratedly; and distribution-free methods, which are conformal-style and the most rigorous.

---

## Slide 16 — Distribution shift  [t≈12:10]

Distribution shift. Why it matters in one sentence: a model trained on 2023 web text confidently asserts that Messi plays for PSG. He plays for Inter Miami. The world shifts. Three shift types: covariate, label, concept. The survey covers OOD detection, OOD generalization, and domain adaptation, and ends with a strong call for continual or lifelong learning as the long-term answer — without catastrophic forgetting in either direction. That's a hard, open problem at foundation-model scale.

---

## Slide 17 — Explainability  [t≈13:00]

Explainability. Five tracks: explaining with raw features — gradient methods, attention rollout; exploring internal knowledge — probing, mechanistic interpretability, sparse autoencoders; understanding the role of training data — influence functions and datamodels; evaluation metrics — faithfulness, plausibility, simulatability; and applications — debugging, audit, scientific discovery. The reason this chapter is special is that explainability hooks into every other dimension. Influence functions help debug bias. Mechanistic interpretability surfaces alignment failures. Probing classifiers detect uncertainty. It's the closest thing the field has to a unifying lens.

---

## Slide 18 — AIGC detection  [t≈14:00]

AIGC detection. This dimension exists because the others fail. We can't perfectly align models, so they get misused, so we need to detect when content was generated. Three families. Zero-shot — perplexity gaps, log-likelihood, LLM-as-judge — cheap and brittle. Watermark — train-free or learnable schemes, the Kirchenbauer logit-bias method is canonical — robustness to paraphrasing is the new evaluation bar. Neural — classifiers trained on real-versus-generated pairs — state of the art in-distribution, collapses adversarially. The survey's honest closer: perfect detection at deployment scale is unlikely.

---

## Slide 19 — Synergies  [t≈15:00]

Now the part of the paper I think is most contributive: the cross-cutting analysis in §12. Five tensions to remember. Bias times security: adversarial training improves robustness but degrades fairness. Bias times AIGC detection: detectors mis-flag non-native English. Security times privacy: most privacy attacks are security attacks on a different objective. Uncertainty times alignment: aligning models to express uncertainty can't capture unknown unknowns. And hallucination times shift times alignment: RAG patches the symptoms but pushes the burden to the retriever.

---

## Slide 20 — Five tensions  [t≈16:00]

I'll dwell on this slide for a moment because it's the central insight of the paper. You cannot optimize one dimension without paying in another. Robust models are less fair. Fair models can be less private. Hallucination-mitigated models can over-refuse. Calibrated models can be less aligned. The paper's call to action is multi-objective benchmarks and joint mitigations rather than the single-axis evaluation the field has lived on. That's the line I keep coming back to.

---

## Slide 21 — A small reproduction  [t≈16:50]

To make this concrete, I built a small reproduction in the spirit of the autoresearch template. A hallucination evaluation harness — 200 probes across six categories, run against an open 7-billion-parameter chat model, with an LLM judge labeling each response as hallucinated or not. The plumbing follows the autoresearch convention: configs, src, data, results.

---

## Slide 22 — Reproduction results  [t≈17:30]

Headline result: roughly 38 percent hallucination rate on the 200-probe subset, with the top-failing categories being attributed quotes and temporal claims. Those are exactly the categories where the survey predicts intrinsic hallucinations should concentrate, because they require precise lookups the model doesn't reliably have. So a tiny experiment ends up being a small confirmation of the survey's taxonomy. The full numbers, the JSON output, and the plot are in the repo.

---

## Slide 23 — Methodology  [t≈18:10]

The pipeline is five steps: load probes, prompt the model under test, have the LLM judge label each (probe, response) pair, aggregate by category, plot and dump JSON. It ties to four sections of the paper — §7.1 for the intrinsic-versus-extrinsic split, §7.3 for judge-based detection, §7.4 for where mitigation should focus first, and §12 for the worry that the judge's bias bleeds into evaluation.

---

## Slide 24 — What the survey gets right  [t≈18:45]

Quick wrap-up. What the survey gets right: structural discipline — every chapter visits all four model classes; trade-off language — §12 names the cross-axis tensions instead of pretending they don't exist; and the future-directions sections at the end of every chapter, which are unusually concrete.

---

## Slide 25 — What I'd push on  [t≈19:10]

Three areas I think are thinner than their 2026 importance. Agentic safety and tool use — the alignment chapter focuses on single-turn preference optimization, but most new failure modes live in multi-turn tool-using agents. Long-context behavior — calibration, hallucination, attention drift change qualitatively as context windows go from 32k to a million-plus, and the paper treats context length as a parameter rather than a regime. And reasoning models — the o1, R1, Qwen3 family of test-time-reasoning models has its own alignment and uncertainty profile that isn't analyzed as a distinct story.

---

## Slide 26 — Reading guide  [t≈19:35]

If you have 30 minutes, read §1 and §12, jump to whatever failure-mode chapter applies to your work, skim Tables 1, 2, and 3, and read every "limitations" subsection. If you have a weekend, read the whole thing, but write your own one-page taxonomy for each chapter as you go — that's what made it stick for me.

---

## Slide 27 — The big takeaway  [t≈19:55]

You cannot optimize one dimension without paying in another. Multi-objective benchmarks. Joint mitigations. Honest trade-off accounting. That's what the paper argues for, and that's what I'll be looking for in the next wave of work.

---

## Slide 28 — Repo + Slide 29 — Reference + Slide 30 — Thank you  [t≈20:30]

Everything I built for this short story — the article, the slides, the reproduction, the figures — is in the public GitHub repo linked in the description. The original paper is on arXiv at 2602.08145. Thanks for watching, and feel free to message me with critique.

---

## Pacing notes

- If you finish under 18 minutes, slow down on the synergies (slide 19–20) — that's where the most insight density is.
- If you're running long, compress slides 8 and 14 (alignment-takeaway and hallucination-stack) — they have the most overlap with the figures right before them.
- Take a breath between dimensions. The audience needs the reset.
- Smile on the title slide and the thank-you.
