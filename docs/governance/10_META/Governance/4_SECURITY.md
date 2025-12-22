# 🛡️ ARTICLE 4: SECURITY & BOUNDARIES

## 4.1 File System Boundaries
*   **The Sanctuary:** Agents may READ/WRITE freely within `.YBIS_Dev`.
*   **The Product:** Agents may WRITE to `apps/`, `packages/`, `docs/` ONLY when assigned a specific task.
*   **The Forbidden Zone:** Agents must NEVER modify:
    *   `.git/` folder.
    *   System files outside of `C:\Projeler\YBIS`.
    *   User's personal directories.

## 4.2 State Integrity
*   **No Hidden State:** All agent memory must be persisted in `40_KNOWLEDGE_BASE/Memory` (ChromaDB/Redis/JSON).
*   **No Secret Keys:** API Keys (OpenAI, Supabase) must be read from Environment Variables (`.env`). NEVER hardcode secrets.

## 4.3 Quality Assurance Mandate
*   **Testing is Non-Negotiable:** All new or modified code must be accompanied by comprehensive tests. No code shall be deployed without passing its designated test suite.
*   **Regression Prevention:** Tests serve as a critical safety net. Agents are mandated to update or create tests to cover all new functionality and bug fixes, preventing future regressions.

## 4.4 Human Override
*   **Kill Switch:** The Chairman can terminate any agent process (Docker or CLI) at any time.
*   **Manual Override:** If an agent gets stuck, the Chairman can edit the file manually. The agent must respect the human edit as the new "Ground Truth".
