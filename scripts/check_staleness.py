#!/usr/bin/env python
"""
CLI to manually run staleness check.

Usage:
    python scripts/check_staleness.py
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.services.staleness_hook import run_staleness_check


async def main():
    print("Running staleness check...")
    report = await run_staleness_check(project_root)

    print("\n" + "=" * 50)
    print("STALENESS CHECK REPORT")
    print("=" * 50)

    print(f"\nChanged files: {len(report.get('changed_files', []))}")
    for f in report.get('changed_files', [])[:10]:
        print(f"  - {f}")

    print(f"\nStale files: {len(report.get('stale_files', []))}")
    for s in report.get('stale_files', [])[:10]:
        print(f"  - {s['file']} (depends on {s['depends_on']})")

    print(f"\nTasks created: {len(report.get('tasks_created', []))}")
    for t in report.get('tasks_created', []):
        print(f"  - {t}")

    if report.get('error'):
        print(f"\nError: {report['error']}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    asyncio.run(main())

