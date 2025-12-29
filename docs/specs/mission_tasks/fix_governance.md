# Mission Task Template: fix_governance
Source: scripts/missions/run_fix_governance.py (deprecated)

Goal:
Inject the constitution into planning prompts to enforce governance.

Details:
- Update src/agentic/core/plugins/simple_planner.py:
  - Add _read_constitution() helper.
  - Include constitution text in plan prompt under "SYSTEM CONSTITUTION (MUST FOLLOW)".
  - Provide fallback string if constitution file missing.

Verification:
- Unit test for prompt composition.
- protocol_check passes.
