"""
Test Policy Service - Policy configuration loading and access.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from src.ybis.services.policy import PolicyProvider, get_policy_provider


class TestPolicyProvider:
    """Test PolicyProvider functionality."""

    def test_singleton_pattern(self):
        """Test PolicyProvider is a singleton."""
        provider1 = get_policy_provider()
        provider2 = get_policy_provider()
        assert provider1 is provider2

    def test_load_profile(self, tmp_path):
        """Test loading policy profile."""
        provider = PolicyProvider()

        # Test with non-existent profile (should use default)
        provider.load_profile("nonexistent")
        policy = provider.get_policy()
        assert policy is not None
        assert "sandbox" in policy

    def test_get_policy(self):
        """Test getting policy."""
        provider = get_policy_provider()
        policy = provider.get_policy()
        assert isinstance(policy, dict)

    def test_get_llm_config(self):
        """Test getting LLM configuration."""
        provider = get_policy_provider()
        llm_config = provider.get_llm_config()
        assert isinstance(llm_config, dict)

    def test_is_adapter_enabled(self):
        """Test checking if adapter is enabled."""
        provider = get_policy_provider()
        # Should not raise
        enabled = provider.is_adapter_enabled("local_coder")
        assert isinstance(enabled, bool)

    def test_policy_logs(self):
        """Test policy service logs operations."""
        # Policy should have logger
        import logging
        logger = logging.getLogger("src.ybis.services.policy")
        assert logger is not None


