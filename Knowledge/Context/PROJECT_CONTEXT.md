# YBIS Project Context
> This file is automatically injected into Aider prompts to ensure project-aware code generation.

## LLM Configuration (CRITICAL)

### Available Providers
- **Ollama (LOCAL)** - Primary provider, always available
  - Models: qwen2.5-coder:32b, qwen2.5-coder:7b
  - Base URL: http://localhost:11434
  - NO API KEY REQUIRED

### NOT Available (DO NOT USE)
- ❌ OpenAI - No API key configured
- ❌ Anthropic - No API key configured  
- ❌ Google AI - No API key configured

### How to Call LLM in This Project
```python
# CORRECT - Use Ollama via requests
import requests
response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "qwen2.5-coder:7b", "prompt": "..."}
)

# CORRECT - Use ModelRouter
from src.agentic.core.plugins.model_router import default_router
config = default_router.get_model("CODING")  # Returns Ollama config

# WRONG - Never do this!
import openai  # ❌ NO API KEY
from anthropic import Anthropic  # ❌ NO API KEY
```

## Project Structure

### Core Components
- `src/agentic/core/` - Core orchestration (LangGraph + Pydantic)
- `src/agentic/core/plugins/` - Executor, Planner, Verifier plugins
- `scripts/run_orchestrator.py` - Main entry point
- `Knowledge/` - RAG data, lessons, errors

### Key Files
- `src/agentic/core/plugins/model_router.py` - Model selection (ALWAYS Ollama)
- `src/agentic/core/plugins/aider_executor_enhanced.py` - Code execution
- `src/agentic/core/plugins/sentinel_enhanced.py` - Verification
- `docs/governance/YBIS_CONSTITUTION.md` - Rules and principles

## Dependencies

### Installed Python Packages
- pydantic, langgraph, langchain
- requests, aiohttp
- chromadb, sentence-transformers
- pytest, ruff

### NOT Installed (Don't Import)
- openai (API package)
- anthropic
- google-generativeai

## Constitution Highlights

1. **Local-First**: Always prefer local solutions (Ollama over cloud APIs)
2. **Test-First**: Write tests before implementation
3. **Plugin-First**: Use adapters, never modify core frameworks
4. **Deterministic-First**: Prefer rule-based over ML when possible

## Common Patterns

### Adding LLM Functionality
```python
# Good pattern - local with fallback
class MyService:
    def __init__(self):
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.model = "qwen2.5-coder:7b"
    
    def call_llm(self, prompt: str) -> str:
        try:
            resp = requests.post(f"{self.ollama_url}/api/generate", 
                json={"model": self.model, "prompt": prompt, "stream": False})
            return resp.json().get("response", "")
        except Exception:
            return self._fallback_logic(prompt)  # Graceful degradation
```

### File Operations
```python
# Always use pathlib
from pathlib import Path
file_path = Path("Knowledge/Logs/lessons.jsonl")
file_path.parent.mkdir(parents=True, exist_ok=True)
```

---
*Last updated: 2026-01-03*
*This context is injected by aider_executor_enhanced.py*

