# Current Active Issues & Feature Backlog
**Date:** 2025-11-30
**Status:** Aligned with official Closed Beta scope.

**Scope Note:** This document tracks active bugs for the Closed Beta and serves as a backlog for future ideas. The definitive plan for the Closed Beta release is `docs/CLOSED_BETA_FINAL_SCOPE.md`. All items not listed as P0/P1 bugs below are considered "Post-Beta".

---

## 🟥 P0 - CRITICAL BUGS (Active)

### 1. Event Creation - Partially Fixed
**Status:** 🟡 PARTIAL (Manual works, AI doesn't)
**What's Broken:** AI cannot create events (tool missing or broken).
**Next Steps:** Investigate `createEvent` tool existence and functionality.
**Assigned:** @ClaudeCode

### 2. i18n Translation Keys - Partially Fixed
**Status:** 🟡 PARTIAL (Still missing keys)
**What's Broken:** Some UI elements still show translation keys instead of text.
**Next Steps:** Comprehensive audit of codebase to find and add all missing keys.
**Assigned:** @ClaudeCode

---

## 🟧 P1 - HIGH PRIORITY BUGS (Active)

### 3. Menu Big Button - Intermittent Bug
**Status:** 🟡 UNSTABLE
**Issue:** The main menu's large button is intermittently unresponsive.
**Needs Investigation:** Event handler timing, z-index, or touch event conflicts.
**Assigned:** @Cursor

### 4. Chat Markdown Rendering Missing
**Status:** 🟡 MISSING FEATURE
**Issue:** AI messages with markdown are not rendered correctly in chat bubbles.
**Solution:** Add a markdown rendering component to chat message bubbles.
**Assigned:** @ClaudeCode

### 5. Flow System Design
**Status:** 🔵 PLANNING
**Issue:** The core "Flows" system needs its architecture finalized. This is a P0 feature for the Beta, making its design a P1 bug/task.
**Needs:** Architecture discussion.
**Assigned:** @Gemini (design) + Team discussion

---

## ✅ RESOLVED BUGS (as of 2025-11-27)

<details>
<summary>View resolved critical bugs...</summary>

### AI Tool Calling - Partial Failures
- **Status:** ✅ RESOLVED (2025-11-27)
- **Fix:** Corrected tool chaining in `useChat.ts`, added IDs to search results, and improved tool descriptions.

### Widget Refresh After AI Operations
- **Status:** ✅ RESOLVED (2025-11-27)
- **Fix:** Implemented `RefreshControl` on Notes and Tasks screens and fixed handler logic.

</details>

---

## 📂 DEFERRED (POST-BETA) FEATURE BACKLOG

*This section contains all feature requests and ideas that are NOT part of the initial Closed Beta scope. They will be reviewed and prioritized after the beta release.*

- **6. Conversations List:** Implement a UI for managing multiple conversation histories.
- **7. Loading States:** Add loading indicators and skeleton screens for async operations.
- **8. Reply from Notifications:** Add action buttons to push notifications.
- **9. Unanswered Item Reminders:** Create a system to resurface unanswered items.
- **10. Wider Widgets:** Redesign home screen widgets to be wider and more content-rich.
- **11. Advanced Calendar Views:** Add Weekly, Monthly, and Yearly calendar views.
- **12. Task Progress Tracking on Calendar:** Visualize completed tasks on the calendar.
- **13. Yearly Data Heat Chart:** Create a GitHub-style contribution chart for tasks.
- **14. Advanced Notification Actions:** Add "Approve", "Postpone" actions to notifications.
- **15. Phone Notification Integration:** Access and filter native phone notifications.
- **16. Mail Integration:** Fetch and prioritize important emails. (**Note:** All Google integrations are deferred post-beta).
- **17. Task Status Enhancement:** Fix bug with task status updates and potentially add more states.
- **18. Flexible Recurring Tasks:** Support for non-fixed schedules (e.g., "twice a week").
- **19. Time-based Tasks:** Add duration tracking to tasks.
- **20. Motivation Mode:** Add gamification, achievements, and streak tracking.
- **21. AI Subtask Suggestions:** Have AI suggest breaking down large tasks.
- **22. Nested Tasks:** Implement task hierarchy (parent-child relationships).
- **23. Note Types:** Add categories for notes (e.g., Person, File).
- **25. Statistics Page:** A dedicated screen for user analytics.
- **26. Journaling Mode:** A dedicated mode for daily journaling and mood tracking.
- **27. Monthly Statistics:** Automated monthly productivity reports.
- **28. Annual Report:** A "Year in Review" summary.
- **29. Google Contacts Integration:** Sync with Google Contacts.
- **30. Broader AI Capabilities:** General request for "everything ChatGPT can do".
- **31. Sound Design:** Add sound effects and audio feedback.
- **32. Custom Themes & Sounds:** Expand theme customization.
- **33. Advanced User Settings:** More granular user preferences.

---

## 🎯 NEXT ACTIONS (Active Sprint)

### Next Up (P1):
- **@Cursor:** Investigate menu button bug (#3).
- **@ClaudeCode:** Add markdown rendering to chat (#4).
- **@Gemini + Team:** Design Flow system (#5).

### Clarification Needed from User:
- **Flows:** What are the most important initial use cases?
- **Widgets:** What data is most important to see on the home screen?
- **Notification Integration:** What permissions are acceptable?
- **Task Flexibility:** What is the desired logic for "at least twice a week"?
- **Statistics:** What are the most important metrics to track?

---
**Last Updated:** 2025-11-30 by @Gemini
**Official Scope Document:** `docs/CLOSED_BETA_FINAL_SCOPE.md`
