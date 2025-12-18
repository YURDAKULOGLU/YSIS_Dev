# YBIS-OS Lessons Learned

## 2025-12-14: PydanticAI Version Mismatch
- **Issue:** `pydantic_ai` version 1.32.0 throws `Unknown keyword arguments: result_type` when passed to `Agent` constructor OR `run` method.
- **Root Cause:** The API surface seems to have changed or is stricter than expected.
- **Solution:** Removed `result_type` from both constructor and `run` method.
- **Workaround:** Implemented robust manual JSON extraction (`_extract_json`) in Agent classes (`developer.py`, `qa.py`) to parse LLM output safely.
- **Action Item:** Do not rely on PydanticAI's built-in structured output validation for now. Use Pydantic models for manual validation after extraction.

## 2025-12-14: Ollama Models
- **Constraint:** Local routing requires specific models to be pulled.
- **Solution:** Updated `runner.py` to use `qwen2.5-coder:14b` and `llama3.2:3b` which were available.
