"""
Test ByteRover Adapter - Team knowledge sharing.
"""

import pytest

from src.ybis.adapters.byterover_adapter import get_byterover_adapter, ByteRoverAdapter
from src.ybis.data_plane.vector_store import VectorStore


class TestByteRoverAdapter:
    """Test ByteRover adapter functionality."""

    def test_adapter_initialization(self):
        """Test adapter can be initialized."""
        adapter = get_byterover_adapter()
        assert adapter is not None
        assert isinstance(adapter, ByteRoverAdapter)

    def test_adapter_is_available(self):
        """Test adapter availability check."""
        adapter = get_byterover_adapter()
        # Should always be available (has fallback)
        assert adapter.is_available() is True

    def test_adapter_policy_integration(self):
        """Test adapter reads from policy."""
        adapter = get_byterover_adapter()
        # Should have config from policy
        assert hasattr(adapter, "team_id")
        assert hasattr(adapter, "project_id")

    def test_share_knowledge_fallback(self):
        """Test share_knowledge with fallback (VectorStore)."""
        adapter = get_byterover_adapter()

        # Should work even if ByteRover not available
        result = adapter.share_knowledge(
            content="Test knowledge",
            tags=["test"],
        )

        assert result is not None
        assert "status" in result or "knowledge_id" in result

    def test_search_team_knowledge_fallback(self):
        """Test search_team_knowledge with fallback (VectorStore)."""
        adapter = get_byterover_adapter()

        # Should work even if ByteRover not available
        results = adapter.search_team_knowledge(
            query="test query",
            limit=5,
        )

        assert isinstance(results, list)

    @pytest.mark.skip(reason="Requires ByteRover SDK")
    def test_share_knowledge_cloud(self):
        """Test share_knowledge with cloud ByteRover."""
        # This would require actual ByteRover SDK
        pass

    @pytest.mark.skip(reason="Requires ByteRover SDK")
    def test_search_team_knowledge_cloud(self):
        """Test search_team_knowledge with cloud ByteRover."""
        # This would require actual ByteRover SDK
        pass


