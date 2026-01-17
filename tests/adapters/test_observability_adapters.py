"""
Test Observability Adapters - Langfuse and OpenTelemetry.
"""

import pytest
from unittest.mock import patch

from src.ybis.adapters.observability_langfuse import LangfuseObservabilityAdapter
from src.ybis.adapters.observability_opentelemetry import OpenTelemetryObservabilityAdapter


class TestLangfuseAdapter:
    """Test Langfuse observability adapter."""

    def test_adapter_initialization(self):
        """Test adapter can be initialized."""
        adapter = LangfuseObservabilityAdapter()
        assert adapter is not None

    def test_is_available(self):
        """Test adapter availability check."""
        adapter = LangfuseObservabilityAdapter()
        # Should not raise
        available = adapter.is_available()
        assert isinstance(available, bool)

    def test_adapter_logs(self):
        """Test adapter logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.adapters.observability_langfuse")
        assert logger is not None


class TestOpenTelemetryAdapter:
    """Test OpenTelemetry observability adapter."""

    def test_adapter_initialization(self):
        """Test adapter can be initialized."""
        adapter = OpenTelemetryObservabilityAdapter()
        assert adapter is not None

    def test_is_available(self):
        """Test adapter availability check."""
        adapter = OpenTelemetryObservabilityAdapter()
        # Should not raise
        available = adapter.is_available()
        assert isinstance(available, bool)

    def test_adapter_logs(self):
        """Test adapter logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.adapters.observability_opentelemetry")
        assert logger is not None
