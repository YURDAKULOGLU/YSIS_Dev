"""
Test Execution MCP Tools.

Tools for running tests via MCP.
"""

import asyncio
import json
import logging
import subprocess
import sys

from ...constants import PROJECT_ROOT

logger = logging.getLogger(__name__)


async def run_tests(
    test_path: str = "tests/",
    verbose: bool = True,
    coverage: bool = False,
    specific_test: str | None = None,
) -> str:
    """
    Run YBIS tests using pytest.

    Args:
        test_path: Path to test directory or file (default: "tests/")
        verbose: Enable verbose output (default: True)
        coverage: Run with coverage (default: False)
        specific_test: Run specific test file or function (optional)

    Returns:
        JSON string with test results
    """
    try:
        # Build pytest command
        cmd = [sys.executable, "-m", "pytest"]

        if verbose:
            cmd.append("-v")

        # Try to use pytest-xdist for parallel execution (faster)
        try:
            # Use auto-detected number of workers (or 4 max)
            import os

            import pytest_xdist
            workers = min(4, os.cpu_count() or 1)
            cmd.extend(["-n", str(workers)])  # Parallel execution
        except ImportError:
            # pytest-xdist not installed, run sequentially
            pass

        if coverage:
            cmd.extend(["--cov=src/ybis", "--cov-report=term"])

        if specific_test:
            cmd.append(specific_test)
        else:
            cmd.append(test_path)

        cmd.extend(["--tb=short", "--no-header"])

        # Run tests in thread to avoid blocking (subprocess.run is synchronous)
        def run_test_sync():
            """Run test synchronously in thread."""
            try:
                result = subprocess.run(
                    cmd,
                    cwd=PROJECT_ROOT,
                    capture_output=True,
                    text=True,
                    timeout=10,  # 10 second timeout (tests should complete in ~2s)
                )
                return {
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "error": None,
                }
            except subprocess.TimeoutExpired as e:
                return {
                    "returncode": -1,
                    "stdout": "",
                    "stderr": f"Test execution timed out: {e}",
                    "error": "subprocess.TimeoutExpired",
                }
            except Exception as e:
                return {
                    "returncode": -1,
                    "stdout": "",
                    "stderr": f"Error running tests: {e}",
                    "error": str(e),
                }

        # Tests are now fast (~2 seconds), so run them in thread to avoid blocking
        try:
            if hasattr(asyncio, 'to_thread'):
                # Python 3.9+ - use to_thread
                result_dict = await asyncio.wait_for(
                    asyncio.to_thread(run_test_sync),
                    timeout=15.0  # 15 second timeout
                )
            else:
                # Python < 3.9 - use run_in_executor
                loop = asyncio.get_event_loop()
                result_dict = await asyncio.wait_for(
                    loop.run_in_executor(None, run_test_sync),
                    timeout=15.0
                )

            return_code = result_dict["returncode"]
            stdout_text = result_dict["stdout"]
            stderr_text = result_dict["stderr"]
            error_msg = result_dict["error"]

            if error_msg:
                return json.dumps(
                    {
                        "success": False,
                        "exit_code": return_code,
                        "stdout": stdout_text,
                        "stderr": stderr_text,
                        "error": error_msg,
                        "command": " ".join(cmd),
                    },
                    indent=2,
                )
        except TimeoutError:
            return json.dumps(
                {
                    "success": False,
                    "error": "Test execution timed out after 15 seconds (asyncio timeout)",
                    "command": " ".join(cmd),
                },
                indent=2,
            )

        return json.dumps(
            {
                "success": return_code == 0,
                "exit_code": return_code,
                "stdout": stdout_text,
                "stderr": stderr_text,
                "command": " ".join(cmd),
            },
            indent=2,
        )
    except subprocess.TimeoutExpired:
        return json.dumps(
            {
                "success": False,
                "error": "Test execution timed out after 5 minutes",
                "command": " ".join(cmd),
            },
            indent=2,
        )
    except Exception as e:
        return json.dumps(
            {
                "success": False,
                "error": str(e),
                "command": " ".join(cmd) if "cmd" in locals() else "unknown",
            },
            indent=2,
        )


async def run_linter(
    path: str = "src/",
    fix: bool = False,
) -> str:
    """
    Run linter (ruff) on codebase.

    Args:
        path: Path to lint (default: "src/")
        fix: Auto-fix issues (default: False)

    Returns:
        JSON string with lint results
    """
    try:
        cmd = [sys.executable, "-m", "ruff", "check"]

        if fix:
            cmd.append("--fix")

        cmd.append(path)

        # Run linter using async subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=PROJECT_ROOT,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=60.0
            )
            return_code = process.returncode
            stdout_text = stdout.decode('utf-8', errors='replace')
            stderr_text = stderr.decode('utf-8', errors='replace')
        except TimeoutError:
            process.kill()
            await process.wait()
            return json.dumps(
                {
                    "success": False,
                    "error": "Linter execution timed out",
                    "command": " ".join(cmd),
                },
                indent=2,
            )

        result = type('Result', (), {
            'returncode': return_code,
            'stdout': stdout_text,
            'stderr': stderr_text,
        })()

        return json.dumps(
            {
                "success": result.returncode == 0,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": " ".join(cmd),
            },
            indent=2,
        )
    except Exception as e:
        return json.dumps(
            {
                "success": False,
                "error": str(e),
                "command": " ".join(cmd) if "cmd" in locals() else "unknown",
            },
            indent=2,
        )


async def check_test_coverage(
    test_path: str = "tests/",
    min_coverage: float = 0.0,
) -> str:
    """
    Check test coverage.

    Args:
        test_path: Path to test directory (default: "tests/")
        min_coverage: Minimum coverage threshold (default: 0.0)

    Returns:
        JSON string with coverage results
    """
    try:
        cmd = [
            sys.executable,
            "-m",
            "pytest",
            test_path,
            "--cov=src/ybis",
            "--cov-report=term",
            "--cov-report=json",
            "--no-header",
        ]

        # Run coverage using async subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=PROJECT_ROOT,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=300.0
            )
            return_code = process.returncode
            stdout_text = stdout.decode('utf-8', errors='replace')
            stderr_text = stderr.decode('utf-8', errors='replace')
        except TimeoutError:
            process.kill()
            await process.wait()
            return json.dumps(
                {
                    "success": False,
                    "error": "Coverage check timed out",
                    "command": " ".join(cmd),
                },
                indent=2,
            )

        result = type('Result', (), {
            'returncode': return_code,
            'stdout': stdout_text,
            'stderr': stderr_text,
        })()

        # Try to parse coverage from JSON report
        coverage_data = {}
        coverage_json_path = PROJECT_ROOT / "coverage.json"
        if coverage_json_path.exists():
            try:
                coverage_data = json.loads(coverage_json_path.read_text())
            except Exception:
                pass

        return json.dumps(
            {
                "success": result.returncode == 0,
                "exit_code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "coverage": coverage_data,
                "command": " ".join(cmd),
            },
            indent=2,
        )
    except Exception as e:
        return json.dumps(
            {
                "success": False,
                "error": str(e),
                "command": " ".join(cmd) if "cmd" in locals() else "unknown",
            },
            indent=2,
        )

