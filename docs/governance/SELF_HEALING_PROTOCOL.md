# Self-Healing Protocol V1.0

> "The system that learns from its failures becomes antifragile."

This document defines the self-healing capabilities of the YBIS Autonomous Factory.

---

## 1. Core Philosophy

### 1.1 Infinite Solution Space

When solving problems, the solution space is UNBOUNDED. We do not restrict possible solutions.

**Solution Priority Order:**
```
1. FRAMEWORK    -> Open-source solution exists? USE IT (highest priority)
2. LIBRARY      -> Add a library?
3. CONFIG       -> Change configuration?
4. TWEAK        -> Small code modification?
5. PATTERN      -> Apply design pattern?
6. CUSTOM       -> Write from scratch (last resort)
```

### 1.2 Requirements for Any Solution
- **(a) Documented** - Solution must be recorded
- **(b) Tested** - Solution must be verified
- **(c) Persisted** - Solution must be stored for future reference

---

## 2. Self-Healing Loop

```
+-------------------------------------------------------------------+
|                     SELF-HEALING LOOP                             |
+-------------------------------------------------------------------+
|  OBSERVE  |  Metrics, logs, events continuously collected         |
|  DETECT   |  Anomaly/error patterns identified                    |
|  DEBATE   |  Solution space explored (framework? tweak? custom?)  |
|  DECIDE   |  Best solution selected via voting/consensus          |
|  APPLY    |  Solution implemented (code/config/framework install) |
|  VERIFY   |  Solution tested in isolation then integration        |
|  LEARN    |  Pattern added to Knowledge Base                      |
+-------------------------------------------------------------------+
```

---

## 3. Infrastructure Requirements

### 3.1 Event Bus (Redis)

```yaml
# docker-compose.yml
services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
```

**Event Types:**
- `task.created` / `task.completed` / `task.failed`
- `error.detected` / `error.resolved`
- `debate.started` / `debate.concluded`
- `pattern.learned`

### 3.2 Metrics Collector

**Core Metrics:**
| Metric | Type | Description |
|--------|------|-------------|
| `task_success_rate` | Gauge | % of tasks completed successfully |
| `task_duration_seconds` | Histogram | Task completion time |
| `error_count` | Counter | Errors by type |
| `self_heal_count` | Counter | Auto-resolved issues |

### 3.3 Knowledge Base (ChromaDB + SQLite)

**Learned Patterns Storage:**
```sql
CREATE TABLE learned_patterns (
    id TEXT PRIMARY KEY,
    error_signature TEXT,        -- Error pattern hash
    solution_type TEXT,          -- FRAMEWORK, TWEAK, CONFIG, etc.
    solution_description TEXT,   -- Human-readable
    solution_code TEXT,          -- Actual fix (if applicable)
    success_count INTEGER,       -- Times this solution worked
    created_at TIMESTAMP,
    last_used_at TIMESTAMP
);
```

---

## 4. Debate Protocol

### 4.1 When to Trigger Debate

- Error occurs 2+ times with same signature
- New error type with no known solution
- Framework upgrade decision needed
- Architecture change proposed

### 4.2 Debate Structure

```json
{
  "id": "DEBATE-20260103-001",
  "topic": "Recurring MERGE_FAILED errors",
  "trigger": {
    "error_type": "MERGE_FAILED",
    "occurrences": 5,
    "first_seen": "2026-01-03T10:00:00Z"
  },
  "proposals": [
    {"agent": "claude-code", "solution_type": "TWEAK", "description": "Add auto-stash"},
    {"agent": "gemini-cli", "solution_type": "CONFIG", "description": "Require clean repo"}
  ],
  "votes": [],
  "status": "OPEN",
  "deadline": "2026-01-03T18:00:00Z"
}
```

### 4.3 Resolution Criteria

- **Consensus:** 2/3 agents agree on solution
- **Timeout:** If no consensus in 24h, human decides
- **Emergency:** Single agent can apply fix if severity=CRITICAL

---

## 5. Automatic Remediation

### 5.1 Pre-Approved Auto-Fixes

These fixes can be applied WITHOUT debate:

| Error Type | Auto-Fix | Condition |
|------------|----------|-----------|
| Stale IN_PROGRESS | Release to BACKLOG | Age > 30 min |
| Dirty repo merge | Auto-stash | Always |
| Lint errors | Ruff --fix | Non-semantic |
| Import errors | Auto-add to path | Known patterns |

### 5.2 Escalation Path

```
ERROR DETECTED
    |
    v
[Known Pattern?] --YES--> [Auto-Fix] --> [Verify] --> [Log]
    |
    NO
    v
[Severity?]
    |
    +-- CRITICAL --> [Apply Best-Effort Fix] + [Notify Human]
    |
    +-- HIGH ------> [Open Debate] (24h deadline)
    |
    +-- MEDIUM ----> [Open Debate] (72h deadline)
    |
    +-- LOW -------> [Log for Review]
```

---

## 6. Framework Integration Patterns

### 6.1 Adding New Framework

```
1. RESEARCH     -> Does framework solve our problem?
2. POC          -> Minimal proof-of-concept in isolated branch
3. ADAPTER      -> Write adapter implementing our Protocol
4. CONTRACT     -> Write contract tests for adapter
5. FALLBACK     -> Implement fallback when framework fails
6. INTEGRATE    -> Merge adapter (not framework code) to main
7. MONITOR      -> Track success rate for 7 days
8. GRADUATE     -> If stable, mark as "production-ready"
```

### 6.2 Framework Deprecation

When replacing Framework A with Framework B:
1. Keep both adapters active
2. Route 10% traffic to B (canary)
3. If B stable for 7 days, increase to 50%
4. If B stable for 14 days, increase to 100%
5. Keep A adapter for 30 days (rollback ready)
6. Remove A adapter after 30 days

---

## 7. Commands

```bash
# Trigger self-healing check
python scripts/ybis.py health

# Release stuck tasks
python scripts/ybis.py release --all

# Start debate
python scripts/ybis.py debate start --topic "..." --proposal "..."

# Check debate status
python scripts/ybis.py debate list --status open

# Apply learned pattern
python scripts/ybis.py pattern apply PATTERN-001
```

---

## 8. Metrics Dashboard

The system exposes metrics at: `http://localhost:8080/metrics`

Key indicators:
- **MTTR** (Mean Time To Recover): Target < 5 min for auto-fixes
- **Self-Heal Rate**: % of issues auto-resolved
- **Debate Resolution Time**: Target < 24h for HIGH severity

---

**Created:** 2026-01-03
**Status:** ACTIVE
**Owner:** System Architect
