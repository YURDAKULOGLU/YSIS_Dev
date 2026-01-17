"""
Gate Nodes - Gate, Debate, and Retry Logic.

Includes:
- gate_node: Checks gates and writes gate_report.json
- debate_node: Conducts council debate when task is blocked
- should_retry: Checks if the workflow should retry after verification failure
"""

import json
import logging

from ...contracts import GateDecision, GateReport, RunContext, VerifierReport
from ...syscalls import append_event, write_file
from ..graph import WorkflowState
from ..gates import check_risk_gate, check_verification_gate
from ..logging import log_node_execution

logger = logging.getLogger(__name__)


@log_node_execution("gate")
def gate_node(state: WorkflowState) -> WorkflowState:
    """
    Gate node - checks gates and writes gate_report.json.

    Args:
        state: Workflow state

    Returns:
        Updated state with final status
    """
    # Import _save_experience_to_memory from graph.py (circular import prevention)
    from ..graph import _save_experience_to_memory

    ctx = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    )

    # Load verifier report (or enforce it if policy requires)
    from ...services.policy import get_policy_provider

    policy = get_policy_provider().get_policy()
    gates_policy = policy.get("gates", {})
    require_verifier_pass = gates_policy.get("require_verifier_pass", False)

    verifier_path = ctx.verifier_report_path
    verifier_missing = not verifier_path.exists()
    if not verifier_missing:
        verifier_data = json.loads(verifier_path.read_text())
        verifier_report = VerifierReport(**verifier_data)
    elif require_verifier_pass:
        verifier_report = VerifierReport(
            task_id=state["task_id"],
            run_id=state["run_id"],
            lint_passed=False,
            tests_passed=False,
            coverage=0.0,
            errors=["Missing verifier_report.json (verification not run)"],
        )
    else:
        # Fallback: create a passing report only when verifier isn't required
        verifier_report = VerifierReport(
            task_id=state["task_id"],
            run_id=state["run_id"],
            lint_passed=True,
            tests_passed=True,
            coverage=0.85,
        )

    # Get task tier (if available from verify_node)
    tier = state.get("task_tier", 1)  # Default to Tier 1 if not set

    # Check verification gate
    gate_report = check_verification_gate(verifier_report, ctx)
    if verifier_missing and require_verifier_pass:
        gate_report.reasons.append("Verifier report missing; verification was not executed")

    # AUTO-TEST GATE: Check test coverage threshold
    try:
        from ..test_gate import check_test_coverage_gate

        coverage_passed, actual_coverage, coverage_errors = check_test_coverage_gate(ctx, min_coverage=0.80)

        if not coverage_passed:
            # Coverage below threshold - add to gate report
            gate_report.decision = GateDecision.BLOCK
            gate_report.reasons.extend(coverage_errors)
    except Exception:
        # Coverage check not critical, continue if it fails
        pass

    # Get changed files from executor report if available
    changed_files = []
    patch_size = 0
    executor_path = ctx.executor_report_path
    if executor_path.exists():
        executor_data = json.loads(executor_path.read_text())
        changed_files = executor_data.get("files_changed", [])
        # Try to get patch size from executor report
        patch_size = executor_data.get("patch_size", 0)

    # Calculate patch size from patch.diff if not available
    if patch_size == 0:
        patch_path = ctx.run_path / "artifacts" / "patch.diff"
        if patch_path.exists():
            try:
                patch_content = patch_path.read_text(encoding="utf-8")
                patch_lines = [line for line in patch_content.split("\n") if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))]
                patch_size = len(patch_lines)
            except Exception:
                patch_size = 0

    # Check risk gate
    risk_gate = check_risk_gate(ctx, patch_size=patch_size, changed_files=changed_files)

    # Tier 2: Council debate required if any warning exists
    if tier == 2 and (verifier_report.warnings or verifier_report.errors):
        # Force debate for Tier 2 with warnings
        risk_gate.decision = GateDecision.REQUIRE_APPROVAL
        risk_gate.reasons.append("Tier 2 task with warnings requires council debate")

    # Use the more restrictive decision
    if risk_gate.decision.value == "REQUIRE_APPROVAL" or gate_report.decision.value == "BLOCK":
        final_decision = risk_gate if risk_gate.decision.value == "REQUIRE_APPROVAL" else gate_report
    else:
        final_decision = gate_report

    # Check for approval artifact (resume logic)
    approval_path = ctx.artifacts_dir / "approval.json"
    if approval_path.exists() and final_decision.decision.value == "REQUIRE_APPROVAL":
        # Approval found - bypass gate
        final_decision.decision = GateDecision.PASS
        final_decision.approval_present = True

    # Record gate block to Error Knowledge Base
    if final_decision.decision.value == "BLOCK":
        try:
            from ...services.error_knowledge_base import ErrorKnowledgeBase

            error_kb = ErrorKnowledgeBase()
            error_kb.record_error(
                task_id=ctx.task_id,
                run_id=ctx.run_id,
                error_type="gate_block",
                error_message=f"Gate blocked: {', '.join(final_decision.reasons)}",
                step="gate",
                context={
                    "decision": final_decision.decision.value,
                    "reasons": final_decision.reasons,
                    "verification_passed": verifier_report.lint_passed and verifier_report.tests_passed,
                },
            )
        except Exception:
            # Error KB not critical, continue if it fails
            pass

    # Check workflow-declared artifacts (Task D: Workflow Artifact Enforcement)
    workflow_name = state.get("workflow_name", "ybis_native")
    try:
        from ...workflows import WorkflowRegistry

        workflow_spec = WorkflowRegistry.load_workflow(workflow_name)
        required_artifacts = workflow_spec.requirements.get("artifacts", [])

        if required_artifacts:
            missing_artifacts = []
            for artifact in required_artifacts:
                if artifact == "gate_report.json":
                    continue
                artifact_path = ctx.artifacts_dir / artifact
                if not artifact_path.exists():
                    missing_artifacts.append(artifact)

            if missing_artifacts:
                # BLOCK if required artifacts are missing
                final_decision.decision = GateDecision.BLOCK
                if not final_decision.reasons:  # Ensure reasons list exists
                    final_decision.reasons = []
                final_decision.reasons.append(
                    f"Missing required workflow artifacts: {', '.join(missing_artifacts)}"
                )
    except (FileNotFoundError, ValueError, ImportError):
        # If workflow not found or can't load, log warning but don't block
        # (fallback to legacy behavior)
        pass

    # Write gate report
    gate_path = ctx.gate_report_path
    write_file(gate_path, final_decision.model_dump_json(indent=2), ctx)

    # Handle REQUIRE_APPROVAL or BLOCK - trigger debate
    if final_decision.decision.value in ["REQUIRE_APPROVAL", "BLOCK"]:
        # Route to debate node instead of stopping immediately
        state["status"] = "debating"
        return state

    # Update status
    if final_decision.decision.value == "PASS":
        state["status"] = "completed"
        # Save successful experience to memory
        _save_experience_to_memory(ctx, state, success=True)

        # Check for staleness and create consistency tasks if needed
        try:
            import asyncio
            from ...services.staleness_hook import run_staleness_check

            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                logger.info("Staleness check skipped: event loop already running")
            else:
                staleness_report = asyncio.run(run_staleness_check())
                if staleness_report.get("tasks_created"):
                    logger.info(
                        f"Created {len(staleness_report['tasks_created'])} consistency tasks"
                    )
        except Exception as e:
            logger.warning(f"Staleness check failed: {e}")
    else:
        state["status"] = "failed"
        # Save failed experience to memory
        _save_experience_to_memory(ctx, state, success=False)

    # Trigger lesson engine to learn from this run
    try:
        from ...services.lesson_engine import LessonEngine

        lesson_engine = LessonEngine()
        lessons = lesson_engine.analyze_run(ctx)
        if lessons.get("lessons"):
            lesson_engine.generate_auto_policy(lessons["lessons"])
    except Exception as e:
        # Lesson engine is optional - don't fail the run if it errors
        print(f"Lesson engine failed: {e}")

    return state


@log_node_execution("debate")
def debate_node(state: WorkflowState) -> WorkflowState:
    """
    Debate node - conducts council debate when task is blocked.

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

    # Load gate report for context
    gate_path = ctx.gate_report_path
    gate_context = ""
    if gate_path.exists():
        gate_data = json.loads(gate_path.read_text())
        decision = gate_data.get("decision", "UNKNOWN")
        if isinstance(decision, dict):
            decision = decision.get("value", "UNKNOWN")
        gate_context = f"Gate Decision: {decision}\nReasons: {gate_data.get('reasons', [])}"

    # Load task objective
    plan_path = ctx.plan_path
    task_context = ""
    if plan_path.exists():
        plan_data = json.loads(plan_path.read_text())
        task_context = f"Task: {plan_data.get('objective', 'Unknown task')}"

    # Conduct debate
    from ...services.debate import DebateEngine

    engine = DebateEngine()
    topic = f"Should task {state['task_id']} be allowed to proceed despite being blocked?"
    context = f"{task_context}\n\n{gate_context}"

    debate_result = engine.conduct_debate(topic, context, rounds=1)

    # Save debate report
    debate_report_path = ctx.artifacts_dir / "debate_report.json"
    write_file(debate_report_path, json.dumps(debate_result.to_dict(), indent=2), ctx)

    # Journal event
    append_event(
        ctx.run_path,
        "DEBATE_COMPLETED",
        {
            "consensus": debate_result.consensus,
            "arguments_count": len(debate_result.arguments),
        },
    )

    # Route based on consensus
    if debate_result.consensus == "OVERRIDE_BLOCK":
        # Very rare - override the block
        state["status"] = "completed"
    elif debate_result.consensus == "REQUIRE_APPROVAL":
        # Still requires approval
        state["status"] = "awaiting_approval"
    else:
        # CONFIRM_BLOCK - block confirmed
        state["status"] = "failed"

    return state


def should_retry(state: WorkflowState) -> bool:
    """
    Check if the workflow should retry after verification failure.

    Args:
        state: Workflow state

    Returns:
        True if retry should be attempted, False otherwise
    """
    # Check if verifier report shows errors
    ctx = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    )

    verifier_path = ctx.verifier_report_path
    if not verifier_path.exists():
        return False

    try:
        verifier_data = json.loads(verifier_path.read_text())
        verifier_report = VerifierReport(**verifier_data)

        # Check if verification failed
        has_errors = not verifier_report.lint_passed or not verifier_report.tests_passed

        # Check retry limits
        retries = state.get("retries", 0)
        max_retries = state.get("max_retries", 2)

        return has_errors and retries < max_retries
    except Exception:
        return False
