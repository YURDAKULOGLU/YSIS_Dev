"""
Migration System - Database schema versioning.

Simple file-based migrations with version tracking.
"""

import logging
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Callable

logger = logging.getLogger(__name__)


@dataclass
class Migration:
    """Migration definition."""
    version: int
    name: str
    up: Callable[[sqlite3.Connection], None]
    down: Callable[[sqlite3.Connection], None] | None = None


class MigrationRunner:
    """Runs database migrations."""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._migrations: list[Migration] = []

    def register(self, migration: Migration):
        """Register a migration."""
        self._migrations.append(migration)
        self._migrations.sort(key=lambda m: m.version)

    def _ensure_migrations_table(self, conn: sqlite3.Connection):
        """Create migrations tracking table."""
        conn.execute("""
            CREATE TABLE IF NOT EXISTS _migrations (
                version INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                applied_at TEXT NOT NULL
            )
        """)
        conn.commit()

    def _get_current_version(self, conn: sqlite3.Connection) -> int:
        """Get current migration version."""
        try:
            cursor = conn.execute("SELECT MAX(version) FROM _migrations")
            result = cursor.fetchone()[0]
            return result or 0
        except sqlite3.OperationalError:
            return 0

    def migrate(self, target_version: int | None = None) -> list[str]:
        """
        Run migrations up to target version.

        Args:
            target_version: Target version (None = latest)

        Returns:
            List of applied migration names
        """
        conn = sqlite3.connect(self.db_path)
        self._ensure_migrations_table(conn)

        current = self._get_current_version(conn)
        target = target_version or (max(m.version for m in self._migrations) if self._migrations else 0)

        applied = []

        if target > current:
            # Migrate up
            for migration in self._migrations:
                if current < migration.version <= target:
                    logger.info(f"Applying migration {migration.version}: {migration.name}")
                    try:
                        migration.up(conn)
                        conn.execute(
                            "INSERT INTO _migrations (version, name, applied_at) VALUES (?, ?, ?)",
                            (migration.version, migration.name, datetime.now().isoformat()),
                        )
                        conn.commit()
                        applied.append(migration.name)

                        # Journal event
                        try:
                            from ..constants import PROJECT_ROOT
                            from ..syscalls.journal import append_event
                            append_event(
                                PROJECT_ROOT / "platform_data",
                                "MIGRATION_APPLIED",
                                {
                                    "version": migration.version,
                                    "name": migration.name,
                                    "direction": "up",
                                },
                            )
                        except Exception:
                            pass

                    except Exception as e:
                        conn.rollback()
                        logger.error(f"Migration {migration.version} failed: {e}")
                        raise

        elif target < current:
            # Migrate down
            for migration in reversed(self._migrations):
                if target < migration.version <= current:
                    if migration.down is None:
                        raise ValueError(f"Migration {migration.version} has no down migration")

                    logger.info(f"Rolling back migration {migration.version}: {migration.name}")
                    try:
                        migration.down(conn)
                        conn.execute("DELETE FROM _migrations WHERE version = ?", (migration.version,))
                        conn.commit()
                        applied.append(f"ROLLBACK: {migration.name}")
                    except Exception as e:
                        conn.rollback()
                        logger.error(f"Rollback {migration.version} failed: {e}")
                        raise

        conn.close()
        return applied

    def status(self) -> dict:
        """Get migration status."""
        conn = sqlite3.connect(self.db_path)
        self._ensure_migrations_table(conn)

        current = self._get_current_version(conn)
        latest = max(m.version for m in self._migrations) if self._migrations else 0

        pending = [m for m in self._migrations if m.version > current]

        conn.close()
        return {
            "current_version": current,
            "latest_version": latest,
            "pending_count": len(pending),
            "pending": [{"version": m.version, "name": m.name} for m in pending],
        }

