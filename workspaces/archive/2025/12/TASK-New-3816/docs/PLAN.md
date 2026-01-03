---
id: TASK-New-3816
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-28T23:50:00
target_files:
  - src/agentic/skills/code_graph.py
  - scripts/ingest_code_graph.py
  - requirements.txt
---

# Task: Code Graph Ingestion (TASK-New-3816)

## Objective
To move beyond simple file-level dependency tracking. We need a semantic "Code Knowledge Graph" that understands Functions, Classes, and method calls. This enables the "GraphRAG" capability for semantic memory.

## Approach
We will use `tree-sitter` to parse Python code into an Abstract Syntax Tree (AST). We will then map this AST to a Neo4j schema.

## Schema Design
- **Nodes:** `Function`, `Class`, `File`, `Module`.
- **Relationships:**
  - `(Function)-[:DEFINED_IN]->(File)`
  - `(Class)-[:DEFINED_IN]->(File)`
  - `(Function)-[:CALLS]->(Function)`
  - `(Class)-[:INHERITS_FROM]->(Class)`

## Steps
1.  **Dependencies:** Install `tree-sitter` and `tree-sitter-languages` (binary wheels for Windows/Linux).
2.  **Parser:** Create `src/agentic/skills/code_graph.py` to handle AST parsing.
3.  **Ingestor:** Create `scripts/ingest_code_graph.py` to walk the `src/` directory and populate Neo4j.
4.  **Verify:** Run the script and check for errors.

## Risks & Mitigations
*   **Risk:** `tree-sitter` compilation issues on Windows.
*   **Mitigation:** Use `tree-sitter-languages` which provides pre-built binaries.
*   **Risk:** Neo4j connection failure.
*   **Mitigation:** Script will verify connection before starting.

## Acceptance Criteria
- [ ] `tree-sitter` installed and working.
- [ ] Code creates Nodes for Classes and Functions in Neo4j.
- [ ] Code creates Relationships (CALLS, DEFINED_IN).
- [ ] Script runs without crashing on the current codebase.
