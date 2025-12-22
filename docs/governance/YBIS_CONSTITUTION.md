# YBIS CONSTITUTION (The Supreme Law)

> **Status:** Active & Enforced
> **Mission:** Autonomous, Self-Improving Software Factory

## 1. PATH INTEGRITY
- **Absolute Rule:** NEVER hardcode paths like `C:\Users`. Always use `PROJECT_ROOT` from config.
- **Isolation:** Agents MUST only write to `.sandbox_worker` or designated `src/` files.
- **Legacy:** `legacy/` directory is READ-ONLY. Do not write there.

## 2. ARTIFACTS & EVIDENCE
- **No Ghost Work:** Every task MUST produce `PLAN.md` and `RUNBOOK.md`.
- **Proof:** "Done" means verified by Sentinel.

## 3. FRAMEWORK PROTOCOL (RTFM)
- **Read First:** Before using any external library (Mem0, CrewAI, LangGraph, MCP), agents MUST read the corresponding guide in `Knowledge/API_References/`.
- **Config:** Use standardized configuration bridges (`src/agentic/bridges/`). Do not instantiate raw clients with hardcoded API keys.
- **Local First:** Always prefer Local LLM (Ollama) and Local Vector Store (Chroma). Cloud is a fallback.

## 4. EXECUTION FLOW
- **State Machine:** All complex logic MUST be managed by LangGraph (`src/agentic/graph`).
- **Loop Prevention:** Max retries = 3. After that, mark as FAILED.
- **Code Quality:** Sentinel Verification is mandatory before commit.

## 5. SELF-CORRECTION
- **Feedback:** If a step fails, the next attempt MUST explicitly address the previous error.
- **Memory:** Use Mem0 to store decisions and lessons learned.
