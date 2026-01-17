"""
Spec Node - Generates SPEC.md using Chief Architect persona.

Includes helper functions for spec validation and generation.
"""

import json
import logging
import re

from ...constants import PROJECT_ROOT
from ...contracts import RunContext, VerifierReport
from ...syscalls.journal import append_event
from ..graph import WorkflowState
from ..logging import llm_call_with_logging, log_node_execution

logger = logging.getLogger(__name__)


@log_node_execution("spec")
def spec_node(state: WorkflowState) -> WorkflowState:
    """
    Spec node - generates SPEC.md using Chief Architect persona.

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

    logger.info(f"Spec node: task_id={ctx.task_id}, run_id={ctx.run_id}")

    # Check if spec already exists
    spec_path = PROJECT_ROOT / "docs" / "specs" / f"{state['task_id']}_SPEC.md"
    spec_path.parent.mkdir(parents=True, exist_ok=True)

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
                    feedback_parts.extend(verifier_report.errors[:10])  # Limit to 10 errors
                if verifier_report.warnings:
                    feedback_parts.append("\nVERIFIER WARNINGS:")
                    feedback_parts.extend(verifier_report.warnings[:10])  # Limit to 10 warnings
                if feedback_parts:
                    verifier_feedback = "\n".join(feedback_parts)
        except Exception:
            pass  # Ignore if verifier report can't be read

    # Also check error_context from repair node
    error_context = state.get("error_context")
    if error_context and not verifier_feedback:
        verifier_feedback = error_context

    # If spec exists and we have feedback, regenerate with feedback
    if spec_path.exists() and not verifier_feedback:
        # Spec already exists, no feedback - skip generation
        state["status"] = "running"
        return state

    # Load task objective from state
    task_objective = state.get("task_objective", "Execute task")

    # Get error insights from Error Knowledge Base
    error_insights = None
    try:
        from ...services.error_knowledge_base import ErrorKnowledgeBase

        error_kb = ErrorKnowledgeBase()
        insights = error_kb.get_insights_for_task(state["task_id"])

        if insights.get("error_count", 0) > 0:
            # Build insights message
            insights_parts = []
            insights_parts.append("📚 ERROR KNOWLEDGE BASE INSIGHTS:")
            insights_parts.append(f"This task has {insights['error_count']} recorded errors.")

            if insights.get("patterns"):
                insights_parts.append("\nRecurring error patterns:")
                for pattern in insights["patterns"][:3]:  # Limit to 3 patterns
                    insights_parts.append(f"  - {pattern.get('error_type', 'unknown')}: {pattern.get('occurrence_count', 0)} occurrences")

            if insights.get("suggestions"):
                insights_parts.append("\nSuggested fixes:")
                for suggestion in insights["suggestions"][:3]:  # Limit to 3 suggestions
                    insights_parts.append(f"  - {suggestion.get('suggestion', 'N/A')}")

            error_insights = "\n".join(insights_parts)
    except Exception:
        # Error KB not critical, continue if it fails
        pass

    # Generate spec using Chief Architect persona
    try:
        from ...contracts.personas import COUNCIL_MEMBERS
        from ...services.policy import get_policy_provider
        from ...services.resilience import ollama_retry

        policy_provider = get_policy_provider()
        if policy_provider._policy is None:
            policy_provider.load_profile()
        llm_config = policy_provider.get_llm_config()

        # Find Architect persona
        architect = next((p for p in COUNCIL_MEMBERS if p.name == "Architect"), None)
        if not architect:
            # Fallback: use first persona
            architect = COUNCIL_MEMBERS[0]

        model = llm_config.get("planner_model", "ollama/llama3.2:3b")
        api_base = llm_config.get("api_base", "http://localhost:11434")

        codebase_context = _get_codebase_context_for_spec()
        spec_template = _load_spec_template()

        @ollama_retry
        def _call_llm():
            # Build user message with feedback if available
            user_content = f"Task Objective: {task_objective}\n\n"

            # Add error insights from Error Knowledge Base
            if error_insights:
                user_content += f"{error_insights}\n\n"
                user_content += "IMPORTANT: Learn from these past errors and ensure the spec prevents them.\n\n"

            if verifier_feedback:
                user_content += f"⚠️ FEEDBACK FROM VERIFIER (Previous Run Failed):\n{verifier_feedback}\n\n"
                user_content += "IMPORTANT: The previous spec/implementation had these issues. Please:\n"
                user_content += "1. Address these errors in the new spec\n"
                user_content += "2. Ensure the spec prevents these issues\n"
                user_content += "3. Add requirements/acceptance criteria that would catch these errors\n\n"
            user_content += "Create a detailed technical specification (SPEC.md) for this task."

            messages = [
                {
                    "role": "system",
                    "content": architect.system_prompt
                    + "\n\nYou are acting as the Chief Architect. Create a technical specification (SPEC.md) for the given task objective.\n"
                    + "Follow the template exactly, fill in every section, and include concrete file paths.\n"
                    + "Do not use placeholders like TBD/TODO/path/to.\n\n"
                    + "IMPORTANT SPEC-KIT REQUIREMENTS:\n"
                    + "- User stories MUST be prioritized (P1, P2, P3, etc.) where P1 is most critical\n"
                    + "- Each user story must be INDEPENDENTLY TESTABLE (can be implemented and tested alone)\n"
                    + "- Acceptance scenarios MUST use Given/When/Then format\n"
                    + "- Success criteria MUST be measurable and technology-agnostic\n"
                    + "- Include edge cases section with boundary conditions and error scenarios\n"
                    + "- Mark unclear requirements with [NEEDS CLARIFICATION] if needed\n\n"
                    + f"Template:\n{spec_template}\n\n"
                    + (f"Codebase context:\n{codebase_context}\n" if codebase_context else ""),
                },
                {
                    "role": "user",
                    "content": user_content,
                },
            ]

            return llm_call_with_logging(
                model=model,
                messages=messages,
                run_path=ctx.run_path,
                trace_id=ctx.trace_id,
                api_base=api_base,
                timeout=30,
            )

        response = _call_llm()
        spec_content = response.choices[0].message.content

        if not _is_structured_spec(spec_content) or _contains_placeholders(spec_content):
            spec_content = _build_spec_from_objective(state["task_id"], task_objective)

        # Write spec to file
        spec_path.write_text(spec_content, encoding="utf-8")

        # Journal event
        append_event(
            ctx.run_path,
            "SPEC_GENERATED",
            {
                "spec_path": str(spec_path),
                "task_id": state["task_id"],
            },
            trace_id=ctx.trace_id,
        )

    except Exception as e:
        # If spec generation fails, create a minimal spec
        spec_content = _build_spec_from_objective(state["task_id"], task_objective)
        spec_content += (
            "\n\n## Status\n"
            f"Spec generation failed: {e!s}\n"
            "## Note\n"
            "This is a fallback spec. Full spec generation requires LLM access."
        )
        spec_path.write_text(spec_content, encoding="utf-8")

    state["status"] = "running"
    return state


def _is_structured_spec(spec_content: str) -> bool:
    """Check if spec content contains required sections for parsing."""
    required_sections = [
        "## Objective",
        "## Requirements",
        "## Acceptance Criteria",
    ]
    return all(section in spec_content for section in required_sections)


def _contains_placeholders(content: str) -> bool:
    """Detect placeholder text that should not ship in specs."""
    placeholder_patterns = [
        r"\bTBD\b",
        r"\bTODO\b",
        r"\bFIXME\b",
        r"path/to",
        r"placeholder",
    ]
    return any(re.search(pattern, content, flags=re.IGNORECASE) for pattern in placeholder_patterns)


def _extract_files_from_text(text: str) -> list[str]:
    """Extract file paths from text."""
    file_pattern = r"[\w./\\:-]+\.(?:py|md|yaml|yml|json|toml)"
    return sorted(set(re.findall(file_pattern, text)))


def _build_spec_from_objective(task_id: str, task_objective: str) -> str:
    """Build a minimal structured spec from the task objective."""
    files = _extract_files_from_text(task_objective)
    files_block = "\n".join(f"- `{path}`" for path in files) if files else "- `TBD`"
    return (
        f"# SPEC: {task_id}\n\n"
        "## Objective\n"
        f"{task_objective}\n\n"
        "## Requirements\n"
        "- Implement the objective exactly as stated.\n"
        "- Keep changes scoped to the identified files.\n\n"
        "## Acceptance Criteria\n"
        "- Required files are created or updated.\n"
        "- Verifier passes under the active profile.\n\n"
        "## Constraints\n"
        "- Respect policy gates and protected paths.\n\n"
        "## Files\n"
        f"{files_block}\n"
    )


def _load_spec_template() -> str:
    """Load spec template, preferring spec-kit template from vendors."""
    # Try spec-kit template first (from vendors, in case it gets updated)
    spec_kit_template = PROJECT_ROOT / "vendors" / "spec-kit" / "templates" / "spec-template.md"
    if spec_kit_template.exists():
        return spec_kit_template.read_text(encoding="utf-8")

    # Try YBIS template (copy of spec-kit template)
    template_path = PROJECT_ROOT / "templates" / "spec_template.md"
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")

    # Fallback to minimal template
    return (
        "# SPEC: <task_id>\n\n"
        "## Objective\n"
        "<clear objective>\n\n"
        "## Requirements\n"
        "- <requirement 1>\n\n"
        "## Acceptance Criteria\n"
        "- <criterion 1>\n\n"
        "## Constraints\n"
        "- <constraint 1>\n\n"
        "## Files\n"
        "- `<path/to/file>`\n"
    )


def _get_codebase_context_for_spec() -> str:
    """Get a lightweight codebase summary for spec creation."""
    try:
        from ...services.knowledge import scan_codebase

        ybis_root = PROJECT_ROOT / "src" / "ybis"
        if ybis_root.exists():
            return scan_codebase(ybis_root)
    except Exception:
        return ""
    return ""
