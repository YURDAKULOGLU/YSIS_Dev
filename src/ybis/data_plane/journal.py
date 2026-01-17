"""
Journal writer - Append-only event logging.
"""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class JournalWriter:
    """Append-only journal writer for events.jsonl."""

    def __init__(self, journal_path: Path):
        """
        Initialize journal writer.

        Args:
            journal_path: Path to events.jsonl file
        """
        self.journal_path = journal_path
        # Ensure parent directory exists
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)

    def append_event(self, event: dict[str, Any]) -> None:
        """
        Append event to journal (atomic write).

        Args:
            event: Event dictionary to append
        """
        # Atomic write: open in append mode, write, close
        with open(self.journal_path, "a", encoding="utf-8") as f:
            json_line = json.dumps(event, ensure_ascii=False)
            f.write(json_line + "\n")
            f.flush()  # Ensure data is written immediately

