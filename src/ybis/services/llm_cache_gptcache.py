"""
LLM Cache with GPTCache - Semantic caching for LLM responses.

Uses GPTCache for semantic similarity-based caching (similar prompts = cache hit).
Falls back to exact-match caching if GPTCache is unavailable.
"""

import logging
from pathlib import Path
from typing import Any

from ..constants import PROJECT_ROOT
from ..syscalls.journal import append_event

logger = logging.getLogger(__name__)

# Try to import GPTCache
try:
    from gptcache import Cache
    from gptcache.adapter import openai
    from gptcache.embedding import Onnx
    from gptcache.manager import CacheBase, VectorBase, get_data_manager
    from gptcache.similarity_evaluation import SearchDistanceEvaluation

    GPTCACHE_AVAILABLE = True
except ImportError:
    GPTCACHE_AVAILABLE = False
    logger.warning("GPTCache not installed. Falling back to exact-match caching.")


class GPTCacheLLMCache:
    """
    LLM Cache using GPTCache for semantic similarity.

    Provides semantic caching: similar prompts reuse cache (not just exact match).
    Higher cache hit rate than exact-match caching.
    """

    def __init__(self, cache_dir: Path | None = None):
        """
        Initialize GPTCache.

        Args:
            cache_dir: Directory for cache storage. Defaults to platform_data/cache/gptcache
        """
        if not GPTCACHE_AVAILABLE:
            raise ImportError(
                "GPTCache not available. Install with: pip install gptcache"
            )

        self.cache_dir = cache_dir or PROJECT_ROOT / "platform_data" / "cache" / "gptcache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        # Initialize GPTCache
        self._init_cache()

    def _init_cache(self) -> None:
        """Initialize GPTCache with semantic similarity."""
        try:
            # Use ONNX embedding model (lightweight, no external API)
            embedding_model = Onnx()

            # Create data manager (SQLite + vector store)
            data_manager = get_data_manager(
                cache_base=CacheBase("sqlite", sql_url=f"sqlite:///{self.cache_dir / 'cache.db'}"),
                vector_base=VectorBase("faiss", dimension=embedding_model.dimension),
            )

            # Create cache with similarity evaluation
            self.cache = Cache()
            self.cache.init(
                embedding_func=embedding_model.to_embeddings,
                data_manager=data_manager,
                similarity_evaluation=SearchDistanceEvaluation(),
            )

            logger.info("GPTCache initialized with semantic similarity")
        except Exception as e:
            logger.error(f"Failed to initialize GPTCache: {e}")
            raise

    def get(self, model: str, prompt: str, temperature: float = 0.0) -> str | None:
        """
        Get cached response using semantic similarity.

        Args:
            model: Model name
            prompt: The prompt text
            temperature: Temperature setting (0.0 for deterministic)

        Returns:
            Cached response or None if not found
        """
        # Only cache deterministic responses
        if temperature > 0.1:
            return None

        try:
            # GPTCache uses prompt as key (semantic similarity)
            # Create a cache key that includes model for separation
            cache_key = f"{model}:{prompt}"

            # Try to get from cache
            cached_response = self.cache.get(cache_key)

            if cached_response:
                append_event(
                    PROJECT_ROOT / "platform_data",
                    "LLM_CACHE_HIT_SEMANTIC",
                    {
                        "model": model,
                        "prompt_length": len(prompt),
                        "cached_length": len(str(cached_response)),
                    },
                )
                return str(cached_response)

            return None
        except Exception as e:
            logger.warning(f"GPTCache get failed: {e}")
            return None

    def set(
        self,
        model: str,
        prompt: str,
        response: str,
        temperature: float = 0.0,
    ) -> None:
        """
        Store response in cache using semantic similarity.

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

        try:
            # Create cache key
            cache_key = f"{model}:{prompt}"

            # Store in cache (GPTCache handles semantic similarity automatically)
            self.cache.put(cache_key, response)

            append_event(
                PROJECT_ROOT / "platform_data",
                "LLM_CACHE_SET_SEMANTIC",
                {
                    "model": model,
                    "prompt_length": len(prompt),
                    "response_length": len(response),
                },
            )
        except Exception as e:
            logger.warning(f"GPTCache set failed: {e}")

    def get_stats(self) -> dict[str, Any]:
        """Get cache statistics."""
        try:
            # GPTCache doesn't expose stats directly, return basic info
            cache_db = self.cache_dir / "cache.db"
            return {
                "cache_type": "gptcache_semantic",
                "cache_db_exists": cache_db.exists(),
                "cache_db_size": cache_db.stat().st_size if cache_db.exists() else 0,
            }
        except Exception:
            return {"cache_type": "gptcache_semantic", "error": "stats_unavailable"}


# Hybrid cache: Try GPTCache first, fallback to exact-match
def get_llm_cache_hybrid() -> Any:
    """
    Get LLM cache instance (GPTCache if available, else exact-match).

    Returns:
        GPTCacheLLMCache if available, else LLMCache (exact-match)
    """
    if GPTCACHE_AVAILABLE:
        try:
            return GPTCacheLLMCache()
        except Exception as e:
            logger.warning(f"GPTCache initialization failed: {e}, falling back to exact-match")
            from .llm_cache import get_llm_cache
            return get_llm_cache()
    else:
        from .llm_cache import get_llm_cache
        return get_llm_cache()


