"""
Contracts - Pydantic models for tasks, runs, evidence reports.
"""

from .context import RunContext
from .evidence import (
    BaseEvidence,
    ExecutorReport,
    GateDecision,
    GateReport,
    PatchApplyReport,
    VerifierReport,
)
from .protocol import (
    AgentLearningProtocol,
    AgentRuntimeProtocol,
    CouncilReviewProtocol,
    ExecutorProtocol,
    Plan,
    SelfImproveLoopProtocol,
    WorkflowEvolutionProtocol,
)
from .resources import Run, Task

__all__ = [
    "Task",
    "Run",
    "RunContext",
    "BaseEvidence",
    "VerifierReport",
    "GateReport",
    "ExecutorReport",
    "PatchApplyReport",
    "GateDecision",
    "ExecutorProtocol",
    "Plan",
    # Vendor adapter protocols
    "WorkflowEvolutionProtocol",
    "AgentRuntimeProtocol",
    "CouncilReviewProtocol",
    "AgentLearningProtocol",
    "SelfImproveLoopProtocol",
]
