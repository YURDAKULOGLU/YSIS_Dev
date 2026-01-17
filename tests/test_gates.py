"""
Tests for Deterministic Gates.

DoD:
- Unit test: Small patch passes
- Unit test: Large patch returns REQUIRE_APPROVAL
- Unit test: Core changes return REQUIRE_APPROVAL
"""

import tempfile
from pathlib import Path

import pytest

from src.ybis.contracts import GateDecision, RunContext, VerifierReport
from src.ybis.orchestrator.gates import check_risk_gate, check_verification_gate


def test_verification_gate_pass():
    """Test that verification gate passes when all checks pass."""
    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir) / "runs" / "R-001"
        run_path.mkdir(parents=True)
        (run_path / "journal").mkdir()

        ctx = RunContext(
            task_id="T-001",
            run_id="R-001",
            run_path=run_path,
            trace_id="trace-T-001-R-001",
        )

        verifier_report = VerifierReport(
            task_id="T-001",
            run_id="R-001",
            lint_passed=True,
            tests_passed=True,
            coverage=0.85,
        )

        gate_report = check_verification_gate(verifier_report, ctx)

        assert gate_report.decision == GateDecision.PASS
        assert gate_report.risk_score == 0


def test_verification_gate_block():
    """Test that verification gate blocks when checks fail."""
    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir) / "runs" / "R-001"
        run_path.mkdir(parents=True)
        (run_path / "journal").mkdir()

        ctx = RunContext(
            task_id="T-001",
            run_id="R-001",
            run_path=run_path,
            trace_id="trace-T-001-R-001",
        )

        verifier_report = VerifierReport(
            task_id="T-001",
            run_id="R-001",
            lint_passed=False,
            tests_passed=True,
            coverage=0.85,
        )

        gate_report = check_verification_gate(verifier_report, ctx)

        assert gate_report.decision == GateDecision.BLOCK
        assert gate_report.risk_score == 100
        assert "Lint checks failed" in gate_report.reasons


def test_risk_gate_small_patch():
    """Test that small patch passes risk gate."""
    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir) / "runs" / "R-001"
        run_path.mkdir(parents=True)
        (run_path / "journal").mkdir()

        ctx = RunContext(
            task_id="T-001",
            run_id="R-001",
            run_path=run_path,
            trace_id="trace-T-001-R-001",
        )

        gate_report = check_risk_gate(ctx, patch_size=50, changed_files=["tests/test_file.py"])

        assert gate_report.decision == GateDecision.PASS
        assert gate_report.risk_score < 50


def test_risk_gate_large_patch():
    """Test that large patch requires approval."""
    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir) / "runs" / "R-001"
        run_path.mkdir(parents=True)
        (run_path / "journal").mkdir()

        ctx = RunContext(
            task_id="T-001",
            run_id="R-001",
            run_path=run_path,
            trace_id="trace-T-001-R-001",
        )

        gate_report = check_risk_gate(ctx, patch_size=150, changed_files=["tests/test_file.py"])

        assert gate_report.decision == GateDecision.REQUIRE_APPROVAL
        assert gate_report.approval_required is True
        assert "Large patch size" in gate_report.reasons[0]


def test_risk_gate_core_changes():
    """Test that core changes require approval regardless of size."""
    with tempfile.TemporaryDirectory() as tmpdir:
        run_path = Path(tmpdir) / "runs" / "R-001"
        run_path.mkdir(parents=True)
        (run_path / "journal").mkdir()

        ctx = RunContext(
            task_id="T-001",
            run_id="R-001",
            run_path=run_path,
            trace_id="trace-T-001-R-001",
        )

        gate_report = check_risk_gate(
            ctx, patch_size=10, changed_files=["src/ybis/contracts/resources.py"]
        )

        assert gate_report.decision == GateDecision.REQUIRE_APPROVAL
        assert gate_report.approval_required is True
        assert "protected paths" in gate_report.reasons[0].lower()
        assert len(gate_report.protected_paths_touched) > 0

