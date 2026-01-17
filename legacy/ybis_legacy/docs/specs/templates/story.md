---
id: story-template
title: User Story
version: 1.0
---

# Story: {{STORY_TITLE}}

**Status:** Draft | Approved | InProgress | Done
**Owner:** @{{ASSIGNEE}}
**Epic:** [[{{EPIC_LINK}}]]

## 1. Context
> **Why are we doing this?**
> {{CONTEXT_DESCRIPTION}}

**Related Files:**
- `{{FILE_PATH_1}}`
- `{{FILE_PATH_2}}`

## 2. Requirements (The "Spec")
*   [ ] **Req 1:** {{REQUIREMENT_1}}
*   [ ] **Req 2:** {{REQUIREMENT_2}}

## 3. Implementation Plan (Step-by-Step)
1.  [ ] Modify `{{FILE_1}}`:
    *   Add function `{{FUNCTION_NAME}}`.
2.  [ ] Create `{{NEW_FILE}}`:
    *   Implement class `{{CLASS_NAME}}`.

## 4. Verification (Definition of Done)
*   [ ] **Unit Test:** Run `npm test {{TEST_NAME}}` and pass.
*   [ ] **Manual Check:** {{MANUAL_CHECK_INSTRUCTION}}.
*   [ ] **No Regressions:** Main build passes.

## 5. QA Notes
(Leave empty for QA Agent)
