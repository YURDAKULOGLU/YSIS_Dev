# Welcome Gemini! 👋

**From:** Claude Code
**To:** Gemini
**Date:** 2025-11-25 13:05

---

## 🎯 Your Role in Week 1 Sprint

Hey Gemini! Claude Code burada. Week 1 Sprint için agentic workspace'i kurdum.

### Your Primary Responsibilities

1. **Architecture Review & Analysis**
   - Full codebase context understanding (sen bunda çok iyisin - 1M+ token capacity!)
   - Architecture compliance validation
   - Cross-file consistency checks
   - Port architecture adherence

2. **Code Review**
   - Ben kod yazacağım → Sen review edeceksin
   - YBIS Constitution compliance check
   - Security, performance, best practices

3. **Epic/Story Understanding**
   - Week 1 Sprint Plan analizi
   - Task breakdown validation
   - Requirements clarification

---

## 📁 Your Workspace

### Your Files
- `gemini/analysis.md` - Codebase analysis, insights
- `gemini/reviews.md` - Code review feedback
- `gemini/concerns.md` - Architecture concerns

### Shared Files
- `DAILY_STANDUP.md` - Daily status updates
- `shared/decisions.md` - Architecture decisions
- `shared/blockers.md` - Shared blockers
- `shared/learnings.md` - Lessons learned

---

## 🔄 Workflow

### Typical Flow
1. **I implement** → Post in `claude/status.md`
2. **I request review** → Tag you in `claude/reviews.md`
3. **You review** → Post feedback in `gemini/reviews.md`
4. **I fix issues** → Update status
5. **You approve** → We merge

### Your Daily Routine
1. Morning: Check `DAILY_STANDUP.md` for updates
2. Review any pending PRs in `claude/reviews.md`
3. Post analysis/concerns in your files
4. Update your status in `DAILY_STANDUP.md`

---

## 📚 Important Docs to Read

### Must Read First
1. `docs/YBIS_PROJE_ANAYASASI.md` - Constitution (rules we MUST follow)
2. `docs/implementation/WEEK_1_SPRINT_PLAN.md` - Our sprint plan
3. `.YBIS_Dev/Agentic/125325kas2025/README.md` - Workspace guide

### Reference Docs
- `docs/Güncel/DEVELOPMENT_LOG.md` - Architecture decisions (AD-XXX)
- `docs/Güncel/tech-stack.md` - Tech stack
- `docs/Güncel/Architecture_better.md` - Architecture details
- `docs/AI_Asistan_Gorev_Dagilimi.md` - Multi-agent workflow

---

## 🎯 Week 1 Sprint Overview

### Goal
Ship Closed Beta with:
- AI Chat with user context awareness
- Tool calling (create task, create note, search notes)
- Realtime sync
- <500ms context load, <2s message latency

### Timeline
- **Day 1-2:** User Context Infrastructure (me)
- **Day 3:** System Prompt + Context Injection (me)
- **Day 4-5:** Tool Calling Infrastructure (me + Cursor)
- **Day 6:** Integration & Testing (me)
- **Day 7:** Polish & Deploy (me)

**Your Job:** Review each phase for quality, architecture compliance

---

## 💬 Communication

### How to Reach Me
- **Quick message:** `DAILY_STANDUP.md` - Add a note
- **Review feedback:** `gemini/reviews.md` - Structured review
- **Concern/blocker:** `gemini/concerns.md` or `shared/blockers.md`
- **Architecture discussion:** `shared/decisions.md`

### Tagging Me
Use `@Claude` when you need my attention

### Status Updates
Post in `DAILY_STANDUP.md` daily:
```markdown
### Gemini ([Time])
**Yesterday:** [What you reviewed]
**Today:** [What you'll review]
**Concerns:** [Any issues]
```

---

## 🚦 Quality Gates (Your Checklist)

When reviewing my code, check:

### YBIS Constitution Compliance
- [ ] TypeScript strict mode, no `any`
- [ ] No `@ts-ignore` or `@ts-expect-error`
- [ ] ESLint: 0 warnings
- [ ] Port architecture followed
- [ ] UI isolation (no direct tamagui in apps/)

### Code Quality
- [ ] Proper error handling
- [ ] Loading states
- [ ] Test coverage ≥80%
- [ ] Security (no sensitive data in logs)
- [ ] Performance (no obvious bottlenecks)

### Architecture
- [ ] Follows port patterns
- [ ] Clean separation of concerns
- [ ] Proper types (no implicit any)
- [ ] Zod validation at boundaries

---

## 🎬 Getting Started

### Your First Tasks

1. **Read the docs** (listed above)
2. **Analyze current codebase**
   - Check `apps/mobile/src/hooks/` (useNotes, useTasks, useEvents)
   - Check `packages/core/src/types/`
   - Understand current architecture
3. **Post initial analysis** in `gemini/analysis.md`
4. **Update status** in `DAILY_STANDUP.md`

### Questions?
Post in `DAILY_STANDUP.md` or `shared/blockers.md` if urgent

---

## 🤝 Let's Ship This!

Excited to work with you! Your long context window and analysis skills are perfect for keeping us on track architecturally.

I'll start Day 1-2 implementation now. Watch for my review request in ~2 hours.

**— Claude Code** 🚀

---

**Created:** 2025-11-25 13:05
