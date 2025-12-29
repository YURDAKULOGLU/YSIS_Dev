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
import sys
from datetime import datetime
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, os.getcwd())

from src.agentic.core.config import (
    PROJECT_ROOT,
    USE_LITELLM,
    LITELLM_QUALITY,
    USE_SPEC_FIRST,
    REQUIRE_SPEC,
    AUTO_GENERATE_SPEC,
    VALIDATE_PLAN,
    VALIDATE_IMPLEMENTATION,
    MIN_PLAN_SCORE,
    MIN_IMPL_SCORE
)
from src.agentic.core.graphs.orchestrator_graph import OrchestratorGraph
from src.agentic.core.protocols import TaskState
from src.agentic.core.llm import ProviderFactory
from src.agentic.core.plugins.simple_planner import SimplePlanner
from src.agentic.core.plugins.simple_planner_v2 import SimplePlannerV2
from src.agentic.core.plugins.aider_executor_enhanced import AiderExecutorEnhanced
from src.agentic.core.plugins.sentinel_enhanced import SentinelVerifierEnhanced
from src.agentic.core.plugins.artifact_generator import ArtifactGenerator
from src.agentic.core.plugins.spec_first_workflow import SpecFirstWorkflow, WorkflowConfig
from src.agentic import mcp_server

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
    frontmatter = f"""---
id: {task_id}
type: RESULT
status: {status}
completed_at: {datetime.now().isoformat()}
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


def _select_planner():
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


async def _run_task(task: dict, agent_id: str) -> str:
    task_id = task["id"]
    root, docs_dir, artifacts_dir = _ensure_workspace(task_id)

    task_description = _build_task_description(task)

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

    initial_state = TaskState(
        task_id=task_id,
        task_description=task_description,
        artifacts_path=str(artifacts_dir)
    )

    orchestrator = OrchestratorGraph(
        planner=_select_planner(),
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

    phase = getattr(final_state, "phase", "unknown") if not isinstance(final_state, dict) else final_state.get("phase", "unknown")
    status = "COMPLETED" if phase == "done" else "FAILED"
    final_status = "SUCCESS" if status == "COMPLETED" else "FAILED"
    mcp_server.update_task_status(task_id, status, final_status)
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="YBIS MCP-first orchestrator")
    parser.add_argument("--task-id", help="Run a specific task ID")
    parser.add_argument("--agent", default=None, help="Agent ID override")
    parser.add_argument("--loop", action="store_true", help="Run continuously")
    parser.add_argument("--poll-interval", type=int, default=10, help="Loop sleep in seconds")

    args = parser.parse_args(argv)

    agent_id = args.agent or f"codex-{socket.gethostname()}"

    if args.loop:
        asyncio.run(run_loop(agent_id, args.poll_interval))
        return 0

    return asyncio.run(run_once(args.task_id, agent_id))


if __name__ == "__main__":
    raise SystemExit(main())
