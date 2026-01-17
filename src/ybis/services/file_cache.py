"""File Content Cache.

Caches file contents with mtime-based invalidation.
"""

import logging
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


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

