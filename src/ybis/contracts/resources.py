"""
Resource contracts - Task and Run models.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class Task(BaseModel):
    """Task model - represents a unit of work."""

    task_id: str = Field(..., description="Unique task identifier")
    title: str = Field(..., description="Task title")
    objective: str = Field(..., description="Task objective/description")
    status: str = Field(default="pending", description="Task status (pending, running, completed, failed)")
    priority: str = Field(default="MEDIUM", description="Task priority (LOW, MEDIUM, HIGH)")
    protected: bool = Field(default=False, description="Whether this task is protected from retention")
    schema_version: int = Field(default=1, description="Schema version for migration compatibility")
    workspace_path: str | None = Field(default=None, description="Path to task workspace")
    is_sub_factory: bool = Field(default=False, description="Whether this task spawns a sub-factory")
    created_at: datetime = Field(default_factory=datetime.now, description="Task creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Task last update timestamp")

    @field_serializer("created_at", "updated_at")
    def serialize_datetime(self, value: datetime, _info) -> str:
        """Serialize datetime to ISO format."""
        return value.isoformat()

    model_config = ConfigDict(frozen=False)


class PerformanceMetrics(BaseModel):
    """Performance metrics for a run."""

    latency_ms: float = Field(default=0.0, description="Average response latency in milliseconds")
    token_count: int = Field(default=0, description="Total tokens consumed")
    gpu_load: float = Field(default=0.0, description="GPU load percentage (0-100)")
    model_type: str = Field(default="unknown", description="Model type used (e.g., 'ollama/llama3.2:3b')")
    success_rate: float = Field(default=0.0, description="Success rate (0-1)")


class Run(BaseModel):
    """Run model - represents a single execution attempt for a task."""

    run_id: str = Field(..., description="Unique run identifier")
    task_id: str = Field(..., description="Parent task identifier")
    workflow: str = Field(default="build", description="Workflow type (build, repair, research, debate, evolve)")
    status: str = Field(default="pending", description="Run status (pending, running, completed, failed, blocked)")
    risk_level: str = Field(default="low", description="Risk level (low, medium, high)")
    run_path: str = Field(..., description="Path to run directory (workspaces/<task_id>/runs/<run_id>/)")
    schema_version: int = Field(default=1, description="Schema version for migration compatibility")
    started_at: datetime | None = Field(default=None, description="Run start timestamp")
    completed_at: datetime | None = Field(default=None, description="Run completion timestamp")
    created_at: datetime = Field(default_factory=datetime.now, description="Run creation timestamp")
    performance_metrics: PerformanceMetrics | None = Field(
        default=None, description="Performance metrics (latency, tokens, GPU load)"
    )

    @field_serializer("started_at", "completed_at", "created_at")
    def serialize_datetime(self, value: datetime | None, _info) -> str | None:
        """Serialize datetime to ISO format."""
        return value.isoformat() if value is not None else None

    model_config = ConfigDict(frozen=False)

