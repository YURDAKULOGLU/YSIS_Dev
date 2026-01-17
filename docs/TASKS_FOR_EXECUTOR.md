# EXECUTOR TASK BATCH 17.5: THE SAFETY NET (SANDBOX & WORKTREE)

**Objective:** Implement strict isolation to prevent accidental corruption of the main codebase.
**Context:** Root is `src/ybis/`. Reference `docs/SANDBOX_AND_ISOLATION_STATUS.md`.

---

## TASK 17.5.1: Git Worktree Manager

**Objective:** Isolate every run in its own Git Worktree.

**Requirements:**
1.  Create `src/ybis/data_plane/git_workspace.py`:
    - Method `init_worktree(task_id: str, run_id: str) -> Path`:
        - Creates a new git branch `run/T-XXX/R-YYY`.
        - Creates a worktree at `workspaces/active/T-XXX/runs/R-YYY/code`.
    - Method `cleanup_worktree(path: Path)`.
2.  Update `src/ybis/data_plane/workspace.py`:
    - Use `git_workspace` to initialize the run folder.

**DoD:**
- Every run operates in a clean checkout of the code, not the main folder.

---

## TASK 17.5.2: Sandbox Execution Wrapper

**Objective:** Ensure commands run INSIDE the worktree, never on root.

**Requirements:**
1.  Update `src/ybis/syscalls/exec.py`:
    - Enforce `cwd` (Current Working Directory) to be the worktree path.
    - Block any command that tries to access `../` or absolute paths outside the worktree.

**DoD:**
- `run_command(["ls"], ctx)` lists files in the worktree, not the project root.

---

## TASK 17.5.3: Atomic Merge (The Commit)

**Objective:** Only apply changes to main if verification passes.

**Requirements:**
1.  Update `src/ybis/orchestrator/graph.py` -> `finalize_node`:
    - If `status == SUCCESS`:
        - Merge the worktree branch into the main branch (or create a PR).
    - If `status == FAILED`:
        - Discard the worktree (safe rollback).

**DoD:**
- Main codebase remains untouched until the very end of a successful run.
