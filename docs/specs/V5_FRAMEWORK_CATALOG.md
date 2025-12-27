
# YBIS V5: The Ultimate Framework Catalog (Frankenstein's Menu)

**Author:** Gemini-CLI (The Architect)
**Status:** REFERENCE
**Date:** 2025-12-28

## 1. THE BRAIN (Orchestration & Council)
*   **LangGraph (Current):** Best for stateful, cyclic workflows. The Core.
*   **AutoGen (Candidate):** Best for conversational multi-agent debate. Use for "The Council".
*   **MetaGPT (Candidate):** Generates full PRDs from one line. Use for "Architect Mode".

## 2. THE HANDS (Coding & Engineering)
*   **Aider (Current):** Best for chat-based file editing. The Editor.
*   **OpenDevin (Candidate):** Autonomous engineer in a sandbox. The Builder.
*   **SWE-agent (Candidate):** GitHub issue solver. The Maintainer.

## 3. THE MEMORY (Semantic & Persistent)
*   **ChromaDB (Local):** Vector store for RAG.
*   **LlamaIndex:** Data connector.
*   **MemGPT (Priority):** "Infinite Memory" OS for agents. Allows recalling past mistakes across sessions.

## 4. THE ENGINE (Local Inference)
*   **Ollama (Current):** Easy, API-compatible. Development standard.
*   **vLLM (Future):** High-throughput production engine (requires GPU).
*   **Llama.cpp:** Low-level python bindings for CPU inference.

## 5. THE BODY (OS Control)
*   **Open Interpreter (Priority):** Allows agents to run terminal commands, install apps, and control the OS naturally.

---

## IMPLEMENTATION STRATEGY (The Stitching)

We do not replace; we integrate.

1.  **Phase 1 (Memory):** Integrate `MemGPT` core into `mcp_server.py`.
2.  **Phase 2 (OS):** Add `Open Interpreter` as a specialized MCP Tool (`execute_os_command`).
3.  **Phase 3 (Council):** Use `AutoGen` to simulate debates in RAM before committing to `tasks.db`.
