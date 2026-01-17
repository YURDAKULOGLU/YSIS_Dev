"""
Langfuse Observability Adapter - Tracing and metrics via Langfuse.

Provides LLM call tracing, workflow observability, and metrics collection.
"""

import logging
import os
from typing import Any

from ..adapters.registry import AdapterProtocol

logger = logging.getLogger(__name__)


class LangfuseObservabilityAdapter(AdapterProtocol):
    """Langfuse-based observability adapter."""

    def __init__(self):
        """Initialize Langfuse adapter."""
        self._client = None
        self._available = False
        self._init_client()

    def _init_client(self) -> None:
        """Initialize Langfuse client."""
        try:
            from langfuse import Langfuse
            from langfuse.decorators import langfuse_context, observe

            public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
            secret_key = os.getenv("LANGFUSE_SECRET_KEY")
            host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

            if public_key and secret_key:
                self._client = Langfuse(
                    public_key=public_key,
                    secret_key=secret_key,
                    host=host,
                )
                self._available = True
            else:
                self._available = False
        except ImportError:
            self._available = False
        except Exception:
            self._available = False

    def is_available(self) -> bool:
        """Check if Langfuse is available."""
        return self._available

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
        if not self._available or not self._client:
            return

        try:
            self._client.generation(
                name=name,
                model=model,
                input=input_data,
                output=output_data,
                metadata=metadata or {},
            )
        except Exception:
            pass  # Graceful degradation

    def trace_span(
        self,
        name: str,
        metadata: dict[str, Any] | None = None,
        trace_id: str | None = None,
    ) -> Any:
        """
        Create a trace span.

        Args:
            name: Span name
            metadata: Optional metadata
            trace_id: Optional trace ID for correlation

        Returns:
            Context manager for span
        """
        if not self._available or not self._client:
            # Return no-op context manager
            from contextlib import nullcontext

            return nullcontext()

        try:
            from langfuse.decorators import langfuse_context

            if trace_id:
                langfuse_context.update_current_trace(id=trace_id)

            return self._client.trace(name=name, metadata=metadata or {})
        except Exception:
            from contextlib import nullcontext

            return nullcontext()

    def flush(self) -> None:
        """Flush pending traces."""
        if self._available and self._client:
            try:
                self._client.flush()
            except Exception:
                pass  # Graceful degradation


