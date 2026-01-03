# Task ID: T-016

- **Title:** Chat Markdown Rendering + Conversations List (mobile/web)
- **Priority:** P0 (visible UX)
- **Assigned To:** @Cursor (UI) + @ClaudeCode (integration)
- **Description:**
  1) Render AI/user messages with Markdown (bold, code, lists, links).
  2) Add conversations list with title + last message preview + new conversation action.
  3) Basic empty/loading/error states for chat and list.

## Acceptance
- Messages render Markdown safely (no raw Markdown text).
- Conversation list shows multiple items; supports create/select; graceful empty state.
- New conversation starts a fresh thread; chat view updates accordingly.
