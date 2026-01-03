import ast
import json
import logging
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

from src.agentic.core.config import REQUIRE_TESTS
from src.agentic.core.protocols import CodeResult, VerificationResult, VerifierProtocol


class SentinelVerifierEnhanced(VerifierProtocol):
    """
    Enhanced Gatekeeper with AST analysis, Import checking, and Emoji banning.
    Ensures code meets YBIS high standards before allowing it into the codebase.
    """
    def __init__(self):
        self.logger = logging.getLogger("SentinelEnhanced")
        self.restricted_imports = ["os.system", "shutil.rmtree"] # Examples

    def name(self) -> str:
        return "Sentinel-Enhanced-Verifier"

    async def verify(self, code_result: CodeResult, sandbox_path: str) -> VerificationResult:
        errors = []
        warnings = []
        logs = {}

        if not code_result.success:
            errors.append(f"EXECUTOR FAIL: {code_result.error or 'unknown error'}")
            return VerificationResult(
                lint_passed=False,
                tests_passed=False,
                coverage=0.0,
                errors=errors,
                warnings=warnings,
                logs=logs
            )

        # 0. Identify REALLY modified files (not just everything in git status)
        # We only care about files that are in the CodeResult and actually exist
        files_modified = [f for f in code_result.files_modified.keys() if os.path.exists(f)]
        if not files_modified:
            errors.append("No files modified by executor.")
            return VerificationResult(
                lint_passed=False,
                tests_passed=False,
                coverage=0.0,
                errors=errors,
                warnings=warnings,
                logs=logs
            )

        # 1. Path Safety Check (CRITICAL)
        # Only block if the file is explicitly in a protected directory
        for file in files_modified:
            f_lower = file.lower()
            if "legacy" in f_lower or ".venv" in f_lower or "_archive" in f_lower:
                # Double check: is it actually modified or just listed?
                # If we are here, Aider reported it as modified.
                errors.append(f"SECURITY VIOLATION: Unauthorized write attempt to {file}")

        # 2. AST Analysis & Emoji Ban & Type Hints Check (Only for real Python files)
        py_files = [f for f in files_modified if f.endswith(".py")]
        type_hint_errors = []  # Collect type hint errors separately for Aider feedback
        for file_path in py_files:
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()

                # Emoji Ban
                if any(ord(char) > 127 for char in content):
                    if re.search(r'[^\x00-\x7F]+', content):
                        warnings.append(f"Non-ASCII characters in {os.path.basename(file_path)}.")

                # AST Syntax Check & Type Hints Verification
                tree = ast.parse(content)

                # Check for missing type hints (Constitution requirement)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        # Skip private methods and __init__ if they're just pass
                        if node.name.startswith('_') and node.name != '__init__':
                            continue

                        # Check return type annotation
                        if node.returns is None:
                            file_name = os.path.basename(file_path)
                            error_msg = (
                                f"MISSING TYPE HINT: {file_name}:{node.lineno} - "
                                f"Function '{node.name}' missing return type annotation"
                            )
                            errors.append(error_msg)
                            type_hint_errors.append(error_msg)

                        # Check parameter type annotations
                        for arg in node.args.args:
                            if arg.annotation is None:
                                # Skip 'self' and 'cls' parameters
                                if arg.arg not in ('self', 'cls'):
                                    file_name = os.path.basename(file_path)
                                    error_msg = (
                                        f"MISSING TYPE HINT: {file_name}:{node.lineno} - "
                                        f"Function '{node.name}' parameter '{arg.arg}' "
                                        f"missing type annotation"
                                    )
                                    errors.append(error_msg)
                                    type_hint_errors.append(error_msg)

            except SyntaxError as e:
                errors.append(f"SYNTAX ERROR in {file_path}: {e}")
            except Exception as e:
                self.logger.warning(f"AST check failed for {file_path}: {e}")

        # 3. Static Analysis (Ruff) - DETERMINISTRIC with auto-fix
        if py_files:
            target = " ".join([f'"{f}"' for f in py_files])
            env = os.environ.copy()
            env["PYTHONPATH"] = "."
            try:
                # Step 1: Check for linting errors
                result = subprocess.run(
                    f"ruff check {target}",
                    check=False,
                    shell=True,
                    capture_output=True,
                    text=True,
                    env=env
                )

                if result.returncode != 0 and result.stdout.strip():
                    self.logger.info("[Sentinel] Linting errors detected. Attempting auto-fix...")
                    logs["ruff_initial_errors"] = result.stdout

                    # Step 2: Try auto-fix
                    fix_result = subprocess.run(
                        f"ruff check --fix {target}",
                        check=False,
                        shell=True,
                        capture_output=True,
                        text=True,
                        env=env
                    )
                    logs["ruff_fix_output"] = fix_result.stdout

                    # Step 3: Re-check after auto-fix
                    recheck = subprocess.run(
                        f"ruff check {target}",
                        check=False,
                        shell=True,
                        capture_output=True,
                        text=True,
                        env=env
                    )

                    if recheck.returncode != 0 and recheck.stdout.strip():
                        # Auto-fix didn't resolve all issues - provide feedback to Aider
                        warnings.append("Linting issues remain after auto-fix. Feedback provided for retry.")
                        logs["ruff_feedback"] = recheck.stdout  # This will be sent to Aider
                        logs["ruff_needs_feedback"] = True

                        # Save errors for future learning (RAG)
                        self._save_linting_errors(recheck.stdout, py_files)
                    else:
                        self.logger.info("[Sentinel] Auto-fix successful!")
                        logs["ruff_status"] = "fixed"

            except Exception as e:
                errors.append(f"Ruff system error: {e}")

        # Add type hint errors to feedback if any were found
        if type_hint_errors:
            type_hint_feedback = "TYPE HINT ERRORS (Constitution Requirement):\n"
            type_hint_feedback += "All functions MUST have type hints for parameters and return types.\n"
            type_hint_feedback += "Example: def merge_dicts(dict1: dict, dict2: dict) -> dict:\n\n"
            type_hint_feedback += "\n".join(type_hint_errors)

            # Combine with existing ruff feedback or create new feedback entry
            if logs.get("ruff_feedback"):
                logs["ruff_feedback"] = logs["ruff_feedback"] + "\n\n" + type_hint_feedback
            else:
                logs["ruff_feedback"] = type_hint_feedback
                logs["ruff_needs_feedback"] = True

        # 4. RUNTIME IMPORT TEST (NEW - Catches broken imports like OpenAI without key)
        for file_path in py_files:
            try:
                import_errors = self._check_runtime_imports(file_path, sandbox_path)
                for err in import_errors:
                    errors.append(f"RUNTIME IMPORT ERROR in {os.path.basename(file_path)}: {err}")
            except Exception as e:
                warnings.append(f"Runtime check skipped for {file_path}: {e}")

        # 5. Isolated Functional Testing (Pytest)
        try:
            # ONLY run tests that were modified in THIS task
            task_tests = [f for f in files_modified if "test_" in os.path.basename(f)]

            code_change = any(
                ("/src/" in f.replace("\\", "/"))
                or ("/scripts/" in f.replace("\\", "/"))
                or f.endswith(".py")
                for f in files_modified
            )

            if task_tests:
                cmd = f"pytest {' '.join([f'"{t}"' for t in task_tests])}"
                test_result = subprocess.run(cmd, check=False, shell=True, capture_output=True, text=True, env=env)
                logs["pytest_stdout"] = test_result.stdout
                if test_result.returncode != 0:
                    error_summary = "\n".join(test_result.stdout.splitlines()[-5:])
                    errors.append(f"Task-specific tests failed: {error_summary}")
            else:
                # No new tests? Just pass if lint passed, or run a very minimal check
                warnings.append("No specific tests found for this task. Reliability not guaranteed.")
                if REQUIRE_TESTS and code_change:
                    errors.append("Test requirement not met: no task-specific tests were updated.")
        except Exception as e:
            errors.append(f"Pytest system error: {e}")
# Lint passes if no syntax errors AND (no ruff errors OR ruff errors were auto-fixed)
        lint_passed = not any(e for e in errors if "Ruff" in e or "SYNTAX" in e) and not logs.get("ruff_needs_feedback", False)
        tests_passed = not any(e for e in errors if "Tests failed" in e or "SECURITY" in e or "RESTRICTED" in e)

        return VerificationResult(
            lint_passed=lint_passed,
            tests_passed=tests_passed,
            coverage=0.0, # Could be integrated with pytest-cov
            errors=errors,
            warnings=warnings,
            logs=logs
        )

    def _check_runtime_imports(self, file_path: str, sandbox_path: str) -> list[str]:
        """
        Check if a Python file can be imported without runtime errors.
        Catches issues like missing API keys, unavailable packages, etc.
        """
        errors = []
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content)

            # Extract all imports
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

            # Check for problematic external API dependencies
            external_apis = {
                "openai": "OpenAI API requires OPENAI_API_KEY - use Ollama/LiteLLM for local-first",
                "anthropic": "Anthropic API requires API key - use Ollama for local-first",
                "google.generativeai": "Google AI requires API key - use Ollama for local-first",
            }

            for imp in imports:
                if imp in external_apis:
                    errors.append(f"CONSTITUTION VIOLATION: {external_apis[imp]}")

            # Quick instantiation test for classes
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    # Check if __init__ requires API keys or external services
                    for item in node.body:
                        if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                            init_code = ast.unparse(item)
                            if "raise ValueError" in init_code and "API" in init_code.upper():
                                errors.append(f"Class {node.name}.__init__ will crash without API key")
                            if "os.getenv" in init_code and "raise" in init_code:
                                errors.append(f"Class {node.name} requires environment variable that may not exist")

        except Exception as e:
            self.logger.warning(f"Runtime import check failed: {e}")

        return errors

    def _save_linting_errors(self, ruff_output: str, files: list[str]) -> None:
        """Save linting errors for future learning (RAG/Mem-0)."""
        try:
            # Create errors directory
            errors_dir = Path("Knowledge/Errors/Linting")
            errors_dir.mkdir(parents=True, exist_ok=True)

            # Create error log entry
            timestamp = datetime.now().isoformat()
            error_log = {
                "timestamp": timestamp,
                "files": files,
                "ruff_output": ruff_output,
                "error_type": "linting"
            }

            # Save to file
            log_file = errors_dir / f"lint_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(log_file, 'w', encoding='utf-8') as f:
                json.dump(error_log, f, indent=2)

            self.logger.info(f"[Sentinel] Linting errors saved to {log_file}")

        except Exception as e:
            self.logger.warning(f"[Sentinel] Failed to save linting errors: {e}")
