"""
Test CrewAI Adapter - Multi-agent orchestration.
"""

import pytest

from src.ybis.adapters.crewai_adapter import get_crewai_adapter, CrewAIAdapter


class TestCrewAIAdapter:
    """Test CrewAI adapter functionality."""

    def test_adapter_initialization(self):
        """Test adapter can be initialized (if available)."""
        adapter = get_crewai_adapter()
        # May be None if CrewAI not installed
        if adapter is not None:
            assert isinstance(adapter, CrewAIAdapter)

    def test_adapter_is_available(self):
        """Test adapter availability check."""
        adapter = get_crewai_adapter()
        if adapter is not None:
            assert hasattr(adapter, "is_available")
            # Check doesn't raise
            available = adapter.is_available()
            assert isinstance(available, bool)

    def test_adapter_policy_integration(self):
        """Test adapter reads from policy."""
        adapter = get_crewai_adapter()
        if adapter is not None:
            # Should have LLM config from policy
            assert hasattr(adapter, "llm_model")
            assert hasattr(adapter, "api_base")

    @pytest.mark.skip(reason="Requires CrewAI SDK")
    def test_create_crew(self):
        """Test crew creation."""
        # This would require actual CrewAI SDK
        pass

    @pytest.mark.skip(reason="Requires CrewAI SDK")
    def test_execute_crew(self):
        """Test crew execution."""
        # This would require actual CrewAI SDK
        pass


