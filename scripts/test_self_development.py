#!/usr/bin/env python3
"""Test YBIS self-development: Use YBIS to develop itself."""

import sys
import asyncio
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.services.mcp_tools.task_tools import task_create, task_run
import json

async def test_self_development():
    """Test YBIS self-development workflow."""
    print("Testing YBIS Self-Development")
    print("=" * 50)
    print("\nQuestion: Can YBIS use itself to develop itself?")
    print("Test: Complete EvoAgentX integration using YBIS workflows\n")
    
    # Step 1: Create task via MCP
    print("Step 1: Creating self-development task...")
    task_result = await task_create(
        title="Complete EvoAgentX Integration",
        objective="Complete EvoAgentX adapter implementation: install missing dependencies (dashscope, etc.), implement real evolution using TextGradOptimizer, complete YBIS↔EvoAgentX conversion, test end-to-end evolution",
        priority="HIGH"
    )
    
    task_data = json.loads(task_result)
    task_id = task_data["task_id"]
    print(f"[OK] Task created: {task_id}")
    print(f"  Title: {task_data['title']}")
    print(f"  Objective: {task_data['objective'][:80]}...")
    
    # Step 2: Run self-development workflow
    print(f"\nStep 2: Running self-development workflow...")
    print(f"  Command: python scripts/ybis_run.py {task_id} --workflow self_develop")
    print(f"\n[INFO] This will:")
    print(f"  1. reflect - Identify EvoAgentX integration gap")
    print(f"  2. analyze - Prioritize integration")
    print(f"  3. propose - Create task objective")
    print(f"  4. spec - Generate SPEC.md")
    print(f"  5. plan - Generate PLAN.json")
    print(f"  6. execute - Install deps, implement evolution")
    print(f"  7. verify - Test integration")
    print(f"  8. gate - Check governance")
    print(f"  9. integrate - Integrate changes")
    
    print(f"\n[INFO] To run manually:")
    print(f"  python scripts/ybis_run.py {task_id} --workflow self_develop")
    
    # Step 3: Show what to check
    print(f"\nStep 3: Verification checklist:")
    print(f"  - Check workspaces/{task_id}/runs/*/artifacts/")
    print(f"    - reflection_report.json")
    print(f"    - analysis_report.json")
    print(f"    - proposal_report.json")
    print(f"    - spec.md")
    print(f"    - plan.json")
    print(f"    - executor_report.json")
    print(f"    - verifier_report.json")
    print(f"    - gate_report.json")
    print(f"    - integration_report.json")
    
    print(f"\n" + "=" * 50)
    print(f"[OK] Self-development test setup complete!")
    print(f"\nTask ID: {task_id}")
    print(f"Run: python scripts/ybis_run.py {task_id} --workflow self_develop")
    
    return task_id

if __name__ == "__main__":
    task_id = asyncio.run(test_self_development())
    print(f"\nTask ID: {task_id}")

