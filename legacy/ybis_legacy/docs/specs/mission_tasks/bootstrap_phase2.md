# Mission Task Template: bootstrap_phase2
Source: scripts/missions/run_bootstrap_phase2.py (deprecated)

Goal:
Implement Phase 2 of the Bootstrap Protocol: Docker sandbox for isolated execution.

Details:
- Deliverables:
  1) docker/Dockerfile.sandbox (Python 3.12 slim with git, aider, pytest)
  2) docker/docker-compose.yml to manage sandbox container
  3) src/agentic/core/plugins/docker_executor.py (run code in Docker)
  4) Task artifacts in workspaces/active/<TASK_ID> (PLAN/RUNBOOK/RESULT)
- Constraints:
  - Follow ARCHITECTURE_V2.md
  - Use PROJECT_ROOT paths from config
  - Avoid legacy paths (.sandbox, .sandbox_hybrid)

Verification:
- Targeted tests for docker executor and container startup.
- protocol_check passes for the task.
