"""
Tests for Data Plane - Workspace and Journaling.

DoD:
- Unit test creates a folder structure
- Unit test appends 3 events and verifies events.jsonl has 3 lines
"""

import json
import tempfile
from pathlib import Path

import pytest

from src.ybis.constants import ARTIFACTS_DIR, JOURNAL_DIR
from src.ybis.data_plane import JournalWriter, init_run_structure


def test_init_run_structure():
    """Test that run structure is created correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock PROJECT_ROOT
        import src.ybis.data_plane.workspace as ws_module

        original_root = ws_module.PROJECT_ROOT
        ws_module.PROJECT_ROOT = Path(tmpdir)

        try:
            task_id = "T-001"
            run_id = "R-001"

            run_path = init_run_structure(task_id, run_id)

            # Verify structure
            assert run_path.exists(), "Run directory should exist"
            assert (run_path / ARTIFACTS_DIR).exists(), "Artifacts directory should exist"
            assert (run_path / JOURNAL_DIR).exists(), "Journal directory should exist"

            # Verify path structure
            assert run_path.name == run_id
            assert run_path.parent.name == "runs"
            assert run_path.parent.parent.name == task_id
        finally:
            ws_module.PROJECT_ROOT = original_root


def test_journal_writer_append():
    """Test that journal writer appends events correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        journal_path = Path(tmpdir) / "events.jsonl"
        writer = JournalWriter(journal_path)

        # Append 3 events
        writer.append_event({"event_type": "TEST", "data": "event1"})
        writer.append_event({"event_type": "TEST", "data": "event2"})
        writer.append_event({"event_type": "TEST", "data": "event3"})

        # Verify file has 3 lines
        assert journal_path.exists(), "Journal file should exist"

        lines = journal_path.read_text(encoding="utf-8").strip().split("\n")
        assert len(lines) == 3, f"Journal should have 3 lines, got {len(lines)}"

        # Verify each line is valid JSON
        for i, line in enumerate(lines, 1):
            event = json.loads(line)
            assert event["event_type"] == "TEST"
            assert event["data"] == f"event{i}"

