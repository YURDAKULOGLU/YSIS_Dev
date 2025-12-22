"""
YBIS FACTORY BRAIN (LangGraph)
A cyclic, self-correcting state machine powered by RTX 5090.
"""

from langgraph.graph import StateGraph, END
from .state import FactoryState
from .nodes.planner import planner_node
from .nodes.executor import executor_node
from .nodes.reviewer import reviewer_node
from .nodes.memory_manager import memory_read_node, memory_write_node

# --- GRAPH CONSTRUCTION ---
workflow = StateGraph(FactoryState)

# 1. Add Nodes (The Assembly Line)
workflow.add_node("memory_read", memory_read_node)   # Recall past mistakes/successes
workflow.add_node("planner", planner_node)           # Architect
workflow.add_node("executor", executor_node)         # Worker (Aider)
workflow.add_node("reviewer", reviewer_node)         # QA / Sentinel
workflow.add_node("memory_write", memory_write_node) # Learn

# 2. Define Flow (The Process)
workflow.set_entry_point("memory_read")

workflow.add_edge("memory_read", "planner")
workflow.add_edge("planner", "executor")
workflow.add_edge("executor", "reviewer")

# 3. Conditional Logic (The Feedback Loop)
def review_gate(state: FactoryState):
    if state["status"] == "APPROVED":
        return "memory_write"
    elif state["retry_count"] > 3:
        return "memory_write" # Fail but remember
    else:
        return "executor" # Go back and fix code

workflow.add_conditional_edges(
    "reviewer",
    review_gate,
    {
        "memory_write": "memory_write",
        "executor": "executor"
    }
)

workflow.add_edge("memory_write", END)

app = workflow.compile()