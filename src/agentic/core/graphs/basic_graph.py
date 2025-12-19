from typing import TypedDict, Annotated, List
import operator
from langgraph.graph import StateGraph, START, END

# 1. Define State
class GraphState(TypedDict):
    message: Annotated[str, operator.add] # Append logic if updated

# 2. Define Nodes
def node_a(state: GraphState):
    return {"message": " Hello"} # Operator.add will append this

def node_b(state: GraphState):
    return {"message": " World"}

# 3. Build Graph
def build_basic_graph():
    builder = StateGraph(GraphState)
    builder.add_node("node_a", node_a)
    builder.add_node("node_b", node_b)
    builder.add_edge(START, "node_a")
    builder.add_edge("node_a", "node_b")
    builder.add_edge("node_b", END)
    return builder.compile()