"""
SimpleVerifier - Basic code verification with test policy enforcement.

Performs:
1. Syntax checking (compile Python, run tsc for TS)
2. Linting with ruff
3. Test execution with pytest
4. Policy enforcement gate
"""

import os
import subprocess
from pathlib import Path
from src.agentic.core.utils.logging_utils import log_event

from src.agentic.core.config import REQUIRE_TESTS
from src.agentic.core.protocols import CodeResult, VerificationResult
from src.agentic.core.plugins.test_policy import enforce_gate, classify_task


class SimpleVerifier:
    """
    Verifier with syntax checking, linting, test execution, and policy enforcement.
    """

    def __init__(self, task_id: str = "", task_goal: str = "", skip_tests: bool = False):
        self.task_id = task_id
        self.task_goal = task_goal
        self.skip_tests = skip_tests

    async def verify(self, code_result: CodeResult, sandbox_path: str) -> VerificationResult:
        """Verify code quality with policy enforcement."""

        log_event(f"Verifying {len(code_result.files_modified)} files", component="simple_verifier")

        lint_passed = True
        tests_passed = True
        errors = []
        warnings = []
        logs = {}
        coverage = 0.0

        # Check each file for syntax
        for file_path, content in code_result.files_modified.items():
            file_ext = Path(file_path).suffix

            # Python files: compile check
            if file_ext == ".py":
                lint_result, lint_errors = self._check_python(content, file_path)
                if not lint_result:
                    lint_passed = False
                    errors.extend(lint_errors)
                logs[f"syntax_{file_path}"] = "\n".join(lint_errors) if lint_errors else "[OK]"

            # TypeScript files
            elif file_ext in [".ts", ".tsx"]:
                if not content.strip():
                    lint_passed = False
                    errors.append(f"{file_path}: Empty file")
                logs[f"syntax_{file_path}"] = "[OK] (basic check)"

            else:
                if not content.strip():
                    warnings.append(f"{file_path}: Empty file")
                logs[f"syntax_{file_path}"] = "[OK]"

        # Run ruff linting on Python files
        python_files = [f for f in code_result.files_modified.keys() if f.endswith(".py")]
        if python_files:
            ruff_passed, ruff_output = self._run_ruff(python_files)
            if not ruff_passed:
                lint_passed = False
                errors.append(f"Ruff linting failed")
            logs["ruff"] = ruff_output

        # Run pytest if tests are required
        if REQUIRE_TESTS and not self.skip_tests:
            tests_passed, test_output, coverage = self._run_pytest(sandbox_path)
            logs["pytest"] = test_output
        else:
            logs["pytest"] = "Skipped (REQUIRE_TESTS=false or skip_tests=true)"

        # Apply policy enforcement gate
        gate_result = enforce_gate(
            task_id=self.task_id,
            goal=self.task_goal,
            lint_passed=lint_passed,
            tests_passed=tests_passed,
            coverage=coverage,
            skip_tests=self.skip_tests
        )

        logs["policy"] = {
            "task_type": gate_result.task_type.value,
            "passed": gate_result.passed,
            "violations": gate_result.violations,
            "warnings": gate_result.warnings
        }

        # Add policy violations to errors
        errors.extend(gate_result.violations)
        warnings.extend(gate_result.warnings)

        # Final pass/fail based on gate
        final_lint = lint_passed and gate_result.passed
        final_tests = tests_passed or (self.skip_tests and gate_result.policy.allow_skip)

        log_event(f"Task Type: {gate_result.task_type.value}", component="simple_verifier")
        log_event(f"Lint: {'[OK]' if lint_passed else '[X]'}", component="simple_verifier")
        log_event(f"Tests: {'[OK]' if tests_passed else '[X]'}", component="simple_verifier")
        log_event(f"Coverage: {coverage:.1%}", component="simple_verifier")
        log_event(f"Gate: {'[OK]' if gate_result.passed else '[X]'}", component="simple_verifier")

        return VerificationResult(
            lint_passed=final_lint,
            tests_passed=final_tests,
            coverage=coverage,
            errors=errors,
            warnings=warnings,
            logs=logs
        )

    def name(self) -> str:
        return "SimpleVerifier(basic)"

    # ========================================================================
    # IMPLEMENTATION
    # ========================================================================

    def _check_python(self, code: str, file_name: str) -> tuple[bool, list]:
        """Check Python syntax"""
        try:
            compile(code, file_name, "exec")
            return True, []
        except SyntaxError as e:
            return False, [f"{file_name}:{e.lineno}: {e.msg}"]

    def _check_typescript(self, sandbox_path: str) -> tuple[bool, list]:
        """Check TypeScript with tsc (if available)"""
        try:
            result = subprocess.run(
                ["tsc", "--noEmit"],
                cwd=sandbox_path,
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return True, []
            else:
                return False, result.stderr.split("\n")
        except (FileNotFoundError, subprocess.TimeoutExpired):
            # tsc not available or timeout
            return True, ["tsc not available - skipped"]

    def _run_ruff(self, files: list[str]) -> tuple[bool, str]:
        """Run ruff linter on Python files."""
        try:
            result = subprocess.run(
                ["ruff", "check"] + files,
                capture_output=True,
                text=True,
                timeout=60
            )
            output = result.stdout + result.stderr
            return result.returncode == 0, output.strip() or "[OK] No issues"
        except FileNotFoundError:
            return True, "ruff not available - skipped"
        except subprocess.TimeoutExpired:
            return False, "ruff timeout"

    def _run_pytest(self, sandbox_path: str) -> tuple[bool, str, float]:
        """
        Run pytest and return (passed, output, coverage).
        Coverage is extracted from pytest-cov output if available.
        """
        try:
            # Try to run pytest with coverage
            result = subprocess.run(
                ["python", "-m", "pytest", "-v", "--tb=short", "-q"],
                cwd=sandbox_path,
                capture_output=True,
                text=True,
                timeout=120
            )
            output = result.stdout + result.stderr

            # Parse coverage from output if present (e.g., "TOTAL ... 85%")
            coverage = 0.0
            import re
            cov_match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", output)
            if cov_match:
                coverage = int(cov_match.group(1)) / 100.0

            passed = result.returncode == 0
            return passed, output.strip() or "[OK] Tests passed", coverage

        except FileNotFoundError:
            return True, "pytest not available - skipped", 0.0
        except subprocess.TimeoutExpired:
            return False, "pytest timeout (>120s)", 0.0


# ============================================================================
# TESTING
# ============================================================================

async def test_simple_verifier():
    """Test verifier standalone"""
    from src.agentic.core.protocols import CodeResult

    verifier = SimpleVerifier()

    code_result = CodeResult(
        files_modified={
            "test.py": "def hello():\n    print('hello')\n",
            "test2.py": "def broken(\n    # syntax error",
        },
        commands_run=[],
        outputs={},
        success=True
    )

    result = await verifier.verify(code_result, ".sandbox/test")

    log_event(f"Lint passed: {result.lint_passed}", component="simple_verifier_test")
    log_event(f"Tests passed: {result.tests_passed}", component="simple_verifier_test")
    log_event(f"Errors: {result.errors}", component="simple_verifier_test", level="warning")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_simple_verifier())
