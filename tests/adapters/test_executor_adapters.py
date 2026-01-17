"""
Executor Adapter Conformance Tests.

Tests for executor adapters (local_coder, aider).
"""

import pytest
from src.ybis.services.adapter_bootstrap import bootstrap_adapters
from src.ybis.adapters.registry import get_registry
from src.ybis.contracts import RunContext, Plan
from pathlib import Path


class TestExecutorAdapters:
    """Test executor adapter conformance."""

    def setup_method(self):
        """Set up test fixtures."""
        bootstrap_adapters()
        self.registry = get_registry()

    def test_local_coder_adapter_exists(self):
        """Test that local_coder adapter is registered."""
        adapter = self.registry.get("local_coder", adapter_type="executor")
        assert adapter is not None, "local_coder adapter should be registered"

    def test_local_coder_implements_protocol(self):
        """Test that local_coder implements ExecutorProtocol."""
        adapter = self.registry.get("local_coder", adapter_type="executor")
        if adapter is None:
            pytest.skip("local_coder adapter not available")

        # Check that adapter has generate_code method
        assert hasattr(
            adapter, "generate_code"
        ), "local_coder must implement generate_code() method"

        # Check that generate_code is callable
        assert callable(
            getattr(adapter, "generate_code")
        ), "local_coder generate_code must be callable"

    def test_aider_adapter_registered(self):
        """Test that aider adapter is registered (may not be available)."""
        adapters = self.registry.list_adapters(adapter_type="executor")
        aider_found = any(a["name"] == "aider" for a in adapters)
        assert aider_found, "aider adapter should be registered (even if not available)"

    def test_executor_adapter_types(self):
        """Test that executor adapters have correct type."""
        adapters = self.registry.list_adapters(adapter_type="executor")

        for adapter_info in adapters:
            assert (
                adapter_info["type"] == "executor"
            ), f"Adapter '{adapter_info['name']}' should have type 'executor'"


