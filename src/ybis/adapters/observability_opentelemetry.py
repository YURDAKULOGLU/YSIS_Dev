"""
OpenTelemetry Observability Adapter - Distributed tracing via OpenTelemetry.

Provides OpenTelemetry-based tracing for distributed systems.
"""

import logging
import os
from typing import Any

from ..adapters.registry import AdapterProtocol

logger = logging.getLogger(__name__)


class OpenTelemetryObservabilityAdapter(AdapterProtocol):
    """OpenTelemetry-based observability adapter."""

    def __init__(self):
        """Initialize OpenTelemetry adapter."""
        self._tracer = None
        self._available = False
        self._init_tracer()

    def _init_tracer(self) -> None:
        """Initialize OpenTelemetry tracer."""
        try:
            from opentelemetry import trace
            from opentelemetry.sdk.resources import Resource
            from opentelemetry.sdk.trace import TracerProvider
            from opentelemetry.sdk.trace.export import BatchSpanProcessor

            service_name = os.getenv("OTEL_SERVICE_NAME", "ybis")
            resource = Resource.create({"service.name": service_name})
            provider = TracerProvider(resource=resource)

            # Add exporters based on environment
            exporter_type = os.getenv("OTEL_EXPORTER", "console")

            if exporter_type == "otlp":
                from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

                endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
                exporter = OTLPSpanExporter(endpoint=endpoint)
                provider.add_span_processor(BatchSpanProcessor(exporter))
            elif exporter_type == "jaeger":
                from opentelemetry.exporter.jaeger.thrift import JaegerExporter

                endpoint = os.getenv("JAEGER_ENDPOINT", "http://localhost:14268/api/traces")
                exporter = JaegerExporter(agent_host_name=endpoint)
                provider.add_span_processor(BatchSpanProcessor(exporter))
            else:
                # Console exporter (default)
                from opentelemetry.sdk.trace.export import ConsoleSpanExporter

                exporter = ConsoleSpanExporter()
                provider.add_span_processor(BatchSpanProcessor(exporter))

            trace.set_tracer_provider(provider)
            self._tracer = trace.get_tracer(service_name)
            self._available = True
        except ImportError:
            self._available = False
        except Exception:
            self._available = False

    def is_available(self) -> bool:
        """Check if OpenTelemetry is available."""
        return self._available

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
            Span context manager
        """
        if not self._available or not self._tracer:
            from contextlib import nullcontext

            return nullcontext()

        try:
            span = self._tracer.start_as_current_span(name)
            if attributes:
                for key, value in attributes.items():
                    span.set_attribute(key, str(value))
            return span
        except Exception:
            from contextlib import nullcontext

            return nullcontext()


