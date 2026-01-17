"""
Tests for Syscall FS operations.

DoD:
- write_file fails if trying to overwrite src/ybis/constants.py
- write_file succeeds elsewhere and an event is seen in events.jsonl
"""

import json
import tempfile
from pathlib import Path

import pytest

from src.ybis.contracts import RunContext
from src.ybis.syscalls.fs import write_file


def test_write_file_protected_path():
    """Test that write_file fails for protected paths."""
    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir) / "runs" / "R-001"
        run_path.mkdir(parents=True)

        ctx = RunContext(
            task_id="T-001",
            run_id="R-001",
            run_path=run_path,
        )

        # Try to write to protected path (use absolute path)
        from src.ybis.constants import PROJECT_ROOT

        protected_path = PROJECT_ROOT / "src" / "ybis" / "constants.py"

        with pytest.raises(PermissionError, match="Protected path"):
            write_file(protected_path, "test content", ctx)


def test_write_file_success():
    """Test that write_file succeeds for non-protected paths and records event."""
    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir) / "runs" / "R-001"
        run_path.mkdir(parents=True)
        (run_path / "journal").mkdir()

        ctx = RunContext(
            task_id="T-001",
            run_id="R-001",
            run_path=run_path,
        )

        # Write to non-protected path
        test_file = Path(tmpdir) / "test_file.txt"
        content = "test content"

        write_file(test_file, content, ctx)

        # Verify file was written
        assert test_file.exists(), "File should be created"
        assert test_file.read_text() == content, "File content should match"

        # Verify event was recorded
        journal_path = run_path / "journal" / "events.jsonl"
        assert journal_path.exists(), "Journal file should exist"

        lines = journal_path.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 1, "Journal should have 1 event"

        event = json.loads(lines[0])
        assert event["event_type"] == "FILE_WRITE"
        # Check payload structure
        payload = event.get("payload", {})
        assert "path" in payload or "path" in event, "Path should be in event"
        path_value = payload.get("path") or event.get("path")
        assert str(test_file) in str(path_value), f"Path should match: {path_value}"
        assert payload.get("content_length") == len(content) or event.get("content_length") == len(content)

