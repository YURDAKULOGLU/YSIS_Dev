"""
Unified Message Manager for YBIS_Dev.

Provides a single interface to manage inter-agent communication across
various backends (Redis, file-based, database, SPADE XMPP, MCP) using
the MessageProtocol interface.
"""

from typing import Dict, Any, Optional, List, Callable

from src.agentic.core.protocols import InterAgentMessage
from src.agentic.infrastructure.message_protocol import MessageProtocol
from src.agentic.infrastructure.adapters.redis_adapter import RedisMessageAdapter
from src.agentic.infrastructure.adapters.file_based_adapter import FileBasedMessageAdapter
from src.agentic.infrastructure.adapters.db_adapter import DatabaseMessageAdapter
from src.agentic.infrastructure.adapters.spade_xmpp_adapter import SPADEXMPPMessageAdapter
from src.agentic.infrastructure.adapters.mcp_adapter import MCPMessageAdapter
from src.agentic.core.utils.logging_utils import log_event


class UnifiedMessageManager:
    """Manages inter-agent communication across all backends using unified interface."""
    
    def __init__(self, default_backend: str = "redis"):
        self.backends: Dict[str, MessageProtocol] = {}
        self.default_backend = default_backend
        self._initialize_backends()
    
    def _initialize_backends(self):
        """Initialize all available messaging backends."""
        # Redis (EventBus)
        try:
            redis_adapter = RedisMessageAdapter()
            if redis_adapter.is_available():
                self.backends["redis"] = redis_adapter
                log_event("Redis messaging backend initialized", component="unified_message_manager")
        except Exception as e:
            log_event(f"Redis backend initialization failed: {e}", component="unified_message_manager", level="warning")
        
        # File-based (AgentMessaging)
        try:
            file_adapter = FileBasedMessageAdapter()
            if file_adapter.is_available():
                self.backends["file"] = file_adapter
                log_event("File-based messaging backend initialized", component="unified_message_manager")
        except Exception as e:
            log_event(f"File-based backend initialization failed: {e}", component="unified_message_manager", level="warning")
        
        # Database (SQLite)
        try:
            db_adapter = DatabaseMessageAdapter()
            if db_adapter.is_available():
                self.backends["database"] = db_adapter
                log_event("Database messaging backend initialized", component="unified_message_manager")
        except Exception as e:
            log_event(f"Database backend initialization failed: {e}", component="unified_message_manager", level="warning")
        
        # SPADE XMPP
        try:
            spade_adapter = SPADEXMPPMessageAdapter()
            if spade_adapter.is_available():
                self.backends["spade"] = spade_adapter
                log_event("SPADE XMPP messaging backend initialized", component="unified_message_manager")
        except Exception as e:
            log_event(f"SPADE backend initialization failed: {e}", component="unified_message_manager", level="warning")
        
        # MCP
        try:
            mcp_adapter = MCPMessageAdapter()
            if mcp_adapter.is_available():
                self.backends["mcp"] = mcp_adapter
                log_event("MCP messaging backend initialized", component="unified_message_manager")
        except Exception as e:
            log_event(f"MCP backend initialization failed: {e}", component="unified_message_manager", level="warning")
    
    async def send(
        self,
        message: InterAgentMessage,
        backend: Optional[str] = None
    ) -> bool:
        """Send a message using the specified backend (or default)."""
        backend_name = backend or self.default_backend
        backend_instance = self.backends.get(backend_name)
        
        if not backend_instance:
            log_event(f"Backend '{backend_name}' not available, trying default '{self.default_backend}'", component="unified_message_manager", level="warning")
            backend_instance = self.backends.get(self.default_backend)
        
        if not backend_instance:
            log_event("No messaging backend available", component="unified_message_manager", level="error")
            return False
        
        if not backend_instance.is_available():
            log_event(f"Backend '{backend_name}' is not available", component="unified_message_manager", level="warning")
            return False
        
        log_event(f"Sending message via {backend_name}: {message.subject}", component="unified_message_manager")
        return await backend_instance.send(message)
    
    async def receive(
        self,
        agent_id: str,
        backend: Optional[str] = None,
        timeout: Optional[float] = None
    ) -> Optional[InterAgentMessage]:
        """Receive a message for the given agent."""
        backend_name = backend or self.default_backend
        backend_instance = self.backends.get(backend_name)
        
        if not backend_instance:
            backend_instance = self.backends.get(self.default_backend)
        
        if not backend_instance or not backend_instance.is_available():
            return None
        
        return await backend_instance.receive(agent_id, timeout)
    
    async def subscribe(
        self,
        agent_id: str,
        callback: Callable[[InterAgentMessage], None],
        backend: Optional[str] = None
    ) -> bool:
        """Subscribe to messages for the given agent."""
        backend_name = backend or self.default_backend
        backend_instance = self.backends.get(backend_name)
        
        if not backend_instance:
            backend_instance = self.backends.get(self.default_backend)
        
        if not backend_instance or not backend_instance.is_available():
            return False
        
        return await backend_instance.subscribe(agent_id, callback)
    
    async def unsubscribe(self, agent_id: str, backend: Optional[str] = None) -> bool:
        """Unsubscribe from messages for the given agent."""
        backend_name = backend or self.default_backend
        backend_instance = self.backends.get(backend_name)
        
        if not backend_instance:
            backend_instance = self.backends.get(self.default_backend)
        
        if not backend_instance or not backend_instance.is_available():
            return False
        
        return await backend_instance.unsubscribe(agent_id)
    
    async def get_unread_count(self, agent_id: str, backend: Optional[str] = None) -> int:
        """Get count of unread messages for the given agent."""
        backend_name = backend or self.default_backend
        backend_instance = self.backends.get(backend_name)
        
        if not backend_instance:
            backend_instance = self.backends.get(self.default_backend)
        
        if not backend_instance or not backend_instance.is_available():
            return 0
        
        return await backend_instance.get_unread_count(agent_id)
    
    def list_available_backends(self) -> List[str]:
        """List all available messaging backends."""
        return [name for name, backend in self.backends.items() if backend.is_available()]

