from typing import Protocol, Any, Dict

class AgentFrameworkBridge(Protocol):
    """
    Universal interface for any agent framework (CrewAI, AutoGen, LangGraph).
    Allows the Orchestrator to delegate sub-tasks to entire specialized teams.
    """
    
    async def run_mission(self, mission_goal: str, context: Dict[str, Any]) -> str:
        """Run a mission using the specific framework's agents."""
        ...
        
    def get_capabilities(self) -> list[str]:
        """Return what this squad is good at (e.g., 'research', 'coding')."""
        ...
