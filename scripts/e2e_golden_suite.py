#!/usr/bin/env python3
"""
Golden E2E Suite - Executes canonical scenarios and validates artifacts/gates.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import urllib.request
import uuid
from pathlib import Path
from typing import Any

import aiosqlite

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.ybis.control_plane import ControlPlaneDB
from src.ybis.contracts import Run, Task
from src.ybis.data_plane import init_run_structure
from src.ybis.orchestrator import build_workflow_graph
from src.ybis.services.policy import get_policy_provider


SCENARIO_OBJECTIVES = {
    1: (
        "Create a Currency Converter Service",
        "Implement a new service src/ybis/services/currency.py that converts USD "
        "to EUR using a hardcoded rate. Then, expose this service via a new MCP "
        "tool convert_currency in mcp_server.py.",
    ),
    2: (
        "Fix the bug in currency.py",
        "Fix the syntax error in src/ybis/services/currency.py",
    ),
    3: (
        "Expose system environment variables",
        "Create a script scripts/dump_env.py that prints environment variables "
        "using subprocess.run('env', shell=True) for debugging.",
    ),
    4: (
        "Explain the Retry Strategy",
        "Create a documentation file docs/RETRY_LOGIC.md explaining how the "
        "exponential backoff is implemented in this project.",
    ),
}


def _check_llm_endpoint(api_base: str) -> None:
    test_url = f"{api_base.rstrip('/')}/api/tags"
    with urllib.request.urlopen(test_url, timeout=2) as response:
        if response.status >= 400:
            raise RuntimeError(f"LLM endpoint returned {response.status}")


def _preflight(expected_profile: str) -> None:
    policy_provider = get_policy_provider()
    policy_provider.load_profile()

    llm_config = policy_provider.get_llm_config()
    api_base = llm_config.get("api_base", "http://localhost:11434")
    _check_llm_endpoint(api_base)

    profile = os.getenv("YBIS_PROFILE")
    if profile != expected_profile:
        raise RuntimeError(
            f"YBIS_PROFILE must be '{expected_profile}' for golden E2E runs"
        )

    if policy_provider.is_sandbox_enabled() and policy_provider.get_sandbox_type() != "local":
        raise RuntimeError("Golden E2E requires local sandbox (no cloud)")

    if not (PROJECT_ROOT / ".git").exists():
        raise RuntimeError("Not a git repository; worktree isolation is unavailable")


def _load_suite() -> dict[str, Any]:
    suite_path = PROJECT_ROOT / "tests" / "e2e" / "golden_tasks.json"
    return json.loads(suite_path.read_text(encoding="utf-8"))


def _require_artifacts(run_path: Path, required: list[str]) -> list[str]:
    missing = []
    for name in required:
        if name.startswith("journal/"):
            candidate = run_path / name
        else:
            candidate = run_path / "artifacts" / name
        if not candidate.exists():
            missing.append(name)
    return missing


def _validate_run(run_path: Path, scenario: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    artifacts_dir = run_path / "artifacts"
    gate_path = artifacts_dir / "gate_report.json"
    verifier_path = artifacts_dir / "verifier_report.json"
    executor_path = artifacts_dir / "executor_report.json"

    if not gate_path.exists():
        errors.append("gate_report.json missing")
        return errors

    gate_report = json.loads(gate_path.read_text(encoding="utf-8"))
    decision = gate_report.get("decision")
    expected_decision = scenario["expect"]["gate_decision"]
    if decision != expected_decision:
        errors.append(f"gate decision '{decision}' != expected '{expected_decision}'")

    missing = _require_artifacts(run_path, scenario["expect"]["must_include_artifacts"])
    if missing:
        errors.append(f"missing artifacts: {missing}")

    if executor_path.exists():
        executor_report = json.loads(executor_path.read_text(encoding="utf-8"))
        files_changed = executor_report.get("files_changed", [])
        if scenario["expect"].get("requires_changes") and not files_changed:
            errors.append("expected file changes but executor_report is empty")
    else:
        errors.append("executor_report.json missing")

    spec_path = PROJECT_ROOT / "docs" / "specs" / f"{scenario['task_id']}_SPEC.md"
    if not spec_path.exists():
        errors.append("spec file missing")

    if verifier_path.exists():
        verifier_report = json.loads(verifier_path.read_text(encoding="utf-8"))
        expected_fragments = scenario["expect"].get("errors_contain", [])
        if expected_fragments:
            error_text = "\n".join(verifier_report.get("errors", []))
            for fragment in expected_fragments:
                if fragment not in error_text:
                    errors.append(f"verifier errors missing fragment: {fragment}")
    else:
        errors.append("verifier_report.json missing")

    return errors


async def _create_and_run_task(title: str, objective: str) -> tuple[str, Path]:
    db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    db = ControlPlaneDB(db_path)
    await db.initialize()

    task_id = f"T-{uuid.uuid4().hex[:8]}"
    task = Task(
        task_id=task_id,
        title=title,
        objective=objective,
        status="pending",
        priority="HIGH",
    )
    await db.register_task(task)

    run_id = f"R-{uuid.uuid4().hex[:8]}"
    trace_id = f"trace-{uuid.uuid4().hex[:16]}"

    run_path = init_run_structure(task_id, run_id, trace_id=trace_id, use_git_worktree=True)

    run = Run(
        run_id=run_id,
        task_id=task_id,
        run_path=str(run_path),
        status="running",
    )
    await db.register_run(run)

    graph = build_workflow_graph()
    initial_state = {
        "task_id": task_id,
        "run_id": run_id,
        "run_path": run_path,
        "trace_id": trace_id,
        "task_objective": objective,
        "status": "pending",
        "retries": 0,
        "max_retries": 2,
        "error_context": None,
        "current_step": 0,
    }

    final_state = graph.invoke(initial_state)
    run.status = final_state["status"]

    async with aiosqlite.connect(db_path) as db_conn:
        await db_conn.execute(
            "UPDATE runs SET status = ?, completed_at = ? WHERE run_id = ?",
            (final_state["status"], None, run_id),
        )
        await db_conn.commit()

    if final_state["status"] == "awaiting_approval":
        task.status = "blocked"
    else:
        task.status = final_state["status"]
    await db.register_task(task)

    return task_id, run_path


async def main() -> int:
    suite = _load_suite()
    _preflight(suite["profile"])

    failures: list[str] = []
    for scenario in suite["scenarios"]:
        scenario_id = scenario["id"]
        title, objective = SCENARIO_OBJECTIVES[scenario_id]
        print(f"\nRunning golden scenario {scenario_id}: {scenario['name']}")

        task_id, run_path = await _create_and_run_task(title, objective)
        scenario["task_id"] = task_id

        errors = _validate_run(run_path, scenario)
        if errors:
            failures.append(f"{scenario['name']}: {errors}")
        else:
            print(f"Scenario {scenario['name']} passed")

    if failures:
        print("\nGOLDEN E2E FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("\nGOLDEN E2E SUITE PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
