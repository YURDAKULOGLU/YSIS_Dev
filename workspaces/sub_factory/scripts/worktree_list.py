#!/usr/bin/env python3
from pathlib import Path

from src.agentic.core.plugins.git_manager import GitWorktreeManager


def main() -> int:
    manager = GitWorktreeManager(Path("."))
    worktrees = manager.list_worktrees()
    if not worktrees:
        print("No worktrees found.")
        return 0
    print("Worktrees:")
    for wt in worktrees:
        print(f"- {wt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
