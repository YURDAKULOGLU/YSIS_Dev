# Codex - Assigned Tasks

Auto-synced from Knowledge/LocalDB/tasks.db. Last updated: 2025-12-27 22:02

## Active Tasks (IN_PROGRESS)

None - All current assignments complete.

Ready for new work! Check backlog or claim UI/docs tasks.

## Watching

### Debates Participating
- DEBATE-20251227211027: Agents-First Onboarding (SUPPORT)
- DEBATE-20251227202311: Graph Viz Architecture (Option B complete)
- DEBATE-20251227202455: Messaging Overhaul (schema implemented)

### Pending Work from Debates
- Messaging cutover cleanup (remove legacy tooling references)
- Dashboard integration for Smart Inbox features
- Agents/ folder documentation polish

## Recently Completed

### NEO-VIZ-001 (COMPLETED)
PROJECT NEO: Visualization strategy for large graphs
- Priority: HIGH
- Deliverables:
  - Vite + React + Sigma.js app (src/dashboard/viz)
  - Standalone architecture (Option B)
  - Ready for Neo4j endpoint integration
- Status: COMPLETED/SUCCESS

### DOC-TOOL-001 (DONE)
Document tool-based protocol + frontmatter standard
- Priority: HIGH
- Updated AI_START_HERE.md and SYSTEM_STATE.md
- Documented tool-based workflow
- Status: DONE

### DOC-DRIFT-001 (DONE)
Onboarding/docs alignment
- Priority: HIGH
- Aligned docs to tasks.db + messaging CLI
- Fixed drift issues
- Status: DONE

## Current Specializations

### Graph Visualization
- src/dashboard/viz/ (Vite + React)
- Sigma.js integration
- Subgraph fetch skeleton
- Performance optimized for 5k+ nodes

### Messaging Infrastructure
- ybis.py message commands (send/read/ack)
- Backward-compatible validation
- MCP integration

### Documentation System
- Agents-First Onboarding support
- Tool-based protocol docs
- Auto-generation scripts

## Standing Responsibilities

- Frontend/UI maintenance
- Documentation accuracy
- Test coverage
- User experience improvements
- Visualization performance

## Task History (Last 7 Days)

2025-12-27: Messaging unification, Graph viz, Docs updates
2025-12-26: [No tasks logged]

How to claim new work:
```bash
python scripts/ybis.py list --status BACKLOG
python scripts/ybis.py claim TASK-ID
```

This file is auto-synced. Manual edits will be overwritten.
