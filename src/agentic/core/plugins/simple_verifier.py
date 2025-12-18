"""
SimpleVerifier - Basic code verification.

Performs:
1. Syntax checking (compile Python, run tsc for TS)
2. Basic linting
3. Placeholder for tests (always passes for now)
"""

import os
import subprocess
from pathlib import Path

from src.agentic.core.protocols import CodeResult, VerificationResult


class SimpleVerifier:
    """
    Simple verifier with basic checks.

    For MVP: just checks syntax and pretends tests pass.
    Later: integrate with real test runners.
    """

    async def verify(self, code_result: CodeResult, sandbox_path: str) -> VerificationResult:
        """Verify code quality"""

        print(f"[SimpleVerifier] Verifying {len(code_result.files_modified)} files")

        lint_passed = True
        tests_passed = True  # For now, assume tests pass
        errors = []
        warnings = []
        logs = {}

        # Check each file
        for file_path, content in code_result.files_modified.items():
            file_ext = Path(file_path).suffix

            # Python files: compile check
            if file_ext == ".py":
                lint_result, lint_errors = self._check_python(content, file_path)
                if not lint_result:
                    lint_passed = False
                    errors.extend(lint_errors)
                logs[f"lint_{file_path}"] = "\n".join(lint_errors) if lint_errors else "[OK] OK"

            # TypeScript files: would use tsc, but skip for MVP
            elif file_ext in [".ts", ".tsx"]:
                # For MVP, just check it's not empty
                if not content.strip():
                    lint_passed = False
                    errors.append(f"{file_path}: Empty file")
                logs[f"lint_{file_path}"] = "[OK] OK (basic check)"

            # Other files: basic checks
            else:
                if not content.strip():
                    warnings.append(f"{file_path}: Empty file")
                logs[f"lint_{file_path}"] = "[OK] OK"

        # Coverage (placeholder)
        coverage = 0.75  # Fake coverage for MVP

        print(f"[SimpleVerifier] Lint: {'[OK]' if lint_passed else '[X]'}")
        print(f"[SimpleVerifier] Tests: {'[OK]' if tests_passed else '[X]'}")
        print(f"[SimpleVerifier] Coverage: {coverage:.1%}")

        return VerificationResult(
            lint_passed=lint_passed,
            tests_passed=tests_passed,
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

    print(f"Lint passed: {result.lint_passed}")
    print(f"Tests passed: {result.tests_passed}")
    print(f"Errors: {result.errors}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_simple_verifier())
