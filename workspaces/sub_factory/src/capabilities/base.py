from typing import Protocol, Any, Dict, Optional

class Capability(Protocol):
    """
    Base interface for system capabilities (Sandbox, Git, Browser, etc.)
    """

    @property
    def name(self) -> str:
        ...

    async def is_available(self) -> bool:
        """Check if capability is ready (e.g. API keys present)"""
        ...
