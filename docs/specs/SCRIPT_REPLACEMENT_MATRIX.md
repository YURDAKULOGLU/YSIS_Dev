# Script Replacement Matrix (Draft)
> Goal: Identify legacy scripts, preserve useful logic, and migrate to the single execution spine.
> Rule: No script is deleted without understanding the behavior and an alternative path.

## Summary
- Keep: core tooling required for governance and orchestration.
- Migrate: ad-hoc missions and direct-exec scripts into task workflows.
- Retire: legacy runners and redundant entrypoints.

## Keep (Core Tooling)
- `scripts/run_orchestrator.py` (single entrypoint)
- `scripts/ybis.py` (task + messaging CLI)
- `scripts/protocol_check.py` (artifact enforcement)
- `scripts/enforce_architecture.py` (governance gate)
- `scripts/smart_exec.py` (token-safe shell execution)
- `scripts/system_health_check.py` (diagnostics)

## Retire or Replace (Legacy Runners)
These bypass the single spine and should be replaced with orchestrator tasks:
- `scripts/run_graph.py` -> replace with orchestrator task for graph execution.
- `scripts/run_next.py`, `scripts/run_production.py`, `scripts/runners/orchestrator_main.py`
  -> replace with `scripts/run_orchestrator.py` (already canonical).

## Migrate (Mission Scripts)
All `scripts/missions/*` should be turned into task templates:
- Bootstrap/repair tasks (e.g., `run_bootstrap_phase2.py`, `run_fix_*`) -> tasks in `tasks.db` with plan/runbook.
- Demo tasks (e.g., `run_snake_mission.py`, `run_weather_mission.py`) -> sample tasks or docs-only examples.
- Stress/bench tasks (e.g., `run_stress_test_suite.py`) -> integration tests or dedicated benchmarking workflow.

## Migrate (Ingest and Automation)
- `scripts/ingest_*` -> orchestrator tasks or scheduled jobs with artifacts.
- `scripts/automation/run_playwright_scrape.py` -> keep as a workflow-driven tool or move to `tests/e2e` if used for verification.

## Migrate (Utilities)
Utilities that can be task-driven:
- `scripts/add_task.py` -> use `scripts/ybis.py create`.
- `scripts/listen.py` -> integrate into orchestrator loop or retire if unused.
- `scripts/test_tracing.py`, `scripts/test_publish.py` -> fold into tests or diagnostics.

## Keep With Caution (Debug Utilities)
These can stay but should be labeled "debug-only" and excluded from production:
- `scripts/utils/*` (debug_*.py, inspect_fastmcp.py, error_parser.py)

## Migration Rules
1. Capture the logic in a task PLAN and RESULT before replacing.
2. Provide an equivalent task or workflow path.
3. Mark legacy scripts as deprecated with a clear pointer to the new path.
4. Remove legacy script only after the replacement is verified.

## Staged Execution Plan
Phase 1: Legacy runner deprecations (runners + run_graph).
Phase 2: Convert missions to tasks (start with bootstrap/fix scripts).
Phase 3: Consolidate utilities and ingest scripts.
