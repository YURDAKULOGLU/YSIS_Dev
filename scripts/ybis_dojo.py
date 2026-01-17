#!/usr/bin/env python3
"""
YBIS Dojo - Interactive onboarding tutorial for agents and humans.

Teaches the basics of the YBIS platform through hands-on examples.
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.constants import PROJECT_ROOT
from src.ybis.control_plane import ControlPlaneDB
from src.ybis.services.mcp_server import MCPServer


class YBISDojo:
    """Interactive YBIS onboarding tutorial."""

    def __init__(self):
        """Initialize dojo."""
        self.db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
        self.artifacts_dir = PROJECT_ROOT / "artifacts"
        self.artifacts_dir.mkdir(exist_ok=True)
        self.completed_steps = []

    async def run(self) -> None:
        """Run the complete dojo tutorial."""
        print("=" * 70)
        print("🌌 YBIS DOJO - Welcome to the Agentic Development Platform")
        print("=" * 70)
        print()
        print("This interactive tutorial will teach you:")
        print("  1. How to create a task")
        print("  2. How to view the dashboard")
        print("  3. How to debug a failure")
        print()
        input("Press ENTER to begin...")
        print()

        # Step 1: Create a task
        await self.step_1_create_task()

        # Step 2: View dashboard
        await self.step_2_view_dashboard()

        # Step 3: Debug a failure
        await self.step_3_debug_failure()

        # Generate certificate
        await self.generate_certificate()

    async def step_1_create_task(self) -> None:
        """Step 1: Create a task."""
        print("=" * 70)
        print("STEP 1: Creating a Task")
        print("=" * 70)
        print()
        print("Tasks are the unit of work in YBIS. Let's create one!")
        print()

        # Initialize MCP server
        server = MCPServer(str(self.db_path))
        await server.initialize()

        # Create a demo task
        print("Creating task via MCP server...")
        result = await server.task_create(
            title="Dojo Demo Task",
            objective="Learn how to use the YBIS platform",
            priority="MEDIUM",
        )

        print(f"✅ Task created!")
        print(f"   Task ID: {result['task_id']}")
        print(f"   Title: {result['title']}")
        print(f"   Status: {result['status']}")
        print()

        self.completed_steps.append(
            {
                "step": 1,
                "title": "Create a Task",
                "task_id": result["task_id"],
                "completed_at": datetime.now().isoformat(),
            }
        )

        print("Key concepts:")
        print("  - Tasks are created via MCP server or control plane DB")
        print("  - Each task has a unique task_id")
        print("  - Tasks start in 'pending' status")
        print("  - Workers claim tasks and execute them")
        print()
        input("Press ENTER to continue to Step 2...")
        print()

    async def step_2_view_dashboard(self) -> None:
        """Step 2: View dashboard."""
        print("=" * 70)
        print("STEP 2: Viewing the Dashboard")
        print("=" * 70)
        print()
        print("YBIS provides multiple ways to view system state:")
        print()

        # Check if dashboard service exists
        try:
            from src.ybis.services.dashboard import main as dashboard_main

            print("📊 Streamlit Dashboard:")
            print("   Run: streamlit run src/ybis/services/dashboard.py")
            print("   URL: http://localhost:8501")
            print()
            print("   The dashboard shows:")
            print("     - Overview: Tasks, Workers, Recent Runs")
            print("     - Run Explorer: Detailed run information")
            print("     - Control: Task creation and management")
            print()
        except ImportError:
            print("⚠️  Dashboard service not available (Streamlit not installed)")
            print()

        # CLI Dashboard
        print("📋 CLI Dashboard (ybis_top):")
        print("   Run: python scripts/ybis_top.py")
        print()
        print("   The CLI dashboard shows:")
        print("     - Active Workers")
        print("     - Task Queue")
        print("     - Recent Runs")
        print()

        # Query DB directly
        print("💾 Direct DB Query:")
        db = ControlPlaneDB(self.db_path)
        await db.initialize()
        tasks = await db.get_pending_tasks()
        workers = await db.get_workers()

        print(f"   Pending Tasks: {len(tasks)}")
        print(f"   Active Workers: {len(workers)}")
        print()

        self.completed_steps.append(
            {
                "step": 2,
                "title": "View Dashboard",
                "pending_tasks": len(tasks),
                "active_workers": len(workers),
                "completed_at": datetime.now().isoformat(),
            }
        )

        print("Key concepts:")
        print("  - Dashboard provides real-time system overview")
        print("  - Multiple interfaces: Web (Streamlit), CLI (ybis_top), DB (direct)")
        print("  - All interfaces read from the same control plane DB")
        print()
        input("Press ENTER to continue to Step 3...")
        print()

    async def step_3_debug_failure(self) -> None:
        """Step 3: Debug a failure."""
        print("=" * 70)
        print("STEP 3: Debugging a Failure")
        print("=" * 70)
        print()
        print("When a task fails, YBIS provides comprehensive debugging information.")
        print()

        # Show sample log structure
        print("📁 Run Structure:")
        print("   workspaces/<task_id>/runs/<run_id>/")
        print("     ├── artifacts/")
        print("     │   ├── plan.json")
        print("     │   ├── executor_report.json")
        print("     │   ├── verifier_report.json")
        print("     │   ├── gate_report.json")
        print("     │   └── patch.diff")
        print("     └── journal/")
        print("         └── events.jsonl")
        print()

        # Show sample verifier report
        print("📄 Sample Verifier Report (verifier_report.json):")
        sample_report = {
            "task_id": "T-12345678",
            "run_id": "R-abcdefgh",
            "lint_passed": False,
            "tests_passed": True,
            "coverage": 0.85,
            "errors": ["Ruff check failed: E501 line too long"],
            "warnings": ["Function complexity: 12 (max: 10)"],
        }
        print(json.dumps(sample_report, indent=2))
        print()

        # Show sample gate report
        print("📄 Sample Gate Report (gate_report.json):")
        sample_gate = {
            "task_id": "T-12345678",
            "run_id": "R-abcdefgh",
            "verification_passed": False,
            "risk_level": "MEDIUM",
            "decision": {"value": "BLOCK", "reason": "Lint errors detected"},
        }
        print(json.dumps(sample_gate, indent=2))
        print()

        # Show sample journal event
        print("📄 Sample Journal Event (events.jsonl):")
        sample_event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": "FILE_WRITE",
            "payload": {
                "path": "src/ybis/orchestrator/planner.py",
                "source": "executor",
            },
        }
        print(json.dumps(sample_event))
        print()

        print("🔍 Debugging Workflow:")
        print("  1. Check gate_report.json for decision and reason")
        print("  2. Check verifier_report.json for lint/test errors")
        print("  3. Check executor_report.json for execution errors")
        print("  4. Check journal/events.jsonl for chronological event log")
        print("  5. Check patch.diff to see what changes were attempted")
        print()

        self.completed_steps.append(
            {
                "step": 3,
                "title": "Debug a Failure",
                "completed_at": datetime.now().isoformat(),
            }
        )

        print("Key concepts:")
        print("  - All evidence is stored in immutable run folders")
        print("  - Artifacts are the source of truth (not DB)")
        print("  - Journal provides chronological audit trail")
        print("  - Gate reports explain why a run was blocked/approved")
        print()

    async def generate_certificate(self) -> None:
        """Generate completion certificate."""
        print("=" * 70)
        print("🎓 DOJO COMPLETE - Certificate Generated")
        print("=" * 70)
        print()

        certificate = {
            "certificate_id": f"CERT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "issued_at": datetime.now().isoformat(),
            "completed_steps": self.completed_steps,
            "status": "COMPLETED",
            "message": "Congratulations! You have completed the YBIS Dojo tutorial.",
        }

        cert_path = self.artifacts_dir / "DOJO_CERTIFICATE.md"
        cert_path.write_text(
            f"""# YBIS Dojo Certificate

**Certificate ID:** {certificate['certificate_id']}
**Issued At:** {certificate['issued_at']}
**Status:** {certificate['status']}

## Completed Steps

"""
            + "\n".join(
                [
                    f"### Step {step['step']}: {step['title']}\n"
                    + f"- Completed: {step['completed_at']}\n"
                    for step in self.completed_steps
                ]
            )
            + f"""

## Message

{certificate['message']}

## Next Steps

- Read `docs/AI_START_HERE.md` for detailed documentation
- Explore `docs/INTERFACES.md` for API reference
- Check `docs/WORKFLOWS.md` for workflow details
- Run `python scripts/ybis_pulse.py` for system health check

---
*Generated by YBIS Dojo on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
""",
            encoding="utf-8",
        )

        print(f"✅ Certificate saved to: {cert_path}")
        print()
        print(cert_path.read_text())
        print()


async def main() -> None:
    """Main entry point."""
    dojo = YBISDojo()
    await dojo.run()


if __name__ == "__main__":
    asyncio.run(main())

