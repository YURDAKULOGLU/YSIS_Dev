# Task ID: T-031

- **Source Document:** `docs/epics/4.flows-workflow-automation.md`, `RELEASE_READINESS_ASSESSMENT.md`, `resources/proposals/FLOW_TEMPLATES_BASED_ON_SURVEY.md`
- **Title:** (P0) Complete Flow Templates - Survey-Based Priority Templates
- **Description:** 
  Based on user survey results (~30 respondents), implement high-priority flow templates that users actually need. Survey shows top needs: task reminders, daily planning, study support, email organization, budget tracking.

  **Survey-Based Priority Templates (P0):**
  1. **Daily Task Reminder & Planning** (15+ votes) - Most requested feature
     - Daily reminders at user's preferred time
     - Priority tasks + overdue tasks summary
     - Notification with task count
  2. **Smart Daily Planning** (12+ votes) - Personalized daily plan
     - AI-powered priority detection (queryRAG)
     - Time blocks based on work hours
     - Events + tasks integration
  3. **Study Session Planner** (8+ votes) - For student user base
     - Customizable study duration
     - Break reminders
     - Study goal tracking
  4. **Weekly Review & Planning** (6+ votes) - Reflection and planning
     - Completed tasks summary
     - Next week goals
     - Achievement tracking

  **Epic 4 Original Templates (Keep as P1):**
  5. **Morning Routine** (8 AM daily) - email summary + task list
  6. **Project Kickoff** (manual) - create project note + tasks + calendar event
  7. **Focus Mode** (manual) - mute notifications + create focus note + start timer

  **Current Templates (in `useFlows.ts`):**
  1. `daily-summary` (6 PM daily) - Can be enhanced to "Daily Task Reminder"
  2. `overdue-reminder` (9 AM daily) - Keep, useful
  3. `weekly-planning` (9 AM Monday) - Update to "Weekly Review" (Sunday 6 PM)
  4. `task-tracker` (manual) - Keep or replace with "Study Session Planner"

  **Requirements:**
  1. **P0 Templates (Survey Priority):**
     - Add "Daily Task Reminder & Planning" template
     - Add "Smart Daily Planning" template (requires queryRAG)
     - Add "Study Session Planner" template
     - Update "Weekly Review" template (Sunday 6 PM, enhanced with task summary)
  
  2. **P1 Templates (Epic 4):**
     - Add "Morning Routine" template
     - Add "Project Kickoff" template
     - Add "Focus Mode" template
  
  3. **Template Features:**
     - All templates must support variables (time, duration, boolean options)
     - Templates should be customizable before activation
     - Template format: JSON (not YAML, easier to parse in TypeScript)
     - See `resources/proposals/FLOW_TEMPLATES_BASED_ON_SURVEY.md` for detailed specs

  **Technical Notes:**
  - Templates are defined in `apps/mobile/src/features/flows/hooks/useFlows.ts` as `FLOW_TEMPLATES` array
  - Each template needs: id, name, description, config (trigger, steps)
  - Template variables: `{{today}}`, `{{now}}`, `{{week_number}}`, `{{user.name}}` (if supported)
  - Step types: createTask, createNote, sendNotification, delay, createCalendarEvent
  - See Epic 4 Story 4.3 for detailed template specifications

  **Acceptance Criteria:**
  - [ ] **P0 Templates (Survey-Based):**
    - [ ] Daily Task Reminder & Planning (schedule, variables: reminder_time, include_priority_tasks)
    - [ ] Smart Daily Planning (schedule, variables: planning_time, work_hours, uses queryRAG)
    - [ ] Study Session Planner (manual, variables: study_subject, study_duration, include_break)
    - [ ] Weekly Review & Planning (Sunday 6 PM, variables: review_time, includes task summary)
  - [ ] **P1 Templates (Epic 4):**
    - [ ] Morning Routine (8 AM daily)
    - [ ] Project Kickoff (manual, variables: project_name, deadline, team_size)
    - [ ] Focus Mode (manual, variables: duration, focus_goal)
  - [ ] All templates support variable customization
  - [ ] Templates are functional and can be executed
  - [ ] Template variables work correctly ({{today}}, {{now}}, {{user.name}}, etc.)
  - [ ] Template UI shows preview before activation
  - [ ] Users can customize variables before creating flow from template

- **Priority:** P0 (Critical - Blocks Epic 4 completion)
- **Assigned To:** @ClaudeCode
- **Related Tasks:** 
  - Epic 4: Flows & Workflow Automation
  - Story 4.3: Flow Templates - Pre-built Workflows
- **Estimated Effort:** 6-8 hours (7 templates total: 4 P0 + 3 P1)
- **Dependencies:** 
  - Flow Engine (✅ exists)
  - Step types: createTask, createNote, sendNotification, delay (✅ exist)
  - createCalendarEvent step type (⚠️ may need to be added to Flow Engine)

