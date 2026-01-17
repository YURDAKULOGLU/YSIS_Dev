# YBIS Self-Development Plan

**Purpose:** Enable YBIS to develop itself using its own workflows and governance.
**Status:** Planning Phase
**Date:** 2026-01-09

---

## Executive Summary

YBIS should be able to develop itself using its own workflows, following the principle: **"We build the factory, not just the product."**

This plan defines a YBIS-native self-development system that:
1. Uses existing YBIS workflows (spec → plan → execute → verify → gate)
2. Adds self-development specific nodes (reflect, analyze, propose)
3. Enforces stricter governance for self-changes
4. Requires evidence (spec + plan + tests + gate) for all self-changes
5. Provides rollback mechanisms

---

## Core Principles

### 1. Self-Development as First-Class Workflow
- Self-development is a **workflow** like any other
- Uses same artifact schema (spec, plan, executor_report, verifier_report, gate_report)
- Follows same governance rules (gates, approvals)

### 2. Evidence-First for Self-Changes
- **Every self-change requires:**
  - SPEC.md (what we're changing and why)
  - PLAN.json (how we'll change it)
  - Executor report (what changed)
  - Verifier report (tests pass)
  - Gate report (governance passed)
- **No exceptions** - even "small" changes need evidence

### 3. Stricter Governance
- Self-changes to core require **explicit approval**
- Self-changes to workflows require **workflow validation**
- Self-changes to adapters require **adapter conformance tests**
- Rollback plan required for all self-changes

### 4. Reflection-Driven
- System reflects on:
  - Recent failures (verifier errors, gate blocks)
  - Performance metrics (execution time, success rate)
  - Code quality (lint errors, test coverage)
  - User feedback (if available)
- Reflection generates improvement opportunities

---

## Architecture

### Self-Development Workflow

```yaml
name: self_develop
version: 1
description: "YBIS-native self-development workflow"

nodes:
  - id: reflect
    type: self_reflect
    description: "Reflect on system state and identify improvements"
  
  - id: analyze
    type: self_analyze
    description: "Analyze reflection and prioritize improvements"
  
  - id: propose
    type: self_propose
    description: "Propose specific improvements as tasks"
  
  - id: spec
    type: spec_generator
    description: "Generate SPEC.md for proposed improvement"
  
  - id: plan
    type: planner
    description: "Generate PLAN.json for implementation"
  
  - id: execute
    type: executor
    description: "Execute self-change"
  
  - id: verify
    type: verifier
    description: "Verify self-change (tests + lint)"
  
  - id: gate
    type: self_gate
    description: "Stricter gate for self-changes"
  
  - id: integrate
    type: self_integrate
    description: "Integrate self-change (with rollback plan)"

connections:
  - from: START
    to: reflect
  
  - from: reflect
    to: analyze
  
  - from: analyze
    to: propose
  
  - from: propose
    to: spec
  
  - from: spec
    to: plan
  
  - from: plan
    to: execute
  
  - from: execute
    to: verify
  
  - from: verify
    to: gate
  
  - from: gate
    to: integrate
  
  - from: integrate
    to: END

requirements:
  artifacts:
    - reflection_report.json
    - analysis_report.json
    - proposal_report.json
    - spec.md
    - plan.json
    - executor_report.json
    - verifier_report.json
    - gate_report.json
    - rollback_plan.json
```

---

## Node Implementations

### 1. self_reflect Node

**Purpose:** Reflect on system state and identify improvement opportunities.

**Inputs:**
- Recent runs (last N runs)
- Verifier reports (errors, warnings)
- Gate reports (blocks, approvals)
- Performance metrics (execution time, success rate)
- Code quality metrics (lint errors, test coverage)

**Outputs:**
- `reflection_report.json` with:
  - Issues identified
  - Opportunities identified
  - Patterns detected
  - Priority scores

**Implementation:**
- Analyze recent runs from control_plane.db
- Extract patterns from verifier/gate reports
- Calculate metrics (success rate, avg execution time)
- Use LLM to identify improvements (with codebase context)

### 2. self_analyze Node

**Purpose:** Analyze reflection and prioritize improvements.

**Inputs:**
- `reflection_report.json`

**Outputs:**
- `analysis_report.json` with:
  - Prioritized improvements (P1, P2, P3)
  - Impact assessment
  - Risk assessment
  - Dependencies

**Implementation:**
- Score improvements by impact and risk
- Check dependencies (what needs to change first)
- Prioritize based on:
  - Impact on system stability
  - Risk of breaking changes
  - User value
  - Technical debt reduction

### 3. self_propose Node

**Purpose:** Propose specific improvements as actionable tasks.

**Inputs:**
- `analysis_report.json`

**Outputs:**
- `proposal_report.json` with:
  - Proposed tasks (one per improvement)
  - Task objectives
  - Success criteria
  - Rollback plans

**Implementation:**
- Convert prioritized improvements to task objectives
- Define success criteria for each task
- Create rollback plan (how to undo if fails)
- Register tasks in control_plane.db (status: PROPOSED)

### 4. self_gate Node

**Purpose:** Stricter gate for self-changes.

**Additional Checks:**
- Core changes require explicit approval
- Workflow changes require workflow validation
- Adapter changes require adapter conformance tests
- Rollback plan must exist
- All tests must pass (no exceptions)

**Implementation:**
- Extend existing `gate_node()` with self-development specific checks
- Check if changes touch protected paths (core, workflows, adapters)
- Require approval for protected path changes
- Validate rollback plan exists
- Enforce stricter test requirements

### 5. self_integrate Node

**Purpose:** Integrate self-change with rollback capability.

**Inputs:**
- `gate_report.json` (must be PASS)
- `rollback_plan.json`

**Outputs:**
- Integration report
- Git commit (if enabled)
- Rollback checkpoint

**Implementation:**
- Create rollback checkpoint (git tag or snapshot)
- Apply changes (already done by execute node)
- Create integration report
- Optionally commit changes (if workflow allows)

---

## Task Schema for Self-Development

### Self-Development Task Type

```python
class SelfDevelopmentTask(Task):
    """Task for self-development."""
    
    task_type: str = "self_develop"
    improvement_area: str  # e.g., "core", "workflow", "adapter"
    rollback_plan: Dict[str, Any]
    requires_approval: bool = True
```

### Self-Development Artifacts

**Required Artifacts:**
1. `reflection_report.json` - System reflection
2. `analysis_report.json` - Improvement analysis
3. `proposal_report.json` - Proposed tasks
4. `spec.md` - Specification for self-change
5. `plan.json` - Implementation plan
6. `executor_report.json` - What changed
7. `verifier_report.json` - Tests and lint results
8. `gate_report.json` - Governance check
9. `rollback_plan.json` - How to undo changes

---

## Governance Rules

### Protected Paths for Self-Changes

**Core (Requires Approval):**
- `src/ybis/contracts/`
- `src/ybis/syscalls/`
- `src/ybis/control_plane/`
- `src/ybis/orchestrator/gates.py`
- `src/ybis/constants.py`

**Workflows (Requires Validation):**
- `configs/workflows/*.yaml`
- Must pass workflow validation
- Must have gate node
- Must declare artifacts

**Adapters (Requires Conformance Tests):**
- `src/ybis/adapters/*.py`
- Must pass adapter conformance tests
- Must implement `is_available()`
- Must be registered in catalog

### Rollback Requirements

**All self-changes must have:**
- Rollback plan in `rollback_plan.json`
- Git checkpoint (tag or commit hash)
- Manual rollback instructions (if automated rollback not possible)

---

## Implementation Plan

### Phase 1: Core Infrastructure
- [ ] Create `self_develop.yaml` workflow spec
- [ ] Implement `self_reflect` node
- [ ] Implement `self_analyze` node
- [ ] Implement `self_propose` node
- [ ] Implement `self_gate` node (extend existing)
- [ ] Implement `self_integrate` node

### Phase 2: Reflection System
- [ ] Build reflection data collection (runs, reports, metrics)
- [ ] Implement reflection analysis (pattern detection)
- [ ] Implement improvement identification (LLM-based)

### Phase 3: Task Generation
- [ ] Implement task proposal system
- [ ] Implement rollback plan generation
- [ ] Implement task registration

### Phase 4: Governance
- [ ] Extend gate node for self-changes
- [ ] Implement approval workflow
- [ ] Implement rollback checkpoint system

### Phase 5: Integration
- [ ] Test self-development workflow end-to-end
- [ ] Validate governance rules
- [ ] Test rollback mechanisms

---

## Example: Self-Development Task

**Scenario:** System detects that `gate_node()` is missing artifact enforcement.

**Reflection:**
- Recent runs show missing artifacts not being caught
- Gate reports show PASS even when artifacts missing
- Code analysis shows `gate_node()` doesn't check artifacts

**Analysis:**
- Priority: P1 (high impact on governance)
- Risk: Medium (core change)
- Impact: High (fixes governance gap)

**Proposal:**
- Task: "Add artifact enforcement to gate_node"
- Objective: "Ensure gate_node checks for required artifacts from workflow spec"
- Success Criteria:
  - Gate blocks when artifacts missing
  - Gate passes when artifacts present
  - Tests pass
- Rollback: Revert gate_node changes, restore previous version

**Execution:**
- Generate SPEC.md
- Generate PLAN.json
- Execute changes
- Verify (tests pass)
- Gate (governance check)
- Integrate (commit with rollback tag)

---

## Next Steps

1. **Create workflow spec:** `configs/workflows/self_develop.yaml`
2. **Implement nodes:** Start with `self_reflect` node
3. **Build reflection system:** Collect and analyze system state
4. **Test with simple improvement:** Fix a small issue using self-development workflow

---

## References

- `docs/reports/SYSTEM_INVENTORY_BRAINSTORM.md` - Self-development requirements
- `docs/governance/SELF_HEALING_PROTOCOL.md` - Self-healing concepts
- `configs/workflows/self_improve.yaml` - Vendor-based self-improvement (reference)
- `src/ybis/orchestrator/graph.py` - Existing node implementations

