# Governance Documentation Conflicts - Patch Plan

**Date:** 2025-12-29
**Author:** claude-code
**Status:** READY FOR EXECUTION

---

## Executive Summary

Comprehensive scan found **37 conflicts** across **21 files** that contradict governance rules in `docs/governance/YBIS_CONSTITUTION.md` and `docs/specs/GOVERNANCE_ACTION_PLAN.md`.

**Risk Assessment:**
- 4 CRITICAL conflicts blocking governance enforcement
- 6 HIGH priority conflicts causing agent confusion
- 17 MEDIUM priority conflicts creating inconsistency
- 10 LOW priority legacy documentation issues

**Timeline:** 4 weeks organized into prioritized tasks

---

## PHASE 1: CRITICAL FIXES (Week 1, Days 1-2)

### TASK-DOC-001: Add Constitution References to Primary Onboarding

**Priority:** CRITICAL
**Files:** 2
**Effort:** 2 hours

**Problem:** `AI_START_HERE.md` and `README.md` (primary entry points) don't reference the constitution.

**Patch:**

**File 1: `AI_START_HERE.md`**
- **Location:** After line 14 (after "What is YBIS?")
- **Action:** INSERT new section

```markdown
## 📜 Governance (READ FIRST)

**CRITICAL:** Before you do anything, read the supreme law:
- **Constitution:** [`docs/governance/YBIS_CONSTITUTION.md`](docs/governance/YBIS_CONSTITUTION.md)
- **Action Plan:** [`docs/specs/GOVERNANCE_ACTION_PLAN.md`](docs/specs/GOVERNANCE_ACTION_PLAN.md)

These documents define:
- Single execution spine: `scripts/run_orchestrator.py` is the only runner
- MCP-first: Use `scripts/ybis.py` for all task operations
- Artifact requirements: PLAN, RUNBOOK, RESULT, META, CHANGES (lite mode)
- Local-first: Local providers default, cloud is feature-flagged
```

**File 2: `README.md`**
- **Location:** After line 15 (after project description)
- **Action:** INSERT new section

```markdown
## 📜 Governance

**Start here:** [`docs/governance/YBIS_CONSTITUTION.md`](docs/governance/YBIS_CONSTITUTION.md) - Supreme law for all agents and workflows.

Key principles:
- Single execution spine
- MCP-first operations
- Artifact-based traceability
- Local-first with feature flags
```

**Verification:**
- [ ] Links resolve correctly
- [ ] New agents see constitution reference immediately
- [ ] Both files updated and committed

---

### TASK-DOC-002: Remove Alternative Runner References

**Priority:** CRITICAL
**Files:** 1
**Effort:** 1 hour

**Problem:** `docs/specs/STABLE_VNEXT_ROADMAP.md` references alternative runners contradicting single spine.

**Patch:**

**File: `docs/specs/STABLE_VNEXT_ROADMAP.md`**
- **Location:** Line 23
- **Action:** REPLACE

**Before:**
```markdown
Wrappers: scripts/run_next.py, scripts/run_production.py
```

**After:**
```markdown
Single Runner: scripts/run_orchestrator.py (constitutional requirement)
Note: Legacy wrappers (run_next.py, run_production.py) deprecated. Use --mode flags instead.
```

**Verification:**
- [ ] No references to alternative runners remain
- [ ] Constitution compliance verified
- [ ] File updated and committed

---

### TASK-DOC-003: Remove Direct Script Execution Pattern

**Priority:** CRITICAL
**Files:** 1
**Effort:** 1 hour

**Problem:** `SPEC_NEXT_EVOLUTION.md` instructs `python scripts/add_task.py` (bypasses MCP).

**Patch:**

**File: `docs/specs/SPEC_NEXT_EVOLUTION.md`**
- **Location:** Line 52
- **Action:** REPLACE

**Before:**
```markdown
Execute `python scripts/add_task.py` to add the implementation task to the backlog.
```

**After:**
```markdown
Use MCP-first approach:
```bash
# Via ybis.py (recommended)
python scripts/ybis.py task create --goal "..." --details "..."

# Via MCP tool (if available)
mcp_tools.create_task(goal="...", details="...")
```
Direct script execution (`scripts/add_task.py`) is deprecated per constitution.
```

**Verification:**
- [ ] MCP-first pattern enforced
- [ ] Old script reference removed
- [ ] Constitution alignment verified

---

### TASK-DOC-004: Add Constitution Reference to Agent Onboarding

**Priority:** CRITICAL
**Files:** 1
**Effort:** 1 hour

**Problem:** `AGENTS_ONBOARDING.md` doesn't reference constitution or governance.

**Patch:**

**File: `docs/AGENTS_ONBOARDING.md`**
- **Location:** After line 3 (after title)
- **Action:** INSERT new section

```markdown
## 📜 Constitutional Requirements

**BEFORE YOU START:** Read the supreme law:
- [`docs/governance/YBIS_CONSTITUTION.md`](governance/YBIS_CONSTITUTION.md)

All agents must follow:
1. Single execution spine: `scripts/run_orchestrator.py` only
2. MCP-first: All task ops via `scripts/ybis.py` or MCP tools
3. Artifacts required: PLAN, RUNBOOK, RESULT, META, CHANGES
4. Local-first: Local providers default, cloud feature-flagged

Violations block task completion.
```

**Verification:**
- [ ] Constitution link added
- [ ] Core principles summarized
- [ ] Enforcement noted

---

## PHASE 2: HIGH PRIORITY FIXES (Week 1, Days 3-5)

### TASK-DOC-005: Standardize Workspace Path References

**Priority:** HIGH
**Files:** 3
**Effort:** 3 hours

**Problem:** Conflicting workspace paths: `workspaces/active/` vs `.sandbox*` vs `.YBIS_Dev/.sandbox*`

**Decision Required:** Choose canonical path (recommend: `workspaces/active/<TASK_ID>/`)

**Patches:**

**File 1: `docs/governance/00_GENESIS/AGENT_CONTRACT.md`**
- **Lines:** 17, 24, 58, 65
- **Action:** REPLACE all `.YBIS_Dev/.sandbox/**` references

**Before:**
```markdown
Runtime artifacts must go to `.YBIS_Dev/.sandbox/**` or `.YBIS_Dev/.sandbox_hybrid/**`
```

**After:**
```markdown
Runtime artifacts must go to `workspaces/active/<TASK_ID>/` per constitution.
Subdirectories: docs/, artifacts/, tests/ (see YBIS_CONSTITUTION.md §3)
```

**File 2: `docs/MULTI_AGENT.md`**
- **Line:** 12
- **Action:** REPLACE

**Before:**
```markdown
Isolation: Agents MUST only write to `.sandbox_worker` or designated `src/` files.
```

**After:**
```markdown
Isolation: Agents write to `workspaces/active/<TASK_ID>/` (artifacts, tests, docs).
Code changes: src/ directory only. All changes tracked in CHANGES/changed_files.json.
```

**File 3: `docs/specs/SPEC_NEXT_EVOLUTION.md`**
- **Line:** 12
- **Action:** Same as File 2

**Verification:**
- [ ] All workspace references use `workspaces/active/`
- [ ] No `.sandbox*` references remain in active docs
- [ ] Constitution alignment verified

---

### TASK-DOC-006: Clarify Brain Path (Orchestrator vs Server Mode)

**Priority:** HIGH
**Files:** 1
**Effort:** 2 hours

**Problem:** `AGENTS_ONBOARDING.md` references `ybis_server.py --brain-mode` creating confusion about canonical brain.

**Patch:**

**File: `docs/AGENTS_ONBOARDING.md`**
- **Lines:** 8-16
- **Action:** REPLACE brain protocol section

**Before:**
```markdown
Protocol: MCP (Model Context Protocol) over SSE.
Endpoint: `http://localhost:8000/sse` (when `ybis_server.py --brain-mode` is running).
```

**After:**
```markdown
Brain Architecture (per Governance Action Plan):
- **Canonical Brain:** `src/agentic/core/graphs/orchestrator_graph.py` (single source of truth)
- **Execution Spine:** `scripts/run_orchestrator.py` (only runner)
- **MCP Interface:** `scripts/ybis.py` (task operations, messaging)

Optional server mode (`ybis_server.py --brain-mode`) for external integrations only.
Internal agents use orchestrator_graph directly.
```

**Verification:**
- [ ] Canonical brain path clarified
- [ ] Server mode marked as optional/external
- [ ] Constitution alignment verified

---

### TASK-DOC-007: Standardize Verification Tool References

**Priority:** HIGH
**Files:** 4
**Effort:** 3 hours

**Problem:** Multiple verification tools mentioned: `protocol_check.py`, `ybis-dev verify`, `Sentinel`

**Decision:** Constitution specifies `scripts/protocol_check.py` as canonical

**Patches:**

**File 1: `docs/governance/00_GENESIS/AGENT_CONTRACT.md`**
- **Line:** 74
- **Action:** REPLACE

**Before:**
```markdown
Base verification (always required) - `ybis-dev verify` passes
```

**After:**
```markdown
Base verification (always required):
```bash
python scripts/protocol_check.py --task-id <TASK_ID> --mode lite
# For risk:high tasks, use --mode full
```
Per YBIS_CONSTITUTION.md §4, this is the canonical verification tool.
```

**File 2-4: `docs/MULTI_AGENT.md`, `docs/specs/SPEC_NEXT_EVOLUTION.md`**
- **Lines:** Multiple (17, 27 in each)
- **Action:** REPLACE all "Sentinel" references

**Before:**
```markdown
Proof: 'Done' means verified by Sentinel.
Code Quality: Sentinel Verification is mandatory before commit.
```

**After:**
```markdown
Verification: 'Done' means `protocol_check.py` passes (constitution §4).
Code Quality: Run `python scripts/protocol_check.py --mode lite` before completion.
```

**Verification:**
- [ ] All verification refs point to protocol_check.py
- [ ] Mode (lite/full) explained
- [ ] No Sentinel or ybis-dev verify refs remain

---

### TASK-DOC-008: Add Constitution Refs to Protocol Docs

**Priority:** HIGH
**Files:** 2
**Effort:** 2 hours

**Problem:** `STABILIZATION_PROTOCOL.md` and `EXTERNAL_AGENTS_PIPELINE.md` lack governance references.

**Patches:**

**File 1: `docs/specs/STABILIZATION_PROTOCOL.md`**
- **Location:** After line 1 (after title)
- **Action:** INSERT

```markdown
> **Governance Alignment:** This protocol implements requirements from [`docs/governance/YBIS_CONSTITUTION.md`](../governance/YBIS_CONSTITUTION.md) §3 (Execution Protocol) and §4 (Artifacts).
```

**File 2: `docs/EXTERNAL_AGENTS_PIPELINE.md`**
- **Location:** After line 1
- **Action:** INSERT

```markdown
> **Constitutional Requirements for External Agents:**
> All external agents must comply with [`docs/governance/YBIS_CONSTITUTION.md`](governance/YBIS_CONSTITUTION.md):
> - Use single spine (scripts/run_orchestrator.py)
> - MCP-first operations (scripts/ybis.py)
> - Produce required artifacts (PLAN, RUNBOOK, RESULT, META, CHANGES)
> - Pass verification (scripts/protocol_check.py)
```

**Verification:**
- [ ] Constitution references added
- [ ] Alignment noted
- [ ] External agents informed of requirements

---

## PHASE 3: MEDIUM PRIORITY FIXES (Week 2-3)

### TASK-DOC-009: Update Graph Path References

**Priority:** MEDIUM
**Files:** 3
**Effort:** 2 hours

**Problem:** Legacy `src/agentic/graph` path used instead of `src/agentic/core/graphs/orchestrator_graph.py`

**Patches:** Update all refs in `AI_START_HERE.md`, `MULTI_AGENT.md`, `SPEC_NEXT_EVOLUTION.md`

**Pattern:** Replace `src/agentic/graph` → `src/agentic/core/graphs/orchestrator_graph.py`

---

### TASK-DOC-010: Qualify Local-First Language

**Priority:** MEDIUM
**Files:** 2
**Effort:** 1 hour

**Problem:** "Always prefer Ollama" creates tech lock-in vs constitution's flexible "local by default"

**Patches:** Soften language in `MULTI_AGENT.md` and `SPEC_NEXT_EVOLUTION.md`

**Pattern:**
"Always prefer Local LLM (Ollama)" →
"Use local providers by default (constitution §1). Common: Ollama for LLM, Chroma for vectors. Cloud is opt-in via feature flags."

---

### TASK-DOC-011: Add Governance to Workflow Docs

**Priority:** MEDIUM
**Files:** 2
**Effort:** 2 hours

**Problem:** `PROMPTS_WORKFLOWS.md` and `system_overview.md` lack governance references

**Patches:** Add constitution pointers to both files

---

## PHASE 4: LOW PRIORITY CLEANUP (Week 3-4)

### TASK-DOC-012: Archive Legacy Genesis Docs

**Priority:** LOW
**Files:** 3
**Effort:** 1 hour

**Problem:** `docs/governance/00_GENESIS/ONBOARDING.md`, `AI_SYSTEM_GUIDE.md`, `3_PROTOCOLS.md` contain outdated paths

**Action:** Move to `docs/governance/00_GENESIS/LEGACY_ARCHIVE/` with README explaining deprecation

---

### TASK-DOC-013: Update Agent Contract for Current Architecture

**Priority:** LOW
**Files:** 1
**Effort:** 2 hours

**Problem:** `AGENT_CONTRACT.md` references old task board location and verification tools

**Patches:** Update to reference SQLite tasks.db and protocol_check.py

---

### TASK-DOC-014: Add Constitutional Alignment Sections to Specs

**Priority:** LOW
**Files:** 10
**Effort:** 5 hours

**Problem:** Spec documents (STABLE_V2_ROADMAP, UAP_PHASE_2_3, etc.) don't explain alignment with constitution

**Patches:** Add "Constitutional Alignment" section to each spec explaining how it complies with core principles

---

## PATCH PLAN SUMMARY

**Total Tasks:** 14
**Total Effort:** ~30 hours over 4 weeks
**Files to Update:** 21

**Week 1 (Critical + High):** 8 tasks, ~15 hours
**Week 2-3 (Medium):** 3 tasks, ~5 hours
**Week 3-4 (Low):** 3 tasks, ~10 hours

**Risk:** LOW - All changes are documentation updates, no code changes

**Rollback:** Git revert if any patch causes confusion

**Verification:** After each phase, run doc review with agents to confirm clarity

---

## EXECUTION CHECKLIST

### Before Starting
- [ ] Review patch plan with governance owner
- [ ] Get approval for workspace path decision (Phase 2, TASK-DOC-005)
- [ ] Create tracking tasks in YBIS task system

### During Execution
- [ ] One task at a time, sequential
- [ ] Verify each patch before committing
- [ ] Update this plan if new conflicts discovered

### After Completion
- [ ] Run full doc scan again to verify all conflicts resolved
- [ ] Update Governance Action Plan Phase 2 as complete
- [ ] Announce completion to all agents via debate

---

**STATUS:** READY FOR APPROVAL AND EXECUTION
