#!/usr/bin/env python3
"""
Protocol check for task artifacts with tier support.

Supports --json flag for machine-readable output (used by run_orchestrator.py).
"""
import argparse
import json
import subprocess
from pathlib import Path


# Tier 0: Doc-only tasks (minimal token cost)
REQUIRED_TIER0 = [
    "docs/RUNBOOK.md",
]

# Tier 1: Low-risk tasks
REQUIRED_TIER1 = REQUIRED_TIER0 + [
    "artifacts/RESULT.md",
]

# Tier 2: Standard tasks (formerly "lite")
REQUIRED_TIER2 = [
    "docs/PLAN.md",
    "docs/RUNBOOK.md",
    "artifacts/RESULT.md",
    "CHANGES/changed_files.json",
    "META.json",
]

# Legacy aliases
REQUIRED_LITE = REQUIRED_TIER2
REQUIRED_FULL = REQUIRED_TIER2 + [
    "EVIDENCE/summary.md",
]


def auto_detect_tier(task_id: str) -> int:
    """
    Auto-detect tier from git diff statistics.

    Rules:
    - <10 lines changed: Tier 0 (doc-only)
    - <50 lines changed: Tier 1 (low-risk)
    - ≥50 lines changed: Tier 2 (high-risk)
    """
    try:
        # Get commit hash from RUNBOOK or git log
        result = subprocess.run(
            ["git", "log", "--all", "--grep", task_id, "-1", "--format=%H"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return 2  # Default to Tier 2 if no commit found

        commit_hash = result.stdout.strip()

        # Get diff stats
        result = subprocess.run(
            ["git", "diff", "--stat", f"{commit_hash}~1", commit_hash],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return 2

        # Parse lines changed from last line (e.g., "3 files changed, 42 insertions(+), 10 deletions(-)")
        last_line = result.stdout.strip().split('\n')[-1]

        # Extract total changes
        total_changes = 0
        if "insertion" in last_line:
            parts = last_line.split(',')
            for part in parts:
                if "insertion" in part or "deletion" in part:
                    num = ''.join(filter(str.isdigit, part.split()[0]))
                    if num:
                        total_changes += int(num)

        # Determine tier
        if total_changes < 10:
            return 0
        elif total_changes < 50:
            return 1
        else:
            return 2

    except (subprocess.TimeoutExpired, Exception):
        return 2  # Default to Tier 2 on any error


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate task artifact checklist with tier support")
    parser.add_argument("--task-id", required=True, help="Task ID (e.g., TASK-New-1234)")
    parser.add_argument("--root", default="workspaces/active", help="Workspace root")
    parser.add_argument("--auto-archive", action="store_true", help="Fallback to archive/YYYY/MM if not found in active")
    parser.add_argument("--mode", default=None, choices=["lite", "full"], help="Legacy: Artifact mode (use --tier instead)")
    parser.add_argument("--tier", default="auto", help="Artifact tier: 0 (doc-only), 1 (low-risk), 2 (standard), auto (detect from git)")
    parser.add_argument("--json", action="store_true", help="Output JSON format for machine parsing")
    args = parser.parse_args()

    base = Path(args.root) / args.task_id
    if args.auto_archive and not base.exists():
        archive_root = Path("workspaces") / "archive"
        for year_dir in archive_root.glob("*"):
            for month_dir in year_dir.glob("*"):
                candidate = month_dir / args.task_id
                if candidate.exists():
                    base = candidate
                    break
            if base.exists():
                break

    # Determine tier
    if args.mode:
        # Legacy mode support
        tier = "full" if args.mode == "full" else 2
        tier_name = args.mode
    else:
        if args.tier == "auto":
            tier = auto_detect_tier(args.task_id)
            tier_name = f"tier{tier} (auto-detected)"
        else:
            try:
                tier = int(args.tier)
                if tier not in [0, 1, 2]:
                    print(f"[ERROR] Invalid tier: {args.tier}. Must be 0, 1, 2, or 'auto'")
                    return 1
                tier_name = f"tier{tier}"
            except ValueError:
                if args.tier == "full":
                    tier = "full"
                    tier_name = "full"
                else:
                    print(f"[ERROR] Invalid tier: {args.tier}. Must be 0, 1, 2, 'auto', or 'full'")
                    return 1

    # Select required artifacts
    if tier == "full":
        required = REQUIRED_FULL
    elif tier == 0:
        required = REQUIRED_TIER0
    elif tier == 1:
        required = REQUIRED_TIER1
    else:  # tier == 2
        required = REQUIRED_TIER2

    missing = []
    for rel in required:
        path = base / rel
        if not path.exists():
            missing.append(rel)

    # Determine numeric tier for JSON output
    tier_num = tier if isinstance(tier, int) else 2  # 'full' maps to 2

    if missing:
        if args.json:
            print(json.dumps({
                "success": False,
                "tier": tier_num,
                "tier_name": tier_name,
                "task_id": args.task_id,
                "missing": missing
            }))
        else:
            print(f"[FAIL] Missing artifacts for {args.task_id} ({tier_name}):")
            for item in missing:
                print(f"- {item}")
        return 1

    if args.json:
        print(json.dumps({
            "success": True,
            "tier": tier_num,
            "tier_name": tier_name,
            "task_id": args.task_id,
            "missing": []
        }))
    else:
        print(f"[OK] All required artifacts present for {args.task_id} ({tier_name}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
