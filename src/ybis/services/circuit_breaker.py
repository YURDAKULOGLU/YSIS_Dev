"""
Circuit Breaker Service - Prevents cascade failures.

Uses pybreaker for circuit breaker pattern implementation.
"""

import logging
from functools import wraps
from typing import Any, Callable

logger = logging.getLogger(__name__)

# Try to import pybreaker, fallback to simple implementation if not available
try:
    import pybreaker
    PYBREAKER_AVAILABLE = True
except ImportError:
    PYBREAKER_AVAILABLE = False
    logger.warning("pybreaker not installed. Circuit breaker will use simple fallback.")

# Circuit breaker instances for different services
_breakers: dict[str, Any] = {}


class CircuitBreakerListener:
    """Listener for circuit breaker state changes."""

    def __init__(self, name: str):
        self.name = name

    def state_change(self, cb: Any, old_state: str, new_state: str):
        logger.warning(f"Circuit breaker '{self.name}': {old_state} -> {new_state}")

        # Journal event
        try:
            from ..constants import PROJECT_ROOT
            from ..syscalls.journal import append_event
            append_event(
                PROJECT_ROOT / "platform_data",
                "CIRCUIT_BREAKER_STATE_CHANGE",
                {
                    "breaker": self.name,
                    "old_state": str(old_state),
                    "new_state": str(new_state),
                },
            )
        except Exception:
            pass

    def failure(self, cb: Any, exc: Exception):
        logger.debug(f"Circuit breaker '{self.name}' recorded failure: {exc}")

    def success(self, cb: Any):
        pass


def get_breaker(
    name: str,
    fail_max: int = 5,
    reset_timeout: int = 60,
) -> Any:
    """
    Get or create a circuit breaker.

    Args:
        name: Breaker identifier (e.g., "ollama", "neo4j")
        fail_max: Number of failures before opening circuit
        reset_timeout: Seconds before attempting to close circuit

    Returns:
        CircuitBreaker instance
    """
    if name not in _breakers:
        if PYBREAKER_AVAILABLE:
            _breakers[name] = pybreaker.CircuitBreaker(
                fail_max=fail_max,
                reset_timeout=reset_timeout,
                listeners=[CircuitBreakerListener(name)],
                name=name,
            )
        else:
            # Simple fallback implementation
            from .circuit_breaker_simple import SimpleCircuitBreaker
            _breakers[name] = SimpleCircuitBreaker(
                name=name,
                fail_max=fail_max,
                reset_timeout=reset_timeout,
            )
    return _breakers[name]


def circuit_protected(
    breaker_name: str,
    fail_max: int = 5,
    reset_timeout: int = 60,
    fallback: Callable[..., Any] | None = None,
):
    """
    Decorator to protect function with circuit breaker.

    Args:
        breaker_name: Name of the circuit breaker
        fail_max: Max failures before opening
        reset_timeout: Seconds before retry
        fallback: Optional fallback function when circuit is open

    Example:
        @circuit_protected("ollama", fallback=lambda *a, **k: None)
        def call_ollama(prompt):
            ...
    """
    def decorator(func: Callable) -> Callable:
        breaker = get_breaker(breaker_name, fail_max, reset_timeout)

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if PYBREAKER_AVAILABLE:
                    return breaker.call(func, *args, **kwargs)
                else:
                    # Simple fallback
                    return breaker.call(func, *args, **kwargs)
            except Exception as e:
                if PYBREAKER_AVAILABLE and isinstance(e, pybreaker.CircuitBreakerError):
                    logger.warning(f"Circuit '{breaker_name}' is OPEN, using fallback")
                    if fallback:
                        return fallback(*args, **kwargs)
                    raise
                elif not PYBREAKER_AVAILABLE and hasattr(breaker, 'is_open') and breaker.is_open():
                    logger.warning(f"Circuit '{breaker_name}' is OPEN, using fallback")
                    if fallback:
                        return fallback(*args, **kwargs)
                    raise
                else:
                    # Re-raise non-circuit-breaker errors
                    raise

        return wrapper
    return decorator


def get_breaker_status(name: str) -> dict[str, Any]:
    """Get status of a circuit breaker."""
    if name not in _breakers:
        return {"exists": False}

    breaker = _breakers[name]
    if PYBREAKER_AVAILABLE:
        return {
            "exists": True,
            "name": name,
            "state": str(breaker.current_state),
            "fail_counter": breaker.fail_counter,
            "fail_max": breaker.fail_max,
            "reset_timeout": breaker.reset_timeout,
        }
    else:
        return {
            "exists": True,
            "name": name,
            "state": breaker.get_state(),
            "fail_counter": breaker.fail_counter,
            "fail_max": breaker.fail_max,
            "reset_timeout": breaker.reset_timeout,
        }


def get_all_breaker_status() -> dict[str, dict]:
    """Get status of all circuit breakers."""
    return {name: get_breaker_status(name) for name in _breakers}


def reset_breaker(name: str) -> bool:
    """Manually reset a circuit breaker."""
    if name in _breakers:
        breaker = _breakers[name]
        if PYBREAKER_AVAILABLE:
            breaker.close()
        else:
            breaker.reset()
        logger.info(f"Circuit breaker '{name}' manually reset")
        return True
    return False

