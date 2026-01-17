#!/usr/bin/env python3
"""
End-to-End Smoke Test for Aider Capability.

Tests that the system can actually modify a file using Aider.

DoD:
- Script passes (requires Aider to be installed/functional in environment)
"""

import json
import os
import sys
import tempfile
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.contracts import Plan, RunContext, Task
from src.ybis.control_plane import ControlPlaneDB
from src.ybis.data_plane import init_run_structure
from src.ybis.orchestrator import build_workflow_graph


def test_aider_capability() -> None:
    """Test that Aider can modify a file."""
    # Check if Aider is available
    import subprocess

    try:
        result = subprocess.run(
            ["aider", "--version"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        aider_available = result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        aider_available = False

    if not aider_available:
        print("SKIP: Aider not available in environment")
        print("Install Aider with: pip install aider-chat")
        return

    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock PROJECT_ROOT
        import src.ybis.data_plane.workspace as ws_module

        original_root = ws_module.PROJECT_ROOT
        ws_module.PROJECT_ROOT = Path(tmpdir)

        try:
            # Create test file with typo
            test_file = Path(tmpdir) / "hello.py"
            test_file.write_text('print("helo")\n')

            # Create task
            task_id = "T-TEST-001"
            run_id = "R-TEST-001"

            # Initialize workspace (with git worktree if available)
            run_path = init_run_structure(task_id, run_id, use_git_worktree=True)

            # Create plan
            ctx = RunContext(
                task_id=task_id,
                run_id=run_id,
                run_path=run_path,
            )

            plan_data = {
                "task_id": task_id,
                "run_id": run_id,
                "objective": "Fix typo: change 'helo' to 'hello'",
                "files": [str(test_file)],
            }

            from src.ybis.syscalls import write_file

            write_file(ctx.plan_path, json.dumps(plan_data, indent=2), ctx)

            # Enable Aider
            os.environ["YBIS_AIDER_ENABLED"] = "true"

            # Build and run graph
            graph = build_workflow_graph()

            initial_state = {
                "task_id": task_id,
                "run_id": run_id,
                "run_path": run_path,
                "status": "pending",
            }

            print("Running workflow with Aider...")
            final_state = graph.invoke(initial_state)

            # Verify file was modified
            file_content = test_file.read_text()
            assert "hello" in file_content, f"Expected 'hello' in file, got: {file_content}"
            assert "helo" not in file_content, f"Typo 'helo' should be fixed, got: {file_content}"

            print("✓ Test passed: File was modified correctly")
            print(f"  Final content: {file_content.strip()}")

        finally:
            ws_module.PROJECT_ROOT = original_root
            os.environ.pop("YBIS_AIDER_ENABLED", None)


if __name__ == "__main__":
    test_aider_capability()

