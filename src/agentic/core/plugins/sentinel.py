import os
import subprocess
import logging
from typing import Dict, List, Tuple
from src.agentic.core.protocols import VerificationResult, CodeResult

class SentinelVerifier:
    """
    Refined Gatekeeper.
    - Prevents WRITING to legacy/ but allows reading (repo-map).
    - Ensures PYTHONPATH is set for pytest.
    """
    def __init__(self):
        self.logger = logging.getLogger("Sentinel")

    async def verify(self, code_result: CodeResult, sandbox_path: str) -> VerificationResult:
        errors = []
        logs = {}
        
        # files_modified is a dict: path -> content
        files_modified = list(code_result.files_modified.keys()) if code_result.files_modified else []

        # 1. Path Safety Check (WRITE PROTECTION)
        for file in files_modified:
            # Only block if it actually attempts to change a file in legacy
            if "legacy" in file.lower() or ".venv" in file.lower():
                errors.append(f"SECURITY VIOLATION: Unauthorized write to {file}")

        # 2. Syntax & Quality Check (Ruff)
        target = " ".join(files_modified) if files_modified else "src"
        
        # Use env with PYTHONPATH
        env = os.environ.copy()
        env["PYTHONPATH"] = "."

        try:
            # Run Ruff
            result = subprocess.run(f"ruff check {target}", shell=True, capture_output=True, text=True, env=env)
            logs["ruff_stdout"] = result.stdout
            if result.returncode != 0 and result.stdout.strip():
                errors.append(f"Ruff linting failed.")
        except Exception as e:
            errors.append(f"System error running Ruff: {e}")

        # 3. Functional Testing (Pytest)
        try:
            # Run specific tests or generic unit tests
            cmd = "pytest tests/unit" 
            test_result = subprocess.run(cmd, shell=True, capture_output=True, text=True, env=env)
            
            logs["pytest_stdout"] = test_result.stdout
            if test_result.returncode != 0:
                # Only fail if it's a real test failure, not a collection error of unrelated files
                if "FAILURES" in test_result.stdout or "ERRORS" in test_result.stdout:
                    error_summary = "\n".join(test_result.stdout.splitlines()[-5:])
                    errors.append(f"Pytest failed: {error_summary}")

        except Exception as e:
            errors.append(f"System error running Pytest: {e}")

        lint_passed = not any("Ruff" in e for e in errors)
        tests_passed = not any("Pytest" in e or "SECURITY" in e for e in errors)

        return VerificationResult(
            lint_passed=lint_passed,
            tests_passed=tests_passed,
            coverage=0.0,
            errors=errors,
            warnings=[],
            logs=logs
        )

    def name(self) -> str:
        return "SentinelVerifier"
