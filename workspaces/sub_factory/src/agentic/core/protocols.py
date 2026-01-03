"""
Protocol definitions for orchestrator_v3 plugin architecture.

This module defines the contracts that all plugins must implement.
Allows easy swapping of implementations without changing core logic.
"""

from datetime import datetime
from typing import Any, Protocol, Literal
from src.agentic.core.utils.logging_utils import log_event
from uuid import uuid4

from pydantic import BaseModel, Field
try:
    from pydantic import ConfigDict
except Exception:
    ConfigDict = None

# ============================================================================
# CONSTANTS & STANDARDS
# ============================================================================
MAX_FILES_PER_TASK = 50
MIN_TEST_COVERAGE = 0.7

# ============================================================================
# DATA MODELS (Using Pydantic - The Industry Standard)
# ============================================================================

class Plan(BaseModel):
    """Structured plan output from planners"""
    objective: str
    steps: list[str]
    files_to_modify: list[str]
    dependencies: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    success_criteria: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

class CodeResult(BaseModel):
    """Result from code execution"""
    files_modified: dict[str, str] = Field(default_factory=dict) # path -> content/status
    commands_run: list[str] = Field(default_factory=list)
    outputs: dict[str, str] = Field(default_factory=dict) # command -> output
    success: bool
    error: str | None = None

class VerificationResult(BaseModel):
    """Result from verification/testing"""
    lint_passed: bool
    tests_passed: bool
    coverage: float = 0.0
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    logs: dict[str, Any] = Field(default_factory=dict)

class ProposedTask(BaseModel):
    """A task proposed by an agent to be added to the backlog."""
    title: str
    description: str
    priority: str = "MEDIUM"

class TaskState(BaseModel):
    """The central State object for the entire factory. Supports task chaining."""
    task_id: str = Field(default="UNKNOWN")
    task_description: str = Field(default="")
    context: dict[str, Any] = Field(default_factory=dict)
    artifacts_path: str = Field(default=".sandbox_worker/default")
    phase: str = "init"
    plan: Plan | None = None
    code_result: CodeResult | None = None
    verification: VerificationResult | None = None
    retry_count: int = 0
    max_retries: int = 3
    error: str | None = None
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: datetime | None = None
    error_history: list[str] = Field(default_factory=list)
    failed_at: datetime | None = None
    files_modified: list[str] = Field(default_factory=list)
    quality_score: float = 0.0
    final_status: str = "UNKNOWN"
    proposed_tasks: list[ProposedTask] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True

class InterAgentMessage(BaseModel):
    """
    Universal message schema for inter-agent communication.

    Enforces strict typing for all agent-to-agent messages across:
    - File-based messaging
    - MCP tools
    - Redis pub/sub
    - REST API

    Based on DEBATE-20251227202515 (Messaging System Hardening).
    """
    # Core Identity
    id: str = Field(default_factory=lambda: f"MSG-{datetime.now().strftime('%Y%m%d%H%M%S')}")
    from_agent: str = Field(description="Agent ID of sender (e.g., 'claude-code', 'gemini-cli')")
    to: str | list[str] = Field(description="Recipient agent ID(s) or 'all' for broadcast")

    # Message Content
    subject: str = Field(description="Message subject line")
    content: str = Field(description="Message body (supports markdown)")
    message_type: Literal["broadcast", "direct", "debate", "task_assignment", "ack"] = "direct"

    # Threading & Context
    reply_to: str | None = Field(default=None, description="ID of message being replied to")
    thread_id: str | None = Field(default=None, description="Thread identifier for conversation grouping")
    debate_id: str | None = Field(default=None, description="Debate ID if this is a debate message")

    # Priority & Classification
    priority: Literal["CRITICAL", "HIGH", "NORMAL", "LOW"] = "NORMAL"
    tags: list[str] = Field(default_factory=list, description="Tags for filtering (e.g., ['urgent', 'project-neo'])")

    # Delivery Tracking
    timestamp: datetime = Field(default_factory=datetime.now)
    seen_by: list[str] = Field(default_factory=list, description="List of agent IDs who have read this message")
    ack_by: dict[str, str] = Field(default_factory=dict, description="Agent ID -> ACK status (noted, will_do, done)")

    # Metadata
    metadata: dict[str, Any] = Field(default_factory=dict, description="Extensible metadata field")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "MSG-20251227203000",
                "from_agent": "claude-code",
                "to": "gemini-cli",
                "subject": "PROJECT NEO Complete",
                "content": "Graph ingestion finished. 88 CodeFiles, 52 DocFiles.",
                "message_type": "direct",
                "priority": "HIGH",
                "tags": ["project-neo", "completion"],
                "timestamp": "2025-12-27T20:30:00",
                "seen_by": [],
                "ack_by": {}
            }
        }


# ============================================================================
# PROTOCOLS (Interfaces for plugins)
# ============================================================================

class PlannerProtocol(Protocol):
    """
    Interface that all planners must implement.

    A planner analyzes a task and generates a structured execution plan.
    Can be implemented by:
    - CrewAI-based planner
    - Simple LLM prompt planner
    - Rule-based planner
    - etc.
    """

    async def plan(self, task: str, context: dict[str, Any]) -> Plan:
        """
        Generate execution plan for the task.

        Args:
            task: Task description from TASK_BOARD
            context: Additional context (repo state, files, etc)

        Returns:
            Structured Plan object
        """
        ...

    def name(self) -> str:
        """Return planner identifier (for logging)"""
        ...


class ExecutorProtocol(Protocol):
    """
    Interface that all executors must implement.

    An executor takes a plan and produces code/changes.
    Can be implemented by:
    - Local agent executor (Ollama)
    - OpenHands executor
    - Claude API executor
    - etc.
    """

    async def execute(
        self,
        plan: Plan,
        sandbox_path: str,
        error_history: list[str] | None = None,
        retry_count: int = 0
    ) -> CodeResult:
        """
        Execute the plan and generate code.
        """
        ...

    def name(self) -> str:
        """Return executor identifier"""
        ...


class VerifierProtocol(Protocol):
    """
    Interface that all verifiers must implement.
    """

    async def verify(self, code_result: CodeResult, sandbox_path: str) -> VerificationResult:
        """
        Verify code quality and correctness.
        """
        ...

    def name(self) -> str:
        """Return verifier identifier"""
        ...


class ArtifactGeneratorProtocol(Protocol):
    """
    Interface for artifact generation.
    """

    async def generate(self, state: TaskState) -> dict[str, str]:
        """
        Generate all artifacts for current state.
        """
        ...


class TaskBoardProtocol(Protocol):
    """
    Interface for TASK_BOARD integration.
    """

    async def get_next_task(self) -> dict[str, Any] | None:
        """Get next IN PROGRESS task assigned to current agent"""
        ...

    async def update_task_status(self, task_id: str, status: str, metadata: dict[str, Any]) -> None:
        """Update task status in TASK_BOARD"""
        ...

    async def create_task(self, title: str, description: str, priority: str) -> str:
        """Create new task, return task_id"""
        ...


# ============================================================================
# GATE VALIDATORS (Core logic - not pluggable)
# ============================================================================

class GateValidator:
    """
    Built-in validation logic for gates.
    """

    @staticmethod
    def validate_plan(plan: Plan) -> tuple[bool, str | None]:
        """
        Validate that plan is actionable.
        """
        if not plan.objective:
            return False, "Plan has no objective"

        if len(plan.steps) == 0:
            return False, "Plan has no steps"

        if len(plan.files_to_modify) == 0:
            return False, "Plan specifies no files to modify"

        # Check file count limits (from Constitution)
        file_count = len(plan.files_to_modify)
        if file_count > MAX_FILES_PER_TASK:
            return False, f"Plan modifies too many files ({file_count} > {MAX_FILES_PER_TASK})."

        return True, None

    @staticmethod
    def validate_code(code_result: CodeResult) -> tuple[bool, str | None]:
        """
        Validate that code execution succeeded.
        """
        if not code_result.success:
            return False, code_result.error or "Code execution failed"

        if len(code_result.files_modified) == 0:
            return False, "No files were modified"

        # Basic syntax check
        for path, content in code_result.files_modified.items():
            if not content or len(content.strip()) == 0:
                return False, f"File {path} is empty"

        return True, None

    @staticmethod
    def validate_verification(verification: VerificationResult) -> tuple[bool, str | None]:
        """
        Validate that verification passed.
        """
        if not verification.lint_passed:
            return False, f"Lint failed: {', '.join(verification.errors)}"

        if not verification.tests_passed:
            return False, f"Tests failed: {', '.join(verification.errors)}"

        # Coverage check
        if verification.coverage < MIN_TEST_COVERAGE:
            return False, f"Coverage too low: {verification.coverage:.1%} < {MIN_TEST_COVERAGE:.0%}"

        return True, None

    @staticmethod
    def should_retry(state: TaskState) -> bool:
        """
        Check if we should retry after failure.
        CRITICAL: Do not retry on security violations.
        """
        # 1. Check for Security Violations (Fast Fail)
        last_error = state.error
        if not last_error and state.error_history:
            last_error = state.error_history[-1]

        if last_error and ("VIOLATION" in last_error or "⛔" in last_error):
            log_event("🛑 SECURITY VIOLATION DETECTED. NO RETRY ALLOWED.", component="gate_validator", level="warning")
            return False

        # 2. Check Retry Count
        return state.retry_count < state.max_retries
