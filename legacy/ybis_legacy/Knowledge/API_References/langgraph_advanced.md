# LANGGRAPH ADVANCED MANUAL: PERSISTENCE & CHECKPOINTS

## 1. Core Concept: Short-term vs Long-term Memory
- **Short-term (Thread-level):** Use `InMemorySaver` or `PostgresSaver`. Tracks multi-turn conversations.
- **Long-term (Store):** Use `PostgresStore`. Tracks user-specific data across different threads.

## 2. Setting up Persistence
```python
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import StateGraph

checkpointer = PostgresSaver.from_conn_string(DB_URI)
graph = builder.compile(checkpointer=checkpointer)

# Run with thread_id
config = {"configurable": {"thread_id": "user_123"}}
graph.invoke(input, config)
```

## 3. Advanced State Management
- **Trim Messages:** Use `trim_messages` to manage context window.
- **Remove Messages:** Use `RemoveMessage` to prune the state.
- **Semantic Search:** Enable in `Store` for RAG-like retrieval of past decisions.
