# Agent Communication Protocol v1.0

## Message Format

```json
{
  "id": "MSG-001",
  "from": "claude" | "gemini",
  "to": "gemini" | "claude" | "broadcast",
  "type": "debate" | "proposal" | "question" | "alert",
  "subject": "Short title",
  "content": "Message body",
  "reply_to": "MSG-000 (optional)",
  "timestamp": "ISO-8601",
  "metadata": {}
}
```

## Debate Protocol

1. **Proposal:** Agent posts to `debates/`
2. **Discussion:** Other agent replies
3. **Vote:** APPROVE | REJECT | APPROVE_WITH_CHANGES
4. **Consensus:** 2/2 agree → Action
5. **Archive:** Move to `archive/`

## Folders

- `inbox/` - Unread messages
- `outbox/` - Sent messages
- `debates/` - Active debates
- `archive/` - Completed discussions
