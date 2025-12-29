---
id: TASK-New-3354
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-29T17:10:21.454702
target_files:
  - docs/governance/YBIS_CONSTITUTION.md
  - examples/RUNBOOK.sh (new)
---

# Task: TASK-GOV-SLIM-003: RUNBOOK command-only format

## Objective

Eliminate prose from RUNBOOK.md to reduce token waste. Convert to pure command list format. Add optional executable RUNBOOK.sh/ps1 scripts for replay/verification.

Current RUNBOOK prose wastes ~300 tokens with narrative text. Command-only format: ~50 tokens.

## Approach

1. Define new RUNBOOK.md format spec (command-only, no prose)
2. Add optional RUNBOOK.sh format spec (executable with exit codes)
3. Update constitution §4 with new format requirements
4. Create example templates

## Steps

1. Update YBIS_CONSTITUTION.md §4:
   - Document RUNBOOK.md format: command list only (bash code block)
   - Document optional RUNBOOK.sh format (executable, exit codes)
   - Specify when to use each format
2. Create example template: `examples/RUNBOOK.sh`
   - Shebang, set -e, commands with || exit codes
   - Self-documenting via comments
3. Create this task's RUNBOOK in new format
4. Commit changes
5. Verify new format works

## Risks & Mitigations

**Risk:** Existing RUNBOOKs with prose become non-compliant
**Mitigation:** Grandfather clause - new format applies to new tasks only

**Risk:** Loss of context without prose
**Mitigation:** Git commit messages provide context. RESULT.md has rationale.

**Risk:** RUNBOOK.sh might not work cross-platform
**Mitigation:** Make it optional. Provide both .sh and .ps1 templates.

## Success Criteria

- [ ] Constitution §4 updated with command-only RUNBOOK spec
- [ ] Optional RUNBOOK.sh format documented
- [ ] Example template created (examples/RUNBOOK.sh)
- [ ] This task's RUNBOOK follows new format
- [ ] Changes committed
- [ ] Token savings verified (300 → 50 tokens)

## Token Impact

**Current RUNBOOK:** ~300 tokens (prose + commands)
**Command-only:** ~50 tokens (just commands)
**Savings:** 250 tokens/task × 75% of tasks = **massive savings**
