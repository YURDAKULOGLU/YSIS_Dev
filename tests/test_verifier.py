"""
Tests for Verifier Adapter.

DoD:
- Verifier correctly identifies a syntax error (lint fail) or a failing test
- verifier_report.json schema matches contracts/evidence.py
"""

import json
import tempfile
from pathlib import Path

import pytest

from src.ybis.contracts import RunContext, VerifierReport
from src.ybis.orchestrator.verifier import run_verifier


def test_verifier_report_schema():
    """Test that verifier report schema matches contracts."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Mock PROJECT_ROOT
        import src.ybis.data_plane.workspace as ws_module

        original_root = ws_module.PROJECT_ROOT
        ws_module.PROJECT_ROOT = Path(tmpdir)

        try:
            run_path = Path(tmpdir) / "workspaces" / "T-001" / "runs" / "R-001"
            run_path.mkdir(parents=True)
            (run_path / "artifacts").mkdir()
            (run_path / "journal").mkdir()

            ctx = RunContext(
                task_id="T-001",
                run_id="R-001",
                run_path=run_path,
                trace_id="trace-T-001-R-001",
            )

            # Run verifier (will likely fail if ruff/pytest not available, but should still create report)
            report = run_verifier(ctx)

            # Verify report is valid VerifierReport
            assert isinstance(report, VerifierReport)
            assert report.task_id == "T-001"
            assert report.run_id == "R-001"
            assert isinstance(report.lint_passed, bool)
            assert isinstance(report.tests_passed, bool)
            assert isinstance(report.coverage, float)
            assert 0.0 <= report.coverage <= 1.0

            # Verify report file exists and is valid JSON
            assert ctx.verifier_report_path.exists()
            report_data = json.loads(ctx.verifier_report_path.read_text())
            assert "lint_passed" in report_data
            assert "tests_passed" in report_data
            assert "coverage" in report_data

            # Verify it can be deserialized back to VerifierReport
            loaded_report = VerifierReport(**report_data)
            assert loaded_report.task_id == report.task_id

        finally:
            ws_module.PROJECT_ROOT = original_root

