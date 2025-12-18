# Feedback Synthesis Report (2025-12-07)

**Source:** Chat Logs (Yurdakul), Survey Data.

## 🚨 Critical Bugs (Immediate Actions)
1.  **Text Selection:** Users cannot copy text from Chat bubbles. *Critical for usability.*
2.  **Alarm Logic:** "Why couldn't I set an alarm?" -> Permission or Logic failure in `NotificationService`.

## 📊 Survey Insights (The "Trust Gap")
*   **Usage Pattern:** Daily usage is common, but mostly for "Information/Translation/Coding".
*   **Major Pain Point:** **"Yanlış veya Tutarsız Cevaplar" (Hallucinations).** Users do not trust AI for facts.
*   **Opportunity:** YBIS must leverage its **"Memory"** and **"Integration"** (Ground Truth) to offer higher reliability than generic LLMs.
*   **Key Requests:**
    *   "Planlama ve Düzenleme" (Personalized Scheduling).
    *   "Mail Kontrolü" (Email summarization).
    *   "Complex Analysis" (Bill calculation, detailed research).

## 💡 Feature Requests (Yurdakul & Chat Logs)
### **Visuals & UI (Addressing Chat Fatigue)**
*   **Widgets:** "Too narrow" -> Needs density and interactivity.
*   **Calendar:** Daily/Weekly/Monthly/Yearly views requested.
*   **Statistics:** "Heat Charts" (Github style), Mood Tracking graphs.
*   **Aesthetics:** "Paper-like notes", "Better Chat Bubbles", "Sound Themes".

### **Smart Logic**
*   **Notifications:** Actionable buttons (Approve/Postpone).
*   **Tasks:** Nested Tasks, Subtask suggestions, "Motivation Mode".
*   **Context:** "Kargon çok yaklaştı" (Parsing emails for real-world context).

## 🧭 Strategic Implication for v0.1.1
**Pivot Confirmation:** The request for *Widgets, Calendar Views, and Statistics* strongly supports the **"View Refactoring" (Phase 3)** and **"Visuals"** over just pure Chat.
**Differentiation:** "Reliability" via RAG/Memory is the killer feature against generic ChatGPT.

## Action Plan
1.  **Fix Bugs:** Copy Text & Alarm.
2.  **Phase 1.1:** Prioritize "Actionable Notifications" and "Widget Redesign" to show immediate value.
