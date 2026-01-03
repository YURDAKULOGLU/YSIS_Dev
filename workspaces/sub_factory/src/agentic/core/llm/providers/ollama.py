import os
from typing import Optional

import httpx

from ..base import BaseProvider, ProviderCapabilities, ProviderResult


class OllamaProvider:
    name = "ollama"
    capabilities = ProviderCapabilities()

    def __init__(self, base_url: Optional[str] = None, default_model: str = "qwen2.5-coder:32b"):
        self.base_url = base_url or os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.default_model = default_model

    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: int = 2048
    ) -> ProviderResult:
        base = self.base_url.rstrip("/").replace("/v1", "")
        url = f"{base}/api/generate"

        payload = {
            "model": model or self.default_model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()

        content = data.get("response", "")
        return ProviderResult(
            content=content,
            model=payload["model"],
            provider=self.name,
            cached=False,
            cost=0.0,
            usage=None,
            metadata={"raw": data}
        )
