# GEMINI & SYSTEM LESSONS LEARNED
This file serves as the persistent meta-memory for the AI Architect (Gemini).
Read this before complex tasks to avoid repeating past mistakes.

## 1. Coding & Syntax
- **F-String Escaping:** When generating Python code that contains JSON-like structures inside an f-string, ALWAYS escape curly braces.
  - *Wrong:* `f"result = { 'key': 'val' }"`
  - *Right:* `f"result = {{ 'key': 'val' }}"`
- **Path Handling:** NEVER assume files are in `./`. Always use `os.getcwd()` or the centralized `config.py` paths.
  - *Impact:* Aider creates files in `.sandbox` instead of `src` if paths are relative.

## 2. Agentic Behavior
- **Aider "Resistance":** Aider tends to hallucinate libraries if it doesn't know them.
  - *Fix:* Provide explicit "Cheat Sheet" or boilerplate code in the prompt.
  - *Better Fix:* Write the skeleton manually, use Aider for filling gaps.
- **Git Status Noise:** Aider creates untracked files or commits automatically.
  - *Fix:* Use `--no-auto-commits` to let the Orchestrator/Sentinel handle verification before committing.

## 3. System Architecture
- **Single Source of Truth:** `src/agentic/core/config.py` is the ONLY place for paths. Do not hardcode paths in plugins.
- **RAG Memory:** Must handle `chroma_db` locking or corruption gracefully. Use `try-except` during initialization.
