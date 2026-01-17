#!/usr/bin/env python3
"""Check quality of self-development workflow execution."""

import sys
import json
from pathlib import Path
import asyncio

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.control_plane import ControlPlaneDB

async def check_quality(task_id: str):
    """Check quality of self-development execution."""
    print("=" * 60)
    print("SELF-DEVELOPMENT QUALITY CONTROL")
    print("=" * 60)
    print(f"\nTask: {task_id}\n")
    
    # Initialize DB
    db = ControlPlaneDB("platform_data/control_plane.db")
    await db.initialize()
    
    # Get task
    try:
        task = await db.get_task(task_id)
        print(f"✅ Task found: {task.title}")
        print(f"   Status: {task.status}")
        print(f"   Priority: {task.priority}")
    except Exception as e:
        print(f"❌ Task not found: {e}")
        return
    
    # Get runs
    try:
        # Query runs for this task
        import aiosqlite
        async with aiosqlite.connect("platform_data/control_plane.db") as conn:
            conn.row_factory = aiosqlite.Row
            async with conn.execute(
                "SELECT * FROM runs WHERE task_id = ? ORDER BY created_at DESC",
                (task_id,)
            ) as cursor:
                rows = await cursor.fetchall()
                runs = [dict(row) for row in rows]
        
        print(f"\n📊 Runs: {len(runs)}")
        
        if not runs:
            print("   ⚠️  No runs found - workflow may not have started")
            return
        
        # Check latest run
        latest_run = runs[0]
        run_id = latest_run.get("run_id") or latest_run.get("run_id")
        run_status = latest_run.get("status") or latest_run.get("status")
        workflow = latest_run.get("workflow") or latest_run.get("workflow")
        run_path_str = latest_run.get("run_path") or latest_run.get("run_path")
        
        print(f"\n🔍 Latest Run: {run_id}")
        print(f"   Status: {run_status}")
        print(f"   Workflow: {workflow}")
        print(f"   Path: {run_path_str}")
        
        # Check artifacts
        run_path = Path(run_path_str)
        artifacts_dir = run_path / "artifacts"
        
        print(f"\n📦 Artifacts Check:")
        
        required_artifacts = {
            "reflection_report.json": "Reflection",
            "analysis_report.json": "Analysis",
            "proposal_report.json": "Proposal",
            "spec.md": "Spec",
            "plan.json": "Plan",
            "executor_report.json": "Execution",
            "verifier_report.json": "Verification",
            "gate_report.json": "Gate",
            "integration_report.json": "Integration",
        }
        
        artifacts_found = {}
        for artifact_name, artifact_type in required_artifacts.items():
            artifact_path = artifacts_dir / artifact_name
            if artifact_path.exists():
                artifacts_found[artifact_name] = artifact_path
                print(f"   ✅ {artifact_name} ({artifact_type})")
            else:
                print(f"   ❌ {artifact_name} ({artifact_type}) - MISSING")
        
        # Quality checks
        print(f"\n🔬 Quality Checks:")
        
        # 1. Spec quality
        if "spec.md" in artifacts_found:
            spec_path = artifacts_found["spec.md"]
            spec_content = spec_path.read_text(encoding="utf-8")
            spec_checks = {
                "Has Objective": "## Objective" in spec_content or "# Objective" in spec_content,
                "Has Requirements": "## Requirements" in spec_content or "# Requirements" in spec_content,
                "Has Acceptance": "## Acceptance" in spec_content or "Acceptance" in spec_content,
                "Has User Stories": "User Story" in spec_content or "user story" in spec_content,
                "Has Given/When/Then": "Given" in spec_content and "When" in spec_content and "Then" in spec_content,
                "Length > 500 chars": len(spec_content) > 500,
            }
            for check, passed in spec_checks.items():
                status = "✅" if passed else "❌"
                print(f"   {status} Spec: {check}")
        else:
            print(f"   ⚠️  Spec not found - cannot check quality")
        
        # 2. Plan quality
        if "plan.json" in artifacts_found:
            plan_path = artifacts_found["plan.json"]
            try:
                plan_data = json.loads(plan_path.read_text(encoding="utf-8"))
                plan_checks = {
                    "Has steps": "steps" in plan_data or "tasks" in plan_data,
                    "Has files": "files" in plan_data or any("file" in str(k).lower() for k in plan_data.keys()),
                    "Non-empty": len(str(plan_data)) > 100,
                }
                for check, passed in plan_checks.items():
                    status = "✅" if passed else "❌"
                    print(f"   {status} Plan: {check}")
            except Exception as e:
                print(f"   ❌ Plan: Invalid JSON - {e}")
        else:
            print(f"   ⚠️  Plan not found - cannot check quality")
        
        # 3. Verifier report
        if "verifier_report.json" in artifacts_found:
            verifier_path = artifacts_found["verifier_report.json"]
            try:
                verifier_data = json.loads(verifier_path.read_text(encoding="utf-8"))
                lint_passed = verifier_data.get("lint_passed", False)
                tests_passed = verifier_data.get("tests_passed", False)
                errors = verifier_data.get("errors", [])
                warnings = verifier_data.get("warnings", [])
                
                print(f"   {'✅' if lint_passed else '❌'} Verifier: Lint passed")
                print(f"   {'✅' if tests_passed else '❌'} Verifier: Tests passed")
                print(f"   {'✅' if len(errors) == 0 else '❌'} Verifier: Errors ({len(errors)})")
                print(f"   {'✅' if len(warnings) == 0 else '⚠️ '} Verifier: Warnings ({len(warnings)})")
            except Exception as e:
                print(f"   ❌ Verifier: Invalid JSON - {e}")
        else:
            print(f"   ⚠️  Verifier report not found")
        
        # 4. Gate report
        if "gate_report.json" in artifacts_found:
            gate_path = artifacts_found["gate_report.json"]
            try:
                gate_data = json.loads(gate_path.read_text(encoding="utf-8"))
                decision = gate_data.get("decision", {})
                if isinstance(decision, dict):
                    decision = decision.get("value", "UNKNOWN")
                reasons = gate_data.get("reasons", [])
                
                print(f"   {'✅' if decision == 'PASS' else '❌'} Gate: Decision = {decision}")
                if reasons:
                    print(f"   📝 Gate: Reasons ({len(reasons)})")
                    for reason in reasons[:3]:
                        print(f"      - {reason[:60]}...")
            except Exception as e:
                print(f"   ❌ Gate: Invalid JSON - {e}")
        else:
            print(f"   ⚠️  Gate report not found")
        
        # 5. Execution report
        if "executor_report.json" in artifacts_found:
            executor_path = artifacts_found["executor_report.json"]
            try:
                executor_data = json.loads(executor_path.read_text(encoding="utf-8"))
                status = executor_data.get("status", "unknown")
                changes = executor_data.get("changes", [])
                
                print(f"   {'✅' if status == 'success' else '❌'} Execution: Status = {status}")
                print(f"   📝 Execution: Changes ({len(changes)})")
                for change in changes[:3]:
                    print(f"      - {change.get('file', 'unknown')}: {change.get('action', 'unknown')}")
            except Exception as e:
                print(f"   ❌ Execution: Invalid JSON - {e}")
        else:
            print(f"   ⚠️  Execution report not found")
        
        # Summary
        print(f"\n📊 Summary:")
        total_artifacts = len(required_artifacts)
        found_artifacts = len(artifacts_found)
        print(f"   Artifacts: {found_artifacts}/{total_artifacts} ({found_artifacts*100//total_artifacts}%)")
        print(f"   Run Status: {latest_run.status}")
        
        # Summary
        print(f"\n📊 Summary:")
        print(f"   Artifacts: {found_artifacts}/{total_artifacts} ({found_artifacts*100//total_artifacts}%)")
        print(f"   Run Status: {run_status}")
        print(f"   Workflow: {workflow}")
        
        # Final quality assessment
        if run_status == "completed" and found_artifacts == total_artifacts:
            print(f"\n✅ QUALITY: PASS - All artifacts present, run completed")
        elif run_status == "completed":
            print(f"\n⚠️  QUALITY: PARTIAL - Run completed but artifacts missing")
        elif run_status == "running":
            print(f"\n⏳ QUALITY: IN PROGRESS - Run still executing")
        else:
            print(f"\n❌ QUALITY: FAIL - Run status: {run_status}")
        
    except Exception as e:
        print(f"❌ Error checking runs: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    task_id = sys.argv[1] if len(sys.argv) > 1 else "T-7db43405"
    asyncio.run(check_quality(task_id))

