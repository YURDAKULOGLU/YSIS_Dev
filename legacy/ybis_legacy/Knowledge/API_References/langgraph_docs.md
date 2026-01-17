# LANGGRAPH DOCUMENTATION

## 1. Core Concept
State Machine for Agents. Graph = Nodes + Edges + State.

## 2. State Definition
Use `TypedDict` or `Pydantic`.
```python
from typing import TypedDict, Annotated, List
import operator

class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add] # Append-only list
    count: int
```

## 3. Building the Graph
```python
from langgraph.graph import StateGraph, END

# Initialize
workflow = StateGraph(AgentState)

# Add Nodes (Functions that return State update)
workflow.add_node("agent", agent_node)
workflow.add_node("action", action_node)

# Set Entry
workflow.set_entry_point("agent")

# Add Edges
workflow.add_edge("action", "agent")

# Conditional Edge
def should_continue(state):
    if state["count"] > 5: return END
    return "action"

workflow.add_conditional_edges(
    "agent",
    should_continue,
    {END: END, "action": "action"}
)

# Compile
app = workflow.compile()
```

## 4. Execution
```python
inputs = {"messages": ["Hi"], "count": 0}
result = await app.ainvoke(inputs)
```
