# LangGraph API Reference (Quick Reference)

## StateGraph

### Basic Usage
```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class MyState(TypedDict):
    field1: str
    field2: int

builder = StateGraph(MyState)
```

### Adding Nodes
```python
# Node functions receive state, return dict of updates
async def my_node(state: MyState) -> dict:
    return {"field1": "updated", "field2": state["field2"] + 1}

builder.add_node("node_name", my_node)
```

### Adding Edges

**Simple edges:**
```python
builder.add_edge(START, "first_node")
builder.add_edge("node_a", "node_b")
builder.add_edge("last_node", END)
```

**Conditional edges:**
```python
def routing_function(state: MyState) -> str:
    # Return string key for routing
    if state["field2"] > 10:
        return "path_a"
    else:
        return "path_b"

builder.add_conditional_edges(
    "source_node",
    routing_function,
    {
        "path_a": "target_node_a",
        "path_b": "target_node_b",
        "done": END
    }
)
```

## CRITICAL: Common Mistakes

### ❌ WRONG
```python
# Do NOT use add_edge with condition parameter (doesn't exist!)
builder.add_edge("verifier", END, condition=my_function)
```

### ✅ CORRECT
```python
# Use add_conditional_edges instead
builder.add_conditional_edges(
    "verifier",
    my_routing_function,
    {
        "success": END,
        "retry": "executor"
    }
)
```

## State Updates

Node functions return dictionaries. LangGraph merges these into state:

```python
# State before: {"field1": "old", "field2": 5}

async def node(state):
    return {"field2": 10}  # Only update field2

# State after: {"field1": "old", "field2": 10}
```

## Compiling

```python
graph = builder.compile()

# Invoke
result = await graph.ainvoke(initial_state)
```

## Complete Example

```python
from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class TaskState(TypedDict):
    task: str
    result: str
    retry_count: int

async def process(state: TaskState) -> dict:
    return {"result": f"Processed: {state['task']}"}

async def check(state: TaskState) -> dict:
    return {"retry_count": state["retry_count"] + 1}

def should_retry(state: TaskState) -> str:
    if state["retry_count"] >= 3:
        return "done"
    if state["result"]:
        return "done"
    return "retry"

builder = StateGraph(TaskState)
builder.add_node("process", process)
builder.add_node("check", check)

builder.add_edge(START, "process")
builder.add_edge("process", "check")

builder.add_conditional_edges(
    "check",
    should_retry,
    {
        "retry": "process",
        "done": END
    }
)

graph = builder.compile()

result = await graph.ainvoke({
    "task": "example",
    "result": "",
    "retry_count": 0
})
```
