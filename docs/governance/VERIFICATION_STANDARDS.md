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
 - Enforcement: Tasks modifying code must add or update at least one task-specific test.

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

---

## 4. NON-TESTABLE ARTIFACTS (NEW PRINCIPLE)

**Principle:** Test yazılamayacak şeylerin kalitesi de kontrol edilecek.

### Scope
Artifacts that cannot be tested with automated tests (e.g., documentation, configuration, design decisions) must still undergo quality verification.

### Verification Methods for Non-Testable Artifacts

#### A) Documentation Quality
- **Markdown Validation:** No malformed tables, broken links, or syntax errors
- **Completeness:** All required sections present (PLAN, RESULT, META)
- **Accuracy:** Paths, references, and examples must be valid
- **Consistency:** Terminology and formatting consistent with project standards
- **Command:** `python scripts/protocol_check.py --task-id <TASK_ID> --mode lite`

#### B) Configuration Quality
- **Syntax Validation:** YAML/JSON/TOML files must be valid
- **Schema Compliance:** Configuration must match expected schema
- **Dependency Check:** All referenced dependencies exist
- **Command:** `python -m json.tool <config.json>` or `yamllint <config.yaml>`

#### C) Design Decision Quality
- **Documentation:** Design decisions must be documented in RESULT.md
- **Rationale:** Clear explanation of why this approach was chosen
- **Alternatives:** Document considered alternatives and why they were rejected
- **Impact Analysis:** Document potential impact on other components

#### D) Manual Verification Checklist
For artifacts that cannot be automatically tested:
1. **Completeness Check:** All required information present?
2. **Accuracy Check:** All facts, paths, and references correct?
3. **Consistency Check:** Aligns with existing patterns and standards?
4. **Clarity Check:** Clear and understandable?
5. **Impact Check:** Potential side effects documented?

### Enforcement
- **Mandatory:** All non-testable artifacts must pass manual verification checklist
- **Documentation:** Verification results must be recorded in RESULT.md
- **Gate:** Task cannot be completed without quality verification for non-testable artifacts

### Examples

**Documentation Task:**
- ✅ Markdown syntax valid
- ✅ All links work
- ✅ Examples are accurate
- ✅ Terminology consistent
- ✅ Manual review completed

**Configuration Task:**
- ✅ YAML/JSON syntax valid
- ✅ Schema matches expected format
- ✅ All dependencies exist
- ✅ No deprecated options used
- ✅ Manual review completed

**Design Decision Task:**
- ✅ Decision documented
- ✅ Rationale clear
- ✅ Alternatives considered
- ✅ Impact analyzed
- ✅ Manual review completed