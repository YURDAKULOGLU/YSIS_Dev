"""
Observability Service - Unified interface for metrics, logs, and tracing.

Uses adapter pattern to support multiple observability backends.
"""

import logging
from typing import Any

from ..adapters.registry import get_registry
from ..services.policy import get_policy_provider

logger = logging.getLogger(__name__)


class ObservabilityService:
    """
    Unified observability service.

    Supports multiple backends via adapters:
    - Langfuse (tracing, metrics)
    - OpenTelemetry (distributed tracing)
    - Future: Prometheus, Datadog, etc.
    """

    def __init__(self):
        """Initialize observability service."""
        self._adapters = []
        self._init_adapters()

    def _init_adapters(self) -> None:
        """Initialize observability adapters based on policy."""
        registry = get_registry()
        policy = get_policy_provider()

        # Try Langfuse adapter
        if policy.is_adapter_enabled("langfuse_observability"):
            adapter = registry.get("langfuse_observability", adapter_type="observability")
            if adapter and adapter.is_available():
                self._adapters.append(adapter)

        # Try OpenTelemetry adapter
        if policy.is_adapter_enabled("opentelemetry_observability"):
            adapter = registry.get("opentelemetry_observability", adapter_type="observability")
            if adapter and adapter.is_available():
                self._adapters.append(adapter)

    def trace_generation(
        self,
        name: str,
        model: str,
        input_data: Any,
        output_data: Any,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Trace an LLM generation call.

        Args:
            name: Trace name
            model: Model identifier
            input_data: Input data
            output_data: Output data
            metadata: Optional metadata
        """
        for adapter in self._adapters:
            if hasattr(adapter, "trace_generation"):
                try:
                    adapter.trace_generation(name, model, input_data, output_data, metadata)
                except Exception:
                    pass  # Graceful degradation

    def start_span(
        self,
        name: str,
        attributes: dict[str, Any] | None = None,
        trace_id: str | None = None,
    ) -> Any:
        """
        Start a trace span.

        Args:
            name: Span name
            attributes: Optional span attributes
            trace_id: Optional trace ID for correlation

        Returns:
            Span context manager (from first available adapter)
        """
        for adapter in self._adapters:
            if hasattr(adapter, "start_span"):
                try:
                    return adapter.start_span(name, attributes, trace_id)
                except Exception:
                    continue

        # No-op context manager if no adapters
        from contextlib import nullcontext

        return nullcontext()

    def flush(self) -> None:
        """Flush pending traces."""
        for adapter in self._adapters:
            if hasattr(adapter, "flush"):
                try:
                    adapter.flush()
                except Exception:
                    pass  # Graceful degradation


# Global service instance
_observability_service: ObservabilityService | None = None


def get_observability_service() -> ObservabilityService:
    """Get global observability service instance."""
    global _observability_service
    if _observability_service is None:
        _observability_service = ObservabilityService()
    return _observability_service


