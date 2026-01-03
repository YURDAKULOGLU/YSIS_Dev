# [ALERT] P0 (Critical) Task Protocol

> **Standard v1.0**
> *Total accountability for system-critical changes.*

---

## 1. DEFINITION
A **P0 Task** is any task with `priority: CRITICAL` or one that triggers `Level 3 Risk` (High Risk).

## 2. THE FLOW
Agents cannot unilaterally complete P0 tasks. The following flow is MANDATORY:

1. **Implementation:** Agent performs work and creates ALL artifacts (including `EVIDENCE/summary.md`).
2. **Review Request:** Agent sends a message to the Architect (User):
   `ybis.py message send --to cli-user --subject "Review Required: TASK-ID" --content "Work finished. Please review evidence at workspace X."`
3. Architect Review: Human/Architect reviews the RESULT.md and EVIDENCE.
   - Use the **[Manual Verification Checklist](./templates/MANUAL_VERIFICATION.md)** for standardized auditing.
4. Acknowledgment: Architect acknowledges the message with action done or approved.
   `ybis.py message ack --id MSG-ID --agent cli-user --action approved`
5. **Final Completion:** Only after acknowledgment, the agent runs `ybis.py complete`.

Token budget applies to RESULT/META, but EVIDENCE/summary.md remains mandatory.

## 3. VIOLATION
Completing a P0 task without Architect Acknowledgment results in a **Constitutional Violation** and immediate rollback of the changes.
