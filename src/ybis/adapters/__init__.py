"""
Adapter package - External tool integrations.

All adapters must be registered via the adapter registry.
Core modules should use registry.get() instead of direct imports.
"""

from .registry import AdapterRegistry, get_registry, set_registry

__all__ = ["AdapterRegistry", "get_registry", "set_registry"]
