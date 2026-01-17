"""
Vector Store Adapter Conformance Tests.

Tests for vector store adapters (chroma, qdrant).
"""

import pytest
from src.ybis.services.adapter_bootstrap import bootstrap_adapters
from src.ybis.adapters.registry import get_registry


class TestVectorStoreAdapters:
    """Test vector store adapter conformance."""

    def setup_method(self):
        """Set up test fixtures."""
        bootstrap_adapters()
        self.registry = get_registry()

    def test_chroma_adapter_registered(self):
        """Test that chroma adapter is registered."""
        adapters = self.registry.list_adapters(adapter_type="vector_store")
        chroma_found = any(a["name"] == "chroma_vector_store" for a in adapters)
        assert chroma_found, "chroma_vector_store adapter should be registered"

    def test_qdrant_adapter_registered(self):
        """Test that qdrant adapter is registered."""
        adapters = self.registry.list_adapters(adapter_type="vector_store")
        qdrant_found = any(a["name"] == "qdrant_vector_store" for a in adapters)
        assert qdrant_found, "qdrant_vector_store adapter should be registered"

    def test_vector_store_adapter_protocol(self):
        """Test that vector store adapters implement required methods."""
        adapters = self.registry.list_adapters(adapter_type="vector_store")

        for adapter_info in adapters:
            name = adapter_info["name"]
            adapter = self.registry.get(name)

            if adapter is None:
                # Adapter not available (dependencies missing)
                continue

            # Check required methods
            assert hasattr(
                adapter, "add_documents"
            ), f"Vector store adapter '{name}' must implement add_documents()"
            assert hasattr(
                adapter, "query"
            ), f"Vector store adapter '{name}' must implement query()"
            assert hasattr(
                adapter, "is_available"
            ), f"Vector store adapter '{name}' must implement is_available()"


