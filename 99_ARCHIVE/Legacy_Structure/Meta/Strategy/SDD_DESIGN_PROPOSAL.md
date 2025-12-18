# design: YBIS Spec-Driven Development (SDD) Protocol

**Status:** PROPOSAL
**Inspiration:** Bmad Framework, GitHub Spec Kit, Kiro.dev
**Target:** Phase 2 (Deterministic Hardening)

## 1. Core Philosophy: "Code is the Last Step"
Current YBIS agents jump to code too quickly ("Vibe Coding"). The new protocol enforces a strict chain of custody for requirements.

**The "Vibe" vs. "Spec" Shift:**
- **Old:** User Prompt -> Planner -> Coder -> Code
- **New:** User Prompt -> **Spec** -> **Plan** -> **Stories** -> Coder -> Code

## 2. The Native Bmad Architecture (Verified)

We will leverage the existing **Multi-Agent / File-Centric** tools found in `.YBIS_Dev/Veriler`.

### Phase 1: Specification (The PM Agent)
*   **Command:** `/create-doc` (wraps `Veriler/commands/create-doc.md`)
*   **Template:** `Veriler/templates/prd-tmpl.yaml` (Needs Restoration)
*   **Output:** `docs/prd.md` (Canonical Location)
    *   *Constraint:* Uses Bmad's interactive elicitation protocol.

### Phase 2: Sharding (The Architect Agent)
*   **Command:** `/shard-doc` (wraps `Veriler/commands/shard-doc.md`)
*   **Action:** Splits `docs/prd.md` into `docs/prd/*.md`.
*   **Tool:** `md-tree` (Auto-sharding) or Agentic Fallback.

### Phase 3: Execution (The Developer Agent)
*   **Command:** `/implement` or `/feature-implement`
*   **Input:** Single `docs/prd/story-name.md`
*   **Constraint:** The Coder is **FORBIDDEN** from inventing new requirements.
*   **Output:** Code Changes + Test Results.

## 3. Implementation Plan for YBIS

1.  **Restore Templates:**
    - The `Veriler/templates` directory is missing. We must recreate `prd-tmpl.yaml` and `story-tmpl.yaml` based on `bmad-doc-template.md`.
2.  **Activate Commands:**
    - Ensure `/create-doc` and `/shard-doc` are registered in the Orchestrator.
3.  **Golden Rails:**
    - Update `Veriler/checklists/story-dod-checklist.md` to enforce strict spec compliance.

## 4. Comparison to Alternatives

| Feature | YBIS SDD (Native) | Previous Proposal |
| :--- | :--- | :--- |
| **Orchestrator** | Bmad Command System | Custom Scripts |
| **Context** | `docs/` (Canonical) | `specs/` (Parallel) |
| **Sharding** | `md-tree` + `shard-doc.md` | New Splitter |
| **Execution** | `/implement` | Custom Worker |

## 5. Next Steps
1.  Approve this "Native" Design.
2.  **Action:** Create `.YBIS_Dev/Veriler/templates/prd-tmpl.yaml`.
3.  **Action:** Create `.YBIS_Dev/Veriler/templates/story-tmpl.yaml`.
4.  **Action:** Test `/create-doc` flow.
