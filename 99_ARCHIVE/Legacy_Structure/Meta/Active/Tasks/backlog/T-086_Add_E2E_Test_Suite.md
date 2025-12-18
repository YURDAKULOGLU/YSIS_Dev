## Title
Add minimal E2E test suite for mobile + API

## Description
Set up an automated end-to-end test harness covering the critical happy paths for the 0.1.0 app: mobile login, flows run/activate, and logout, plus backend API sanity (auth + LLM). Choose appropriate tools (Detox for mobile, Playwright for API) and integrate into CI.

## Acceptance Criteria
- Test runner/tooling chosen and scaffolded (Detox for mobile; Playwright for API is acceptable).
- Happy-path scenarios automated: login, create/run flow, verify output rendered, manual trigger run, logout.
- Backend API smoke: auth, /llm/chat or /llm/generate, and a flow execution endpoint respond successfully with assertions.
- Tests run headlessly in CI with documented commands/env vars.
- Failing E2E blocks the pipeline for regressions.

## Notes
- Target is post-0.1.0; keep lightweight to avoid blocking release.
- Reuse existing test users/fixtures; avoid hitting production data.
