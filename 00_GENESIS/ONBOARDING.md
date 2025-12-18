# 🔰 YBIS Agent Onboarding Protocol (v1.0)

> **⚠️ STOP & READ:** This is the entry point for ALL agents (Human & AI).
> Do not proceed to execute tasks until you have assimilated this protocol.

## 1. 🆔 Who Are You? (Identity Handshake)

Before executing any task, identify your role and scope within YBIS:

| Role | Scope | Primary Directive | Access Level |
|------|-------|-------------------|--------------|
| **Strategist (Orchestrator)** | System-Wide | Plan, Delegate, Audit. Do not implement code directly. | Read/Write (Meta) |
| **Architect** | `docs/` | Define "HOW". Convert PRD to Specs. | Read/Write (Docs) |
| **Developer** | `apps/`, `packages/` | Implement Specs. **NEVER** invent logic not in Spec. | Read/Write (Code) |
| **Auditor (QA)** | System-Wide | Verify integrity. Run `verify-doc-chain`. | Read Only |

---

## 2. 🔗 The "Iron Chain" of Truth (Dependency System)

YBIS uses a strict **Deterministic Document Dependency** system. Information flows downstream only.

**The Flow:**
1.  `PRODUCT_REQUIREMENTS.md` (The Source)
    ↓ *depends on*
2.  `ARCHITECTURE.md`
    ↓ *depends on*
3.  `specs/*.md` (Feature Specs)
    ↓ *depends on*
4.  `Code` (Implementation)

> **⛔ FATAL RULE:** If a document higher in the chain is modified (hash changed), all downstream artifacts are immediately considered **INVALID (Broken)**. You MUST update the downstream document to match the new version before writing any code.

### 🛠️ Action: Verify Integrity Now
Run this command immediately to check if the chain is intact:
```bash
python .YBIS_Dev/Meta/System/Automation/verify-doc-integrity.py
```
*If this command fails, you are NOT AUTHORIZED to write code. Fix the documentation gap first.*

---

## 3. 🗺️ Navigation Router

Where should you go next?

- **If you are here to fix a bug:**
  - Go to `docs/logs/` to see recent errors.
  - Check `specs/` related to the bug.

- **If you are here to add a feature:**
  - Check `docs/Güncel/tasks.md` for the roadmap.
  - Run `.YBIS_Dev/Veriler/scripts/create-new-feature.ps1` to start the spec process.

- **If you are "The Dog" (System Maintenance):**
  - Monitor `.YBIS_Dev/Meta/Bridges/`.

---

## 4. 🧠 Context Loading
Do not hallucinate project structure.
- **Project Root:** `C:\Projeler\YBIS`
- **Agent Brain:** `.YBIS_Dev/Agentic`
- **System Bridge:** `.YBIS_Dev/Meta/Bridges`

**Status:** WAITING FOR HANDSHAKE.
