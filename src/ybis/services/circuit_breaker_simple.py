"""
Simple Circuit Breaker - Fallback when pybreaker is not available.
"""

import logging
import time
from typing import Any, Callable

logger = logging.getLogger(__name__)


class SimpleCircuitBreaker:
    """Simple circuit breaker implementation."""

    def __init__(self, name: str, fail_max: int = 5, reset_timeout: int = 60):
        self.name = name
        self.fail_max = fail_max
        self.reset_timeout = reset_timeout
        self.fail_counter = 0
        self.last_failure_time: float | None = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def get_state(self) -> str:
        """Get current state."""
        if self.state == "OPEN":
            # Check if we should transition to HALF_OPEN
            if self.last_failure_time and (time.time() - self.last_failure_time) >= self.reset_timeout:
                self.state = "HALF_OPEN"
                self.fail_counter = 0
        return self.state

    def is_open(self) -> bool:
        """Check if circuit is open."""
        return self.get_state() == "OPEN"

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Call function through circuit breaker."""
        if self.is_open():
            raise RuntimeError(f"Circuit breaker '{self.name}' is OPEN")

        try:
            result = func(*args, **kwargs)
            # Success - reset counter if in HALF_OPEN
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.fail_counter = 0
            elif self.state == "CLOSED":
                self.fail_counter = 0
            return result
        except Exception as e:
            # Failure
            self.fail_counter += 1
            self.last_failure_time = time.time()

            if self.fail_counter >= self.fail_max:
                self.state = "OPEN"
                logger.warning(f"Circuit breaker '{self.name}' opened after {self.fail_counter} failures")

            raise

    def reset(self):
        """Manually reset circuit breaker."""
        self.state = "CLOSED"
        self.fail_counter = 0
        self.last_failure_time = None

