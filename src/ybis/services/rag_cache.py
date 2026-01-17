"""RAG Query Caching Service.

Caches vector store query results to avoid repeated embedding + search operations.
"""

import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any

from ..constants import PROJECT_ROOT

logger = logging.getLogger(__name__)


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

