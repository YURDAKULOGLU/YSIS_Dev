"""
Rate Limiter Service - Prevents API overload.

Uses token bucket algorithm for rate limiting.
"""

import logging
import threading
import time
from functools import wraps
from typing import Callable

logger = logging.getLogger(__name__)


class TokenBucket:
    """Token bucket rate limiter."""

    def __init__(self, rate: float, capacity: int):
        """
        Args:
            rate: Tokens per second to add
            capacity: Maximum tokens in bucket
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.monotonic()
        self._lock = threading.Lock()

    def acquire(self, tokens: int = 1, block: bool = True) -> bool:
        """
        Acquire tokens from bucket.

        Args:
            tokens: Number of tokens to acquire
            block: If True, wait for tokens; if False, return immediately

        Returns:
            True if tokens acquired, False otherwise
        """
        with self._lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
            self.last_update = now

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True

            if not block:
                return False

            # Calculate wait time
            wait_time = (tokens - self.tokens) / self.rate

        # Wait outside lock
        logger.debug(f"Rate limit: waiting {wait_time:.2f}s")
        time.sleep(wait_time)

        with self._lock:
            self.tokens = 0
            self.last_update = time.monotonic()

        return True


# Rate limiters for different services
_limiters: dict[str, TokenBucket] = {}


def get_limiter(name: str, rate: float = 10.0, capacity: int = 10) -> TokenBucket:
    """
    Get or create a rate limiter.

    Args:
        name: Limiter identifier
        rate: Requests per second
        capacity: Burst capacity

    Returns:
        TokenBucket instance
    """
    if name not in _limiters:
        _limiters[name] = TokenBucket(rate, capacity)
        logger.info(f"Created rate limiter '{name}': {rate}/s, burst={capacity}")
    return _limiters[name]


def rate_limited(
    limiter_name: str,
    rate: float = 10.0,
    capacity: int = 10,
    tokens: int = 1,
):
    """
    Decorator to rate limit function calls.

    Args:
        limiter_name: Name of the rate limiter
        rate: Requests per second
        capacity: Burst capacity
        tokens: Tokens per call

    Example:
        @rate_limited("ollama", rate=5.0, capacity=10)
        def call_ollama(prompt):
            ...
    """
    def decorator(func: Callable) -> Callable:
        limiter = get_limiter(limiter_name, rate, capacity)

        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.monotonic()
            limiter.acquire(tokens)
            wait_time = time.monotonic() - start

            if wait_time > 0.1:
                logger.debug(f"Rate limit '{limiter_name}': waited {wait_time:.2f}s")
                # Journal event for significant waits
                try:
                    from ..constants import PROJECT_ROOT
                    from ..syscalls.journal import append_event
                    append_event(
                        PROJECT_ROOT / "platform_data",
                        "RATE_LIMIT_WAIT",
                        {
                            "limiter": limiter_name,
                            "wait_seconds": round(wait_time, 3),
                        },
                    )
                except Exception:
                    pass

            return func(*args, **kwargs)

        return wrapper
    return decorator


def get_limiter_status(name: str) -> dict:
    """Get status of a rate limiter."""
    if name not in _limiters:
        return {"exists": False}

    limiter = _limiters[name]
    return {
        "exists": True,
        "name": name,
        "rate": limiter.rate,
        "capacity": limiter.capacity,
        "current_tokens": round(limiter.tokens, 2),
    }

