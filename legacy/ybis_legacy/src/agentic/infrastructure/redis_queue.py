"""
EventBus - Redis-based pub/sub for system observability.

Implements Constitution Article 7.1 (Observability).
Provides real-time event distribution for agents, workers, and dashboard.
"""

import json
import os
import threading
import asyncio
from datetime import datetime
from typing import Any, Callable, List, Optional, Union

import redis
from src.agentic.core.utils.logging_utils import log_event


class EventBus:
    """
    Thread-safe Singleton EventBus for system-wide event publishing.
    Supports both synchronous and asynchronous operations.

    Usage:
        from src.agentic.infrastructure.redis_queue import event_bus
        event_bus.publish("task.completed", {"task_id": "TASK-123", "status": "SUCCESS"})
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._host = os.getenv("REDIS_HOST", "localhost")
        self._port = int(os.getenv("REDIS_PORT", "6379"))
        self._db = int(os.getenv("REDIS_DB", "0"))
        self._password = os.getenv("REDIS_PASSWORD", None)

        self.redis_client: Optional[redis.StrictRedis] = None
        self._available = False
        self._connect()

        self._initialized = True

    def _connect(self):
        """Establish connection to Redis."""
        try:
            self.redis_client = redis.StrictRedis(
                host=self._host,
                port=self._port,
                db=self._db,
                password=self._password,
                decode_responses=True,
                socket_connect_timeout=2,
                retry_on_timeout=True
            )
            self.redis_client.ping()
            self._available = True
            log_event(f"Connected to Redis at {self._host}:{self._port}", component="event_bus")
        except (redis.ConnectionError, redis.TimeoutError) as e:
            self._available = False
            log_event(f"Redis connection failed: {e}", component="event_bus", level="warning")

    @property
    def available(self) -> bool:
        """Check if Redis is available and try to reconnect if not."""
        if not self._available:
            self._connect()
        return self._available

    def publish(self, event_type: str, data: dict[str, Any], namespace: str = "ybis") -> bool:
        """
        Publish an event to the bus.

        Args:
            event_type: Event type (e.g., "task.completed")
            data: Event payload
            namespace: Channel namespace (default: ybis)

        Returns:
            True if published successfully
        """
        if not self.available:
            return False

        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "sender": os.getenv("AGENT_ID", "unknown-agent")
        }

        channel = f"{namespace}:{event_type}"
        try:
            self.redis_client.publish(channel, json.dumps(event))
            # Also publish to a master broadcast channel
            self.redis_client.publish(f"{namespace}:events", json.dumps(event))
            return True
        except Exception as e:
            log_event(f"Failed to publish event {event_type}: {e}", component="event_bus", level="error")
            return False

    async def subscribe_async(self, event_types: List[str], callback: Callable, namespace: str = "ybis"):
        """
        Asynchronously subscribe to event types.

        Args:
            event_types: List of event types (or ['*'] for all)
            callback: Async or sync function to handle events
            namespace: Channel namespace
        """
        if not self.available:
            log_event("Cannot subscribe: Redis unavailable", component="event_bus", level="error")
            return

        channels = [f"{namespace}:{et}" for et in event_types]
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(*channels)

        log_event(f"Subscribed to {channels}", component="event_bus")

        try:
            while True:
                # Check for messages without blocking infinitely to allow for cancellation
                message = pubsub.get_message(timeout=1.0)
                if message and message["type"] == "message":
                    try:
                        event = json.loads(message["data"])
                        if asyncio.iscoroutinefunction(callback):
                            await callback(event)
                        else:
                            callback(event)
                    except Exception as e:
                        log_event(f"Error in event callback: {e}", component="event_bus", level="error")

                await asyncio.sleep(0.1)
        except asyncio.CancelledError:
            pubsub.unsubscribe()
            log_event("Unsubscribed from Redis channels", component="event_bus")
            raise

    def subscribe(self, event_types: List[str], callback: Callable, namespace: str = "ybis"):
        """Synchronous subscription (blocks the thread)."""
        if not self.available: return

        channels = [f"{namespace}:{et}" for et in event_types]
        pubsub = self.redis_client.pubsub()
        pubsub.subscribe(*channels)

        for message in pubsub.listen():
            if message["type"] == "message":
                try:
                    event = json.loads(message["data"])
                    callback(event)
                except Exception as e:
                    print(f"[EventBus] Callback error: {e}")


# Standardized Event Types (Constitution Article 7)
class Events:
    # Task Lifecycle
    TASK_CREATED = "task.created"
    TASK_CLAIMED = "task.claimed"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
    TASK_CANCELLED = "task.cancelled"

    # Code & Quality
    CODE_MODIFIED = "code.modified"
    TEST_FAILED = "test.failed"
    LINT_ERROR = "lint.error"
    COMMIT_SUCCESS = "commit.success"

    # Self-Healing & Intelligence
    ERROR_DETECTED = "error.detected"
    DEBATE_STARTED = "debate.started"
    DEBATE_REPLY = "debate.reply"
    DEBATE_CONCLUDED = "debate.concluded"
    PATTERN_LEARNED = "pattern.learned"
    SELF_HEAL_APPLIED = "self_heal.applied"

    # System State
    HEALTH_CHECK = "health.check"
    HEALTH_DEGRADED = "health.degraded"
    CONFIG_CHANGED = "config.changed"


# Singleton instance
event_bus = EventBus()


# Legacy compatibility
class RedisQueue:
    def __init__(self, host=None, port=None, db=0):
        self._bus = event_bus

    def publish(self, channel: str, message: str):
        # Map legacy channel to event_type if possible
        event_type = channel.split(':')[-1] if ':' in channel else channel
        try:
            data = json.loads(message) if isinstance(message, str) else message
            self._bus.publish(event_type, data)
        except:
            self._bus.publish("legacy_event", {"raw": message, "channel": channel})

    def subscribe(self, channels: List[str]):
        # Returns a pubsub object for legacy manual loops
        if not self._bus.available: return None
        pubsub = self._bus.redis_client.pubsub()
        pubsub.subscribe(*channels)
        return pubsub
