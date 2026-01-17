"""
Staleness Hook - Run after each orchestrator run to detect staleness.

Usage:
    from ybis.services.staleness_hook import run_staleness_check
    await run_staleness_check()
"""

import asyncio
from pathlib import Path

from ..constants import PROJECT_ROOT
from .staleness import StalenessWatcher


async def run_staleness_check(project_root: Path | None = None) -> dict:
    """
    Run staleness check and create consistency tasks if needed.

    Args:
        project_root: Project root path (default: PROJECT_ROOT)

    Returns:
        Staleness check report
    """
    watcher = StalenessWatcher(project_root or PROJECT_ROOT)
    return await watcher.check_and_create_tasks()


def run_staleness_check_sync(project_root: Path | None = None) -> dict:
    """Synchronous wrapper for staleness check."""
    return asyncio.run(run_staleness_check(project_root))


# CLI entry point
if __name__ == "__main__":
    import json
    report = run_staleness_check_sync()
    print(json.dumps(report, indent=2))

