# DEVELOPMENT DISCIPLINE RULES

> **"Quality is not an act, it is a habit."** - Aristotle
>
> Bu doküman CONSTITUTION.md'den sonra ikinci en önemli dokümandır.
> Tüm agentler, her task'ta bu kurallara **TAM** uymalıdır.

**References:**
- CONSTITUTION.md (Supreme Law - Founding Principles)
- CODE_STANDARDS.md
- SECURITY.md
- INTERFACES.md

---

## 0. FOUNDING PRINCIPLES (Her İşten Önce Oku)

Bu iki prensip diğer tüm kuralların temelidir. (Detay: CONSTITUTION.md Section 0)

### 0.1 Self-Bootstrapping ("Dog Scales Dog")

```
Sistem kendini kendi araçlarıyla geliştirmeli.
```

**Pratik Uygulama:**
- Task'ları `python scripts/ybis_run.py TASK-XXX` ile çalıştır
- External script yazma, orchestrator'ı kullan
- Yeni feature YBIS'in işini kolaylaştırmalı
- Self-improve workflow'u test için kullan

**Soru:** "Bu değişiklik YBIS'in kendini geliştirmesini kolaylaştırıyor mu?"

### 0.2 Zero Reinvention ("Vendor First")

```
Hazır varsa KODLAMA. Adapte et.
```

**Karar Ağacı:**
```
Yeni özellik gerekiyor?
    │
    ├─► Vendor var mı? (pip search, GitHub)
    │       │
    │       ├─► EVET → pip install + adapters/<name>.py (thin wrapper)
    │       │
    │       └─► HAYIR → Emin misin? Tekrar ara.
    │               │
    │               └─► Hala yok → Custom code (minimal, sadece core için)
    │
    └─► Custom code SADECE şunlar için:
            - Task, Run, Workflow (core abstractions)
            - Syscalls (security layer)
            - Policy/Gates (enforcement)
```

**Soru:** "Bu kodu yazmadan önce vendor araştırdım mı?"

---

## I. PRE-IMPLEMENTATION CHECKLIST

**Her kod yazmadan ÖNCE bu checklist tamamlanmalı:**

### 1.0 Founding Principles Check (YENİ - En Önemli)
- [ ] **Self-Bootstrapping:** Bu task YBIS orchestrator üzerinden mi çalışacak?
- [ ] **Zero Reinvention:** Vendor araştırması yaptım mı?
  - [ ] PyPI'da aradım: `pip search <keyword>`
  - [ ] GitHub'da aradım: `<keyword> python library`
  - [ ] Vendor varsa → `adapters/` içinde thin wrapper yazacağım
  - [ ] Vendor yoksa → Custom code için onay aldım

### 1.1 Requirement Clarity
- [ ] Task objective net mi? (Ambiguous ise sor)
- [ ] Success criteria tanımlı mı?
- [ ] Edge cases listelenmiş mi?
- [ ] Scope boundaries net mi? (Ne YAPMAYACAKSIN)

### 1.2 Context Gathering
- [ ] Mevcut kod okundu mu? (Edit etmeden önce READ)
- [ ] Related files identified mi?
- [ ] Dependency impact analizi yapıldı mı?
- [ ] Breaking change riski değerlendirildi mi?

### 1.3 Design Decision
- [ ] Birden fazla approach var mı?
- [ ] Trade-offs documented mı?
- [ ] SOTA tool var mı? (Önce adapt, sonra yaz)
- [ ] Existing pattern var mı? (Consistency > Perfection)

### 1.4 Plan Approval
- [ ] Plan.json üretildi mi?
- [ ] Plan validate edildi mi?
- [ ] High-risk ise approval alındı mı?

**KURAL:** Checklist tamamlanmadan KOD YAZILMAZ.

---

## II. CODE CHANGE RULES

### 2.1 The Single Responsibility Rule
```
Bir değişiklik = Bir amaç
```
- Tek PR'da birden fazla feature YASAK
- Refactor + Feature aynı commit'te YASAK
- Bug fix + Enhancement aynı PR'da YASAK

### 2.2 The Minimal Change Rule
```
Gereken minimum değişikliği yap, fazlasını YAPMA
```
- Sadece task'ın gerektirdiği dosyalara dokun
- "While I'm here" refactoring YASAK
- Cosmetic changes (format, import sort) sadece `pre-commit` ile
- Docstring ekleme zorunlu değilse YAPMA

### 2.3 The Reversibility Rule
```
Her değişiklik geri alınabilir olmalı
```
- Breaking change öncesi deprecation period
- Database migration'lar reversible olmalı
- Feature flags ile soft launch
- Rollback planı olmadan deploy YASAK

### 2.4 The Evidence Rule
```
Kanıt yoksa, olmamıştır
```
- Her değişiklik journal'a kaydedilmeli
- Test evidence zorunlu
- Performance change'lerde benchmark evidence
- Config change'lerde before/after snapshot

---

## III. ERROR HANDLING POLICY

### 3.1 Error Classification
| Level | Name | Action | Example |
|-------|------|--------|---------|
| FATAL | System Crash | Immediate shutdown, alert | Database connection lost |
| ERROR | Operation Failed | Log, retry, escalate | LLM API timeout |
| WARN | Degraded | Log, continue with fallback | Cache miss |
| INFO | Expected | Log only | User cancelled |

### 3.2 Error Handling Pattern
```python
# DOĞRU
try:
    result = await risky_operation()
except SpecificError as e:
    append_event(ctx.run_path, "OPERATION_ERROR", {
        "error_type": type(e).__name__,
        "message": str(e),
        "recoverable": True,
    })
    return fallback_result()
except Exception as e:
    append_event(ctx.run_path, "UNEXPECTED_ERROR", {
        "error_type": type(e).__name__,
        "message": str(e),
        "traceback": traceback.format_exc()[:500],
    })
    raise

# YANLIŞ
try:
    result = await risky_operation()
except:  # Bare except YASAK
    pass   # Silent fail YASAK
```

### 3.3 Error Recovery Rules
1. **Retry:** Transient errors için (network, rate limit)
2. **Fallback:** Degraded operation mümkünse
3. **Circuit Break:** Persistent failure'da durdur
4. **Escalate:** Unknown error'ları üst seviyeye taşı

### 3.4 Error Message Standards
```python
# DOĞRU
raise ValueError(f"Invalid file path: {path!r} - must be absolute and within workspace")

# YANLIŞ
raise ValueError("bad path")  # Neden bad? Hangi path?
```

---

## IV. DEPENDENCY MANAGEMENT

### 4.1 Adding Dependencies
**Yeni dependency eklemeden ÖNCE:**

1. **Necessity Check:**
   - Bu işi stdlib ile yapabilir miyim?
   - Mevcut dependency ile yapabilir miyim?
   - 50 satır kod yazmak mı dependency eklemek mi?

2. **Quality Check:**
   - PyPI'da aktif mi? (Son release < 6 ay)
   - Maintainer güvenilir mi?
   - Test coverage var mı?
   - Security vulnerabilities var mı?

3. **Compatibility Check:**
   - Python version uyumlu mu?
   - Mevcut dependencies ile conflict var mı?
   - License uyumlu mu? (MIT, Apache, BSD OK)

4. **Approval:**
   - Core dependency (Pydantic, LangGraph) için HUMAN approval
   - Optional dependency için adapter pattern

### 4.2 Dependency Declaration
```toml
# pyproject.toml

[project]
dependencies = [
    # Core - Zorunlu
    "pydantic>=2.0,<3.0",  # Always pin major version

    # Optional - Feature-flagged
]

[project.optional-dependencies]
vector = ["chromadb>=0.4"]
graph = ["neo4j>=5.0"]
```

### 4.3 Version Pinning
| Type | Strategy | Example |
|------|----------|---------|
| Core | Pin major, allow minor | `pydantic>=2.0,<3.0` |
| DevOps | Pin exact | `ruff==0.5.0` |
| Optional | Pin major | `chromadb>=0.4` |

---

## V. API DESIGN GUIDELINES

### 5.1 Function Signatures
```python
# DOĞRU
def create_task(
    title: str,
    objective: str,
    *,  # Force keyword arguments after this
    priority: Priority = Priority.MEDIUM,
    labels: list[str] | None = None,
) -> Task:
    """Create a new task.

    Args:
        title: Short task title (max 100 chars)
        objective: Detailed description of what to achieve
        priority: Task priority level
        labels: Optional categorization labels

    Returns:
        Created Task object with generated ID

    Raises:
        ValidationError: If title is empty or too long
    """

# YANLIŞ
def create_task(title, obj, p="med", l=None):  # Cryptic, no types
    ...
```

### 5.2 Return Types
| Scenario | Return Type |
|----------|-------------|
| Success/Failure | `Result[T, E]` or `tuple[T | None, str | None]` |
| Optional value | `T | None` |
| Collection | `list[T]` (never raw `list`) |
| Dict | `dict[str, T]` (never raw `dict`) |

### 5.3 Error Signaling
```python
# Option 1: Exception (for unexpected errors)
def get_task(task_id: str) -> Task:
    task = db.find(task_id)
    if task is None:
        raise TaskNotFoundError(f"Task {task_id} not found")
    return task

# Option 2: Optional (for expected absence)
def find_task(task_id: str) -> Task | None:
    return db.find(task_id)

# Option 3: Result type (for operations that can fail)
@dataclass
class Result(Generic[T]):
    success: bool
    value: T | None = None
    error: str | None = None
```

### 5.4 Breaking Changes
**ASLA** yapmadan önce:

1. Deprecation warning ekle (1 version)
2. Migration guide yaz
3. Backward compatibility layer (if possible)
4. CHANGELOG'a ekle
5. Dependent code'u update et

```python
# Deprecation Pattern
import warnings

def old_function():
    warnings.warn(
        "old_function is deprecated, use new_function instead. "
        "Will be removed in v2.0",
        DeprecationWarning,
        stacklevel=2,
    )
    return new_function()
```

---

## VI. STATE MANAGEMENT

### 6.1 State Categories
| Category | Storage | Lifetime | Example |
|----------|---------|----------|---------|
| Ephemeral | Memory | Request | Current LLM response |
| Session | RunContext | Run | Accumulated changes |
| Persistent | Database | Forever | Task history |
| Config | YAML/ENV | Deploy | Model settings |

### 6.2 State Mutation Rules
```python
# DOĞRU - Immutable state transitions
new_state = state.copy(update={"status": "completed"})

# YANLIŞ - Direct mutation
state["status"] = "completed"  # Side effect, hard to track
```

### 6.3 Global State
```
GLOBAL STATE = YASAK (except singletons)
```

Allowed singletons:
- `get_llm_cache()` - LLM response cache
- `get_db()` - Database connection pool
- `get_config()` - Frozen config

Her singleton:
- Thread-safe olmalı
- Lazy initialization
- Clear teardown mechanism

---

## VII. ASYNC/CONCURRENCY RULES

### 7.1 Async-First
```python
# DOĞRU - All I/O is async
async def fetch_data():
    async with httpx.AsyncClient() as client:
        return await client.get(url)

# YANLIŞ - Blocking I/O in async context
async def fetch_data():
    return requests.get(url)  # BLOCKS event loop!
```

### 7.2 Concurrency Limits
| Resource | Limit | Reason |
|----------|-------|--------|
| LLM calls | 3 concurrent | Rate limits, cost |
| File I/O | 10 concurrent | OS handles |
| DB connections | 5 per pool | Connection exhaustion |
| HTTP requests | 10 concurrent | Memory, sockets |

### 7.3 Race Condition Prevention
```python
# DOĞRU - Atomic operations
async with db.transaction():
    task = await db.get_task(task_id)
    if task.status == "pending":
        await db.update_task(task_id, status="claimed")

# YANLIŞ - Check-then-act race
task = await db.get_task(task_id)
if task.status == "pending":  # Can change between check and update!
    await db.update_task(task_id, status="claimed")
```

### 7.4 Timeout Rules
| Operation | Timeout | Action on Timeout |
|-----------|---------|-------------------|
| LLM call | 120s | Retry with fallback model |
| File read | 30s | Fail |
| HTTP request | 30s | Retry 3x |
| Database query | 10s | Fail |
| Total task | 30min | Force terminate |

---

## VIII. CONFIGURATION MANAGEMENT

### 8.1 Config Hierarchy
```
1. Environment variables (highest priority)
2. configs/*.yaml
3. defaults in code (lowest priority)
```

### 8.2 Config Access Pattern
```python
# DOĞRU
from ybis.config import get_config

config = get_config()
model = config.llm.model  # Type-safe access

# YANLIŞ
import os
model = os.getenv("MODEL", "gpt-4")  # Scattered, no validation
```

### 8.3 Secret Management
```yaml
# configs/settings.yaml
llm:
  model: "gpt-4o-mini"
  api_key: "${OPENAI_API_KEY}"  # Reference env var, never store directly

# YASAK
llm:
  api_key: "sk-..."  # Never commit secrets!
```

### 8.4 Feature Flags
```yaml
# configs/features.yaml
features:
  vector_store: true       # Stable
  neo4j_graph: false       # Experimental
  council_debate: false    # Not ready
```

```python
if get_config().features.vector_store:
    # Use vector store
else:
    # Fallback
```

---

## IX. TESTING DISCIPLINE

### 9.1 Test Pyramid
```
        /\
       /E2E\         <- Few, slow, expensive
      /------\
     /Integration\   <- Medium
    /--------------\
   /     Unit       \<- Many, fast, cheap
  /------------------\
```

### 9.2 Test Requirements per Change Type
| Change Type | Unit | Integration | E2E | Golden |
|-------------|------|-------------|-----|--------|
| Bug fix | Required | If API affected | No | If regression |
| New function | Required | If I/O | No | No |
| API change | Required | Required | If user-facing | Yes |
| Config change | No | Required | No | No |
| Core change | Required | Required | Required | Required |

### 9.3 Test Naming
```python
# Pattern: test_<what>_<scenario>_<expected>
def test_create_task_with_empty_title_raises_validation_error():
    ...

def test_planner_with_no_context_returns_heuristic_plan():
    ...
```

### 9.4 Mock Rules
```python
# DOĞRU - Mock external boundaries only
@patch("litellm.acompletion")
async def test_local_coder_calls_llm(mock_llm):
    mock_llm.return_value = create_mock_response("new code")
    ...

# YANLIŞ - Over-mocking internal logic
@patch("ybis.adapters.local_coder._validate_content")  # Don't mock internals!
```

---

## X. GIT DISCIPLINE

### 10.1 Commit Message Format
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code change that neither fixes nor adds
- `docs`: Documentation only
- `test`: Adding tests
- `chore`: Maintenance (deps, config)

**Examples:**
```
feat(planner): add RAG context to plan generation

- Query vector store for relevant code context
- Include context in LLM prompt
- Add journal events for RAG queries

Refs: TASK-123
```

### 10.2 Branch Strategy
```
main (protected)
  └── develop
        ├── feature/TASK-123-add-caching
        ├── fix/TASK-124-empty-response
        └── refactor/TASK-125-cleanup
```

**Rules:**
- Direct push to `main` = YASAK
- Feature branch per task
- Squash merge to develop
- Merge develop to main with version tag

### 10.3 PR Requirements
Before merging:
- [ ] CI passes (lint + unit tests)
- [ ] Coverage not decreased
- [ ] No new type errors (mypy)
- [ ] Golden tasks pass (core subset)
- [ ] At least 1 approval (for protected paths)
- [ ] Linked to task ID

---

## XI. DOCUMENTATION REQUIREMENTS

### 11.1 What Needs Documentation
| Item | Doc Required | Location |
|------|--------------|----------|
| New public function | Docstring | In code |
| New module | Module docstring | In code |
| New adapter | Adapter doc | `docs/adapters/` |
| API change | Update existing | Relevant doc |
| Config option | Config doc | `docs/configuration.md` |
| New workflow | Workflow doc | `docs/workflows/` |

### 11.2 Docstring Standard
```python
def create_plan(
    ctx: RunContext,
    objective: str,
    *,
    max_files: int = 10,
) -> Plan:
    """Create execution plan for given objective.

    Queries RAG for relevant context, analyzes dependencies,
    and generates a structured plan via LLM.

    Args:
        ctx: Current run context with workspace path
        objective: What to achieve (clear, actionable)
        max_files: Maximum files to include in plan

    Returns:
        Plan with files, steps, and success criteria

    Raises:
        PlannerError: If LLM fails after retries
        ValidationError: If objective is empty

    Example:
        >>> plan = await create_plan(ctx, "Fix login bug")
        >>> print(plan.files)
        ['src/auth/login.py']

    Note:
        Uses RAG cache for repeated queries.
        LLM calls are logged to journal.
    """
```

---

## XII. INCIDENT RESPONSE

### 12.1 Incident Severity
| Severity | Definition | Response Time |
|----------|------------|---------------|
| P0 | System down | Immediate |
| P1 | Major feature broken | < 1 hour |
| P2 | Minor feature broken | < 4 hours |
| P3 | Cosmetic/minor | Next sprint |

### 12.2 Incident Response Flow
```
1. DETECT → Journal/Monitoring alerts
2. TRIAGE → Classify severity
3. CONTAIN → Disable feature if needed
4. DIAGNOSE → Read logs, reproduce
5. FIX → Minimal fix, not refactor
6. VERIFY → Test fix
7. DEPLOY → With rollback ready
8. POSTMORTEM → Document lessons
```

### 12.3 Postmortem Template
```markdown
# Incident: [TITLE]
Date: YYYY-MM-DD
Severity: P[0-3]
Duration: X hours

## Summary
One paragraph description.

## Timeline
- HH:MM - Event happened
- HH:MM - Detected
- HH:MM - Fixed

## Root Cause
What actually broke and why.

## Resolution
What was done to fix it.

## Lessons Learned
- What went well
- What went poorly
- Action items (with owners)

## Prevention
How to prevent recurrence.
```

---

## XIII. PERFORMANCE DISCIPLINE

### 13.1 Performance Budgets
| Operation | Budget | Alert Threshold |
|-----------|--------|-----------------|
| Plan generation | < 30s | > 45s |
| File edit (LLM) | < 60s | > 90s |
| Verification | < 120s | > 180s |
| Full workflow | < 10min | > 15min |

### 13.2 Performance Testing Rules
- Benchmark before/after for optimization PRs
- No PR that degrades performance > 10%
- Memory usage tracked per workflow
- Token count logged per LLM call

### 13.3 Optimization Rules
```
1. MEASURE first (don't guess)
2. PROFILE to find bottleneck
3. OPTIMIZE only the bottleneck
4. MEASURE again to verify
```

**YASAK:** Premature optimization without measurement.

---

## XIV. SECURITY DISCIPLINE

### 14.1 Input Validation
```python
# DOĞRU - Validate at boundaries
def create_task(title: str, objective: str) -> Task:
    if not title or len(title) > 200:
        raise ValidationError("Title must be 1-200 characters")
    if not objective:
        raise ValidationError("Objective required")
    # Now safe to use

# YANLIŞ - Trust input
def create_task(title, objective):
    return Task(title=title, objective=objective)  # SQL injection risk
```

### 14.2 Path Validation
```python
# DOĞRU
def read_file(path: Path, workspace: Path) -> str:
    resolved = path.resolve()
    if not resolved.is_relative_to(workspace):
        raise SecurityError(f"Path {path} escapes workspace")
    return resolved.read_text()

# YANLIŞ
def read_file(path: str) -> str:
    return open(path).read()  # Path traversal vulnerability!
```

### 14.3 Secret Handling
- Secrets NEVER in logs
- Secrets NEVER in journal events
- Secrets NEVER in error messages
- Secrets from env vars only

---

## XV. COMPLIANCE CHECKLIST

**Her task tamamlanmadan önce bu checklist tamamlanmalı:**

### Pre-Implementation
- [ ] Task objective understood
- [ ] Plan created and validated
- [ ] High-risk approval obtained (if needed)

### Implementation
- [ ] Single responsibility (one purpose)
- [ ] Minimal change (only what's needed)
- [ ] Error handling complete
- [ ] Journal events added
- [ ] Type hints complete

### Verification
- [ ] Unit tests pass
- [ ] Lint clean (ruff)
- [ ] Type check clean (mypy)
- [ ] Integration tests pass (if applicable)
- [ ] Golden tasks pass (core subset)

### Documentation
- [ ] Docstrings complete
- [ ] API changes documented
- [ ] CHANGELOG updated (if user-facing)

### Security
- [ ] Input validated
- [ ] Paths sanitized
- [ ] No secrets in code/logs

### Final
- [ ] verifier_report.json: PASS
- [ ] gate_report.json: PASS
- [ ] Evidence artifacts complete

---

## XVI. VIOLATION CONSEQUENCES

| Violation | Consequence |
|-----------|-------------|
| Skip pre-implementation checklist | Task rejected |
| Breaking change without deprecation | Immediate revert |
| Silent error handling | Task fails |
| Missing tests | Task incomplete |
| Missing journal events | Task incomplete |
| Secret in code | Emergency revert |
| Direct mutation of protected paths | Task blocked |

---

## XVII. EVOLUTION

Bu doküman:
- **LessonEngine** tarafından AUTO_RULES.md'ye yeni kurallar eklenir
- Persistent failure patterns → Yeni kural ekleme
- Success patterns → Best practice güncelleme

**Son güncelleme:** 2026-01-12
**Versiyon:** 1.0
