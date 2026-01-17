# Self-Improve Workflow Specification

**Status**: Ready for Implementation  
**Priority**: HIGH  
**Type**: Proactive Self-Improvement Loop

---

## Overview

Build a **proactive self-improvement workflow** that continuously improves the system without waiting for failures. This is Phase 2 - moving from reactive loops to proactive improvement.

```
REFLECT → PLAN → IMPLEMENT → TEST → INTEGRATE → (loop)
```

---

## Workflow Structure

### Node Sequence

1. **reflect** - Analyze system state, metrics, recent runs
2. **plan** - Generate improvement plan based on reflection
3. **implement** - Execute improvements
4. **test** - Verify improvements work
5. **integrate** - Integrate tested improvements

### Key Differences from Reactive Loops

- **Proactive**: Runs on schedule or trigger, not just on failures
- **Evidence-based**: Uses metrics, not just errors
- **Continuous**: Forms a loop that keeps improving
- **YBIS-native**: Uses existing YBIS components, not external adapters

---

## Implementation Plan

### 1. Reflect Node

**Purpose**: Analyze current system state and identify improvement opportunities

**Inputs**:
- Recent run metrics (success rate, execution time)
- Error patterns from Error KB
- Code quality metrics (test coverage, lint issues)
- Performance metrics (gate pass rate, verification time)
- Staleness detection results

**Outputs**:
- `reflection_report.json` with:
  - System health score
  - Identified issues
  - Improvement opportunities
  - Prioritized action items

**Implementation**: `src/ybis/orchestrator/self_improve.py`

### 2. Plan Node

**Purpose**: Generate concrete improvement plan from reflection

**Inputs**:
- Reflection report
- Current system state
- Policy constraints

**Outputs**:
- `improvement_plan.json` with:
  - Specific improvements to make
  - Files to modify
  - Implementation steps
  - Success criteria

**Implementation**: Uses existing `LLMPlanner` with reflection context

### 3. Implement Node

**Purpose**: Execute improvement plan

**Inputs**:
- Improvement plan
- Reflection report

**Outputs**:
- `implementation_report.json`
- Modified files
- Change summary

**Implementation**: Uses existing `Executor` with improvement plan

### 4. Test Node

**Purpose**: Verify improvements work correctly

**Inputs**:
- Implementation report
- Modified files

**Outputs**:
- `test_report.json`
- Test results
- Verification status

**Implementation**: Uses existing `Verifier` + custom improvement tests

### 5. Integrate Node

**Purpose**: Integrate tested improvements into system

**Inputs**:
- Test report
- Implementation report
- Gate decision

**Outputs**:
- `integration_report.json`
- Rollback plan (if needed)
- Integration status

**Implementation**: Uses existing `self_integrate_node` logic

---

## Workflow Configuration

**File**: `configs/workflows/self_improve.yaml`

```yaml
name: self_improve
version: 2
description: "Proactive self-improvement workflow (YBIS-native)"

nodes:
  - id: reflect
    type: self_improve_reflect
    description: "Reflect on system state and identify improvements"
  
  - id: plan
    type: self_improve_plan
    description: "Plan improvements based on reflection"
  
  - id: implement
    type: self_improve_implement
    description: "Implement improvement plan"
  
  - id: test
    type: self_improve_test
    description: "Test implementation"
  
  - id: integrate
    type: self_improve_integrate
    description: "Integrate tested implementation"

connections:
  - from: START
    to: reflect
  
  - from: reflect
    to: plan
  
  - from: plan
    to: implement
  
  - from: implement
    to: test
  
  - from: test
    to: integrate
  
  - from: integrate
    to: END

requirements:
  modules:
    - planner
    - executor
    - verifier
  artifacts:
    - reflection_report.json
    - improvement_plan.json
    - implementation_report.json
    - test_report.json
    - integration_report.json
```

---

## Triggering the Workflow

### Option 1: Scheduled Trigger

```python
# Run every hour
python scripts/ybis_run.py SELF-IMPROVE --workflow self_improve
```

### Option 2: Event-Based Trigger

- After N successful runs
- When metrics degrade
- On schedule (cron)

### Option 3: Manual Trigger

```bash
python scripts/trigger_self_improve.py
```

---

## Success Criteria

1. **Reflection** identifies real improvement opportunities
2. **Planning** generates actionable improvement plans
3. **Implementation** successfully makes changes
4. **Testing** verifies improvements work
5. **Integration** safely integrates changes
6. **Loop** continues improving over time

---

## Implementation Files

1. `src/ybis/orchestrator/self_improve.py` - Self-improve node implementations
2. `configs/workflows/self_improve.yaml` - Workflow configuration
3. `scripts/trigger_self_improve.py` - CLI trigger script
4. `src/ybis/services/reflection_engine.py` - Reflection logic

---

## Next Steps

1. Implement reflection engine
2. Implement self-improve nodes
3. Update workflow configuration
4. Add trigger mechanism
5. Test end-to-end loop

