"""Tiny OpenAI-compatible client wrapper.

Works against any provider that exposes a chat-completions endpoint at
`{base_url}/chat/completions` (OpenAI, Together, Fireworks, Groq, vLLM,
Ollama with the openai shim, etc.).

We deliberately avoid a hard dependency on the `openai` package so the
harness runs anywhere with just `requests`.
"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class LLMConfig:
    name: str
    base_url: str = "https://api.openai.com/v1"
    api_key_env: str = "OPENAI_API_KEY"
    temperature: float = 0.0
    max_tokens: int = 256


class LLM:
    """Minimal chat-completions client."""

    def __init__(self, cfg: LLMConfig):
        self.cfg = cfg
        self.api_key = os.environ.get(cfg.api_key_env)
        if not self.api_key:
            raise RuntimeError(
                f"Missing {cfg.api_key_env} in environment. "
                "Set it to your provider's API key."
            )

    def complete(self, system: str, user: str, *, retries: int = 3) -> str:
        url = self.cfg.base_url.rstrip("/") + "/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.cfg.name,
            "temperature": self.cfg.temperature,
            "max_tokens": self.cfg.max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        last_err: Optional[Exception] = None
        for attempt in range(retries):
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=60)
                r.raise_for_status()
                return r.json()["choices"][0]["message"]["content"].strip()
            except Exception as e:  # noqa: BLE001 — keep harness resilient
                last_err = e
                time.sleep(2 ** attempt)
        raise RuntimeError(f"LLM call failed after {retries} retries: {last_err}")
