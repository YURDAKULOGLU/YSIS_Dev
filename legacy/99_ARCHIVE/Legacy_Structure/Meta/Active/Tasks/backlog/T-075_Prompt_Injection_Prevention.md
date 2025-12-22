# T-075: AI Prompt Injection Prevention

**Priority:** P1 (Important)
**Effort:** 0.5 day
**Assignee:** @Coding
**Source:** COMPREHENSIVE_APP_AUDIT_REPORT.md - Section 7.2

---

## Description

Prevent prompt injection attacks where user input could manipulate AI behavior.

## Attack Vectors

1. User message containing system prompt overrides
2. Note/task content injecting instructions
3. Tool arguments being manipulated

## Tasks

- [ ] Sanitize user input before including in prompts
- [ ] Separate user content from instructions clearly
- [ ] Validate tool arguments
- [ ] Add content moderation (optional)
- [ ] Log suspicious inputs

## Implementation

```typescript
// apps/mobile/src/services/ai/promptSecurity.ts

const INJECTION_PATTERNS = [
  /ignore previous instructions/i,
  /you are now/i,
  /new system prompt/i,
  /disregard all/i,
  /<system>/i,
  /\[INST\]/i,
];

export function sanitizeUserInput(input: string): string {
  let sanitized = input;
  
  // Remove potential injection attempts
  for (const pattern of INJECTION_PATTERNS) {
    sanitized = sanitized.replace(pattern, '[filtered]');
  }
  
  return sanitized;
}

export function isInputSuspicious(input: string): boolean {
  return INJECTION_PATTERNS.some(pattern => pattern.test(input));
}
```

## Apply Sanitization

```typescript
// In chat or AI service
if (isInputSuspicious(userMessage)) {
  Logger.warn('Suspicious input detected', { type: 'SECURITY' });
}

const sanitizedMessage = sanitizeUserInput(userMessage);
```

## Acceptance Criteria

- Injection attempts logged
- Suspicious content filtered
- AI behavior not manipulatable
- No false positives on normal input

