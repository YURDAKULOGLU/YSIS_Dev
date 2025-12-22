---
title: "Fixing Flows Architecture & Chat Rendering"
status: "PROPOSED"
author: "@Antigravity"
date: "2025-12-04"
---

# Proposal: Flows & Chat Fixes

## 1. Problem Statement

### 1.1. Flows Feature Instability
The "Flows" feature is currently unstable due to:
- **Inconsistent State Management:** Logic is split between `useFlows` (local hook) and `useFlowsStore` (Zustand).
- **Broken Triggers:** `FlowBuilder` creates triggers as Objects, but Templates use Cron Strings.
- **Missing Handlers:** Output handlers (`output_notification`, etc.) are defined in the Engine but not registered in the runtime.
- **AI Stub:** AI processing is not implemented.

### 1.2. Chat Rendering Issues
- **HTML Parsing:** `MessageBubble` fails to parse HTML entities (e.g., `&quot;`) and tags.
- **Markdown:** List rendering is broken.

## 2. Proposed Solution

### 2.1. Flows Architecture Refactor
We will standardize on the **Zustand Store** pattern (`useFlowsStore`) to align with the "Notes" and "Tasks" (future state) architecture.

**Changes:**
1.  **Refactor `useFlowsStore.ts`:**
    - Ensure it handles all CRUD operations.
    - Add `runFlow` action that invokes `FlowEngine`.
2.  **Update `FlowEngine.ts` (`packages/core`):**
    - Add a default "AI Handler" (mock for now) to prevent crashes.
3.  **Update `useFlows.ts` (`apps/mobile`):**
    - **DEPRECATE** the internal state logic.
    - Make it a wrapper around `useFlowsStore`.
    - Register missing output handlers (`output_notification`, `output_note`, etc.) in the `FlowEngine` initialization within the hook.
4.  **Fix `FlowBuilder.tsx`:**
    - Update form submission to convert "Schedule Object" -> "Cron String" before saving.
    - Add input fields for Tool Parameters (if AI is disabled).

### 2.2. Chat Rendering Fix
We will replace the custom/incomplete Markdown rendering with a robust library.

**Changes:**
1.  **Install Dependency:** `react-native-render-html` in `packages/chat`.
2.  **Update `MarkdownRenderer.tsx`:**
    - Integrate `RenderHTML` for handling HTML content.
    - Fix `marked` configuration for standard Markdown (lists, bold).

## 3. Implementation Steps (for @ClaudeCode)

### Step 1: Chat Fix (Low Risk)
- Install `react-native-render-html`.
- Modify `packages/chat/src/MarkdownRenderer.tsx`.
- Verify in `MessageList`.

### Step 2: Flows Refactor (High Risk)
- Update `packages/core/src/services/FlowEngine.ts` (add AI stub).
- Update `apps/mobile/src/stores/useFlowsStore.ts` (add `runFlow`).
- Rewrite `apps/mobile/src/features/flows/hooks/useFlows.ts` to use the store.
- Fix `apps/mobile/src/features/flows/components/FlowBuilder.tsx` (Cron conversion).

## 4. Verification
- **Chat:** Send a message with `<b>bold</b>` and `<ul><li>list</li></ul>` to verify rendering.
- **Flows:** Create a scheduled flow, verify it saves as Cron, and run it manually to check Output Handlers.
