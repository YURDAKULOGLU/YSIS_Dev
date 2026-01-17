# EXTERNAL AGENTS PIPELINE

> **Constitutional Requirements for External Agents:**
> All external agents must comply with [`docs/CONSTITUTION.md`](CONSTITUTION.md):
> - Use single spine (`scripts/run_orchestrator.py`)
> - MCP-first operations (`scripts/ybis.py`)
> - Produce required artifacts (PLAN, RUNBOOK, RESULT, META, CHANGES)
> - Pass verification (`scripts/protocol_check.py`)

## Purpose
Define how external agents connect, declare capabilities, and pass acceptance gates.

## Requirements
- MCP-compatible interface or CLI that can read/write Markdown.
- Task execution must obey CoreConfig paths and allowed directories.
- Artifacts are mandatory: PLAN.md, RUNBOOK.md, EVIDENCE/*, CHANGES/*, META.json.

## Agent Package Standard
External agents must provide:
- agent.yaml (identity + capabilities)
- adapter.py (MCP tool wrapper)
- tests_contract.py (contract tests)
- runbook.md (setup + verification)
- policy_requirements.md (permissions needed)

## Sandbox and Permissions
- Default: tool deny, network deny, minimal file access.
- Allowlists must be explicit per task.
- Any violation fails the task.

## Acceptance Gate
- Manifest valid
- Contract tests pass
- Drift scan pass
- Artifacts pass
- Replay pass
