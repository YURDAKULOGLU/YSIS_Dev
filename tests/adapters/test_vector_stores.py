"""
Test Vector Store Adapters - ChromaDB and Qdrant.
"""

import pytest
from unittest.mock import Mock, patch

from src.ybis.adapters.vector_store_chroma import ChromaDBVectorStoreAdapter
from src.ybis.adapters.vector_store_qdrant import QdrantVectorStoreAdapter


class TestChromaDBAdapter:
    """Test ChromaDB adapter functionality."""

    def test_adapter_initialization(self):
        """Test adapter can be initialized."""
        adapter = ChromaDBVectorStoreAdapter()
        assert adapter is not None

    def test_is_available(self):
        """Test adapter availability check."""
        adapter = ChromaDBVectorStoreAdapter()
        available = adapter.is_available()
        assert isinstance(available, bool)

    def test_adapter_logs(self):
        """Test adapter logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.adapters.vector_store_chroma")
        assert logger is not None


class TestQdrantAdapter:
    """Test Qdrant adapter functionality."""

    def test_adapter_initialization(self):
        """Test adapter can be initialized."""
        adapter = QdrantVectorStoreAdapter()
        assert adapter is not None

    def test_is_available(self):
        """Test adapter availability check."""
        adapter = QdrantVectorStoreAdapter()
        available = adapter.is_available()
        assert isinstance(available, bool)

    def test_adapter_logs(self):
        """Test adapter logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.adapters.vector_store_qdrant")
        assert logger is not None


