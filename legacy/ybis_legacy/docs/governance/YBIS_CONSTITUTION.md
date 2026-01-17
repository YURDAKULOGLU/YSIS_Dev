# YBIS CONSTITUTION (Supreme Law)
> Status: Active and enforced
> Scope: All agents, tools, and workflows in this repo
> Authority: This document is the single source of truth for governance

## 0) Purpose
We are building a disciplined autonomous software factory. This constitution
defines quality standards, internal operations, and enforcement rules.

## 1) Core Principles (Non-Negotiable)
1. Single execution spine: `scripts/run_orchestrator.py` is the only runner.
2. MCP-first: all task operations and messaging use MCP tools or `scripts/ybis.py`.
3. Local-first: use local providers by default; cloud is opt-in and feature-flagged.
4. Traceability: no work without artifacts and verifiable outputs.
5. Minimal drift: one canonical path for brains, docs, and workflows.

## 2) Roles and Accountability
- Orchestrator owner: ensures the run spine stays canonical and stable.
- Governance owner: keeps this constitution and related docs consistent.
- Task owner: responsible for artifacts, verification, and accurate status.

## 3) Execution Protocol (Required)
All tasks follow the lifecycle:
Plan -> Execute -> Verify -> Artifacts -> Archive

Required steps:
1. Claim via MCP or `scripts/run_orchestrator.py`.
2. Create plan and runbook.
3. Implement changes with minimal scope.
4. Verify changes (tests or explicit manual checks).
5. Produce artifacts and mark task complete.
6. Archive workspace.

Messaging standard:
- Follow `docs/governance/MESSAGING_GUIDELINE.md` to reduce filler and tokens.

## 4) Artifacts and Evidence (Tiered System)

Artifacts scale with task risk to reduce token waste:

### Tier 0 (Doc-Only Tasks)
**Scope:** Documentation changes, <10 lines modified
**Required:** `docs/RUNBOOK.md` (command-only format, see below)
**Token Cost:** ~50 tokens

#### RUNBOOK Format Spec (All Tiers)
RUNBOOK.md must contain ONLY commands (no prose):
```bash
# Command 1
git add file.md
# Command 2
git commit -m "message"
# Commit: abc123
```

**Optional:** `docs/RUNBOOK.sh` (executable, self-verifying):
```bash
#!/bin/bash
set -e
git add file.md || exit 1
git commit -m "message" || exit 2
python scripts/protocol_check.py --task-id TASK-123 || exit 3
```
Use RUNBOOK.sh for replay/verification. Use RUNBOOK.md for auditability.

### Tier 1 (Low-Risk Tasks)
**Scope:** Small changes, <50 lines modified
**Required:** Tier 0 + `artifacts/RESULT.md` (5-line summary)
**Token Cost:** ~300 tokens

### Tier 2 (Standard Tasks - Default)
**Scope:** Normal tasks, ≥50 lines modified
**Required:** PLAN.md, RUNBOOK.md, RESULT.md, CHANGES/changed_files.json, META.json
**Token Cost:** ~800 tokens

### Tier 3 (High-Risk/Critical)
**Scope:** Explicit risk:high designation
**Required:** Tier 2 + `EVIDENCE/summary.md`
**Token Cost:** ~1200 tokens

### Auto-Detection & Enforcement
- `protocol_check.py --tier auto` auto-detects from git diff stats
- Manual override: `--tier 0|1|2` or `--mode full` (legacy Tier 3)
- Backward compatible: `--mode lite` = Tier 2, `--mode full` = Tier 3

### META.json Constitution Tags
All META.json files (Tier 2+) must include `constitution_tags` array:
```json
{
  "task_id": "TASK-123",
  "constitution_tags": ["§1", "§3", "§4"]
}
```

**Tag Mapping** (see `docs/governance/TAGGING_STANDARD.md`):
- **§1**: Prime Directives (Core Principles)
- **§2**: Corporate Hierarchy (Roles & Accountability)
- **§3**: Operational Protocols (Execution)
- **§4**: Artifacts & Evidence (Quality Standards)
- **§5**: Risk & Quality Gates

**Purpose**: Enables automated compliance verification and token-efficient constitutional alignment tracking.

## 4.5) Token Budget
- PLAN and RESULT frontmatter must include `token_budget` (default 2000).
- If the budget is exceeded, switch to summary-only mode:
  - RESULT: 5-10 lines max (what changed, why, verification).
  - META: only essential fields (task_id, owner, status, tests_run).
- Prefer diff-first reading (`rg`) instead of full file dumps.

## 5) Quality Standards
- No silent changes: every code change must be documented in RESULT and CHANGES.
- Testing: add or run tests when behavior changes. If not possible, record a
  clear manual verification in RESULT and explain the limitation in META.
- **Non-Testable Artifacts:** Test yazılamayacak şeylerin kalitesi de kontrol edilecek.
  Documentation, configuration, and design decisions must undergo quality verification
  even if automated tests are not possible. See VERIFICATION_STANDARDS.md §4 for details.
- Safety: avoid destructive commands unless explicitly approved.
- Observability: tracing hooks must be preserved or extended, never removed.

## 6) Framework Onboarding (RTFM)
Before adopting a framework:
1. Read its guide in `Knowledge/API_References/` or project docs.
2. Use a bridge in `src/agentic/bridges/` when applicable.
3. Record the decision in META and update governance docs if it changes policy.

## 7) Security and Secrets
- No secrets in the repo. Use environment variables only.
- Redact system prompts and sensitive data in any external telemetry.
- External network calls must be traceable and optional.

## 8) Exceptions and Waivers
If a rule must be broken:
1. Record the reason in META.
2. Add a temporary waiver entry in RESULT with an expiration condition.
3. Open a follow-up task to remove the waiver.

## 9) Change Control
- Any constitutional change must be announced to all agents.
- Update references in docs to prevent split-brain behavior.

## 10) Enforcement
Violations block task completion until resolved. Governance owner may pause work
and reassign tasks if compliance is repeatedly broken.
