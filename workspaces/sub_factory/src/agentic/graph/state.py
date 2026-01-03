from typing import Annotated, List, TypedDict, Dict, Any
import operator

class FactoryState(TypedDict):
    task_id: str
    goal: str
    plan: str
    files: List[str]
    # 'add' allows appending logs/history
    history: Annotated[List[str], operator.add]
    status: str # START, PLANNING, CODING, REVIEWING, FIXING, DONE, FAILED
    retry_count: int
    feedback: str # Reviewer's feedback for the Coder
    memory_context: List[str] # Retrieved memories
