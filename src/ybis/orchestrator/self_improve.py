"""
Self-Improve Workflow Nodes - YBIS-native proactive self-improvement.

This implements the reflect → plan → implement → test → integrate loop
without external adapter dependencies, with automatic repair loops.
"""

import json
import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path

from ..constants import PROJECT_ROOT
from ..contracts import Plan, RunContext, Task
from ..services.reflection_engine import ReflectionEngine
from ..syscalls import write_file
from ..syscalls.journal import append_event
from .graph import WorkflowState
from .planner import LLMPlanner
from .verifier import run_verifier

logger = logging.getLogger(__name__)


def _fix_pyproject_toml_deprecated_settings(project_root: Path, worktree_path: Path | None = None) -> bool:
    """
    Fix deprecated ruff settings in pyproject.toml.
    
    Moves top-level 'select' and 'ignore' to [tool.ruff.lint] section.
    
    Args:
        project_root: Project root directory (fallback)
        worktree_path: Worktree path (preferred, if available)
        
    Returns:
        True if fixed successfully
    """
    # Prefer worktree path if available (repair should fix worktree, not main project)
    if worktree_path and (worktree_path / "pyproject.toml").exists():
        toml_path = worktree_path / "pyproject.toml"
    else:
        toml_path = project_root / "pyproject.toml"
    
    if not toml_path.exists():
        return False
    
    try:
        content = toml_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        
        # Find [tool.ruff] section and check if select/ignore are at top level
        ruff_section_start = None
        lint_section_start = None
        select_line = None
        ignore_line = None
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped == "[tool.ruff]":
                ruff_section_start = i
            elif stripped == "[tool.ruff.lint]":
                lint_section_start = i
            elif ruff_section_start is not None and lint_section_start is None:
                # Check if select/ignore are in [tool.ruff] but not in [tool.ruff.lint]
                if stripped.startswith("select ="):
                    select_line = i
                elif stripped.startswith("ignore ="):
                    ignore_line = i
        
        # If we found deprecated settings, move them
        if select_line is not None or ignore_line is not None:
            # Ensure [tool.ruff.lint] section exists
            if lint_section_start is None:
                # Find end of [tool.ruff] section
                ruff_section_end = len(lines)
                for i in range(ruff_section_start + 1, len(lines)):
                    if lines[i].strip().startswith("[") and not lines[i].strip().startswith("#"):
                        ruff_section_end = i
                        break
                
                # Insert [tool.ruff.lint] section
                lines.insert(ruff_section_end, "")
                lines.insert(ruff_section_end, "[tool.ruff.lint]")
                lint_section_start = ruff_section_end
                # Adjust line numbers for select/ignore
                if select_line and select_line >= ruff_section_end:
                    select_line += 2
                if ignore_line and ignore_line >= ruff_section_end:
                    ignore_line += 2
            
            # Move select and ignore to lint section
            new_lines = []
            moved_lines = []
            
            for i, line in enumerate(lines):
                if i == select_line or i == ignore_line:
                    # Skip original line, will add to lint section
                    moved_lines.append(line)
                    continue
                elif i == lint_section_start + 1:
                    # Insert after [tool.ruff.lint]
                    new_lines.append(line)
                    # Add moved lines
                    for moved_line in moved_lines:
                        new_lines.append(moved_line)
                else:
                    new_lines.append(line)
            
            # Write back
            toml_path.write_text("\n".join(new_lines), encoding="utf-8")
            logger.info("Fixed pyproject.toml deprecated settings")
            return True
        
        return False
    except Exception as e:
        logger.error(f"Failed to fix pyproject.toml: {e}", exc_info=True)
        return False


def _validate_improvement_plan(plan: Plan, ctx: RunContext) -> Plan:
    """
    Validate improvement plan quality.
    
    - Removes invalid file references
    - Filters out duplicate steps
    - Validates file paths exist
    
    Args:
        plan: Generated plan
        ctx: Run context
        
    Returns:
        Validated plan
    """
    validated_files = []
    seen_files = set()
    
    # Protected files - require explicit approval
    PROTECTED_FILES = {
        "pyproject.toml",
        "requirements.txt",
        "setup.py",
        "setup.cfg",
        ".gitignore",
        ".env",
        "docker-compose.yml",
        "Dockerfile",
    }
    
    # Invalid file patterns
    INVALID_PATTERNS = [
        "all", "of", "the", "existing", "code",
        "tests",  # Directory, not a file
        "*.rst",  # Glob pattern
        "pytest.ini",  # Config file
    ]
    
    # Validate file paths
    for file_path in plan.files:
        # Skip invalid references
        if file_path in INVALID_PATTERNS or file_path.endswith("*"):
            logger.warning(f"Skipping invalid file reference: {file_path}")
            continue
        
        # Check if it's a protected file
        file_name = Path(file_path).name
        if file_name in PROTECTED_FILES:
            logger.warning(f"Protected file in plan: {file_path}. Skipping for safety.")
            continue
        
        # Fix typos (double underscores)
        if file_path.endswith("__"):
            file_path = file_path[:-1]
        
        # Try multiple path resolutions
        possible_paths = [
            file_path,  # As-is
            f"src/ybis/{file_path}",  # Relative to src/ybis
            file_path.replace("\\", "/"),  # Normalize Windows paths
        ]
        
        # Also try without leading slash
        if file_path.startswith("/"):
            possible_paths.append(file_path[1:])
        
        found_path = None
        for path_attempt in possible_paths:
            full_path = PROJECT_ROOT / path_attempt
            if full_path.exists() and full_path.is_file():
                found_path = path_attempt
                break
        
        if not found_path:
            logger.warning(f"File not found after trying multiple paths: {file_path}")
            continue
        
        # Avoid duplicates
        if found_path not in seen_files:
            validated_files.append(found_path)
            seen_files.add(found_path)
    
    # Validate steps
    validated_steps = []
    seen_step_descriptions = set()
    
    for step in plan.steps:
        step_desc = step.get("description", "")
        
        # Skip duplicates
        if step_desc in seen_step_descriptions:
            logger.warning(f"Skipping duplicate step: {step_desc}")
            continue
        
        # Validate step files
        step_files = step.get("files", [])
        validated_step_files = []
        for f in step_files:
            # Check if already validated
            if f in validated_files:
                validated_step_files.append(f)
                continue
            
            # Try to find file
            possible_paths = [
                f,
                f"src/ybis/{f}",
                f.replace("\\", "/"),
            ]
            if f.startswith("/"):
                possible_paths.append(f[1:])
            
            found = False
            for path_attempt in possible_paths:
                if (PROJECT_ROOT / path_attempt).exists():
                    validated_step_files.append(path_attempt)
                    found = True
                    break
            
            if not found and f not in ["all", "of", "the", "existing", "code"]:
                # Keep file reference even if not found (might be created)
                validated_step_files.append(f)
        
        step["files"] = validated_step_files
        validated_steps.append(step)
        seen_step_descriptions.add(step_desc)
    
    # If validation removed all files, try to extract from RAG context
    if not validated_files and plan.referenced_context:
        logger.info("No valid files found, extracting from RAG context...")
        for ctx in plan.referenced_context:
            metadata = ctx.get("metadata", {})
            file_path = metadata.get("file") or metadata.get("file_path", "")
            if file_path and file_path.startswith("src/ybis"):
                full_path = PROJECT_ROOT / file_path
                if full_path.exists() and file_path not in validated_files:
                    validated_files.append(file_path)
                    logger.info(f"Added file from RAG context: {file_path}")
    
    # Create validated plan
    validated_plan = Plan(
        objective=plan.objective,
        files=validated_files,
        instructions=plan.instructions or "Implement improvements based on reflection analysis",
        steps=validated_steps,
        referenced_context=plan.referenced_context,
    )
    
    if len(validated_files) < len(plan.files):
        logger.info(f"Plan validation: {len(plan.files)} → {len(validated_files)} valid files")
    elif len(validated_files) > 0:
        logger.info(f"Plan validation: {len(validated_files)} valid files")
    if len(validated_steps) < len(plan.steps):
        logger.info(f"Plan validation: {len(plan.steps)} → {len(validated_steps)} valid steps")
    
    return validated_plan


def self_improve_reflect_node(state: WorkflowState) -> WorkflowState:
    """
    Reflect on system state and identify improvements.
    
    YBIS-native implementation - uses ReflectionEngine.
    
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
    
    # Journal: Self-improve reflect start
    append_event(
        ctx.run_path,
        "SELF_IMPROVE_REFLECT_START",
        {
            "task_id": ctx.task_id,
        },
        trace_id=ctx.trace_id,
    )
    
    try:
        start_time = time.time()
        # Use reflection engine with journal logging
        reflection_engine = ReflectionEngine(run_path=ctx.run_path, trace_id=ctx.trace_id)
        reflection = reflection_engine.reflect()
        elapsed_ms = (time.time() - start_time) * 1000
        
        # Save reflection report
        reflection_path = ctx.artifacts_dir / "reflection_report.json"
        write_file(reflection_path, json.dumps(reflection, indent=2), ctx)
        
        issues_count = len(reflection.get('issues_identified', []))
        opportunities_count = len(reflection.get('opportunities_identified', []))
        
        # Journal: Self-improve reflect complete
        append_event(
            ctx.run_path,
            "SELF_IMPROVE_REFLECT_COMPLETE",
            {
                "issues_count": issues_count,
                "opportunities_count": opportunities_count,
                "duration_ms": round(elapsed_ms, 2),
            },
            trace_id=ctx.trace_id,
        )
        
        logger.info(f"Reflection completed: {issues_count} issues, {opportunities_count} opportunities")
        state["status"] = "running"
    except (FileNotFoundError, PermissionError) as e:
        logger.error(f"Self-improve reflection failed (file error): {e}", exc_info=True)
        # Create minimal reflection
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "issues_identified": [],
            "opportunities_identified": [{
                "area": "system_reliability",
                "priority": "medium",
                "description": "Improve system reliability",
            }],
        }
        reflection_path = ctx.artifacts_dir / "reflection_report.json"
        write_file(reflection_path, json.dumps(reflection, indent=2), ctx)
        state["status"] = "running"
    except Exception as e:
        logger.error(f"Self-improve reflection failed (unexpected error): {e}", exc_info=True)
        # Create minimal reflection
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "issues_identified": [],
            "opportunities_identified": [{
                "area": "system_reliability",
                "priority": "medium",
                "description": "Improve system reliability",
            }],
        }
        reflection_path = ctx.artifacts_dir / "reflection_report.json"
        write_file(reflection_path, json.dumps(reflection, indent=2), ctx)
        state["status"] = "running"
    
    return state


def self_improve_plan_node(state: WorkflowState) -> WorkflowState:
    """
    Plan improvements based on reflection.
    
    Uses LLMPlanner with reflection context and RAG.
    
    Args:
        state: Workflow state
        
    Returns:
        Updated state with improvement_plan.json
    """
    ctx = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    )
    
    # Journal: Self-improve plan start
    append_event(
        ctx.run_path,
        "SELF_IMPROVE_PLAN_START",
        {
            "task_id": ctx.task_id,
        },
        trace_id=ctx.trace_id,
    )
    
    try:
        # Load reflection
        reflection_path = ctx.artifacts_dir / "reflection_report.json"
        if not reflection_path.exists():
            state["status"] = "running"
            return state
        
        reflection = json.loads(reflection_path.read_text())
        
        # Build improvement objective from reflection
        issues = reflection.get("issues_identified", [])
        opportunities = reflection.get("opportunities_identified", [])
        error_patterns = reflection.get("error_patterns", {})
        
        # Build enriched objective with context
        objective_parts = []
        
        # Add high-priority issues
        high_priority_issues = [i for i in issues if i.get("severity") == "high"]
        if high_priority_issues:
            issue_descs = [i.get('description', '') for i in high_priority_issues[:3]]
            objective_parts.append(f"Fix high-priority issues: {', '.join(issue_descs)}")
        
        # Add top opportunity
        if opportunities:
            top_opp = opportunities[0]
            objective_parts.append(f"Improve {top_opp.get('area', 'system')}: {top_opp.get('description', '')}")
        
        # Add error pattern context
        if error_patterns.get("top_patterns"):
            top_pattern = error_patterns["top_patterns"][0]
            objective_parts.append(
                f"Address recurring {top_pattern.get('error_type', 'error')} "
                f"(occurs {top_pattern.get('occurrences', 0)} times)"
            )
        
        # Fallback if no specific issues
        if not objective_parts:
            objective_parts.append("Improve system reliability and performance")
        
        objective = " | ".join(objective_parts)
        
        # Create task for planning with reflection context
        task = Task(
            task_id=ctx.task_id,
            title="Self-Improvement: Plan Improvements",
            objective=objective,
            status="pending",
            priority="MEDIUM",
        )
        
        # Use planner to generate improvement plan
        # Planner will use RAG to get codebase context
        start_time = time.time()
        planner = LLMPlanner()
        plan = planner.plan(task, ctx)
        elapsed_ms = (time.time() - start_time) * 1000
        
        # Journal: Self-improve plan complete
        append_event(
            ctx.run_path,
            "SELF_IMPROVE_PLAN_COMPLETE",
            {
                "files_count": len(plan.files),
                "steps_count": len(plan.steps) if hasattr(plan, "steps") else 0,
                "duration_ms": round(elapsed_ms, 2),
            },
            trace_id=ctx.trace_id,
        )
        
        # Validate plan quality
        plan = _validate_improvement_plan(plan, ctx)
        
        # Save improvement plan
        plan_path = ctx.artifacts_dir / "improvement_plan.json"
        # Plan is a dataclass, convert to dict for JSON
        plan_dict = {
            "objective": plan.objective,
            "files": plan.files,
            "instructions": plan.instructions,
            "steps": plan.steps if hasattr(plan, 'steps') else [],
        }
        write_file(plan_path, json.dumps(plan_dict, indent=2), ctx)
        
        # Also save as plan.json for executor compatibility
        executor_plan_path = ctx.plan_path
        write_file(executor_plan_path, json.dumps(plan_dict, indent=2), ctx)
        
        logger.info(f"Improvement plan generated: {len(plan_dict.get('steps', []))} steps, "
                   f"{len(plan_dict.get('files', []))} files")
        state["status"] = "running"
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        logger.error(f"Self-improve planning failed (data error): {e}", exc_info=True)
        # Create minimal plan
        plan = {
            "objective": "Improve system reliability",
            "files": [],
            "instructions": "Review and improve error handling",
            "steps": [],
        }
        plan_path = ctx.artifacts_dir / "improvement_plan.json"
        write_file(plan_path, json.dumps(plan, indent=2), ctx)
        state["status"] = "running"
    except Exception as e:
        logger.error(f"Self-improve planning failed (unexpected error): {e}", exc_info=True)
        # Create minimal plan
        plan = {
            "objective": "Improve system reliability",
            "files": [],
            "instructions": "Review and improve error handling",
            "steps": [],
        }
        plan_path = ctx.artifacts_dir / "improvement_plan.json"
        write_file(plan_path, json.dumps(plan, indent=2), ctx)
        state["status"] = "running"
    
    return state


def self_improve_implement_node(state: WorkflowState) -> WorkflowState:
    """
    Implement improvement plan.
    
    Uses existing executor to make changes.
    
    Args:
        state: Workflow state
        
    Returns:
        Updated state with implementation_report.json
    """
    ctx = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    )
    
    # NOTE: repair_retries is initialized in repair_node, not here
    # This ensures consistent state management
    
    try:
        # Load plan
        plan_path = ctx.plan_path
        if not plan_path.exists():
            state["status"] = "running"
            return state
        
        plan_data = json.loads(plan_path.read_text())
        plan = Plan(**plan_data)
        
        # If plan has no files, try to extract from reflection
        if not plan.files:
            logger.warning("Plan has no files, attempting to extract from reflection...")
            reflection_path = ctx.artifacts_dir / "reflection_report.json"
            if reflection_path.exists():
                try:
                    reflection = json.loads(reflection_path.read_text())
                    # Extract file suggestions from error patterns
                    error_patterns = reflection.get("error_patterns", {})
                    top_patterns = error_patterns.get("top_patterns", [])
                    
                    # Common file mappings based on error types
                    file_suggestions = []
                    for pattern in top_patterns[:3]:
                        error_type = pattern.get("error_type", "")
                        if "verifier" in error_type.lower():
                            file_suggestions.append("src/ybis/orchestrator/verifier.py")
                        elif "gate" in error_type.lower():
                            file_suggestions.append("src/ybis/orchestrator/gates.py")
                        elif "policy" in error_type.lower():
                            file_suggestions.append("src/ybis/services/policy.py")
                    
                    # Also check RAG context from plan
                    if hasattr(plan, 'referenced_context') and plan.referenced_context:
                        for ctx_item in plan.referenced_context[:3]:
                            metadata = ctx_item.get("metadata", {})
                            file_path = metadata.get("file") or metadata.get("file_path", "")
                            if file_path and file_path.startswith("src/ybis") and file_path not in file_suggestions:
                                file_suggestions.append(file_path)
                    
                    if file_suggestions:
                        # Update plan with suggested files
                        plan.files = list(set(file_suggestions))[:5]  # Max 5 files
                        logger.info(f"Added {len(plan.files)} files from reflection/RAG context")
                except Exception as e:
                    logger.warning(f"Failed to extract files from reflection: {e}")
        
        # Use executor to implement (same pattern as execute_node)
        from ..executors.registry import get_executor_registry
        
        executor_registry = get_executor_registry()
        executor = executor_registry.get_executor(None)  # Use policy default
        
        if executor is None:
            raise RuntimeError(
                "No executor available. Check policy: adapters.local_coder.enabled"
            )
        
        # Executor uses generate_code method
        executor_report = executor.generate_code(ctx, plan)
        
        # Save implementation report
        impl_path = ctx.artifacts_dir / "implementation_report.json"
        write_file(impl_path, executor_report.model_dump_json(indent=2), ctx)
        
        # Also save as executor_report.json for verifier compatibility
        executor_report_path = ctx.executor_report_path
        write_file(executor_report_path, executor_report.model_dump_json(indent=2), ctx)
        
        files_changed_count = len(executor_report.files_changed)
        logger.info(f"Implementation completed: {files_changed_count} files changed")
        
        # Journal: Self-improve implement complete
        append_event(
            ctx.run_path,
            "SELF_IMPROVE_IMPLEMENT_COMPLETE",
            {
                "files_changed": files_changed_count,
            },
            trace_id=ctx.trace_id,
        )
        
        # Preserve all state keys (especially repair_retries for repair loop)
        # LangGraph merges state, but we explicitly preserve to be safe
        state["status"] = "running"
        logger.debug(f"State after implement: repair_retries={state.get('repair_retries')}, max={state.get('max_repair_retries')}")
        # Note: repair_retries, max_repair_retries, and other keys are preserved by LangGraph state merge
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Self-improve implementation failed (data error): {e}", exc_info=True)
        # Create minimal implementation report
        impl_report = {
            "timestamp": datetime.now().isoformat(),
            "status": "failed",
            "error": str(e),
            "files_modified": [],
        }
        impl_path = ctx.artifacts_dir / "implementation_report.json"
        write_file(impl_path, json.dumps(impl_report, indent=2), ctx)
        state["status"] = "running"
    except RuntimeError as e:
        logger.error(f"Self-improve implementation failed (executor error): {e}", exc_info=True)
        # Create minimal implementation report
        impl_report = {
            "timestamp": datetime.now().isoformat(),
            "status": "failed",
            "error": str(e),
            "files_modified": [],
        }
        impl_path = ctx.artifacts_dir / "implementation_report.json"
        write_file(impl_path, json.dumps(impl_report, indent=2), ctx)
        state["status"] = "running"
    except Exception as e:
        logger.error(f"Self-improve implementation failed (unexpected error): {e}", exc_info=True)
        # Create minimal implementation report
        impl_report = {
            "timestamp": datetime.now().isoformat(),
            "status": "failed",
            "error": str(e),
            "files_modified": [],
        }
        impl_path = ctx.artifacts_dir / "implementation_report.json"
        write_file(impl_path, json.dumps(impl_report, indent=2), ctx)
        state["status"] = "running"
    
    return state


def self_improve_test_node(state: WorkflowState) -> WorkflowState:
    """
    Test implementation.
    
    Uses existing verifier to test changes.
    
    Args:
        state: Workflow state
        
    Returns:
        Updated state with test_report.json and test_passed flag
    """
    ctx = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    )
    
    try:
        # Use verifier to test
        verifier_report = run_verifier(ctx)
        
        # Save test report
        test_path = ctx.artifacts_dir / "test_report.json"
        write_file(test_path, verifier_report.model_dump_json(indent=2), ctx)
        
        # Also save as verifier_report.json for gate compatibility
        verifier_report_path = ctx.verifier_report_path
        write_file(verifier_report_path, verifier_report.model_dump_json(indent=2), ctx)
        
        # Set test flags for conditional routing
        test_passed = verifier_report.lint_passed and verifier_report.tests_passed
        state["test_passed"] = test_passed
        state["lint_passed"] = verifier_report.lint_passed
        state["tests_passed"] = verifier_report.tests_passed
        state["test_errors"] = verifier_report.errors or []
        state["test_warnings"] = verifier_report.warnings or []
        
        logger.info(f"Testing completed: lint={verifier_report.lint_passed}, "
                   f"tests={verifier_report.tests_passed}, passed={test_passed}")
        state["status"] = "running"
    except (FileNotFoundError, AttributeError) as e:
        logger.error(f"Self-improve testing failed (data error): {e}", exc_info=True)
        # Create minimal test report
        test_report = {
            "timestamp": datetime.now().isoformat(),
            "lint_passed": False,
            "tests_passed": False,
            "error": str(e),
        }
        test_path = ctx.artifacts_dir / "test_report.json"
        write_file(test_path, json.dumps(test_report, indent=2), ctx)
        state["test_passed"] = False
        state["lint_passed"] = False
        state["tests_passed"] = False
        state["test_errors"] = [str(e)]
        state["status"] = "running"
    except Exception as e:
        logger.error(f"Self-improve testing failed (unexpected error): {e}", exc_info=True)
        # Create minimal test report
        test_report = {
            "timestamp": datetime.now().isoformat(),
            "lint_passed": False,
            "tests_passed": False,
            "error": str(e),
        }
        test_path = ctx.artifacts_dir / "test_report.json"
        write_file(test_path, json.dumps(test_report, indent=2), ctx)
        state["test_passed"] = False
        state["lint_passed"] = False
        state["tests_passed"] = False
        state["test_errors"] = [str(e)]
        state["status"] = "running"
    
    return state


def self_improve_repair_node(state: WorkflowState) -> WorkflowState:
    """
    Repair lint/test failures automatically.
    
    - Auto-fixes lint errors using ruff
    - Analyzes test failures and creates fix plan
    - Limits retries to prevent infinite loops
    
    Args:
        state: Workflow state
        
    Returns:
        Updated state with repair_report.json
    """
    ctx = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    )
    
    # Initialize repair retry counters if not set
    if "repair_retries" not in state:
        state["repair_retries"] = 0
    if "max_repair_retries" not in state:
        state["max_repair_retries"] = 3
    
    # Check retry limits BEFORE incrementing
    retries = state.get("repair_retries", 0)  # Use .get() to handle missing key
    max_repair_retries = state.get("max_repair_retries", 3)
    
    logger.debug(f"Repair node called: retries={retries}, max={max_repair_retries}")
    
    if retries >= max_repair_retries:
        logger.warning(f"Max repair retries ({max_repair_retries}) reached. Stopping repair loop and proceeding to integrate.")
        state["repair_failed"] = True
        state["repair_max_retries_reached"] = True
        # Force test_passed to True so routing goes to integrate
        state["test_passed"] = True
        state["status"] = "running"
        return state
    
    # Increment retry counter BEFORE using it
    new_retries = retries + 1
    state["repair_retries"] = new_retries
    logger.info(f"Repair attempt {new_retries}/{max_repair_retries} (previous retries: {retries})")
    
    # Journal: Self-improve repair start
    append_event(
        ctx.run_path,
        "SELF_IMPROVE_REPAIR_START",
        {
            "attempt": new_retries,
            "max_retries": max_repair_retries,
        },
        trace_id=ctx.trace_id,
    )
    
    repair_actions = []
    
    try:
        # Load test report
        test_path = ctx.artifacts_dir / "test_report.json"
        if not test_path.exists():
            state["status"] = "running"
            return state
        
        test_data = json.loads(test_path.read_text())
        lint_passed = test_data.get("lint_passed", False)
        tests_passed = test_data.get("tests_passed", False)
        errors = test_data.get("errors", [])
        warnings = test_data.get("warnings", [])
        
        # Auto-fix lint errors
        lint_fixed = False
        if not lint_passed:
            logger.info("Attempting to auto-fix lint errors...")
            
            # Check if it's a pyproject.toml deprecated settings issue
            is_deprecated_settings_error = False
            if errors:
                error_text = str(errors[0]).lower()
                if "deprecated" in error_text and ("pyproject.toml" in error_text or "lint" in error_text):
                    is_deprecated_settings_error = True
            
            # Try ruff auto-fix first (in worktree if available)
            try:
                worktree_path = Path(ctx.run_path) if ctx.run_path else PROJECT_ROOT
                src_path = worktree_path / "src" if (worktree_path / "src").exists() else PROJECT_ROOT / "src"
                
                result = subprocess.run(
                    ["ruff", "check", "--fix", str(src_path)],
                    cwd=worktree_path,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=60,
                )
                if result.returncode == 0:
                    repair_actions.append("Auto-fixed lint errors with ruff --fix")
                    logger.info("Lint errors auto-fixed")
                    lint_fixed = True
                else:
                    # If ruff failed and it's a deprecated settings issue, fix directly
                    if is_deprecated_settings_error:
                        # Fix in worktree if available, otherwise in project root
                        worktree_path = Path(ctx.run_path) if ctx.run_path else None
                        lint_fixed = _fix_pyproject_toml_deprecated_settings(PROJECT_ROOT, worktree_path)
                        if lint_fixed:
                            repair_actions.append("Fixed pyproject.toml deprecated settings directly")
                            logger.info("Fixed pyproject.toml deprecated settings")
                        else:
                            repair_actions.append(f"Failed to fix deprecated settings: {result.stderr[:200]}")
                    else:
                        repair_actions.append(f"Ruff auto-fix attempted but had issues: {result.stderr[:200]}")
            except FileNotFoundError:
                repair_actions.append("Ruff not found, cannot auto-fix lint errors")
            except Exception as e:
                repair_actions.append(f"Lint auto-fix failed: {str(e)[:200]}")
        
        # Only create test repair plan if tests actually failed (not just lint)
        # If only lint failed and tests passed, skip test plan creation
        # Also skip if lint was just fixed (give it a chance to pass on next test)
        should_create_test_plan = (
            not tests_passed  # Tests actually failed
            and errors  # There are errors
            and not lint_fixed  # Lint wasn't just fixed
            and not (not lint_passed and tests_passed)  # Not just lint error
        )
        
        if should_create_test_plan:
            logger.info(f"Analyzing {len(errors)} test errors...")
            
            # Extract error patterns with full context
            error_summary = "\n".join([str(e)[:200] for e in errors[:5]])
            warning_summary = "\n".join([str(w)[:200] for w in warnings[:3]]) if warnings else ""
            
            # Get current plan files for context
            main_plan_path = ctx.plan_path
            current_files = []
            if main_plan_path.exists():
                try:
                    main_plan_data = json.loads(main_plan_path.read_text())
                    current_files = main_plan_data.get("files", [])
                except Exception:
                    pass
            
            # Build enriched repair objective with full context
            repair_objective_parts = [
                "Fix test failures in the following files:",
                f"Files being modified: {', '.join(current_files) if current_files else 'See errors below'}",
                "",
                "ERRORS:",
                error_summary,
            ]
            if warning_summary:
                repair_objective_parts.extend([
                    "",
                    "WARNINGS:",
                    warning_summary,
                ])
            repair_objective_parts.extend([
                "",
                "INSTRUCTIONS:",
                "1. Review the errors above",
                "2. Identify which files need to be fixed",
                "3. Make minimal changes to fix the errors",
                "4. Ensure fixes don't break existing functionality",
                "",
                "IMPORTANT: Only modify files that are causing the errors. Do not modify unrelated files.",
            ])
            
            repair_objective = "\n".join(repair_objective_parts)
            repair_task = Task(
                task_id=f"{ctx.task_id}-repair-{retries}",
                title="Repair Test Failures",
                objective=repair_objective,
                status="pending",
                priority="HIGH",
            )
            
            planner = LLMPlanner()
            repair_plan = planner.plan(repair_task)
            
            # Validate repair plan files exist
            # NOTE: For repair, we allow protected files (like pyproject.toml) since repair needs to fix config issues
            validated_repair_files = []
            for file_path in repair_plan.files:
                # Skip invalid patterns
                if not file_path or file_path in ["all", "of", "the", "existing", "code"]:
                    continue
                
                # Try multiple path resolutions
                possible_paths = [
                    file_path,
                    f"src/ybis/{file_path}",
                    file_path.replace("\\", "/"),
                ]
                if file_path.startswith("/"):
                    possible_paths.append(file_path[1:])
                
                found = False
                for path_attempt in possible_paths:
                    full_path = PROJECT_ROOT / path_attempt
                    # For repair, allow protected files (they need to be fixed)
                    if full_path.exists():
                        validated_repair_files.append(path_attempt)
                        found = True
                        break
                
                if not found:
                    logger.warning(f"Repair plan file not found, skipping: {file_path}")
            
            # Only proceed if we have valid files
            if validated_repair_files:
                # Save repair plan with validated files
                repair_plan_path = ctx.artifacts_dir / f"repair_plan_{retries}.json"
                plan_dict = {
                    "objective": repair_plan.objective,
                    "files": validated_repair_files,  # Use validated files
                    "instructions": repair_plan.instructions,
                    "steps": repair_plan.steps if hasattr(repair_plan, 'steps') else [],
                }
                write_file(repair_plan_path, json.dumps(plan_dict, indent=2), ctx)
                repair_actions.append(f"Created repair plan with {len(validated_repair_files)} valid files")
                
                # Update main plan with repair plan
                # IMPORTANT: Replace plan with repair plan (don't merge old steps)
                # This ensures implement node uses only the repair plan
                main_plan_path = ctx.plan_path
                if main_plan_path.exists():
                    # Create new plan with repair plan data
                    repair_plan_data = {
                        "objective": plan_dict["objective"],
                        "files": validated_repair_files,  # Only repair files
                        "instructions": plan_dict["instructions"],
                        "steps": plan_dict["steps"],  # Only repair steps (don't merge old steps)
                    }
                    write_file(main_plan_path, json.dumps(repair_plan_data, indent=2), ctx)
                    repair_actions.append("Updated main plan with repair steps (replaced, not merged)")
                else:
                    # If plan doesn't exist, create it
                    repair_plan_data = {
                        "objective": plan_dict["objective"],
                        "files": validated_repair_files,
                        "instructions": plan_dict["instructions"],
                        "steps": plan_dict["steps"],
                    }
                    write_file(main_plan_path, json.dumps(repair_plan_data, indent=2), ctx)
                    repair_actions.append("Created main plan with repair steps")
            else:
                logger.warning("Repair plan has no valid files, skipping plan update")
                repair_actions.append("Repair plan validation failed - no valid files found")
        
        # Save repair report
        repair_report = {
            "timestamp": datetime.now().isoformat(),
            "repair_attempt": state["repair_retries"],  # Use state value, not local variable
            "max_retries": max_repair_retries,
            "lint_passed_before": lint_passed,
            "tests_passed_before": tests_passed,
            "actions_taken": repair_actions,
            "errors_analyzed": len(errors),
        }
        repair_report_path = ctx.artifacts_dir / f"repair_report_{state['repair_retries'] - 1}.json"  # Use 0-indexed for filename
        write_file(repair_report_path, json.dumps(repair_report, indent=2), ctx)
        
        actions_count = len(repair_actions)
        logger.info(f"Repair completed: {actions_count} actions taken")
        
        # Journal: Self-improve repair complete
        append_event(
            ctx.run_path,
            "SELF_IMPROVE_REPAIR_COMPLETE",
            {
                "actions_taken": actions_count,
                "attempt": state["repair_retries"],
            },
            trace_id=ctx.trace_id,
        )
        
        state["status"] = "running"
        
    except Exception as e:
        logger.error(f"Self-improve repair failed: {e}", exc_info=True)
        repair_report = {
            "timestamp": datetime.now().isoformat(),
            "repair_attempt": state.get("repair_retries", retries + 1),  # Use state value if available
            "error": str(e),
            "actions_taken": repair_actions,
        }
        repair_report_path = ctx.artifacts_dir / f"repair_report_{state.get('repair_retries', retries) - 1}.json"  # Use 0-indexed for filename
        write_file(repair_report_path, json.dumps(repair_report, indent=2), ctx)
        state["status"] = "running"
    
    return state


def self_improve_integrate_node(state: WorkflowState) -> WorkflowState:
    """
    Integrate tested implementation.
    
    For self-improve workflow, integration happens BEFORE gate (unlike regular workflow).
    This node creates an integration report based on test results, without waiting for gate.
    
    Args:
        state: Workflow state
        
    Returns:
        Updated state with integration_report.json
    """
    ctx = RunContext(
        task_id=state["task_id"],
        run_id=state["run_id"],
        run_path=state["run_path"],
        trace_id=state.get("trace_id", f"{state['task_id']}-{state['run_id']}"),
    )
    
    try:
        # Load test report to check if tests passed
        test_path = ctx.artifacts_dir / "test_report.json"
        test_passed = False
        test_data = {}
        
        if test_path.exists():
            test_data = json.loads(test_path.read_text())
            test_passed = test_data.get("lint_passed", False) and test_data.get("tests_passed", False)
        
        # Load implementation report
        impl_path = ctx.artifacts_dir / "implementation_report.json"
        impl_data = {}
        if impl_path.exists():
            impl_data = json.loads(impl_path.read_text())
        
        # Create integration report
        integration = {
            "timestamp": datetime.now().isoformat(),
            "task_id": ctx.task_id,
            "run_id": ctx.run_id,
            "status": "integrated" if test_passed else "integrated_with_warnings",
            "test_passed": test_passed,
            "files_changed": impl_data.get("files_changed", []),
            "test_summary": {
                "lint_passed": test_data.get("lint_passed", False),
                "tests_passed": test_data.get("tests_passed", False),
                "errors": test_data.get("errors", []),
                "warnings": test_data.get("warnings", []),
            },
        }
        
        integration_path = ctx.artifacts_dir / "integration_report.json"
        write_file(integration_path, json.dumps(integration, indent=2), ctx)
        
        logger.info(f"Integration completed: status={integration['status']}, test_passed={test_passed}")
        state["status"] = "running"
    except Exception as e:
        logger.error(f"Self-improve integration failed: {e}", exc_info=True)
        # Create minimal integration report even on error
        integration = {
            "timestamp": datetime.now().isoformat(),
            "task_id": ctx.task_id,
            "run_id": ctx.run_id,
            "status": "failed",
            "error": str(e),
        }
        integration_path = ctx.artifacts_dir / "integration_report.json"
        write_file(integration_path, json.dumps(integration, indent=2), ctx)
        state["status"] = "running"
    
    return state
