# RESILIENCE TASK

## Objective
Add production-grade resilience patterns: Circuit Breaker, Rate Limiting, Graceful Shutdown.

## Current State
- **Circuit Breaker:** 0 implementations
- **Rate Limiting:** 0 implementations
- **Graceful Shutdown:** 4 files (minimal)
- **Retry Logic:** 11 files (exists but inconsistent)

---

## 1. CIRCUIT BREAKER

### Purpose
Prevent cascade failures when external services (Ollama, Neo4j, ChromaDB) are down.

### Install Dependency
```bash
pip install pybreaker
```

Add to `requirements.txt`:
```
pybreaker>=1.0.0
```

### Create Circuit Breaker Service

**File:** `src/ybis/services/circuit_breaker.py`

```python
"""
Circuit Breaker Service - Prevents cascade failures.

Uses pybreaker for circuit breaker pattern implementation.
"""

import logging
from functools import wraps
from typing import Any, Callable

import pybreaker

logger = logging.getLogger(__name__)

# Circuit breaker instances for different services
_breakers: dict[str, pybreaker.CircuitBreaker] = {}


class CircuitBreakerListener(pybreaker.CircuitBreakerListener):
    """Listener for circuit breaker state changes."""

    def __init__(self, name: str):
        self.name = name

    def state_change(self, cb: pybreaker.CircuitBreaker, old_state: str, new_state: str):
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

    def failure(self, cb: pybreaker.CircuitBreaker, exc: Exception):
        logger.debug(f"Circuit breaker '{self.name}' recorded failure: {exc}")

    def success(self, cb: pybreaker.CircuitBreaker):
        pass


def get_breaker(
    name: str,
    fail_max: int = 5,
    reset_timeout: int = 60,
) -> pybreaker.CircuitBreaker:
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
        _breakers[name] = pybreaker.CircuitBreaker(
            fail_max=fail_max,
            reset_timeout=reset_timeout,
            listeners=[CircuitBreakerListener(name)],
            name=name,
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
                return breaker.call(func, *args, **kwargs)
            except pybreaker.CircuitBreakerError:
                logger.warning(f"Circuit '{breaker_name}' is OPEN, using fallback")
                if fallback:
                    return fallback(*args, **kwargs)
                raise

        return wrapper
    return decorator


def get_breaker_status(name: str) -> dict[str, Any]:
    """Get status of a circuit breaker."""
    if name not in _breakers:
        return {"exists": False}

    breaker = _breakers[name]
    return {
        "exists": True,
        "name": name,
        "state": str(breaker.current_state),
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
        _breakers[name].close()
        logger.info(f"Circuit breaker '{name}' manually reset")
        return True
    return False
```

### Apply to Adapters

**File:** `src/ybis/adapters/local_coder.py`

```python
# Add at top
from ..services.circuit_breaker import circuit_protected

# Wrap LLM call (around line 234)
@circuit_protected("ollama", fail_max=3, reset_timeout=30)
def _call_llm_with_breaker(model, messages, api_base, timeout):
    import litellm
    return litellm.completion(
        model=model,
        messages=messages,
        api_base=api_base,
        timeout=timeout,
    )

# In _generate_file_content, replace direct call:
# OLD:
# response = _call_llm()
# NEW:
response = _call_llm_with_breaker(
    self.model,
    [{"role": "user", "content": prompt}],
    self.api_base,
    30,
)
```

**File:** `src/ybis/adapters/graph_store_neo4j.py`

```python
from ..services.circuit_breaker import circuit_protected

@circuit_protected("neo4j", fail_max=5, reset_timeout=60)
def execute_query(self, query: str, params: dict = None):
    # existing query code
    ...
```

**File:** `src/ybis/data_plane/vector_store.py`

```python
from ..services.circuit_breaker import circuit_protected

@circuit_protected("chromadb", fail_max=3, reset_timeout=30)
def query(self, collection: str, query: str, top_k: int = 5):
    # existing query code
    ...
```

### Files to Modify

| File | Change |
|------|--------|
| `src/ybis/services/circuit_breaker.py` | CREATE - New service |
| `src/ybis/adapters/local_coder.py` | ADD - `@circuit_protected("ollama")` |
| `src/ybis/adapters/aider.py` | ADD - `@circuit_protected("aider")` |
| `src/ybis/adapters/graph_store_neo4j.py` | ADD - `@circuit_protected("neo4j")` |
| `src/ybis/adapters/llamaindex_adapter.py` | ADD - `@circuit_protected("llamaindex")` |
| `src/ybis/data_plane/vector_store.py` | ADD - `@circuit_protected("chromadb")` |
| `src/ybis/adapters/vector_store_qdrant.py` | ADD - `@circuit_protected("qdrant")` |
| `src/ybis/services/health_monitor.py` | ADD - Breaker status check |
| `requirements.txt` | ADD - `pybreaker>=1.0.0` |

---

## 2. RATE LIMITING

### Purpose
Prevent overwhelming external APIs (Ollama, OpenAI, etc.) with too many requests.

### Install Dependency
```bash
pip install ratelimit
```

Add to `requirements.txt`:
```
ratelimit>=2.2.1
```

### Create Rate Limiter Service

**File:** `src/ybis/services/rate_limiter.py`

```python
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
```

### Apply to LLM Calls

**File:** `src/ybis/adapters/local_coder.py`

```python
from ..services.rate_limiter import rate_limited

# Combine with circuit breaker
@rate_limited("ollama", rate=2.0, capacity=5)  # 2 requests/sec, burst of 5
@circuit_protected("ollama", fail_max=3, reset_timeout=30)
def _call_llm_protected(model, messages, api_base, timeout):
    import litellm
    return litellm.completion(...)
```

**File:** `src/ybis/orchestrator/planner.py`

```python
from ..services.rate_limiter import rate_limited

@rate_limited("planner_llm", rate=1.0, capacity=3)  # 1 req/sec for planning
def _call_planner_llm(self, ...):
    ...
```

### Rate Limit Configuration

**File:** `configs/rate_limits.yaml`

```yaml
# Rate limiting configuration
rate_limits:
  ollama:
    rate: 5.0        # requests per second
    capacity: 10     # burst capacity

  openai:
    rate: 3.0
    capacity: 5

  neo4j:
    rate: 50.0
    capacity: 100

  chromadb:
    rate: 20.0
    capacity: 50

  aider:
    rate: 1.0        # Aider is heavy
    capacity: 2
```

### Files to Modify

| File | Change |
|------|--------|
| `src/ybis/services/rate_limiter.py` | CREATE - New service |
| `src/ybis/adapters/local_coder.py` | ADD - `@rate_limited` decorator |
| `src/ybis/adapters/aider.py` | ADD - `@rate_limited("aider", rate=1.0)` |
| `src/ybis/orchestrator/planner.py` | ADD - `@rate_limited` |
| `configs/rate_limits.yaml` | CREATE - Configuration |
| `requirements.txt` | ADD - `ratelimit>=2.2.1` |

---

## 3. GRACEFUL SHUTDOWN

### Purpose
Clean shutdown of workers, database connections, and running tasks.

### Create Shutdown Manager

**File:** `src/ybis/services/shutdown_manager.py`

```python
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
```

### Apply Shutdown Handlers

**File:** `src/ybis/control_plane/db.py`

```python
from ..services.shutdown_manager import register_shutdown_handler

class ControlPlaneDB:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._connection = None

        # Register cleanup on shutdown
        register_shutdown_handler(
            self._cleanup,
            name="control_plane_db",
            priority=90,  # Close DB late
        )

    def _cleanup(self):
        """Close database connection."""
        if self._connection:
            self._connection.close()
            self._connection = None
```

**File:** `src/ybis/services/worker.py`

```python
from ..services.shutdown_manager import (
    register_shutdown_handler,
    is_shutting_down,
    shutdown_aware,
)

class Worker:
    def __init__(self):
        self._running_tasks: list = []
        register_shutdown_handler(
            self._shutdown,
            name="worker",
            priority=10,  # Stop worker early
        )

    def _shutdown(self):
        """Graceful worker shutdown."""
        logger.info(f"Worker shutting down, {len(self._running_tasks)} tasks in progress")
        # Wait for running tasks (with timeout)
        for task in self._running_tasks:
            task.cancel()

    @shutdown_aware
    def submit_task(self, task):
        """Submit task (fails if shutting down)."""
        ...

    def run_loop(self):
        """Main worker loop."""
        while not is_shutting_down():
            task = self.get_next_task()
            if task:
                self.process_task(task)
```

**File:** `src/ybis/data_plane/vector_store.py`

```python
from ..services.shutdown_manager import register_shutdown_handler

class VectorStore:
    def __init__(self):
        ...
        register_shutdown_handler(
            self._persist_and_close,
            name="vector_store",
            priority=80,
        )

    def _persist_and_close(self):
        """Persist data and close connections."""
        if self.client:
            # ChromaDB auto-persists, but ensure it's done
            pass
```

### Initialize at Startup

**File:** `src/ybis/__init__.py`

```python
# At module load
from .services.shutdown_manager import setup_signal_handlers
setup_signal_handlers()
```

### Files to Modify

| File | Change |
|------|--------|
| `src/ybis/services/shutdown_manager.py` | CREATE - New service |
| `src/ybis/__init__.py` | ADD - `setup_signal_handlers()` |
| `src/ybis/control_plane/db.py` | ADD - Shutdown handler |
| `src/ybis/services/worker.py` | ADD - Shutdown handler + aware loop |
| `src/ybis/data_plane/vector_store.py` | ADD - Shutdown handler |
| `src/ybis/adapters/graph_store_neo4j.py` | ADD - Shutdown handler |
| `src/ybis/orchestrator/graph.py` | ADD - `is_shutting_down()` check in loop |

---

## 4. UNIFIED RETRY STRATEGY

### Current Problem
11 files have retry logic, but inconsistent patterns.

### Create Unified Retry Service

**File:** `src/ybis/services/retry.py`

```python
"""
Unified Retry Service - Consistent retry patterns.

Combines retry, circuit breaker, and rate limiting.
"""

import logging
import random
import time
from functools import wraps
from typing import Any, Callable, Sequence, Type

logger = logging.getLogger(__name__)


class RetryConfig:
    """Retry configuration."""

    def __init__(
        self,
        max_attempts: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
        retryable_exceptions: Sequence[Type[Exception]] = (Exception,),
    ):
        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self.retryable_exceptions = tuple(retryable_exceptions)


# Preset configurations
RETRY_PRESETS = {
    "llm": RetryConfig(
        max_attempts=3,
        base_delay=2.0,
        max_delay=30.0,
        retryable_exceptions=(ConnectionError, TimeoutError, Exception),
    ),
    "database": RetryConfig(
        max_attempts=5,
        base_delay=0.5,
        max_delay=10.0,
        retryable_exceptions=(ConnectionError, TimeoutError),
    ),
    "external_api": RetryConfig(
        max_attempts=3,
        base_delay=1.0,
        max_delay=15.0,
    ),
    "file_operation": RetryConfig(
        max_attempts=3,
        base_delay=0.1,
        max_delay=2.0,
        retryable_exceptions=(IOError, PermissionError),
    ),
}


def with_retry(
    config: RetryConfig | str = "external_api",
    on_retry: Callable[[int, Exception], None] | None = None,
):
    """
    Decorator for retry with exponential backoff.

    Args:
        config: RetryConfig or preset name
        on_retry: Callback on each retry (attempt, exception)

    Example:
        @with_retry("llm")
        def call_ollama():
            ...

        @with_retry(RetryConfig(max_attempts=5))
        def custom_operation():
            ...
    """
    if isinstance(config, str):
        config = RETRY_PRESETS.get(config, RETRY_PRESETS["external_api"])

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(1, config.max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except config.retryable_exceptions as e:
                    last_exception = e

                    if attempt == config.max_attempts:
                        logger.error(f"{func.__name__} failed after {attempt} attempts: {e}")
                        raise

                    # Calculate delay
                    delay = min(
                        config.base_delay * (config.exponential_base ** (attempt - 1)),
                        config.max_delay,
                    )
                    if config.jitter:
                        delay *= (0.5 + random.random())

                    logger.warning(
                        f"{func.__name__} attempt {attempt} failed: {e}. "
                        f"Retrying in {delay:.2f}s..."
                    )

                    # Callback
                    if on_retry:
                        on_retry(attempt, e)

                    # Journal event
                    try:
                        from ..constants import PROJECT_ROOT
                        from ..syscalls.journal import append_event
                        append_event(
                            PROJECT_ROOT / "platform_data",
                            "RETRY_ATTEMPT",
                            {
                                "function": func.__name__,
                                "attempt": attempt,
                                "max_attempts": config.max_attempts,
                                "error": str(e),
                                "delay_seconds": round(delay, 2),
                            },
                        )
                    except Exception:
                        pass

                    time.sleep(delay)

            raise last_exception

        return wrapper
    return decorator


def resilient(
    breaker_name: str | None = None,
    rate_limit: tuple[float, int] | None = None,
    retry_config: RetryConfig | str = "external_api",
):
    """
    Combined decorator: retry + circuit breaker + rate limiting.

    Args:
        breaker_name: Circuit breaker name (None to skip)
        rate_limit: (rate, capacity) tuple (None to skip)
        retry_config: Retry configuration

    Example:
        @resilient(
            breaker_name="ollama",
            rate_limit=(2.0, 5),
            retry_config="llm",
        )
        def call_ollama(prompt):
            ...
    """
    def decorator(func: Callable) -> Callable:
        wrapped = func

        # Apply retry (innermost)
        wrapped = with_retry(retry_config)(wrapped)

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
```

### Apply Unified Pattern

**File:** `src/ybis/adapters/local_coder.py`

```python
from ..services.retry import resilient

# Replace manual retry with unified pattern
@resilient(
    breaker_name="ollama",
    rate_limit=(2.0, 5),
    retry_config="llm",
)
def _call_llm(model, messages, api_base, timeout):
    import litellm
    return litellm.completion(
        model=model,
        messages=messages,
        api_base=api_base,
        timeout=timeout,
    )
```

### Files to Modify

| File | Change |
|------|--------|
| `src/ybis/services/retry.py` | CREATE - Unified retry service |
| `src/ybis/services/resilience.py` | MODIFY - Use new retry service |
| `src/ybis/adapters/local_coder.py` | MODIFY - Use `@resilient` |
| `src/ybis/adapters/aider.py` | MODIFY - Use `@resilient` |
| `src/ybis/orchestrator/planner.py` | MODIFY - Use `@resilient` |

---

## Verification Checklist

```bash
# Verify circuit breaker
python -c "from src.ybis.services.circuit_breaker import get_all_breaker_status; print(get_all_breaker_status())"

# Verify rate limiter
python -c "from src.ybis.services.rate_limiter import get_limiter_status; print(get_limiter_status('ollama'))"

# Verify shutdown handlers
python -c "from src.ybis.services.shutdown_manager import _shutdown_handlers; print(len(_shutdown_handlers), 'handlers registered')"

# Test graceful shutdown
python -c "
from src.ybis.services.shutdown_manager import setup_signal_handlers, register_shutdown_handler
setup_signal_handlers()
register_shutdown_handler(lambda: print('Cleanup!'), 'test')
import signal; signal.raise_signal(signal.SIGTERM)
"
```

---

## Success Criteria

- [ ] Circuit breaker on all external service calls
- [ ] Rate limiting on all LLM calls
- [ ] Graceful shutdown for all long-running processes
- [ ] Unified retry pattern across codebase
- [ ] Journal events for all resilience actions
- [ ] Health check endpoint shows breaker status
