# Feedback Loop Implementation

**Date:** 2026-01-10  
**Status:** ✅ **IMPLEMENTED**

---

## Problem

Previously, verifier errors were not fed back to spec/plan nodes. This meant:
- AI couldn't learn from previous failures
- Same errors repeated across runs
- No improvement in spec/plan quality over retries

## Solution

Implemented a **feedback loop** that:
1. Captures verifier errors
2. Feeds them back to spec/plan nodes
3. Allows AI to learn and improve

---

## Implementation

### 1. Spec Node Feedback Loop

**File:** `src/ybis/orchestrator/graph.py:90-207`

**Changes:**
- Loads `verifier_report.json` if available
- Extracts errors and warnings
- Adds feedback to LLM prompt:
  ```
  ⚠️ FEEDBACK FROM VERIFIER (Previous Run Failed):
  [errors and warnings]
  
  IMPORTANT: The previous spec/implementation had these issues. Please:
  1. Address these errors in the new spec
  2. Ensure the spec prevents these issues
  3. Add requirements/acceptance criteria that would catch these errors
  ```

**Result:** AI now sees previous errors and can improve spec quality.

### 2. Plan Node Feedback Loop

**File:** `src/ybis/orchestrator/graph.py:299-420`

**Changes:**
- Loads `verifier_report.json` if available
- Extracts errors and warnings
- Adds feedback to task objective before planning:
  ```
  ⚠️ FEEDBACK FROM VERIFIER (Previous Run Failed):
  [errors and warnings]
  
  IMPORTANT: The previous plan/implementation had these issues. Please:
  1. Address these errors in the new plan
  2. Ensure the plan avoids these issues
  3. Add validation steps that would catch these errors
  ```

**Result:** AI now sees previous errors and can improve plan quality.

### 3. Enhanced Repair Node

**File:** `src/ybis/orchestrator/graph.py:679-730`

**Changes:**
- Analyzes error types to determine if spec/plan needs repair
- Sets flags:
  - `needs_spec_repair` - if errors suggest spec issues
  - `needs_plan_repair` - if errors suggest plan issues
- Stores error context for spec/plan nodes

**Error Detection:**
- Spec errors: "spec", "requirement", "acceptance", "missing", "incomplete"
- Plan errors: "plan", "file", "step", "instruction", "syntax", "invalid"

### 4. Workflow Routing

**File:** `src/ybis/orchestrator/graph.py:1625-1650`

**Changes:**
- Added `repair_route()` function
- Routes after repair:
  - `spec` - if `needs_spec_repair` is True
  - `plan` - if `needs_plan_repair` is True
  - `execute` - otherwise (re-execute with error context)

**Result:** Workflow can now loop back to spec/plan generation when needed.

---

## Flow Diagram

```
┌─────────┐
│  spec   │
└────┬────┘
     │
     ▼
┌─────────┐
│  plan   │
└────┬────┘
     │
     ▼
┌──────────┐
│ execute  │
└────┬─────┘
     │
     ▼
┌──────────┐
│ verify   │
└────┬─────┘
     │
     ├─► FAIL ──► repair ──► spec (if spec errors)
     │                      └─► plan (if plan errors)
     │                      └─► execute (if execution errors)
     │
     └─► PASS ──► gate
```

---

## Benefits

1. **Learning from Errors:** AI sees previous failures and improves
2. **Better Specs:** Specs improve over retries with feedback
3. **Better Plans:** Plans avoid previous mistakes
4. **Reduced Repetition:** Same errors don't repeat
5. **Quality Improvement:** Overall quality improves over time

---

## Example

**First Run:**
- Spec: Missing requirements section
- Plan: Generated
- Execute: Code generated
- Verify: ❌ "Spec missing requirements"
- Repair: Detects spec error
- **Loop back to spec with feedback**

**Second Run:**
- Spec: ✅ Now includes requirements (learned from feedback)
- Plan: Generated
- Execute: Code generated
- Verify: ✅ Passes

---

## Testing

To test feedback loop:

1. Create a task with a spec that's missing requirements
2. Run workflow
3. Verifier should fail with "Spec missing requirements"
4. Repair node should detect spec error
5. Workflow should loop back to spec node
6. Spec node should see feedback and improve spec
7. New spec should include requirements

---

## Future Enhancements

1. **Structured Feedback:** Parse errors into structured format (file, line, error type)
2. **Error Patterns:** Learn common error patterns and prevent them proactively
3. **Feedback History:** Track feedback across multiple runs
4. **Quality Metrics:** Measure improvement in spec/plan quality over time

---

## References

- `src/ybis/orchestrator/graph.py` - Implementation
- `docs/SELF_DEVELOPMENT_QUALITY_ASSESSMENT.md` - Quality assessment
- `docs/SELF_DEVELOPMENT_PLAN.md` - Self-development plan

