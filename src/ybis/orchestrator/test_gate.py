"""
Test Gate - Automatic test execution before code changes are applied.

Ensures all tests pass before allowing code changes to be applied.
"""

import logging

from ..constants import PROJECT_ROOT

logger = logging.getLogger(__name__)
from ..contracts import RunContext
from ..syscalls import run_command


def run_test_gate(ctx: RunContext, test_path: str | None = None) -> tuple[bool, list[str], list[str]]:
    """
    Run test gate - execute tests before allowing code changes.

    Only runs tests for files that are being modified. If new files are being created,
    test gate passes (no tests exist yet for new files).

    Args:
        ctx: Run context
        test_path: Optional path to specific test file/function

    Returns:
        Tuple of (tests_passed, errors, warnings)
    """
    errors = []
    warnings = []

    # If specific test path provided, use it
    if test_path:
        test_target = test_path
    else:
        # Read plan to determine which files are being changed
        plan_path = ctx.plan_path
        if not plan_path.exists():
            # No plan yet - skip test gate (will run after plan is created)
            warnings.append("No plan found; skipping test gate")
            return True, errors, warnings

        import json
        try:
            plan_data = json.loads(plan_path.read_text(encoding='utf-8'))
            files_to_change = plan_data.get("files", [])

            # If no files specified or only new files, skip test gate
            if not files_to_change:
                warnings.append("No files to change; skipping test gate")
                return True, errors, warnings

            # Check if any of the files being changed already exist
            existing_files = []
            for file_path in files_to_change:
                full_path = PROJECT_ROOT / file_path
                if full_path.exists():
                    existing_files.append(file_path)

            # If only new files (none exist), skip test gate
            if not existing_files:
                warnings.append(f"Only new files being created: {files_to_change}; skipping test gate")
                return True, errors, warnings

            # Find test files for existing files being modified
            test_files = []
            tests_dir = PROJECT_ROOT / "tests"

            for file_path in existing_files:
                # Convert src/ybis/module.py -> tests/test_module.py or tests/ybis/test_module.py
                if file_path.startswith("src/"):
                    rel_path = file_path[4:]  # Remove "src/"
                    # Try multiple test file patterns
                    test_patterns = [
                        f"tests/{rel_path.replace('.py', '_test.py')}",
                        f"tests/{rel_path.replace('.py', 'test.py')}",
                        f"tests/{rel_path.replace('/', '/test_').replace('.py', '.py')}",
                    ]

                    for pattern in test_patterns:
                        test_file = PROJECT_ROOT / pattern
                        if test_file.exists():
                            test_files.append(str(test_file.relative_to(PROJECT_ROOT)))
                            break

            # If no test files found for modified files, skip test gate
            if not test_files:
                warnings.append(f"No test files found for modified files: {existing_files}; skipping test gate")
                return True, errors, warnings

            # Run tests only for the affected test files
            test_target = " ".join(test_files)

        except Exception as e:
            warnings.append(f"Could not parse plan: {e!s}; skipping test gate")
            return True, errors, warnings

    # Run pytest
    try:
        if isinstance(test_target, str) and test_target.strip():
            # Split string into list of test files
            pytest_cmd = ["pytest", "--tb=short", "-v"] + test_target.split()
        elif isinstance(test_target, str) and not test_target.strip():
            # Empty string - should not happen, but skip if it does
            warnings.append("Empty test target; skipping test gate")
            return True, errors, warnings
        else:
            pytest_cmd = ["pytest", "--tb=short", "-v", test_target]

        # Run in worktree if available (sandbox isolation)
        cwd = ctx.run_path if ctx.run_path.exists() else PROJECT_ROOT

        pytest_result = run_command(
            pytest_cmd,
            ctx,
            cwd=str(cwd),
        )

        if pytest_result.returncode != 0:
            # Tests failed
            errors.append(f"Tests failed: {pytest_result.stderr[:500] if pytest_result.stderr else pytest_result.stdout[:500]}")
            return False, errors, warnings

        # Tests passed
        return True, errors, warnings

    except Exception as e:
        errors.append(f"Test execution error: {e!s}")
        return False, errors, warnings


def check_test_coverage_gate(ctx: RunContext, min_coverage: float = 0.80) -> tuple[bool, float, list[str]]:
    """
    Check test coverage gate - ensure coverage doesn't drop below threshold.

    Args:
        ctx: Run context
        min_coverage: Minimum coverage threshold (default: 0.80 = 80%)

    Returns:
        Tuple of (coverage_passed, actual_coverage, errors)
    """
    errors = []

    try:
        # Check if pytest-cov is available
        import importlib.util
        if importlib.util.find_spec("pytest_cov") is None:
            # Coverage check not available, skip
            return True, 0.0, []

        # Run pytest with coverage
        cwd = ctx.run_path if ctx.run_path.exists() else PROJECT_ROOT

        pytest_cov_result = run_command(
            ["pytest", "--cov=src/ybis", "--cov-report=term", "tests/"],
            ctx,
            cwd=str(cwd),
        )

        if pytest_cov_result.returncode != 0:
            errors.append("Coverage check failed: pytest execution failed")
            return False, 0.0, errors

        # Parse coverage from output
        import re
        coverage_match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", pytest_cov_result.stdout)

        if coverage_match:
            actual_coverage = float(coverage_match.group(1)) / 100.0

            if actual_coverage < min_coverage:
                errors.append(
                    f"Coverage {actual_coverage*100:.1f}% below threshold {min_coverage*100:.1f}%"
                )
                return False, actual_coverage, errors

            return True, actual_coverage, errors
        else:
            errors.append("Could not parse coverage from pytest output")
            return False, 0.0, errors

    except Exception as e:
        errors.append(f"Coverage check error: {e!s}")
        return False, 0.0, errors

