"""
Sandbox Adapter Conformance Tests.

Tests for sandbox adapters (e2b_sandbox).
"""

import pytest
from src.ybis.services.adapter_bootstrap import bootstrap_adapters
from src.ybis.adapters.registry import get_registry


class TestSandboxAdapters:
    """Test sandbox adapter conformance."""

    def setup_method(self):
        """Set up test fixtures."""
        bootstrap_adapters()
        self.registry = get_registry()

    def test_e2b_adapter_registered(self):
        """Test that e2b adapter is registered."""
        adapters = self.registry.list_adapters(adapter_type="sandbox")
        e2b_found = any(a["name"] == "e2b_sandbox" for a in adapters)
        assert e2b_found, "e2b_sandbox adapter should be registered"

    def test_sandbox_adapter_protocol(self):
        """Test that sandbox adapters implement required methods."""
        adapters = self.registry.list_adapters(adapter_type="sandbox")

        for adapter_info in adapters:
            name = adapter_info["name"]
            adapter = self.registry.get(name)

            if adapter is None:
                # Adapter not available (dependencies missing)
                continue

            # Check required methods (context manager support)
            assert hasattr(
                adapter, "__enter__"
            ), f"Sandbox adapter '{name}' must support context manager (__enter__)"
            assert hasattr(
                adapter, "__exit__"
            ), f"Sandbox adapter '{name}' must support context manager (__exit__)"
            assert hasattr(
                adapter, "execute_command"
            ), f"Sandbox adapter '{name}' must implement execute_command()"
            assert hasattr(
                adapter, "is_available"
            ), f"Sandbox adapter '{name}' must implement is_available()"


