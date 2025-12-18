# ⚙️ ARTICLE 3: OPERATIONAL PROTOCOLS

## 3.1 The Development Lifecycle

1.  **Drafting (Meta-Layer):**
    *   Strategist receives request.
    *   Updates `docs/PRODUCT_REQUIREMENTS.md`.
    *   Creates/Updates `docs/Architecture.md`.
    *   **Auditor Check:** `verify-doc-integrity.py` runs.

2.  **Specification (Knowledge-Layer):**
    *   Strategist generates a Spec file in `.YBIS_Dev/40_KNOWLEDGE_BASE/Specs_Draft/`.
    *   Chairman approves the Spec.

3.  **Execution (Workforce-Layer):**
    *   Strategist assigns the Spec to a Worker (e.g., "CrewAI, implement Spec #004").
    *   Worker reads the Spec from `40_KNOWLEDGE_BASE`.
    *   Worker writes code to `C:\Projeler\YBIS\apps\...`.

4.  **Verification (Quality Control):**
    *   Tests are run.
    *   If successful, Spec is moved to `99_ARCHIVE` or marked "Done".

## 3.2 The "Definition of Done"
A task is NOT done when the code is written. It is done when:
1.  The Code exists.
2.  The Code matches the Spec.
3.  The Spec matches the Architecture.
4.  The Auditor (`verify-doc-integrity.py`) passes with `exit code 0`.
5.  **The Code is rigorously tested.** This includes writing new, comprehensive test files (`*.test.ts`, `*_test.py` etc.) as required, and ensuring all relevant tests pass successfully.
