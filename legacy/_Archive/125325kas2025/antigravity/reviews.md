# Antigravity - Review Requests

**Last Updated:** 2025-11-25 13:25 (Setup by Claude Code)

---

## Pending Reviews

*No pending reviews yet*

---

## Completed Reviews

*No completed reviews yet*

---

## How to Request Review

When your work is ready for review:

```markdown
## Review Request #[NUMBER] - [Date] [Time]
**Task:** [Task name]
**Reviewer:** @[Agent name] (e.g., @Claude, @Gemini)
**Priority:** [low/medium/high/urgent]

**Files Changed:**
- path/to/file1.ts
- path/to/file2.tsx

**What Changed:**
[Brief description of changes - 2-3 sentences]

**Why:**
[Rationale for changes]

**Testing Done:**
- [ ] TypeScript: 0 errors (`npx tsc --noEmit`)
- [ ] ESLint: 0 warnings (`pnpm lint`)
- [ ] Manual testing done
- [ ] Unit tests pass (if applicable)

**Review Focus:**
[What specifically to review - e.g., "Check Realtime subscription logic"]

**Status:** 🟡 AWAITING REVIEW
```

### Example Review Request

```markdown
## Review Request #1 - 2025-11-25 15:00
**Task:** useUserContext hook implementation
**Reviewer:** @Claude, @Gemini
**Priority:** high

**Files Changed:**
- apps/mobile/src/contexts/useUserContext.tsx

**What Changed:**
Implemented user context hook with notes, tasks, and events state management.
Added Supabase Realtime subscriptions for automatic updates.

**Why:**
Day 1-2 sprint requirement for User Context Infrastructure.

**Testing Done:**
- [x] TypeScript: 0 errors
- [x] ESLint: 0 warnings
- [x] Manual testing: Create note → Context updates ✅
- [ ] Unit tests (pending)

**Review Focus:**
- Realtime subscription logic correctness
- Error handling completeness
- Type safety

**Status:** 🟡 AWAITING REVIEW
```

---

## Review Checklist (For Reviewers)

When reviewing Antigravity's code:

- [ ] YBIS Constitution compliance
- [ ] TypeScript strict mode, no `any`
- [ ] No `@ts-ignore` or `@ts-expect-error`
- [ ] ESLint: 0 warnings
- [ ] Proper error handling
- [ ] Loading states handled
- [ ] Logger usage correct (`type` property present)
- [ ] Performance considerations
- [ ] Security (no sensitive data in logs)

---

## After Review

**Reviewer posts feedback here:**
```markdown
### Review #1 - Feedback from @Claude

**Status:** ✅ APPROVED / 🔄 CHANGES REQUESTED

**Feedback:**
- [List feedback items]

**Required Changes:** (if any)
- [Change 1]
- [Change 2]

**Approved?** YES / NO
```

**Antigravity responds:**
```markdown
### Review #1 - Response

**Changes Made:**
- [Change 1] - Fixed ✅
- [Change 2] - Fixed ✅

**Ready for re-review:** YES
```

---

**Last Updated:** 2025-11-25 13:25 by Claude Code (Setup)
