#!/usr/bin/env python3
"""
Unified MCP-first orchestrator entrypoint.

Modes:
- --once: claim one task and run it (default)
- --loop: keep polling for tasks
"""
import argparse
import asyncio
import json
import os
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, os.getcwd())

from src.agentic import mcp_server
from src.agentic.core.config import (
    AUTO_GENERATE_SPEC,
    LITELLM_QUALITY,
    MIN_IMPL_SCORE,
    MIN_PLAN_SCORE,
    PROJECT_ROOT,
    REQUIRE_SPEC,
    USE_LITELLM,
    USE_SPEC_FIRST,
    VALIDATE_IMPLEMENTATION,
    VALIDATE_PLAN,
)
from src.agentic.core.graphs.orchestrator_graph import OrchestratorGraph
from src.agentic.core.plugins.aider_executor_enhanced import AiderExecutorEnhanced
from src.agentic.core.plugins.artifact_generator import ArtifactGenerator
from src.agentic.core.plugins.sentinel_enhanced import SentinelVerifierEnhanced
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.simple_planner_v2 import SimplePlannerV2
from src.agentic.core.plugins.spec_first_workflow import SpecFirstWorkflow, WorkflowConfig
from src.agentic.core.plugins.story_sharder import StorySharder  # noqa: F401 - will be used in Phase 2
from src.agentic.core.protocols import TaskState

# Optional imports for enhanced pipeline
try:
    from src.agentic.crews.planning_crew import CREWAI_AVAILABLE, PlanningCrew
except ImportError:
    CREWAI_AVAILABLE = False
    PlanningCrew = None

try:
    from src.agentic.tools.local_rag import CHROMADB_AVAILABLE, get_local_rag
except ImportError:
    CHROMADB_AVAILABLE = False
    get_local_rag = None

# Feature flags for legacy pipeline components
USE_CREWAI = os.getenv("YBIS_USE_CREWAI", "true").lower() == "true"
USE_RAG = os.getenv("YBIS_USE_RAG", "true").lower() == "true"
USE_STORY_SHARDING = os.getenv("YBIS_USE_SHARDING", "true").lower() == "true"
USE_HEALTH_CHECK = os.getenv("YBIS_HEALTH_CHECK", "true").lower() == "true"
AUTO_REMEDIATION = os.getenv("YBIS_AUTO_REMEDIATION", "false").lower() == "true"

# MCP 2025-11-25 async support is expected to be added in mcp_server upgrade.


def _workspace_paths(task_id: str) -> tuple[Path, Path, Path]:
    root = PROJECT_ROOT / "workspaces" / "active" / task_id
    docs_dir = root / "docs"
    artifacts_dir = root / "artifacts"
    return root, docs_dir, artifacts_dir


def _ensure_workspace(task_id: str) -> tuple[Path, Path, Path]:
    root, docs_dir, artifacts_dir = _workspace_paths(task_id)
    docs_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    return root, docs_dir, artifacts_dir


def _write_plan_stub(task_id: str, task_goal: str, docs_dir: Path) -> None:
    plan_path = docs_dir / "PLAN.md"
    if plan_path.exists():
        return

    frontmatter = f"""---
id: {task_id}
type: PLAN
status: DRAFT
created_at: {datetime.now().isoformat()}
token_budget: 2000
target_files: []
---
# Task: {task_goal}

## Objective

## Approach

## Steps
1.
2.
3.

## Risks & Mitigations

## Success Criteria
"""
    plan_path.write_text(frontmatter, encoding="utf-8")


def _write_result_stub(task_id: str, task_goal: str, status: str, artifacts_dir: Path) -> None:
    result_path = artifacts_dir / "RESULT.md"
    if result_path.exists() and result_path.read_text(encoding="utf-8").strip():
        return
    frontmatter = f"""---
id: {task_id}
type: RESULT
status: {status}
completed_at: {datetime.now().isoformat()}
token_budget: 2000
---
# Task Result: {task_goal}

## Summary

## Changes Made

## Files Modified

## Tests Run

## Verification

## Notes
"""
    result_path.write_text(frontmatter, encoding="utf-8")


def _claim_specific_task(task_id: str, agent_id: str) -> dict | None:
    result = mcp_server.claim_task(task_id, agent_id)
    if not str(result).startswith("SUCCESS"):
        print(result)
        return None

    tasks_payload = mcp_server.get_tasks(status="IN_PROGRESS", assignee=agent_id)
    tasks = json.loads(tasks_payload).get("tasks", [])
    for task in tasks:
        if task.get("id") == task_id:
            return task

    print(f"ERROR: Claimed task {task_id} but could not load details")
    return None


def _claim_next_task(agent_id: str) -> dict | None:
    payload = json.loads(mcp_server.claim_next_task(agent_id))
    task = payload.get("task")
    if not task:
        print(payload.get("message", "No BACKLOG tasks available"))
        return None
    return task


def _build_task_description(task: dict) -> str:
    goal = task.get("goal", "")
    details = task.get("details", "") or ""
    description = f"{goal}\n{details}".strip()
    return description


def _run_closed_loop_verification(task_id: str, files_modified: list[str]) -> bool:
    print("[Gate] Running closed-loop verification...")
    ok = True

    # Determine task tier using protocol_check.py (with --json for machine parsing)
    try:
        result = subprocess.run(
            [sys.executable, "scripts/protocol_check.py", "--task-id", task_id, "--tier", "auto", "--json"],
            check=False, capture_output=True,
            text=True,
            timeout=30
        )

        tier_info = json.loads(result.stdout)
        tier = tier_info.get("tier")

        if not tier_info.get("success", False):
            ok = False
            missing = tier_info.get("missing", [])
            print(f"[Gate] Missing artifacts: {missing}")
            return ok

    except Exception as exc:
        ok = False
        print(f"[Gate] protocol_check failed: {exc}")
        return ok

    # Tier 0: Only check RUNBOOK.md
    if tier == 0:
        runbook_path = Path("workspaces/active") / task_id / "docs" / "RUNBOOK.md"
        if not runbook_path.exists():
            print(f"[Gate] Missing artifact for {task_id}: docs/RUNBOOK.md")
            ok = False

    # Tier 1: Check RUNBOOK.md and RESULT.md
    elif tier == 1:
        runbook_path = Path("workspaces/active") / task_id / "docs" / "RUNBOOK.md"
        result_path = Path("workspaces/active") / task_id / "artifacts" / "RESULT.md"

        if not runbook_path.exists():
            print(f"[Gate] Missing artifact for {task_id}: docs/RUNBOOK.md")
            ok = False

        if not result_path.exists() or len(result_path.read_text(encoding="utf-8").strip().splitlines()) < 5:
            print("[Gate] RESULT.md must be at least 5 lines long for Tier 1 tasks.")
            ok = False

    # Tier 2 and above: Use protocol_check.py
    elif result.returncode != 0:
        ok = False
        print(result.stderr.strip())

    return ok


def _select_planner():
    """
    Select the best available planner.

    Priority:
    1. CrewAI (multi-agent) - if available and enabled
    2. SimplePlannerV2 (LiteLLM) - if enabled
    3. SimplePlanner (Ollama direct) - fallback
    """
    # Try CrewAI first (legacy pipeline restoration)
    if USE_CREWAI and CREWAI_AVAILABLE:
        try:
            print("[Planner] Using CrewAI PlanningCrew (Product Owner + Architect)")
            return PlanningCrew()
        except Exception as exc:
            print(f"[Planner] CrewAI unavailable: {exc}. Falling back.")

    # Check USE_LITELLM flag from config (YBIS_USE_LITELLM env var)
    if USE_LITELLM:
        try:
            print(f"[Planner] Using SimplePlannerV2 with LiteLLM (quality={LITELLM_QUALITY})")
            return SimplePlannerV2(quality=LITELLM_QUALITY)
        except Exception as exc:
            print(f"[Planner] LiteLLM planner unavailable: {exc}. Falling back to SimplePlanner.")
            return SimplePlanner()

    # Fallback: use manual Ollama-based SimplePlanner
    print("[Planner] Using SimplePlanner (Ollama direct)")
    return SimplePlanner()


def _enrich_context_with_rag(task_description: str) -> dict:
    """
    Enrich task context with RAG results.

    Returns dict with:
    - rag_context: Relevant code snippets
    - related_files: List of related file paths
    """
    context = {}

    if not USE_RAG or not CHROMADB_AVAILABLE or get_local_rag is None:
        return context

    try:
        rag = get_local_rag()
        if rag.is_available():
            print("[RAG] Searching for relevant context...")
            context['rag_context'] = rag.search(task_description, limit=5)
            context['related_files'] = rag.search_files(task_description, limit=3)
            print(f"[RAG] Found {len(context.get('related_files', []))} related files")
    except Exception as e:
        print(f"[RAG] Context enrichment failed: {e}")

    return context


async def _run_task(task: dict, agent_id: str) -> str:
    task_id = task["id"]
    root, docs_dir, artifacts_dir = _ensure_workspace(task_id)

    task_description = _build_task_description(task)

    # === LEGACY PIPELINE RESTORATION: RAG Context Enrichment ===
    print(f"\n[Pipeline] Starting enhanced pipeline for {task_id}")
    rag_context = _enrich_context_with_rag(task_description)
    if rag_context:
        print(f"[Pipeline] RAG context enriched: {len(rag_context.get('rag_context', ''))} chars")

    # === SPEC-FIRST WORKFLOW INTEGRATION ===
    if USE_SPEC_FIRST:
        print(f"\n[SpecFirst] Enabled - Running spec-first workflow for {task_id}")

        # Configure workflow
        spec_config = WorkflowConfig(
            require_spec=REQUIRE_SPEC,
            validate_plan=VALIDATE_PLAN,
            validate_implementation=VALIDATE_IMPLEMENTATION,
            use_llm_validation=True,
            min_plan_score=MIN_PLAN_SCORE,
            min_impl_score=MIN_IMPL_SCORE,
            auto_generate_spec=AUTO_GENERATE_SPEC,
            interactive_review=False
        )

        # Initialize workflow
        spec_workflow = SpecFirstWorkflow(config=spec_config)

        # Run spec generation/validation phase
        try:
            spec_result = await spec_workflow.execute(
                task_id=task_id,
                goal=task.get("goal", ""),
                details=task.get("details", ""),
                workspace_path=root,
                context={"agent_id": agent_id}
            )

            # Check if spec workflow failed
            if not spec_result.success and spec_result.error:
                print(f"[SpecFirst] Workflow failed: {spec_result.error}")
                if REQUIRE_SPEC:
                    print("[SpecFirst] REQUIRE_SPEC=true, aborting task")
                    mcp_server.update_task_status(task_id, "FAILED", "SPEC_VALIDATION_FAILED")
                    _write_result_stub(task_id, task.get("goal", ""), "FAILED", artifacts_dir)
                    return "FAILED"
                else:
                    print("[SpecFirst] REQUIRE_SPEC=false, continuing without spec")

            # Print warnings
            for warning in spec_result.warnings:
                print(f"[SpecFirst] Warning: {warning}")

        except Exception as exc:
            print(f"[SpecFirst] Error during spec workflow: {exc}")
            if REQUIRE_SPEC:
                print("[SpecFirst] REQUIRE_SPEC=true, aborting task")
                mcp_server.update_task_status(task_id, "FAILED", "SPEC_ERROR")
                _write_result_stub(task_id, task.get("goal", ""), "FAILED", artifacts_dir)
                return "FAILED"

    # Create plan stub only if not using spec-first or spec-first doesn't create it
    _write_plan_stub(task_id, task.get("goal", ""), docs_dir)

    # === LEGACY PIPELINE: Enrich task description with RAG context ===
    enriched_description = task_description
    if rag_context.get('rag_context'):
        enriched_description += f"\n\n=== RELEVANT CODE CONTEXT (from RAG) ===\n{rag_context['rag_context']}"
    if rag_context.get('related_files'):
        related_list = "\n".join(f"- {f}" for f in rag_context['related_files'])
        enriched_description += f"\n\n=== RELATED FILES ===\n{related_list}"

    initial_state = TaskState(
        task_id=task_id,
        task_description=enriched_description,
        artifacts_path=str(artifacts_dir)
    )

    # Select planner (CrewAI -> LiteLLM -> SimplePlanner)
    planner = _select_planner()

    orchestrator = OrchestratorGraph(
        planner=planner,
        executor=AiderExecutorEnhanced(),
        verifier=SentinelVerifierEnhanced(),
        artifact_gen=ArtifactGenerator()
    )

    try:
        final_state = await orchestrator.run_task(initial_state.model_dump())
    except Exception as exc:
        print(f"Critical Graph Failure: {exc}")
        import traceback
        traceback.print_exc()
        mcp_server.update_task_status(task_id, "FAILED", "ERROR")
        _write_result_stub(task_id, task.get("goal", ""), "FAILED", artifacts_dir)
        return "FAILED"

    if isinstance(final_state, dict):
        phase = final_state.get("phase", "unknown")
    else:
        phase = getattr(final_state, "phase", "unknown")
    status = "COMPLETED" if phase == "done" else "FAILED"

    if status == "COMPLETED":
        files_modified = []
        if isinstance(final_state, dict):
            files_modified = final_state.get("files_modified", [])
        else:
            files_modified = final_state.files_modified or []

        if not _run_closed_loop_verification(task_id, files_modified):
            status = "FAILED"
            final_status = "VERIFICATION_FAILED"
            mcp_server.update_task_status(task_id, status, final_status)
            _write_result_stub(task_id, task.get("goal", ""), final_status, artifacts_dir)
            print(f"Task Finished with status: {status}")
            return status

    final_status = "SUCCESS" if status == "COMPLETED" else "FAILED"
    mcp_server.update_task_status(task_id, status, final_status)
    if status != "COMPLETED":
        _write_result_stub(task_id, task.get("goal", ""), final_status, artifacts_dir)
    print(f"Task Finished with status: {status}")
    return status


async def run_once(task_id: str | None, agent_id: str) -> int:
    task = _claim_specific_task(task_id, agent_id) if task_id else _claim_next_task(agent_id)
    if not task:
        return 1

    status = await _run_task(task, agent_id)
    return 0 if status == "COMPLETED" else 2


async def run_loop(agent_id: str, poll_interval: int) -> int:
    while True:
        task = _claim_next_task(agent_id)
        if not task:
            await asyncio.sleep(poll_interval)
            continue
        await _run_task(task, agent_id)


def _run_startup_health_check():
    """Run system health check at startup."""
    if not USE_HEALTH_CHECK:
        return

    try:
        from src.agentic.core.plugins.health_monitor import HealthMonitor
        monitor = HealthMonitor(auto_create_tasks=AUTO_REMEDIATION)
        issues = monitor.run_all_checks()

        if issues:
            monitor.print_report()
            critical = sum(1 for i in issues if i.severity == "CRITICAL")
            if critical > 0:
                print(f"[Startup] {critical} critical issues detected - check health report")
    except Exception as e:
        print(f"[Startup] Health check failed: {e}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="YBIS MCP-first orchestrator")
    parser.add_argument("--task-id", help="Run a specific task ID")
    parser.add_argument("--agent", default=None, help="Agent ID override")
    parser.add_argument("--loop", action="store_true", help="Run continuously")
    parser.add_argument("--poll-interval", type=int, default=10, help="Loop sleep in seconds")
    parser.add_argument("--skip-health", action="store_true", help="Skip startup health check")

    args = parser.parse_args(argv)

    # Run health check at startup
    if not args.skip_health:
        _run_startup_health_check()

    agent_id = args.agent or f"codex-{socket.gethostname()}"

    if args.loop:
        asyncio.run(run_loop(agent_id, args.poll_interval))
        return 0

    return asyncio.run(run_once(args.task_id, agent_id))


if __name__ == "__main__":
    raise SystemExit(main())
