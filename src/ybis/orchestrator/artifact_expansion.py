"""
Artifact Expansion - Additional reports and analysis.

Expands verification artifacts with:
- Dependency impact reports
- Spec compliance summaries
- Code quality metrics
- Change impact analysis
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

from ..contracts import RunContext
from ..services.mcp_tools.dependency_tools import check_dependency_impact


def generate_dependency_impact_report(ctx: RunContext) -> Path | None:
    """
    Generate dependency impact report.

    Args:
        ctx: Run context

    Returns:
        Path to dependency impact report, or None if not available
    """
    # Get modified files from executor report
    executor_report_path = ctx.executor_report_path
    if not executor_report_path.exists():
        return None

    try:
        executor_data = json.loads(executor_report_path.read_text(encoding="utf-8"))
        modified_files = executor_data.get("modified_files", [])

        if not modified_files:
            return None

        # Generate impact analysis for each modified file
        impact_data = {
            "task_id": ctx.task_id,
            "run_id": ctx.run_id,
            "modified_files": [],
            "total_impact": 0,
        }

        for file_path in modified_files:
            # Use dependency tools to check impact
            impact_text = check_dependency_impact(file_path, max_depth=3)

            # Parse impact (simplified - full implementation would parse structured data)
            affected_count = impact_text.count("files will be affected") if "files will be affected" in impact_text else 0

            impact_data["modified_files"].append(
                {
                    "file": file_path,
                    "impact_text": impact_text,
                    "affected_count": affected_count,
                }
            )
            impact_data["total_impact"] += affected_count

        # Write report
        report_path = ctx.run_path / "artifacts" / "dependency_impact.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(impact_data, indent=2), encoding="utf-8")

        return report_path

    except Exception:
        # Silently fail if dependency analysis is not available
        return None


def generate_spec_compliance_summary(ctx: RunContext) -> Path | None:
    """
    Generate spec compliance summary.

    Args:
        ctx: Run context

    Returns:
        Path to spec compliance summary, or None if spec not available
    """
    from ..constants import PROJECT_ROOT

    # Check if spec exists
    spec_path = PROJECT_ROOT / "docs" / "specs" / f"{ctx.task_id}_SPEC.md"
    if not spec_path.exists():
        return None

    # Check for spec validation artifact
    spec_validation_path = ctx.run_path / "artifacts" / "spec_validation.json"
    if not spec_validation_path.exists():
        return None

    try:
        validation_data = json.loads(spec_validation_path.read_text(encoding="utf-8"))

        # Generate summary
        summary = {
            "task_id": ctx.task_id,
            "run_id": ctx.run_id,
            "spec_exists": True,
            "compliance_score": validation_data.get("compliance_score", 0.0),
            "validation_messages": validation_data.get("messages", []),
            "validated_at": validation_data.get("validated_at"),
        }

        # Write summary
        summary_path = ctx.run_path / "artifacts" / "spec_compliance_summary.json"
        summary_path.parent.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")

        return summary_path

    except Exception:
        return None


def generate_code_quality_metrics(ctx: RunContext) -> Path | None:
    """
    Generate code quality metrics.

    Args:
        ctx: Run context

    Returns:
        Path to code quality metrics, or None if not available
    """
    # Get verifier report
    verifier_report_path = ctx.run_path / "artifacts" / "verifier_report.json"
    if not verifier_report_path.exists():
        return None

    try:
        verifier_data = json.loads(verifier_report_path.read_text(encoding="utf-8"))

        # Extract metrics
        metrics = {
            "task_id": ctx.task_id,
            "run_id": ctx.run_id,
            "lint_passed": verifier_data.get("lint_passed", False),
            "tests_passed": verifier_data.get("tests_passed", False),
            "coverage": verifier_data.get("coverage", 0.0),
            "warnings": verifier_data.get("warnings", []),
            "errors": verifier_data.get("errors", []),
        }

        # Write metrics
        metrics_path = ctx.run_path / "artifacts" / "code_quality_metrics.json"
        metrics_path.parent.mkdir(parents=True, exist_ok=True)
        metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

        return metrics_path

    except Exception:
        return None


def generate_all_artifacts(ctx: RunContext) -> dict[str, Path | None]:
    """
    Generate all expanded artifacts.

    Args:
        ctx: Run context

    Returns:
        Dictionary of artifact types to paths
    """
    return {
        "dependency_impact": generate_dependency_impact_report(ctx),
        "spec_compliance_summary": generate_spec_compliance_summary(ctx),
        "code_quality_metrics": generate_code_quality_metrics(ctx),
    }


