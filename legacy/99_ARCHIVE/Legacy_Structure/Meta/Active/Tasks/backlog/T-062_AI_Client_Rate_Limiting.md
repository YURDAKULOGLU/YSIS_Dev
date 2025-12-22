# T-062: AI Client-Side Rate Limiting

**Priority:** P0 (Critical)
**Effort:** 0.5 day
**Assignee:** @Coding
**Source:** COMPREHENSIVE_APP_AUDIT_REPORT.md - Section 7.2

---

## Description

Implement client-side rate limiting for AI requests to prevent abuse and control costs.

## Tasks

- [ ] Create rate limiter utility
- [ ] Track requests per minute/hour
- [ ] Show user feedback when rate limited
- [ ] Add token usage tracking
- [ ] Display cost estimate to user (optional)

## Implementation

```typescript
// apps/mobile/src/services/ai/rateLimiter.ts
interface RateLimitConfig {
  maxRequestsPerMinute: number;
  maxTokensPerDay: number;
}

export function createRateLimiter(config: RateLimitConfig) {
  // Track and limit requests
}
```

## Limits

- 10 requests per minute
- 100,000 tokens per day
- Configurable via env vars

## Acceptance Criteria

- Users can't spam AI requests
- Clear message when rate limited
- Token usage visible (nice to have)

