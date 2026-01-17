"""
Executor Registry - Unified interface for executor selection.

Provides policy-driven executor selection with adapter pattern.
"""

import logging

from ..adapters.registry import get_registry

logger = logging.getLogger(__name__)
from ..contracts import ExecutorProtocol
from ..services.policy import get_policy_provider


class ExecutorRegistry:
    """
    Executor Registry - Unified interface for executor selection.

    Uses adapter registry under the hood but provides executor-specific interface.
    """

    def __init__(self):
        """Initialize executor registry."""
        self._adapter_registry = get_registry()
        self._policy = get_policy_provider()

    def get_executor(self, executor_name: str | None = None) -> ExecutorProtocol | None:
        """
        Get executor by name or from policy.

        Args:
            executor_name: Optional executor name (if None, uses policy default)

        Returns:
            Executor instance or None if not available
        """
        # Require explicit executor name (workflow-configured)
        if executor_name is None:
            logger.warning("Executor name not provided; workflow must set node.config.executor")
            return None

        # Check if executor is enabled
        if not self._policy.is_adapter_enabled(executor_name):
            return None

        # Get executor from adapter registry
        executor_instance = self._adapter_registry.get(
            executor_name, adapter_type="executor"
        )
        if executor_instance is None:
            return None
        return executor_instance

    def list_executors(self) -> list[dict]:
        """
        List all available executors.

        Returns:
            List of executor info dicts
        """
        executors = []

        # Get all executor adapters from registry
        all_adapters = self._adapter_registry.list_adapters(adapter_type="executor")

        for adapter_info in all_adapters:
            executor_name = adapter_info["name"]
            enabled = self._policy.is_adapter_enabled(executor_name)

            executors.append(
                {
                    "name": executor_name,
                    "enabled": enabled,
                    "available": adapter_info.get("available", False),
                }
            )

        return executors


# Global executor registry instance
_executor_registry: ExecutorRegistry | None = None


def get_executor_registry() -> ExecutorRegistry:
    """Get global executor registry instance."""
    global _executor_registry
    if _executor_registry is None:
        _executor_registry = ExecutorRegistry()
    return _executor_registry

