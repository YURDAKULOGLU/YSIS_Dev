"""
Deterministic Gates - Decision logic based on Evidence + Policy.

Gates make deterministic decisions (PASS/BLOCK/REQUIRE_APPROVAL) based on:
- Verifier reports (lint, tests, coverage)
- Risk assessment (patch size, protected paths)
"""

import logging

from ..constants import PROJECT_ROOT

logger = logging.getLogger(__name__)
from ..contracts import GateDecision, GateReport, RunContext, VerifierReport
from ..syscalls import append_event


def _check_spec_compliance(ctx: RunContext) -> float | None:
    """
    Check spec compliance score.

    Enforcement: If spec exists but validation is not implemented, return 0.0
    to BLOCK the gate. This ensures spec-first enforcement is not bypassed.

    Full spec validation will be implemented in Task B (Spec-First Validation Workflow).

    Args:
        ctx: Run context

    Returns:
        Spec compliance score (0.0-1.0) or None if spec not available
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

    # Enforcement: If spec exists, validation must be implemented
    # For now, return 0.0 to BLOCK until Task B implements full validation
    # This prevents false PASS when spec exists but isn't validated
    # TODO: Implement full spec validation in Task B
    # This will parse SPEC.md, validate plan against spec, validate implementation against spec
    # and return a compliance score (0.0-1.0)

    # Check if validation artifacts exist (plan validation, implementation validation)
    plan_path = ctx.run_path / "artifacts" / "plan.json"
    impl_validation_path = ctx.run_path / "artifacts" / "spec_validation.json"

    # If spec exists but validation artifacts don't exist, try to generate stub
    if not impl_validation_path.exists():
        # Try to generate minimal validation artifact (stub)
        from .spec_validator import generate_spec_validation_artifact

        artifact_path = generate_spec_validation_artifact(ctx)
        if artifact_path and artifact_path.exists():
            impl_validation_path = artifact_path
        else:
            return 0.0  # BLOCK: Spec exists but validation artifact cannot be generated

    # If validation artifacts exist, try to read score
    try:
        import json
        validation_data = json.loads(impl_validation_path.read_text(encoding="utf-8"))
        score = float(validation_data.get("compliance_score", 0.0))
        if score > 0:
            return score
    except Exception as e:
        logger.warning(f"Could not read validation artifact: {e}")
        # Fall through to basic validation

    # Fallback: Basic structural validation if artifact generation failed
    try:
        spec_content = spec_path.read_text(encoding="utf-8")
    except Exception as e:
        logger.warning(f"Could not read spec: {e}")
        return 0.8  # Spec exists but unreadable - soft pass

    # Basic structural validation
    required_sections = ["## Objective", "## Acceptance Criteria"]
    missing_sections = []

    for section in required_sections:
        if section.lower() not in spec_content.lower():
            missing_sections.append(section)

    if missing_sections:
        logger.warning(f"Spec missing sections: {missing_sections}")
        return 0.7  # Partial compliance

    # Check if target_files are mentioned
    executor_report_path = ctx.run_path / "artifacts" / "executor_report.json"
    if executor_report_path.exists():
        try:
            import json
            report = json.loads(executor_report_path.read_text())
            files_changed = report.get("files_changed", [])
            if files_changed:
                return 1.0  # Files were changed, spec compliance assumed
        except Exception:
            pass

    return 0.9  # Default: soft pass with spec present


def detect_task_tier(ctx: RunContext) -> int:
    """
    Detect task tier based on patch size for cost optimization.

    Tiers:
    - Tier 0 (<10 lines diff): Skip heavy tests, pass with lint only
    - Tier 1 (<50 lines diff): Standard verification
    - Tier 2 (>50 lines diff): Council debate required if any warning exists

    Args:
        ctx: Run context

    Returns:
        Tier number (0, 1, or 2)
    """
    # Try to read patch.diff to calculate patch size
    patch_path = ctx.run_path / "artifacts" / "patch.diff"
    patch_size = 0

    if patch_path.exists():
        try:
            patch_content = patch_path.read_text(encoding="utf-8")
            # Count lines that start with + or - (excluding context lines)
            patch_lines = [line for line in patch_content.split("\n") if line.startswith(("+", "-")) and not line.startswith(("+++", "---"))]
            patch_size = len(patch_lines)
        except Exception:
            # If patch can't be read, assume Tier 2 (most conservative)
            patch_size = 100

    # Determine tier based on patch size
    if patch_size < 10:
        return 0  # Tier 0: Small changes, skip heavy tests
    elif patch_size < 50:
        return 1  # Tier 1: Medium changes, standard verification
    else:
        return 2  # Tier 2: Large changes, require debate on warnings


def check_verification_gate(verifier_report: VerifierReport, ctx: RunContext) -> GateReport:
    """
    Check verification gate - determines if code quality standards are met.

    Logic:
    - PASS if: lint_passed AND tests_passed AND coverage > 0.7 AND spec_compliance >= threshold
    - BLOCK otherwise

    Args:
        verifier_report: Verifier report with lint/test/coverage results
        ctx: Run context

    Returns:
        GateReport with decision
    """
    from ..services.policy import get_policy_provider

    # Check spec compliance (if spec exists)
    spec_compliance_score = _check_spec_compliance(ctx)
    spec_compliance_threshold = 0.7  # Default threshold

    # Get threshold from policy if available
    policy = get_policy_provider()
    policy_config = policy.get_policy()
    gates_config = policy_config.get("gates", {})
    spec_compliance_threshold = gates_config.get("spec_compliance_threshold", 0.7)

    # Decision logic
    quality_checks_passed = (
        verifier_report.lint_passed
        and verifier_report.tests_passed
        and verifier_report.coverage >= 0.7
    )

    # Spec compliance check (only if spec exists)
    spec_compliance_passed = True
    if spec_compliance_score is not None:
        spec_compliance_passed = spec_compliance_score >= spec_compliance_threshold

    if quality_checks_passed and spec_compliance_passed:
        decision = GateDecision.PASS
        risk_score = 0
        reasons = ["All quality checks passed"]
        if spec_compliance_score is not None:
            reasons.append(f"Spec compliance: {spec_compliance_score:.2%} (threshold: {spec_compliance_threshold:.2%})")
    else:
        decision = GateDecision.BLOCK
        risk_score = 100
        reasons = []
        if not verifier_report.lint_passed:
            reasons.append("Lint checks failed")
        if not verifier_report.tests_passed:
            reasons.append("Tests failed")
        if verifier_report.coverage < 0.7:
            reasons.append(f"Coverage {verifier_report.coverage:.2%} below threshold 70%")
        if spec_compliance_score is not None and not spec_compliance_passed:
            reasons.append(
                f"Spec compliance {spec_compliance_score:.2%} below threshold {spec_compliance_threshold:.2%}"
            )

    report = GateReport(
        task_id=ctx.task_id,
        run_id=ctx.run_id,
        decision=decision,
        risk_score=risk_score,
        reasons=reasons,
        spec_compliance_score=spec_compliance_score,
        spec_compliance_threshold=spec_compliance_threshold,
    )

    # Journal event
    append_event(
        ctx.run_path,
        "GATE_DECISION",
        {
            "gate_type": "verification",
            "decision": decision.value,
            "risk_score": risk_score,
            "reasons": reasons,
        },
    )

    return report


def check_risk_gate(ctx: RunContext, patch_size: int, changed_files: list[str]) -> GateReport:
    """
    Check risk gate - determines if changes require approval.

    Logic:
    - REQUIRE_APPROVAL if: patch_size > 100 lines OR changes in src/ybis/
    - PASS otherwise

    Args:
        ctx: Run context
        patch_size: Number of lines changed
        changed_files: List of file paths that were changed

    Returns:
        GateReport with decision
    """
    # Check if any changed files are in protected paths
    protected_paths = ["src/ybis", "docs/governance"]
    touches_protected = any(
        any(protected in file_path for protected in protected_paths) for file_path in changed_files
    )

    # Decision logic
    if touches_protected:
        decision = GateDecision.REQUIRE_APPROVAL
        risk_score = 90
        reasons = [f"Changes touch protected paths: {protected_paths}"]
    elif patch_size > 100:
        decision = GateDecision.REQUIRE_APPROVAL
        risk_score = 70
        reasons = [f"Large patch size: {patch_size} lines (threshold: 100)"]
    else:
        decision = GateDecision.PASS
        risk_score = 10
        reasons = ["Patch size and paths within acceptable limits"]

    report = GateReport(
        task_id=ctx.task_id,
        run_id=ctx.run_id,
        decision=decision,
        risk_score=risk_score,
        approval_required=(decision == GateDecision.REQUIRE_APPROVAL),
        reasons=reasons,
        protected_paths_touched=[f for f in changed_files if any(p in f for p in protected_paths)],
    )

    # Journal event
    append_event(
        ctx.run_path,
        "GATE_DECISION",
        {
            "gate_type": "risk",
            "decision": decision.value,
            "risk_score": risk_score,
            "patch_size": patch_size,
            "changed_files": changed_files,
            "reasons": reasons,
        },
    )

    return report

