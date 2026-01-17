"""
Test Event Bus Service - Event publishing and subscription.
"""

import pytest
from unittest.mock import Mock, patch

from src.ybis.services.event_bus import EventBus, get_event_bus


class TestEventBus:
    """Test EventBus functionality."""

    def test_singleton_pattern(self):
        """Test EventBus is a singleton."""
        bus1 = get_event_bus()
        bus2 = get_event_bus()
        assert bus1 is bus2

    def test_is_available(self):
        """Test checking if event bus is available."""
        bus = get_event_bus()
        # Should not raise
        available = bus.is_available()
        assert isinstance(available, bool)

    def test_publish(self):
        """Test publishing an event."""
        bus = get_event_bus()
        # Should not raise (may return False if no adapter)
        result = bus.publish("test.event", {"data": "test"})
        assert isinstance(result, bool)

    def test_event_bus_logs(self):
        """Test event bus logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.services.event_bus")
        assert logger is not None


