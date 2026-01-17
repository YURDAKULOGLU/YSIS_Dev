"""
Specification Templates for Spec-Driven Development (SDD)

Provides pre-defined templates for different task types:
- Feature development
- Refactoring
- Bug fixes
- Architecture changes
"""

from typing import Dict

# Feature specification template
FEATURE_TEMPLATE = """---
id: {task_id}
type: SPECIFICATION
category: feature
created_at: {timestamp}
---

# SPEC: {feature_name}

## Overview
{description}

## Requirements

### Functional Requirements
- [ ] Requirement 1: {requirement_1}
- [ ] Requirement 2: {requirement_2}
- [ ] Requirement 3: {requirement_3}

### Non-Functional Requirements
- [ ] Performance: {performance_requirement}
- [ ] Security: {security_requirement}
- [ ] Usability: {usability_requirement}

## API Contract

### Endpoints
```
POST /api/v1/{resource}
  Input:
    {input_schema}
  Output:
    {output_schema}
  Errors:
    - 400: Invalid input
    - 404: Resource not found
    - 500: Server error
```

## Data Model

### {entity_name}
```python
class {entity_name}:
    id: UUID              # Primary key
    {field_1}: {type_1}   # Description
    {field_2}: {type_2}   # Description
    created_at: datetime
    updated_at: datetime
```

## Implementation Steps

1. {step_1}
2. {step_2}
3. {step_3}
4. {step_4}

## Dependencies

- {dependency_1}
- {dependency_2}

## Testing Strategy

### Unit Tests
- Test {component_1}
- Test {component_2}

### Integration Tests
- Test end-to-end flow
- Test error handling

### Manual Testing
- [ ] Test scenario 1
- [ ] Test scenario 2

## Success Criteria

- [ ] All functional requirements met
- [ ] All tests passing
- [ ] Performance benchmarks met
- [ ] Documentation updated
- [ ] Code reviewed and approved

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| {risk_1} | {impact_1} | {mitigation_1} |
| {risk_2} | {impact_2} | {mitigation_2} |

## Timeline

- Research & Design: {design_time}
- Implementation: {impl_time}
- Testing: {test_time}
- Review: {review_time}

**Total Estimate:** {total_estimate}
"""

# Refactoring specification template
REFACTOR_TEMPLATE = """---
id: {task_id}
type: SPECIFICATION
category: refactor
created_at: {timestamp}
---

# SPEC: {refactor_name}

## Objective
{description}

## Current State

### Problems
1. {problem_1}
2. {problem_2}
3. {problem_3}

### Affected Files
- `{file_1}` - {file_1_issue}
- `{file_2}` - {file_2_issue}
- `{file_3}` - {file_3_issue}

### Metrics (Before)
- Code complexity: {complexity_before}
- Test coverage: {coverage_before}
- Technical debt: {debt_before}

## Target State

### Improvements
1. {improvement_1}
2. {improvement_2}
3. {improvement_3}

### Metrics (After)
- Code complexity: {complexity_after}
- Test coverage: {coverage_after}
- Technical debt: {debt_after}

## Migration Strategy

### Phase 1: Preparation
1. {prep_step_1}
2. {prep_step_2}

### Phase 2: Refactoring
1. {refactor_step_1}
2. {refactor_step_2}
3. {refactor_step_3}

### Phase 3: Validation
1. Run full test suite
2. Performance benchmarks
3. Code review

## Backward Compatibility

- [ ] API compatibility maintained
- [ ] Database schema compatible
- [ ] Configuration compatible
- [ ] No breaking changes

## Rollback Plan

If issues occur:
1. {rollback_step_1}
2. {rollback_step_2}
3. Restore from: {backup_location}

## Success Criteria

- [ ] No regression in functionality
- [ ] All tests passing (100%)
- [ ] Code complexity reduced by {target_reduction}%
- [ ] Test coverage increased to {target_coverage}%
- [ ] No performance degradation

## Timeline

- Analysis: {analysis_time}
- Refactoring: {refactor_time}
- Testing: {test_time}
- Deployment: {deploy_time}

**Total Estimate:** {total_estimate}
"""

# Bug fix specification template
BUGFIX_TEMPLATE = """---
id: {task_id}
type: SPECIFICATION
category: bugfix
created_at: {timestamp}
---

# SPEC: {bug_name}

## Bug Description
{description}

**Severity:** {severity}
**Priority:** {priority}
**Reported By:** {reporter}
**Reported Date:** {report_date}

## Reproduction Steps

1. {step_1}
2. {step_2}
3. {step_3}

**Expected Behavior:** {expected}
**Actual Behavior:** {actual}

## Root Cause Analysis

### Investigation
{investigation_summary}

### Root Cause
{root_cause}

### Affected Components
- {component_1}
- {component_2}

## Proposed Fix

### Solution
{solution_description}

### Code Changes
- File: `{file_1}`
  - Change: {change_1}
- File: `{file_2}`
  - Change: {change_2}

### Impact Assessment
- **Scope:** {impact_scope}
- **Risk:** {risk_level}
- **Affected Users:** {affected_users}

## Test Plan

### Regression Test
```python
def test_{test_name}():
    # Reproduce the bug
    {test_code}
    # Verify fix
    assert {assertion}
```

### Additional Tests
- [ ] Test {scenario_1}
- [ ] Test {scenario_2}
- [ ] Test edge cases

### Manual Verification
1. {verification_step_1}
2. {verification_step_2}

## Deployment Plan

### Pre-Deployment
- [ ] Code review approved
- [ ] Tests passing
- [ ] Documentation updated

### Deployment
1. {deploy_step_1}
2. {deploy_step_2}

### Post-Deployment
- [ ] Monitor error rates
- [ ] Verify fix in production
- [ ] Close related tickets

## Success Criteria

- [ ] Bug no longer reproducible
- [ ] All tests passing
- [ ] No new regressions introduced
- [ ] Regression test added

## Timeline

- Investigation: {investigation_time}
- Fix Implementation: {fix_time}
- Testing: {test_time}
- Deployment: {deploy_time}

**Total Estimate:** {total_estimate}
"""

# Architecture change specification template
ARCHITECTURE_TEMPLATE = """---
id: {task_id}
type: SPECIFICATION
category: architecture
created_at: {timestamp}
---

# SPEC: {architecture_name}

## Overview
{description}

## Current Architecture

### Diagram
```
{current_diagram}
```

### Components
1. {current_component_1}
2. {current_component_2}
3. {current_component_3}

### Limitations
1. {limitation_1}
2. {limitation_2}
3. {limitation_3}

## Proposed Architecture

### Diagram
```
{proposed_diagram}
```

### New Components
1. {new_component_1}
2. {new_component_2}
3. {new_component_3}

### Improvements
1. {improvement_1}
2. {improvement_2}
3. {improvement_3}

## Migration Strategy

### Phase 1: Foundation
1. {foundation_step_1}
2. {foundation_step_2}

### Phase 2: Migration
1. {migration_step_1}
2. {migration_step_2}

### Phase 3: Cutover
1. {cutover_step_1}
2. {cutover_step_2}

## Impact Analysis

### Services Affected
- {service_1}: {impact_1}
- {service_2}: {impact_2}

### Data Migration
- {data_migration_plan}

### Downtime Required
- Estimated: {downtime_estimate}
- Maintenance window: {maintenance_window}

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| {risk_1} | {prob_1} | {impact_1} | {mitigation_1} |
| {risk_2} | {prob_2} | {impact_2} | {mitigation_2} |

## Success Criteria

- [ ] New architecture deployed
- [ ] All services migrated
- [ ] Performance targets met
- [ ] Zero data loss
- [ ] Rollback plan tested

## Timeline

- Design: {design_time}
- Implementation: {impl_time}
- Testing: {test_time}
- Migration: {migration_time}
- Validation: {validation_time}

**Total Estimate:** {total_estimate}
"""

# Template registry
SPEC_TEMPLATES: Dict[str, str] = {
    "feature": FEATURE_TEMPLATE,
    "refactor": REFACTOR_TEMPLATE,
    "bugfix": BUGFIX_TEMPLATE,
    "bug": BUGFIX_TEMPLATE,  # Alias
    "architecture": ARCHITECTURE_TEMPLATE,
    "arch": ARCHITECTURE_TEMPLATE,  # Alias
}

# Default template (generic)
DEFAULT_TEMPLATE = """---
id: {task_id}
type: SPECIFICATION
category: general
created_at: {timestamp}
---

# SPEC: {task_name}

## Overview
{description}

## Goals
1. {goal_1}
2. {goal_2}
3. {goal_3}

## Approach
{approach}

## Implementation Steps
1. {step_1}
2. {step_2}
3. {step_3}

## Success Criteria
- [ ] {criterion_1}
- [ ] {criterion_2}
- [ ] {criterion_3}

## Timeline
**Estimated Time:** {estimate}
"""


def get_template(task_type: str) -> str:
    """
    Get template for task type.

    Args:
        task_type: Type of task (feature, refactor, bugfix, architecture)

    Returns:
        Template string
    """
    task_type = task_type.lower().strip()
    return SPEC_TEMPLATES.get(task_type, DEFAULT_TEMPLATE)


def list_templates() -> list:
    """List available template types"""
    return list(set(SPEC_TEMPLATES.keys()))


__all__ = [
    "SPEC_TEMPLATES",
    "DEFAULT_TEMPLATE",
    "get_template",
    "list_templates",
]
