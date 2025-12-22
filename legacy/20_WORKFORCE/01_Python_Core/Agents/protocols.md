# AI Agent Communication Protocols v1.0

## 1. Temel İlkeler

### 1.1 Constitution Compliance
Tüm agent'lar `.YBIS_Dev/Meta/Governance/Constitution.md` kurallarına MUTLAK uyar.
Violation = Immediate task rejection.

### 1.2 Zero Tolerance Rules
- ❌ `any` type kullanımı
- ❌ `@ts-ignore` kullanımı
- ❌ `console.log` (sadece `logger` kullan)
- ❌ Direct vendor imports (Port pattern zorunlu)

## 2. İletişim Protokolü

### 2.1 Task Handoff Format
```yaml
handoff:
  from: "<agent_id>"
  to: "<agent_id>"
  task_id: "<uuid>"
  context:
    files_modified: []
    decisions_made: []
    blockers: []
  status: "ready" | "blocked" | "review_needed"
```

### 2.2 Feedback Loop
```
Developer -> Code -> QA Check -> FAIL -> Developer (max 3 iterations)
                             -> PASS -> Code Review -> FAIL -> Developer
                                                    -> PASS -> Merge Ready
```

## 3. Escalation Rules

| Condition | Action |
|-----------|--------|
| 3x QA Fail | Escalate to Architect |
| Security Issue | Immediate halt, notify human |
| Constitution Violation | Auto-reject, log incident |
| Model uncertainty > 0.7 | Request human review |

## 4. Tool Usage Rules

### 4.1 File Operations
- ALWAYS read before write
- NEVER overwrite without diff check
- Use atomic operations for critical files

### 4.2 Git Operations
- Branch naming: `agent/<agent_id>/<task_id>`
- Commit format: `[<agent_id>] <type>: <message>`
- NO force push ever

### 4.3 Code Execution
- Sandbox required for untrusted code
- Timeout: 30s default, 120s max
- Memory limit: 512MB
