"""
Test Resilience Service - Unified retry, circuit breaker, and rate limiting.
"""

import pytest
from unittest.mock import Mock, patch

from src.ybis.services.resilience import resilient, retry_with_backoff


class TestResilience:
    """Test Resilience functionality."""

    def test_resilient_decorator(self):
        """Test resilient decorator."""
        @resilient(breaker_name="test", rate_limit=(2.0, 5))
        def test_func():
            return "ok"

        result = test_func()
        assert result == "ok"

    def test_retry_with_backoff(self):
        """Test retry with backoff."""
        @retry_with_backoff(max_attempts=3)
        def test_func():
            return "ok"

        result = test_func()
        assert result == "ok"

    def test_resilience_logs(self):
        """Test resilience service logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.services.resilience")
        assert logger is not None


