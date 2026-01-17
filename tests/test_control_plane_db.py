"""
Tests for Control Plane Database.

DoD:
- test_db_init passes (creates .db file)
- test_task_lifecycle passes (insert and select)
"""

import asyncio
import tempfile
from pathlib import Path

import pytest

from src.ybis.control_plane import ControlPlaneDB
from src.ybis.contracts import Run, Task


@pytest.mark.asyncio
async def test_db_init():
    """Test database initialization creates .db file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = ControlPlaneDB(db_path)

        # Initialize database
        await db.initialize()

        # Check that .db file exists
        assert db_path.exists(), "Database file should be created"


@pytest.mark.asyncio
async def test_task_lifecycle():
    """Test task insert and select."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = ControlPlaneDB(db_path)

        # Initialize database
        await db.initialize()

        # Create and register task
        task = Task(
            task_id="T-001",
            title="Test Task",
            objective="Test objective",
            status="pending",
        )
        await db.register_task(task)

        # Retrieve task
        retrieved = await db.get_task("T-001")

        # Verify
        assert retrieved is not None, "Task should be retrieved"
        assert retrieved.task_id == "T-001"
        assert retrieved.title == "Test Task"
        assert retrieved.objective == "Test objective"
        assert retrieved.status == "pending"
        assert retrieved.schema_version == 1


@pytest.mark.asyncio
async def test_run_lifecycle():
    """Test run insert and select."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = ControlPlaneDB(db_path)

        # Initialize database
        await db.initialize()

        # Create task first (foreign key constraint)
        task = Task(
            task_id="T-001",
            title="Test Task",
            objective="Test objective",
        )
        await db.register_task(task)

        # Create and register run
        run = Run(
            run_id="R-001",
            task_id="T-001",
            run_path="workspaces/T-001/runs/R-001",
            status="pending",
        )
        await db.register_run(run)

        # Retrieve run
        retrieved = await db.get_run("R-001")

        # Verify
        assert retrieved is not None, "Run should be retrieved"
        assert retrieved.run_id == "R-001"
        assert retrieved.task_id == "T-001"
        assert retrieved.status == "pending"
        assert retrieved.schema_version == 1

