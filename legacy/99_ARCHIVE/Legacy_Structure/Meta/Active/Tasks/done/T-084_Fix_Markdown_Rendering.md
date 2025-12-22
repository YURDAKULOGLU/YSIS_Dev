---
type: bug
priority: low
status: backlog
assignee: @Coding
---

# Fix Markdown Rendering (Tables & Strikethrough)

**Description:**
Chat messages containing Markdown tables or strikethrough text are not rendered correctly.

**Symptoms:**
- Strikethrough (`~~text~~`) appears as raw text.
- Tables (`| col | col |`) appear as raw text or broken layout.
- Log indicates `[API_CALL]` stops abruptly after markdown content (potentially related to rendering crash or log truncation, though user says logs stop).

**Root Cause Hypothesis:**
- `react-native-markdown-display` styles/rules for `table` and `s` (strikethrough) are missing or overridden.
- Message bubble container might be cutting off wide content (tables).

**Acceptance Criteria:**
- [ ] `~~strikethrough~~` renders with a line through the text.
- [ ] Markdown tables render legibly (scrollable if needed).
- [ ] Rendering complex markdown does not crash the list or stop logging.
