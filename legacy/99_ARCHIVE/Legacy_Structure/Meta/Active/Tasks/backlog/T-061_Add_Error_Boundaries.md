# T-061: Add React Error Boundaries

**Priority:** P0 (Critical)
**Effort:** 0.5 day
**Assignee:** @Coding
**Source:** COMPREHENSIVE_APP_AUDIT_REPORT.md - Section 5

---

## Description

Add React Error Boundary components to catch and handle runtime errors gracefully.

## Tasks

- [ ] Create `ErrorBoundary` component in `@ybis/ui`
- [ ] Create `ErrorFallback` component with retry button
- [ ] Wrap main app layout with ErrorBoundary
- [ ] Wrap each tab screen with ErrorBoundary
- [ ] Log errors to Logger when caught
- [ ] Add error recovery action (reload/retry)

## Implementation

```tsx
// packages/ui/src/error/ErrorBoundary.tsx
import { Component, type ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  // Implementation
}
```

## Acceptance Criteria

- App doesn't crash on unhandled errors
- User sees friendly error message
- Retry option available
- Errors logged to backend
