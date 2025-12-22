# PLAN: T-001 Batch Mobile Supabase Logging

Agent: claude
Started: 2025-12-18

## What & Why

**Problem:** Mobile app currently inserts one Supabase log row per event, causing:
- DDoS risk to Supabase
- Battery drain on mobile devices
- Poor performance

**Solution:** Implement client-side batching with periodic + threshold-based flushing.

## Design Notes (Critical)

### 1. Conservative flush parameters (crash/kill safety)
- ❌ ~~30s interval~~ → ✅ **5-10s** interval (beta-safe)
- ❌ ~~50 logs~~ → ✅ **maxBatch=25-50**
- **Rationale:** Shorter intervals = less log loss on app crash/kill

### 2. App lifecycle flush (best-effort)
- Mobile shutdown/background flush is **NOT guaranteed**
- Mark as "best-effort" in code comments
- **Option:** Persist queue to disk (AsyncStorage/SQLite) for error logs
- Consider: Critical logs (errors) → disk, debug logs → memory-only

### 3. Ordering & concurrency
- Single batch insert preserves order (array order = row order)
- **Real issue:** Prevent concurrent flushes → **single-flight lock**
- Implementation: Use atomic `flushing` flag or mutex

### 4. Robust failure handling
- ✅ Drop oldest when queue cap hit
- ✅ **Backoff + jitter** for Supabase rate limits (exponential retry)
- ✅ **Max payload size** check (Supabase row/batch limits)
- Consider: Separate error queue with higher retention

### 5. Testability & architecture
- If unit testing is hard, **first refactor:**
  - Extract queue/flush logic → pure functions
  - Separate transport layer (dependency injection)
  - `SupabaseSink` becomes thin adapter over reusable `BatchQueue`
- Enables: mock transport, deterministic tests, dry-run mode

## Testing Requirements (CONTRACT §5.2 - MANDATORY)

**Before moving to `done/`:**

1. ✅ Search for existing tests: `apps/mobile/src/logging/__tests__/` or `*.test.ts`
2. ✅ Create tests if none exist:
   - `supabase-sink.test.ts` (or similar)
   - `batch-queue.test.ts` (for pure BatchQueue logic)
3. ✅ Minimum coverage:
   - Happy path: batching works, flush triggers correctly
   - Failure cases: queue cap hit, network error, concurrent flush prevented
4. ✅ Run `pnpm test:all` → ALL must pass
5. ✅ Run `pnpm typecheck` → must pass
6. ✅ Document test results in RUNBOOK.md

**Tests must exist and pass before task completion.**

## Steps

1. Read current implementation: `apps/mobile/src/logging/supabase-sink.ts`
2. Search for existing tests: `apps/mobile/src/logging/__tests__/` or nearby `*.test.ts`
3. Design batching queue architecture (separate transport layer for testability)
4. Implement core BatchQueue (pure functions):
   - In-memory queue for log events
   - Time-based flush: **5-10s** interval
   - Count-based flush: **maxBatch=25-50**
   - Single-flight lock (prevent concurrent flushes)
5. Implement SupabaseSink adapter:
   - Dependency injection for transport
   - Best-effort app shutdown/background flush
   - Optional: AsyncStorage persistence for error logs
6. Add robust failure handling:
   - Queue cap + drop oldest
   - Exponential backoff + jitter
   - Max payload size validation
7. **Write unit tests** (MANDATORY):
   - Test BatchQueue logic with mock transport
   - Test SupabaseSink integration
   - Dry-run mode for manual verification
8. **Run verification gates:**
   - `pnpm test:all` (must pass)
   - `pnpm typecheck` (must pass)
   - `ybis-dev verify` (must pass)
9. Verify typical session produces batched inserts (manual check)

## Scope
- Allowed writes: `apps/mobile/**`
- Primary file: `apps/mobile/src/logging/supabase-sink.ts`

## Acceptance Criteria
- Batched inserts (not hundreds of individual requests)
- Safe failure modes (queued logs with cap)
- Unit test or dry-run mode
