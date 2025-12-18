# 🧠 YBIS KERNEL: LEARNINGS & PRINCIPLES

> **Status:** Active Memory
> **Purpose:** To prevent repeating mistakes and to codify success patterns.

---

## 🟢 CODIFIED PRINCIPLES (Immutable Truths)
*Verified patterns that must be applied to all future tasks.*

### [PRIN-001] The Iron Chain Rule
*   **Discovery:** Initial chaos in docs vs code.
*   **Rule:** Documentation dictates Code. Never the reverse. Automation (`verify-doc-integrity.py`) is required to enforce this.
*   **Applied:** 16.12.2025

### [PRIN-002] Modular Governance
*   **Discovery:** Single "README" files become unreadable monoliths.
*   **Rule:** Split governance into atomic "Articles" (Principles, Roles, Protocols) linked by a Constitution.
*   **Applied:** 16.12.2025

---

## 🟡 ACTIVE LESSONS (Under Observation)
*Patterns we are currently testing or refining.*

### [LESSON-001] Docker Environment Configuration
*   **Observation:** `pip install` in Docker without explicit `.venv` activation or `uv` usage can lead to package lookup issues.
*   **Action:** Ensure all package installations are done via `uv pip install` within the designated virtual environment (`/app/.venv`) in `Dockerfile`, and scripts are executed using `/app/.venv/bin/python`.

### [LESSON-002] AutoGen Versioning & Import
*   **Observation:** `pyautogen` (v0.10.0) package does not export the `autogen` module directly (`import autogen` fails).
*   **Rule:** Use `from autogen_agentchat.agents import ...` for core agent components. `pyautogen` acts as a proxy/meta-package.
*   **Applied:** 16.12.2025

### [LESSON-003] Ollama API Error 400 Debugging
*   **Observation:** `Ollama API Error: 400` can be caused by incorrect model names or sending `tools` param to models/versions that don't support it or are not expecting it for simple text completions. Also, command-line argument parsing (like `--once` interfering with `DEFAULT_MODEL`) can cause `model is required` errors.
*   **Rule:**
    1.  Explicitly pass model name (e.g., ` --model codellama:latest`).
    2.  Conditionally send `tools` to Ollama based on task requirement.
    3.  Rigorously parse command-line arguments.
*   **Applied:** 16.12.2025

### [LESSON-004] Build vs. Buy Decision & Hybrid Strategy (YBIS Dev Philosophy)
*   **Discovery:** Comparison of YBIS's custom system with existing AI agent frameworks like MetaGPT, OpenDevin, and AutoGen revealed that no single framework fully supports YBIS's unique combination of local-first operation, strict governance ("Iron Chain" for documentation integrity), and project-agnostic meta-management.
*   **Rule:** Adopt a hybrid strategy:
    1.  **"Build the Company Structure":** Maintain YBIS Dev's custom governance, orchestration, and file-system-based communication (`Inbox/Outbox`). This is our unique "Operating System."
    2.  **"Buy/Integrate the Best Workers":** Integrate best-of-breed frameworks (like AutoGen for multi-agent chat, or OpenDevin's sandbox capabilities) as specialized "Workforce" departments within `20_WORKFORCE`.
*   **Rationale:** YBIS's core value lies in its **Constitution-driven, deterministic, and auditable development process**, which existing frameworks lack. We build our own "Brain" (Meta-Layer) but use powerful "Hands" (Workforce frameworks).
*   **Applied:** 16.12.2025

---

## 🔴 ANTI-PATTERNS (Never Do This)
*Mistakes we have made and vowed never to repeat.*

*   **[ANTI-001]**: Mixing "Project Docs" with "System Docs". (Led to the `docs/` vs `.YBIS_Dev/` separation strategy).
*   **[ANTI-002]**: Manually running scripts without an Auditor check first.

---

## 📝 JOURNAL (Recent Insights)
*   **2025-12-16:** "Dog Scales Dog" metaphor established. The `.YBIS_Dev` folder is now the Headquarters, separated from the Project Product.
