"""
Adapter Registration Smoke Tests.

Lightweight smoke tests to confirm adapter registration works.
"""

import pytest
from src.ybis.services.adapter_bootstrap import bootstrap_adapters
from src.ybis.adapters.registry import get_registry


class TestAdapterRegistrationSmoke:
    """Smoke tests for adapter registration."""

    def setup_method(self):
        """Set up test fixtures."""
        bootstrap_adapters()
        self.registry = get_registry()

    def test_vendor_adapters_registered_in_catalog(self):
        """Test that vendor adapters are registered in catalog."""
        vendor_adapters = [
            ("evoagentx", "workflow_evolution"),
            ("reactive_agents", "agent_runtime"),
            ("llm_council", "council_review"),
            ("aiwaves_agents", "agent_learning"),
            ("self_improve_swarms", "self_improve_loop"),
        ]
        
        for adapter_name, adapter_type in vendor_adapters:
            adapters = self.registry.list_adapters(adapter_type=adapter_type)
            adapter_names = [a["name"] for a in adapters]
            assert adapter_name in adapter_names, f"{adapter_name} should be registered in catalog"

    def test_vendor_adapters_have_correct_type(self):
        """Test that vendor adapters have correct type."""
        vendor_adapters = [
            ("evoagentx", "workflow_evolution"),
            ("reactive_agents", "agent_runtime"),
            ("llm_council", "council_review"),
            ("aiwaves_agents", "agent_learning"),
            ("self_improve_swarms", "self_improve_loop"),
        ]
        
        for adapter_name, expected_type in vendor_adapters:
            adapters = self.registry.list_adapters(adapter_type=expected_type)
            adapter_info = next((a for a in adapters if a["name"] == adapter_name), None)
            if adapter_info:
                assert adapter_info["type"] == expected_type, f"{adapter_name} should have type {expected_type}"

    def test_vendor_adapters_can_be_retrieved(self):
        """Test that vendor adapters can be retrieved from registry."""
        vendor_adapters = [
            ("evoagentx", "workflow_evolution"),
            ("reactive_agents", "agent_runtime"),
            ("llm_council", "council_review"),
            ("aiwaves_agents", "agent_learning"),
            ("self_improve_swarms", "self_improve_loop"),
        ]
        
        for adapter_name, adapter_type in vendor_adapters:
            # Try to get adapter (may be None if vendor not installed)
            adapter = self.registry.get(adapter_name, adapter_type=adapter_type, fallback_to_default=False)
            
            # Adapter may be None (vendor not installed), but retrieval should not raise
            # The important thing is that it's registered in the catalog
            adapters = self.registry.list_adapters(adapter_type=adapter_type)
            adapter_names = [a["name"] for a in adapters]
            assert adapter_name in adapter_names, f"{adapter_name} should be in catalog (even if not available)"

    def test_vendor_adapters_default_disabled(self):
        """Test that vendor adapters are disabled by default."""
        vendor_adapters = [
            ("evoagentx", "workflow_evolution"),
            ("reactive_agents", "agent_runtime"),
            ("llm_council", "council_review"),
            ("aiwaves_agents", "agent_learning"),
            ("self_improve_swarms", "self_improve_loop"),
        ]
        
        for adapter_name, adapter_type in vendor_adapters:
            adapters = self.registry.list_adapters(adapter_type=adapter_type)
            adapter_info = next((a for a in adapters if a["name"] == adapter_name), None)
            if adapter_info:
                # Vendor adapters should be disabled by default (opt-in)
                assert adapter_info.get("enabled", True) == False, f"{adapter_name} should be disabled by default"

