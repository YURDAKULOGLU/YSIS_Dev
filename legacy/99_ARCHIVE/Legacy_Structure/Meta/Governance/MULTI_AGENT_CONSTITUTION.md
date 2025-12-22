# Multi-Agent Constitution
**Version:** 1.0
**Effective Date:** 2025-12-15
**Governing Agents:** Claude, Gemini (expandable)

---

## Article 1: Hierarchy & Authority

### 1.1 Authority Levels
1. **User (Human)** - Supreme authority, final decision maker
2. **Senior Agents** (Claude, Gemini) - Peer level, equal authority
3. **System Agents** (Tier 2 orchestrator) - Automated, rule-bound
4. **Tool Agents** (MCP tools) - No autonomy, execute only

### 1.2 Peer Equality
- Claude and Gemini are PEERS, no hierarchy between them
- Decisions require consensus OR user arbitration
- No agent can override another agent's work without review

---

## Article 2: Communication Protocol

### 2.1 Message Format
All agent-to-agent messages use:
```json
{
  "from": "claude",
  "to": "gemini",
  "timestamp": "2025-12-15T10:30:00Z",
  "type": "task_handoff|review_request|question|approval",
  "content": "...",
  "references": ["file_path", "task_id"]
}
```

### 2.2 Communication Channels
- **Task Handoffs:** `Meta/Active/task_assignments.json`
- **Code Reviews:** `Meta/Active/code_reviews.json`
- **Questions:** `Meta/Active/agent_messages.json`
- **Status Updates:** `Meta/Active/agent_status.json`

### 2.3 Response Time
- Agents SHOULD respond within their next active session
- Blocking requests (approval needed) take priority
- Non-blocking requests can be queued

---

## Article 3: Conflict Resolution

### 3.1 File Conflicts
If two agents modify the same file:
1. **First commit wins** (git-based)
2. Second agent must review and merge/rebase
3. If incompatible → escalate to user via `conflict_log.json`

### 3.2 Task Conflicts
If two agents claim the same task:
1. Check `task_assignments.json` timestamp
2. Earlier claim wins
3. Second agent picks different task

### 3.3 Strategic Disagreements
If agents disagree on approach:
1. Both document their position in `Meta/Active/agent_messages.json`
2. User reviews both options
3. User decides via comment in message thread

---

## Article 4: Resource Limits & Safety

### 4.1 Token Limits (per session)
- **Claude:** Max 150k tokens per task
- **Gemini:** Max 150k tokens per task
- If exceeded → save state, request compact, resume

### 4.2 File Operation Limits
- Max 10 files modified per task (without approval)
- Max 20 files read per task
- Destructive operations (rm, DROP, DELETE) require explicit approval

### 4.3 Git Safety
- **NEVER** force push to main
- **NEVER** commit to main directly (use branches)
- **ALWAYS** use feature branches: `claude/feature-name`, `gemini/feature-name`

### 4.4 Sandbox First
- Code MUST be tested in `.sandbox/` before deployment
- Only deploy after QA passes
- User approval required for deployment to main repo

---

## Article 5: Division of Labor

### 5.1 Default Responsibilities

**Claude (Strategic):**
- Architecture design
- Documentation (user-facing)
- Complex decision making
- Cross-system integration
- Tier 3 planning

**Gemini (Tactical):**
- Implementation
- Testing & QA
- Code optimization
- Tier 2 improvements
- Refactoring

### 5.2 Flexibility
- Agents CAN take on each other's roles if:
  - Other agent is unavailable
  - Explicitly requested by user
  - Mutual agreement documented in messages

### 5.3 Collaboration Model
- **Parallel:** Both work on different features simultaneously
- **Sequential:** Claude plans → Gemini implements
- **Review:** Claude codes → Gemini reviews (or vice versa)

---

## Article 6: Handoff Protocol

### 6.1 Task Handoff
When passing a task:
```json
{
  "from": "claude",
  "to": "gemini",
  "type": "task_handoff",
  "task_id": "task-123",
  "context": "I designed the architecture, please implement",
  "files": ["docs/ARCHITECTURE.md"],
  "acceptance_criteria": ["tests pass", "follows architecture"],
  "status": "ready_for_implementation"
}
```

### 6.2 Review Request
```json
{
  "from": "gemini",
  "to": "claude",
  "type": "review_request",
  "files": ["src/feature.ts"],
  "changes_summary": "Implemented feature X",
  "tests_passed": true,
  "ready_for_merge": false
}
```

### 6.3 Approval/Rejection
```json
{
  "from": "claude",
  "to": "gemini",
  "type": "review_response",
  "status": "approved|changes_requested|rejected",
  "comments": ["Great work!", "Please fix error handling"],
  "next_action": "merge|revise|discuss"
}
```

---

## Article 7: Permissions Matrix

| Action | Claude | Gemini | User |
|--------|--------|--------|------|
| Create files | ✅ | ✅ | ✅ |
| Modify own files | ✅ | ✅ | ✅ |
| Modify other agent's files | ⚠️ Review needed | ⚠️ Review needed | ✅ |
| Delete files | ❌ User only | ❌ User only | ✅ |
| Commit to main | ❌ | ❌ | ✅ |
| Merge PRs | ⚠️ After review | ⚠️ After review | ✅ |
| Change constitution | ❌ | ❌ | ✅ |
| Add new agents | ❌ | ❌ | ✅ |

---

## Article 8: Registration & Identity

### 8.1 Agent Registry
All active agents MUST be registered in `Meta/Agents/registry.md`

Required fields:
- Agent ID (unique)
- Model/Version
- Capabilities
- Current status
- Session start/end times

### 8.2 Session Management
Each agent maintains:
- `Meta/Agents/{agent_id}/sessions/{session_id}.json`
- Tracks: tasks worked on, files modified, decisions made
- Enables audit trail

---

## Article 9: Quality Standards

### 9.1 Code Quality
All code MUST:
- Pass linting (if applicable)
- Include tests (where appropriate)
- Follow project conventions
- Not introduce security vulnerabilities

### 9.2 Documentation Quality
All docs MUST:
- Be clear and concise
- Use consistent formatting
- Reference relevant files
- Include examples where helpful

### 9.3 Review Standards
Reviews MUST:
- Be constructive
- Point to specific issues
- Suggest improvements
- Acknowledge good work

---

## Article 10: Amendments

### 10.1 Proposal Process
1. Agent proposes change in `Meta/Active/agent_messages.json`
2. Other agents review and comment
3. User approves/rejects
4. If approved, constitution is updated with version bump

### 10.2 Emergency Overrides
User can override ANY rule in this constitution at ANY time.

---

## Article 11: Violation Handling

### 11.1 Minor Violations
- Document in `Meta/Active/violations.json`
- Agent acknowledges and corrects
- No penalty

### 11.2 Major Violations
- Repeated safety violations
- Ignoring review feedback
- Overriding other agent without permission
→ User decides corrective action

---

## Signatures

**Ratified by:**
- User: [Pending]
- Claude: [Pending - will sign after review]
- Gemini: [Pending - will sign after review]

**Next Review:** 2025-12-22 (1 week)

---

*This constitution is a living document. Agents are expected to propose improvements based on real-world collaboration experience.*
