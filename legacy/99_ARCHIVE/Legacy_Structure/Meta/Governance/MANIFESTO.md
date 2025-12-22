# YBIS MANIFESTO (The Truth)

**Date:** 2025-12-07
**Version:** 1.2 (The Founder's Defended Vision)

## 🌌 The Core Trinity
YBIS is not just a "To-Do List" or a "Chatbot". It is an innovation built on three pillars to manage a personal agenda with elegance:
1.  **🧠 Intelligence (Zeka):** Proactive, understanding context, not just reactive.
2.  **💾 Memory (Hafıza):** Remembers everything (Rag/Vector), so you don't have to.
3.  **⚡ Automation (Otomasyon):** "Linear, Simple, Flexible." Comparable to n8n power but without the "Spaghetti UI" complexity.

**The Mission:**
Eliminate "Technological Drudgery" (Teknolojik Angarya). Save the user from the chaos of 10 different apps.

---

## 🏗️ The Architecture of Evolution
**"Smooth Transition via Ports"**
The App is built on a **Port Architecture** not just for code cleanliness, but for **Business Strategy**:
-   **Phase 0 (PoC):** Burn credits, use expensive models (OpenAI), log everything.
-   **Phase 1 (Growth):** Swap Ports to cheaper/faster providers without rewriting core logic.
-   **Future:** Local LLMs for Enterprise (Privacy) vs. Cloud LLMs for Personal.

---

## 🔌 The Integration Philosophy (Two-Way Sync)
**"Competitors are Complements"**
-   YBIS is **Standalone**. It works perfectly offline/alone.
-   Integrations (Notion, Google, Microsoft) are **Complements**, not dependencies.
-   **Goal:** Reduce Migration Friction. Users don't "switch" to YBIS; they "connect" YBIS to their existing life.
-   **Two-Way Sync:** Updates flow both ways. YBIS is the "Orchestrator".

---

## 🚀 The Roadmap (Grand Strategy)

### **Stage 1: The Closed Beta (Now - v0.1.x)**
*   **Target:** Friends, Family, Fools (Early Adopters).
*   **Business Model:** "Burn Money for Data." Free App, Free Credits.
*   **Goal:** Aggressive Logging. Understand *real* usage patterns.
    *   *Question:* What does a user actually DO 50 times a day?
*   **Deliverable:** A polished, "Show-offable" PoC for investors.

### **Stage 2: The Core Release (v1.0.0)**
*   Refined based on data from Stage 1.
*   The "Generic" Personal Assistant.

### **Stage 3: The Fork in the Road (Post-Release Paths)**

#### **Path A: Vertical Specialization (The "BIS" Family)**
Tailored versions of YBIS for specific industries, fueled by RAG & Specialized Features.
*   **LawBIS:** RAG on Legislation/Case Law. Hourly updates. Point-shot answers.
*   **StudentBIS:** Flashcards, Academic Papers, Curriculum tracking.
*   **MedBIS:** (Implied) Patient management, drug interactions.

#### **Path B: Cooperative/Enterprise (YBIS for Teams)**
*   **Individuals:** Shared Workspaces, Shared Notes.
*   **SMB (KOBİ):** Automated Customer Service, Boss assigning tasks to Employee Calendars.
*   **Enterprise:** Local LLMs (On-Prem), Zero Data Sharing, 100% Privacy.

---

## 🎨 Design Philosophy
*   **Zarif (Elegant):** It must feel premium.
*   **Simple:** No n8n complexity.
*   **Smooth:** Transitions between phases/features must be invisible.

---

## ⚔️ The Tactics (Detailed Execution Strategy)

### **1. The Brain (Automation & Onboarding)**
**How Automation is Born:**
1.  **User Demand:** Explicitly requested by the user.
2.  **AI Judgment (Proactive):** The AI observes patterns ("You did this task 5 times manually"). It proposes: *"Sen bunları yaptın, şu gün şunu kurmamı ister misin?"*
3.  **Seed Workflows:** We plant "Seed" workflows based on what competitors do best (e.g., Daily Briefing).

**The "Zarif" Onboarding:**
*   User enters the app -> Sees "Daily Briefing" seed.
*   **One Click:** A pre-designed Chat Conversation starts.
*   The Chat interviews the user smoothly to collect preferences and set up the flow.
*   **Result:** Proof of Capabilities. The user instantly sees: *"This app works."*

### **2. The Wallet (Pricing & Cost Strategy)**
*   **Pricing Reality:** Not everything is free forever. Pricing will be calculated based on **Average User Cost** observed in Beta.
*   **Target Price:** Accessible/Competitive (e.g., 100-400 TL range).
*   **Cost Management:** Text generation is cheap. Specialized RAG (like LawBIS) is expensive and will be priced accordingly.
*   **Closed Beta:** We intentionally "burn money" to gather high-quality training data (Intent Logs).
*   **Optimization:** Smart Routing & Local Server Custom Models will lower costs over time.

### **3. The Nightmare (Data & Retention)**
*   **Retention is King:** We analyze *why* a user didn't open the app again.
*   **Hypothesis Testing:** If retention drops, we form a hypothesis -> Send feedback emails -> Iterate.
*   **Aggressive Logging:** We log everything to capture **User Intent**, not just interaction.
*   **Training Data:** This data is the fuel to train YSIS (our specialized agent) to make better feature suggestions.

---

## 🛡️ The Defense (Addressing Critical Risks)

### **4. The "Fat App" Paradox (Architecture)**
*   **Defense:** The "Heavy Lifting" (RAG, PDF Parsing, indexing) happens **Server-Side**, not on the phone.
*   **Binary Size:** Remedied by **OTA Asset Downloads** (like games) only when a feature flag is enabled. The base app remains lightweight.

### **5. The "Bottleneck" Trap (Sync Safety)**
*   **Philosophy:** "Zero-Dependency". If YBIS is deleted, Notion/Google data remains untouched.
*   **Fail-Safe:** A **"Revert"** option is critical. If YBIS corrupts data during sync, the user must be able to rollback to the previous state instantly.
*   **Role:** YBIS is a *Client* to Notion/Google, not a Hostage Taker.

### **6. The "Chat Fatigue" (UX Solution)**
*   **Observation:** Chat is slow for repetitive tasks ("Set Alarm").
*   **Solution:** **Live Widgets**.
*   **Interaction:** 
    *   **Bottom:** Chat (Proactive/Complex requests).
    *   **Top:** Swipable, Interactive Widgets (Reactive/Fast Lane).
    *   **Dynamic:** Widgets update live as the AI works.
    *   **Goal:** 80% of tasks completed on the Home Screen without opening a keyboard.
