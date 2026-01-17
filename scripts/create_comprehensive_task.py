#!/usr/bin/env python3
"""
Create Comprehensive YBIS Task - Template Helper

This script helps create comprehensive, non-shallow tasks for YBIS.
"""

import sys
import asyncio
import json
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def create_comprehensive_task():
    """Interactive task creation with comprehensive template."""
    print("=" * 60)
    print("YBIS Comprehensive Task Creator")
    print("=" * 60)
    print()
    print("This tool helps you create comprehensive, non-shallow tasks.")
    print("All tasks will use the 'self_develop' workflow.")
    print()
    
    # Collect task information
    print("Task Information:")
    print("-" * 60)
    
    category = input("Category [Fix/Feature/Refactor/Integration/Docs]: ").strip() or "Fix"
    action = input("Specific Action: ").strip()
    context = input("Context (optional): ").strip()
    
    title = f"{category}: {action}"
    if context:
        title += f" {context}"
    
    print()
    print(f"Title: {title}")
    print()
    
    # Problem Statement
    print("Problem Statement:")
    print("(Describe the problem or need clearly)")
    problem = input("> ").strip()
    
    # Context
    print()
    print("Context:")
    print("(Files, modules, related issues)")
    context_details = input("> ").strip()
    
    # Requirements
    print()
    print("Requirements (one per line, empty line to finish):")
    requirements = []
    while True:
        req = input("> ").strip()
        if not req:
            break
        requirements.append(req)
    
    # Success Criteria
    print()
    print("Success Criteria (one per line, empty line to finish):")
    criteria = []
    while True:
        crit = input("> ").strip()
        if not crit:
            break
        criteria.append(crit)
    
    # Dependencies
    print()
    print("Dependencies (one per line, empty line to finish):")
    dependencies = []
    while True:
        dep = input("> ").strip()
        if not dep:
            break
        dependencies.append(dep)
    
    # Risks
    print()
    print("Risks (one per line, empty line to finish):")
    risks = []
    while True:
        risk = input("> ").strip()
        if not risk:
            break
        risks.append(risk)
    
    # Priority
    print()
    priority = input("Priority [HIGH/MEDIUM/LOW]: ").strip().upper() or "MEDIUM"
    
    # Build objective
    objective_parts = [
        "# Problem Statement",
        problem,
        "",
        "# Context",
        context_details or "N/A",
        "",
        "# Requirements"
    ]
    for i, req in enumerate(requirements, 1):
        objective_parts.append(f"{i}. {req}")
    
    objective_parts.extend([
        "",
        "# Success Criteria"
    ])
    for crit in criteria:
        objective_parts.append(f"- [ ] {crit}")
    
    if dependencies:
        objective_parts.extend([
            "",
            "# Dependencies"
        ])
        for dep in dependencies:
            objective_parts.append(f"- {dep}")
    
    if risks:
        objective_parts.extend([
            "",
            "# Risks"
        ])
        for risk in risks:
            objective_parts.append(f"- {risk}")
    
    objective = "\n".join(objective_parts)
    
    # Show summary
    print()
    print("=" * 60)
    print("Task Summary:")
    print("=" * 60)
    print(f"Title: {title}")
    print(f"Priority: {priority}")
    print(f"Objective length: {len(objective)} characters")
    print()
    print("Objective preview:")
    print("-" * 60)
    print(objective[:500])
    if len(objective) > 500:
        print("...")
    print("-" * 60)
    print()
    
    # Confirm
    confirm = input("Create this task? [y/N]: ").strip().lower()
    if confirm != 'y':
        print("Cancelled.")
        return
    
    # Connect to MCP and create task
    print()
    print("Connecting to YBIS MCP server...")
    server_params = StdioServerParameters(
        command="python",
        args=["scripts/ybis_mcp_server.py"],
        env=None,
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("Creating task...")
            result = await session.call_tool(
                "task_create",
                arguments={
                    "title": title,
                    "objective": objective,
                    "priority": priority,
                }
            )
            
            task_data = json.loads(result.content[0].text)
            task_id = task_data["task_id"]
            
            print()
            print("=" * 60)
            print("✅ Task Created Successfully!")
            print("=" * 60)
            print(f"Task ID: {task_id}")
            print(f"Title: {task_data.get('title')}")
            print(f"Status: {task_data.get('status')}")
            print()
            print("Next steps:")
            print(f"  1. Run workflow: python scripts/ybis_run.py {task_id} --workflow self_develop")
            print(f"  2. Monitor: python scripts/check_task_status.py {task_id}")
            print(f"  3. Review artifacts: workspaces/{task_id}/runs/")
            print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(create_comprehensive_task())
    except KeyboardInterrupt:
        print("\n⚠️  Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

