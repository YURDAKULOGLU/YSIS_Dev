# Self-Improve Workflow Guide

## Overview

The Self-Improve Workflow is a **proactive self-improvement loop** that continuously improves the system without waiting for failures. It implements:

```
REFLECT → PLAN → IMPLEMENT → TEST → INTEGRATE
```

## Key Features

- **Proactive**: Runs on schedule or trigger, not just on failures
- **Evidence-based**: Uses metrics, error patterns, and system health
- **YBIS-native**: Uses existing YBIS components (no external adapters)
- **Continuous**: Forms a loop that keeps improving

## Workflow Steps

### 1. Reflect

Analyzes system state:
- Recent run metrics (success rate, failure rate)
- Error patterns from Error Knowledge Base
- System health checks
- Code quality metrics
- Performance metrics

**Output**: `reflection_report.json`

### 2. Plan

Generates improvement plan from reflection:
- Prioritizes high-priority issues
- Creates actionable improvement tasks
- Uses LLMPlanner with reflection context

**Output**: `improvement_plan.json` (also saved as `plan.json`)

### 3. Implement

Executes improvement plan:
- Uses existing executor (local_coder or aider)
- Makes code changes
- Tracks modifications

**Output**: `implementation_report.json` (also saved as `executor_report.json`)

### 4. Test

Verifies improvements work:
- Runs verifier (lint + tests)
- Checks code quality
- Validates changes

**Output**: `test_report.json` (also saved as `verifier_report.json`)

### 5. Integrate

Integrates tested improvements:
- Uses existing self_integrate_node logic
- Creates rollback plan if needed
- Marks improvements as integrated

**Output**: `integration_report.json`

## Usage

### Manual Trigger

```bash
# Create self-improvement task
python scripts/trigger_self_improve.py

# Run the workflow
python scripts/ybis_run.py SELF-IMPROVE-XXXXX --workflow self_improve
```

### Scheduled Trigger

Add to cron or scheduler:

```bash
# Run every hour
0 * * * * cd /path/to/YBIS_Dev && python scripts/trigger_self_improve.py && python scripts/ybis_run.py $(python -c "import sys; sys.path.insert(0, '.'); from src.ybis.control_plane import ControlPlaneDB; import asyncio; db = ControlPlaneDB('platform_data/control_plane.db'); tasks = asyncio.run(db.get_pending_tasks()); print(tasks[-1].task_id if tasks else '')") --workflow self_improve
```

### Event-Based Trigger

Trigger after N successful runs or when metrics degrade.

## Workflow Configuration

**File**: `configs/workflows/self_improve.yaml`

The workflow uses YBIS-native nodes:
- `self_improve_reflect` - ReflectionEngine
- `self_improve_plan` - LLMPlanner
- `self_improve_implement` - Executor
- `self_improve_test` - Verifier
- `self_improve_integrate` - Integration logic

## Reflection Engine

The `ReflectionEngine` analyzes:

1. **System Health**: Health monitor checks
2. **Recent Metrics**: Success/failure rates from recent runs
3. **Error Patterns**: Recurring errors from Error KB
4. **Code Quality**: TODO/FIXME counts, technical debt
5. **Performance**: Execution times, verification times

Based on this analysis, it identifies:
- **Issues**: Problems that need fixing
- **Opportunities**: Improvements that can be made

## Example Reflection Report

```json
{
  "timestamp": "2026-01-10T12:00:00",
  "system_health": {
    "score": 0.8,
    "status": "degraded"
  },
  "recent_metrics": {
    "total_runs": 20,
    "success_rate": 0.85,
    "failure_rate": 0.15
  },
  "error_patterns": {
    "patterns_detected": 3,
    "top_patterns": [...]
  },
  "issues_identified": [
    {
      "type": "high_failure_rate",
      "severity": "high",
      "description": "Failure rate is 15.0% (threshold: 20%)"
    }
  ],
  "opportunities_identified": [
    {
      "area": "reliability",
      "priority": "high",
      "description": "Success rate is 85.0% - target: 90%"
    }
  ]
}
```

## Integration with Reactive Loops

The Self-Improve Workflow complements the reactive loops:

- **Reactive Loops** (Phase 1): Respond to failures
  - Lesson Engine → Policy
  - Health Monitor → Self-Heal
  - Error KB → Planner
  - Staleness → Tasks

- **Proactive Loop** (Phase 2): Improve before failures
  - Reflect → Plan → Implement → Test → Integrate

Together, they form a complete self-improvement system:
- Reactive loops fix immediate problems
- Proactive loop prevents future problems

## Success Criteria

A successful self-improvement cycle:
1. Reflection identifies real opportunities
2. Planning generates actionable plans
3. Implementation makes changes successfully
4. Testing verifies improvements work
5. Integration safely integrates changes
6. System metrics improve over time

## Monitoring

Track self-improvement effectiveness:
- Success rate trends
- Error pattern reduction
- Code quality improvements
- Performance improvements

## Next Steps

1. Run initial reflection to establish baseline
2. Let system improve itself over time
3. Monitor metrics to verify improvements
4. Adjust reflection criteria as needed

