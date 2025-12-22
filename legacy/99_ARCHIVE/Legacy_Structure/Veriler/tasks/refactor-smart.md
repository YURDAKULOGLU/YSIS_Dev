# Smart Refactor Task
**Type:** Implementation
**Required Agent:** Developer (Tier 2) + QA
**Context:** Tier 2 Execution

## Objective
Refactor a specific module or file to improve maintainability, reduce complexity, or fix technical debt, WITHOUT changing external behavior.

## Workflow Steps
1.  **Analyze:** Read the target file and its tests. Calculate Cyclomatic Complexity (if possible).
2.  **Safety Check:** Run existing tests. IF FAIL -> STOP. Refactoring requires passing tests first.
3.  **Plan:** Identify code smells (long functions, duplicated logic, magic numbers).
4.  **Execute (Sandbox):**
    *   Apply refactoring patterns (Extract Method, Rename Variable, etc.).
    *   Keep changes atomic.
5.  **Verify:** Run tests again in Sandbox.
6.  **Review:** Compare complexity before/after.

## Inputs
- `target_file`: Path to the file to refactor.
- `focus_area`: (Optional) Specific concern (e.g., "performance", "readability").

## Success Criteria
- [ ] Tests pass (100%).
- [ ] Code is cleaner (subjective check by QA).
- [ ] No behavioral changes.
