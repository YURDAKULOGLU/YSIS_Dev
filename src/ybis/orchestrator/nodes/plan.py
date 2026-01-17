"""
Plan Node - Generates plan using LLM planner, reading SPEC.md if available.

Includes feedback from verifier if available (feedback loop).
"""

import json
import logging

from ...constants import PROJECT_ROOT
from ...contracts import Plan, RunContext, Task, VerifierReport
from ...syscalls import write_file
from ...syscalls.journal import append_event
from ..graph import WorkflowState
from ..logging import log_node_execution
from ..planner import plan_task

logger = logging.getLogger(__name__)


@log_node_execution("plan")
def plan_node(state: WorkflowState) -> WorkflowState:
    """
    Plan node - generates plan using LLM planner, reading SPEC.md if available.

    Now includes feedback from verifier if available (feedback loop).

    Args:
        state: Workflow state

    Returns:
        Updated state
    """
    ctx = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    )

    logger.info(f"Plan node: task_id={ctx.task_id}, run_id={ctx.run_id}")

    # Load feedback from verifier if available (feedback loop)
    verifier_feedback = None
    verifier_path = ctx.verifier_report_path
    if verifier_path.exists():
        try:
            verifier_data = json.loads(verifier_path.read_text())
            verifier_report = VerifierReport(**verifier_data)
            if not verifier_report.lint_passed or not verifier_report.tests_passed:
                # Build structured feedback
                feedback_parts = []
                if verifier_report.errors:
                    feedback_parts.append("VERIFIER ERRORS:")
                    feedback_parts.extend(verifier_report.errors[:10])
                if verifier_report.warnings:
                    feedback_parts.append("\nVERIFIER WARNINGS:")
                    feedback_parts.extend(verifier_report.warnings[:10])
                if feedback_parts:
                    verifier_feedback = "\n".join(feedback_parts)
        except Exception:
            pass

    # Also check error_context from repair node
    error_context = state.get("error_context")
    if error_context and not verifier_feedback:
        verifier_feedback = error_context

    # Try to load spec if available
    spec_path = PROJECT_ROOT / "docs" / "specs" / f"{state['task_id']}_SPEC.md"
    spec_content = ""
    if spec_path.exists():
        spec_content = spec_path.read_text(encoding="utf-8")

    # Try to load plan from existing plan.json if available
    plan_path = ctx.plan_path
    if plan_path.exists():
        plan_data = json.loads(plan_path.read_text())
        plan = Plan(
            objective=plan_data.get("objective", ""),
            files=plan_data.get("files", []),
            instructions=plan_data.get("instructions", ""),
            steps=plan_data.get("steps", []),  # Include steps when loading!
        )
    else:
        # Use real planner (synchronous fallback for now)
        # In production, task would be passed via state or loaded synchronously
        # Create task object - objective should be in state or we'll use a fallback
        # The planner will query DB or use RAG to get context
        task_objective = state.get("task_objective", "Execute task")

        # If spec exists, inject it into task objective for better planning
        if spec_content:
            task_objective = f"Based on SPEC:\n{spec_content}\n\nOriginal objective: {task_objective}"

        # Get similar errors from Error Knowledge Base
        similar_errors_context = None
        try:
            from ...services.error_knowledge_base import ErrorKnowledgeBase

            error_kb = ErrorKnowledgeBase()
            # Get similar errors from previous tasks
            similar_errors = error_kb.get_similar_errors(
                step="plan",
                limit=5,
            )

            if similar_errors:
                similar_errors_context = "📚 SIMILAR ERRORS FROM PAST TASKS:\n"
                for error in similar_errors:
                    similar_errors_context += f"  - [{error.error_type}] {error.error_message[:100]}...\n"
                similar_errors_context += "\nIMPORTANT: Learn from these past errors and avoid them in your plan.\n\n"
        except Exception:
            # Error KB not critical, continue if it fails
            pass

        # Add similar errors context if available
        if similar_errors_context:
            task_objective = similar_errors_context + task_objective

        # Add verifier feedback if available (feedback loop)
        if verifier_feedback:
            task_objective += f"\n\n⚠️ FEEDBACK FROM VERIFIER (Previous Run Failed):\n{verifier_feedback}\n\n"
            task_objective += "IMPORTANT: The previous plan/implementation had these issues. Please:\n"
            task_objective += "1. Address these errors in the new plan\n"
            task_objective += "2. Ensure the plan avoids these issues\n"
            task_objective += "3. Add validation steps that would catch these errors\n"

        task = Task(
            task_id=state["task_id"],
            title="Task",
            objective=task_objective,
        )

        plan = plan_task(task, ctx)

    # Ensure steps inherit plan files when missing
    if plan.files and plan.steps:
        for step in plan.steps:
            if isinstance(step, dict) and not step.get("files"):
                step["files"] = list(plan.files)

    # Write plan to artifacts
    plan_data = {
        "task_id": state["task_id"],
        "run_id": state["run_id"],
        "objective": plan.objective,
        "files": plan.files,
        "instructions": plan.instructions,
        "steps": plan.steps if hasattr(plan, "steps") and plan.steps else [],  # Include steps!
        "referenced_context": [
            {
                "document": ctx.get("document", "")[:200] if isinstance(ctx, dict) else str(ctx)[:200],
                "metadata": ctx.get("metadata", {}) if isinstance(ctx, dict) else {},
            }
            for ctx in (plan.referenced_context if hasattr(plan, "referenced_context") else [])
        ],
    }

    plan_path = ctx.plan_path
    write_file(plan_path, json.dumps(plan_data, indent=2), ctx)

    append_event(
        ctx.run_path,
        "PLAN_CREATED",
        {
            "files": plan.files,
            "steps_count": len(plan.steps),
            "has_spec": bool(spec_content),
            "has_verifier_feedback": bool(verifier_feedback),
        },
        trace_id=ctx.trace_id,
    )

    state["status"] = "running"
    return state
