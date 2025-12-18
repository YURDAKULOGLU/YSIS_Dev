from typing import TypedDict, Annotated, List, Dict, Any, Union
import operator
from src.agentic.core.protocols import Plan, CodeResult

class AgentState(TypedDict):
    """
    Unified State for the YBIS Tier 4 Orchestrator.
    Holds all context, plan, and execution results for a single task flow.
    """
    task: Union[str, None]
    task_data: Union[Dict, None]
    plan: Union[Plan, None]
    code_result: Union[CodeResult, None]
    verification: Union[Dict, None]
    retry_count: int
    history: Annotated[List[str], operator.add]
