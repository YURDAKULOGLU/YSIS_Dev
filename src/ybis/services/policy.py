"""
Policy Provider - Loads and provides policy configuration from YAML files.

Singleton pattern for policy access across syscalls.
"""

import logging
import os
from typing import Any

import yaml

from ..constants import PROJECT_ROOT

logger = logging.getLogger(__name__)


class PolicyProvider:
    """
    Policy Provider - Singleton for policy configuration.

    Loads policy from YAML profiles and provides access to:
    - Sandbox settings
    - Exec allowlist
    - Protected paths
    """

    _instance: "PolicyProvider | None" = None
    _policy: dict[str, Any] | None = None

    def __new__(cls) -> "PolicyProvider":
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_profile(self, profile_name: str = "default") -> None:
        """
        Load policy profile from YAML.

        Args:
            profile_name: Profile name (default: "default")
        """
        env_profile = os.getenv("YBIS_PROFILE")
        if env_profile:
            profile_name = env_profile
        profile_path = PROJECT_ROOT / "configs" / "profiles" / f"{profile_name}.yaml"

        if not profile_path.exists():
            # Fallback to default hardcoded policy
            self._policy = {
                "sandbox": {"enabled": True, "network": False},
                "exec": {"allowlist": ["python", "pytest", "ruff", "ls", "cat"]},
                "paths": {"protected": ["src/ybis", "docs/governance", "configs"]},
            }
            return

        with open(profile_path, encoding="utf-8") as f:
            loaded_policy = yaml.safe_load(f) or {}
            # Ensure all required keys exist, preserve all sections
            self._policy = {
                "sandbox": loaded_policy.get("sandbox", {"enabled": True, "network": False}),
                "exec": loaded_policy.get("exec", {"allowlist": []}),
                "paths": loaded_policy.get("paths", {"protected": []}),
                "llm": loaded_policy.get("llm", {}),
                "planner": loaded_policy.get("planner", {}),
                "gates": loaded_policy.get("gates", {}),
                "verifier": loaded_policy.get("verifier", {}),
                "features": loaded_policy.get("features", {}),
                "openhands": loaded_policy.get("openhands", {}),
                "adapters": loaded_policy.get("adapters", {}),
                "event_bus": loaded_policy.get("event_bus", {"enabled": False}),
            }

    def get_policy(self) -> dict[str, Any]:
        """
        Get current policy configuration.

        Returns:
            Policy dictionary
        """
        if self._policy is None:
            self.load_profile()
        return self._policy or {}

    def get_protected_paths(self) -> list[str]:
        """
        Get list of protected paths.

        Returns:
            List of protected path patterns
        """
        policy = self.get_policy()
        return policy.get("paths", {}).get("protected", [])

    def get_exec_allowlist(self) -> list[str]:
        """
        Get exec command allowlist.

        Returns:
            List of allowed commands
        """
        policy = self.get_policy()
        return policy.get("exec", {}).get("allowlist", [])

    def is_sandbox_enabled(self) -> bool:
        """
        Check if sandbox is enabled.

        Returns:
            True if sandbox enabled
        """
        policy = self.get_policy()
        return policy.get("sandbox", {}).get("enabled", True)

    def get_sandbox_type(self) -> str:
        """
        Get sandbox type (e2b, local, docker).

        Returns:
            Sandbox type string
        """
        policy = self.get_policy()
        return policy.get("sandbox", {}).get("type", "local")

    def is_network_allowed(self) -> bool:
        """
        Check if network access is allowed.

        Returns:
            True if network allowed
        """
        policy = self.get_policy()
        return policy.get("sandbox", {}).get("network", False)

    def get_llm_config(self) -> dict[str, Any]:
        """
        Get LLM configuration.

        Returns:
            LLM config dictionary
        """
        policy = self.get_policy()
        return policy.get("llm", {})

    def get_verifier_config(self) -> dict[str, Any]:
        """
        Get verifier configuration.

        Returns:
            Verifier config dictionary
        """
        policy = self.get_policy()
        return policy.get("verifier", {})

    def is_adapter_enabled(self, adapter_name: str) -> bool:
        """
        Check if an adapter is enabled via policy.

        Enforcement: Default is False (opt-in). Adapters must be explicitly enabled
        in policy to prevent accidental usage and enforce policy gating.

        Args:
            adapter_name: Adapter name (e.g., "aider", "e2b_sandbox", "neo4j_graph")

        Returns:
            True if adapter is explicitly enabled in policy, False otherwise
        """
        policy = self.get_policy()
        adapters = policy.get("adapters", {})
        # Adapter is enabled ONLY if explicitly set to True (opt-in, default False)
        return adapters.get(adapter_name, {}).get("enabled", False)


def get_policy_provider() -> PolicyProvider:
    """
    Get policy provider instance.

    Returns:
        PolicyProvider singleton
    """
    return PolicyProvider()
