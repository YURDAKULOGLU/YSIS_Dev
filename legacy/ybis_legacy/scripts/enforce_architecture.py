#!/usr/bin/env python3
"""
ARCHITECTURE ENFORCER
Enforces the decisions from DEBATE-20251228174942.

Rules:
1. NO imports of 'src.agentic.graph.workflow' (The Old Brain).
2. NO usage of 'run_next.py' or 'run_production.py' without deprecation acknowledgment.
3. LEGACY folders are exempt.
"""

import os
import sys
from pathlib import Path
import re

# Config
PROJECT_ROOT = Path(__file__).parent.parent
FORBIDDEN_IMPORTS = [
    "src.agentic.graph.workflow",
    "agentic.graph.workflow"
]
DEPRECATED_SCRIPTS = [
    "scripts/run_next.py",
    "scripts/run_production.py"
]
IGNORED_DIRS = [
    "legacy",
    "workspaces",
    ".git",
    "__pycache__",
    ".sandbox"
]

def scan_file_for_imports(file_path: Path):
    """Scan a file for forbidden imports."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        issues = []
        for imp in FORBIDDEN_IMPORTS:
            if imp in content:
                issues.append(f"FORBIDDEN IMPORT: '{imp}' found.")
        return issues
    except Exception as e:
        return [f"Could not read file: {e}"]

def check_architecture():
    print("[INFO]  STARTING ARCHITECTURE ENFORCEMENT SCAN...")
    print(f"   Root: {PROJECT_ROOT}")

    violations = 0

    # 1. Scan SRC for forbidden imports
    print("\n[INFO] Scanning src/ for The Old Brain...")
    src_dir = PROJECT_ROOT / "src"
    if src_dir.exists():
        for file_path in src_dir.rglob("*.py"):
            # Skip tests for now if needed, but better to check everything in src
            issues = scan_file_for_imports(file_path)
            if issues:
                for issue in issues:
                    print(f"   [ERROR] [VIOLATION] {file_path.relative_to(PROJECT_ROOT)}: {issue}")
                    violations += 1

    # 2. Check Scripts
    print("\n[INFO] Checking Script Status...")
    for script in DEPRECATED_SCRIPTS:
        p = PROJECT_ROOT / script
        if p.exists():
            print(f"   [WARN]  [DEPRECATED] {script} still exists. Should be replaced by 'run_orchestrator.py'.")
            # This is a warning, not a violation for now, until Codex finishes.

    new_runner = PROJECT_ROOT / "scripts" / "run_orchestrator.py"
    if not new_runner.exists():
        print(f"   [WARN]  [MISSING] 'scripts/run_orchestrator.py' is not yet created (Waiting for Codex).")
    else:
        print(f"   [SUCCESS] [OK] 'scripts/run_orchestrator.py' exists.")

    print("\n" + "="*40)
    if violations > 0:
        print(f"[ERROR] ARCHITECTURE CHECK FAILED: {violations} violations found.")
        sys.exit(1)
    else:
        print("[SUCCESS] ARCHITECTURE CHECK PASSED. System is compliant.")
        sys.exit(0)

if __name__ == "__main__":
    check_architecture()
