# Closed Beta Release Scope: Investigation and Proposal

**Task ID:** T-016
**Author:** @Gemini (Research Agent)
**Date:** 2025-11-30
**Status:** Complete

---

## 1. Executive Summary

This report details the findings of an investigation into the scope of the YBIS Closed Beta release. The investigation confirms that a definitive plan already exists and was finalized on **October 29, 2025**.

The core finding is a strategic pivot away from broad, external integrations towards a focused, self-contained application to accelerate time-to-market and validate the core value proposition first.

**The proposed Closed Beta will focus on:**
- **Core User Experience:** A self-contained application with built-in Notes, Tasks, and a simple Calendar.
- **Core Technology:** The AI-powered "Flows" (workflow automation) and "Tool Calling" systems.
- **Explicitly Excluded:** All external Google Workspace integrations (Calendar, Gmail, Tasks) are deferred to post-beta patches based on user feedback.

This report summarizes the final, approved plan as detailed in the `docs/CLOSED_BETA_FINAL_SCOPE.md` document.

---

## 2. Investigation Process

The following documents were analyzed to determine the current, authoritative plan for the Closed Beta:

- `docs/CLOSED_BETA_FINAL_SCOPE.md` **(Primary Source of Truth)**
- `docs/vision/PROJECT_VISION.md` (Historical Context)
- `docs/roadmap/PRODUCT_ROADMAP.md` (Outdated)
- `docs/roadmap/DEVELOPMENT_ROADMAP.md` (Outdated)
- `docs/PRODUCTION_CHECKLIST.md` (Supporting Evidence)

The analysis revealed a clear strategic decision made on October 29, 2025, to narrow the scope of the initial release. The "FINAL SCOPE" document supersedes the older vision and roadmap documents.

---

## 3. The Final Closed Beta Scope (Approved Plan)

The following is a summary of the official, approved scope for the Closed Beta release.

### 3.1. Core Philosophy
- **"Ship working app first, Google integrations later."**
- **"Built-in features > External sync (for beta)."**

### 3.2. Features INCLUDED in Closed Beta

#### **P0 - Critical (Shipment Blockers):**
1.  **Backend Foundation:**
    - Supabase backend (Auth, Database with RLS).
    - `AuthPort` with Google OAuth and Email/Password.
    - APIs for Notes, Tasks, and Flows (CRUD + Realtime).
2.  **Flows & Workflow Automation:**
    - A "Flow Engine" for executing automated workflows.
    - 5 pre-built, functional Flow templates (e.g., Morning Routine, Daily Planning).
    - Manual and scheduled triggers for flows.
3.  **AI Tool Calling System:**
    - LLM function calling via `LLMPort` (initially OpenAI).
    - 5 core tools for the AI to use (e.g., `createTask`, `createNote`, `searchNotes`).

#### **P1 - High Priority (Polish Features):**
1.  **Push Notifications & Monitoring:**
    - Basic push notifications for key events (e.g., task due).
    - Error tracking via Sentry.
2.  **RAG (Retrieval-Augmented Generation) System:**
    - Document upload (PDF, TXT, MD).
    - Semantic search over user documents.
    - AI context injection from user's documents.

### 3.3. Features EXCLUDED from Closed Beta (Deferred)

The most significant decision was to defer all deep Google integrations to post-beta patches.

- **Google Calendar Sync:** The beta will have a simple, built-in calendar only.
- **Gmail Sync:** The beta will rely on the built-in Notes system.
- **Google Tasks Sync:** The beta will use its own built-in Tasks system.
- **Plugin System:** Deemed unnecessary for the initial release (YAGNI).

---

## 4. Goals & Success Criteria for Closed Beta

- **Primary Goal:** Validate the core value proposition of AI-powered automation (Flows and Tool Calling) in a self-contained environment.
- **Secondary Goal:** Gather user feedback to determine the priority for post-beta features (e.g., which Google integration is most requested).
- **Shipment Criteria:**
    - **Must-Haves:** All P0 features are fully functional (Auth, Notes, Tasks, Flows, AI Chat).
    - **Should-Haves:** All P1 features are implemented (Push Notifications, RAG).

---

## 5. Conclusion & Recommendation

The investigation concludes that a well-defined and strategically sound plan for the Closed Beta release is already in place. **No new proposal is necessary.**

**Recommendation:** Proceed with the execution of the plan as detailed in `docs/CLOSED_BETA_FINAL_SCOPE.md`. All development efforts should align with the epics, priorities, and timelines outlined in that document.

---

## Appendix: Critical Analysis of Issue-Tracking Documents

As a continuation of the investigation, a critical analysis was performed on two documents related to active and current issues: `.../shared/ACTIVE_PROBLEMS.md` and `.../shared/CURRENT_ISSUES.md`.

### A.1. Key Findings

1.  **`ACTIVE_PROBLEMS.md` is Obsolete:** This document from 2025-11-25 17:30 detailed critical sprint-blockers that have since been resolved, as confirmed by the log in `CURRENT_ISSUES.md` (updated 2025-11-27). It should be archived to prevent confusion.

2.  **`CURRENT_ISSUES.md` is Misaligned:** This document is a more useful, dynamic log, but it is not fully aligned with the official Closed Beta scope.
    *   **Strong Alignment:** It correctly identifies the "Flows System" (#24) as "VERY IMPORTANT" and tracks relevant bugs for the core features.
    *   **Major Misalignment:** It contains numerous feature requests (e.g., "Mail Entegrasyonu" #16, "Google Kişiler / Rehber" #29) that directly contradict the strategic decision to defer all Google integrations. Its internal "Feature Roadmap" is also outdated.

### A.2. Recommendations from Issue Analysis

1.  **Triage `CURRENT_ISSUES.md`:** The document should be edited to align with the official scope. All feature requests not part of the Closed Beta MVP (especially Google-related ones) should be moved to a "Deferred / Post-Beta" category.
2.  **Consolidate Priority Management:** The roadmap and priority sections within `CURRENT_ISSUES.md` should be removed and replaced with a direct link to `docs/CLOSED_BETA_FINAL_SCOPE.md` to serve as the single source of truth for prioritization.

This analysis reinforces the conclusion that `docs/CLOSED_BETA_FINAL_SCOPE.md` is the definitive plan, and other peripheral documents need to be updated to reflect its strategic decisions.
