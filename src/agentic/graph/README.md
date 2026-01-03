# 🕸️ LangGraph Orchestrator

> **Zone:** The Brain / State Machine
> **Access:** Architects & Surgeons

## Workflow Overview

The system follows a cyclic graph defined in `workflow.py` (or `orchestrator_graph.py` in atomic mode).

### The Cycle
`PLAN` -> `EXECUTE` (Aider) -> `VERIFY` (Sentinel) -> `COMMIT` (Git)

## Nodes

| Node | Function |
|------|----------|
| **Planner** | Decomposes high-level goals into steps. |
| **Executor** | Uses `Aider` to generate/modify code. |
| **Verifier** | Uses `Sentinel` to run linters, tests, and security checks. |
| **Chainer** | (Optional) Spawns new tasks based on outcomes. |

## Emergent Behavior
- **Self-Healing:** If `VERIFY` fails, the graph loops back to `EXECUTE` with feedback.
- **Atomic:** Each run claims one task from SQLite.
