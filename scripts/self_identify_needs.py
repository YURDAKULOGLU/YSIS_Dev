#!/usr/bin/env python3
"""
Self-Identify System Needs - Use YBIS to identify its own needs.

This script creates a comprehensive task for YBIS to reflect on itself,
identify gaps, and propose improvements.
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


async def create_self_reflection_task():
    """Create a comprehensive task for YBIS to identify its own needs."""
    print("=" * 60)
    print("YBIS Self-Reflection: Identifying System Needs")
    print("=" * 60)
    print()
    
    # Comprehensive task objective
    objective = """
# Problem Statement
YBIS needs to identify its own gaps, needs, and improvement opportunities.
This includes checking observability (logging, monitoring, tracing, metrics),
workflow completeness, adapter coverage, governance enforcement, and overall
system health.

# Context
- System: YBIS (Yapay Zeka Destekli İşletim Sistemi)
- Current state: Self-development workflow exists, logging implemented
- Need: Comprehensive self-assessment and gap identification

# Requirements
1. Reflect on current system state:
   - Check observability completeness (logging, monitoring, tracing, metrics)
   - Check workflow coverage (all workflows working?)
   - Check adapter coverage (all adapters registered and working?)
   - Check governance enforcement (gates, approvals working?)
   - Check documentation completeness
   - Check test coverage
   - Check performance metrics

2. Identify gaps and needs:
   - Missing observability features (graph visualization, real-time monitoring, etc.)
   - Incomplete workflows or nodes
   - Missing adapters or adapter issues
   - Governance gaps
   - Documentation gaps
   - Test coverage gaps
   - Performance issues

3. Prioritize improvements:
   - Critical gaps (blocking or high-risk)
   - Important improvements (quality of life)
   - Nice-to-have features

4. Generate comprehensive report:
   - Current state assessment
   - Gap analysis
   - Prioritized improvement list
   - Implementation recommendations

# Success Criteria
- [ ] Comprehensive reflection report generated
- [ ] All observability features checked (logging, monitoring, tracing, metrics)
- [ ] All workflows checked for completeness
- [ ] All adapters checked for availability and issues
- [ ] Governance enforcement verified
- [ ] Gap analysis completed
- [ ] Prioritized improvement list created
- [ ] Implementation recommendations provided

# Dependencies
- Self-development workflow (`self_develop`)
- Reflection node (`self_reflect`)
- Analysis node (`self_analyze`)
- Proposal node (`self_propose`)

# Risks
- Risk: Reflection may miss some gaps
  Mitigation: Use comprehensive checklist and multiple reflection passes
- Risk: Too many improvements identified
  Mitigation: Prioritize and focus on critical gaps first

# Implementation Notes
- Use `self_develop` workflow
- Start with `self_reflect` node to analyze current state
- Use `self_analyze` to identify gaps
- Use `self_propose` to create improvement tasks
- Generate artifacts: reflection_report.json, analysis_report.json, proposal_report.json
"""
    
    title = "Self-Reflection: Identify System Needs and Gaps"
    priority = "HIGH"
    
    print("Creating comprehensive self-reflection task...")
    print(f"Title: {title}")
    print(f"Priority: {priority}")
    print()
    
    # Connect to MCP and create task
    server_params = StdioServerParameters(
        command="python",
        args=["scripts/ybis_mcp_server.py"],
        env=None,
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            print("Creating task via MCP...")
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
            print("✅ Self-Reflection Task Created!")
            print("=" * 60)
            print(f"Task ID: {task_id}")
            print(f"Title: {task_data.get('title')}")
            print(f"Status: {task_data.get('status')}")
            print()
            print("Next steps:")
            print(f"  1. Run workflow: python scripts/ybis_run.py {task_id} --workflow self_develop")
            print(f"  2. Monitor: python scripts/check_task_status.py {task_id}")
            print(f"  3. Review artifacts: workspaces/{task_id}/runs/")
            print()
            print("This task will:")
            print("  - Reflect on system state")
            print("  - Identify gaps and needs")
            print("  - Prioritize improvements")
            print("  - Generate comprehensive report")
            print("=" * 60)
            
            return task_id


if __name__ == "__main__":
    try:
        task_id = asyncio.run(create_self_reflection_task())
        print(f"\n✅ Task created: {task_id}")
        print(f"\nTo run: python scripts/ybis_run.py {task_id} --workflow self_develop")
    except KeyboardInterrupt:
        print("\n⚠️  Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

