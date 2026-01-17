"""
Run context - Lightweight context object for workflow execution.

Crucial: This does NOT hold plan or result data. Only paths.
"""

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from ..constants import ARTIFACTS_DIR, JOURNAL_DIR


class RunContext(BaseModel):
    """
    Run context - lightweight context for workflow execution.

    This is NOT a "God Object". It only holds:
    - Task and run identifiers
    - Trace ID for distributed tracing
    - Paths to artifacts (not the artifacts themselves)

    This keeps memory usage low and allows for lazy loading of artifacts.
    """

    task_id: str = Field(..., description="Task identifier")
    run_id: str = Field(..., description="Run identifier")
    run_path: Path = Field(..., description="Path to run directory")
    trace_id: str = Field(..., description="Unique trace ID for distributed tracing")

    @field_serializer("run_path")
    def serialize_path(self, value: Path, _info) -> str:
        """Serialize Path to string."""
        return str(value)

    @property
    def plan_path(self) -> Path:
        """Path to plan.json artifact."""
        return self.run_path / ARTIFACTS_DIR / "plan.json"

    @property
    def verifier_report_path(self) -> Path:
        """Path to verifier_report.json artifact."""
        return self.run_path / ARTIFACTS_DIR / "verifier_report.json"

    @property
    def gate_report_path(self) -> Path:
        """Path to gate_report.json artifact."""
        return self.run_path / ARTIFACTS_DIR / "gate_report.json"

    @property
    def executor_report_path(self) -> Path:
        """Path to executor_report.json artifact."""
        return self.run_path / ARTIFACTS_DIR / "executor_report.json"

    @property
    def patch_apply_report_path(self) -> Path:
        """Path to patch_apply_report.json artifact."""
        return self.run_path / ARTIFACTS_DIR / "patch_apply_report.json"

    @property
    def journal_path(self) -> Path:
        """Path to journal events.jsonl file."""
        return self.run_path / JOURNAL_DIR / "events.jsonl"

    @property
    def artifacts_dir(self) -> Path:
        """Path to artifacts directory."""
        return self.run_path / ARTIFACTS_DIR

    @property
    def journal_dir(self) -> Path:
        """Path to journal directory."""
        return self.run_path / JOURNAL_DIR

    model_config = ConfigDict(frozen=False)

