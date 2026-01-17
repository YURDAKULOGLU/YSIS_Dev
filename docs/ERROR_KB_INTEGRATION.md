# Error Knowledge Base Integration

## Status: ✅ INTEGRATED

Error Knowledge Base has been integrated into workflow nodes for cross-task learning.

---

## Integration Points

### 1. ✅ verifier_node → record_error()

**Location:** `src/ybis/orchestrator/graph.py:728`

**Implementation:**
```python
# Record errors to Error Knowledge Base
try:
    from ..services.error_knowledge_base import ErrorKnowledgeBase
    
    error_kb = ErrorKnowledgeBase()
    error_kb.record_from_verifier_report(ctx, verifier_report)
except Exception:
    # Error KB not critical, continue if it fails
    pass
```

**What it does:**
- Records all verifier errors (lint, test failures, warnings)
- Stores error type, message, location, step
- Extracts patterns automatically

---

### 2. ✅ gate_node → record_block()

**Location:** `src/ybis/orchestrator/graph.py:929`

**Implementation:**
```python
# Record gate block to Error Knowledge Base
if final_decision.decision.value == "BLOCK":
    try:
        from ..services.error_knowledge_base import ErrorKnowledgeBase
        
        error_kb = ErrorKnowledgeBase()
        error_kb.record_error(
            task_id=ctx.task_id,
            run_id=ctx.run_id,
            error_type="gate_block",
            error_message=f"Gate blocked: {', '.join(final_decision.reasons)}",
            step="gate",
            context={
                "decision": final_decision.decision.value,
                "reasons": final_decision.reasons,
                "verification_passed": verifier_report.lint_passed and verifier_report.tests_passed,
            },
        )
    except Exception:
        # Error KB not critical, continue if it fails
        pass
```

**What it does:**
- Records when gate blocks a task
- Stores block reasons and context
- Helps identify recurring block patterns

---

### 3. ✅ spec_node → get_insights()

**Location:** `src/ybis/orchestrator/graph.py:157`

**Implementation:**
```python
# Get error insights from Error Knowledge Base
error_insights = None
try:
    from ..services.error_knowledge_base import ErrorKnowledgeBase
    
    error_kb = ErrorKnowledgeBase()
    insights = error_kb.get_insights_for_task(state["task_id"])
    
    if insights.get("error_count", 0) > 0:
        # Build insights message
        insights_parts = []
        insights_parts.append("📚 ERROR KNOWLEDGE BASE INSIGHTS:")
        insights_parts.append(f"This task has {insights['error_count']} recorded errors.")
        
        if insights.get("patterns"):
            insights_parts.append("\nRecurring error patterns:")
            for pattern in insights["patterns"][:3]:  # Limit to 3 patterns
                insights_parts.append(f"  - {pattern.get('error_type', 'unknown')}: {pattern.get('occurrence_count', 0)} occurrences")
        
        if insights.get("suggestions"):
            insights_parts.append("\nSuggested fixes:")
            for suggestion in insights["suggestions"][:3]:  # Limit to 3 suggestions
                insights_parts.append(f"  - {suggestion.get('suggestion', 'N/A')}")
        
        error_insights = "\n".join(insights_parts)
except Exception:
    # Error KB not critical, continue if it fails
    pass
```

**What it does:**
- Queries Error KB for task-specific insights
- Gets error patterns and suggestions
- Injects insights into LLM prompt
- Helps spec generation learn from past errors

---

### 4. ✅ plan_node → get_similar()

**Location:** `src/ybis/orchestrator/graph.py:420`

**Implementation:**
```python
# Get similar errors from Error Knowledge Base
similar_errors_context = None
try:
    from ..services.error_knowledge_base import ErrorKnowledgeBase
    
    error_kb = ErrorKnowledgeBase()
    # Get similar errors from previous tasks
    similar_errors = error_kb.get_similar_errors(
        step="plan",
        limit=5,
    )
    
    if similar_errors:
        similar_errors_context = "📚 SIMILAR ERRORS FROM PAST TASKS:\n"
        for error in similar_errors:
            similar_errors_context += f"  - [{error.error_type}] {error.error_message[:100]}...\n"
        similar_errors_context += "\nIMPORTANT: Learn from these past errors and avoid them in your plan.\n\n"
except Exception:
    # Error KB not critical, continue if it fails
    pass

# Add similar errors context if available
if similar_errors_context:
    task_objective = similar_errors_context + task_objective
```

**What it does:**
- Queries Error KB for similar errors from past tasks
- Filters by step="plan" to get planning-related errors
- Injects similar errors into task objective
- Helps plan generation avoid past mistakes

---

## Storage

**Location:** `platform_data/error_kb/`

**Files:**
- `errors.jsonl` - One error per line (JSONL format)
- `patterns.json` - Extracted error patterns
- `stats.json` - Statistics (optional)

**Example error record:**
```json
{
  "task_id": "T-123",
  "run_id": "R-456",
  "error_type": "lint_error",
  "error_message": "E501 line too long (120 > 100 characters)",
  "error_location": "src/ybis/orchestrator/graph.py:123",
  "step": "verify",
  "timestamp": "2026-01-11T14:00:00",
  "context": {"lint_passed": false}
}
```

---

## Benefits

1. **Cross-Task Learning:**
   - Task'lar birbirinden öğreniyor
   - Geçmiş hatalar yeni task'larda kullanılıyor

2. **Pattern Detection:**
   - Benzer hatalar otomatik gruplanıyor
   - Recurring patterns tespit ediliyor

3. **Proactive Prevention:**
   - spec_node geçmiş hataları görüyor
   - plan_node benzer hataları görüyor
   - Aynı hatalar tekrar edilmiyor

4. **Continuous Improvement:**
   - Her task Error KB'yi zenginleştiriyor
   - Sistem zamanla daha akıllı oluyor

---

## Future Enhancements

- [ ] Dashboard integration (show error patterns in UI)
- [ ] Auto-suggest fixes based on patterns
- [ ] Error correlation analysis
- [ ] Predictive error detection

