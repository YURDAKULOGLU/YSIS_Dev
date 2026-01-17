"""
Graceful Shutdown Manager - Handles clean process termination.

Ensures all resources are properly released on shutdown.
"""

import atexit
import logging
import signal
import sys
import threading
from typing import Callable

logger = logging.getLogger(__name__)

_shutdown_handlers: list[tuple[int, str, Callable]] = []
_is_shutting_down = threading.Event()
_shutdown_lock = threading.Lock()


def is_shutting_down() -> bool:
    """Check if shutdown is in progress."""
    return _is_shutting_down.is_set()


def register_shutdown_handler(
    handler: Callable,
    name: str = "",
    priority: int = 50,
):
    """
    Register a shutdown handler.

    Args:
        handler: Function to call on shutdown (no arguments)
        name: Handler name for logging
        priority: Lower = earlier execution (0-100)

    Example:
        def cleanup_db():
            db.close()
        register_shutdown_handler(cleanup_db, "database", priority=90)
    """
    with _shutdown_lock:
        _shutdown_handlers.append((priority, name or handler.__name__, handler))
        _shutdown_handlers.sort(key=lambda x: x[0])
    logger.debug(f"Registered shutdown handler: {name} (priority={priority})")


def unregister_shutdown_handler(handler: Callable):
    """Remove a shutdown handler."""
    with _shutdown_lock:
        _shutdown_handlers[:] = [
            (p, n, h) for p, n, h in _shutdown_handlers if h != handler
        ]


def _run_shutdown_handlers():
    """Execute all shutdown handlers."""
    if _is_shutting_down.is_set():
        return  # Already shutting down

    _is_shutting_down.set()
    logger.info("Graceful shutdown initiated...")

    # Journal event
    try:
        from ..constants import PROJECT_ROOT
        from ..syscalls.journal import append_event
        append_event(
            PROJECT_ROOT / "platform_data",
            "GRACEFUL_SHUTDOWN_START",
            {"handlers_count": len(_shutdown_handlers)},
        )
    except Exception:
        pass

    errors = []
    for priority, name, handler in _shutdown_handlers:
        try:
            logger.debug(f"Running shutdown handler: {name}")
            handler()
            logger.debug(f"Shutdown handler completed: {name}")
        except Exception as e:
            logger.error(f"Shutdown handler '{name}' failed: {e}")
            errors.append((name, str(e)))

    # Journal completion
    try:
        from ..constants import PROJECT_ROOT
        from ..syscalls.journal import append_event
        append_event(
            PROJECT_ROOT / "platform_data",
            "GRACEFUL_SHUTDOWN_COMPLETE",
            {
                "handlers_run": len(_shutdown_handlers),
                "errors": errors,
            },
        )
    except Exception:
        pass

    logger.info(f"Graceful shutdown complete ({len(errors)} errors)")


def _signal_handler(signum, frame):
    """Handle termination signals."""
    sig_name = signal.Signals(signum).name
    logger.info(f"Received signal {sig_name}")
    _run_shutdown_handlers()
    sys.exit(0)


def setup_signal_handlers():
    """Setup signal handlers for graceful shutdown."""
    # Handle SIGTERM (docker stop, kill)
    signal.signal(signal.SIGTERM, _signal_handler)

    # Handle SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, _signal_handler)

    # Handle atexit (normal exit)
    atexit.register(_run_shutdown_handlers)

    logger.info("Signal handlers configured for graceful shutdown")


# Context manager for shutdown-aware operations
class ShutdownAware:
    """Context manager that checks for shutdown."""

    def __init__(self, operation_name: str = "operation"):
        self.operation_name = operation_name

    def __enter__(self):
        if is_shutting_down():
            raise RuntimeError(f"Cannot start {self.operation_name}: shutdown in progress")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


def shutdown_aware(func: Callable) -> Callable:
    """Decorator to make function shutdown-aware."""
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_shutting_down():
            raise RuntimeError(f"Cannot run {func.__name__}: shutdown in progress")
        return func(*args, **kwargs)

    return wrapper

