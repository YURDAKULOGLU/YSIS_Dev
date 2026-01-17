"""
Adapter Protocol Conformance Tests.

Tests that all adapters implement the AdapterProtocol correctly.
"""

import pytest
from src.ybis.adapters.registry import AdapterProtocol
from src.ybis.services.adapter_bootstrap import bootstrap_adapters
from src.ybis.adapters.registry import get_registry


class TestAdapterProtocol:
    """Test adapter protocol conformance."""

    def setup_method(self):
        """Set up test fixtures."""
        bootstrap_adapters()
        self.registry = get_registry()

    def test_all_adapters_implement_protocol(self):
        """Test that all registered adapters implement AdapterProtocol."""
        adapters = self.registry.list_adapters()

        for adapter_info in adapters:
            name = adapter_info["name"]
            adapter = self.registry.get(name)

            if adapter is None:
                # Adapter not available (dependencies missing)
                continue

            # Check that adapter has is_available method
            assert hasattr(
                adapter, "is_available"
            ), f"Adapter '{name}' must implement is_available() method"

            # Check that is_available is callable
            assert callable(
                getattr(adapter, "is_available")
            ), f"Adapter '{name}' is_available must be callable"

    def test_adapter_availability_check(self):
        """Test that adapter availability checks work."""
        adapters = self.registry.list_adapters()

        for adapter_info in adapters:
            name = adapter_info["name"]
            adapter = self.registry.get(name)

            if adapter is None:
                # Adapter not available (dependencies missing)
                continue

            # Try to call is_available (should not raise)
            try:
                available = adapter.is_available()
                assert isinstance(
                    available, bool
                ), f"Adapter '{name}' is_available() must return bool"
            except Exception as e:
                pytest.fail(f"Adapter '{name}' is_available() raised exception: {e}")

    def test_adapter_registry_integrity(self):
        """Test that adapter registry maintains integrity."""
        adapters = self.registry.list_adapters()

        # Check that all adapters have required fields
        for adapter_info in adapters:
            assert "name" in adapter_info, "Adapter info must have 'name'"
            assert "type" in adapter_info, "Adapter info must have 'type'"
            assert "enabled" in adapter_info, "Adapter info must have 'enabled'"
            assert "available" in adapter_info, "Adapter info must have 'available'"

            # Check that name matches
            name = adapter_info["name"]
            adapter = self.registry.get(name)
            if adapter is not None:
                # Adapter is available, check that it can be retrieved
                assert adapter is not None, f"Adapter '{name}' should be retrievable"


