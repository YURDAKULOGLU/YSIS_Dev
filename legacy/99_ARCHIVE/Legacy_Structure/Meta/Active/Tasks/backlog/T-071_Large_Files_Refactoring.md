# T-071: Refactor Large Files

**Priority:** P2 (Nice to Have)
**Effort:** 1 day
**Assignee:** @Coding
**Source:** COMPREHENSIVE_APP_AUDIT_REPORT.md - Section 2.2

---

## Description

Some files are too long (500+ lines) and should be split into smaller modules.

## Files to Refactor

### Priority 1 (Over 500 lines)
- [ ] `useFlows.ts` (~630 lines) - Split templates, handlers, CRUD
- [ ] `toolServiceFunctions.ts` - Group by entity (note, task, event, flow)
- [ ] `toolExecutor.ts` - Extract case handlers

### Priority 2 (300-500 lines)
- [ ] `_layout.tsx` - Extract providers to separate file
- [ ] `useAuth.ts` - Extract push token logic
- [ ] Chat-related components

## Refactoring Strategy

### useFlows.ts Split

```
features/flows/
├── hooks/
│   ├── useFlows.ts          # Main hook, imports from below
│   ├── useFlowCRUD.ts       # create, update, delete
│   ├── useFlowExecution.ts  # runFlow, FlowEngine
│   └── flowTemplates.ts     # FLOW_TEMPLATES constant
```

### toolServiceFunctions.ts Split

```
services/data/
├── toolServiceFunctions.ts  # Re-exports all
├── noteTools.ts             # Note-related functions
├── taskTools.ts             # Task-related functions
├── eventTools.ts            # Event-related functions
└── flowTools.ts             # Flow-related functions
```

## Acceptance Criteria

- No file over 400 lines
- All imports still work
- No functionality changes
- Tests pass (when they exist)
