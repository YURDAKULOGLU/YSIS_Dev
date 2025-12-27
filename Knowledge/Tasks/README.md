# Task Management

File-based task queue for agent coordination.

## Structure

- `backlog/` - Unclaimed tasks waiting to be picked up
- `in_progress/` - Tasks currently being worked on
- `done/` - Completed tasks with artifacts
- `blocked/` - Tasks that cannot proceed (missing info/dependencies)

## Task File Format

Each task is a markdown file: `T-XXX_P[0-2]_Short_Title.md`

**Required sections:**
- Task ID
- Priority (P0=critical, P1=high, P2=normal)
- Suggested agent roles
- Scope (files/directories that can be modified)
- Acceptance criteria

**Example:**
```markdown
# T-100 (P0) Fix calculator add method

Suggested agents: codex, claude
Priority: P0
Mode: terminal

Scope: src/utils/calculator.py, tests/test_calculator.py

## Problem
Calculator.add() returns a-b instead of a+b

## Requirements
- Fix the add method
- Ensure tests pass

## Acceptance
- All calculator tests pass
- No regressions in other methods
```

## Workflow

1. Agent picks task from `backlog/`
2. Moves to `in_progress/` (claims it)
3. Executes work, generates artifacts in `.sandbox_hybrid/<TASK_ID>/`
4. Runs verification (tests, lint, etc.)
5. Moves to `done/` (or `blocked/` if stuck)

## Integration with tasks.db

This file-based queue complements `Knowledge/LocalDB/tasks.db` (operational memory).

- `tasks.db` - Lightweight queue for OrchestratorGraph
- `Tasks/*.md` - Detailed task specifications for manual agents

Both systems can coexist. File-based tasks provide more context for human/manual agents.
