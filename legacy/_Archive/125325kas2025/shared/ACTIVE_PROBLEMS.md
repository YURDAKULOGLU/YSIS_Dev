# Active Problems - Week 1 Sprint
**Date:** 2025-11-25 17:30
**Status:** 🔴 BLOCKED - 2 Critical Errors

---

## 🚨 Problem #1: Table Name Mismatch - `calendar_events`

### Error Message
```
DatabaseError: Could not find the table 'public.calendar_events' in the schema cache
Code: UNKNOWN_ERROR
```

### Root Cause
Code is querying `calendar_events` but Supabase table is named `events`

### Evidence
- Supabase has table: `events` ✅ (verified with SQL query)
- Code is calling: `calendar_events` ❌
- Stack trace: `useWorkspace` or similar hook calling database

### Investigation Needed
**@Claude Code:** Find all code references to `calendar_events`:
```bash
grep -r "calendar_events" apps/mobile/src/
```

### Solution Options
1. **Rename in code** (PREFERRED): Change all `calendar_events` → `events` in codebase
2. **Rename in DB**: Run SQL to rename `events` → `calendar_events` (NOT recommended)

### Assigned To
**Primary:** @Claude Code (find all references)
**Review:** @Gemini (architectural review)

### Priority
🔴 P0 - BLOCKER (cannot load calendar data)

---

## 🚨 Problem #2: OpenAI Initialization Failure

### Error Message
```
LLMError: Failed to initialize OpenAI client
Code: NOT_INITIALIZED
Original Error: Failed to connect to OpenAI
```

### Root Cause
OpenAI healthCheck() failing - possible causes:
1. Invalid API key
2. Network connectivity issue
3. API key doesn't have proper permissions
4. Rate limiting

### Evidence
- `EXPO_PUBLIC_OPENAI_API_KEY` exists in `.env` ✅
- Key is being loaded ✅ (otherwise different error)
- healthCheck() failing ❌ (OpenAIAdapter.ts:70)

### Investigation Needed
**@Claude Code:**
1. Check if API key is valid (test with curl)
2. Check healthCheck() implementation
3. Add more detailed error logging in OpenAIAdapter

**Investigation Steps:**
```bash
# Test API key manually
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $EXPO_PUBLIC_OPENAI_API_KEY"
```

### Solution Options
1. **Verify API key**: Ensure key has correct permissions
2. **Add retry logic**: healthCheck might be timing out
3. **Better error handling**: Show specific OpenAI error message
4. **Fallback**: Allow app to work without AI (graceful degradation)

### Assigned To
**Primary:** @Claude Code (investigate + fix)
**Review:** @Gemini (review error handling)

### Priority
🟡 P1 - HIGH (AI chat blocked, but app otherwise works)

---

## 📊 Impact Assessment

### Users Affected
- 100% of users (Closed Beta testing)

### Features Blocked
- ✅ Authentication: WORKING
- ✅ Notes: WORKING
- ✅ Tasks: WORKING
- ❌ Calendar/Events: BLOCKED (Problem #1)
- ❌ AI Chat: BLOCKED (Problem #2)

### Sprint Impact
- Day 1-2 (User Context): ⚠️ PARTIAL (events broken)
- Day 3 (System Prompt): ❌ BLOCKED (depends on AI)
- Day 4-5 (Tool Calling): ❌ BLOCKED (depends on AI)
- Day 6 (Testing): ❌ BLOCKED (cannot test AI)
- Day 7 (Deploy): ❌ BLOCKED (critical bugs)

**Sprint Status:** 🔴 AT RISK

---

## 🎯 Action Plan

### Immediate Actions (Next 30 min)

**@Claude Code:**
1. ✅ Find all `calendar_events` references in codebase
2. ✅ Replace with `events`
3. ✅ Test calendar loading
4. ⏳ Investigate OpenAI connection issue
5. ⏳ Fix or implement workaround

**@Gemini:**
1. ⏳ Review architectural implications of fixes
2. ⏳ Suggest error handling improvements
3. ⏳ Review if healthCheck() implementation is correct

**@User:**
1. ⏳ Restart Metro after fixes
2. ⏳ Test calendar + AI chat
3. ⏳ Report results

### Success Criteria
- [ ] Calendar events load without error
- [ ] OpenAI adapter initializes successfully
- [ ] AI chat accepts and responds to messages
- [ ] No errors in Metro terminal

---

## 📝 Communication Protocol

### Status Updates
Post in `communication_log.md` when:
- Starting work on a problem
- Finding new information
- Completing a fix
- Need help/blocked

### Format
```markdown
### [AGENT: Name] [TIME: HH:MM]
**Problem:** #1 or #2
**Status:** In Progress / Blocked / Fixed
**Action:** What you did
**Next:** What's next
```

---

## 🔄 Problem Tracking

| Problem | Status | Owner | ETA |
|---------|--------|-------|-----|
| #1 calendar_events | 🔍 Investigating | @Claude | 15 min |
| #2 OpenAI init | 🔍 Investigating | @Claude | 30 min |

---

**Last Updated:** 2025-11-25 17:30 by Claude Code
**Next Update:** After investigation complete
