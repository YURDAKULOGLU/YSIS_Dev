"""
Unified Message Protocol for Inter-Agent Communication.

Defines abstract base class for all messaging backends, similar to UnifiedTask.
Supports: Redis pub/sub, file-based, database (SQLite), SPADE XMPP, and MCP.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from datetime import datetime

from src.agentic.core.protocols import InterAgentMessage


class MessageProtocol(ABC):
    """Abstract base class for all messaging backends."""
    
    def __init__(self, backend_name: str, metadata: Dict[str, Any] = None):
        self.backend_name = backend_name
        self.metadata = metadata or {}
    
    @abstractmethod
    async def send(self, message: InterAgentMessage) -> bool:
        """Send a message. Returns True if successful."""
        pass
    
    @abstractmethod
    async def receive(self, agent_id: str, timeout: Optional[float] = None) -> Optional[InterAgentMessage]:
        """Receive a message for the given agent. Blocks until message arrives or timeout."""
        pass
    
    @abstractmethod
    async def subscribe(self, agent_id: str, callback: callable) -> bool:
        """Subscribe to messages for the given agent. Callback receives InterAgentMessage."""
        pass
    
    @abstractmethod
    async def unsubscribe(self, agent_id: str) -> bool:
        """Unsubscribe from messages for the given agent."""
        pass
    
    @abstractmethod
    async def get_unread_count(self, agent_id: str) -> int:
        """Get count of unread messages for the given agent."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the messaging backend is available."""
        pass

