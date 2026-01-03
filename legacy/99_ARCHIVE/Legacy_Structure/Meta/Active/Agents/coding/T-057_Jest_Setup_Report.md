# T-057: Jest Setup for React Native Tests

**Agent:** @Codex (Terminal Coder)
**Status:** Completed
**Scope:** Auth login/signup UI tests under Jest runner

## Work Completed
- Stabilized signup screen Jest suite: aligned mocks with `@ybis/ui` global toast, added explicit Expo Haptics mock, and reset mocks per test.
- Removed flaky toast mock that returned `undefined`; now reuse `getGlobalToast()` from the UI mock for expectations.
- Addressed setTimeout-driven navigation in signup tests by waiting for the real 1.5s timer; eliminated overlapping act/waitFor warnings and timeouts.
- Revalidated login test compatibility with updated Jest setup.
- Wired the default `pnpm test`/`test:watch` scripts in `apps/mobile` to run the Jest auth suites so both login + signup run via the standard test entrypoint (without pulling in vitest suites).

## Files Touched
- `apps/mobile/app/(auth)/__tests__/signup.test.tsx` (mock and timer fixes)
- `apps/mobile/app/(auth)/__tests__/login.test.tsx` (execution only to confirm passing)

## Testing
- `pnpm test:jest --runTestsByPath "app/(auth)/__tests__/signup.test.tsx" --runInBand`
- `pnpm test:jest --runTestsByPath "app/(auth)/__tests__/login.test.tsx" "app/(auth)/__tests__/signup.test.tsx" --runInBand`

## Notes
- Jest runner now executes both auth UI suites without act/timeout errors. No changes were made to the production signup/login components.
