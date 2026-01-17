"""
Test AIWaves Agents Adapter - Symbolic learning and pipeline optimization.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from src.ybis.adapters.aiwaves_agents import AIWavesAgentsAdapter


class TestAIWavesAgentsAdapter:
    """Test AIWavesAgentsAdapter functionality."""

    @pytest.fixture
    def adapter(self):
        """Create adapter instance."""
        return AIWavesAgentsAdapter()

    def test_adapter_initialization(self, adapter):
        """Test adapter can be initialized."""
        assert adapter is not None
        assert hasattr(adapter, "_available")
        assert isinstance(adapter._available, bool)

    def test_is_available(self, adapter):
        """Test is_available check."""
        available = adapter.is_available()
        assert isinstance(available, bool)

    @patch("src.ybis.adapters.aiwaves_agents.PROJECT_ROOT")
    def test_check_availability_when_exists(self, mock_project_root, adapter):
        """Test availability check when aiwaves-agents exists."""
        mock_path = MagicMock()
        mock_path.exists.return_value = True
        mock_project_root.__truediv__.return_value = mock_path

        adapter._check_availability()
        assert adapter._available is True

    @patch("src.ybis.adapters.aiwaves_agents.PROJECT_ROOT")
    def test_check_availability_when_not_exists(self, mock_project_root, adapter):
        """Test availability check when aiwaves-agents doesn't exist."""
        mock_path = MagicMock()
        mock_path.exists.return_value = False
        mock_project_root.__truediv__.return_value = mock_path

        adapter._check_availability()
        assert adapter._available is False

    def test_learn_when_not_available(self, adapter):
        """Test learn method when adapter is not available."""
        adapter._available = False

        trajectory = {"states": [1, 2, 3], "actions": ["a", "b"], "rewards": [0.5, 0.7]}
        result = adapter.learn(trajectory)

        assert result is not None
        assert "insights" in result
        assert "patterns" in result
        assert "improvements" in result
        assert "gradients" in result
        assert result["insights"] == []
        assert result["patterns"] == []

    def test_learn_when_available(self, adapter):
        """Test learn method when adapter is available."""
        adapter._available = True

        trajectory = {"states": [1, 2, 3], "actions": ["a", "b"], "rewards": [0.5, 0.7]}
        result = adapter.learn(trajectory)

        assert result is not None
        assert "insights" in result
        assert "patterns" in result
        assert "improvements" in result
        assert "gradients" in result
        assert "trajectory_length" in result
        assert result["trajectory_length"] == 3

    def test_learn_with_empty_trajectory(self, adapter):
        """Test learn method with empty trajectory."""
        adapter._available = True

        trajectory = {}
        result = adapter.learn(trajectory)

        assert result is not None
        assert "trajectory_length" in result
        assert result["trajectory_length"] == 0

    def test_update_pipeline_when_not_available(self, adapter):
        """Test update_pipeline when adapter is not available."""
        adapter._available = False

        pipeline = {"config": "value", "params": {"a": 1}}
        gradients = {"grad1": 0.5, "grad2": 0.3}

        result = adapter.update_pipeline(pipeline, gradients)

        assert result == pipeline  # Should return unchanged

    def test_update_pipeline_when_available(self, adapter):
        """Test update_pipeline when adapter is available."""
        adapter._available = True

        pipeline = {"config": "value", "params": {"a": 1}}
        gradients = {"grad1": 0.5, "grad2": 0.3}

        result = adapter.update_pipeline(pipeline, gradients)

        assert result is not None
        assert result != pipeline  # Should have update metadata
        assert "_update_metadata" in result
        assert result["_update_metadata"]["gradients_applied"] == 2

    def test_update_pipeline_preserves_original(self, adapter):
        """Test update_pipeline preserves original pipeline keys."""
        adapter._available = True

        pipeline = {"config": "value", "params": {"a": 1}}
        gradients = {}

        result = adapter.update_pipeline(pipeline, gradients)

        assert "config" in result
        assert "params" in result
        assert result["config"] == "value"

    def test_adapter_logs(self, adapter):
        """Test adapter has logging configured."""
        import logging
        logger = logging.getLogger("src.ybis.adapters.aiwaves_agents")
        assert logger is not None

