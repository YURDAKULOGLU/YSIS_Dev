"""
Test AutoGen Adapter - Multi-agent conversations.
"""

import pytest

from src.ybis.adapters.autogen_adapter import get_autogen_adapter, AutoGenAdapter


class TestAutoGenAdapter:
    """Test AutoGen adapter functionality."""

    def test_adapter_initialization(self):
        """Test adapter can be initialized (if available)."""
        adapter = get_autogen_adapter()
        # May be None if AutoGen not installed
        if adapter is not None:
            assert isinstance(adapter, AutoGenAdapter)

    def test_adapter_is_available(self):
        """Test adapter availability check."""
        adapter = get_autogen_adapter()
        if adapter is not None:
            assert hasattr(adapter, "is_available")
            # Check doesn't raise
            available = adapter.is_available()
            assert isinstance(available, bool)

    def test_adapter_policy_integration(self):
        """Test adapter reads from policy."""
        adapter = get_autogen_adapter()
        if adapter is not None:
            # Should have LLM config from policy
            assert hasattr(adapter, "llm_config")
            assert adapter.llm_config is not None

    @pytest.mark.skip(reason="Requires AutoGen SDK")
    def test_create_debate_group(self):
        """Test debate group creation."""
        # This would require actual AutoGen SDK
        pass

    @pytest.mark.skip(reason="Requires AutoGen SDK")
    def test_run_debate(self):
        """Test debate execution."""
        # This would require actual AutoGen SDK
        pass


