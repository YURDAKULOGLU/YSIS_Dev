# YBIS Dev MVP Contract (Agent-Agnostic)

This is the minimal “shared contract” that all CLI agents (Codex/Cursor/Claude/Gemini/etc) must follow when operating in `.YBIS_Dev`.

The goal is consistency: same inputs, same outputs, same safety boundaries, same artifacts.

---

## 1) Scope & Boundaries

### Allowed write scope (default)
- ✅ Write freely under `.YBIS_Dev/**`
- ❌ Do not write to `apps/**`, `packages/**`, `docs/**` unless the task explicitly grants it.
- ❌ Never touch `.git/**`

### Runtime state policy
- Runtime artifacts must go to `.YBIS_Dev/.sandbox/**` or `.YBIS_Dev/.sandbox_hybrid/**`
- Knowledge base state (if any) must go to `.YBIS_Dev/40_KNOWLEDGE_BASE/**`

### No local DB / no “agent memory services” (MVP constraint)
For the MVP pipeline, do **not** rely on local databases (Chroma/SQLite/Redis) or background daemons.
All coordination and memory must be expressed as plain files:
- task files under `.YBIS_Dev/Meta/Active/Tasks/**`
- artifacts under `.YBIS_Dev/.sandbox_hybrid/<TASK_ID>/**`
- handoffs under `.YBIS_Dev/Meta/Active/communication_log.md`

---

## 2) Single Source of Tasks

All tasks live in:
- `.YBIS_Dev/Meta/Active/TASK_BOARD.md`

No other ad-hoc task queues are “authoritative”.

---

## 3) Standard Task Format

Each task must be a markdown checklist item and include:
- `ID` (unique)
- `Title`
- `Scope` (where writes are allowed)
- `Acceptance` (how to verify)

Example:
```
- [ ] T-001: Fix `.YBIS_Dev` import drift
  Scope: .YBIS_Dev/**
  Acceptance: `ybis-dev verify` passes; `ybis-dev mcp --dry-run` succeeds
```

---

## 4) Mandatory Artifacts Per Task

For each executed task, generate artifacts under:
- `.YBIS_Dev/.sandbox_hybrid/<TASK_ID>/` (preferred)
  - `PLAN.md` (what/why)
  - `RUNBOOK.md` (commands run, in order)
  - `DECISIONS.json` (versions/options chosen)
  - `STATE_SNAPSHOT.json` (minimal state: inputs/outputs, hashes, timestamps)
  - `RESULT.md` (what changed, what remains, risks)

If `.sandbox_hybrid` is not used, use `.YBIS_Dev/.sandbox/<TASK_ID>/` with same filenames.

---

## 5) Verification & Testing ("Gates")

Every task must end with verification steps:

### 5.1) Base verification (always required)
- `ybis-dev verify` (required for all tasks)

### 5.2) Code changes (STRICT - if task touches `apps/**`, `packages/**`)

**MANDATORY steps before marking task as done:**

1. **Search for existing tests:**
   - Find test files for modified code: `*.test.ts`, `*.test.tsx`, `*.spec.ts`, `__tests__/`

2. **If no test exists → CREATE ONE:**
   - Write test file following repo patterns
   - Minimum coverage: happy path + one failure case
   - Document test file path in RESULT.md

3. **Run full test suite:**
   ```bash
   pnpm test:all
   ```
   - **ALL tests MUST pass** (zero exceptions)
   - Document results in RUNBOOK.md

4. **Additional checks (when applicable):**
   - `pnpm typecheck` (if TypeScript changes)
   - `pnpm lint` (if applicable)

**No task can move to `done/` without:**
- ✅ All tests passing (`pnpm test:all`)
- ✅ Test coverage for new/changed code
- ✅ `ybis-dev verify` passing

---

## 6) File/Path Safety

Agents must never create files or folders with:
- newlines in names
- markdown code-fences (```) in names
- leading/trailing whitespace

If an output contains such characters, it must be sanitized before writing.
