"""
Tests for Planner Config Integration.

DoD:
- Unit test: Planner initializes with model from YAML
"""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.ybis.orchestrator.planner import LLMPlanner


def test_planner_uses_config():
    """Test that planner initializes with model from YAML config."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test profile
        profile_dir = Path(tmpdir) / "configs" / "profiles"
        profile_dir.mkdir(parents=True, exist_ok=True)
        profile_path = profile_dir / "default.yaml"

        profile_data = {
            "llm": {
                "planner_model": "ollama/test-model:1b",
                "coder_model": "ollama/test-coder:1b",
                "api_base": "http://localhost:9999",
            },
        }
        profile_path.write_text(yaml.dump(profile_data), encoding="utf-8")

        # Mock PROJECT_ROOT
        import src.ybis.services.policy as policy_module

        original_root = policy_module.PROJECT_ROOT
        policy_module.PROJECT_ROOT = Path(tmpdir)

        try:
            # Reset singleton
            from src.ybis.services.policy import PolicyProvider

            PolicyProvider._instance = None
            PolicyProvider._policy = None

            # Load profile explicitly - this will be used by planner
            provider = PolicyProvider()
            provider.load_profile("default")

            # Verify provider loaded correctly
            llm_config = provider.get_llm_config()
            assert llm_config.get("planner_model") == "ollama/test-model:1b"

            # Create planner - should use the same singleton
            planner = LLMPlanner()

            # Verify it uses config values
            assert planner.model == "ollama/test-model:1b"
            assert planner.api_base == "http://localhost:9999"

        finally:
            policy_module.PROJECT_ROOT = original_root
            PolicyProvider._instance = None
            PolicyProvider._policy = None
