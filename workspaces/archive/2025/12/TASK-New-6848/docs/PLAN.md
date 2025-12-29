---
id: TASK-New-6848
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-29T15:59:01.736509
target_files:
  - docs/specs/STABILIZATION_PROTOCOL.md
  - docs/EXTERNAL_AGENTS_PIPELINE.md
---

# Task: TASK-DOC-008: Add Constitution Refs to Protocol Docs

## Objective

Add constitutional governance references to two key protocol documents (STABILIZATION_PROTOCOL.md and EXTERNAL_AGENTS_PIPELINE.md) that currently lack any mention of YBIS_CONSTITUTION.md. This ensures all protocol docs explicitly acknowledge their governance foundation.

## Approach

Insert governance alignment sections immediately after the title (line 1) in both files:
1. STABILIZATION_PROTOCOL.md: Add §3 (Execution Protocol) and §4 (Artifacts) reference
2. EXTERNAL_AGENTS_PIPELINE.md: Add constitutional requirements summary for external agents

Both additions will be formatted as blockquotes for visual prominence.

## Steps

1. Read current state of both files (DONE)
2. Update STABILIZATION_PROTOCOL.md
   - Insert governance alignment blockquote after line 1
   - Reference constitution §3 (Execution Protocol) and §4 (Artifacts)
3. Update EXTERNAL_AGENTS_PIPELINE.md
   - Insert constitutional requirements blockquote after line 1
   - List 4 core requirements (single spine, MCP-first, artifacts, verification)
4. Update RUNBOOK.md with actions taken
5. Commit changes with constitutional reference
6. Create completion artifacts
7. Verify with protocol_check.py
8. Complete task

## Risks & Mitigations

**Risk:** Adding governance references might seem redundant to teams familiar with constitution
**Mitigation:** These are high-profile protocol docs read by external agents who may not know constitution exists

**Risk:** Blockquote formatting might conflict with existing document structure
**Mitigation:** Both docs start with markdown headings, blockquotes are valid after title

## Success Criteria

- [ ] Constitution reference added to STABILIZATION_PROTOCOL.md (§3 and §4)
- [ ] Constitutional requirements added to EXTERNAL_AGENTS_PIPELINE.md
- [ ] Blockquote formatting used for visual prominence
- [ ] External agents informed of 4 core requirements
- [ ] Changes committed
- [ ] All artifacts created
- [ ] Protocol check passes

## Constitutional Alignment

This task ensures protocol documentation explicitly acknowledges:
- YBIS_CONSTITUTION.md as supreme governance document
- §3 (Execution Protocol) - workflow requirements
- §4 (Artifacts & Verification) - deliverable requirements
