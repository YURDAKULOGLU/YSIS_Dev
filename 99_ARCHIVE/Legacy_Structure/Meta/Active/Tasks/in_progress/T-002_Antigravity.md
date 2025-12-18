# Task ID: T-002

- **Description:** Investigate and fix `vitest` parsing error (`Error: Expected 'from', got 'typeOf'`) affecting `packages/database`, `llm`, and `storage`.
- **Type:** Bug Fix
- **Priority:** P0 (Critical)
- **Assigned To:** @Antigravity

## Experiment Log (2025-11-30)

### Baseline
- **Config:** Node v24.11.1, Vitest v2.1.8, Supabase v2.58.0.
- **Result:** CRASH (Exit code 1).

### Experiment 1: Supabase SDK Downgrade
- **Attempt 1:** Downgrade to `v2.39.0`. **Result:** CRASH.
- **Attempt 2:** Downgrade to `v2.0.0`. **Result:** CRASH.
- **Conclusion:** Issue is not specific to recent Supabase SDK versions.

### Experiment 2: Config Tweaks
- **Attempt 1:** `esbuild.target: 'es2022'` + `pool: 'forks'`.

## Scope & Goal
- Tests crash before running; goal is a config/mitigation so tests run on **Node v24** (current env). If impossible, deliver evidence and the safest fallback.

## Current Status
- Tests fail immediately with `Expected 'from', got 'typeOf'` even on a sanity test. Environment: Node v24.11.x.

## Required Outputs
- Minimal repro file + exact command and full stack/output.
- Matrix: Node v24 vs v22/v20 (pass/fail) + relevant tool versions (Vitest/Rollup/esbuild).
- Proposed config-based fix/mitigation for Node v24. If none works, justify why.
- Patch steps (what to change in repo) if a mitigation exists.

## Repro (starting point)
- Create `packages/database/src/__tests__/repro.test.ts`:
  ```ts
  import { createClient } from '@supabase/supabase-js';
  import { describe, it, expect } from 'vitest';
  describe('repro', () => { it('client exists', () => expect(createClient).toBeDefined()); });
  ```
- Run: `pnpm vitest packages/database/src/__tests__/repro.test.ts --runInBand --passWithNoTests=false --reporter=verbose`

## Experiments to Run (log each result)
1) Supabase SDK pin/downgrade: which version fails/passes on Node v24?
2) Vitest/esbuild config tweaks: `esbuild.target` (es2022/esnext), `allowImportingTsExtensions`, `pool: 'forks'`.
3) `server.deps.inline` / `ssr.noExternal` / `optimizeDeps.include` to force transpile of `@supabase/supabase-js`.
4) Full externalize or mock of Supabase (no library parse).
5) Vitest version bump (v2.x) and Rollup/esbuild bumps if relevant.
- [ ] Experiment 5: Vitest Version Bump (Retry) <!-- id: 14 -->
- [x] Document findings in `T-002_Antigravity.md` <!-- id: 15 -->

## Resolution (2025-12-01)
- **Action:** User manually installed **Node.js v20.11.1**.
- **Status:** Downgrade complete.
- **Next Step:** Restart application/terminal to load new PATH and verify fix.

## Constraints
- Aim to make **Node v24** work; do not default to “downgrade Node” without hard evidence. If downgrade is the only path, document why with repro logs.
- Record all attempts in this file; avoid repeating failed knobs.
