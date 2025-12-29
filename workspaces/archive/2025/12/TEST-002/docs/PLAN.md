---
id: TEST-002
type: PLAN
status: DRAFT
target_files:
  - tests/integration/test_run_orchestrator_smoke.py
  - workspaces/active/TEST-002/docs/PLAN.md
  - workspaces/active/TEST-002/docs/RUNBOOK.md
  - workspaces/active/TEST-002/artifacts/RESULT.md
  - workspaces/active/TEST-002/META.json
  - workspaces/active/TEST-002/CHANGES/changed_files.json
---
Goal: Add an orchestrator integration smoke test without invoking real LLMs.

Steps:
1. Add integration test that monkeypatches run_orchestrator dependencies.
2. Ensure workspace stubs (PLAN/RESULT) are created during the test.
3. Record status update calls for verification.
4. Document results and verification status in RESULT/META.
