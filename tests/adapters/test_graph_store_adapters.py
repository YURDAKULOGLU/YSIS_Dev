"""
Graph Store Adapter Conformance Tests.

Tests for graph store adapters (neo4j).
"""

import pytest
from src.ybis.services.adapter_bootstrap import bootstrap_adapters
from src.ybis.adapters.registry import get_registry


class TestGraphStoreAdapters:
    """Test graph store adapter conformance."""

    def setup_method(self):
        """Set up test fixtures."""
        bootstrap_adapters()
        self.registry = get_registry()

    def test_neo4j_adapter_registered(self):
        """Test that neo4j adapter is registered."""
        adapters = self.registry.list_adapters(adapter_type="graph_store")
        neo4j_found = any(a["name"] == "neo4j_graph" for a in adapters)
        assert neo4j_found, "neo4j_graph adapter should be registered"

    def test_graph_store_adapter_protocol(self):
        """Test that graph store adapters implement required methods."""
        adapters = self.registry.list_adapters(adapter_type="graph_store")

        for adapter_info in adapters:
            name = adapter_info["name"]
            adapter = self.registry.get(name)

            if adapter is None:
                # Adapter not available (dependencies missing)
                continue

            # Check required methods
            assert hasattr(
                adapter, "impact_analysis"
            ), f"Graph store adapter '{name}' must implement impact_analysis()"
            assert hasattr(
                adapter, "find_circular_dependencies"
            ), f"Graph store adapter '{name}' must implement find_circular_dependencies()"
            assert hasattr(
                adapter, "get_critical_nodes"
            ), f"Graph store adapter '{name}' must implement get_critical_nodes()"
            assert hasattr(
                adapter, "is_available"
            ), f"Graph store adapter '{name}' must implement is_available()"


