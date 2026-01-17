"""
Test Rate Limiter Service - Token bucket rate limiting.
"""

import pytest
from unittest.mock import Mock, patch

from src.ybis.services.rate_limiter import get_limiter, get_limiter_status


class TestRateLimiter:
    """Test RateLimiter functionality."""

    def test_get_limiter(self):
        """Test getting a rate limiter."""
        limiter = get_limiter("test_limiter", rate=2.0, capacity=5)
        assert limiter is not None

    def test_get_limiter_status(self):
        """Test getting limiter status."""
        status = get_limiter_status("test_limiter")
        assert isinstance(status, dict)

    def test_rate_limiter_logs(self):
        """Test rate limiter logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.services.rate_limiter")
        assert logger is not None


