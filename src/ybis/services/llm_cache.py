"""LLM Response Caching Service.

Caches LLM responses based on prompt hash to avoid duplicate API calls.
"""

import hashlib
import json
import logging
import time
from pathlib import Path
from typing import Any

from ..constants import PROJECT_ROOT
from ..syscalls.journal import append_event

logger = logging.getLogger(__name__)


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

