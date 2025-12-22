# Architectural Decision Records (ADR)

**Purpose:** Log of all key architectural and process decisions made in the "Meeting Room".

## Template
```markdown
### [ADR-00X] Title
**Date:** YYYY-MM-DD
**Status:** PROPOSED / ACCEPTED / REJECTED
**Context:** [Why are we making this decision?]
**Decision:** [What did we decide?]
**Consequences:** [What are the trade-offs?]
```

---

## Decisions

### [ADR-001] Agentic Workspace Structure
**Date:** 2025-11-25
**Status:** ACCEPTED
**Context:** Need a standard way for agents to coordinate.
**Decision:** Use `.YBIS_Dev/Agentic` with `communication_log.md` and `TASK_BOARD.md`.

### [ADR-002] Meeting Room Protocol
**Date:** 2025-11-26
**Status:** ACCEPTED
**Context:** Need a space for high-level discussion separate from execution logs.
**Decision:** Use `### [MEETING]` tag in `communication_log.md` and Antigravity as moderator.
