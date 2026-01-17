#!/usr/bin/env python3
"""Test runner with coverage and reporting."""

import argparse
import subprocess
import sys
from pathlib import Path


def run_tests(
    category: str = "all",
    coverage: bool = True,
    verbose: bool = False,
    failfast: bool = False,
) -> int:
    """Run tests with specified options.

    Args:
        category: Test category (unit, integration, e2e, all)
        coverage: Enable coverage reporting
        verbose: Verbose output
        failfast: Stop on first failure

    Returns:
        Exit code
    """
    cmd = ["pytest"]

    # Category selection
    if category == "unit":
        cmd.extend(["tests/unit", "-m", "unit"])
    elif category == "integration":
        cmd.extend(["tests/integration", "-m", "integration"])
    elif category == "e2e":
        cmd.extend(["tests/e2e", "-m", "e2e"])
    else:
        cmd.append("tests/")

    # Options
    if verbose:
        cmd.append("-v")
    if failfast:
        cmd.append("-x")

    # Coverage
    if coverage:
        cmd.extend([
            "--cov=src/ybis",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov",
            "--cov-report=xml:coverage.xml",
            "--cov-fail-under=60",
        ])

    # Run
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    return result.returncode


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run tests")
    parser.add_argument(
        "category",
        nargs="?",
        default="all",
        choices=["unit", "integration", "e2e", "all"],
        help="Test category",
    )
    parser.add_argument("--no-coverage", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-x", "--failfast", action="store_true")

    args = parser.parse_args()

    sys.exit(
        run_tests(
            category=args.category,
            coverage=not args.no_coverage,
            verbose=args.verbose,
            failfast=args.failfast,
        )
    )


if __name__ == "__main__":
    main()

