---
title: "Closed Beta Release Plan"
status: "DRAFT"
author: "@Antigravity"
date: "2025-12-04"
---

# Closed Beta Release Plan

## 1. Goal
Deliver a stable, functional, and secure version of the YBIS mobile application to a limited group of beta testers. The focus is on **Core Loops** (Chat, Flows, Notes, Tasks) and **Crash Prevention**.

## 2. Task Prioritization

### 🚨 Must Have (Blockers)
*These tasks MUST be completed before the release. They address critical bugs, missing core features, or security risks.*

- **T-051: Fix Flows Feature Architecture & Bugs** (Critical Feature Fix)
    - *Why:* The Flows feature is currently broken and crashes. It's a core USP.
- **T-052: Fix MessageBubble HTML & Markdown Rendering** (UX/Bug)
    - *Why:* Chat is a primary interface; broken text rendering makes it unusable.
- **T-054: Vitest Config Fix** (DevOps/Stability)
    - *Why:* We cannot verify code stability without working tests.
- **T-060: Security Audit Data Queries** (Security)
    - *Why:* Beta users will have real data. We must ensure basic RLS and query safety.
- **T-061: Add Error Boundaries** (Stability)
    - *Why:* Prevent the entire app from crashing (White Screen of Death) when a component fails.
- **T-065: Crash Reporting (Sentry)** (Observability)
    - *Why:* Essential for Beta. We need to know *why* it crashes on user devices.
- **T-068: Google OAuth Completion** (Auth)
    - *Why:* Smooth onboarding is critical for beta testers.
- **T-069: Push Tokens Table Setup** (Feature Enabler)
    - *Why:* Required for Notifications, which are a key part of Flows.

### ⚠️ Should Have (High Priority)
*These tasks are highly recommended for a good beta experience but won't block the release if time is tight.*

- **T-064: Basic Offline Support** (UX)
    - *Why:* Mobile apps should not break immediately without internet.
- **T-067: Complete i18n Coverage** (UX)
    - *Why:* Ensure no missing translation keys (e.g., `flow.title.missing`) appear.
- **T-074: Accessibility Labels** (UX/Quality)
    - *Why:* Basic accessibility is a standard quality gate.
- **T-075: Prompt Injection Prevention** (Security/AI)
    - *Why:* Protect the AI agent from basic attacks.

### 📉 Nice to Have (Post-Beta)
*These can be deferred to the Public Beta or v1.0.*

- **T-012: Backend rate limiting** (Scale)
- **T-062: AI Client Rate Limiting** (Scale)
- **T-063: Bundle Analysis Optimization** (Performance)
- **T-070: FlowEngine Platform Decoupling** (Refactor)
- **T-071: Large Files Refactoring** (Refactor)
- **T-072: Navigation Deep Linking** (Feature)
- **T-073: Performance Memoization** (Optimization)

## 3. Release Roadmap

### Phase 1: Stabilization (Week 1)
1.  Fix Vitest (T-054).
2.  Fix Flows (T-051) & Chat (T-052).
3.  Implement Error Boundaries (T-061).

### Phase 2: Core Features & Security (Week 2)
1.  Complete Google OAuth (T-068).
2.  Setup Push Tokens (T-069).
3.  Security Audit (T-060).
4.  Setup Sentry (T-065).

### Phase 3: Polish & Ship (Week 3)
1.  i18n Check (T-067).
2.  Final Manual QA.
3.  **RELEASE** to TestFlight / Google Play Console (Internal Track).

## 4. Recommendation
Assign **T-051**, **T-052**, and **T-054** immediately to @ClaudeCode to unblock Phase 1.
