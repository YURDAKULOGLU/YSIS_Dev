# Agent Onboarding Guide

**Welcome to YBIS Week 1 Sprint!** 🚀

This guide will help you get up to speed quickly and start contributing to the team.

---

## 🎯 Quick Start (5 minutes)

### Step 1: Read Core Documents (in order)
1. **This file** (you're here!) - Onboarding overview
2. `README.md` - Workspace structure and rules
3. `SPRINT_STATUS.md` - Current sprint progress
4. `DAILY_STANDUP.md` - Team communication hub

### Step 2: Understand Your Role
Check the **Agent Roles** section in `README.md` to understand your responsibilities:
- **Claude Code:** Implementation, git, testing, debugging
- **Gemini:** Architecture review, full context analysis
- **Cursor:** Multi-file features, composer mode
- **Antigravity:** System operator, orchestrator, troubleshooter

### Step 3: Set Up Your Files
1. Create your status file: `[your-agent]/status.md`
2. Post first update in: `DAILY_STANDUP.md`
3. Check for assigned tasks in: `SPRINT_STATUS.md`

### Step 4: Say Hello!
Post your first message in `communication_log.md`:
```markdown
### [AGENT: YourName] [TIME: YYYY-MM-DDTHH:MM:SS+03:00]
**Status:** Active
**Objective:** [What you're working on]
**Action:** Just joined the team! Reading docs and getting oriented.
```

---

## 📚 Essential Reading (15 minutes)

### Must Read (Priority 1)
These documents are **mandatory** before starting any work:

1. **YBIS Constitution** (30 min read)
   - Location: `docs/YBIS_PROJE_ANAYASASI.md`
   - Why: Contains all technical rules we MUST follow
   - Key Points:
     - Zero-tolerance enforcement (no exceptions)
     - TypeScript strict mode, no `any`, no `@ts-ignore`
     - Port architecture principles
     - ESLint warnings = errors
     - Test coverage ≥80%

2. **Week 1 Sprint Plan** (15 min read)
   - Location: `docs/implementation/WEEK_1_SPRINT_PLAN.md`
   - Why: Our sprint goal and daily breakdown
   - Key Points:
     - Goal: Ship Closed Beta with AI Chat + Context + Tool Calling
     - 7-day timeline (Day 1-2: Context, Day 3: System Prompt, etc.)
     - Success metrics and deliverables

3. **Agent Task Distribution** (10 min read)
   - Location: `docs/AI_Asistan_Gorev_Dagilimi.md`
   - Why: Understand multi-agent workflow
   - Key Points:
     - Which agent does what
     - When to use which agent
     - Coordination patterns

### Should Read (Priority 2)
Read these as you start working:

4. **Development Log** (skim, 10 min)
   - Location: `docs/Güncel/DEVELOPMENT_LOG.md`
   - Why: Architecture decisions (AD-XXX format)
   - What to look for: Recent decisions (AD-015 to AD-020)

5. **Architecture Overview** (20 min read)
   - Location: `docs/Güncel/Architecture_better.md`
   - Why: Understand system design
   - Key Points:
     - Port architecture (DatabasePort, LLMPort, etc.)
     - Package structure
     - Technology choices

6. **Tech Stack** (5 min scan)
   - Location: `docs/Güncel/tech-stack.md`
   - Why: Know what versions we're using
   - Key Points:
     - React 19.1.0, Expo SDK 54, TypeScript 5.7.3
     - Supabase, OpenAI, Tamagui

### Reference Docs (as needed)
Consult these when you need specific information:

7. **Development Guidelines** - `docs/Güncel/DEVELOPMENT_GUIDELINES.md`
8. **Quality Standards** - `docs/codex/004-quality-testing.md`
9. **Package Structure** - `docs/Güncel/package-structure.md`

---

## 🔄 Daily Workflow

### Morning Routine (Every Day)
1. **Check DAILY_STANDUP.md**
   - Read what other agents are doing
   - Check for mentions of your name (@YourName)
   - Look for blockers that might affect you

2. **Post Your Standup**
   ```markdown
   ### [Your Agent Name] (HH:MM)
   **Yesterday:** [What you completed]
   **Today:** [What you'll work on]
   **Blockers:** [None / Issue description]
   **Status:** 🟢 Active
   ```

3. **Check Your Assignments**
   - Look at `SPRINT_STATUS.md` for assigned tasks
   - Check `[your-agent]/status.md` for pending work
   - Review any review requests in `[your-agent]/reviews.md`

### During Work
1. **Update Your Status File** (every 2 hours or on major progress)
   ```markdown
   **Current Task:** [Task name]
   **Progress:** [0-100%]
   **Status:** 🟢 Active / 🔴 Blocked
   ```

2. **Communicate Actively**
   - Post in `communication_log.md` when starting/finishing tasks
   - Tag other agents when you need help: `@Claude`, `@Gemini`
   - Escalate blockers immediately in `shared/blockers.md`

3. **Follow YBIS Rules**
   - TypeScript strict mode always
   - No `any` types (use `unknown` + type guards)
   - No `@ts-ignore` (fix the root cause)
   - ESLint: 0 warnings
   - Test coverage ≥80%

### Before Finishing
1. **Post Completion Update**
   ```markdown
   ### [AGENT: YourName] [TIME: timestamp]
   **Task:** [Task name] ✅ COMPLETED
   **Duration:** [How long it took]
   **Files Changed:** [List files]
   **Next:** [What's next / ready for review]
   ```

2. **Request Review** (if applicable)
   - Update `[your-agent]/reviews.md`
   - Tag reviewer in `DAILY_STANDUP.md`
   - Be specific about what to review

3. **Update SPRINT_STATUS.md**
   - Mark tasks as completed
   - Update progress percentages

---

## 🚦 Quality Gates Checklist

Before requesting review, ensure:

### Code Quality
- [ ] TypeScript: 0 errors (run `npx tsc --noEmit`)
- [ ] ESLint: 0 warnings (run `pnpm lint`)
- [ ] All imports are typed (no implicit `any`)
- [ ] No `console.log` (use `Logger` from `@ybis/logging`)

### Architecture
- [ ] Follows port architecture (no direct vendor imports)
- [ ] UI isolation maintained (use `@ybis/ui`, not `tamagui` directly)
- [ ] Proper error handling (try/catch, error boundaries)
- [ ] Loading states implemented

### Testing
- [ ] Unit tests written (coverage ≥80%)
- [ ] Tests pass locally (run `pnpm test`)
- [ ] Integration tests if applicable
- [ ] Manual testing done

### Documentation
- [ ] Code comments for complex logic
- [ ] JSDoc for public APIs
- [ ] Update relevant docs if architecture changed
- [ ] Add to DEVELOPMENT_LOG.md if architecture decision made

---

## 🛠️ Common Tasks

### How to: Fix TypeScript Errors
```bash
# Check errors
cd apps/mobile
npx tsc --noEmit

# Common fixes:
# 1. Add explicit return types to functions
# 2. Use `unknown` instead of `any`, then type guard
# 3. Add type assertions for JSON responses: `as Promise<Type>`
# 4. Check for undefined: `if (!variable) return;`
```

### How to: Request Code Review
1. Update `[your-agent]/reviews.md`:
   ```markdown
   ## Review Request #1 - [Date] [Time]
   **Task:** [Task name]
   **Reviewer:** @Gemini
   **Priority:** medium

   **Files Changed:**
   - apps/mobile/src/hooks/useUserContext.ts
   - packages/core/src/types/context.ts

   **What Changed:** Implemented user context with realtime sync

   **Testing Done:**
   - [x] Unit tests pass
   - [x] Manual testing done
   - [x] No TypeScript errors

   **Status:** 🟡 AWAITING REVIEW
   ```

2. Tag reviewer in `DAILY_STANDUP.md`:
   ```markdown
   @Gemini - Ready for review: useUserContext hook (#1 in my reviews.md)
   ```

### How to: Report a Blocker
1. Post in `[your-agent]/blockers.md`:
   ```markdown
   ## BLOCKER #1 - [Date] [Time]
   **Task:** Implement realtime subscriptions
   **Issue:** Supabase Realtime not connecting
   **Impact:** Cannot test context updates
   **Tried:** Checked API key, network, subscription syntax
   **Need:** Help debugging Realtime connection
   **Owner:** @Team
   **Priority:** P1 (high)
   **Status:** 🔴 BLOCKED
   ```

2. If it affects sprint: Post in `shared/blockers.md` (same format)

3. If urgent: Tag team in `DAILY_STANDUP.md`:
   ```markdown
   🚨 BLOCKED on realtime subscriptions - need help! See my blockers.md
   ```

### How to: Coordinate with Other Agents
**Before starting work that might overlap:**
1. Check `communication_log.md` - Is someone else working on this?
2. Post your plan:
   ```markdown
   ### [AGENT: YourName] [TIME: timestamp]
   **Action:** Starting work on [feature]
   **Files I'll touch:** [list files]
   **ETA:** [when you'll be done]

   @[Other Agent] - Let me know if this conflicts with your work!
   ```
3. Wait for confirmation before proceeding

**If you discover a conflict:**
1. Stop work immediately
2. Post in `communication_log.md`:
   ```markdown
   ⚠️ CONFLICT DETECTED
   @[Other Agent] - We're both working on [file/feature]
   Proposal: [How to resolve - e.g., "I'll wait for you to finish"]
   ```
3. Use `shared/decisions.md` to document resolution

---

## 📞 Who to Ask for Help

### Architecture Questions
**Ask:** @Gemini (architecture expert)
**Example:** "Should I create a new port or use existing DatabasePort?"

### Code Implementation Help
**Ask:** @Claude (implementation lead)
**Example:** "How do I set up Supabase Realtime subscriptions?"

### Multi-File Refactoring
**Ask:** @Cursor (multi-file expert)
**Example:** "Need to refactor authentication across 10 files"

### Git/PR/Merge Issues
**Ask:** @Claude (git expert)
**Example:** "How do I resolve this merge conflict?"

### General Questions
**Post in:** `DAILY_STANDUP.md` or `communication_log.md`
**Tag:** @Team or specific agent

---

## 🎓 Tips for Success

### DO ✅
- **Communicate early and often** - No surprises
- **Follow YBIS Constitution strictly** - Zero tolerance
- **Update status files regularly** - Keep team informed
- **Ask questions immediately** - Don't waste time stuck
- **Review other agents' work** - Learn and improve together
- **Use proper logging** - `Logger.info()`, not `console.log()`
- **Write tests as you go** - Don't leave for later
- **Check in frequently** - Small commits, continuous integration

### DON'T ❌
- **Don't work in silence** - Team needs to know what you're doing
- **Don't skip quality gates** - No shortcuts on testing/linting
- **Don't use `any` type** - Use `unknown` + type guards
- **Don't use `@ts-ignore`** - Fix the root cause
- **Don't merge without review** - Always get approval
- **Don't assume** - Ask if unclear
- **Don't batch updates** - Update status as you go
- **Don't work on same files without coordination**

---

## 🚀 Ready to Start?

### Your First Day Checklist
- [ ] Read this document
- [ ] Read `README.md`, `SPRINT_STATUS.md`, `DAILY_STANDUP.md`
- [ ] Read YBIS Constitution (mandatory!)
- [ ] Read Week 1 Sprint Plan
- [ ] Create your status file
- [ ] Post first update in DAILY_STANDUP.md
- [ ] Post first message in communication_log.md
- [ ] Check for assigned tasks
- [ ] Set up your local environment (if needed)
- [ ] Run `pnpm install` (if first time)
- [ ] Verify TypeScript: `cd apps/mobile && npx tsc --noEmit`
- [ ] Verify ESLint: `pnpm lint`

### Questions?
Post in `DAILY_STANDUP.md` or `communication_log.md` and tag @Team

---

**Welcome aboard! Let's ship Closed Beta! 🎉**

---

**Last Updated:** 2025-11-25 13:20 by Claude Code
