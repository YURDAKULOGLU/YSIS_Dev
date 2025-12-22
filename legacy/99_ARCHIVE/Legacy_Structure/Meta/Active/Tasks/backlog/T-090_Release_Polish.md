# T-090: Release Polish & Final Features

**Status:** Ready for Development
**Priority:** High
**Objective:** Implement the final set of agreed features to prepare the app for release.

## 1. RAG & Context Awareness (Critical)
- [x] **Verify RAG Integration:** Ensure `queryContext` tool is correctly used by the AI.
- [x] **System Prompt Update:** Modify `promptGenerator.ts` to explicitly encourage the AI to check context (Tasks, Events, Notes) when answering vague queries (e.g., "What do I have today?").
- [x] **Testing:** Verify the AI can answer questions about user data.

# T-090: Release Polish & Final Features

**Status:** Ready for Development
**Priority:** High
**Objective:** Implement the final set of agreed features to prepare the app for release.

## 1. RAG & Context Awareness (Critical)
- [x] **Verify RAG Integration:** Ensure `queryContext` tool is correctly used by the AI.
- [x] **System Prompt Update:** Modify `promptGenerator.ts` to explicitly encourage the AI to check context (Tasks, Events, Notes) when answering vague queries (e.g., "What do I have today?").
- [x] **Testing:** Verify the AI can answer questions about user data.

## 2. Alarm & Flow System
- [ ] **Tool-less Flows:** Update `toolServiceFunctions.ts` to allow Flows without tools (Trigger -> Output).
- [ ] **Alarm Output:** Implement `output_type: 'alarm'` logic.
- [ ] **Notification Integration:** Use `expo-notifications` to schedule local notifications for Flows.
- [ ] **Sound Manager:** Implement `SoundManager` (code-only) to handle alarm sounds when app is open.

## 3. Integrated Reminders
- [x] **Tasks:** Update `createTask` to schedule a notification if `due_date` is provided.
- [x] **Events:** Update `createCalendarEvent` to schedule a notification 15 minutes before start.

## 4. UX Polish
- [ ] **Haptics:** Implement `useHaptics` hook and add feedback to:
    - Button presses
    - Message sent/received
    - Task completion
    - Error states
- [x] **Weather Tool:** Implement `get_weather` tool using OpenMeteo API.

## 5. Onboarding
- [ ] **Pre-made Flow:** Create a "Daily Briefing" Flow for new users (Weather + Task Summary) in the database setup or `useFlows` initialization.

## 6. Verification & E2E Testing
- [ ] **Integration Tests (Jest):**
    - Create `__tests__/integration/reminders.test.tsx`
    - Test: Create Task -> Check `scheduleNotificationAsync` called.
    - Test: Create Event -> Check `scheduleNotificationAsync` called.
    - Test: Create Alarm Flow -> Check `scheduleNotificationAsync` called.
    - Test: Server flow runner smoke (requires `SUPABASE_SERVICE_ROLE_KEY` and cron): call Edge Function `flow-runner` with service key header -> expect 200 and `ran` field.
- [ ] **Manual Walkthrough:**
    - Verify Haptics on real device (if possible) or simulator.
    - Verify Notification appearance.

## Notes
- **TTS (Text-to-Speech):** Cancelled due to poor Turkish quality.
- **Web Search:** Cancelled due to missing API Key.
- **Global Search:** Cancelled for now.

# Progress Report (2025-12-06)

## 1. RAG & Context Awareness (Completed)
We have significantly enhanced the AI's ability to understand user context.
- **`queryContext` Tool:** Implemented a unified search tool that queries Notes, Tasks, and Events simultaneously.
- **System Prompt:** Updated `promptGenerator.ts` to explicitly instruct the AI to use `queryContext` when answering vague questions like "What do I have today?".
- **Verification:** Added unit tests (`promptGenerator.test.ts`) confirming the prompt includes the correct instructions and context hints.

## 2. Integrated Reminders (Completed)
Automatic notifications are now deeply integrated into the core creation flows.
- **Tasks:** Creating a task with a `due_date` now automatically schedules a local notification.
- **Events:** Creating a calendar event automatically schedules a reminder 15 minutes before the start time.
- **Implementation:** Modified `toolServiceFunctions.ts` to call `scheduleAlarmService` directly within `createTask` and `createCalendarEvent`.

## 3. Weather Tool (Completed)
The AI can now provide real-time weather information.
- **Tool:** Implemented `getWeather` using the OpenMeteo API (no API key required).
- **Functionality:** Supports querying by City Name or Latitude/Longitude.
- **Integration:** Added to `tools.ts` and `toolServiceFunctions.ts`.

## 4. Visual Polish (Completed)
- **App Icon:** Updated the app icon with a new "Vortex" design.
- **Adaptive Icon:** Configured fallback for Android adaptive icons.

## 5. Flow Engine Refactor (Completed)
- **Platform Agnostic:** Refactored `FlowEngine.ts` to use `crypto.randomUUID` (Web Standard) with a fallback, removing the hard dependency on `expo-crypto`. This paves the way for running Flows on the server (Supabase Edge Functions) in the future.
- **Default Seeding:** Implemented logic to seed default Flow templates for new users.

## 6. Modified Files (2025-12-06)

### RAG & AI Context
- `apps/mobile/src/services/ai/promptGenerator.ts`
- `apps/mobile/src/services/ai/tools.ts`
- `apps/mobile/src/services/ai/__tests__/promptGenerator.test.ts` (NEW)

### Integrated Reminders & Tools
- `apps/mobile/src/services/data/toolServiceFunctions.ts`
- `apps/mobile/src/services/data/__tests__/toolServiceFunctions.reminders.test.ts` (NEW)

### Flow Engine & Onboarding
- `apps/mobile/src/features/flows/hooks/useFlows.ts`
- `packages/core/src/services/FlowEngine.ts`

### Visual & UI
- `apps/mobile/assets/icon.png`
- `apps/mobile/assets/adaptive-icon.png`
- `apps/mobile/src/features/chat/hooks/useChat.ts`

### Documentation
- `task.md`
- `T-090_Release_Polish.md`
- `walkthrough.md` (NEW)
