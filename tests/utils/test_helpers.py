"""Test helper utilities."""

import json
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock


def create_mock_llm_response(content: str) -> MagicMock:
    """Create mock LLM response.

    Args:
        content: Response content

    Returns:
        Mocked response object
    """
    mock = MagicMock()
    mock.choices = [MagicMock(message=MagicMock(content=content))]
    return mock


def create_mock_plan(
    files: list[str] | None = None,
    steps: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Create mock plan.

    Args:
        files: List of files
        steps: List of steps

    Returns:
        Plan dictionary
    """
    return {
        "files": files or ["src/main.py"],
        "steps": steps
        or [
            {"action": "read", "file": "src/main.py"},
            {"action": "edit", "file": "src/main.py", "instruction": "Fix bug"},
        ],
    }


def load_fixture(name: str) -> dict[str, Any]:
    """Load JSON fixture.

    Args:
        name: Fixture name (without extension)

    Returns:
        Parsed fixture data
    """
    fixture_path = Path(__file__).parent.parent / "fixtures" / f"{name}.json"
    return json.loads(fixture_path.read_text())


def assert_journal_has_event(
    journal_path: Path,
    event_type: str,
    payload_contains: dict[str, Any] | None = None,
) -> None:
    """Assert journal contains event.

    Args:
        journal_path: Path to journal directory
        event_type: Expected event type
        payload_contains: Expected payload keys/values
    """
    events_file = journal_path / "events.jsonl"
    assert events_file.exists(), f"Journal file not found: {events_file}"

    events = [
        json.loads(line)
        for line in events_file.read_text().strip().split("\n")
        if line
    ]

    matching = [e for e in events if e.get("event_type") == event_type]
    assert matching, f"No events of type {event_type} found"

    if payload_contains:
        for key, value in payload_contains.items():
            assert any(
                e.get("payload", {}).get(key) == value for e in matching
            ), f"No event with {key}={value} found"

