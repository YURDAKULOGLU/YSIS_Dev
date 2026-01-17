"""
Tests for Syscall Exec operations.

DoD:
- run_command(["rm", "-rf", "/"]) fails (not in allowlist)
- run_command(["ls"]) succeeds and records event
"""

import json
import tempfile
from pathlib import Path

import pytest

from src.ybis.contracts import RunContext
from src.ybis.syscalls.exec import run_command


def test_run_command_not_allowed():
    """Test that run_command fails for non-allowlisted commands."""
    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir) / "runs" / "R-001"
        run_path.mkdir(parents=True)
        (run_path / "journal").mkdir()

        ctx = RunContext(
            task_id="T-001",
            run_id="R-001",
            run_path=run_path,
        )

        # Try to run non-allowlisted command
        with pytest.raises(PermissionError, match="not in allowlist"):
            run_command(["rm", "-rf", "/"], ctx)


def test_run_command_success():
    """Test that run_command succeeds for allowlisted commands and records event."""
    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir) / "runs" / "R-001"
        run_path.mkdir(parents=True)
        (run_path / "journal").mkdir()

        ctx = RunContext(
            task_id="T-001",
            run_id="R-001",
            run_path=run_path,
        )

        # Run allowlisted command (ls on Windows, use dir or just test with python)
        import sys

        if sys.platform == "win32":
            # On Windows, use dir or python
            result = run_command([sys.executable, "-c", "print('test')"], ctx)
        else:
            result = run_command(["ls"], ctx)

        # Verify command succeeded
        assert result.returncode == 0, "Command should succeed"

        # Verify event was recorded
        journal_path = run_path / "journal" / "events.jsonl"
        assert journal_path.exists(), "Journal file should exist"

        lines = journal_path.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 1, "Journal should have 1 event"

        event = json.loads(lines[0])
        assert event["event_type"] == "COMMAND_EXEC"
        assert "command" in event
        assert "exit_code" in event

