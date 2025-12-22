"""
YBIS Factory Graph (LangGraph)
The State Machine of the Autonomous Factory.

Flow:
[Task] -> Planner -> [Plan] -> Executor(Aider) -> [Code] -> Verifier -> [Pass/Fail]
   ^
   |
   -----------------------(Retry with Feedback)---------------------------
"""

import operator
from typing import Annotated, List, TypedDict, Union, Optional
from langgraph.graph import StateGraph, END

# --- STATE DEFINITION ---
class AgentState(TypedDict):
    task: str
    plan: str
    files_to_edit: List[str]
    error_history: Annotated[List[str], operator.add]
    retry_count: int
    status: str # "PLANNING", "EXECUTING", "VERIFYING", "DONE", "FAILED"
    artifacts_path: str

# --- NODES (The Workers) ---

def planner_node(state: AgentState):
    """
    Analyzes the task and creates a plan.
    Uses PydanticAI / Local LLM (Ollama) logic here.
    """
    print(f"\n[PLANNER] Analyzing: {state['task']}")
    
    # MOCK FOR NOW - We will hook real Ollama here next
    plan_text = "1. Create hello_factory.py\n2. Add greet function\n3. Add main block"
    files = ["src/utils/hello_factory.py"]
    
    return {
        "plan": plan_text, 
        "files_to_edit": files,
        "status": "EXECUTING"
    }

def executor_node(state: AgentState):
    """
    Executes the plan using Aider.
    """
    print(f"\n[EXECUTOR] Coding... (Attempt {state.get('retry_count', 0) + 1})")
    print(f"Target Files: {state['files_to_edit']}")
    
    # MOCK FOR NOW - We will hook real Aider here next
    # Simulating a successful run
    return {
        "status": "VERIFYING"
    }

def verifier_node(state: AgentState):
    """
    Checks the work (Sentinel Logic).
    """
    print(f"\n[VERIFIER] Checking code quality...")
    
    # MOCK Sentinel Logic
    # If retry_count > 2, fail. Else pass.
    
    return {
        "status": "DONE"
    }

# --- GRAPH CONSTRUCTION ---

workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("planner", planner_node)
workflow.add_node("executor", executor_node)
workflow.add_node("verifier", verifier_node)

# Add Edges
workflow.set_entry_point("planner")
workflow.add_edge("planner", "executor")
workflow.add_edge("executor", "verifier")
workflow.add_edge("verifier", END) # Simple flow for smoke test

# Compile
app = workflow.compile()
