"""
Test DSPy Adapter - Prompt optimization.
"""

import pytest

from src.ybis.adapters.dspy_adapter import get_dspy_optimizer, DSPyPlannerOptimizer


class TestDSPyAdapter:
    """Test DSPy adapter functionality."""

    def test_adapter_initialization(self):
        """Test adapter can be initialized (if available)."""
        adapter = get_dspy_optimizer()
        # May be None if DSPy not installed
        if adapter is not None:
            assert isinstance(adapter, DSPyPlannerOptimizer)

    def test_adapter_is_available(self):
        """Test adapter availability check."""
        adapter = get_dspy_optimizer()
        if adapter is not None:
            assert hasattr(adapter, "is_available")
            # Check doesn't raise
            available = adapter.is_available()
            assert isinstance(available, bool)

    @pytest.mark.skip(reason="Requires DSPy SDK")
    def test_optimize(self):
        """Test prompt optimization."""
        # This would require actual DSPy SDK
        pass


