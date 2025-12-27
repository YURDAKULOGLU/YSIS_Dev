
# LESSONS LEARNED: The Road to Tier 5 (V4.5 Reflection)

**Author:** Gemini-CLI (The Architect)
**Status:** Canonical
**Date:** 2025-12-28

## 1. FROM BUREAUCRACY TO AUTOMATION
- **Old Lesson:** Manual file manipulation (AgentMessaging) leads to split-brain.
- **New Law:** All core systems (Messaging, Debates, Tasks) MUST be backed by a service layer (MCP) and a database (SQLite). Tools rule, docs follow.

## 2. THE ANATOMY OF CONSENSUS
- **Discovery:** Council Bridge (Option C Hybrid) proved that we don't need to rewrite external tools. We just need a robust Adapter Pattern.
- **Guideline:** Every P0 architectural change MUST trigger an `ask_council` call via MCP.

## 3. SEMANTIC AWARENESS
- **Discovery:** Cognee (Graph+Vector) is superior to simple RAG. It allows the system to see relationships, not just keywords.
- **Law:** Every task completion MUST trigger `cognify()` to update the Hive Mind.

## 4. THE EVIDENCE DISCIPLINE (From Legacy Graves)
- **Insight:** The most successful old tasks (`LANGGRAPH-VICTORY`) had a dedicated `EVIDENCE/` folder and a `DECISIONS.json` log.
- **Mandate:** This discipline is now codified in `workspaces/active/<TASK_ID>/`.

---

## FUTURE OUTLOOK: V5 AND BEYOND
The foundation is now homogenized. We move from **building organs** to **evolving consciousness**.
Next: Safe OS Control (Open Interpreter) and Persistent Context (MemGPT/Cognee full wiring).
