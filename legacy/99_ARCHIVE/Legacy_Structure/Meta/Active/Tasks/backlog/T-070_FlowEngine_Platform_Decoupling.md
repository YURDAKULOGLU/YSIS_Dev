# T-070: FlowEngine Platform Decoupling

**Priority:** P2 (Nice to Have)
**Effort:** 0.5 day
**Assignee:** @Coding
**Source:** COMPREHENSIVE_APP_AUDIT_REPORT.md - Section 1.1

---

## Description

FlowEngine in `@ybis/core` uses `expo-crypto` which couples it to Expo platform. Should use dependency injection.

## Current Issue

```typescript
// packages/core/src/services/FlowEngine.ts
import { randomUUID } from 'expo-crypto'; // Platform-specific!
```

## Solution

Inject UUID generator via constructor:

```typescript
export interface FlowEngineConfig {
  logger?: FlowLogger;
  generateId?: () => string;
}

export class FlowEngine {
  private generateId: () => string;

  constructor(config?: FlowEngineConfig) {
    this.generateId = config?.generateId ?? (() => crypto.randomUUID());
  }
}
```

## Tasks

- [ ] Add `generateId` to FlowEngine constructor
- [ ] Remove direct expo-crypto import
- [ ] Update useFlows.ts to inject UUID generator
- [ ] Test FlowEngine still works

## Acceptance Criteria

- `@ybis/core` has no expo-* dependencies
- FlowEngine works with injected dependencies
- No breaking changes to API
