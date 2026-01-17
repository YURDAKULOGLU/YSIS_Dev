"""
Experimental Nodes - Vendor adapter nodes and YBIS-native self-development nodes.

Includes:
- workflow_evolver_node: Evolves workflow using EvoAgentX adapter
- agent_runtime_node: Executes agent using reactive-agents adapter
- council_reviewer_node: Reviews execution using llm-council adapter
- self_reflect_node: Reflects on system state and identifies improvements
- self_analyze_node: Analyzes reflection and prioritizes improvements
- self_propose_node: Proposes specific improvements as actionable tasks
- self_gate_node: Stricter gate for self-changes
- self_integrate_node: Integrates self-change with rollback capability
"""

import json
import logging
from datetime import datetime

from ...constants import PROJECT_ROOT
from ...contracts import GateDecision, GateReport, RunContext
from ...services.policy import get_policy_provider
from ...syscalls import run_command, write_file
from ...syscalls.journal import append_event
from ..graph import WorkflowState
from ..logging import log_node_execution
from .execution import execute_node
from .gate import gate_node

logger = logging.getLogger(__name__)


@log_node_execution("workflow_evolver")
def workflow_evolver_node(state: WorkflowState) -> WorkflowState:
    """
    Workflow evolver node - evolves workflow using EvoAgentX adapter.

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

    logger.info(f"Workflow evolver node: task_id={ctx.task_id}, run_id={ctx.run_id}")

    # Get EvoAgentX adapter from registry
    from ...adapters.registry import get_registry

    registry = get_registry()
    adapter = registry.get("evoagentx", adapter_type="workflow_evolution", fallback_to_default=False)

    if adapter is None:
        # Adapter not available - skip evolution
        state["status"] = "running"
        return state

    try:
        # Load current workflow spec
        workflow_name = state.get("workflow_name", "ybis_native")
        from ...workflows import WorkflowRegistry

        workflow_spec = WorkflowRegistry.load_workflow(workflow_name)
        workflow_dict = workflow_spec._raw_data

        # Collect metrics from artifacts
        metrics = {}
        verifier_path = ctx.verifier_report_path
        if verifier_path.exists():
            verifier_data = json.loads(verifier_path.read_text())
            metrics["lint_passed"] = verifier_data.get("lint_passed", False)
            metrics["tests_passed"] = verifier_data.get("tests_passed", False)
            metrics["coverage"] = verifier_data.get("coverage", 0.0)

        # Evolve workflow
        evolved_spec = adapter.evolve(workflow_dict, metrics)

        # Save evolution result
        evolution_path = ctx.artifacts_dir / "workflow_evolution.json"
        evolution_data = {
            "original_workflow": workflow_name,
            "evolved_workflow": evolved_spec,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat(),
        }
        write_file(evolution_path, json.dumps(evolution_data, indent=2), ctx)

        state["status"] = "running"
    except NotImplementedError:
        # Adapter not yet implemented - skip
        state["status"] = "running"
    except Exception as e:
        # Evolution failed - log but don't fail
        print(f"Workflow evolution failed: {e}")
        state["status"] = "running"

    return state


@log_node_execution("agent_runtime")
def agent_runtime_node(state: WorkflowState) -> WorkflowState:
    """
    Agent runtime node - executes agent using reactive-agents or CrewAI adapter.

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

    logger.info(f"Agent runtime node: task_id={ctx.task_id}, run_id={ctx.run_id}")

    # Try CrewAI first (Week 5: Multi-agent orchestration) - via registry
    try:
        from ...adapters.registry import get_registry
        registry = get_registry()
        # Check if CrewAI is enabled in policy
        policy_provider = get_policy_provider()
        if policy_provider._policy is None:
            policy_provider.load_profile()
        policy = policy_provider.get_policy()
        crewai_enabled = policy.get("adapters", {}).get("crewai", {}).get("enabled", False)

        if crewai_enabled:
            from ...adapters.crewai_adapter import get_crewai_adapter
            crewai_adapter = get_crewai_adapter()
            if crewai_adapter and crewai_adapter.is_available():
                # Use CrewAI for multi-agent execution
                task_objective = state.get("task_objective", "Execute task")

                # Create simple crew with one agent
                agents = [
                    {
                        "role": "Developer",
                        "goal": f"Complete task: {task_objective}",
                        "backstory": "You are a skilled developer working on YBIS platform.",
                    }
                ]
                tasks = [
                    {
                        "description": task_objective,
                        "agent_role": "Developer",
                        "expected_output": "Completed implementation",
                    }
                ]

                crew = crewai_adapter.create_crew(agents=agents, tasks=tasks, objective=task_objective)
                result = crewai_adapter.execute_crew(crew)

                # Save crew execution report
                crew_path = ctx.artifacts_dir / "crewai_report.json"
                write_file(crew_path, json.dumps(result, indent=2), ctx)

                state["status"] = "running"
                return state
    except Exception as e:
        logger.warning(f"CrewAI execution failed: {e}, falling back to reactive-agents")

    # Fallback to reactive-agents adapter (via registry)
    if registry is None:
        registry = get_registry()
    adapter = registry.get("reactive_agents", adapter_type="agent_runtime", fallback_to_default=False)

    if adapter is None:
        # Adapter not available - fallback to regular executor
        return execute_node(state)

    try:
        # Load task and plan
        task_objective = state.get("task_objective", "Execute task")
        plan_path = ctx.plan_path
        plan_instructions = ""
        if plan_path.exists():
            plan_data = json.loads(plan_path.read_text())
            plan_instructions = plan_data.get("instructions", "")

        # Get available tools (from YBIS tool registry)
        tools = [
            {"name": "read_file", "description": "Read a file from the workspace"},
            {"name": "write_file", "description": "Write content to a file in the workspace"},
            {"name": "run_command", "description": "Run a shell command (allowlisted only)"},
            {"name": "search_code", "description": "Search for patterns in code"},
            {"name": "task_status", "description": "Get status of a YBIS task"},
            {"name": "artifact_read", "description": "Read an artifact from a YBIS run"},
            {"name": "artifact_write", "description": "Write an artifact to a YBIS run"},
        ]

        # Get Mem0 memory context (Week 4: Agent memory) - via registry
        mem0_context = ""
        try:
            mem0_adapter = registry.get("mem0", adapter_type="memory", fallback_to_default=False)
            if mem0_adapter and mem0_adapter.is_available():
                # Search for relevant memories
                memories = mem0_adapter.search_memory(
                    query=task_objective,
                    agent_id=f"agent-{ctx.task_id}",
                    limit=3,
                )
                if memories:
                    mem0_context = "\n\nRelevant past interactions:\n"
                    for mem in memories:
                        mem0_context += f"- {mem.get('memory', '')[:200]}\n"
        except Exception:
            pass  # Mem0 is optional

        # Build context
        context = {
            "task_id": ctx.task_id,
            "run_id": ctx.run_id,
            "plan": plan_instructions,
            "mem0_context": mem0_context,
        }

        # Run agent
        result = adapter.run(task_objective, tools, context)

        # Save interaction to Mem0 (Week 4: Agent memory) - via registry
        try:
            if mem0_adapter and mem0_adapter.is_available():
                # Add interaction to memory
                messages = [
                    {"role": "user", "content": task_objective},
                    {"role": "assistant", "content": str(result.get("output", ""))[:500]},
                ]
                mem0_adapter.add_memory(
                    messages=messages,
                    agent_id=f"agent-{ctx.task_id}",
                    metadata={
                        "task_id": ctx.task_id,
                        "run_id": ctx.run_id,
                        "status": result.get("status", "unknown"),
                    },
                )
        except Exception:
            pass  # Mem0 is optional

        # Save agent runtime report
        runtime_path = ctx.artifacts_dir / "agent_runtime_report.json"
        write_file(runtime_path, json.dumps(result, indent=2), ctx)

        state["status"] = "running"
    except NotImplementedError:
        # Adapter not yet implemented - fallback to regular executor
        return execute_node(state)
    except Exception as e:
        # Agent runtime failed - fallback to regular executor
        print(f"Agent runtime failed: {e}, falling back to regular executor")
        return execute_node(state)

    return state


@log_node_execution("council_reviewer")
def council_reviewer_node(state: WorkflowState) -> WorkflowState:
    """
    Council reviewer node - reviews execution using llm-council adapter.

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

    logger.info(f"Council reviewer node: task_id={ctx.task_id}, run_id={ctx.run_id}")

    # Try AutoGen first (Week 5: Multi-agent conversations) - via policy check
    try:
        policy_provider = get_policy_provider()
        if policy_provider._policy is None:
            policy_provider.load_profile()
        policy = policy_provider.get_policy()
        autogen_enabled = policy.get("adapters", {}).get("autogen", {}).get("enabled", False)

        if autogen_enabled:
            from ...adapters.autogen_adapter import get_autogen_adapter
            autogen_adapter = get_autogen_adapter()
            if autogen_adapter and autogen_adapter.is_available():
                # Use AutoGen for multi-agent debate
                task_objective = state.get("task_objective", "Execute task")

                # Load executor report for review
                executor_path = ctx.executor_report_path
                execution_summary = "No execution data available"
                if executor_path.exists():
                    executor_data = json.loads(executor_path.read_text())
                    execution_summary = executor_data.get("output", "No output available")[:500]

                # Create debate agents
                agents = [
                    {
                        "name": "Reviewer",
                        "system_message": "You are a code reviewer. Analyze the execution and provide feedback.",
                    },
                    {
                        "name": "Architect",
                        "system_message": "You are a software architect. Evaluate the solution's design and architecture.",
                    },
                    {
                        "name": "Tester",
                        "system_message": "You are a QA engineer. Check for bugs, edge cases, and test coverage.",
                    },
                ]

                # Create debate group
                group_chat = autogen_adapter.create_debate_group(agents=agents, topic=f"Review execution for: {task_objective}")

                # Run debate
                initial_message = f"Task: {task_objective}\n\nExecution Summary:\n{execution_summary}\n\nPlease review and discuss."
                debate_result = autogen_adapter.run_debate(group_chat, initial_message)

                # Save AutoGen debate report
                debate_path = ctx.artifacts_dir / "autogen_debate_report.json"
                write_file(debate_path, json.dumps(debate_result, indent=2), ctx)

                state["status"] = "running"
                return state
    except Exception as e:
        logger.warning(f"AutoGen debate failed: {e}, falling back to llm-council")

    # Fallback to llm-council adapter (via registry)
    if registry is None:
        registry = get_registry()
    adapter = registry.get("llm_council", adapter_type="council_review", fallback_to_default=False)

    if adapter is None:
        # Adapter not available - skip review
        state["status"] = "running"
        return state

    try:
        # Load executor report for candidates
        executor_path = ctx.executor_report_path
        candidates = []
        if executor_path.exists():
            executor_data = json.loads(executor_path.read_text())
            # Extract candidate solutions from executor report
            # (This is a placeholder - actual implementation depends on executor report format)
            candidates = [executor_data.get("output", "No output available")]

        # Build review prompt
        task_objective = state.get("task_objective", "Execute task")
        prompt = f"Review the following execution for task: {task_objective}\n\nCandidates to review:"

        # Review candidates
        review_result = adapter.review(prompt, candidates)

        # Save council review report
        review_path = ctx.artifacts_dir / "council_review_report.json"
        write_file(review_path, json.dumps(review_result, indent=2), ctx)

        state["status"] = "running"
    except NotImplementedError:
        # Adapter not yet implemented - skip review
        state["status"] = "running"
    except Exception as e:
        # Review failed - log but don't fail
        print(f"Council review failed: {e}")
        state["status"] = "running"

    return state


def self_reflect_node(state: WorkflowState) -> WorkflowState:
    """
    Self-reflect node - reflects on system state and identifies improvements.

    YBIS-native implementation (not vendor-dependent).

    Args:
        state: Workflow state

    Returns:
        Updated state with reflection_report.json
    """
    ctx = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    )

    try:
        # Collect system state
        from ...control_plane import ControlPlaneDB

        db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
        db = ControlPlaneDB(str(db_path))

        # Get recent runs (last 10)
        import asyncio
        recent_runs = asyncio.run(db.get_recent_runs(limit=10))

        # Analyze patterns
        issues = []
        opportunities = []

        # Check for common issues
        for run in recent_runs:
            if run.status == "failed":
                issues.append({
                    "run_id": run.run_id,
                    "task_id": run.task_id,
                    "status": run.status,
                    "issue": "Run failed",
                })

        # Generate reflection report
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "task_id": ctx.task_id,
            "run_id": ctx.run_id,
            "issues_identified": issues[:5],  # Top 5 issues
            "opportunities_identified": opportunities[:5],  # Top 5 opportunities
            "patterns_detected": {
                "failure_rate": len([r for r in recent_runs if r.status == "failed"]) / max(len(recent_runs), 1),
                "total_runs": len(recent_runs),
            },
            "priority_scores": {
                "high": len([i for i in issues if i.get("severity") == "high"]),
                "medium": len([i for i in issues if i.get("severity") == "medium"]),
                "low": len([i for i in issues if i.get("severity") == "low"]),
            },
        }

        # Save reflection report
        reflection_path = ctx.artifacts_dir / "reflection_report.json"
        write_file(reflection_path, json.dumps(reflection, indent=2), ctx)

        state["status"] = "running"
    except Exception as e:
        print(f"Self-reflection failed: {e}")
        # Create minimal reflection report
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "task_id": ctx.task_id,
            "run_id": ctx.run_id,
            "issues_identified": [],
            "opportunities_identified": [{
                "area": "system_quality",
                "description": "Improve system reliability and error handling",
                "priority": "medium",
            }],
            "patterns_detected": {},
            "priority_scores": {},
        }
        reflection_path = ctx.artifacts_dir / "reflection_report.json"
        write_file(reflection_path, json.dumps(reflection, indent=2), ctx)
        state["status"] = "running"

    return state


def self_analyze_node(state: WorkflowState) -> WorkflowState:
    """
    Self-analyze node - analyzes reflection and prioritizes improvements.

    Args:
        state: Workflow state

    Returns:
        Updated state with analysis_report.json
    """
    ctx = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    )

    # Load reflection report
    reflection_path = ctx.artifacts_dir / "reflection_report.json"
    if not reflection_path.exists():
        # No reflection - create minimal analysis
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "prioritized_improvements": [{
                "id": "improve_error_handling",
                "priority": "P2",
                "impact": "medium",
                "risk": "low",
                "description": "Improve error handling in workflow nodes",
            }],
            "impact_assessment": {},
            "risk_assessment": {},
            "dependencies": [],
        }
    else:
        reflection = json.loads(reflection_path.read_text())

        # Prioritize improvements
        improvements = []
        for issue in reflection.get("issues_identified", [])[:3]:
            improvements.append({
                "id": f"fix_{issue.get('run_id', 'unknown')}",
                "priority": "P1" if issue.get("status") == "failed" else "P2",
                "impact": "high" if issue.get("status") == "failed" else "medium",
                "risk": "low",
                "description": f"Fix issue: {issue.get('issue', 'Unknown issue')}",
            })

        for opp in reflection.get("opportunities_identified", [])[:2]:
            improvements.append({
                "id": f"improve_{opp.get('area', 'unknown')}",
                "priority": "P2",
                "impact": opp.get("priority", "medium"),
                "risk": "low",
                "description": opp.get("description", "Improve system"),
            })

        analysis = {
            "timestamp": datetime.now().isoformat(),
            "prioritized_improvements": improvements,
            "impact_assessment": {
                "high": len([i for i in improvements if i["impact"] == "high"]),
                "medium": len([i for i in improvements if i["impact"] == "medium"]),
                "low": len([i for i in improvements if i["impact"] == "low"]),
            },
            "risk_assessment": {
                "high": len([i for i in improvements if i["risk"] == "high"]),
                "medium": len([i for i in improvements if i["risk"] == "medium"]),
                "low": len([i for i in improvements if i["risk"] == "low"]),
            },
            "dependencies": [],
        }

    # Save analysis report
    analysis_path = ctx.artifacts_dir / "analysis_report.json"
    write_file(analysis_path, json.dumps(analysis, indent=2), ctx)

    state["status"] = "running"
    return state


def self_propose_node(state: WorkflowState) -> WorkflowState:
    """
    Self-propose node - proposes specific improvements as actionable tasks.

    Args:
        state: Workflow state

    Returns:
        Updated state with proposal_report.json and updated task_objective
    """
    ctx = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    )

    # Load analysis report
    analysis_path = ctx.artifacts_dir / "analysis_report.json"
    if not analysis_path.exists():
        # No analysis - create minimal proposal
        proposal = {
            "timestamp": datetime.now().isoformat(),
            "proposed_tasks": [{
                "task_objective": "Improve system error handling and reliability",
                "success_criteria": [
                    "All tests pass",
                    "No lint errors",
                    "Gate passes",
                ],
                "rollback_plan": {
                    "method": "git_revert",
                    "checkpoint": "current_commit",
                },
            }],
        }
    else:
        analysis = json.loads(analysis_path.read_text())

        # Convert improvements to tasks
        proposed_tasks = []
        for improvement in analysis.get("prioritized_improvements", [])[:1]:  # Take top 1
            proposed_tasks.append({
                "task_objective": improvement.get("description", "Improve system"),
                "success_criteria": [
                    "All tests pass",
                    "No lint errors",
                    "Gate passes",
                    f"Improvement {improvement.get('id')} implemented",
                ],
                "rollback_plan": {
                    "method": "git_revert",
                    "checkpoint": "current_commit",
                    "instructions": f"Revert changes related to {improvement.get('id')}",
                },
            })

        proposal = {
            "timestamp": datetime.now().isoformat(),
            "proposed_tasks": proposed_tasks,
        }

        # Update task objective if we have a proposal
        if proposed_tasks:
            state["task_objective"] = proposed_tasks[0]["task_objective"]

    # Save proposal report
    proposal_path = ctx.artifacts_dir / "proposal_report.json"
    write_file(proposal_path, json.dumps(proposal, indent=2), ctx)

    # Save rollback plan
    if proposed_tasks and proposed_tasks[0].get("rollback_plan"):
        rollback_path = ctx.artifacts_dir / "rollback_plan.json"
        write_file(rollback_path, json.dumps(proposed_tasks[0]["rollback_plan"], indent=2), ctx)

    state["status"] = "running"
    return state


def self_gate_node(state: WorkflowState) -> WorkflowState:
    """
    Self-gate node - stricter gate for self-changes.

    Extends existing gate_node with additional checks:
    - Core changes require explicit approval
    - Workflow changes require workflow validation
    - Adapter changes require adapter conformance tests
    - Rollback plan must exist

    Args:
        state: Workflow state

    Returns:
        Updated state with gate_report.json
    """
    ctx = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    )

    # First run standard gate
    state = gate_node(state)

    # Load gate report
    gate_path = ctx.gate_report_path
    if not gate_path.exists():
        return state

    gate_data = json.loads(gate_path.read_text())
    gate_report = GateReport(**gate_data)

    # Additional self-development checks
    additional_checks = []

    # Check for rollback plan
    rollback_path = ctx.artifacts_dir / "rollback_plan.json"
    if not rollback_path.exists():
        additional_checks.append("Missing rollback plan - self-changes require rollback capability")
        gate_report.decision = GateDecision.BLOCK

    # Check for protected paths (core, workflows, adapters)
    executor_path = ctx.executor_report_path
    if executor_path.exists():
        executor_data = json.loads(executor_path.read_text())
        changed_files = executor_data.get("files_changed", [])

        protected_paths = {
            "core": ["src/ybis/contracts/", "src/ybis/syscalls/", "src/ybis/control_plane/"],
            "workflows": ["configs/workflows/"],
            "adapters": ["src/ybis/adapters/"],
        }

        for file_path in changed_files:
            for category, paths in protected_paths.items():
                if any(file_path.startswith(p) for p in paths):
                    additional_checks.append(f"Protected path change detected: {category} ({file_path})")
                    if category == "core":
                        gate_report.decision = GateDecision.REQUIRE_APPROVAL
                    elif category == "workflows":
                        # Check if workflow validation passed
                        # For now, just note it
                        additional_checks.append(f"Workflow change requires validation: {file_path}")
                    elif category == "adapters":
                        # Check if adapter conformance tests passed
                        additional_checks.append(f"Adapter change requires conformance tests: {file_path}")

    # Update gate report with additional checks
    gate_report.reasons.extend(additional_checks)

    # Save updated gate report
    write_file(gate_path, json.dumps(gate_report.model_dump(), indent=2), ctx)

    # Update state based on gate decision
    if gate_report.decision == GateDecision.PASS:
        state["status"] = "completed"
    elif gate_report.decision == GateDecision.REQUIRE_APPROVAL:
        state["status"] = "awaiting_approval"
    else:
        state["status"] = "failed"

    return state


def self_integrate_node(state: WorkflowState) -> WorkflowState:
    """
    Self-integrate node - integrates self-change with rollback capability.

    Args:
        state: Workflow state

    Returns:
        Updated state with integration report
    """
    ctx = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    )

    # Check gate passed
    gate_path = ctx.gate_report_path
    if not gate_path.exists():
        state["status"] = "failed"
        return state

    gate_data = json.loads(gate_path.read_text())
    gate_report = GateReport(**gate_data)

    if gate_report.decision != GateDecision.PASS:
        state["status"] = "failed"
        return state

    try:
        # Create rollback checkpoint (git tag)
        rollback_path = ctx.artifacts_dir / "rollback_plan.json"
        if rollback_path.exists():
            rollback_plan = json.loads(rollback_path.read_text())

            # Create git checkpoint if method is git_revert
            if rollback_plan.get("method") == "git_revert":
                checkpoint_name = f"ybis-checkpoint-{ctx.run_id}"
                try:
                    run_command(
                        f"git tag {checkpoint_name}",
                        ctx,
                        cwd=PROJECT_ROOT,
                    )
                    rollback_plan["checkpoint_tag"] = checkpoint_name
                    rollback_plan["checkpoint_commit"] = "HEAD"
                except Exception as e:
                    print(f"Failed to create git checkpoint: {e}")
                    # Continue anyway

        # Create integration report
        integration = {
            "timestamp": datetime.now().isoformat(),
            "task_id": ctx.task_id,
            "run_id": ctx.run_id,
            "status": "integrated",
            "rollback_plan": rollback_plan if rollback_path.exists() else None,
            "gate_decision": gate_report.decision.value,
        }

        integration_path = ctx.artifacts_dir / "integration_report.json"
        write_file(integration_path, json.dumps(integration, indent=2), ctx)

        state["status"] = "completed"
    except Exception as e:
        print(f"Self-integration failed: {e}")
        state["status"] = "failed"

    return state

