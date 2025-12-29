---
id: TASK-New-814
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-29T01:10:00
target_files:
  - src/agentic/core/memory/manager.py
  - src/agentic/core/memory/cognee_provider.py
  - requirements.txt
---

# Task: Persistent Context Bridge (TASK-New-814)

## Objective
To implement a "MemGPT-style" hierarchical memory system. It will manage:
1. **Core Context:** (In-RAM) Current task specifics.
2. **Episodic Memory:** (Vector) Past actions and logs.
3. **Semantic Memory:** (Graph - Cognee) System-wide knowledge and code relationships.

## Approach
We will use **Cognee** as the underlying engine to link vector embeddings with Neo4j graph relationships. The `MemoryManager` will act as the unified interface for agents.

## Steps
1.  **Dependencies:** Ensure `cognee` is installed.
2.  **Cognee Provider:** Implement `cognee_provider.py` to handle extraction and search.
3.  **Memory Manager:** Create `manager.py` to coordinate between providers.
4.  **Verify:** Run a search and ingestion test.

## Acceptance Criteria
- [ ] `MemoryManager` can ingest a document.
- [ ] `MemoryManager` can retrieve context based on a query.
- [ ] Integrates with existing Neo4j instance.
- [ ] All mandatory artifacts produced.