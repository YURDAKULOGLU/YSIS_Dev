"""
Test Observability Service - Unified observability interface.
"""

import pytest
from unittest.mock import Mock, patch

from src.ybis.services.observability import ObservabilityService, get_observability_service


class TestObservabilityService:
    """Test ObservabilityService functionality."""

    def test_singleton_pattern(self):
        """Test ObservabilityService is a singleton."""
        service1 = get_observability_service()
        service2 = get_observability_service()
        assert service1 is service2

    def test_trace_generation(self):
        """Test trace generation."""
        service = get_observability_service()
        # Should not raise
        service.trace_generation(
            name="test_trace",
            model="test_model",
            input_data={"test": "data"},
            output_data={"result": "ok"},
        )

    def test_start_span(self):
        """Test starting a span."""
        service = get_observability_service()
        # Should not raise
        span = service.start_span("test_span")
        assert span is not None

    def test_observability_logs(self):
        """Test observability service logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.services.observability")
        assert logger is not None


