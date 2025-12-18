from typing import TypedDict, Annotated, List, Dict, Any, Literal
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    """
    The unified state object for the YBIS Agentic System.
    This state is passed between nodes in the LangGraph.
    """
    # Core Task Info
    task: str
    task_id: str
    user_id: str
    
    # Workflow Status
    current_phase: str  # e.g., "analyze", "plan", "implement"
    status: Literal["idle", "running", "waiting_for_input", "completed", "failed"]
    
    # Chat History (LangChain format)
    messages: Annotated[List[Any], add_messages]
    
    # Context & Memory
    files_context: List[str]  # List of file paths relevant to the task
    decisions: List[str]      # Log of decisions made
    artifacts: Dict[str, Any] # Generated outputs (code, specs, plans)
    
    # Errors & Retries
    error: str | None
    retry_count: int
