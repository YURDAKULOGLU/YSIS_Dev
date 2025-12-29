# YBIS Risk Classification Matrix

> Standard v1.1
> Tasks triggering Level 3 MUST have a Council Vote and Full Artifacts.

---

## Level 1: LOW RISK
Standard execution. No special gating.
- Triggers:
  - Logic-only code changes within src/ (algorithms, formatting).
  - Documentation updates.
  - Read-only database queries (SQLite).
  - Unit test creation.

## Level 2: MEDIUM RISK
Requires Architect Review or Peer Review.
- Triggers:
  - Modifying Core Config (src/agentic/core/config.py).
  - Adding new dependencies to requirements.txt.
  - Database schema changes.
  - Changes to public API/Protocols.

## Level 3: HIGH RISK
Mandatory Council Vote + Full Artifact Mode.
- Triggers:
  - Shell Access: Any task using subprocess, os.system, or shell-based tools.
  - Network Access: External API calls (outside whitelist) or web scraping.
  - Secret Access: Handling, rotating, or creating API keys/secrets.
  - Self-Modification: Tasks that modify Graph Nodes or Workflow logic.
  - Out-of-Bounds Access: Writing files outside the Project Root or assigned workspaces.

---

## High Risk Enforcement
When a task is classified as Level 3:
1. Council Vote: At least 3 LLMs must approve the PLAN.md.
2. Full Artifacts: EVIDENCE/summary.md is mandatory.
3. Sandbox: Execution should occur in a restricted container where feasible.