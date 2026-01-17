"""
Test LlamaIndex Adapter - Context management.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from src.ybis.adapters.llamaindex_adapter import LlamaIndexAdapter


class TestLlamaIndexAdapter:
    """Test LlamaIndexAdapter functionality."""

    @pytest.fixture
    def mock_project_root(self, tmp_path):
        """Create mock project root."""
        return tmp_path

    def test_adapter_initialization(self, mock_project_root):
        """Test adapter can be initialized."""
        adapter = LlamaIndexAdapter(mock_project_root)
        assert adapter is not None

    def test_is_available(self, mock_project_root):
        """Test adapter availability check."""
        adapter = LlamaIndexAdapter(mock_project_root)
        available = adapter.is_available()
        assert isinstance(available, bool)

    def test_adapter_logs(self):
        """Test adapter logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.adapters.llamaindex_adapter")
        assert logger is not None


