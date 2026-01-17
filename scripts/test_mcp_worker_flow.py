#!/usr/bin/env python3
"""
E2E External Worker Test - Verify MCP worker flow without internal worker.py.

Tests the entire flow:
1. Create a task via MCP
2. Claim it via MCP
3. Write an artifact via MCP
4. Complete it via MCP
"""

import asyncio
import json
import sys
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.constants import PROJECT_ROOT
from src.ybis.control_plane import ControlPlaneDB
from src.ybis.services.mcp_server import MCPServer


async def test_mcp_worker_flow() -> None:
    """Test the complete MCP worker flow."""
    # Use temporary directory for test
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock PROJECT_ROOT for this test
        original_root = PROJECT_ROOT
        try:
            from src.ybis import constants

            constants.PROJECT_ROOT = Path(tmpdir)

            # Initialize MCP server
            db_path = Path(tmpdir) / "platform_data" / "control_plane.db"
            server = MCPServer(db_path=str(db_path))
            await server.initialize()

            print("[1/4] Creating task via MCP...")
            task_result = await server.task_create(
                title="Test Task",
                objective="Test MCP worker flow",
                priority="MEDIUM",
            )
            task_id = task_result["task_id"]
            print(f"    Created task: {task_id}")

            # Verify task in DB
            db = ControlPlaneDB(db_path)
            task = await db.get_task(task_id)
            assert task is not None, "Task should exist in DB"
            assert task.status == "pending", "Task should be pending"
            print("    [OK] Task exists in DB")

            print("[2/4] Claiming task via MCP...")
            claim_result = await server.task_claim(worker_id="test-worker")
            assert claim_result.get("task") is not None or claim_result.get("task_id"), "Task should be claimed"
            claimed_task_id = claim_result.get("task_id") or claim_result.get("task", {}).get("task_id")
            assert claimed_task_id == task_id, "Claimed task should match created task"

            run_id = claim_result.get("run_id")
            assert run_id is not None, "Run ID should be returned"
            print(f"    Claimed task: {task_id}, run: {run_id}")

            # Verify lease in DB
            # Try to claim again with different worker - should fail
            claim_result_2 = await server.task_claim(worker_id="test-worker-2")
            # Should either return null or a different task
            if claim_result_2.get("task_id"):
                assert claim_result_2.get("task_id") != task_id, "Task should not be claimable by another worker"
            print("    [OK] Task lease is exclusive")

            print("[3/4] Writing artifact via MCP...")
            executor_report = {
                "task_id": task_id,
                "run_id": run_id,
                "success": True,
                "files_changed": ["test_file.py"],
                "commands_run": ["python test_file.py"],
                "outputs": {"python test_file.py": "Test output"},
                "error": None,
            }
            artifact_result = await server.artifact_write(
                run_id=run_id,
                name="executor_report.json",
                content=json.dumps(executor_report, indent=2),
            )
            assert "error" not in artifact_result, f"Artifact write should succeed: {artifact_result.get('error')}"
            assert artifact_result.get("status") == "written" or artifact_result.get("artifact_name"), "Artifact should be written"
            print(f"    Written artifact: {artifact_result.get('artifact_name', 'executor_report.json')}")

            # Verify artifact file exists
            artifact_path = Path(tmpdir) / "workspaces" / task_id / "runs" / run_id / "artifacts" / "executor_report.json"
            assert artifact_path.exists(), "Artifact file should exist"
            print("    [OK] Artifact file exists")

            # Verify journal event
            journal_path = Path(tmpdir) / "workspaces" / task_id / "runs" / run_id / "journal" / "events.jsonl"
            assert journal_path.exists(), "Journal file should exist"
            with open(journal_path, "r", encoding="utf-8") as f:
                events = [json.loads(line) for line in f if line.strip()]
            file_write_events = [e for e in events if e.get("event_type") == "FILE_WRITE"]
            assert len(file_write_events) > 0, "FILE_WRITE event should be recorded"
            print("    [OK] Journal event recorded")

            print("[4/4] Completing task via MCP...")
            complete_result = await server.task_complete(
                task_id=task_id,
                run_id=run_id,
                status="completed",
                result_summary="Test completed successfully",
                worker_id="test-worker",
            )
            assert complete_result.get("lease_released") is True, "Lease should be released"
            print(f"    Completed task: {task_id}")

            # Verify task status in DB
            updated_task = await db.get_task(task_id)
            assert updated_task is not None, "Task should still exist"
            assert updated_task.status == "completed", "Task status should be completed"
            print("    [OK] Task status updated in DB")

            # Verify run status
            run = await db.get_run(run_id)
            assert run is not None, "Run should exist"
            assert run.status == "completed", "Run status should be completed"
            print("    [OK] Run status updated in DB")

            print("\n[SUCCESS] All MCP worker flow tests passed!")
            print("External entities can successfully drive the platform via MCP.")

        finally:
            from src.ybis import constants

            constants.PROJECT_ROOT = original_root


if __name__ == "__main__":
    asyncio.run(test_mcp_worker_flow())

