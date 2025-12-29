from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol


@dataclass
class ProviderCapabilities:
    caching: bool = False
    structured_output: bool = False
    extended_thinking: bool = False
    video: bool = False


@dataclass
class ProviderResult:
    content: str
    model: str
    provider: str
    cached: bool = False
    cost: float = 0.0
    usage: Dict[str, Any] | None = None
    metadata: Dict[str, Any] | None = None


class BaseProvider(Protocol):
    name: str
    capabilities: ProviderCapabilities

    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.0,
        max_tokens: int = 2048
    ) -> ProviderResult:
        ...
