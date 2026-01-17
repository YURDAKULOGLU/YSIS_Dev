"""
Test Mem0 Adapter - Agent memory infrastructure.
"""

import pytest
from unittest.mock import Mock, patch

from src.ybis.adapters.mem0_adapter import get_mem0_adapter, Mem0Adapter
from src.ybis.data_plane.vector_store import VectorStore


class TestMem0Adapter:
    """Test Mem0 adapter functionality."""

    def test_adapter_initialization(self):
        """Test adapter can be initialized."""
        adapter = get_mem0_adapter()
        assert adapter is not None
        assert isinstance(adapter, Mem0Adapter)

    def test_adapter_is_available(self):
        """Test adapter availability check."""
        adapter = get_mem0_adapter()
        # Should always be available (has fallback)
        assert adapter.is_available() is True

    def test_adapter_policy_integration(self):
        """Test adapter reads from policy."""
        adapter = get_mem0_adapter()
        # Should have mode set
        assert hasattr(adapter, "mode")
        assert adapter.mode in ["cloud", "local", "auto", "fallback"]

    def test_add_memory_fallback(self):
        """Test add_memory with fallback (VectorStore)."""
        adapter = get_mem0_adapter()

        # Should work even if Mem0 not available (fallback to VectorStore)
        result = adapter.add_memory(
            messages=[
                {"role": "user", "content": "Test message"},
                {"role": "assistant", "content": "Test response"},
            ],
            agent_id="test-agent",
        )

        assert result is not None
        assert "status" in result or "memory_id" in result

    def test_search_memory_fallback(self):
        """Test search_memory with fallback (VectorStore)."""
        adapter = get_mem0_adapter()

        # Should work even if Mem0 not available
        results = adapter.search_memory(
            query="test query",
            agent_id="test-agent",
            limit=5,
        )

        assert isinstance(results, list)

    @pytest.mark.skip(reason="Requires Mem0 SDK")
    def test_add_memory_cloud(self):
        """Test add_memory with cloud Mem0."""
        # This would require actual Mem0 SDK
        pass

    @pytest.mark.skip(reason="Requires Mem0 SDK")
    def test_search_memory_cloud(self):
        """Test search_memory with cloud Mem0."""
        # This would require actual Mem0 SDK
        pass


