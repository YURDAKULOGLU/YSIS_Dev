# PERFORMANCE OPTIMIZATION TASK

## Objective
Implement comprehensive caching, concurrency, and resource optimization across all components.

## Current State
- **Caching:** 0 explicit cache decorators in src/ybis/
- **Redis:** Only used for event bus (optional)
- **Concurrency:** ThreadPoolExecutor in 2 files (parallel_execution.py, registry.py)
- **Connection Pooling:** None
- **Request Batching:** None

---

## CRITICAL PRIORITY

### 1. LLM Response Caching Service

**Location:** `src/ybis/services/llm_cache.py` (NEW FILE)

**Why:** Same prompts often sent repeatedly. LLM calls are expensive ($) and slow.

```python
"""LLM Response Caching Service.

Caches LLM responses based on prompt hash to avoid duplicate API calls.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

from ..constants import PROJECT_ROOT
from ..syscalls.journal import append_event


class LLMCache:
    """Cache for LLM responses using file-based storage."""

    def __init__(self, cache_dir: Path | None = None, ttl_seconds: int = 86400):
        """Initialize cache.

        Args:
            cache_dir: Directory for cache files. Defaults to platform_data/cache/llm
            ttl_seconds: Time-to-live for cache entries. Default 24 hours.
        """
        self.cache_dir = cache_dir or PROJECT_ROOT / "platform_data" / "cache" / "llm"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl_seconds = ttl_seconds
        self._stats = {"hits": 0, "misses": 0}

    def _hash_key(self, model: str, prompt: str, temperature: float = 0.0) -> str:
        """Generate cache key from prompt parameters."""
        key_data = f"{model}:{temperature}:{prompt}"
        return hashlib.sha256(key_data.encode()).hexdigest()[:32]

    def get(self, model: str, prompt: str, temperature: float = 0.0) -> str | None:
        """Get cached response if exists and not expired.

        Args:
            model: Model name (e.g., "gpt-4")
            prompt: The prompt text
            temperature: Temperature setting (0.0 for deterministic)

        Returns:
            Cached response or None if not found/expired
        """
        # Only cache deterministic responses
        if temperature > 0.1:
            return None

        cache_key = self._hash_key(model, prompt, temperature)
        cache_file = self.cache_dir / f"{cache_key}.json"

        if not cache_file.exists():
            self._stats["misses"] += 1
            return None

        try:
            data = json.loads(cache_file.read_text(encoding="utf-8"))

            # Check TTL
            if time.time() - data["timestamp"] > self.ttl_seconds:
                cache_file.unlink(missing_ok=True)
                self._stats["misses"] += 1
                return None

            self._stats["hits"] += 1
            append_event(
                PROJECT_ROOT / "platform_data",
                "LLM_CACHE_HIT",
                {
                    "model": model,
                    "prompt_hash": cache_key,
                    "prompt_length": len(prompt),
                    "cached_length": len(data["response"]),
                    "age_seconds": int(time.time() - data["timestamp"]),
                },
            )
            return data["response"]

        except (json.JSONDecodeError, KeyError):
            cache_file.unlink(missing_ok=True)
            self._stats["misses"] += 1
            return None

    def set(
        self,
        model: str,
        prompt: str,
        response: str,
        temperature: float = 0.0,
    ) -> None:
        """Store response in cache.

        Args:
            model: Model name
            prompt: The prompt text
            response: The LLM response to cache
            temperature: Temperature setting
        """
        # Only cache deterministic responses
        if temperature > 0.1:
            return

        # Don't cache empty or very short responses
        if not response or len(response.strip()) < 50:
            return

        cache_key = self._hash_key(model, prompt, temperature)
        cache_file = self.cache_dir / f"{cache_key}.json"

        data = {
            "model": model,
            "prompt_hash": cache_key,
            "response": response,
            "timestamp": time.time(),
            "prompt_length": len(prompt),
        }

        cache_file.write_text(json.dumps(data), encoding="utf-8")

        append_event(
            PROJECT_ROOT / "platform_data",
            "LLM_CACHE_SET",
            {
                "model": model,
                "prompt_hash": cache_key,
                "prompt_length": len(prompt),
                "response_length": len(response),
            },
        )

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        hit_rate = 0.0
        total = self._stats["hits"] + self._stats["misses"]
        if total > 0:
            hit_rate = self._stats["hits"] / total

        # Count cache files
        cache_files = list(self.cache_dir.glob("*.json"))
        total_size = sum(f.stat().st_size for f in cache_files)

        return {
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "hit_rate": round(hit_rate, 3),
            "cache_entries": len(cache_files),
            "cache_size_bytes": total_size,
        }

    def clear_expired(self) -> int:
        """Remove expired cache entries.

        Returns:
            Number of entries removed
        """
        removed = 0
        current_time = time.time()

        for cache_file in self.cache_dir.glob("*.json"):
            try:
                data = json.loads(cache_file.read_text(encoding="utf-8"))
                if current_time - data["timestamp"] > self.ttl_seconds:
                    cache_file.unlink()
                    removed += 1
            except (json.JSONDecodeError, KeyError):
                cache_file.unlink(missing_ok=True)
                removed += 1

        return removed

    def clear_all(self) -> int:
        """Clear entire cache.

        Returns:
            Number of entries removed
        """
        removed = 0
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            removed += 1
        return removed


# Global instance
_llm_cache: LLMCache | None = None


def get_llm_cache() -> LLMCache:
    """Get global LLM cache instance."""
    global _llm_cache
    if _llm_cache is None:
        _llm_cache = LLMCache()
    return _llm_cache
```

---

### 2. Integration with LocalCoder

**Location:** `src/ybis/adapters/local_coder.py`

**Add cache lookup before LLM call (~line 230):**

```python
from ..services.llm_cache import get_llm_cache

# Before LLM call
cache = get_llm_cache()
cached_response = cache.get(self.model, prompt, temperature=0.0)

if cached_response:
    logger.info(f"Using cached LLM response for {file_path.name}")
    new_content = cached_response
else:
    # Existing LLM call
    response = await litellm.acompletion(...)
    new_content = response.choices[0].message.content

    # Cache the response
    cache.set(self.model, prompt, new_content, temperature=0.0)
```

---

### 3. RAG Query Caching

**Location:** `src/ybis/services/rag_cache.py` (NEW FILE)

**Why:** Vector store queries are repeated for similar tasks.

```python
"""RAG Query Caching Service.

Caches vector store query results to avoid repeated embedding + search operations.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any

from ..constants import PROJECT_ROOT


class RAGCache:
    """Cache for RAG query results."""

    def __init__(
        self,
        cache_dir: Path | None = None,
        ttl_seconds: int = 3600,  # 1 hour default
    ):
        self.cache_dir = cache_dir or PROJECT_ROOT / "platform_data" / "cache" / "rag"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl_seconds = ttl_seconds

    def _hash_key(self, collection: str, query: str, top_k: int) -> str:
        """Generate cache key."""
        key_data = f"{collection}:{top_k}:{query}"
        return hashlib.sha256(key_data.encode()).hexdigest()[:32]

    def get(
        self,
        collection: str,
        query: str,
        top_k: int = 5,
    ) -> list[dict[str, Any]] | None:
        """Get cached query results."""
        cache_key = self._hash_key(collection, query, top_k)
        cache_file = self.cache_dir / f"{cache_key}.json"

        if not cache_file.exists():
            return None

        try:
            data = json.loads(cache_file.read_text(encoding="utf-8"))

            if time.time() - data["timestamp"] > self.ttl_seconds:
                cache_file.unlink(missing_ok=True)
                return None

            return data["results"]

        except (json.JSONDecodeError, KeyError):
            cache_file.unlink(missing_ok=True)
            return None

    def set(
        self,
        collection: str,
        query: str,
        results: list[dict[str, Any]],
        top_k: int = 5,
    ) -> None:
        """Store query results in cache."""
        if not results:
            return

        cache_key = self._hash_key(collection, query, top_k)
        cache_file = self.cache_dir / f"{cache_key}.json"

        data = {
            "collection": collection,
            "query_hash": cache_key,
            "results": results,
            "timestamp": time.time(),
        }

        cache_file.write_text(json.dumps(data), encoding="utf-8")


# Global instance
_rag_cache: RAGCache | None = None


def get_rag_cache() -> RAGCache:
    """Get global RAG cache instance."""
    global _rag_cache
    if _rag_cache is None:
        _rag_cache = RAGCache()
    return _rag_cache
```

---

## HIGH PRIORITY

### 4. Connection Pool Manager

**Location:** `src/ybis/services/connection_pool.py` (NEW FILE)

**Why:** Database and HTTP connections are expensive to create.

```python
"""Connection Pool Manager.

Manages pooled connections for database and HTTP clients.
"""
from __future__ import annotations

import sqlite3
import threading
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from queue import Empty, Queue
from typing import Any

import httpx


class SQLitePool:
    """Connection pool for SQLite databases."""

    def __init__(self, db_path: Path, pool_size: int = 5, timeout: float = 30.0):
        self.db_path = db_path
        self.pool_size = pool_size
        self.timeout = timeout
        self._pool: Queue[sqlite3.Connection] = Queue(maxsize=pool_size)
        self._lock = threading.Lock()
        self._initialized = False

    def _create_connection(self) -> sqlite3.Connection:
        """Create a new database connection."""
        conn = sqlite3.connect(
            str(self.db_path),
            timeout=self.timeout,
            check_same_thread=False,  # Allow multi-threaded access
        )
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn

    def initialize(self) -> None:
        """Pre-populate the pool with connections."""
        with self._lock:
            if self._initialized:
                return
            for _ in range(self.pool_size):
                self._pool.put(self._create_connection())
            self._initialized = True

    @contextmanager
    def get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Get a connection from the pool.

        Yields:
            A database connection
        """
        if not self._initialized:
            self.initialize()

        conn = None
        try:
            conn = self._pool.get(timeout=self.timeout)
            yield conn
        finally:
            if conn is not None:
                self._pool.put(conn)

    def close_all(self) -> None:
        """Close all pooled connections."""
        while True:
            try:
                conn = self._pool.get_nowait()
                conn.close()
            except Empty:
                break


class HTTPClientPool:
    """Pooled HTTP client for external API calls."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: float = 30.0,
        max_connections: int = 10,
    ):
        self.base_url = base_url
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            limits=httpx.Limits(
                max_connections=max_connections,
                max_keepalive_connections=max_connections // 2,
            ),
        )

    def get(self, url: str, **kwargs: Any) -> httpx.Response:
        """Make GET request."""
        return self._client.get(url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> httpx.Response:
        """Make POST request."""
        return self._client.post(url, **kwargs)

    def close(self) -> None:
        """Close the HTTP client."""
        self._client.close()


# Global pools
_sqlite_pools: dict[str, SQLitePool] = {}
_http_pools: dict[str, HTTPClientPool] = {}
_pools_lock = threading.Lock()


def get_sqlite_pool(db_path: Path) -> SQLitePool:
    """Get or create SQLite pool for given database."""
    key = str(db_path)
    with _pools_lock:
        if key not in _sqlite_pools:
            _sqlite_pools[key] = SQLitePool(db_path)
        return _sqlite_pools[key]


def get_http_pool(base_url: str | None = None) -> HTTPClientPool:
    """Get or create HTTP client pool."""
    key = base_url or "default"
    with _pools_lock:
        if key not in _http_pools:
            _http_pools[key] = HTTPClientPool(base_url)
        return _http_pools[key]


def close_all_pools() -> None:
    """Close all connection pools. Call on shutdown."""
    with _pools_lock:
        for pool in _sqlite_pools.values():
            pool.close_all()
        for pool in _http_pools.values():
            pool.close()
        _sqlite_pools.clear()
        _http_pools.clear()
```

---

### 5. File Content Cache

**Location:** `src/ybis/services/file_cache.py` (NEW FILE)

**Why:** Same files read multiple times during a workflow run.

```python
"""File Content Cache.

Caches file contents with mtime-based invalidation.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class CachedFile:
    """Cached file entry."""

    content: str
    mtime: float
    size: int


class FileCache:
    """In-memory cache for file contents."""

    def __init__(self, max_entries: int = 100, max_total_size: int = 10_000_000):
        """Initialize file cache.

        Args:
            max_entries: Maximum number of cached files
            max_total_size: Maximum total cache size in bytes
        """
        self.max_entries = max_entries
        self.max_total_size = max_total_size
        self._cache: dict[str, CachedFile] = {}
        self._lock = threading.Lock()
        self._total_size = 0
        self._access_order: list[str] = []  # LRU tracking

    def get(self, file_path: Path) -> str | None:
        """Get cached file content if valid.

        Args:
            file_path: Path to file

        Returns:
            File content or None if not cached/stale
        """
        key = str(file_path.resolve())

        with self._lock:
            if key not in self._cache:
                return None

            entry = self._cache[key]

            # Check if file was modified
            try:
                current_mtime = file_path.stat().st_mtime
                if current_mtime != entry.mtime:
                    # File changed, invalidate
                    self._remove_entry(key)
                    return None
            except FileNotFoundError:
                self._remove_entry(key)
                return None

            # Update access order (LRU)
            if key in self._access_order:
                self._access_order.remove(key)
            self._access_order.append(key)

            return entry.content

    def set(self, file_path: Path, content: str) -> None:
        """Cache file content.

        Args:
            file_path: Path to file
            content: File content
        """
        key = str(file_path.resolve())
        size = len(content.encode("utf-8"))

        # Don't cache very large files
        if size > self.max_total_size // 2:
            return

        with self._lock:
            # Remove existing entry if present
            if key in self._cache:
                self._remove_entry(key)

            # Evict entries if needed
            while (
                len(self._cache) >= self.max_entries
                or self._total_size + size > self.max_total_size
            ) and self._access_order:
                oldest_key = self._access_order[0]
                self._remove_entry(oldest_key)

            try:
                mtime = file_path.stat().st_mtime
            except FileNotFoundError:
                return

            self._cache[key] = CachedFile(content=content, mtime=mtime, size=size)
            self._total_size += size
            self._access_order.append(key)

    def _remove_entry(self, key: str) -> None:
        """Remove entry from cache (must hold lock)."""
        if key in self._cache:
            self._total_size -= self._cache[key].size
            del self._cache[key]
        if key in self._access_order:
            self._access_order.remove(key)

    def invalidate(self, file_path: Path) -> None:
        """Invalidate cache entry for file."""
        key = str(file_path.resolve())
        with self._lock:
            self._remove_entry(key)

    def clear(self) -> None:
        """Clear all cached entries."""
        with self._lock:
            self._cache.clear()
            self._access_order.clear()
            self._total_size = 0

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        with self._lock:
            return {
                "entries": len(self._cache),
                "total_size_bytes": self._total_size,
                "max_entries": self.max_entries,
                "max_total_size": self.max_total_size,
            }


# Global instance
_file_cache: FileCache | None = None


def get_file_cache() -> FileCache:
    """Get global file cache instance."""
    global _file_cache
    if _file_cache is None:
        _file_cache = FileCache()
    return _file_cache
```

---

### 6. Request Batching for LLM Calls

**Location:** `src/ybis/services/llm_batcher.py` (NEW FILE)

**Why:** Multiple small LLM requests can be batched for efficiency.

```python
"""LLM Request Batcher.

Batches multiple LLM requests for improved throughput.
"""
from __future__ import annotations

import asyncio
from dataclasses import dataclass, field
from typing import Any

import litellm


@dataclass
class BatchRequest:
    """Single request in a batch."""

    prompt: str
    model: str
    future: asyncio.Future[str] = field(default_factory=lambda: asyncio.Future())


class LLMBatcher:
    """Batches LLM requests for improved throughput."""

    def __init__(
        self,
        batch_size: int = 5,
        batch_timeout: float = 0.1,  # 100ms
    ):
        """Initialize batcher.

        Args:
            batch_size: Maximum requests per batch
            batch_timeout: Max time to wait for batch to fill (seconds)
        """
        self.batch_size = batch_size
        self.batch_timeout = batch_timeout
        self._queue: asyncio.Queue[BatchRequest] = asyncio.Queue()
        self._running = False
        self._task: asyncio.Task[None] | None = None

    async def start(self) -> None:
        """Start the batch processor."""
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._process_batches())

    async def stop(self) -> None:
        """Stop the batch processor."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _process_batches(self) -> None:
        """Process batches from queue."""
        while self._running:
            batch: list[BatchRequest] = []

            try:
                # Wait for first request
                request = await asyncio.wait_for(
                    self._queue.get(),
                    timeout=1.0,
                )
                batch.append(request)

                # Collect more requests up to batch size or timeout
                deadline = asyncio.get_event_loop().time() + self.batch_timeout
                while len(batch) < self.batch_size:
                    remaining = deadline - asyncio.get_event_loop().time()
                    if remaining <= 0:
                        break
                    try:
                        request = await asyncio.wait_for(
                            self._queue.get(),
                            timeout=remaining,
                        )
                        batch.append(request)
                    except asyncio.TimeoutError:
                        break

                # Process batch
                await self._execute_batch(batch)

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                # Set exception on all pending futures
                for req in batch:
                    if not req.future.done():
                        req.future.set_exception(e)

    async def _execute_batch(self, batch: list[BatchRequest]) -> None:
        """Execute a batch of requests."""
        # Group by model
        by_model: dict[str, list[BatchRequest]] = {}
        for req in batch:
            by_model.setdefault(req.model, []).append(req)

        # Execute each model group
        tasks = []
        for model, requests in by_model.items():
            tasks.append(self._execute_model_batch(model, requests))

        await asyncio.gather(*tasks, return_exceptions=True)

    async def _execute_model_batch(
        self,
        model: str,
        requests: list[BatchRequest],
    ) -> None:
        """Execute batch for single model."""
        # Execute requests concurrently
        async def execute_single(req: BatchRequest) -> None:
            try:
                response = await litellm.acompletion(
                    model=model,
                    messages=[{"role": "user", "content": req.prompt}],
                )
                result = response.choices[0].message.content or ""
                req.future.set_result(result)
            except Exception as e:
                req.future.set_exception(e)

        await asyncio.gather(*[execute_single(r) for r in requests])

    async def submit(self, model: str, prompt: str) -> str:
        """Submit a request and wait for result.

        Args:
            model: Model name
            prompt: Prompt text

        Returns:
            LLM response
        """
        request = BatchRequest(prompt=prompt, model=model)
        await self._queue.put(request)
        return await request.future


# Global instance
_batcher: LLMBatcher | None = None


async def get_batcher() -> LLMBatcher:
    """Get global batcher instance."""
    global _batcher
    if _batcher is None:
        _batcher = LLMBatcher()
        await _batcher.start()
    return _batcher
```

---

## MEDIUM PRIORITY

### 7. Async Concurrency Utilities

**Location:** `src/ybis/services/async_utils.py` (NEW FILE)

```python
"""Async Concurrency Utilities.

Provides controlled concurrency for async operations.
"""
from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

T = TypeVar("T")


class Semaphore:
    """Semaphore with timeout and metrics."""

    def __init__(self, max_concurrent: int = 5, name: str = "default"):
        self.name = name
        self.max_concurrent = max_concurrent
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._waiting = 0
        self._active = 0

    async def __aenter__(self) -> "Semaphore":
        self._waiting += 1
        await self._semaphore.acquire()
        self._waiting -= 1
        self._active += 1
        return self

    async def __aexit__(self, *args: Any) -> None:
        self._active -= 1
        self._semaphore.release()

    @property
    def stats(self) -> dict[str, int]:
        return {
            "name": self.name,
            "max_concurrent": self.max_concurrent,
            "active": self._active,
            "waiting": self._waiting,
        }


async def gather_with_concurrency(
    limit: int,
    *coros: Awaitable[T],
) -> list[T]:
    """Run coroutines with limited concurrency.

    Args:
        limit: Maximum concurrent coroutines
        *coros: Coroutines to run

    Returns:
        List of results in order
    """
    semaphore = asyncio.Semaphore(limit)

    async def limited(coro: Awaitable[T]) -> T:
        async with semaphore:
            return await coro

    return await asyncio.gather(*[limited(c) for c in coros])


async def retry_async(
    func: Callable[..., Awaitable[T]],
    *args: Any,
    max_attempts: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    **kwargs: Any,
) -> T:
    """Retry async function with exponential backoff.

    Args:
        func: Async function to call
        *args: Positional arguments
        max_attempts: Maximum attempts
        delay: Initial delay between retries
        backoff: Backoff multiplier
        **kwargs: Keyword arguments

    Returns:
        Function result

    Raises:
        Last exception if all attempts fail
    """
    last_error: Exception | None = None
    current_delay = delay

    for attempt in range(max_attempts):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_error = e
            if attempt < max_attempts - 1:
                await asyncio.sleep(current_delay)
                current_delay *= backoff

    raise last_error  # type: ignore


# Global semaphores for common operations
_llm_semaphore: Semaphore | None = None
_file_semaphore: Semaphore | None = None


def get_llm_semaphore(max_concurrent: int = 3) -> Semaphore:
    """Get semaphore for LLM operations."""
    global _llm_semaphore
    if _llm_semaphore is None:
        _llm_semaphore = Semaphore(max_concurrent, "llm")
    return _llm_semaphore


def get_file_semaphore(max_concurrent: int = 10) -> Semaphore:
    """Get semaphore for file operations."""
    global _file_semaphore
    if _file_semaphore is None:
        _file_semaphore = Semaphore(max_concurrent, "file")
    return _file_semaphore
```

---

### 8. Lazy Loading for Heavy Imports

**Location:** Update `src/ybis/adapters/__init__.py`

**Why:** Heavy imports (torch, transformers) slow down startup.

```python
"""Adapters module with lazy loading for heavy dependencies."""
from __future__ import annotations

from typing import TYPE_CHECKING

# Type checking imports (no runtime cost)
if TYPE_CHECKING:
    from .llamaindex_adapter import LlamaIndexAdapter
    from .vector_store_chroma import ChromaVectorStore
    from .evoagentx import EvoAgentXAdapter

# Lazy loading implementation
_lazy_imports: dict[str, tuple[str, str]] = {
    "LlamaIndexAdapter": ("llamaindex_adapter", "LlamaIndexAdapter"),
    "ChromaVectorStore": ("vector_store_chroma", "ChromaVectorStore"),
    "EvoAgentXAdapter": ("evoagentx", "EvoAgentXAdapter"),
}


def __getattr__(name: str):
    """Lazy import heavy adapters."""
    if name in _lazy_imports:
        module_name, attr_name = _lazy_imports[name]
        import importlib
        module = importlib.import_module(f".{module_name}", __package__)
        return getattr(module, attr_name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = list(_lazy_imports.keys())
```

---

## Integration Points

### LocalCoder Integration

```python
# src/ybis/adapters/local_coder.py

from ..services.llm_cache import get_llm_cache
from ..services.file_cache import get_file_cache
from ..services.async_utils import get_llm_semaphore

class LocalCoder:
    async def _call_llm(self, prompt: str, file_path: Path) -> str:
        cache = get_llm_cache()

        # Check cache first
        cached = cache.get(self.model, prompt)
        if cached:
            return cached

        # Use semaphore to limit concurrent LLM calls
        async with get_llm_semaphore():
            response = await litellm.acompletion(...)
            result = response.choices[0].message.content

        # Cache result
        cache.set(self.model, prompt, result)
        return result

    def _read_file(self, file_path: Path) -> str:
        cache = get_file_cache()

        # Check cache
        cached = cache.get(file_path)
        if cached:
            return cached

        # Read from disk
        content = file_path.read_text(encoding="utf-8")

        # Cache for later
        cache.set(file_path, content)
        return content
```

### Planner Integration

```python
# src/ybis/orchestrator/planner.py

from ..services.rag_cache import get_rag_cache

class Planner:
    def _query_rag(self, query: str, collection: str) -> list[dict]:
        cache = get_rag_cache()

        # Check cache
        cached = cache.get(collection, query)
        if cached:
            return cached

        # Query vector store
        results = self.vector_store.query(collection, query)

        # Cache results
        cache.set(collection, query, results)
        return results
```

---

## Configuration

**Add to** `configs/performance.yaml`:

```yaml
# Performance Configuration

cache:
  llm:
    enabled: true
    ttl_seconds: 86400  # 24 hours
    max_size_mb: 100

  rag:
    enabled: true
    ttl_seconds: 3600  # 1 hour

  file:
    enabled: true
    max_entries: 100
    max_total_size_mb: 10

concurrency:
  llm:
    max_concurrent: 3
    batch_size: 5
    batch_timeout_ms: 100

  file:
    max_concurrent: 10

  workflow:
    max_parallel_nodes: 4

connection_pool:
  sqlite:
    pool_size: 5
    timeout_seconds: 30

  http:
    max_connections: 10
    keepalive_connections: 5
```

---

## Verification Checklist

After implementation:

```bash
# Check cache modules exist
ls src/ybis/services/*cache*.py

# Check imports work
python -c "from ybis.services.llm_cache import get_llm_cache; print(get_llm_cache())"

# Run with cache enabled and check stats
python scripts/ybis_run.py TEST-PERF --workflow default
python -c "
from ybis.services.llm_cache import get_llm_cache
from ybis.services.file_cache import get_file_cache
print('LLM Cache:', get_llm_cache().get_stats())
print('File Cache:', get_file_cache().get_stats())
"
```

---

## Success Criteria

- [ ] LLM cache hit rate > 20% after 3 runs
- [ ] File cache hit rate > 50% during workflow
- [ ] RAG query cache reduces repeated queries by 80%
- [ ] Connection pool reduces SQLite connection time by 90%
- [ ] Semaphore prevents more than 3 concurrent LLM calls
- [ ] Lazy loading reduces import time by 2+ seconds
- [ ] All cache stats available via journal events

---

## Priority Order

1. **LLM Cache** - Highest cost savings
2. **File Cache** - Most frequent operation
3. **RAG Cache** - Repeated queries
4. **Connection Pool** - Foundation for scaling
5. **Async Utilities** - Concurrency control
6. **LLM Batcher** - Advanced optimization
7. **Lazy Loading** - Startup performance
