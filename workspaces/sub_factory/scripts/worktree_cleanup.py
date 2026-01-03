#!/usr/bin/env python3
import argparse
from pathlib import Path

from src.agentic.core.plugins.git_manager import GitWorktreeManager


def main() -> int:
    parser = argparse.ArgumentParser(description="Cleanup YBIS worktrees")
    parser.add_argument("--force", action="store_true", help="Force remove worktrees")
    parser.add_argument("--keep-branch", action="store_true", help="Do not delete branches")
    args = parser.parse_args()

    manager = GitWorktreeManager(Path("."))
    worktrees = manager.list_worktrees()
    if not worktrees:
        print("No worktrees to clean.")
        return 0

    for wt in worktrees:
        task_id = wt.name
        try:
            manager.cleanup_worktree(
                task_id=task_id,
                branch_name=None,
                keep_branch=args.keep_branch,
                force=args.force,
            )
            print(f"Removed {wt}")
        except Exception as exc:
            print(f"Failed to remove {wt}: {exc}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
