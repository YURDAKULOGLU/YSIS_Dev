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

