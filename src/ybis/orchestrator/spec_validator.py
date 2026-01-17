"""
Spec Validator - Full spec-first validation workflow.

Provides comprehensive spec validation:
- Spec parsing and structure validation
- Plan validation against spec requirements
- Implementation validation against spec
- LLM-assisted semantic validation
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

from ..constants import PROJECT_ROOT
from ..contracts import RunContext
from ..services.policy import get_policy_provider
from ..services.resilience import ollama_retry


class SpecParser:
    """Parse and extract requirements from SPEC.md."""

    @staticmethod
    def parse_spec(spec_path: Path) -> dict[str, Any]:
        """
        Parse SPEC.md and extract structured requirements.

        Args:
            spec_path: Path to SPEC.md

        Returns:
            Dictionary with parsed spec structure
        """
        if not spec_path.exists():
            return {}

        content = spec_path.read_text(encoding="utf-8")

        # Extract sections
        sections = {
            "title": "",
            "objective": "",
            "requirements": [],
            "acceptance_criteria": [],
            "constraints": [],
            "files": [],
            "dependencies": [],
        }

        # Extract title (first # heading)
        title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if title_match:
            sections["title"] = title_match.group(1).strip()

        # Extract objective (usually after title or in "## Objective" section)
        objective_match = re.search(
            r"##\s+Objective\s*\n+(.+?)(?=\n##|\Z)", content, re.DOTALL
        )
        if objective_match:
            sections["objective"] = objective_match.group(1).strip()
        else:
            # Fallback: first paragraph after title
            first_para = re.search(r"^#.+?\n+(.+?)(?=\n##|\Z)", content, re.DOTALL)
            if first_para:
                sections["objective"] = first_para.group(1).strip()

        # Extract requirements (## Requirements or - items)
        req_section = re.search(
            r"##\s+Requirements?\s*\n+(.+?)(?=\n##|\Z)", content, re.DOTALL
        )
        if req_section:
            req_text = req_section.group(1)
            # Extract bullet points
            req_items = re.findall(r"^[-*]\s+(.+)$", req_text, re.MULTILINE)
            sections["requirements"] = [item.strip() for item in req_items]

        # Extract acceptance criteria
        ac_section = re.search(
            r"##\s+Acceptance\s+Criteria\s*\n+(.+?)(?=\n##|\Z)", content, re.DOTALL
        )
        if ac_section:
            ac_text = ac_section.group(1)
            ac_items = re.findall(r"^[-*]\s+(.+)$", ac_text, re.MULTILINE)
            sections["acceptance_criteria"] = [item.strip() for item in ac_items]

        # Extract constraints
        constraints_section = re.search(
            r"##\s+Constraints?\s*\n+(.+?)(?=\n##|\Z)", content, re.DOTALL
        )
        if constraints_section:
            constraints_text = constraints_section.group(1)
            constraint_items = re.findall(r"^[-*]\s+(.+)$", constraints_text, re.MULTILINE)
            sections["constraints"] = [item.strip() for item in constraint_items]

        # Extract files (mentioned in spec)
        file_pattern = r"`([^`]+\.(py|md|yaml|yml|json|toml))`"
        files = re.findall(file_pattern, content)
        sections["files"] = [f[0] for f in files]

        return sections


class PlanValidator:
    """Validate plan against spec requirements."""

    @staticmethod
    def validate_plan_against_spec(
        plan_data: dict[str, Any], spec_data: dict[str, Any]
    ) -> tuple[float, list[str]]:
        """
        Validate plan against spec requirements.

        Args:
            plan_data: Plan dictionary from plan.json
            spec_data: Parsed spec data

        Returns:
            Tuple of (compliance_score, messages)
        """
        score = 1.0
        messages = []

        # Check if plan addresses spec objective
        plan_objective = plan_data.get("objective", "").lower()
        spec_objective = spec_data.get("objective", "").lower()

        if spec_objective and not any(
            word in plan_objective for word in spec_objective.split()[:5]
        ):
            score -= 0.2
            messages.append("Plan objective doesn't align with spec objective")

        # Check if plan addresses requirements
        spec_requirements = spec_data.get("requirements", [])
        plan_files = plan_data.get("files", [])
        plan_instructions_raw = plan_data.get("instructions", "")
        # Handle both string and dict/list formats
        if isinstance(plan_instructions_raw, str):
            plan_instructions = plan_instructions_raw.lower()
        elif isinstance(plan_instructions_raw, (dict, list)):
            plan_instructions = str(plan_instructions_raw).lower()
        else:
            plan_instructions = ""

        addressed_requirements = 0
        for req in spec_requirements:
            req_lower = req.lower()
            # Check if requirement is mentioned in plan
            if any(word in plan_instructions for word in req_lower.split()[:3]) or any(word in str(plan_files) for word in req_lower.split()[:3]):
                addressed_requirements += 1

        if spec_requirements:
            req_coverage = addressed_requirements / len(spec_requirements)
            if req_coverage < 0.7:
                score -= 0.3
                messages.append(
                    f"Plan only addresses {req_coverage:.0%} of spec requirements"
                )

        # Check if plan files match spec files (if specified)
        spec_files = spec_data.get("files", [])
        if spec_files:
            plan_file_set = set(plan_files)
            spec_file_set = set(spec_files)
            overlap = len(plan_file_set & spec_file_set) / len(spec_file_set) if spec_file_set else 0
            if overlap < 0.5:
                score -= 0.2
                messages.append(
                    f"Plan files only overlap {overlap:.0%} with spec files"
                )

        return max(0.0, score), messages


class ImplementationValidator:
    """Validate implementation against spec."""

    @staticmethod
    def validate_implementation_against_spec(
        executor_report: dict[str, Any], spec_data: dict[str, Any]
    ) -> tuple[float, list[str]]:
        """
        Validate implementation against spec.

        Args:
            executor_report: Executor report dictionary
            spec_data: Parsed spec data

        Returns:
            Tuple of (compliance_score, messages)
        """
        score = 1.0
        messages = []

        # Check if implementation was successful
        success = executor_report.get("success", False)
        if not success:
            score = 0.0
            messages.append("Implementation failed")
            return score, messages

        # Check if files were modified as expected
        modified_files = executor_report.get("files_changed", [])
        spec_files = spec_data.get("files", [])

        if spec_files:
            modified_file_set = set(modified_files)
            spec_file_set = set(spec_files)
            overlap = len(modified_file_set & spec_file_set) / len(spec_file_set) if spec_file_set else 0
            if overlap < 0.5:
                score -= 0.3
                messages.append(
                    f"Modified files only overlap {overlap:.0%} with spec files"
                )

        # Check acceptance criteria (if available in executor report)
        # This would require executor to report on acceptance criteria
        # For now, we assume full compliance if implementation succeeded

        return max(0.0, score), messages


class LLMSemanticValidator:
    """LLM-assisted semantic validation."""

    @staticmethod
    @ollama_retry
    def validate_semantically(
        spec_data: dict[str, Any],
        plan_data: dict[str, Any] | None = None,
        executor_report: dict[str, Any] | None = None,
    ) -> tuple[float, list[str]]:
        """
        Use LLM to semantically validate spec compliance.

        Args:
            spec_data: Parsed spec data
            plan_data: Optional plan data
            executor_report: Optional executor report

        Returns:
            Tuple of (compliance_score, messages)
        """
        policy = get_policy_provider()
        llm_config = policy.get_llm_config()

        model = llm_config.get("planner_model", "ollama/llama3.2:3b")
        api_base = llm_config.get("api_base", "http://localhost:11434")

        # Build validation prompt
        prompt = f"""Evaluate spec compliance and return a JSON response.

Spec:
- Objective: {spec_data.get('objective', 'N/A')}
- Requirements: {json.dumps(spec_data.get('requirements', []))}
- Acceptance Criteria: {json.dumps(spec_data.get('acceptance_criteria', []))}
"""

        if plan_data:
            prompt += f"""
Plan:
- Objective: {plan_data.get('objective', 'N/A')}
- Files: {json.dumps(plan_data.get('files', []))}
- Instructions: {plan_data.get('instructions', 'N/A')[:500]}
"""

        if executor_report:
            prompt += f"""
Implementation:
- Success: {executor_report.get('success', False)}
- Files Changed: {json.dumps(executor_report.get('files_changed', []))}
"""

        prompt += """
Return JSON with:
{
  "compliance_score": 0.0-1.0,
  "messages": ["message1", "message2"],
  "reasoning": "brief explanation"
}
"""

        try:
            from .logging import llm_call_with_logging

            # Try to get run_path and trace_id from context if available
            run_path = None
            trace_id = None
            if isinstance(spec_data, dict) and "run_path" in spec_data:
                run_path = spec_data.get("run_path")
            elif hasattr(spec_data, "run_path"):
                run_path = spec_data.run_path
                trace_id = getattr(spec_data, "trace_id", None)

            response = llm_call_with_logging(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                run_path=run_path,
                trace_id=trace_id,
                api_base=api_base,
            )

            content = response.choices[0].message.content.strip()

            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()

            result = json.loads(content)

            score = float(result.get("compliance_score", 0.5))
            messages = result.get("messages", [])

            return max(0.0, min(1.0, score)), messages

        except Exception as e:
            # Fallback: return neutral score
            return 0.5, [f"LLM validation failed: {e!s}"]


def validate_spec(ctx: RunContext) -> dict[str, Any]:
    """
    Validate spec structure and completeness.

    Args:
        ctx: Run context

    Returns:
        Validation result dictionary
    """
    # Try multiple spec locations
    spec_paths = [
        ctx.run_path / "artifacts" / "SPEC.md",  # Primary location (from spec_node)
        PROJECT_ROOT / "docs" / "specs" / f"{ctx.task_id}_SPEC.md",  # Legacy location
    ]

    spec_path = None
    for path in spec_paths:
        if path.exists():
            spec_path = path
            break

    if not spec_path:
        return {
            "spec_exists": False,
            "compliance_score": None,
            "messages": ["Spec not found"],
        }

    # Parse spec
    parser = SpecParser()
    spec_data = parser.parse_spec(spec_path)

    # Validate spec structure
    score = 1.0
    messages = []

    if not spec_data.get("objective"):
        score -= 0.3
        messages.append("Spec missing objective")

    if not spec_data.get("requirements"):
        score -= 0.2
        messages.append("Spec missing requirements")

    if not spec_data.get("acceptance_criteria"):
        score -= 0.2
        messages.append("Spec missing acceptance criteria")

    return {
        "spec_exists": True,
        "spec_data": spec_data,
        "compliance_score": max(0.0, score),
        "messages": messages,
    }


def validate_plan_against_spec(ctx: RunContext) -> dict[str, Any]:
    """
    Validate plan against spec.

    Args:
        ctx: Run context

    Returns:
        Validation result dictionary
    """
    # Try multiple spec locations
    spec_paths = [
        ctx.run_path / "artifacts" / "SPEC.md",  # Primary location (from spec_node)
        PROJECT_ROOT / "docs" / "specs" / f"{ctx.task_id}_SPEC.md",  # Legacy location
    ]

    spec_path = None
    for path in spec_paths:
        if path.exists():
            spec_path = path
            break

    plan_path = ctx.plan_path

    if not spec_path:
        return {
            "spec_exists": False,
            "compliance_score": None,
            "messages": ["Spec not found"],
        }

    if not plan_path.exists():
        return {
            "plan_exists": False,
            "compliance_score": 0.0,
            "messages": ["Plan not found"],
        }

    # Parse spec and plan
    parser = SpecParser()
    spec_data = parser.parse_spec(spec_path)

    plan_data = json.loads(plan_path.read_text(encoding="utf-8"))

    # Validate plan
    validator = PlanValidator()
    score, messages = validator.validate_plan_against_spec(plan_data, spec_data)

    return {
        "spec_exists": True,
        "plan_exists": True,
        "compliance_score": score,
        "messages": messages,
    }


def validate_implementation_against_spec(ctx: RunContext) -> dict[str, Any]:
    """
    Validate implementation against spec.

    Args:
        ctx: Run context

    Returns:
        Validation result dictionary
    """
    # Try multiple spec locations
    spec_paths = [
        ctx.run_path / "artifacts" / "SPEC.md",  # Primary location (from spec_node)
        PROJECT_ROOT / "docs" / "specs" / f"{ctx.task_id}_SPEC.md",  # Legacy location
    ]

    spec_path = None
    for path in spec_paths:
        if path.exists():
            spec_path = path
            break

    executor_report_path = ctx.executor_report_path

    if not spec_path:
        return {
            "spec_exists": False,
            "compliance_score": None,
            "messages": ["Spec not found"],
        }

    if not executor_report_path.exists():
        return {
            "executor_report_exists": False,
            "compliance_score": 0.0,
            "messages": ["Executor report not found"],
        }

    # Parse spec and executor report
    parser = SpecParser()
    spec_data = parser.parse_spec(spec_path)

    executor_report = json.loads(executor_report_path.read_text(encoding="utf-8"))

    # Validate implementation
    validator = ImplementationValidator()
    score, messages = validator.validate_implementation_against_spec(
        executor_report, spec_data
    )

    # Also run LLM semantic validation
    llm_validator = LLMSemanticValidator()
    llm_score, llm_messages = llm_validator.validate_semantically(
        spec_data, executor_report=executor_report
    )

    # Combine scores (weighted average: 70% rule-based, 30% LLM)
    combined_score = (score * 0.7) + (llm_score * 0.3)
    all_messages = messages + llm_messages

    return {
        "spec_exists": True,
        "executor_report_exists": True,
        "compliance_score": combined_score,
        "messages": all_messages,
        "rule_based_score": score,
        "llm_score": llm_score,
    }


def generate_spec_validation_artifact(ctx: RunContext) -> Path | None:
    """
    Generate comprehensive spec_validation.json artifact.

    This runs all validation phases and generates a complete report.

    Args:
        ctx: Run context

    Returns:
        Path to generated artifact, or None if spec doesn't exist
    """
    # Try multiple spec locations
    spec_paths = [
        ctx.run_path / "artifacts" / "SPEC.md",  # Primary location (from spec_node)
        PROJECT_ROOT / "docs" / "specs" / f"{ctx.task_id}_SPEC.md",  # Legacy location
    ]

    spec_path = None
    for path in spec_paths:
        if path.exists():
            spec_path = path
            break

    if not spec_path:
        return None

    # Run all validation phases
    spec_validation = validate_spec(ctx)
    plan_validation = validate_plan_against_spec(ctx)
    impl_validation = validate_implementation_against_spec(ctx)

    # Calculate overall compliance score
    scores = []
    if spec_validation.get("compliance_score") is not None:
        scores.append(spec_validation["compliance_score"])
    if plan_validation.get("compliance_score") is not None:
        scores.append(plan_validation["compliance_score"])
    if impl_validation.get("compliance_score") is not None:
        scores.append(impl_validation["compliance_score"])

    overall_score = sum(scores) / len(scores) if scores else 0.0

    # Build validation artifact
    validation_data = {
        "task_id": ctx.task_id,
        "run_id": ctx.run_id,
        "validated_at": datetime.now().isoformat(),
        "compliance_score": overall_score,
        "validation_phases": {
            "spec_validation": spec_validation,
            "plan_validation": plan_validation,
            "implementation_validation": impl_validation,
        },
        "messages": (
            spec_validation.get("messages", [])
            + plan_validation.get("messages", [])
            + impl_validation.get("messages", [])
        ),
    }

    # Write artifact
    artifact_path = ctx.run_path / "artifacts" / "spec_validation.json"
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(json.dumps(validation_data, indent=2), encoding="utf-8")

    return artifact_path
