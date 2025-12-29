# YBIS Verification Standards

> Standard v1.1
> Fail any of these mandatory criteria = Task Rejection.

---

## 1. CODE TASKS
For any task modifying src/ or scripts/:

### A) Compilation Gate (Mandatory)
- Code must be valid Python (No syntax errors).
- Command: python -m py_compile <changed_files>

### B) Testing Gate (Mandatory)
- Unit Tests: At least one new unit test for new logic.
- Regression: Existing core tests must pass.
- Command: pytest tests/unit/

### C) Linting Gate (Recommended)
- Ruff: Code should pass ruff check if ruff is installed.
- Command: ruff check .

### D) Architectural Gate (Mandatory)
- Enforcer: Must pass scripts/enforce_architecture.py.

---

## 2. DOCUMENTATION TASKS
For any task modifying docs/ or README:
- Markdown Consistency: No malformed tables.
- Accuracy: Paths must exist in the current repo version.
- Frontmatter: Mandatory for PLAN/RESULT files.
- Token Budget: PLAN/RESULT frontmatter includes token_budget.

---

## 3. HIGH-SECURITY (Level 3) TASKS
- AST Analysis: Manual scan for forbidden patterns (exec, eval).
- Architect Review: Human must acknowledge EVIDENCE/summary.md.
