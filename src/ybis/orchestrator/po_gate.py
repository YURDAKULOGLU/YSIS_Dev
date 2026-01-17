"""
PO Gate - Product Owner Validation for Execution Plans.
Enforces legacy 'Adamakıllı' standards on modern plans.
"""
from __future__ import annotations

import logging
from pathlib import Path
from typing import List, Optional

from ..contracts import Plan

logger = logging.getLogger(__name__)


class POGateResult:
    def __init__(self, passed: bool, errors: List[str]) -> None:
        self.passed = passed
        self.errors = errors


def validate_plan_gate(plan: Plan, target_files: List[str]) -> POGateResult:
    """
    Validates an execution plan against PO standards.
    Inspired by legacy po-master-checklist.md
    """
    errors = []

    # 1. Surgicality Check
    if not target_files and plan.objective.lower() != "execute task":
        errors.append(
            "PO_GATE_FAILURE: Plan has no target files defined. Blind execution is prohibited."
        )

    # 2. Scope Protection (Tier-1 Configs)
    protected_configs = ["strict.yaml", "adapters.yaml", "pyproject.toml"]
    for file in target_files:
        if any(protected in file for protected in protected_configs):
            # Special check for these files - they require explicit 'Risk' mention
            if "risk" not in plan.objective.lower() and not any(
                "risk" in str(step).lower() for step in plan.steps
            ):
                errors.append(
                    f"PO_GATE_FAILURE: Modification of protected config '{file}' requires a documented Risk Assessment in the plan."
                )

    # 3. Step Detail Check
    if len(plan.steps) < 1:
        errors.append(
            "PO_GATE_FAILURE: Plan is too abstract. At least one explicit step is required."
        )

    # 4. Constitutional Check
    # (Future: Check for 'constitution' keyword if we want to force agents to mention it)

    return POGateResult(passed=len(errors) == 0, errors=errors)


def check_security_violations(target_files: List[str]) -> Optional[str]:
    """
    Detects attempts to modify prohibited directories.
    """
    prohibited_prefixes = ["legacy/", "_archive/", ".git/"]
    for file in target_files:
        norm_file = str(Path(file).as_posix()).lower()
        if any(norm_file.startswith(prefix) for prefix in prohibited_prefixes):
            return (
                f"SECURITY_VIOLATION: Modification of {file} is strictly prohibited by AI Constitution Art 1.2."
            )

    return None
