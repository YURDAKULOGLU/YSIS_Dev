"""
Event Bus Service - Adapter-based event publishing and subscription.

Provides a unified interface for event distribution with adapter support.
Default adapter is Redis, but can be extended with other backends (NATS, etc.).

This is a service (not core) and should be used via adapters.
"""

import json
import logging
from abc import ABC, abstractmethod
from collections.abc import Callable
from datetime import datetime
from typing import Any

from ..adapters.registry import get_registry
from ..services.policy import get_policy_provider

logger = logging.getLogger(__name__)


class EventBusAdapter(ABC):
    """Base interface for event bus adapters."""

    @abstractmethod
    def is_available(self) -> bool:
        """Check if adapter backend is available."""
        ...

    @abstractmethod
    def publish(self, event_type: str, data: dict[str, Any], namespace: str = "ybis") -> bool:
        """Publish an event."""
        ...

    @abstractmethod
    async def subscribe_async(
        self, event_types: list[str], callback: Callable, namespace: str = "ybis"
    ) -> None:
        """Subscribe to events asynchronously."""
        ...


class RedisEventBusAdapter(EventBusAdapter):
    """Redis-based event bus adapter."""

    def __init__(self):
        """Initialize Redis adapter."""
        self._client = None
        self._available = False
        self._connect()

    def _connect(self) -> None:
        """Connect to Redis."""
        try:
            import os

            import redis

            host = os.getenv("REDIS_HOST", "localhost")
            port = int(os.getenv("REDIS_PORT", "6379"))
            db = int(os.getenv("REDIS_DB", "0"))
            password = os.getenv("REDIS_PASSWORD", None)

            self._client = redis.StrictRedis(
                host=host,
                port=port,
                db=db,
                password=password,
                decode_responses=True,
                socket_connect_timeout=1,  # Reduced to 1 second
                socket_timeout=1,  # Add socket timeout
            )
            # Ping with timeout
            self._client.ping()
            self._available = True
        except (ImportError, Exception):
            self._available = False

    def is_available(self) -> bool:
        """Check if Redis is available."""
        if not self._available:
            self._connect()
        return self._available

    def publish(self, event_type: str, data: dict[str, Any], namespace: str = "ybis") -> bool:
        """Publish event to Redis."""
        if not self.is_available():
            return False

        import os

        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "sender": os.getenv("AGENT_ID", "unknown-agent"),
        }

        channel = f"{namespace}:{event_type}"
        try:
            self._client.publish(channel, json.dumps(event))
            self._client.publish(f"{namespace}:events", json.dumps(event))
            return True
        except Exception:
            return False

    async def subscribe_async(
        self, event_types: list[str], callback: Callable, namespace: str = "ybis"
    ) -> None:
        """Subscribe to Redis events asynchronously."""
        if not self.is_available():
            return

        import asyncio

        channels = [f"{namespace}:{et}" for et in event_types]
        pubsub = self._client.pubsub()
        pubsub.subscribe(*channels)

        try:
            while True:
                message = pubsub.get_message(timeout=1.0)
                if message and message["type"] == "message":
                    try:
                        event = json.loads(message["data"])
                        if asyncio.iscoroutinefunction(callback):
                            await callback(event)
                        else:
                            callback(event)
                    except Exception:
                        pass  # Silently ignore callback errors

                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            pubsub.unsubscribe()
            raise


class EventBus:
    """
    Event Bus Service - Unified interface for event distribution.

    Uses adapter pattern to support multiple backends (Redis, NATS, etc.).
    Adapter selection is policy-driven.
    """

    def __init__(self):
        """Initialize event bus with adapter."""
        self._adapter: EventBusAdapter | None = None
        self._initialize_adapter()

    def _initialize_adapter(self) -> None:
        """Initialize event bus adapter based on policy."""
        policy = get_policy_provider()
        policy_config = policy.get_policy()

        # Check if event bus is enabled
        event_bus_config = policy_config.get("event_bus", {})
        if not event_bus_config.get("enabled", False):
            return  # Event bus disabled

        # Get adapter type from policy
        adapter_type = event_bus_config.get("adapter", "redis")

        # Try to get adapter from registry
        registry = get_registry()
        adapter = registry.get(f"{adapter_type}_event_bus", adapter_type="event_bus")

        if adapter and hasattr(adapter, "is_available") and adapter.is_available():
            self._adapter = adapter
        else:
            # Fallback: try direct instantiation for Redis
            if adapter_type == "redis":
                try:
                    redis_adapter = RedisEventBusAdapter()
                    if redis_adapter.is_available():
                        self._adapter = redis_adapter
                except Exception:
                    pass  # Redis not available

    def is_available(self) -> bool:
        """Check if event bus is available."""
        return self._adapter is not None and self._adapter.is_available()

    def publish(self, event_type: str, data: dict[str, Any], namespace: str = "ybis") -> bool:
        """
        Publish an event.

        Args:
            event_type: Event type (e.g., "task.completed")
            data: Event payload
            namespace: Channel namespace (default: "ybis")

        Returns:
            True if published successfully, False otherwise
        """
        if not self.is_available():
            return False

        return self._adapter.publish(event_type, data, namespace)

    async def subscribe_async(
        self, event_types: list[str], callback: Callable, namespace: str = "ybis"
    ) -> None:
        """
        Subscribe to events asynchronously.

        Args:
            event_types: List of event types (or ['*'] for all)
            callback: Async or sync function to handle events
            namespace: Channel namespace
        """
        if not self.is_available():
            return

        await self._adapter.subscribe_async(event_types, callback, namespace)


# Standardized Event Types
class Events:
    """Standardized event types for system observability."""

    # Task Lifecycle
    TASK_CREATED = "task.created"
    TASK_CLAIMED = "task.claimed"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
    TASK_BLOCKED = "task.blocked"

    # Run Lifecycle
    RUN_STARTED = "run.started"
    RUN_COMPLETED = "run.completed"
    RUN_FAILED = "run.failed"

    # Gate Decisions
    GATE_PASS = "gate.pass"
    GATE_BLOCK = "gate.block"
    GATE_REQUIRE_APPROVAL = "gate.require_approval"

    # Execution
    EXECUTION_STARTED = "execution.started"
    EXECUTION_COMPLETED = "execution.completed"
    EXECUTION_FAILED = "execution.failed"

    # Verification
    VERIFICATION_STARTED = "verification.started"
    VERIFICATION_COMPLETED = "verification.completed"
    VERIFICATION_FAILED = "verification.failed"

    # Health
    HEALTH_CHECK = "health.check"
    HEALTH_DEGRADED = "health.degraded"
    HEALTH_RECOVERED = "health.recovered"
    HEALTH_RECOVERY_FAILED = "health.recovery_failed"
    CONFIG_CHANGED = "config.changed"


# Global event bus instance (lazy initialization)
_event_bus: EventBus | None = None


def get_event_bus() -> EventBus:
    """Get global event bus instance."""
    global _event_bus
    if _event_bus is None:
        _event_bus = EventBus()
    return _event_bus

