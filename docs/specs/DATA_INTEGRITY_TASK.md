# DATA INTEGRITY TASK

## Objective
Implement robust data management: Migrations, Backup/Recovery, Worktree Sync Fix.

## Current State
- **Migrations:** Empty directory (only `__init__.py`)
- **Backup/Recovery:** 2 files (minimal)
- **Worktree Sync:** BROKEN - uncommitted files not available in worktree

---

## 1. DATABASE MIGRATIONS

### Purpose
Version control for database schema changes.

### Create Migration System

**File:** `src/ybis/migrations/base.py`

```python
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
```

### Create Initial Migrations

**File:** `src/ybis/migrations/versions/001_initial_schema.py`

```python
"""
Migration 001: Initial schema for control_plane.db
"""

import sqlite3

from ..base import Migration


def up(conn: sqlite3.Connection):
    """Create initial tables."""
    # Tasks table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            objective TEXT,
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'MEDIUM',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Runs table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            task_id TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL,
            completed_at TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(task_id)
        )
    """)

    # Create indexes
    conn.execute("CREATE INDEX IF NOT EXISTS idx_runs_task_id ON runs(task_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_runs_status ON runs(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")


def down(conn: sqlite3.Connection):
    """Drop tables."""
    conn.execute("DROP TABLE IF EXISTS runs")
    conn.execute("DROP TABLE IF EXISTS tasks")


migration = Migration(
    version=1,
    name="initial_schema",
    up=up,
    down=down,
)
```

**File:** `src/ybis/migrations/versions/002_add_error_knowledge_base.py`

```python
"""
Migration 002: Error Knowledge Base tables
"""

import sqlite3

from ..base import Migration


def up(conn: sqlite3.Connection):
    """Create error KB tables."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS error_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT NOT NULL,
            run_id TEXT,
            step TEXT,
            error_type TEXT NOT NULL,
            error_message TEXT NOT NULL,
            stack_trace TEXT,
            context TEXT,
            created_at TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS error_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_type TEXT NOT NULL,
            error_message_pattern TEXT NOT NULL,
            occurrence_count INTEGER DEFAULT 1,
            suggested_fix TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_error_records_type ON error_records(error_type)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_error_records_task ON error_records(task_id)")


def down(conn: sqlite3.Connection):
    """Drop error KB tables."""
    conn.execute("DROP TABLE IF EXISTS error_patterns")
    conn.execute("DROP TABLE IF EXISTS error_records")


migration = Migration(
    version=2,
    name="add_error_knowledge_base",
    up=up,
    down=down,
)
```

**File:** `src/ybis/migrations/versions/003_add_lessons_table.py`

```python
"""
Migration 003: Lessons learned table
"""

import sqlite3

from ..base import Migration


def up(conn: sqlite3.Connection):
    """Create lessons table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_type TEXT NOT NULL,
            source TEXT,
            content TEXT NOT NULL,
            context TEXT,
            applied_count INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_lessons_type ON lessons(lesson_type)")


def down(conn: sqlite3.Connection):
    """Drop lessons table."""
    conn.execute("DROP TABLE IF EXISTS lessons")


migration = Migration(
    version=3,
    name="add_lessons_table",
    up=up,
    down=down,
)
```

**File:** `src/ybis/migrations/versions/004_add_metrics_table.py`

```python
"""
Migration 004: Metrics tracking table
"""

import sqlite3

from ..base import Migration


def up(conn: sqlite3.Connection):
    """Create metrics table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_name TEXT NOT NULL,
            metric_value REAL NOT NULL,
            labels TEXT,
            timestamp TEXT NOT NULL
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_metrics_name ON metrics(metric_name)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp)")


def down(conn: sqlite3.Connection):
    """Drop metrics table."""
    conn.execute("DROP TABLE IF EXISTS metrics")


migration = Migration(
    version=4,
    name="add_metrics_table",
    up=up,
    down=down,
)
```

### Migration Registry

**File:** `src/ybis/migrations/__init__.py`

```python
"""
Database Migrations - Schema versioning.

Usage:
    from src.ybis.migrations import run_migrations, migration_status

    # Run all pending migrations
    run_migrations()

    # Check status
    status = migration_status()
"""

from pathlib import Path

from .base import MigrationRunner

# Import all migrations
from .versions.v001_initial_schema import migration as m001
from .versions.v002_add_error_knowledge_base import migration as m002
from .versions.v003_add_lessons_table import migration as m003
from .versions.v004_add_metrics_table import migration as m004

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
```

### CLI Commands

**Add to:** `src/ybis/cli/__init__.py`

```python
@cli.group()
def db():
    """Database management commands."""
    pass


@db.command()
def migrate():
    """Run pending migrations."""
    from ..migrations import run_migrations, migration_status

    status = migration_status()
    if status["pending_count"] == 0:
        click.echo("No pending migrations.")
        return

    click.echo(f"Running {status['pending_count']} migrations...")
    applied = run_migrations()
    for name in applied:
        click.echo(f"  Applied: {name}")
    click.echo("Done.")


@db.command()
def status():
    """Show migration status."""
    from ..migrations import migration_status

    status = migration_status()
    click.echo(f"Current version: {status['current_version']}")
    click.echo(f"Latest version: {status['latest_version']}")
    click.echo(f"Pending: {status['pending_count']}")

    if status["pending"]:
        click.echo("\nPending migrations:")
        for m in status["pending"]:
            click.echo(f"  {m['version']}: {m['name']}")


@db.command()
@click.argument("version", type=int)
def rollback(version: int):
    """Rollback to specific version."""
    from ..migrations import rollback as do_rollback

    click.echo(f"Rolling back to version {version}...")
    applied = do_rollback(version)
    for name in applied:
        click.echo(f"  {name}")
    click.echo("Done.")
```

---

## 2. BACKUP & RECOVERY

### Create Backup Service

**File:** `src/ybis/services/backup.py`

```python
"""
Backup Service - Data backup and recovery.

Supports:
- SQLite database backup
- Vector store backup
- Configuration backup
- Workspace artifacts backup
"""

import gzip
import json
import logging
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class BackupService:
    """Handles backup and recovery operations."""

    def __init__(self, backup_dir: Path | None = None):
        from ..constants import PROJECT_ROOT
        self.project_root = PROJECT_ROOT
        self.backup_dir = backup_dir or (PROJECT_ROOT / "backups")
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(self, include_workspaces: bool = False) -> Path:
        """
        Create full system backup.

        Args:
            include_workspaces: Include workspace artifacts

        Returns:
            Path to backup directory
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}"
        backup_path.mkdir(parents=True, exist_ok=True)

        manifest = {
            "timestamp": timestamp,
            "created_at": datetime.now().isoformat(),
            "components": [],
        }

        # Backup database
        db_backup = self._backup_database(backup_path)
        if db_backup:
            manifest["components"].append({"type": "database", "path": str(db_backup)})

        # Backup configs
        config_backup = self._backup_configs(backup_path)
        if config_backup:
            manifest["components"].append({"type": "configs", "path": str(config_backup)})

        # Backup vector store
        vector_backup = self._backup_vector_store(backup_path)
        if vector_backup:
            manifest["components"].append({"type": "vector_store", "path": str(vector_backup)})

        # Backup workspaces (optional)
        if include_workspaces:
            workspace_backup = self._backup_workspaces(backup_path)
            if workspace_backup:
                manifest["components"].append({"type": "workspaces", "path": str(workspace_backup)})

        # Write manifest
        manifest_path = backup_path / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, indent=2))

        # Journal event
        try:
            from ..syscalls.journal import append_event
            append_event(
                self.project_root / "platform_data",
                "BACKUP_CREATED",
                {
                    "backup_path": str(backup_path),
                    "components": len(manifest["components"]),
                    "include_workspaces": include_workspaces,
                },
            )
        except Exception:
            pass

        logger.info(f"Backup created: {backup_path}")
        return backup_path

    def _backup_database(self, backup_path: Path) -> Path | None:
        """Backup SQLite database."""
        db_path = self.project_root / "platform_data" / "control_plane.db"
        if not db_path.exists():
            return None

        backup_file = backup_path / "control_plane.db.gz"

        # Use SQLite backup API for consistency
        source = sqlite3.connect(db_path)
        temp_backup = backup_path / "control_plane.db"
        dest = sqlite3.connect(temp_backup)
        source.backup(dest)
        dest.close()
        source.close()

        # Compress
        with open(temp_backup, "rb") as f_in:
            with gzip.open(backup_file, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        temp_backup.unlink()

        logger.debug(f"Database backup: {backup_file}")
        return backup_file

    def _backup_configs(self, backup_path: Path) -> Path | None:
        """Backup configuration files."""
        configs_dir = self.project_root / "configs"
        if not configs_dir.exists():
            return None

        backup_file = backup_path / "configs.tar.gz"
        shutil.make_archive(
            str(backup_file).replace(".tar.gz", ""),
            "gztar",
            configs_dir,
        )

        logger.debug(f"Configs backup: {backup_file}")
        return backup_file

    def _backup_vector_store(self, backup_path: Path) -> Path | None:
        """Backup ChromaDB vector store."""
        chroma_dir = self.project_root / ".chroma"
        if not chroma_dir.exists():
            return None

        backup_file = backup_path / "chroma.tar.gz"
        shutil.make_archive(
            str(backup_file).replace(".tar.gz", ""),
            "gztar",
            chroma_dir,
        )

        logger.debug(f"Vector store backup: {backup_file}")
        return backup_file

    def _backup_workspaces(self, backup_path: Path) -> Path | None:
        """Backup workspace artifacts only (not full worktrees)."""
        workspaces_dir = self.project_root / "workspaces"
        if not workspaces_dir.exists():
            return None

        artifacts_backup = backup_path / "workspace_artifacts"
        artifacts_backup.mkdir(parents=True, exist_ok=True)

        # Only backup artifacts directories
        for workspace in workspaces_dir.iterdir():
            if workspace.is_dir():
                for run_dir in (workspace / "runs").glob("*/artifacts"):
                    if run_dir.exists():
                        dest = artifacts_backup / workspace.name / run_dir.parent.name / "artifacts"
                        shutil.copytree(run_dir, dest)

        # Compress
        backup_file = backup_path / "workspace_artifacts.tar.gz"
        shutil.make_archive(
            str(backup_file).replace(".tar.gz", ""),
            "gztar",
            artifacts_backup,
        )
        shutil.rmtree(artifacts_backup)

        logger.debug(f"Workspaces backup: {backup_file}")
        return backup_file

    def restore_backup(self, backup_path: Path, components: list[str] | None = None) -> dict:
        """
        Restore from backup.

        Args:
            backup_path: Path to backup directory
            components: List of components to restore (None = all)

        Returns:
            Restoration summary
        """
        manifest_path = backup_path / "manifest.json"
        if not manifest_path.exists():
            raise ValueError(f"Invalid backup: no manifest at {backup_path}")

        manifest = json.loads(manifest_path.read_text())
        restored = []

        for component in manifest["components"]:
            comp_type = component["type"]
            comp_path = backup_path / Path(component["path"]).name

            if components and comp_type not in components:
                continue

            if comp_type == "database":
                self._restore_database(comp_path)
                restored.append(comp_type)
            elif comp_type == "configs":
                self._restore_configs(comp_path)
                restored.append(comp_type)
            elif comp_type == "vector_store":
                self._restore_vector_store(comp_path)
                restored.append(comp_type)

        # Journal event
        try:
            from ..syscalls.journal import append_event
            append_event(
                self.project_root / "platform_data",
                "BACKUP_RESTORED",
                {
                    "backup_path": str(backup_path),
                    "restored_components": restored,
                },
            )
        except Exception:
            pass

        logger.info(f"Restored {len(restored)} components from {backup_path}")
        return {"restored": restored, "backup_timestamp": manifest["timestamp"]}

    def _restore_database(self, backup_file: Path):
        """Restore database from backup."""
        db_path = self.project_root / "platform_data" / "control_plane.db"

        # Decompress
        temp_db = backup_file.parent / "temp_restore.db"
        with gzip.open(backup_file, "rb") as f_in:
            with open(temp_db, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Replace current db
        if db_path.exists():
            db_path.unlink()
        shutil.move(temp_db, db_path)

    def _restore_configs(self, backup_file: Path):
        """Restore configs from backup."""
        configs_dir = self.project_root / "configs"
        if configs_dir.exists():
            shutil.rmtree(configs_dir)
        shutil.unpack_archive(backup_file, configs_dir)

    def _restore_vector_store(self, backup_file: Path):
        """Restore vector store from backup."""
        chroma_dir = self.project_root / ".chroma"
        if chroma_dir.exists():
            shutil.rmtree(chroma_dir)
        shutil.unpack_archive(backup_file, chroma_dir)

    def list_backups(self) -> list[dict]:
        """List available backups."""
        backups = []
        for backup_dir in sorted(self.backup_dir.glob("backup_*"), reverse=True):
            manifest_path = backup_dir / "manifest.json"
            if manifest_path.exists():
                manifest = json.loads(manifest_path.read_text())
                backups.append({
                    "path": str(backup_dir),
                    "timestamp": manifest["timestamp"],
                    "created_at": manifest["created_at"],
                    "components": [c["type"] for c in manifest["components"]],
                })
        return backups

    def cleanup_old_backups(self, keep_count: int = 5):
        """Remove old backups, keeping most recent."""
        backups = self.list_backups()
        for backup in backups[keep_count:]:
            shutil.rmtree(backup["path"])
            logger.info(f"Removed old backup: {backup['path']}")
```

### CLI Commands

**Add to:** `src/ybis/cli/__init__.py`

```python
@cli.group()
def backup():
    """Backup and recovery commands."""
    pass


@backup.command()
@click.option("--include-workspaces", is_flag=True, help="Include workspace artifacts")
def create(include_workspaces: bool):
    """Create a backup."""
    from ..services.backup import BackupService

    service = BackupService()
    path = service.create_backup(include_workspaces=include_workspaces)
    click.echo(f"Backup created: {path}")


@backup.command()
def list():
    """List available backups."""
    from ..services.backup import BackupService

    service = BackupService()
    backups = service.list_backups()

    if not backups:
        click.echo("No backups found.")
        return

    for b in backups:
        click.echo(f"{b['timestamp']} - {', '.join(b['components'])}")


@backup.command()
@click.argument("backup_path", type=click.Path(exists=True))
@click.option("--component", multiple=True, help="Specific component to restore")
def restore(backup_path: str, component: tuple):
    """Restore from backup."""
    from pathlib import Path
    from ..services.backup import BackupService

    service = BackupService()
    components = list(component) if component else None
    result = service.restore_backup(Path(backup_path), components)
    click.echo(f"Restored: {', '.join(result['restored'])}")


@backup.command()
@click.option("--keep", default=5, help="Number of backups to keep")
def cleanup(keep: int):
    """Remove old backups."""
    from ..services.backup import BackupService

    service = BackupService()
    service.cleanup_old_backups(keep_count=keep)
    click.echo(f"Cleanup complete. Kept {keep} most recent backups.")
```

---

## 3. WORKTREE FILE SYNC FIX

### Problem
Git worktree only contains committed files. Uncommitted changes are not available.

### Solution: Pre-sync uncommitted files

**File:** `src/ybis/data_plane/git_workspace.py`

Add this function and modify `init_git_worktree`:

```python
def _sync_uncommitted_files(worktree_path: Path, project_root: Path) -> list[str]:
    """
    Sync uncommitted/untracked files from project root to worktree.

    This ensures files that haven't been committed yet are available
    in the worktree for execution.

    Args:
        worktree_path: Path to worktree
        project_root: Main project root

    Returns:
        List of synced file paths
    """
    import shutil
    from git import Repo

    synced = []
    repo = Repo(project_root)

    # Get untracked files
    untracked = repo.untracked_files

    # Get modified but uncommitted files
    modified = [item.a_path for item in repo.index.diff(None)]

    # Get staged but uncommitted files
    staged = [item.a_path for item in repo.index.diff("HEAD")]

    all_uncommitted = set(untracked + modified + staged)

    for file_path in all_uncommitted:
        source = project_root / file_path
        dest = worktree_path / file_path

        if source.exists() and source.is_file():
            # Skip large files and non-essential
            if source.stat().st_size > 10 * 1024 * 1024:  # 10MB
                continue

            # Skip virtual env and cache
            skip_patterns = [".venv", "__pycache__", ".git", "node_modules", ".chroma"]
            if any(p in str(file_path) for p in skip_patterns):
                continue

            # Copy file
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            synced.append(file_path)

    return synced


def init_git_worktree(
    task_id: str, run_id: str, run_path: Path, trace_id: str | None = None
) -> Path:
    """
    Create git worktree for isolated execution.

    UPDATED: Now syncs uncommitted files after worktree creation.
    """
    try:
        from git import GitCommandError, Repo
    except ImportError:
        raise ImportError(
            "GitPython not installed. Install with: pip install GitPython"
        )

    repo = Repo(PROJECT_ROOT)
    if not repo.git_dir:
        run_path.mkdir(parents=True, exist_ok=True)
        return run_path

    branch_name = f"task-{task_id}-run-{run_id}"

    try:
        branch_exists = any(head.name == branch_name for head in repo.heads)
        if branch_exists:
            repo.git.worktree("add", str(run_path), branch_name)
        else:
            repo.git.worktree("add", "-b", branch_name, str(run_path))

        # NEW: Sync uncommitted files
        synced_files = _sync_uncommitted_files(run_path, PROJECT_ROOT)

        # Journal events
        from ..syscalls.journal import append_event
        append_event(
            run_path,
            "GIT_WORKTREE_CREATED",
            {
                "branch_name": branch_name,
                "worktree_path": str(run_path),
                "task_id": task_id,
                "run_id": run_id,
            },
            trace_id=trace_id,
        )

        if synced_files:
            append_event(
                run_path,
                "WORKTREE_FILES_SYNCED",
                {
                    "synced_count": len(synced_files),
                    "files": synced_files[:20],  # First 20 for log
                },
                trace_id=trace_id,
            )

        return run_path

    except GitCommandError as e:
        # ... existing error handling ...
```

### Alternative: LocalCoder PROJECT_ROOT Fallback

**File:** `src/ybis/adapters/local_coder.py`

Modify file reading to check PROJECT_ROOT if not in worktree:

```python
def generate_code(self, ctx: RunContext, plan: Plan, error_context: str | None = None) -> ExecutorReport:
    # ... existing code ...

    for file_path_str in validated_files:
        try:
            file_path = Path(file_path_str)

            if file_path.is_absolute():
                try:
                    relative_path = file_path.relative_to(PROJECT_ROOT)
                    file_path = (code_root / relative_path).resolve()
                except ValueError:
                    file_path = file_path.resolve()
            else:
                file_path = (code_root / file_path).resolve()

            # Read current file content
            # NEW: Fallback to PROJECT_ROOT if not in worktree
            if file_path.exists():
                current_content = file_path.read_text(encoding="utf-8")
            else:
                # Try reading from PROJECT_ROOT
                project_file = PROJECT_ROOT / file_path_str
                if project_file.exists():
                    current_content = project_file.read_text(encoding="utf-8")
                    logger.info(f"File not in worktree, read from PROJECT_ROOT: {file_path_str}")

                    # Also copy to worktree for consistency
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    file_path.write_text(current_content, encoding="utf-8")

                    # Journal event
                    from ..syscalls.journal import append_event
                    append_event(
                        ctx.run_path,
                        "FILE_SYNCED_FROM_PROJECT_ROOT",
                        {
                            "file": file_path_str,
                            "content_length": len(current_content),
                        },
                        trace_id=ctx.trace_id,
                    )
                else:
                    current_content = ""
                    logger.warning(f"File not found in worktree or PROJECT_ROOT: {file_path_str}")

            # ... rest of existing code ...
```

---

## Files to Create

| File | Purpose |
|------|---------|
| `src/ybis/migrations/base.py` | Migration runner |
| `src/ybis/migrations/__init__.py` | Migration registry |
| `src/ybis/migrations/versions/001_initial_schema.py` | Initial schema |
| `src/ybis/migrations/versions/002_add_error_knowledge_base.py` | Error KB tables |
| `src/ybis/migrations/versions/003_add_lessons_table.py` | Lessons table |
| `src/ybis/migrations/versions/004_add_metrics_table.py` | Metrics table |
| `src/ybis/services/backup.py` | Backup service |

## Files to Modify

| File | Change |
|------|--------|
| `src/ybis/cli/__init__.py` | ADD - `db` and `backup` command groups |
| `src/ybis/data_plane/git_workspace.py` | ADD - `_sync_uncommitted_files`, modify `init_git_worktree` |
| `src/ybis/adapters/local_coder.py` | ADD - PROJECT_ROOT fallback for file reading |

---

## Verification

```bash
# Test migrations
ybis db status
ybis db migrate

# Test backup
ybis backup create
ybis backup list
ybis backup restore backups/backup_YYYYMMDD_HHMMSS

# Test worktree sync
git status  # Should show uncommitted files
python scripts/ybis_run.py TEST-SYNC --workflow default
ls workspaces/TEST-SYNC/runs/*/src/ybis/  # Should have files
```

---

## Success Criteria

- [ ] Migrations system working
- [ ] All tables have migrations
- [ ] Backup creates valid archives
- [ ] Restore recovers data correctly
- [ ] Worktree contains uncommitted files
- [ ] LocalCoder reads from PROJECT_ROOT if needed
