# MCP Messaging Cutover Plan

## Goal
Complete the migration from file-based messaging to MCP messaging (`scripts/ybis.py message ...`) and remove legacy tooling.

## Phase 0 - Prep (Done)
- MCP messaging tools exist in `src/agentic/mcp_server.py`.
- `scripts/ybis.py message` is available.
- File-based messaging is now archive-only.

## Phase 1 - Cutover (Done)
- `scripts/msg_tool.py` removed.
- Agents send/read/ack via `scripts/ybis.py message`.

## Phase 2 - Archive Only (Now)
- `Knowledge/Messages/` remains for historical reference.
- No new messages should be written to file inbox/outbox.

## Phase 3 - Clean-Up (Next)
- Remove remaining doc references to msg_tool.
- Ensure debates use MCP message type or dedicated MCP debate tools (if added).

## Success Criteria
- All active agents can send/read/ack via MCP.
- No new messages written to `Knowledge/Messages/inbox` during Phase 2+.
- Agents confirm that ack flow is visible to senders.

## Rollback
- Reintroduce a legacy CLI only if MCP tools are unavailable.
- Keep MCP tools live; treat file-based as last-resort fallback.
