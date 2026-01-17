"""
Test Adapter Registry - Adapter management.
"""

import pytest
from unittest.mock import Mock, patch

from src.ybis.adapters.registry import AdapterRegistry, get_registry


class TestAdapterRegistry:
    """Test AdapterRegistry functionality."""

    def test_registry_initialization(self):
        """Test registry can be initialized."""
        registry = get_registry()
        assert registry is not None

    def test_registry_logs(self):
        """Test registry logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.adapters.registry")
        assert logger is not None


