"""
Adapter Registry - Policy-driven adapter selection and registration.

This module provides a registry for adapters, allowing policy-based selection
and graceful fallback when adapters are disabled or unavailable.

Core principle: Core modules never directly instantiate adapters. They use
the registry to get adapters based on policy configuration.
"""

import logging
from pathlib import Path
from typing import Any, Protocol, TypeVar

logger = logging.getLogger(__name__)

from ..services.policy import PolicyProvider
from ..syscalls.journal import append_event

T = TypeVar("T")


class AdapterProtocol(Protocol):
    """Protocol that all adapters must implement."""

    def is_available(self) -> bool:
        """Check if adapter is available (dependencies installed, services running)."""
        ...


class AdapterRegistry:
    """
    Registry for adapters with policy-driven selection.

    Adapters are registered by name and can be enabled/disabled via policy.
    The registry provides a single point of access for adapters, ensuring
    that core modules never directly instantiate adapters.
    """

    def __init__(self, policy_provider: PolicyProvider | None = None, run_path: Path | None = None, trace_id: str | None = None):
        """
        Initialize adapter registry.

        Args:
            policy_provider: Policy provider for checking adapter enablement
            run_path: Optional run path for journal logging
            trace_id: Optional trace ID for journal logging
        """
        self._adapters: dict[str, dict[str, Any]] = {}
        self._policy_provider = policy_provider
        self._availability_cache: dict[str, tuple[bool, float]] = {}
        self._cache_ttl: float = 300.0  # 5 minutes
        self.run_path = run_path
        self.trace_id = trace_id

    def register(
        self,
        name: str,
        adapter_class: type[T],
        adapter_type: str,
        default_enabled: bool = False,
        required_dependencies: list[str] | None = None,
    ) -> None:
        """
        Register an adapter.

        Args:
            name: Adapter name (e.g., "aider", "e2b_sandbox", "neo4j_graph")
            adapter_class: Adapter class
            adapter_type: Adapter type (e.g., "executor", "sandbox", "graph_store")
            default_enabled: Whether adapter is enabled by default
            required_dependencies: List of required dependency names (for availability checks)
        """
        self._adapters[name] = {
            "class": adapter_class,
            "type": adapter_type,
            "default_enabled": default_enabled,
            "required_dependencies": required_dependencies or [],
        }

        # Journal: Adapter registered
        if self.run_path:
            append_event(
                self.run_path,
                "ADAPTER_REGISTER",
                {
                    "name": name,
                    "type": adapter_type,
                },
                trace_id=self.trace_id,
            )

    def get(
        self,
        name: str,
        adapter_type: str | None = None,
        fallback_to_default: bool = True,
    ) -> Any | None:
        """
        Get an adapter instance by name.

        Args:
            name: Adapter name
            adapter_type: Optional adapter type filter
            fallback_to_default: If True, return default adapter if requested one is disabled

        Returns:
            Adapter instance or None if not available
        """
        if name not in self._adapters:
            return None

        adapter_info = self._adapters[name]

        # Check adapter type filter
        if adapter_type and adapter_info["type"] != adapter_type:
            return None

        # Check if adapter is enabled via policy
        if self._policy_provider:
            enabled = self._policy_provider.is_adapter_enabled(name)
            if not enabled:
                if fallback_to_default:
                    # Try to find a default adapter of the same type
                    return self._get_default_adapter(adapter_type)
                return None

        # Check if adapter is available
        adapter_class = adapter_info["class"]
        try:
            instance = adapter_class()
            if hasattr(instance, "is_available"):
                if not instance.is_available():
                    if fallback_to_default:
                        return self._get_default_adapter(adapter_type)
                    return None

            # Journal: Adapter retrieved
            if self.run_path:
                append_event(
                    self.run_path,
                    "ADAPTER_GET",
                    {
                        "name": name,
                        "type": adapter_info["type"],
                    },
                    trace_id=self.trace_id,
                )

            return instance
        except Exception:
            # Adapter instantiation failed
            if fallback_to_default:
                return self._get_default_adapter(adapter_type)
            return None

    def _get_default_adapter(self, adapter_type: str | None) -> Any | None:
        """Get default adapter for a type."""
        if not adapter_type:
            return None

        # Find first enabled adapter of the same type
        for name, info in self._adapters.items():
            if info["type"] == adapter_type:
                if self._policy_provider:
                    if not self._policy_provider.is_adapter_enabled(name):
                        continue
                try:
                    instance = info["class"]()
                    if hasattr(instance, "is_available"):
                        if instance.is_available():
                            return instance
                    else:
                        return instance
                except Exception:
                    continue

        return None

    def list_adapters(self, adapter_type: str | None = None) -> list[dict[str, Any]]:
        """
        List all registered adapters.

        Args:
            adapter_type: Optional filter by adapter type

        Returns:
            List of adapter info dictionaries
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed
        from concurrent.futures import TimeoutError as FutureTimeoutError

        # Filter adapters first
        filtered_adapters = []
        for name, info in self._adapters.items():
            if adapter_type and info["type"] != adapter_type:
                continue
            filtered_adapters.append((name, info))

        # Check availability in parallel (much faster!)
        import time as time_module
        current_time = time_module.time()

        def check_adapter_availability(name_info_pair):
            name, info = name_info_pair
            enabled = True
            available = False

            if self._policy_provider:
                enabled = self._policy_provider.is_adapter_enabled(name)

            # Check cache first
            if name in self._availability_cache:
                cached_available, cache_time = self._availability_cache[name]
                if current_time - cache_time < self._cache_ttl:
                    available = cached_available
                else:
                    # Cache expired, remove it
                    del self._availability_cache[name]

            # If not in cache, check availability (with timeout to prevent hanging)
            if name not in self._availability_cache:
                try:
                    def check_availability():
                        instance = info["class"]()
                        if hasattr(instance, "is_available"):
                            return instance.is_available()
                        return True

                    # Use ThreadPoolExecutor with timeout (works on Windows and Unix)
                    with ThreadPoolExecutor(max_workers=1) as executor:
                        future = executor.submit(check_availability)
                        try:
                            available = future.result(timeout=0.5)  # 0.5 second timeout (faster!)
                            # Cache the result
                            self._availability_cache[name] = (available, current_time)
                        except FutureTimeoutError:
                            available = False
                            # Cache negative result too
                            self._availability_cache[name] = (False, current_time)
                except Exception:
                    available = False
                    self._availability_cache[name] = (False, current_time)

            return {
                "name": name,
                "type": info["type"],
                "enabled": enabled,
                "available": available,
                "default_enabled": info["default_enabled"],
            }

        # Check all adapters in parallel (max 10 workers to avoid overwhelming)
        adapters = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(check_adapter_availability, pair): pair for pair in filtered_adapters}
            for future in as_completed(futures):
                try:
                    adapter_info = future.result()
                    adapters.append(adapter_info)
                except Exception:
                    # If check fails, add adapter with available=False
                    name, info = futures[future]
                    adapters.append({
                        "name": name,
                        "type": info["type"],
                        "enabled": self._policy_provider.is_adapter_enabled(name) if self._policy_provider else True,
                        "available": False,
                        "default_enabled": info["default_enabled"],
                    })

        return adapters

    def is_enabled(self, name: str) -> bool:
        """Check if an adapter is enabled via policy."""
        if name not in self._adapters:
            return False

        if self._policy_provider:
            return self._policy_provider.is_adapter_enabled(name)

        return self._adapters[name]["default_enabled"]


# Global registry instance (initialized by services)
_global_registry: AdapterRegistry | None = None


def get_registry() -> AdapterRegistry:
    """Get the global adapter registry."""
    global _global_registry
    if _global_registry is None:
        from ..services.policy import get_policy_provider

        _global_registry = AdapterRegistry(policy_provider=get_policy_provider())
    return _global_registry


def set_registry(registry: AdapterRegistry) -> None:
    """Set the global adapter registry (for testing)."""
    global _global_registry
    _global_registry = registry

