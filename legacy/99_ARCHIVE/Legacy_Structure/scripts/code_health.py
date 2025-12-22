import subprocess
from pathlib import Path
from datetime import datetime

# Configuration
# Deterministic Path: Resolve relative to this script file
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent  # .YBIS_Dev root
TARGET_DIR = PROJECT_ROOT  # Scan .YBIS_Dev itself
REPORT_FILE = PROJECT_ROOT / "Veriler" / "HEALTH_REPORT.md"


def run_command(cmd):
    try:
        # Check=False is default, explicitly adding for clarity
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout, result.returncode
    except FileNotFoundError:
        return "Tool not found", 1


def scan_complexity(target):
    # Using Radon for complexity
    # Convert path to string for subprocess
    target_str = str(target)
    print(f"   Scanner: Running Radon (Complexity) on {target_str}...")
    # Exclude .venv
    cmd = ["radon", "cc", target_str, "-a", "-s", "--exclude", "*/.venv/*,*/__pycache__/*,*/node_modules/*"]
    out, _ = run_command(cmd)
    return out


def scan_lint(target):
    # Using Flake8 for linting
    target_str = str(target)
    print(f"   Scanner: Running Flake8 (Lint) on {target_str}...")
    exclusions = ".venv,__pycache__,node_modules"

    # Standard flake8 args
    base_args = [
        "flake8", target_str, "--count", "--exit-zero",
        "--statistics", f"--exclude={exclusions}"
    ]

    # Specific select for high priority issues
    # E9: SyntaxError, F63: NameError, F7: Break/Continue, F82: Undefined name
    out, _ = run_command(base_args + ["--select=E9,F63,F7,F82", "--show-source"])

    # Full scan with complexity limit and line length
    out_full, count = run_command(base_args + ["--max-complexity=10", "--max-line-length=120"])

    return out_full


def generate_report():
    print(f"[Auditor] Starting Scan on {TARGET_DIR}...")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    complexity_data = scan_complexity(TARGET_DIR)
    lint_data = scan_lint(TARGET_DIR)

    report_content = f"""# YBIS Code Health Report
**Date:** {timestamp}
**Target:** `{TARGET_DIR}`

## 1. Cyclomatic Complexity (Radon)
> Goal: Average Complexity < 5 (A). Blocks > 10 (B) allow. Blocks > 20 (C) fail.

```text
{complexity_data.strip() if complexity_data.strip() else "No complexity data (Is radon installed?)"}
```

## 2. Lint Issues (Flake8)
> Goal: 0 Errors.

```text
{lint_data.strip() if lint_data.strip() else "No lint issues found (or flake8 missing)."}
```

## 3. Action Plan
- [ ] Fix High Complexity Blocks.
- [ ] Resolve Lint Errors.
"""

    # Ensure parent dir exists
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)

    print(f"[Auditor] Scan Complete. Report generated: {REPORT_FILE}")


if __name__ == "__main__":
    generate_report()
