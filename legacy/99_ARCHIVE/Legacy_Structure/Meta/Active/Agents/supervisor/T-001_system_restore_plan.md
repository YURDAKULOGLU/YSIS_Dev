# Task T-001 — System Restore & Optimization Plan

## Goal
Stabilize the agentic workflow, clear task-state drift, and queue critical execution work so build/test health can be restored quickly.

## Current Snapshot (observed)
- Task state drift: backlog still contains tasks already marked done (T-004, T-005, T-008, T-009, T-010, T-015/016), and T-002 exists in both `done/` (WONTFIX) and `in_progress/` (reopened).
- Blockers: Vitest parse failure (`Expected 'from', got 'typeOf'`) still open; ESLint parserOptions warning on backend tests noted on STATUS_BOARD.
- Ready work: Conversations list architecture delivered (`agents/research/CONVERSATION_HISTORY_ARCHITECTURE.md`); needs implementation. Documentation homogenization plan waiting for summaries/validators.

## Immediate Actions (today)
1) **Task hygiene (@Supervisor)**: Reconcile backlog vs done vs in_progress to remove dupes and reflect real state; ensure STATUS_BOARD matches directories.
2) **Vitest parse blocker (@Antigravity)**: Reproduce in a minimal test in `packages/database`; capture full stack; propose fix or mitigation (transpile Supabase SDK, version pin, or mocks). Update task file with findings.
3) **Conversations list impl (@ClaudeCode + @Cursor)**: Start T-006 implementation using existing architecture doc; deliver minimal create/select/delete with empty/loading/error states.
4) **Auth/test lint issue (@Cursor)**: Triage ESLint parserOptions complaint in `apps/backend/src/middleware/__tests__/auth.test.ts` and push config fix.

## Short-Term Queue (next)
- **Performance check (T-011, @Cursor)**: Verify bundle size + asset optimization; propose top 3 wins.
- **Rate limiting (T-012, @ClaudeCode)**: Add API rate limiter (e.g., `hono-rate-limiter`) with safe defaults and env toggles.
- **Docs homogenization (T-013/T-014, @Automation → @ClaudeCode)**: Phase 1 add YAML frontmatter; Phase 2 validators (`validate-frontmatter.ts`, `check-doc-links.ts`) and CI wiring.
- **Plan summary (T-015, @Gemini)**: Summarize `DOCUMENTATION_HOMOGENIZATION_PLAN.md` for quick consumption.

## Process Guardrails
- Keep `tasks/` directories single-source-of-truth (one location per task ID); update STATUS_BOARD on each state change.
- For reopened tasks (e.g., T-002), mark prior WONTFIX context in the in-progress file to avoid history loss.
- Store agent outputs under their role directories; prefer summaries for large docs per efficiency protocols.

## Deliverables Checklist
- [ ] Task directory reconciliation done
- [ ] STATUS_BOARD updated
- [ ] T-002 reproduction notes captured
- [ ] T-006 implementation underway
