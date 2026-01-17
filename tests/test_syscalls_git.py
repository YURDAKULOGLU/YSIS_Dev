"""
Tests for Syscall Git operations.

DoD:
- Methods work and record events
"""

import json
import subprocess
import tempfile
from pathlib import Path

import pytest

from src.ybis.contracts import RunContext
from src.ybis.syscalls.git import commit, get_diff


def test_git_get_diff():
    """Test that get_diff works and doesn't fail."""
    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir) / "runs" / "R-001"
        run_path.mkdir(parents=True)

        # Initialize git repo
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True, check=False)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True, check=False)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True, check=False)

        ctx = RunContext(
            task_id="T-001",
            run_id="R-001",
            run_path=run_path,
        )

        # Get diff (should work even if empty)
        diff = get_diff(ctx, cwd=Path(tmpdir))
        assert isinstance(diff, str), "Diff should return string"


def test_git_commit():
    """Test that commit works and records event."""
    import subprocess

    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir) / "runs" / "R-001"
        run_path.mkdir(parents=True)
        (run_path / "journal").mkdir()

        # Initialize git repo
        subprocess.run(["git", "init"], cwd=tmpdir, capture_output=True, check=False)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=tmpdir, capture_output=True, check=False)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=tmpdir, capture_output=True, check=False)

        # Create a file and add it
        test_file = Path(tmpdir) / "test.txt"
        test_file.write_text("test content")
        subprocess.run(["git", "add", "test.txt"], cwd=tmpdir, capture_output=True, check=False)

        ctx = RunContext(
            task_id="T-001",
            run_id="R-001",
            run_path=run_path,
        )

        # Commit
        commit("Test commit", "Test Author", ctx, cwd=Path(tmpdir))

        # Verify event was recorded
        journal_path = run_path / "journal" / "events.jsonl"
        assert journal_path.exists(), "Journal file should exist"

        lines = journal_path.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 1, "Journal should have 1 event"

        event = json.loads(lines[0])
        assert event["event_type"] == "GIT_COMMIT"
        assert event["message"] == "Test commit"
        assert event["author"] == "Test Author"

