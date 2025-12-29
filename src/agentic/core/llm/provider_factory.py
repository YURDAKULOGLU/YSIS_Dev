import os
from typing import List, Optional

from .base import BaseProvider, ProviderCapabilities
from .providers import OllamaProvider


class ProviderFactory:
    """
    Manual provider selector with a defined fallback chain.

    Modes:
    - manual: use OllamaProvider (default)
    - litellm: optional path via UniversalLLMProvider (feature-flagged elsewhere)
    """

    def __init__(self) -> None:
        self.fallback_chain = ["api", "cli", "ollama"]

    def get_default_mode(self) -> str:
        return os.getenv("YBIS_PROVIDER_MODE", "manual").lower()

    def select_provider(
        self,
        preferred: Optional[str] = None,
        required: Optional[ProviderCapabilities] = None
    ) -> BaseProvider:
        mode = (preferred or self.get_default_mode()).lower()

        if mode in ("api", "cli"):
            # Not implemented yet; fallback to Ollama.
            print(f"[ProviderFactory] '{mode}' provider not implemented. Falling back to ollama.")
            return OllamaProvider()

        return OllamaProvider()

    def get_fallback_chain(self) -> List[str]:
        return list(self.fallback_chain)
