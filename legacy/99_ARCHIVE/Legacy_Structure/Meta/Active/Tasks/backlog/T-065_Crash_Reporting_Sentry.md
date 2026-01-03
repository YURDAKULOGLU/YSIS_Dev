# T-065: Add Crash Reporting (Sentry)

**Priority:** P1 (Important)
**Effort:** 0.5 day
**Assignee:** @Coding
**Source:** COMPREHENSIVE_APP_AUDIT_REPORT.md - Section 11

---

## Description

Integrate Sentry for crash reporting and error monitoring in production.

## Tasks

- [ ] Create Sentry project for YBIS
- [ ] Install @sentry/react-native
- [ ] Configure Sentry in app entry point
- [ ] Add Sentry as Logger sink
- [ ] Test error reporting
- [ ] Set up alerting rules in Sentry dashboard

## Installation

```bash
pnpm add @sentry/react-native -w --filter @ybis/mobile
```

## Configuration

```typescript
// apps/mobile/app/_layout.tsx
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: process.env.EXPO_PUBLIC_SENTRY_DSN,
  environment: __DEV__ ? 'development' : 'production',
  tracesSampleRate: 0.2,
});
```

## Environment Variables

Add to `.env`:
```
EXPO_PUBLIC_SENTRY_DSN=https://xxx@sentry.io/xxx
```

## Acceptance Criteria

- Crashes reported to Sentry
- Source maps uploaded for readable stack traces
- Alerts configured for errors
