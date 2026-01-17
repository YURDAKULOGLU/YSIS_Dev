"""
CrewAI Adapter - Multi-agent orchestration.

Provides agent-based workflow execution as an alternative to task-based workflows.
Complements YBIS's existing task-based system (spec → plan → execute → verify).
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)

# Try to import CrewAI from vendors/ (local clone) first
try:
    import sys
    from pathlib import Path

    vendors_path = Path(__file__).parent.parent.parent.parent / "vendors" / "crewai"
    if vendors_path.exists():
        sys.path.insert(0, str(vendors_path))
        try:
            from crewai import Agent, Crew, Task

            CREWAI_LOCAL_CLONE_AVAILABLE = True
            logger.info("Using CrewAI from vendors/ (local clone)")
        except ImportError:
            CREWAI_LOCAL_CLONE_AVAILABLE = False
    else:
        CREWAI_LOCAL_CLONE_AVAILABLE = False
except (ImportError, Exception) as e:
    CREWAI_LOCAL_CLONE_AVAILABLE = False
    logger.debug(f"CrewAI local clone not available: {e}")

# Try to import CrewAI from pip
if not CREWAI_LOCAL_CLONE_AVAILABLE:
    try:
        from crewai import Agent, Crew, Task

        CREWAI_PIP_AVAILABLE = True
        logger.info("Using CrewAI from pip")
    except ImportError:
        CREWAI_PIP_AVAILABLE = False
        logger.warning("CrewAI not installed. Install with: pip install crewai or clone to vendors/crewai")

# Combined availability
CREWAI_AVAILABLE = CREWAI_LOCAL_CLONE_AVAILABLE or CREWAI_PIP_AVAILABLE


class CrewAIAdapter:
    """
    CrewAI Adapter - Multi-agent orchestration.

    Provides agent-based workflow execution:
    - Multiple specialized agents working together
    - Agent autonomy and decision-making
    - Free-form execution (complements task-based workflows)

    Use cases:
    - Complex multi-step tasks requiring different expertise
    - Exploratory tasks (no clear plan upfront)
    - Agent collaboration scenarios
    """

    def __init__(self, llm_model: str | None = None, api_base: str | None = None):
        """
        Initialize CrewAI adapter.

        Args:
            llm_model: LLM model name (default from policy)
            api_base: API base URL (default from policy)
        """
        if not CREWAI_AVAILABLE:
            raise ImportError(
                "CrewAI not available. Install with: pip install crewai or clone to vendors/crewai"
            )

        from ..services.policy import get_policy_provider

        policy_provider = get_policy_provider()
        if policy_provider._policy is None:
            policy_provider.load_profile()
        llm_config = policy_provider.get_llm_config()

        self.llm_model = llm_model or llm_config.get("planner_model", "ollama/llama3.2:3b")
        self.api_base = api_base or llm_config.get("api_base", "http://localhost:11434")

        # Configure CrewAI LLM
        try:
            from langchain_community.llms import Ollama

            self.llm = Ollama(model=self.llm_model.split("/")[-1], base_url=self.api_base)
        except Exception as e:
            logger.warning(f"Failed to configure CrewAI LLM: {e}")
            self.llm = None

    def create_crew(
        self,
        agents: list[dict[str, Any]],
        tasks: list[dict[str, Any]],
        objective: str,
    ) -> Crew:
        """
        Create a Crew with agents and tasks.

        Args:
            agents: List of agent definitions (role, goal, backstory, etc.)
            tasks: List of task definitions (description, agent, expected_output)
            objective: Overall crew objective

        Returns:
            Crew instance
        """
        logger.info(f"Creating CrewAI crew: {len(agents)} agents, {len(tasks)} tasks, objective={objective[:50]}")
        if not CREWAI_AVAILABLE:
            raise ImportError("CrewAI not available")

        # Create agents
        crew_agents = []
        for agent_def in agents:
            agent = Agent(
                role=agent_def.get("role", "Agent"),
                goal=agent_def.get("goal", ""),
                backstory=agent_def.get("backstory", ""),
                llm=self.llm,
                verbose=True,
            )
            crew_agents.append(agent)

        # Create tasks
        crew_tasks = []
        for task_def in tasks:
            # Find agent by role
            agent = next(
                (a for a in crew_agents if a.role == task_def.get("agent_role")),
                crew_agents[0] if crew_agents else None,
            )

            task = Task(
                description=task_def.get("description", ""),
                agent=agent,
                expected_output=task_def.get("expected_output", ""),
            )
            crew_tasks.append(task)

        # Create crew
        crew = Crew(
            agents=crew_agents,
            tasks=crew_tasks,
            verbose=True,
        )

        logger.info("CrewAI crew created successfully")
        return crew

    def execute_crew(self, crew: Crew) -> dict[str, Any]:
        """
        Execute a Crew and return results.

        Args:
            crew: Crew instance

        Returns:
            Execution results
        """
        logger.info(f"Executing CrewAI crew with {len(crew.agents)} agents")
        try:
            result = crew.kickoff()
            execution_result = {
                "status": "completed",
                "output": str(result),
                "tasks_completed": len(crew.tasks),
            }
            logger.info(f"CrewAI execution completed: {execution_result['status']}")
            return execution_result
        except Exception as e:
            logger.error(f"CrewAI execution failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
            }

    def is_available(self) -> bool:
        """Check if CrewAI adapter is available."""
        available = CREWAI_AVAILABLE and self.llm is not None
        logger.debug(f"CrewAI adapter available: {available}")
        return available


# Global instance
_crewai_adapter: CrewAIAdapter | None = None


def get_crewai_adapter(llm_model: str | None = None, api_base: str | None = None) -> CrewAIAdapter | None:
    """
    Get global CrewAI adapter instance.

    Args:
        llm_model: LLM model name (default from policy)
        api_base: API base URL (default from policy)

    Returns:
        CrewAIAdapter if available, else None
    """
    global _crewai_adapter

    if not CREWAI_AVAILABLE:
        return None

    if _crewai_adapter is None:
        try:
            _crewai_adapter = CrewAIAdapter(llm_model=llm_model, api_base=api_base)
        except Exception as e:
            logger.warning(f"Failed to initialize CrewAI adapter: {e}")
            return None

    return _crewai_adapter
