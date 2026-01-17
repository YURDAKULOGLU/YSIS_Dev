"""
Metrics tracking for Optimization Trinity features.
Tracks cost, latency, cache hits, and parse errors.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class OptimizationMetrics:
    """Track metrics for Optimization Trinity features"""

    # Cost tracking
    total_cost: float = 0.0
    total_requests: int = 0

    # Cache tracking (Claude only)
    cache_hits: int = 0
    cache_misses: int = 0

    # Parse error tracking
    parse_errors: int = 0
    successful_parses: int = 0

    # Provider tracking
    requests_by_provider: Dict[str, int] = field(default_factory=dict)

    # Latency tracking
    total_latency_ms: float = 0.0
    min_latency_ms: Optional[float] = None
    max_latency_ms: Optional[float] = None

    # Feature usage
    caching_enabled_requests: int = 0
    structured_output_requests: int = 0
    extended_thinking_requests: int = 0

    def record_request(
        self,
        provider: str,
        cost: float,
        latency_ms: float,
        cached: bool = False,
        parse_success: bool = True,
        used_caching: bool = False,
        used_structured: bool = False,
        used_thinking: bool = False
    ):
        """Record a single request's metrics"""
        self.total_requests += 1
        self.total_cost += cost
        self.total_latency_ms += latency_ms

        # Update latency bounds
        if self.min_latency_ms is None or latency_ms < self.min_latency_ms:
            self.min_latency_ms = latency_ms
        if self.max_latency_ms is None or latency_ms > self.max_latency_ms:
            self.max_latency_ms = latency_ms

        # Track provider
        self.requests_by_provider[provider] = self.requests_by_provider.get(provider, 0) + 1

        # Track caching
        if cached:
            self.cache_hits += 1
        elif used_caching:
            self.cache_misses += 1

        # Track parse errors
        if parse_success:
            self.successful_parses += 1
        else:
            self.parse_errors += 1

        # Track feature usage
        if used_caching:
            self.caching_enabled_requests += 1
        if used_structured:
            self.structured_output_requests += 1
        if used_thinking:
            self.extended_thinking_requests += 1

    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate (0-1)"""
        total = self.cache_hits + self.cache_misses
        if total == 0:
            return 0.0
        return self.cache_hits / total

    @property
    def parse_error_rate(self) -> float:
        """Calculate parse error rate (0-1)"""
        total = self.successful_parses + self.parse_errors
        if total == 0:
            return 0.0
        return self.parse_errors / total

    @property
    def average_latency_ms(self) -> float:
        """Calculate average latency"""
        if self.total_requests == 0:
            return 0.0
        return self.total_latency_ms / self.total_requests

    @property
    def average_cost(self) -> float:
        """Calculate average cost per request"""
        if self.total_requests == 0:
            return 0.0
        return self.total_cost / self.total_requests

    def calculate_cost_savings(self) -> Dict[str, Any]:
        """Calculate cost savings from caching"""
        if self.cache_hits == 0:
            return {
                "savings_percent": 0.0,
                "estimated_savings": 0.0,
                "actual_cost": self.total_cost,
                "cost_without_caching": self.total_cost
            }

        # Assume 90% cost reduction for cached requests
        cache_savings_rate = 0.90
        cost_per_uncached = self.total_cost / (self.cache_misses + (self.cache_hits * (1 - cache_savings_rate)))

        cost_without_caching = cost_per_uncached * (self.cache_hits + self.cache_misses)
        estimated_savings = cost_without_caching - self.total_cost
        savings_percent = (estimated_savings / cost_without_caching) * 100 if cost_without_caching > 0 else 0

        return {
            "savings_percent": savings_percent,
            "estimated_savings": estimated_savings,
            "actual_cost": self.total_cost,
            "cost_without_caching": cost_without_caching
        }

    def report(self) -> Dict[str, Any]:
        """Generate comprehensive metrics report"""
        cost_savings = self.calculate_cost_savings()

        return {
            "summary": {
                "total_requests": self.total_requests,
                "total_cost": f"${self.total_cost:.4f}",
                "average_cost": f"${self.average_cost:.4f}",
                "average_latency_ms": f"{self.average_latency_ms:.2f}",
            },
            "caching": {
                "cache_hits": self.cache_hits,
                "cache_misses": self.cache_misses,
                "hit_rate": f"{self.cache_hit_rate * 100:.1f}%",
                "savings_percent": f"{cost_savings['savings_percent']:.1f}%",
                "estimated_savings": f"${cost_savings['estimated_savings']:.4f}",
            },
            "quality": {
                "successful_parses": self.successful_parses,
                "parse_errors": self.parse_errors,
                "error_rate": f"{self.parse_error_rate * 100:.2f}%",
            },
            "providers": self.requests_by_provider,
            "latency": {
                "average_ms": f"{self.average_latency_ms:.2f}",
                "min_ms": f"{self.min_latency_ms:.2f}" if self.min_latency_ms else "N/A",
                "max_ms": f"{self.max_latency_ms:.2f}" if self.max_latency_ms else "N/A",
            },
            "features": {
                "caching_enabled": self.caching_enabled_requests,
                "structured_output": self.structured_output_requests,
                "extended_thinking": self.extended_thinking_requests,
            }
        }

    def to_json(self) -> str:
        """Export metrics as JSON"""
        return json.dumps(self.report(), indent=2)

    def __str__(self) -> str:
        """String representation for logging"""
        report = self.report()
        lines = [
            "\n=== Optimization Trinity Metrics ===",
            f"Total Requests: {self.total_requests}",
            f"Total Cost: {report['summary']['total_cost']}",
            f"Average Cost: {report['summary']['average_cost']}",
            f"Average Latency: {report['summary']['average_latency_ms']}",
            "",
            "Caching:",
            f"  Hit Rate: {report['caching']['hit_rate']}",
            f"  Cost Savings: {report['caching']['savings_percent']} (${report['caching']['estimated_savings']})",
            "",
            "Quality:",
            f"  Parse Error Rate: {report['quality']['error_rate']}",
            "",
            "Providers:",
        ]

        for provider, count in report['providers'].items():
            lines.append(f"  {provider}: {count}")

        lines.append("=" * 35)
        return "\n".join(lines)


# Global metrics instance
_global_metrics: Optional[OptimizationMetrics] = None


def get_metrics() -> OptimizationMetrics:
    """Get global metrics instance"""
    global _global_metrics
    if _global_metrics is None:
        _global_metrics = OptimizationMetrics()
    return _global_metrics


def reset_metrics():
    """Reset global metrics"""
    global _global_metrics
    _global_metrics = OptimizationMetrics()
