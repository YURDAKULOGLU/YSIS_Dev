# Evidence

## Commands
- Get-Content -Raw src/agentic/core/llm/__init__.py
- Get-Content -Raw src/agentic/core/llm/base.py
- Get-Content -Raw src/agentic/core/llm/providers/ollama.py
- Get-Content -Raw src/agentic/core/llm/provider_factory.py
- Get-Content -Raw scripts/run_orchestrator.py
- rg -n "YBIS_PROVIDER_MODE|YBIS_PLANNER_MODE" scripts/run_orchestrator.py

## Notes
- Manual provider abstraction added (BaseProvider + OllamaProvider).
- ProviderFactory defines fallback chain (API -> CLI -> Ollama).
- run_orchestrator uses provider mode flags to select planner.
