# 📚 YBIS INFORMATION HIERARCHY (The 5-Tier System)

> **Status:** Active Governance
> **Authority:** 10_META/Governance
> **Purpose:** Defines the "Source of Truth" hierarchy. Information flows strictly from Tier -1 to Tier 3.

---

## [*] TIER -1: STRATEGIC LAYER (The "Why")
*The guiding stars. Changes here ripple through the entire system.*

*   **Scope:** Product Vision, Business Goals, Market Strategy.
*   **Key Docs:**
    *   `10_META/Strategy/PRODUCT_ROADMAP.md`
    *   `10_META/Strategy/MARKET_RESEARCH.md`
*   **Change Protocol:** Requires Chairman (Human) approval.

---

## 🔥 TIER 0: CANONICAL SOURCES (The "Law")
*The Single Source of Truth (SSOT). If code contradicts Tier 0, code is wrong.*

*   **Scope:** Constitution, Core Protocols, System Architecture.
*   **Key Docs:**
    *   `00_GENESIS/YBIS_CONSTITUTION.md`
    *   `00_GENESIS/ONBOARDING.md`
    *   `10_META/Governance/*.md`
*   **Change Protocol:** High-Level "Strategist" Agent only.

---

## 📚 TIER 1: REFERENCE BLUEPRINTS (The "What")
*Derived from Tier 0. Read-Only for developers during execution.*

*   **Scope:** Technical Specifications, Port Definitions, Tech Stack choices.
*   **Key Docs:**
    *   `docs/Architecture.md` (Project Level)
    *   `docs/PRODUCT_REQUIREMENTS.md` (Project Level)
    *   `40_KNOWLEDGE_BASE/Templates/*.md`
*   **Rule:** "Think Twice, Code Once." You must read these before writing code.

---

## ⚙️ TIER 2: EXECUTION ARTIFACTS (The "How")
*Dynamic documents that track progress.*

*   **Scope:** Tasks, Epics, Stories, Spec Files (Specific Feature Specs).
*   **Key Docs:**
    *   `docs/specs/*.md`
    *   `docs/Güncel/tasks.md`
*   **Lifecycle:** Created -> Active -> Completed -> Archived.

---

## 📖 TIER 3: SUPPORT & LOGS (The "Memory")
*Auto-generated or retrospective data.*

*   **Scope:** Audit logs, Error logs, Meeting notes, "Memory" dumps.
*   **Key Docs:**
    *   `40_KNOWLEDGE_BASE/Memory/LEARNINGS.md`
    *   `40_KNOWLEDGE_BASE/Memory/logs/*.log`

---

## 🔗 The Dependency Chain
`TIER -1` -> `TIER 0` -> `TIER 1` -> `TIER 2` -> `Code`

*   **Violation:** Writing code based on Tier 2 without checking Tier 1 is a violation.
*   **Enforcement:** `verify-doc-integrity.py` checks these links.
