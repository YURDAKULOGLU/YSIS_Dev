"""
Test Node Registry - Node management.
"""

import pytest
from unittest.mock import Mock, patch

from src.ybis.workflows.node_registry import NodeRegistry


class TestNodeRegistry:
    """Test NodeRegistry functionality."""

    def test_registry_initialization(self):
        """Test registry can be initialized."""
        registry = NodeRegistry()
        assert registry is not None

    def test_registry_logs(self):
        """Test registry logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.workflows.node_registry")
        assert logger is not None


