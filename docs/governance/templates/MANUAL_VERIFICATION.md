# Manual Verification Checklist

> Required for all P0 (Critical) tasks.
> Attachment to EVIDENCE/summary.md.

---

## 1. PRE-CHECK
- [ ] Task ID matches the assigned workspace.
- [ ] PLAN.md was approved by Council (if High Risk).
- [ ] PLAN/RESULT include token_budget.

## 2. EVIDENCE REVIEW
- [ ] Logic: Does the code implementation match the PLAN?
- [ ] Security: No hardcoded secrets or accidental out-of-bounds writes?
- [ ] Performance: No obvious infinite loops or memory leaks?

## 3. VERIFICATION RUN
- [ ] Automated tests passed (pytest output attached).
- [ ] Linting passed (Ruff/Sentinel output attached).
- [ ] Compile check passed.

## 4. SIGN-OFF
- Agent ID: _______________
- Date: _______________
- Architect/User Ack: [YES / NO]
