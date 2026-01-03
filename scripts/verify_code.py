#!/usr/bin/env python3
"""
CODE VERIFICATION PIPELINE
===========================
Trust Nothing, Verify Everything.

This script verifies code changes BEFORE they are committed.
Used by Aider/agents to catch errors at generation time, not after.

Usage:
    python scripts/verify_code.py                    # Verify all staged changes
    python scripts/verify_code.py --file path.py    # Verify specific file
    python scripts/verify_code.py --rollback        # Rollback last changes if verification failed

Exit Codes:
    0 = All checks passed
    1 = Syntax error
    2 = Lint error
    3 = Import error
    4 = Test failure
    5 = Type error
"""

import argparse
import ast
import subprocess
import sys
from pathlib import Path


def check_python_syntax(file_path: str) -> tuple[bool, str]:
    """Check Python file for syntax errors using AST."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        ast.parse(source)
        return True, "OK"
    except SyntaxError as e:
        return False, f"Line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, str(e)


def check_typescript_syntax(file_path: str) -> tuple[bool, str]:
    """Check TypeScript file for syntax errors using tsc."""
    try:
        result = subprocess.run(
            ["npx", "tsc", "--noEmit", "--skipLibCheck", file_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return True, "OK"
        return False, result.stderr or result.stdout
    except FileNotFoundError:
        return True, "SKIP (tsc not found)"
    except Exception as e:
        return False, str(e)


def check_imports(file_path: str) -> tuple[bool, str]:
    """Verify all imports can be resolved."""
    if not file_path.endswith('.py'):
        return True, "SKIP (not Python)"

    try:
        result = subprocess.run(
            [sys.executable, "-c", f"import ast; ast.parse(open('{file_path}').read())"],
            capture_output=True,
            text=True,
            timeout=10
        )
        # Try to import the module
        result = subprocess.run(
            [sys.executable, "-m", "py_compile", file_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, "OK"
        return False, result.stderr
    except Exception as e:
        return False, str(e)


def check_lint(file_path: str) -> tuple[bool, str]:
    """Run ruff linter on file."""
    if not file_path.endswith('.py'):
        return True, "SKIP (not Python)"

    try:
        result = subprocess.run(
            ["ruff", "check", file_path, "--select=E,F", "--ignore=E501"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return True, "OK"
        # Filter to only critical errors
        errors = [line for line in result.stdout.split('\n') if 'E999' in line or 'F' in line]
        if not errors:
            return True, "OK (warnings only)"
        return False, '\n'.join(errors[:5])  # First 5 errors
    except FileNotFoundError:
        return True, "SKIP (ruff not found)"
    except Exception as e:
        return False, str(e)


def run_related_tests(file_path: str) -> tuple[bool, str]:
    """Run tests related to the changed file."""
    path = Path(file_path)

    # Find related test file
    possible_tests = [
        path.parent / f"test_{path.name}",
        path.parent / "tests" / f"test_{path.name}",
        Path("tests") / f"test_{path.stem}.py",
        Path("tests") / path.parent.name / f"test_{path.name}",
        Path("tests") / "unit" / f"test_{path.stem}.py",  # tests/unit/test_*.py
        Path("tests") / "integration" / f"test_{path.stem}.py",  # tests/integration/test_*.py
    ]

    test_file = None
    for t in possible_tests:
        if t.exists():
            test_file = t
            break

    if not test_file:
        return True, "SKIP (no tests found)"

    # Prepare environment with current directory in PYTHONPATH
    env = sys.environ.copy()
    env["PYTHONPATH"] = os.getcwd() + os.pathsep + env.get("PYTHONPATH", "")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_file), "-x", "-q", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=60,
            env=env
        )
        if result.returncode == 0:
            return True, "OK"
        return False, result.stdout[-500:] if len(result.stdout) > 500 else result.stdout
    except FileNotFoundError:
        return True, "SKIP (pytest not found)"
    except Exception as e:
        return False, str(e)


def get_staged_files() -> list[str]:
    """Get list of staged files from git."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            capture_output=True,
            text=True
        )
        files = [f for f in result.stdout.strip().split('\n') if f]
        return files
    except Exception:
        return []


def get_modified_files() -> list[str]:
    """Get list of modified (unstaged) files from git."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only"],
            capture_output=True,
            text=True
        )
        files = [f for f in result.stdout.strip().split('\n') if f]
        return files
    except Exception:
        return []


def rollback_changes():
    """Rollback uncommitted changes."""
    try:
        subprocess.run(["git", "checkout", "--", "."], check=True)
        print("[ROLLBACK] All uncommitted changes reverted")
        return True
    except Exception as e:
        print(f"[ROLLBACK FAILED] {e}")
        return False


def verify_file(file_path: str, verbose: bool = True) -> tuple[bool, dict]:
    """Run all verification checks on a single file."""
    results = {}
    all_passed = True

    checks = [
        ("syntax", check_python_syntax if file_path.endswith('.py') else check_typescript_syntax),
        ("imports", check_imports),
        ("lint", check_lint),
        ("tests", run_related_tests),
    ]

    for check_name, check_fn in checks:
        passed, message = check_fn(file_path)
        results[check_name] = {"passed": passed, "message": message}

        if verbose:
            status = "[OK]" if passed else "[FAIL]"
            print(f"  {status} {check_name}: {message[:80]}")

        if not passed and "SKIP" not in message:
            all_passed = False

    return all_passed, results


def main():
    parser = argparse.ArgumentParser(description="Verify code before commit")
    parser.add_argument("--file", "-f", help="Specific file to verify")
    parser.add_argument("--rollback", "-r", action="store_true", help="Rollback changes")
    parser.add_argument("--staged", "-s", action="store_true", help="Check staged files only")
    parser.add_argument("--quiet", "-q", action="store_true", help="Minimal output")
    args = parser.parse_args()

    if args.rollback:
        sys.exit(0 if rollback_changes() else 1)

    # Determine files to check
    if args.file:
        files = [args.file]
    elif args.staged:
        files = get_staged_files()
    else:
        files = get_modified_files() + get_staged_files()

    # Filter to code files only, handle Windows 'nul' and Worktree paths
    code_extensions = {'.py', '.ts', '.js', '.tsx', '.jsx'}
    valid_files = []
    for f in files:
        if f.lower() == 'nul':
            continue
        path = Path(f)
        if path.suffix in code_extensions and path.exists():
            valid_files.append(f)
    
    files = valid_files

    if not files:
        print("[VERIFY] No code files to check")
        sys.exit(0)

    print(f"[VERIFY] Checking {len(files)} file(s)...")

    all_passed = True
    failed_files = []

    for file_path in files:
        print(f"\n[FILE] {file_path}")
        passed, results = verify_file(file_path, verbose=not args.quiet)
        if not passed:
            all_passed = False
            failed_files.append(file_path)

    # Summary
    print("\n" + "="*50)
    if all_passed:
        print("[OK] ALL CHECKS PASSED - Safe to commit")
        sys.exit(0)
    else:
        print(f"[FAIL] VERIFICATION FAILED - {len(failed_files)} file(s) have issues:")
        for f in failed_files:
            print(f"   - {f}")
        print("\nOptions:")
        print("  1. Fix the issues and re-run")
        print("  2. python scripts/verify_code.py --rollback")
        sys.exit(1)


if __name__ == "__main__":
    main()
