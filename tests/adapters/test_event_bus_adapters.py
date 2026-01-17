"""
Event Bus Adapter Conformance Tests.

Tests for event bus adapters (redis_event_bus).
"""

import pytest
from src.ybis.services.adapter_bootstrap import bootstrap_adapters
from src.ybis.adapters.registry import get_registry


class TestEventBusAdapters:
    """Test event bus adapter conformance."""

    def setup_method(self):
        """Set up test fixtures."""
        bootstrap_adapters()
        self.registry = get_registry()

    def test_redis_event_bus_registered(self):
        """Test that redis event bus adapter is registered."""
        adapters = self.registry.list_adapters(adapter_type="event_bus")
        redis_found = any(a["name"] == "redis_event_bus" for a in adapters)
        assert redis_found, "redis_event_bus adapter should be registered"

    def test_event_bus_adapter_protocol(self):
        """Test that event bus adapters implement required methods."""
        adapters = self.registry.list_adapters(adapter_type="event_bus")

        for adapter_info in adapters:
            name = adapter_info["name"]
            adapter = self.registry.get(name)

            if adapter is None:
                # Adapter not available (dependencies missing)
                continue

            # Check required methods
            assert hasattr(
                adapter, "publish"
            ), f"Event bus adapter '{name}' must implement publish()"
            assert hasattr(
                adapter, "subscribe_async"
            ), f"Event bus adapter '{name}' must implement subscribe_async()"
            assert hasattr(
                adapter, "is_available"
            ), f"Event bus adapter '{name}' must implement is_available()"


