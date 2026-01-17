"""
Tests for Dynamic Policy Loader.

DoD:
- Changing YAML file immediately changes syscall behavior
"""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.ybis.services.policy import PolicyProvider, get_policy_provider
from src.ybis.syscalls.exec import _is_allowed
from src.ybis.syscalls.fs import _is_protected


def test_policy_loader_yaml():
    """Test that policy loads from YAML file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test profile in correct location
        profile_dir = Path(tmpdir) / "configs" / "profiles"
        profile_dir.mkdir(parents=True, exist_ok=True)
        profile_path = profile_dir / "test.yaml"
        profile_data = {
            "profile": "test",
            "sandbox": {"enabled": True, "network": False},
            "exec": {"allowlist": ["python", "testcmd"]},
            "paths": {"protected": ["test/protected"]},
        }
        profile_path.write_text(yaml.dump(profile_data), encoding="utf-8")

        # Mock PROJECT_ROOT
        import src.ybis.services.policy as policy_module

        original_root = policy_module.PROJECT_ROOT
        policy_module.PROJECT_ROOT = Path(tmpdir)

        try:
            # Reset singleton
            PolicyProvider._instance = None
            PolicyProvider._policy = None

            provider = PolicyProvider()
            provider.load_profile("test")

            assert provider.get_exec_allowlist() == ["python", "testcmd"]
            assert provider.get_protected_paths() == ["test/protected"]
            assert provider.is_sandbox_enabled() is True
            assert provider.is_network_allowed() is False
        finally:
            policy_module.PROJECT_ROOT = original_root
            PolicyProvider._instance = None
            PolicyProvider._policy = None


def test_syscall_uses_policy():
    """Test that syscalls use policy from YAML."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test profile
        profile_path = Path(tmpdir) / "configs" / "profiles" / "default.yaml"
        profile_path.parent.mkdir(parents=True, exist_ok=True)

        profile_data = {
            "exec": {"allowlist": ["customcmd"]},
            "paths": {"protected": ["custom/protected"]},
        }
        profile_path.write_text(yaml.dump(profile_data), encoding="utf-8")

        # Mock PROJECT_ROOT
        import src.ybis.constants as const_module
        import src.ybis.services.policy as policy_module

        original_root = const_module.PROJECT_ROOT
        const_module.PROJECT_ROOT = Path(tmpdir)
        policy_module.PROJECT_ROOT = Path(tmpdir)

        try:
            # Reset policy provider
            PolicyProvider._instance = None
            PolicyProvider._policy = None

            # Test exec allowlist
            assert _is_allowed(["customcmd"]) is True
            assert _is_allowed(["python"]) is False  # Not in allowlist

            # Test protected paths
            test_path = Path(tmpdir) / "custom" / "protected" / "file.py"
            assert _is_protected(test_path) is True

        finally:
            const_module.PROJECT_ROOT = original_root
            policy_module.PROJECT_ROOT = original_root
            PolicyProvider._instance = None
            PolicyProvider._policy = None

