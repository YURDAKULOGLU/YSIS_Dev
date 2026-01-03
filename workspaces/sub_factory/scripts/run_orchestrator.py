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
import re
import socket
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# FIX: Windows console encoding for CrewAI emojis (Constitution Section 1)
# This must be set BEFORE importing CrewAI
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
os.environ.setdefault("PYTHONUTF8", "1")

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
from src.agentic.core.utils.logging_utils import log_event
from src.agentic.core.graphs.orchestrator_graph import OrchestratorGraph        
from src.agentic.core.plugins.aider_executor_enhanced import AiderExecutorEnhanced
from src.agentic.core.plugins.artifact_generator import ArtifactGenerator
from src.agentic.core.plugins.git_manager import GitWorktreeManager
from src.agentic.core.plugins.patch_executor import PatchExecutor
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
USE_WORKTREES = os.getenv("YBIS_USE_WORKTREES", "true").lower() == "true"
WORKTREE_AUTO_CLEANUP = os.getenv("YBIS_WORKTREE_AUTO_CLEANUP", "true").lower() == "true"
WORKTREE_KEEP_BRANCH = os.getenv("YBIS_WORKTREE_KEEP_BRANCH", "true").lower() == "true"
WORKTREE_AUTO_MERGE = os.getenv("YBIS_WORKTREE_AUTO_MERGE", "true").lower() == "true"
WORKTREE_MERGE_STRATEGY = os.getenv("YBIS_WORKTREE_MERGE_STRATEGY", "squash").lower()
WORKTREE_AUTO_COMMIT = os.getenv("YBIS_WORKTREE_AUTO_COMMIT", "true").lower() == "true"
USE_REVIEW_GATE = os.getenv("YBIS_REVIEW_GATE", "true").lower() == "true"
REVIEW_GATE_MODE = os.getenv("YBIS_REVIEW_GATE_MODE", "rules").lower()
USE_FRAMEWORK_DEBATE = os.getenv("YBIS_DEBATE_FRAMEWORK", "true").lower() == "true"
EXECUTOR_MODE = os.getenv("YBIS_EXECUTOR_MODE", "aider").lower()

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


def _parse_frontmatter(content: str) -> dict[str, str]:
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    _, fm_text, _ = parts
    fm = {}
    for line in fm_text.strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fm[key.strip()] = value.strip()
    return fm


def _artifact_review(task_id: str, files_modified: list[str]) -> tuple[bool, list[str]]:
    base = Path("workspaces/active") / task_id
    issues: list[str] = []

    result_path = base / "artifacts" / "RESULT.md"
    if not result_path.exists():
        issues.append("RESULT.md missing")
    else:
        content = result_path.read_text(encoding="utf-8", errors="replace")
        if not _parse_frontmatter(content):
            issues.append("RESULT.md missing frontmatter")
        summary_match = re.search(r"## Summary\r?\n(.+?)(\r?\n## |\Z)", content, re.S)
        if not summary_match or not summary_match.group(1).strip():
            issues.append("RESULT.md Summary section is empty")

    runbook_path = base / "docs" / "RUNBOOK.md"
    if files_modified and (not runbook_path.exists() or not runbook_path.read_text(encoding="utf-8", errors="replace").strip()):
        issues.append("RUNBOOK.md must include at least one command for code changes")

    plan_path = base / "docs" / "PLAN.md"
    if plan_path.exists():
        plan_text = plan_path.read_text(encoding="utf-8", errors="replace")
        if not _parse_frontmatter(plan_text):
            issues.append("PLAN.md missing frontmatter")

    return len(issues) == 0, issues


def _is_framework_task(description: str) -> bool:
    lowered = description.lower()
    keywords = [
        "framework", "integration", "adapter", "plugin", "langgraph",
        "openhands", "aider", "crewai", "metagpt", "langfuse",
        "opentelemetry", "litellm", "council", "consensus"
    ]
    return any(word in lowered for word in keywords)


def _maybe_start_framework_debate(task_id: str, description: str, agent_id: str, docs_dir: Path) -> str | None:
    if not USE_FRAMEWORK_DEBATE:
        return None
    if not _is_framework_task(description):
        return None

    marker_path = docs_dir / "DEBATE.md"
    if marker_path.exists():
        return None

    proposal = (
        f"Framework intake for {task_id}.\\n\\n"
        "Questions:\\n"
        "1) Does this close a spine gap?\\n"
        "2) Extension or Adapter?\\n"
        "3) Deterministic gate?\\n"
        "4) Homogeneous integration?\\n"
        "5) Alternative already in system?\\n"
    )

    debate_id = None
    try:
        if hasattr(mcp_server, "start_debate"):
            result = mcp_server.start_debate(topic=f"Framework Intake: {task_id}", proposal=proposal, agent_id=agent_id)
            if isinstance(result, str) and "ID:" in result:
                debate_id = result.split("ID:")[-1].strip()
        else:
            result = mcp_server.send_message(
                to="all",
                subject=f"Framework Intake: {task_id}",
                content=proposal,
                from_agent=agent_id,
                message_type="debate",
                priority="HIGH",
                reply_to=None,
                tags="debate"
            )
            if isinstance(result, str) and "ID:" in result:
                debate_id = result.split("ID:")[-1].strip()
    except Exception as exc:
        log_event(f"Failed to start framework debate: {exc}", component="debate", level="warning")

    if debate_id:
        marker_path.write_text(f"debate_id: {debate_id}\n", encoding="utf-8")
    return debate_id


def _extract_debate_id(docs_dir: Path) -> str:
    marker_path = docs_dir / "DEBATE.md"
    if not marker_path.exists():
        return ""

    marker = marker_path.read_text(encoding="utf-8", errors="replace")
    for line in marker.splitlines():
        if line.startswith("debate_id:"):
            return line.split(":", 1)[1].strip()
    return ""


def _load_debate_summary(docs_dir: Path, max_chars: int = 1500) -> str:
    debate_id = _extract_debate_id(docs_dir)
    if not debate_id:
        return ""

    debate_path = Path("Knowledge/Messages/debates") / f"{debate_id}.json"
    if not debate_path.exists():
        return ""

    try:
        data = json.loads(debate_path.read_text(encoding="utf-8"))
    except Exception:
        return ""

    proposal = data.get("proposal", "")
    messages = data.get("messages", [])[-3:]
    parts = [f"Debate: {debate_id}"]
    if proposal:
        parts.append("Proposal:\n" + proposal)
    if messages:
        parts.append("Recent replies:")
        for msg in messages:
            author = msg.get("from", "unknown")
            content = msg.get("content", "")
            parts.append(f"- {author}: {content}")

    summary = "\n".join(parts).strip()
    if len(summary) > max_chars:
        summary = summary[:max_chars].rstrip() + "\n... [truncated]"
    return summary


def _run_council_review(task_id: str, summary: str) -> tuple[bool, str]:
    if not hasattr(mcp_server, "ask_council"):
        return True, "Council tool unavailable"
    question = (
        "Review the following task artifacts summary for quality/completeness. "
        "Respond with PASS or FAIL and a short reason.\n\n"
        f"Task: {task_id}\n\n{summary}"
    )
    try:
        response = mcp_server.ask_council(question=question, agent_id="orchestrator", use_local=True, return_stages=False)
    except Exception as exc:
        return True, f"Council review skipped: {exc}"
    if isinstance(response, str) and response.upper().startswith("COUNCIL ERROR"):
        return True, "Council review skipped: error"
    verdict = "PASS"
    if isinstance(response, str) and "FAIL" in response.upper():
        verdict = "FAIL"
    return verdict == "PASS", response if isinstance(response, str) else "Council review complete"


def _record_lesson(
    task_id: str,
    status: str,
    final_status: str,
    error_history: list[str] | None,
    files_modified: list[str],
    docs_dir: Path
) -> None:
    if status == "COMPLETED":
        return

    lessons_dir = Path("Knowledge") / "Logs"
    lessons_dir.mkdir(parents=True, exist_ok=True)

    taxonomy = {
        "SPEC_VALIDATION_FAILED": "spec",
        "SPEC_ERROR": "spec",
        "VERIFICATION_FAILED": "verification",
        "REVIEW_FAILED": "review",
        "MERGE_FAILED": "merge",
        "ERROR": "runtime",
        "FAILED": "runtime",
    }

    payload = {
        "task_id": task_id,
        "status": status,
        "final_status": final_status,
        "category": taxonomy.get(final_status, "unknown"),
        "errors": error_history or [],
        "files_modified": files_modified,
        "debate_id": _extract_debate_id(docs_dir),
        "timestamp": datetime.now().isoformat(),
    }

    try:
        path = lessons_dir / "lessons.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload) + "\n")
    except Exception as exc:
        log_event(f"Failed to record lesson: {exc}", component="lessons", level="warning")


def _record_merge_failure(
    task_id: str,
    branch_name: str,
    base_branch: str,
    error: str,
    worktree_path: Path | None,
) -> None:
    logs_dir = Path("Knowledge") / "Logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "task_id": task_id,
        "branch": branch_name,
        "base_branch": base_branch,
        "worktree_path": str(worktree_path) if worktree_path else None,
        "error": error,
        "timestamp": datetime.now().isoformat(),
    }

    try:
        path = logs_dir / "merge_failures.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload) + "\n")
    except Exception as exc:
        log_event(f"Failed to record merge failure: {exc}", component="merge_triage", level="warning")


def _claim_specific_task(task_id: str, agent_id: str) -> dict | None:
    result = mcp_server.claim_task(task_id, agent_id)
    if not str(result).startswith("SUCCESS"):
        log_event(str(result), component="task_board")
        return None

    tasks_payload = mcp_server.get_tasks(status="IN_PROGRESS", assignee=agent_id)
    tasks = json.loads(tasks_payload).get("tasks", [])
    for task in tasks:
        if task.get("id") == task_id:
            return task

    log_event(f"ERROR: Claimed task {task_id} but could not load details", component="task_board", level="error")
    return None


def _claim_next_task(agent_id: str) -> dict | None:
    payload = json.loads(mcp_server.claim_next_task(agent_id))
    task = payload.get("task")
    if not task:
        log_event(payload.get("message", "No BACKLOG tasks available"), component="task_board")
        return None
    return task


def _build_task_description(task: dict) -> str:
    goal = task.get("goal", "")
    details = task.get("details", "") or ""
    description = f"{goal}\n{details}".strip()
    return description


def _build_repo_tree(base_root: Path, max_entries: int = 60) -> str:
    """
    Build a lightweight repo tree summary for planner context.
    """
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=str(base_root)
        )
    except Exception:
        return ""

    if result.returncode != 0 or not result.stdout.strip():
        return ""

    files = [line.strip().replace("\\", "/") for line in result.stdout.splitlines() if line.strip()]
    if not files:
        return ""

    top_levels: dict[str, int] = {}
    for path in files:
        top = path.split("/", 1)[0]
        top_levels[top] = top_levels.get(top, 0) + 1

    lines = ["Top-level directories:"]
    for name, count in sorted(top_levels.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- {name}/ ({count} files)")

    lines.append("\nSample files:")
    for path in files[:max_entries]:
        lines.append(f"- {path}")

    return "\n".join(lines)


def _restore_code_root(previous_code_root: str | None) -> None:
    if previous_code_root is None:
        os.environ.pop("YBIS_CODE_ROOT", None)
    else:
        os.environ["YBIS_CODE_ROOT"] = previous_code_root


def _run_closed_loop_verification(task_id: str, files_modified: list[str]) -> bool:
    log_event("Running closed-loop verification...", component="gate")
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
            log_event(f"Missing artifacts: {missing}", component="gate", level="warning")
            return ok

    except Exception as exc:
        ok = False
        log_event(f"protocol_check failed: {exc}", component="gate", level="warning")
        return ok

    # Tier 0: Only check RUNBOOK.md
    if tier == 0:
        runbook_path = Path("workspaces/active") / task_id / "docs" / "RUNBOOK.md"
        if not runbook_path.exists():
            log_event(f"Missing artifact for {task_id}: docs/RUNBOOK.md", component="gate", level="warning")
            ok = False

    # Tier 1: Check RUNBOOK.md and RESULT.md
    elif tier == 1:
        runbook_path = Path("workspaces/active") / task_id / "docs" / "RUNBOOK.md"
        result_path = Path("workspaces/active") / task_id / "artifacts" / "RESULT.md"

        if not runbook_path.exists():
            log_event(f"Missing artifact for {task_id}: docs/RUNBOOK.md", component="gate", level="warning")
            ok = False

        if not result_path.exists() or len(result_path.read_text(encoding="utf-8").strip().splitlines()) < 5:
        log_event("RESULT.md must be at least 5 lines long for Tier 1 tasks.", component="gate", level="warning")
            ok = False

    # Tier 2 and above: Use protocol_check.py
    elif result.returncode != 0:
        ok = False
        log_event(result.stderr.strip(), component="gate", level="warning")

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
            log_event("Using CrewAI PlanningCrew (Product Owner + Architect)", component="planner")
            return PlanningCrew()
        except Exception as exc:
            log_event(f"CrewAI unavailable: {exc}. Falling back.", component="planner", level="warning")

    # Check USE_LITELLM flag from config (YBIS_USE_LITELLM env var)
    if USE_LITELLM:
        try:
            log_event(f"Using SimplePlannerV2 with LiteLLM (quality={LITELLM_QUALITY})", component="planner")
            return SimplePlannerV2(quality=LITELLM_QUALITY)
        except Exception as exc:
            log_event(f"LiteLLM planner unavailable: {exc}. Falling back to SimplePlanner.", component="planner", level="warning")
            return SimplePlanner()

    # Fallback: use manual Ollama-based SimplePlanner
    log_event("Using SimplePlanner (Ollama direct)", component="planner")
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
            log_event("Searching for relevant context...", component="rag")
            context['rag_context'] = rag.search(task_description, limit=3)
            context['related_files'] = rag.search_files(task_description, limit=3)
            log_event(f"Found {len(context.get('related_files', []))} related files", component="rag")
    except Exception as e:
        log_event(f"Context enrichment failed: {e}", component="rag", level="warning")

    return context


def _build_task_context(task_description: str, base_root: Path) -> dict:
    context = _enrich_context_with_rag(task_description)
    if context.get("rag_context") and len(context["rag_context"]) > 2000:       
        context["rag_context"] = context["rag_context"][:2000].rstrip() + "\n... [truncated]"
    repo_tree = _build_repo_tree(base_root)
    if repo_tree:
        context["repo_tree"] = repo_tree
    if context.get("related_files") and "target_files" not in context:
        context["target_files"] = list(context["related_files"])
    context.setdefault("task", task_description)
    return context


def _worktree_is_clean(path: Path) -> bool:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=str(path),
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0 and not result.stdout.strip()


async def _run_task(task: dict, agent_id: str) -> str:
    task_id = task["id"]
    root, docs_dir, artifacts_dir = _ensure_workspace(task_id)

    task_description = _build_task_description(task)
    _maybe_start_framework_debate(task_id, task_description, agent_id, docs_dir)

    worktree_manager = None
    worktree_path = None
    worktree_branch = None
    previous_code_root = os.environ.get("YBIS_CODE_ROOT")

    if USE_WORKTREES:
        try:
            worktree_manager = GitWorktreeManager(PROJECT_ROOT)
            worktree_path, worktree_branch = worktree_manager.ensure_worktree(task_id)
            os.environ["YBIS_CODE_ROOT"] = str(worktree_path)
            log_event(f"Using worktree: {worktree_path} ({worktree_branch})", component="worktree")
            if not _worktree_is_clean(worktree_path):
                log_event(f"Worktree not clean for {task_id}; aborting task.", component="worktree", level="warning")
                mcp_server.update_task_status(task_id, "FAILED", "DIRTY_WORKTREE")
                _write_result_stub(task_id, task.get("goal", ""), "DIRTY_WORKTREE", artifacts_dir)
                _restore_code_root(previous_code_root)
                return "FAILED"
        except Exception as exc:
            log_event(f"Failed to prepare worktree for {task_id}: {exc}", component="worktree", level="error")
            worktree_manager = None
            worktree_path = None
            worktree_branch = None
            os.environ.pop("YBIS_CODE_ROOT", None)

    # === LEGACY PIPELINE RESTORATION: RAG Context Enrichment ===
    log_event(f"Starting enhanced pipeline for {task_id}", component="pipeline")
    repo_root = worktree_path or PROJECT_ROOT
    rag_context = _build_task_context(task_description, repo_root)
    rag_context["repo_root"] = str(repo_root)
    rag_context["worktree_branch"] = worktree_branch
    if rag_context:
        log_event(f"RAG context enriched: {len(rag_context.get('rag_context', ''))} chars", component="pipeline")

    # === SPEC-FIRST WORKFLOW INTEGRATION ===
    if USE_SPEC_FIRST:
        log_event(f"Enabled - Running spec-first workflow for {task_id}", component="spec_first")

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
                log_event(f"Workflow failed: {spec_result.error}", component="spec_first", level="warning")
                if REQUIRE_SPEC:
                    log_event("REQUIRE_SPEC=true, aborting task", component="spec_first", level="warning")
                    mcp_server.update_task_status(task_id, "FAILED", "SPEC_VALIDATION_FAILED")
                    _write_result_stub(task_id, task.get("goal", ""), "FAILED", artifacts_dir)
                    _restore_code_root(previous_code_root)
                    return "FAILED"
                else:
                    log_event("REQUIRE_SPEC=false, continuing without spec", component="spec_first", level="warning")

            # Print warnings
            for warning in spec_result.warnings:
                log_event(f"Warning: {warning}", component="spec_first", level="warning")

        except Exception as exc:
            log_event(f"Error during spec workflow: {exc}", component="spec_first", level="warning")
            if REQUIRE_SPEC:
                log_event("REQUIRE_SPEC=true, aborting task", component="spec_first", level="warning")
                mcp_server.update_task_status(task_id, "FAILED", "SPEC_ERROR")
                _write_result_stub(task_id, task.get("goal", ""), "FAILED", artifacts_dir)
                _restore_code_root(previous_code_root)
                return "FAILED"

    # Create plan stub only if not using spec-first or spec-first doesn't create it
    _write_plan_stub(task_id, task.get("goal", ""), docs_dir)

    # === LEGACY PIPELINE: Enrich task description with RAG context ===
    enriched_description = task_description
    debate_summary = _load_debate_summary(docs_dir)
    if debate_summary:
        enriched_description += f"\n\n=== DEBATE SUMMARY ===\n{debate_summary}"
    if rag_context.get('rag_context'):
        enriched_description += f"\n\n=== RELEVANT CODE CONTEXT (from RAG) ===\n{rag_context['rag_context']}"
    if rag_context.get('related_files'):
        related_list = "\n".join(f"- {f}" for f in rag_context['related_files'])
        enriched_description += f"\n\n=== RELATED FILES ===\n{related_list}"
    if rag_context.get('repo_tree'):
        enriched_description += f"\n\n=== REPO STRUCTURE ===\n{rag_context['repo_tree']}"

    initial_state = TaskState(
        task_id=task_id,
        task_description=enriched_description,
        context=rag_context,
        artifacts_path=str(artifacts_dir)
    )

    # Select planner (CrewAI -> LiteLLM -> SimplePlanner)
    planner = _select_planner()
    executor = PatchExecutor() if EXECUTOR_MODE == "patch" else AiderExecutorEnhanced()

    orchestrator = OrchestratorGraph(
        planner=planner,
        executor=executor,
        verifier=SentinelVerifierEnhanced(),
        artifact_gen=ArtifactGenerator()
    )

    try:
        final_state = await orchestrator.run_task(initial_state.model_dump())
    except Exception as exc:
        log_event(f"Critical Graph Failure: {exc}", component="orchestrator_cli", level="error")
        import traceback
        traceback.print_exc()
        mcp_server.update_task_status(task_id, "FAILED", "ERROR")
        _write_result_stub(task_id, task.get("goal", ""), "FAILED", artifacts_dir)
        return "FAILED"
    finally:
        _restore_code_root(previous_code_root)

    if isinstance(final_state, dict):
        phase = final_state.get("phase", "unknown")
    else:
        phase = getattr(final_state, "phase", "unknown")
    status = "COMPLETED" if phase == "done" else "FAILED"
    files_modified: list[str] = []

    if status == "COMPLETED":
        if isinstance(final_state, dict):
            files_modified = final_state.get("files_modified", [])
        else:
            files_modified = final_state.files_modified or []

        if not _run_closed_loop_verification(task_id, files_modified):
            status = "FAILED"
            final_status = "VERIFICATION_FAILED"
            mcp_server.update_task_status(task_id, status, final_status)
            _write_result_stub(task_id, task.get("goal", ""), final_status, artifacts_dir)
            log_event(f"Task Finished with status: {status}", component="orchestrator_cli")
            return status

        if USE_REVIEW_GATE:
            review_ok, review_issues = _artifact_review(task_id, files_modified)
            if not review_ok:
                status = "FAILED"
                final_status = "REVIEW_FAILED"
                mcp_server.update_task_status(task_id, status, final_status)
                _write_result_stub(task_id, task.get("goal", ""), final_status, artifacts_dir)
                log_event(f"Failed: {review_issues}", component="review", level="warning")
                log_event(f"Task Finished with status: {status}", component="orchestrator_cli")
                return status

            if REVIEW_GATE_MODE == "council":
                review_summary = "\n".join([
                    f"RESULT.md: {task_id}",
                    f"Files modified: {len(files_modified)}",
                    "Review status: rules passed"
                ])
                council_ok, council_note = _run_council_review(task_id, review_summary)
                if not council_ok:
                    status = "FAILED"
                    final_status = "REVIEW_FAILED"
                    mcp_server.update_task_status(task_id, status, final_status)
                    _write_result_stub(task_id, task.get("goal", ""), final_status, artifacts_dir)
                    log_event(f"Council failed: {council_note}", component="review", level="warning")
                    log_event(f"Task Finished with status: {status}", component="orchestrator_cli")
                    return status
                log_event(f"Council: {council_note}", component="review")

    merge_ok = True
    if (
        status == "COMPLETED"
        and WORKTREE_AUTO_MERGE
        and worktree_manager
        and worktree_branch
    ):
        try:
            worktree_manager.merge_worktree_branch(
                task_id=task_id,
                branch_name=worktree_branch,
                strategy=WORKTREE_MERGE_STRATEGY,
                auto_commit=WORKTREE_AUTO_COMMIT,
            )
            log_event(f"Merged {worktree_branch} into {worktree_manager.base_branch}", component="worktree")
        except Exception as exc:
            merge_ok = False
            status = "FAILED"
            final_status = "MERGE_FAILED"
            mcp_server.update_task_status(task_id, status, final_status)
            _write_result_stub(task_id, task.get("goal", ""), final_status, artifacts_dir)
            _record_merge_failure(
                task_id=task_id,
                branch_name=worktree_branch,
                base_branch=worktree_manager.base_branch,
                error=str(exc),
                worktree_path=worktree_path,
            )
            log_event(f"Merge failed for {task_id}: {exc}", component="worktree", level="error")

    final_status = "SUCCESS" if status == "COMPLETED" else "FAILED"
    mcp_server.update_task_status(task_id, status, final_status)
    if status != "COMPLETED":
        _write_result_stub(task_id, task.get("goal", ""), final_status, artifacts_dir)
        errors = []
        if isinstance(final_state, dict):
            errors = final_state.get("error_history", [])
        else:
            errors = getattr(final_state, "error_history", []) or []
        _record_lesson(task_id, status, final_status, errors, files_modified, docs_dir)
    if status == "COMPLETED" and merge_ok and worktree_manager and worktree_path and WORKTREE_AUTO_CLEANUP:
        try:
            worktree_manager.cleanup_worktree(
                task_id,
                worktree_branch,
                keep_branch=WORKTREE_KEEP_BRANCH,
                force=False
            )
            log_event(f"Cleaned up worktree {worktree_path}", component="worktree")
        except Exception as exc:
            log_event(f"Cleanup failed for {task_id}: {exc}", component="worktree", level="warning")
    log_event(f"Task Finished with status: {status}", component="orchestrator_cli")
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
                log_event(f"{critical} critical issues detected - check health report", component="startup", level="warning")
    except Exception as e:
        log_event(f"Health check failed: {e}", component="startup", level="warning")


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
