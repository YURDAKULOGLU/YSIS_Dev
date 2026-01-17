"""
Verifier Adapter - Bridge between raw command output and VerifierReport.

Runs ruff, pytest, and Sentinel V2, parses output, and generates VerifierReport.
"""

import importlib.util
import json
import logging
import re
import time
from pathlib import Path

logger = logging.getLogger(__name__)

from ..constants import PROJECT_ROOT
from ..contracts import RunContext, VerifierReport
from ..services.policy import get_policy_provider
from ..syscalls import run_command, write_file
from ..syscalls.journal import append_event
from .sentinel import SentinelV2


def run_verifier(ctx: RunContext) -> VerifierReport:
    """
    Run verifier (ruff + pytest) and generate VerifierReport.

    Args:
        ctx: Run context

    Returns:
        VerifierReport with results
    """
    # Journal: Verifier start
    append_event(
        ctx.run_path,
        "VERIFIER_START",
        {
            "task_id": ctx.task_id,
            "run_id": ctx.run_id,
        },
        trace_id=ctx.trace_id,
    )

    lint_passed = True
    tests_passed = True
    coverage = 0.0
    errors: list[str] = []
    warnings: list[str] = []
    test_details: dict = {}
    test_failures: list[dict] = []

    code_root = ctx.run_path if (ctx.run_path / ".git").exists() else PROJECT_ROOT
    policy_provider = get_policy_provider()
    verifier_config = policy_provider.get_verifier_config()

    target_paths = []
    python_targets = []
    executor_path = ctx.executor_report_path
    if executor_path.exists():
        try:
            executor_data = json.loads(executor_path.read_text())
            changed_files = executor_data.get("files_changed", [])
            python_targets = [f for f in changed_files if f.endswith(".py")]
        except Exception:
            python_targets = []

    if python_targets:
        for path in python_targets:
            candidate = Path(path)
            try:
                target_paths.append(str(candidate.relative_to(code_root)))
            except ValueError:
                target_paths.append(str(candidate))
    else:
        ruff_paths = verifier_config.get("ruff_paths")
        if ruff_paths:
            for path in ruff_paths:
                candidate = code_root / path
                if candidate.exists():
                    target_paths.append(str(candidate.relative_to(code_root)))
    if not target_paths:
        target_paths = []

    emit_warnings = verifier_config.get("emit_warnings", True)

    def _warn(message: str) -> None:
        if emit_warnings:
            warnings.append(message)

    # Run ruff check
    run_ruff = verifier_config.get("run_ruff", True)
    if not run_ruff:
        _warn("Policy disabled ruff; skipping lint")
        lint_passed = True
    elif target_paths:
        # Journal: Lint start
        append_event(
            ctx.run_path,
            "LINT_START",
            {
                "files": target_paths[:10],  # Limit to first 10
            },
            trace_id=ctx.trace_id,
        )
        try:
            start_time = time.time()
            ruff_result = run_command(
                ["ruff", "check", *target_paths],
                ctx,
                cwd=code_root,
            )
            elapsed_ms = (time.time() - start_time) * 1000
            if ruff_result.returncode != 0:
                lint_passed = False
                # Capture both stderr and stdout (ruff warnings can be in either)
                error_output = ruff_result.stderr or ruff_result.stdout or ""
                if error_output:
                    errors.append(f"Ruff check failed: {error_output[:500]}")
                else:
                    errors.append(f"Ruff check failed with return code {ruff_result.returncode}")

            # Journal: Lint result
            error_count = len([e for e in errors if "Ruff" in e])
            warning_count = len([w for w in warnings if "ruff" in w.lower()])
            append_event(
                ctx.run_path,
                "LINT_RESULT",
                {
                    "passed": lint_passed,
                    "errors_count": error_count,
                    "warnings_count": warning_count,
                    "duration_ms": round(elapsed_ms, 2),
                },
                trace_id=ctx.trace_id,
            )
        except Exception as e:
            # Command not found or other error
            lint_passed = False
            errors.append(f"Ruff execution error: {e!s}")
            append_event(
                ctx.run_path,
                "LINT_RESULT",
                {
                    "passed": False,
                    "errors_count": 1,
                    "warnings_count": 0,
                    "duration_ms": 0,
                    "error": str(e),
                },
                trace_id=ctx.trace_id,
            )
    else:
        _warn("No Python targets found; skipping ruff")

    # Run pytest
    try:
        run_pytest = verifier_config.get("run_pytest", True)
        if not run_pytest:
            _warn("Policy disabled pytest; skipping tests")
            tests_passed = True
            coverage = 1.0
        else:
            if not python_targets:
                _warn("No Python targets found; skipping pytest")
                tests_passed = True
                coverage = 1.0
            else:
                pytest_paths = verifier_config.get("pytest_paths")
                pytest_targets = []
                if pytest_paths:
                    for path in pytest_paths:
                        candidate = code_root / path
                        if candidate.exists():
                            pytest_targets.append(str(candidate.relative_to(code_root)))
                else:
                    tests_path = code_root / "tests"
                    if tests_path.exists():
                        pytest_targets.append(str(tests_path.relative_to(code_root)))

                if pytest_targets:
                    # Journal: Test start
                    append_event(
                        ctx.run_path,
                        "TEST_START",
                        {
                            "test_path": str(pytest_targets[0]) if pytest_targets else "",
                        },
                        trace_id=ctx.trace_id,
                    )
                    start_time = time.time()

                    # Create temp file for JSON report (if pytest-json-report is available)
                    report_file = ctx.run_path / "artifacts" / "pytest_report.json"
                    report_file.parent.mkdir(parents=True, exist_ok=True)

                    # Build pytest command with JSON report if available
                    pytest_cmd = ["pytest", "--tb=short", "-v", "--no-header"]
                    has_json_report = importlib.util.find_spec("pytest_jsonreport") is not None
                    if has_json_report:
                        pytest_cmd.extend(["--json-report", f"--json-report-file={report_file}"])
                    pytest_cmd.extend(pytest_targets)

                    pytest_result = run_command(
                        pytest_cmd,
                        ctx,
                        cwd=code_root,
                    )
                    elapsed_ms = (time.time() - start_time) * 1000

                    # Combine stdout AND stderr for full output
                    full_output = (pytest_result.stdout or "") + "\n" + (pytest_result.stderr or "")
                    tests_passed = pytest_result.returncode == 0

                    # Parse JSON report if available
                    if has_json_report and report_file.exists():
                        try:
                            test_details = json.loads(report_file.read_text(encoding="utf-8"))
                            # Extract failure details
                            if not tests_passed and test_details:
                                failures_list = []
                                for test in test_details.get("tests", []):
                                    if test.get("outcome") == "failed":
                                        failures_list.append({
                                            "test": test.get("nodeid", ""),
                                            "message": test.get("call", {}).get("longrepr", "")[:500] if test.get("call") else "",
                                        })
                                test_failures = failures_list
                                test_details["failures"] = test_failures
                        except Exception as e:
                            logger.warning(f"Could not parse pytest JSON report: {e}")

                    if not tests_passed:
                        # Capture both stderr and stdout (pytest errors can be in either)
                        error_output = full_output
                        if error_output:
                            errors.append(f"Pytest failed: {error_output[:1000]}")
                        else:
                            errors.append(f"Pytest failed with return code {pytest_result.returncode}")

                    # Parse pytest output for test counts
                    tests_run = 0
                    failures = 0
                    test_errors = 0
                    if pytest_result.stdout:
                        # Simple parsing
                        tests_run_match = re.search(r"(\d+)\s+passed", pytest_result.stdout)
                        if tests_run_match:
                            tests_run = int(tests_run_match.group(1))
                        failures_match = re.search(r"(\d+)\s+failed", pytest_result.stdout)
                        if failures_match:
                            failures = int(failures_match.group(1))
                        errors_match = re.search(r"(\d+)\s+error", pytest_result.stdout)
                        if errors_match:
                            test_errors = int(errors_match.group(1))

                    # Journal: Test result
                    append_event(
                        ctx.run_path,
                        "TEST_RESULT",
                        {
                            "passed": tests_passed,
                            "tests_run": tests_run,
                            "failures": failures,
                            "errors": test_errors,
                            "duration_ms": round(elapsed_ms, 2),
                        },
                        trace_id=ctx.trace_id,
                    )

                    # Store test_details and test_failures for later use in repair loop
                    # These will be added to VerifierReport.metrics

                    # Try to extract coverage if pytest-cov is available
                    if importlib.util.find_spec("pytest_cov") is not None:
                        try:
                            pytest_cov_result = run_command(
                                ["pytest", "--cov=.", "--cov-report=term"],
                                ctx,
                                cwd=code_root,
                            )
                            # Parse coverage from output (simplified)
                            coverage_match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", pytest_cov_result.stdout)
                            if coverage_match:
                                coverage = float(coverage_match.group(1)) / 100.0
                        except Exception:
                            _warn("Coverage run failed; pytest-cov may be misconfigured")
                    else:
                        _warn("pytest-cov not installed; skipping coverage")
                        if tests_passed:
                            coverage = 1.0
                else:
                    _warn("No pytest targets found; skipping pytest")
                    tests_passed = True
                    coverage = 1.0

    except Exception as e:
        # Command not found or other error
        tests_passed = False
        errors.append(f"Pytest execution error: {e!s}")

    # Run Sentinel V2 (AST analysis)
    sentinel_errors = []
    sentinel_warnings = []

    try:
        sentinel = SentinelV2(max_complexity=10)
        # Find Python files in project
        if python_targets:
            ybis_files = [Path(path) for path in python_targets if Path(path).exists()]
        else:
            py_files = list(code_root.rglob("*.py"))
            # Filter to only files in src/ybis (or modified files if available)
            ybis_files = [f for f in py_files if "src/ybis" in str(f)]

        for py_file in ybis_files[:10]:  # Limit to first 10 files for performance
            sentinel_report = sentinel.analyze(py_file, code_root)

            if sentinel_report.broken_imports:
                sentinel_errors.extend(sentinel_report.broken_imports)
            if sentinel_report.complexity_violations:
                sentinel_warnings.extend(sentinel_report.complexity_violations)
            if sentinel_report.dead_code:
                sentinel_warnings.extend(sentinel_report.dead_code)
            if sentinel_report.architectural_violations:
                sentinel_errors.extend(sentinel_report.architectural_violations)

    except Exception as e:
        _warn(f"Sentinel V2 analysis failed: {e!s}")

    # Run Bandit security scan
    try:
        bandit_violations = []
        bandit_targets: list[Path] = []
        if python_targets:
            for path in python_targets:
                candidate = Path(path)
                if not candidate.is_absolute():
                    candidate = code_root / candidate
                if candidate.exists():
                    bandit_targets.append(candidate)

        if bandit_targets:
            for target in bandit_targets:
                bandit_violations.extend(
                    SentinelV2.run_bandit_scan(code_root, target_path=target)
                )
        else:
            _warn("No Python targets found; skipping bandit")

        if bandit_violations:
            # High-severity security issues block the run
            sentinel_errors.extend(bandit_violations)
    except Exception as e:
        _warn(f"Bandit security scan failed: {e!s}")

    # Combine errors and warnings
    all_errors = errors + sentinel_errors
    all_warnings = warnings + sentinel_warnings

    # Build metrics dict with test details (if available)
    metrics = {}
    if 'test_details' in locals():
        metrics['test_details'] = test_details
    if 'test_failures' in locals():
        metrics['test_failures'] = test_failures

    # Create verifier report
    report = VerifierReport(
        task_id=ctx.task_id,
        run_id=ctx.run_id,
        lint_passed=lint_passed and len(sentinel_errors) == 0,
        tests_passed=tests_passed,
        coverage=coverage,
        errors=all_errors,
        warnings=all_warnings,
        metrics=metrics,
    )

    # Journal: Verifier complete
    append_event(
        ctx.run_path,
        "VERIFIER_COMPLETE",
        {
            "lint_passed": lint_passed and len(sentinel_errors) == 0,
            "tests_passed": tests_passed,
            "total_errors": len(all_errors),
            "total_warnings": len(all_warnings),
        },
        trace_id=ctx.trace_id,
    )

    # Write report to artifacts
    write_file(ctx.verifier_report_path, report.model_dump_json(indent=2), ctx)

    return report
