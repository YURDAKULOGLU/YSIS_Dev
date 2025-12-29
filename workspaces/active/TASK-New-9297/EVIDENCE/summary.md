# Evidence

## Commands
- rg -n "run_next.py|run_production.py|run_orchestrator.py" docs README.md AI_START_HERE.md
- rg -n "\\.YBIS_Dev" docs AI_START_HERE.md README.md
- Get-Content -Raw scripts/run_next.py
- Get-Content -Raw scripts/run_production.py
- Get-Content -Raw src/agentic/core/graphs/orchestrator_graph.py
- Get-Content -Raw src/agentic/graph/workflow.py

## Notes
- Canonical Brain path selected: src/agentic/core/graphs/orchestrator_graph.py.
- Entry point consolidated to scripts/run_orchestrator.py.
- Onboarding docs updated to remove .YBIS_Dev hardcode in connection methods.
