# REALITY (The Governance of Truth)

**Rule #1:** Code > Documentation.
**Rule #2:** If the Script fails, the Feature waits.

---

## 🛡️ Protocol 1: Monorepo Native Safety
**Trigger:** Before any native build or adding a new native library.
**Action:** Run the Guard Script.

```bash
node Meta/System/Automation/check-native-deps.js
```

**Why?**
In a Monorepo, `expo install` sometimes fails to verify peer dependencies. The script scans source code for imports and ensures they exist in `package.json`.
**Penalty:** If skipped, the build *will* fail on Windows/Android.

---

## 🧬 Protocol 2: The "Codex" Reality Check
(Derived from `DEVELOPER_FEEDBACK.md` - 2025-11-27)

### The Vision-Reality Gap
*   **Vision:** 10/10 (Perfect Architecture)
*   **Reality:** 5/10 (Missing Tests, Ghost Deps)

### The Mandates
1.  **Zero Tolerance means Zero Tolerance.**
    *   No more `console.error` (Use Logger).
    *   No more Wildcard Exports (`index.ts`).
2.  **Test Coverage Floor.**
    *   Do not ship "Blind Code".
    *   Write Integration Tests for Supabase adapters.
3.  **Scope Discipline.**
    *   Focus: Mobile App + Backend.
    *   Deferred: Web App, Complex Integrations.

---

## 🤖 System Status (Active)
*   **@Auditor (Codex):** ENFORCING this document.
*   **@Builder (Claude):** MUST read this before coding.
