"""
Resilience Service - Retry logic using tenacity library.

Provides standard retry decorators with exponential backoff for resilient operations.
Also provides unified resilient decorator combining retry, circuit breaker, and rate limiting.
"""

import logging
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")


def retry_with_backoff(
    func: Callable[..., T] | None = None,
    max_attempts: int = 3,
    multiplier: float = 1.0,
    min_wait: float = 2.0,
    max_wait: float = 10.0,
) -> Callable[..., T] | Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Retry decorator with exponential backoff using tenacity.

    Args:
        func: Function to decorate (if used as decorator)
        max_attempts: Maximum number of retry attempts (default: 3)
        multiplier: Exponential multiplier (default: 1.0)
        min_wait: Minimum wait time in seconds (default: 2.0)
        max_wait: Maximum wait time in seconds (default: 10.0)

    Returns:
        Decorated function with retry logic

    Example:
        @retry_with_backoff(max_attempts=3)
        def call_ollama():
            ...
    """
    if func is None:
        # Used as decorator with parameters
        def decorator(f: Callable[..., T]) -> Callable[..., T]:
            @wraps(f)
            @retry(
                stop=stop_after_attempt(max_attempts),
                wait=wait_exponential(multiplier=multiplier, min=min_wait, max=max_wait),
            )
            def wrapper(*args: Any, **kwargs: Any) -> T:
                return f(*args, **kwargs)

            return wrapper

        return decorator
    else:
        # Used as simple decorator without parameters
        @wraps(func)
        @retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=multiplier, min=min_wait, max=max_wait),
        )
        def wrapper(*args: Any, **kwargs: Any) -> T:
            return func(*args, **kwargs)

        return wrapper


# Standard retry decorator for Ollama calls
ollama_retry = retry_with_backoff(max_attempts=3, multiplier=1.0, min_wait=2.0, max_wait=10.0)


def resilient(
    breaker_name: str | None = None,
    rate_limit: tuple[float, int] | None = None,
    retry_max_attempts: int = 3,
    retry_min_wait: float = 2.0,
    retry_max_wait: float = 10.0,
):
    """
    Combined decorator: retry (tenacity) + circuit breaker + rate limiting.

    This replaces the custom retry.py implementation with tenacity-based retry.

    Args:
        breaker_name: Circuit breaker name (None to skip)
        rate_limit: (rate, capacity) tuple (None to skip)
        retry_max_attempts: Maximum retry attempts (default: 3)
        retry_min_wait: Minimum wait time for retry (default: 2.0)
        retry_max_wait: Maximum wait time for retry (default: 10.0)

    Example:
        @resilient(
            breaker_name="ollama",
            rate_limit=(2.0, 5),
            retry_max_attempts=3,
        )
        def call_ollama(prompt):
            ...
    """
    logger.debug(f"Applying resilient decorator: breaker={breaker_name}, rate_limit={rate_limit}, retries={retry_max_attempts}")
    def decorator(func: Callable) -> Callable:
        wrapped = func

        # Apply retry (innermost) - using tenacity
        wrapped = retry_with_backoff(
            max_attempts=retry_max_attempts,
            min_wait=retry_min_wait,
            max_wait=retry_max_wait,
        )(wrapped)

        # Apply circuit breaker
        if breaker_name:
            from .circuit_breaker import circuit_protected
            wrapped = circuit_protected(breaker_name)(wrapped)

        # Apply rate limiting (outermost)
        if rate_limit:
            from .rate_limiter import rate_limited
            rate, capacity = rate_limit
            wrapped = rate_limited(breaker_name or "default", rate, capacity)(wrapped)

        return wrapped

    return decorator
