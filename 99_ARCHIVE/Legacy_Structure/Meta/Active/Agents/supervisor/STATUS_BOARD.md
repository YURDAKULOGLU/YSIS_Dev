# Status Board (Time-Agnostic)

Use this as the single source of truth for current state. Update anytime there is progress, completion, or a blocker.

---

## 🔴 In Progress

- **T-001 (@Supervisor):** System Restore & Optimization Plan (task-state reconciliation + execution queue).
- **T-002 (@Antigravity):** Vitest parse failure — reopened for root cause + mitigation plan.

---

## ✅ Completed (This Sprint - Nexus)

### Flow Engine V2 - DONE ✅
- **Auto-logout bug fix** - `_layout.tsx` signOut() removed
- **Flow AI Tools (6)** - createFlow, editFlow, toggleFlow, deleteFlow, searchFlows, runFlow
- **queryContext tool** - Enhanced search (notes + tasks + events)
- **Real step handlers** - create_note, create_task, send_notification, create_calendar_event
- **Schedule executor** - Cron parser + interval check (foreground)
- **5 Flow templates** - Morning Routine, Daily Summary, Overdue Reminder, Weekly Planning, Focus Mode
- **Error handling** - console.error → Logger.error (4 files)
- **i18n keys** - flows.* (EN/TR)

### Previous Completions
- **T-003:** AI model landscape research.
- **T-004:** Mobile SmartActionButton touch/position fix.
- **T-005:** Chat Markdown rendering (UI).
- **T-007:** Flows system architecture.
- **T-008:** Supabase BaaS validation layer.
- **T-009:** Backend error handling standardized.
- **T-010:** Test coverage strategy documented.
- **T-015:** Auth onboarding (mobile) delivered.
- **T-016:** Chat markdown + conversations delivered.
- **T-030:** queryRAG/queryContext implemented (moved to done).
- **T-031:** Flow templates completed (moved to done).
- **T-032:** Error handling standardized (moved to done).

---

## 📋 Backlog - DELEGATE TASKS (Çıraklar İçin)

| Task ID | Title | Priority | Complexity | Est. Time |
|---------|-------|----------|------------|-----------|
| **T-050** | Flow List Screen - Template UI | P1 | Easy | 1-2h |
| **T-051** | Google OAuth Callback Handler | P2 | Medium | 2-3h |
| **T-052** | Flow Tools Unit Tests | P2 | Easy-Medium | 2-3h |
| **T-053** | Schedule Executor Tests | P2 | Easy | 1-2h |
| **T-054** | Vitest Config Fix | P3 | Medium | 1-2h |

**Detaylar:** `.YBIS_Dev/ysis_agentic/tasks/backlog/T-05X_*.md`

---

## 🔶 Nexus Remaining (Stratejik)

| Task | Priority | Est. Time |
|------|----------|-----------|
| Flow Builder UI (basit form) | P1 | 2-3h |
| Push Notification entegrasyonu | P2 | 3h |

---

## ⚠️ Open Issues / Blockers

- **Vitest parse failure (T-002):** Prevents running adapter tests.
- **ESLint parserOptions for tests:** Backend test files.

---

## 📌 Notes

- **Closed Beta Scope:** `docs/CLOSED_BETA_FINAL_SCOPE.md`
- **Flow Engine:** Core complete, UI pending
- **BaaS Approach:** Confirmed for Closed Beta (Port architecture enables future migration)
