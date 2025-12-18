# General Software Quality Standards

These are the universal engineering standards applicable to all code written within this environment.

## 1. Type Safety & Reliability
- **Strict Typing:** Never use `any` in TypeScript. Use `unknown` with type guards or specific interfaces.
- **Error Handling:** Never swallow errors silently. Always log or propagate them.
- **Null Safety:** Always handle `null` and `undefined` cases explicitly.

## 2. Code Structure & Style
- **DRY (Don't Repeat Yourself):** Extract common logic into utils or hooks.
- **Single Responsibility:** A function should do one thing. A file should have one main purpose.
- **Descriptive Naming:** Variable names must be descriptive (`userCount` vs `n`).
- **Comments:** Comment *why* complex logic exists, not *what* the code does (code should be self-documenting).

## 3. Testing
- **Unit Tests:** Business logic must have unit tests.
- **Integration Tests:** Critical flows must be tested together.
- **Mocking:** External dependencies (API, DB) must be mocked in tests.

## 4. Performance
- **Cleanups:** Always unsubscribe from listeners/observers in `useEffect` or cleanup functions.
- **Efficiency:** Avoid nested loops (O(n^2)) on large datasets unless necessary.
