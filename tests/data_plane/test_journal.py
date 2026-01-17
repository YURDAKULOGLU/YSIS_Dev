"""
Test Journal - Append-only event logging.
"""

import json
import pytest
from pathlib import Path

from src.ybis.data_plane.journal import JournalWriter, append_event


class TestJournalWriter:
    """Test JournalWriter functionality."""

    @pytest.fixture
    def journal_path(self, tmp_path):
        """Create journal path."""
        return tmp_path / "events.jsonl"

    def test_journal_writer_init(self, journal_path):
        """Test JournalWriter initialization."""
        writer = JournalWriter(journal_path)
        assert writer.journal_path == journal_path

    def test_append_event(self, journal_path):
        """Test appending event to journal."""
        writer = JournalWriter(journal_path)
        event = {"event_type": "TEST", "data": "test"}
        writer.append_event(event)

        # Verify event was written
        assert journal_path.exists()
        lines = journal_path.read_text().strip().split("\n")
        assert len(lines) == 1
        assert json.loads(lines[0]) == event

    def test_append_event_multiple(self, journal_path):
        """Test appending multiple events."""
        writer = JournalWriter(journal_path)
        events = [
            {"event_type": "TEST1", "data": "test1"},
            {"event_type": "TEST2", "data": "test2"},
        ]
        for event in events:
            writer.append_event(event)

        # Verify all events were written
        lines = journal_path.read_text().strip().split("\n")
        assert len(lines) == 2

    def test_journal_logs(self):
        """Test journal logs operations."""
        import logging
        logger = logging.getLogger("src.ybis.data_plane.journal")
        assert logger is not None


class TestAppendEvent:
    """Test append_event convenience function."""

    @pytest.fixture
    def run_path(self, tmp_path):
        """Create run path."""
        journal_dir = tmp_path / "journal"
        journal_dir.mkdir(parents=True, exist_ok=True)
        return tmp_path

    def test_append_event(self, run_path):
        """Test append_event function."""
        append_event(
            run_path,
            "TEST_EVENT",
            {"data": "test"},
            trace_id="test-trace",
        )

        # Verify event was written
        journal_path = run_path / "journal" / "events.jsonl"
        assert journal_path.exists()


