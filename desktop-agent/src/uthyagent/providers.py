"""Provider configuration and OpenAI-compatible chat client."""
from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any

import httpx


@dataclass(frozen=True)
class ProviderConfig:
    base_url: str = "https://openrouter.ai/api/v1"
    model: str = "openrouter/free"
    api_key: str = ""
    timeout_seconds: float = 45.0

    @classmethod
    def from_environment(cls) -> "ProviderConfig":
        return cls(
            base_url=os.getenv("UTHYAGENT_BASE_URL", "https://openrouter.ai/api/v1").rstrip("/"),
            model=os.getenv("UTHYAGENT_MODEL", "openrouter/free"),
            api_key=os.getenv("UTHYAGENT_API_KEY", os.getenv("OPENROUTER_API_KEY", "")),
            timeout_seconds=float(os.getenv("UTHYAGENT_TIMEOUT", "45")),
        )


class ProviderError(RuntimeError):
    """Raised when a provider request fails or returns an invalid response."""


class OpenAICompatibleProvider:
    """Minimal OpenAI-compatible chat completions client.

    Keys should be stored in the desktop Secret Service in the full application.
    Environment variables are supported for development and CI only.
    """

    def __init__(self, config: ProviderConfig) -> None:
        self.config = config

    async def chat(self, messages: list[dict[str, str]]) -> str:
        if not self.config.api_key:
            raise ProviderError(
                "No API key configured. Add a key in Settings or use a local provider."
            )
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/uthumany/uthy-agentic-os",
            "X-Title": "UthyAgent",
        }
        payload: dict[str, Any] = {
            "model": self.config.model,
            "messages": messages,
        }
        try:
            async with httpx.AsyncClient(timeout=self.config.timeout_seconds) as client:
                response = await client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                body = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise ProviderError(f"Provider request failed: {exc}") from exc

        try:
            content = body["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError("Provider response did not contain a chat message.") from exc
        if not isinstance(content, str) or not content.strip():
            raise ProviderError("Provider returned an empty response.")
        return content.strip()


def available_presets() -> list[dict[str, str]]:
    """Return endpoint presets; free model availability changes over time."""
    return [
        {
            "name": "OpenRouter Free",
            "base_url": "https://openrouter.ai/api/v1",
            "model": "openrouter/free",
        },
        {
            "name": "Ollama Local",
            "base_url": "http://localhost:11434/v1",
            "model": "qwen2.5:7b",
        },
        {
            "name": "LM Studio Local",
            "base_url": "http://localhost:1234/v1",
            "model": "local-model",
        },
    ]
