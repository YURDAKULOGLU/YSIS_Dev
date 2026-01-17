"""
Evidence schemas - "Proof of Work" artifacts.

All evidence reports inherit from BaseEvidence and include schema_version for migration compatibility.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class GateDecision(str, Enum):
    """Gate decision types."""

    PASS = "PASS"
    BLOCK = "BLOCK"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"


class BaseEvidence(BaseModel):
    """Base evidence model - all evidence reports inherit from this."""

    schema_version: int = Field(default=1, description="Schema version for migration compatibility")
    timestamp: datetime = Field(default_factory=datetime.now, description="Evidence creation timestamp")
    task_id: str = Field(..., description="Task identifier")
    run_id: str = Field(..., description="Run identifier")

    @field_serializer("timestamp")
    def serialize_datetime(self, value: datetime, _info) -> str:
        """Serialize datetime to ISO format."""
        return value.isoformat()

    model_config = ConfigDict(frozen=False)


class VerifierReport(BaseEvidence):
    """Verifier report - lint and test results."""

    lint_passed: bool = Field(..., description="Lint check passed")
    tests_passed: bool = Field(..., description="Tests passed")
    coverage: float = Field(default=0.0, ge=0.0, le=1.0, description="Test coverage (0.0-1.0)")
    errors: list[str] = Field(default_factory=list, description="Verification errors")
    warnings: list[str] = Field(default_factory=list, description="Verification warnings")
    metrics: dict[str, Any] = Field(default_factory=dict, description="Additional metrics")


class GateReport(BaseEvidence):
    """Gate report - deterministic gate decision."""

    decision: GateDecision = Field(..., description="Gate decision (PASS/BLOCK/REQUIRE_APPROVAL)")
    risk_score: int = Field(default=0, ge=0, le=100, description="Risk score (0-100)")
    policy_snapshot_hash: str | None = Field(default=None, description="Policy snapshot hash reference")
    approval_required: bool = Field(default=False, description="Approval required")
    approval_present: bool = Field(default=False, description="Approval present")
    reasons: list[str] = Field(default_factory=list, description="Decision reasons")
    protected_paths_touched: list[str] = Field(default_factory=list, description="Protected paths touched")
    spec_compliance_score: float | None = Field(
        default=None, ge=0.0, le=1.0, description="Spec compliance score (0.0-1.0), None if spec not available"
    )
    spec_compliance_threshold: float = Field(
        default=0.7, ge=0.0, le=1.0, description="Spec compliance threshold (default: 0.7)"
    )


class ExecutorReport(BaseEvidence):
    """Executor report - execution results."""

    success: bool = Field(..., description="Execution successful")
    files_changed: list[str] = Field(default_factory=list, description="Files changed during execution")
    commands_run: list[str] = Field(default_factory=list, description="Commands executed")
    outputs: dict[str, str] = Field(default_factory=dict, description="Command outputs")
    error: str | None = Field(default=None, description="Execution error if any")


class PatchApplyReport(BaseEvidence):
    """Patch apply report - patch application results."""

    success: bool = Field(..., description="Patch application successful")
    hunks_applied: int = Field(default=0, ge=0, description="Number of hunks applied")
    files_modified: list[str] = Field(default_factory=list, description="Files modified")
    protected_paths_blocked: list[str] = Field(default_factory=list, description="Protected paths blocked")
    diff: str | None = Field(default=None, description="Applied diff")

