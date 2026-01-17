"""
Executor Protocol - Interface for coding agents (Aider, OpenHands, etc.).

Defines the contract that any executor must implement.
"""

from typing import Protocol

from .context import RunContext
from .evidence import ExecutorReport


class Plan:
    """Plan model - represents execution plan."""

    def __init__(
        self,
        objective: str,
        files: list[str] | None = None,
        instructions: str | None = None,
        steps: list[dict] | None = None,
        referenced_context: list[dict] | None = None,
    ):
        """
        Initialize plan.

        Args:
            objective: Task objective/description
            files: List of file paths to modify
            instructions: Additional instructions
            steps: Ordered list of steps (each step is a dict with 'action', 'files', 'description')
            referenced_context: RAG context used for planning
        """
        self.objective = objective
        self.files = files or []
        self.instructions = instructions
        self.steps = steps or []
        self.referenced_context = referenced_context or []


class ExecutorProtocol(Protocol):
    """
    Executor Protocol - Interface for coding agents.

    Any executor (Aider, OpenHands, etc.) must implement this interface.
    """

    def generate_code(self, ctx: RunContext, plan: Plan) -> ExecutorReport:
        """
        Generate code based on plan.

        Args:
            ctx: Run context
            plan: Execution plan

        Returns:
            ExecutorReport with execution results
        """
        ...


# ============================================================================
# Vendor Adapter Protocols (ADAPTER_INTEGRATION_PLAN.md)
# ============================================================================


class WorkflowEvolutionProtocol(Protocol):
    """
    Workflow Evolution Protocol - Interface for workflow optimization adapters.

    Used by EvoAgentX and similar systems for workflow evolution and optimization.
    """

    def evolve(self, workflow_spec: dict, metrics: dict) -> dict:
        """
        Evolve workflow spec based on metrics.

        Args:
            workflow_spec: Current workflow specification (YAML dict)
            metrics: Performance metrics (e.g., execution time, success rate)

        Returns:
            Updated workflow specification dict
        """
        ...

    def score(self, workflow_spec: dict, artifacts: dict) -> float:
        """
        Score workflow spec based on artifacts.

        Args:
            workflow_spec: Workflow specification (YAML dict)
            artifacts: Run artifacts (e.g., verifier_report, gate_report)

        Returns:
            Score (0.0-1.0) indicating workflow quality
        """
        ...


class AgentRuntimeProtocol(Protocol):
    """
    Agent Runtime Protocol - Interface for agent runtime adapters.

    Used by reactive-agents and similar systems for tool-using agent execution.
    """

    def run(self, task: str, tools: list[str], context: dict) -> dict:
        """
        Run agent with task, tools, and context.

        Args:
            task: Task description/objective
            tools: List of available tool names
            context: Additional context (e.g., codebase state, previous results)

        Returns:
            Execution result dict with status, output, artifacts
        """
        ...

    def supports_tools(self) -> bool:
        """
        Check if adapter supports tool usage.

        Returns:
            True if adapter supports tools, False otherwise
        """
        ...


class CouncilReviewProtocol(Protocol):
    """
    Council Review Protocol - Interface for multi-model review adapters.

    Used by llm-council and similar systems for multi-model review and ranking.
    """

    def review(self, prompt: str, candidates: list[str]) -> dict:
        """
        Review candidates using multiple models and return ranking.

        Args:
            prompt: Review prompt/question
            candidates: List of candidate solutions/responses to review

        Returns:
            Review result dict with ranking, consensus, scores
        """
        ...


class AgentLearningProtocol(Protocol):
    """
    Agent Learning Protocol - Interface for agent learning adapters.

    Used by aiwaves-agents and similar systems for symbolic learning and optimization.
    """

    def learn(self, trajectory: dict) -> dict:
        """
        Learn from execution trajectory.

        Args:
            trajectory: Execution trajectory (states, actions, rewards)

        Returns:
            Learning result dict with insights, patterns, improvements
        """
        ...

    def update_pipeline(self, pipeline: dict, gradients: dict) -> dict:
        """
        Update agent pipeline based on gradients.

        Args:
            pipeline: Current pipeline configuration
            gradients: Learning gradients/updates

        Returns:
            Updated pipeline configuration dict
        """
        ...


class SelfImproveLoopProtocol(Protocol):
    """
    Self-Improve Loop Protocol - Interface for self-improvement adapters.

    Used by Self-Improve-Swarms and similar systems for reflection-based improvement.
    """

    def reflect(self, state: dict) -> dict:
        """
        Reflect on current state and identify improvements.

        Args:
            state: Current system state (e.g., codebase, tests, metrics)

        Returns:
            Reflection result dict with insights, issues, opportunities
        """
        ...

    def plan(self, reflection: dict) -> dict:
        """
        Plan improvements based on reflection.

        Args:
            reflection: Reflection result from reflect()

        Returns:
            Improvement plan dict with tasks, priorities, dependencies
        """
        ...

    def implement(self, plan: dict) -> dict:
        """
        Implement improvement plan.

        Args:
            plan: Improvement plan from plan()

        Returns:
            Implementation result dict with changes, artifacts, status
        """
        ...

    def test(self, implementation: dict) -> dict:
        """
        Test implementation.

        Args:
            implementation: Implementation result from implement()

        Returns:
            Test result dict with pass/fail, coverage, metrics
        """
        ...

    def integrate(self, result: dict) -> dict:
        """
        Integrate tested implementation.

        Args:
            result: Test result from test()

        Returns:
            Integration result dict with status, merged changes, artifacts
        """
        ...

