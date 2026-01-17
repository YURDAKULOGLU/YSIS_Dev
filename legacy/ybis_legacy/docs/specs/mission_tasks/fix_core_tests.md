# Mission Task Template: fix_core_tests
Source: scripts/missions/run_fix_core_tests.py (deprecated)

Goal:
Fix broken core tests under tests/ and src/agentic/core/plugin_system/tests/.

Details:
- Common problems to address:
  - Import errors (use src.agentic.core instead of Agentic.Core/Core)
  - Async test setup (pytest-asyncio decorators/config)
  - Mock signature mismatches vs src/agentic/core/protocols.py
- Do not modify legacy/ paths.
- Ensure pytest runs for core test subsets.

Verification:
- Run pytest for targeted core tests.
- Document failures if any remain.
