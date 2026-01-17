#!/usr/bin/env python3
"""
YBIS System Pulse - Health check script.

Verifies:
- DB connection
- MCP Server response
- Ollama connection
- End-to-end dummy task execution

Generates SYSTEM_HEALTH_REPORT.md
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


class HealthCheck:
    """System health checker."""

    def __init__(self):
        """Initialize health checker."""
        self.results = {}
        self.db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"

    async def check_db(self) -> bool:
        """Check database connection."""
        try:
            db = ControlPlaneDB(self.db_path)
            await db.initialize()
            # Try a simple query
            tasks = await db.get_pending_tasks()
            self.results["db"] = {"status": "GREEN", "message": f"DB connected, {len(tasks)} pending tasks"}
            return True
        except Exception as e:
            self.results["db"] = {"status": "RED", "message": f"DB connection failed: {str(e)}"}
            return False

    async def check_mcp(self) -> bool:
        """Check MCP server."""
        try:
            server = MCPServer(db_path=str(self.db_path))
            await server.initialize()
            tools = server.get_tools()
            self.results["mcp"] = {"status": "GREEN", "message": f"MCP server ready, {len(tools)} tools available"}
            return True
        except Exception as e:
            self.results["mcp"] = {"status": "RED", "message": f"MCP server failed: {str(e)}"}
            return False

    async def check_ollama(self) -> bool:
        """Check Ollama connection."""
        try:
            import litellm

            response = litellm.completion(
                model="ollama/llama3.2:3b",
                messages=[{"role": "user", "content": "hi"}],
                api_base="http://localhost:11434",
            )
            result = response.choices[0].message.content
            self.results["ollama"] = {"status": "GREEN", "message": f"Ollama connected, response: {result[:50]}..."}
            return True
        except ImportError:
            self.results["ollama"] = {"status": "YELLOW", "message": "LiteLLM not installed"}
            return False
        except Exception as e:
            self.results["ollama"] = {"status": "RED", "message": f"Ollama connection failed: {str(e)}"}
            return False

    async def check_e2e_task(self) -> bool:
        """Check end-to-end task execution."""
        try:
            # Create a dummy task
            server = MCPServer(db_path=str(self.db_path))
            await server.initialize()

            task_result = await server.task_create(
                title="Pulse Test Task",
                objective="This is a health check dummy task",
                priority="LOW",
            )
            task_id = task_result["task_id"]

            # Claim task
            claim_result = await server.task_claim(worker_id="pulse-worker")
            if not claim_result.get("task_id"):
                self.results["e2e"] = {"status": "YELLOW", "message": "Task created but not claimed (may be expected)"}
                return False

            claimed_task_id = claim_result.get("task_id")
            run_id = claim_result.get("run_id")

            # Write artifact
            executor_report = {
                "task_id": claimed_task_id,
                "run_id": run_id,
                "success": True,
                "files_changed": [],
                "commands_run": ["pulse-check"],
                "outputs": {"pulse-check": "Health check passed"},
                "error": None,
            }
            await server.artifact_write(
                run_id=run_id,
                name="executor_report.json",
                content=json.dumps(executor_report, indent=2),
            )

            # Complete task
            await server.task_complete(
                task_id=claimed_task_id,
                run_id=run_id,
                status="completed",
                result_summary="Health check completed successfully",
                worker_id="pulse-worker",
            )

            self.results["e2e"] = {
                "status": "GREEN",
                "message": f"E2E task completed: {task_id}",
            }
            return True

        except Exception as e:
            self.results["e2e"] = {"status": "RED", "message": f"E2E task failed: {str(e)}"}
            return False

    async def run_all_checks(self) -> dict:
        """Run all health checks."""
        print("Running YBIS System Pulse...")
        print()

        await self.check_db()
        await self.check_mcp()
        await self.check_ollama()
        await self.check_e2e_task()

        return self.results

    def generate_report(self) -> str:
        """Generate health report markdown."""
        report_lines = []
        report_lines.append("# YBIS System Health Report")
        report_lines.append(f"Generated: {datetime.now().isoformat()}")
        report_lines.append("")
        report_lines.append("## System Status")
        report_lines.append("")

        all_green = True
        for component, result in self.results.items():
            status = result["status"]
            message = result["message"]
            status_emoji = {"GREEN": "✅", "YELLOW": "⚠️", "RED": "❌"}.get(status, "❓")
            report_lines.append(f"### {component.upper()}")
            report_lines.append(f"{status_emoji} **{status}**: {message}")
            report_lines.append("")

            if status != "GREEN":
                all_green = False

        report_lines.append("## Summary")
        if all_green:
            report_lines.append("✅ **ALL SYSTEMS GREEN** - System is production ready.")
        else:
            report_lines.append("⚠️ **SOME SYSTEMS NEED ATTENTION** - Review status above.")

        return "\n".join(report_lines)


async def main() -> None:
    """Main entry point."""
    checker = HealthCheck()
    results = await checker.run_all_checks()

    # Print results
    print("Health Check Results:")
    print("=" * 60)
    for component, result in results.items():
        status = result["status"]
        message = result["message"]
        print(f"{component.upper()}: {status} - {message}")

    # Generate report
    report = checker.generate_report()
    report_path = PROJECT_ROOT / "SYSTEM_HEALTH_REPORT.md"
    report_path.write_text(report, encoding="utf-8")

    print()
    print(f"Report saved to: {report_path}")

    # Exit code
    all_green = all(r["status"] == "GREEN" for r in results.values())
    sys.exit(0 if all_green else 1)


if __name__ == "__main__":
    asyncio.run(main())

