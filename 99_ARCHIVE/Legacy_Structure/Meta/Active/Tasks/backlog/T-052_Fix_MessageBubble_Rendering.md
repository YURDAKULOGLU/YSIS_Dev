---
type: task
status: backlog
priority: medium
assignee: "@ClaudeCode"
proposal: "P-001"
---

# T-052: Fix MessageBubble HTML & Markdown Rendering

## Objective
Fix the `MessageBubble` component to correctly render HTML entities and standard Markdown elements (lists, bold).

## Context
The current `MarkdownRenderer` uses `marked` but lacks a handler for HTML tokens, causing broken display (e.g., `&quot;`).

## Requirements

### 1. Add Dependency
- [ ] Add `react-native-render-html` to `packages/chat/package.json`.

### 2. Update Renderer
- [ ] Modify `packages/chat/src/MarkdownRenderer.tsx`:
    - Import `RenderHTML`.
    - Handle `html` tokens from `marked` using `RenderHTML`.
    - Ensure styles (color, font) match the theme.

## Acceptance Criteria
- [ ] HTML entities (e.g., `&quot;`, `&lt;`) render correctly.
- [ ] Markdown lists (`- item`) render as bullet points.
- [ ] Bold text (`**text**`) renders bold.
- [ ] Strikethrough text (`~~text~~`) renders with line-through.
- [ ] Markdown tables render legibly (scrollable if needed).
