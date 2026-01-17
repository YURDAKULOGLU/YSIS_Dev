# Mission Task Template: fix_sentinel
Source: scripts/missions/run_fix_sentinel.py (deprecated)

Goal:
Make sentinel verification targeted instead of running full test suite.

Details:
- Modify src/agentic/core/plugins/sentinel.py:
  - Implement smart test discovery based on modified files.
  - If matching tests exist, run pytest on those files only.
  - If no matching tests, run python -m py_compile on modified files and pass with warning.

Verification:
- Add or adjust tests for sentinel targeting logic.
- Ensure protocol_check passes.
