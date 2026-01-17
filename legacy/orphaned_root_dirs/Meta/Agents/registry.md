# Agent Registry

**Last Updated:** 2025-12-15

---

## Active Agents

### Claude (claude-sonnet-4-5)
- **ID:** `claude`
- **Model:** Claude Sonnet 4.5 (claude-sonnet-4-5-20250929)
- **Role:** Strategic Planning, Architecture, Documentation
- **Status:** Active
- **Session Start:** 2025-12-15
- **Capabilities:**
  - Architecture design
  - Strategic planning
  - Multi-language coding
  - Documentation writing
  - Cross-system reasoning
- **Limitations:**
  - Token limit: 200k per session
  - Cannot execute code locally
  - Read-only file system access (via tools)
- **Contact:** Via CLI (primary interface)

---

### Gemini (pending registration)
- **ID:** `gemini`
- **Model:** TBD (to be specified by user)
- **Role:** Implementation, Testing, Optimization
- **Status:** Pending activation
- **Session Start:** TBD
- **Capabilities:** TBD
- **Limitations:** TBD
- **Contact:** Via CLI

---

## Inactive Agents

None

---

## Agent Addition Protocol

To add a new agent:
1. User creates agent profile in `Meta/Agents/{agent_id}/profile.json`
2. User defines permissions in `Meta/Agents/{agent_id}/permissions.json`
3. Agent reads and signs MULTI_AGENT_CONSTITUTION.md
4. Agent added to this registry
5. Other agents notified via `agent_messages.json`

---

## Session Log

| Agent | Session ID | Start Time | End Time | Tasks Completed |
|-------|------------|------------|----------|-----------------|
| claude | session-001 | 2025-12-14 | ongoing | Tier 1-2 setup, Multi-agent framework |

---

*This registry is automatically updated as agents join/leave the system.*
