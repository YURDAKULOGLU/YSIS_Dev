"""
Tests for Aider Adapter.

DoD:
- Unit test with mocked syscalls.exec verifies correct command construction
- Unit test verifies report generation from dummy stdout
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.ybis.adapters.aider import AiderExecutor
from src.ybis.contracts import Plan, RunContext


def test_aider_command_construction():
    """Test that Aider command is constructed correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir) / "runs" / "R-001"
        run_path.mkdir(parents=True)
        (run_path / "journal").mkdir()

        ctx = RunContext(
            task_id="T-001",
            run_id="R-001",
            run_path=run_path,
        )

        plan = Plan(
            objective="Fix typo in hello.py",
            files=["hello.py"],
        )

        executor = AiderExecutor(aider_path="aider")

        # Mock run_command
        with patch("src.ybis.adapters.aider.run_command") as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = "Modified: hello.py"
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            report = executor.generate_code(ctx, plan)

            # Verify command was constructed correctly
            mock_run.assert_called_once()
            call_args = mock_run.call_args[0]
            cmd = call_args[0]

            assert "aider" in cmd
            assert "--message" in cmd
            assert "Fix typo in hello.py" in cmd
            assert "hello.py" in cmd
            assert "--yes" in cmd

            # Verify report
            assert report.success is True
            assert "hello.py" in report.files_changed


def test_aider_report_generation():
    """Test that ExecutorReport is generated from Aider output."""
    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir) / "runs" / "R-001"
        run_path.mkdir(parents=True)
        (run_path / "journal").mkdir()

        ctx = RunContext(
            task_id="T-001",
            run_id="R-001",
            run_path=run_path,
        )

        plan = Plan(objective="Add function")

        executor = AiderExecutor()

        # Mock run_command with realistic output
        with patch("src.ybis.adapters.aider.run_command") as mock_run:
            mock_result = MagicMock()
            mock_result.returncode = 0
            mock_result.stdout = """
Modified: src/utils.py
Added function calculate_sum()
"""
            mock_result.stderr = ""
            mock_run.return_value = mock_result

            report = executor.generate_code(ctx, plan)

            # Verify report structure
            assert isinstance(report.success, bool)
            assert report.success is True
            assert len(report.files_changed) > 0
            assert "src/utils.py" in report.files_changed or "utils.py" in report.files_changed
            assert len(report.commands_run) > 0
            assert "aider" in report.commands_run[0]


def test_aider_error_handling():
    """Test that errors are handled correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir) / "runs" / "R-001"
        run_path.mkdir(parents=True)
        (run_path / "journal").mkdir()

        ctx = RunContext(
            task_id="T-001",
            run_id="R-001",
            run_path=run_path,
        )

        plan = Plan(objective="Fix bug")

        executor = AiderExecutor()

        # Mock run_command to raise exception
        with patch("src.ybis.adapters.aider.run_command") as mock_run:
            mock_run.side_effect = Exception("Command not found")

            report = executor.generate_code(ctx, plan)

            # Verify error is captured
            assert report.success is False
            assert report.error is not None
            assert "Command not found" in report.error

