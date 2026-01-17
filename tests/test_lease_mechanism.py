"""
Tests for Lease Mechanism.

DoD:
- Unit test: Two workers try to claim the same task; only one succeeds
- Unit test: Expired lease can be claimed by a new worker
"""

import asyncio
import tempfile
from pathlib import Path

import pytest

from src.ybis.control_plane import ControlPlaneDB
from src.ybis.contracts import Task


@pytest.mark.asyncio
async def test_claim_task_exclusive():
    """Test that two workers cannot claim the same task simultaneously."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = ControlPlaneDB(db_path)

        await db.initialize()

        # Create a task
        task = Task(
            task_id="T-001",
            title="Test Task",
            objective="Test objective",
            status="pending",
        )
        await db.register_task(task)

        # Worker 1 claims task
        claimed1 = await db.claim_task("T-001", "worker-1", duration_sec=300)
        assert claimed1 is True, "Worker 1 should successfully claim task"

        # Worker 2 tries to claim same task
        claimed2 = await db.claim_task("T-001", "worker-2", duration_sec=300)
        assert claimed2 is False, "Worker 2 should fail to claim task (already claimed)"

        # Release lease
        await db.release_lease("T-001", "worker-1")

        # Worker 2 should now be able to claim
        claimed2_after = await db.claim_task("T-001", "worker-2", duration_sec=300)
        assert claimed2_after is True, "Worker 2 should claim task after release"


@pytest.mark.asyncio
async def test_expired_lease_can_be_claimed():
    """Test that expired lease can be claimed by a new worker."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = ControlPlaneDB(db_path)

        await db.initialize()

        # Create a task
        task = Task(
            task_id="T-002",
            title="Test Task 2",
            objective="Test objective",
            status="pending",
        )
        await db.register_task(task)

        # Worker 1 claims with very short duration
        claimed1 = await db.claim_task("T-002", "worker-1", duration_sec=1)
        assert claimed1 is True, "Worker 1 should successfully claim task"

        # Wait for lease to expire
        await asyncio.sleep(2)

        # Worker 2 should now be able to claim (lease expired)
        claimed2 = await db.claim_task("T-002", "worker-2", duration_sec=300)
        assert claimed2 is True, "Worker 2 should claim task after lease expiration"


@pytest.mark.asyncio
async def test_heartbeat():
    """Test worker heartbeat mechanism."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        db = ControlPlaneDB(db_path)

        await db.initialize()

        # Send heartbeat
        await db.heartbeat("worker-1")

        # Verify worker exists in DB
        import aiosqlite

        async with aiosqlite.connect(db_path) as conn:
            conn.row_factory = aiosqlite.Row
            async with conn.execute("SELECT * FROM workers WHERE worker_id = ?", ("worker-1",)) as cursor:
                row = await cursor.fetchone()
                assert row is not None, "Worker should exist after heartbeat"
                assert row["worker_id"] == "worker-1"

