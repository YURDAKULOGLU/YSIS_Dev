"""
Database Migrations - Schema versioning.

Usage:
    from src.ybis.migrations import run_migrations, migration_status

    # Run all pending migrations
    run_migrations()

    # Check status
    status = migration_status()
"""

import importlib.util
from pathlib import Path

from .base import MigrationRunner

# Import all migrations
# Note: Python module names can't start with numbers, so we use importlib
def _load_migration(module_name: str):
    """Load migration module by name."""
    versions_dir = Path(__file__).parent / "versions"
    spec = importlib.util.spec_from_file_location(
        module_name,
        versions_dir / f"{module_name}.py"
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load migration {module_name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.migration

m001 = _load_migration("001_initial_schema")
m002 = _load_migration("002_add_error_knowledge_base")
m003 = _load_migration("003_add_lessons_table")
m004 = _load_migration("004_add_metrics_table")

_runner: MigrationRunner | None = None


def _get_runner() -> MigrationRunner:
    """Get or create migration runner."""
    global _runner
    if _runner is None:
        from ..constants import PROJECT_ROOT
        db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)

        _runner = MigrationRunner(db_path)
        _runner.register(m001)
        _runner.register(m002)
        _runner.register(m003)
        _runner.register(m004)

    return _runner


def run_migrations(target_version: int | None = None) -> list[str]:
    """
    Run pending migrations.

    Args:
        target_version: Target version (None = latest)

    Returns:
        List of applied migration names
    """
    return _get_runner().migrate(target_version)


def migration_status() -> dict:
    """Get migration status."""
    return _get_runner().status()


def rollback(target_version: int) -> list[str]:
    """Rollback to target version."""
    return _get_runner().migrate(target_version)
