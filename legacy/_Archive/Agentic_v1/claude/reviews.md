# Claude Code - Review Requests

**Last Updated:** 2025-11-25 13:05

---

## Pending Reviews

*No pending reviews*

---

## Completed Reviews

*No completed reviews yet*

---

## Review Request Template

When ready for review:

```markdown
## Review Request #[NUMBER] - [Date] [Time]
**Task:** [Task name]
**Reviewer:** @[Agent name]
**Priority:** [low/medium/high/urgent]

**Files Changed:**
- file1.ts
- file2.ts
- file3.test.ts

**What Changed:**
[Brief description of changes]

**Why:**
[Rationale for changes]

**Testing Done:**
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing done
- [ ] No TypeScript errors
- [ ] No ESLint warnings

**Review Focus:**
[What specifically to review - architecture, logic, performance, etc.]

**Status:** 🟡 AWAITING REVIEW
```

---

## Review Checklist (For Reviewer)

When reviewing code:

- [ ] YBIS Constitution compliance
- [ ] TypeScript strict mode, no `any`
- [ ] No `@ts-ignore` or `@ts-expect-error`
- [ ] ESLint: 0 warnings
- [ ] Test coverage ≥80%
- [ ] Port architecture followed
- [ ] UI isolation (no direct tamagui imports in apps/)
- [ ] Proper error handling
- [ ] Loading states handled
- [ ] Performance considerations
- [ ] Security (no console.log with sensitive data)

---

**Last Updated:** 2025-11-25 13:05 by Claude Code
