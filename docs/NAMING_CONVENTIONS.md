# NAMING CONVENTIONS

> İsimlendirme tutarlılığı, kod okunabilirliğinin temelidir.
> Bu kurallara istisnasız uyulmalıdır.

**References:**
- CODE_STANDARDS.md
- CODEBASE_STRUCTURE.md
- PEP 8 (Python)

---

## 1. General Principles

### 1.1 Clarity Over Brevity
```python
# DOĞRU - Açık ve anlaşılır
calculate_token_count()
validate_file_path()
get_active_tasks()

# YANLIŞ - Kısa ama belirsiz
calc_tc()
val_fp()
get_at()
```

### 1.2 Consistency Over Creativity
```python
# Eğer projede "task" kullanılıyorsa, "job" kullanma
create_task()  # DOĞRU
create_job()   # YANLIŞ (inconsistent)
```

### 1.3 Domain Language
```python
# YBIS terminolojisini kullan (GLOSSARY.md'ye bak)
run_id      # DOĞRU (our term)
execution_id # YANLIŞ (not our term)

workspace   # DOĞRU
project_dir # YANLIŞ
```

---

## 2. Python Naming

### 2.1 Files/Modules

| Type | Convention | Example |
|------|------------|---------|
| Module | `snake_case.py` | `local_coder.py` |
| Package | `snake_case/` | `adapters/` |
| Test file | `test_<module>.py` | `test_planner.py` |

```python
# DOĞRU
vector_store_chroma.py
graph_store_neo4j.py
mcp_tools/

# YANLIŞ
VectorStoreChroma.py  # PascalCase
vector-store.py       # Kebab-case
vectorStore.py        # camelCase
```

### 2.2 Classes

| Type | Convention | Example |
|------|------------|---------|
| Regular class | `PascalCase` | `LocalCoderExecutor` |
| Exception | `PascalCase` + Error/Exception | `ValidationError` |
| Protocol | `PascalCase` + Protocol | `ExecutorProtocol` |
| Abstract | `Abstract` + `PascalCase` | `AbstractAdapter` |
| Mixin | `PascalCase` + Mixin | `LoggingMixin` |

```python
# DOĞRU
class TaskManager:
    pass

class ExecutorProtocol(Protocol):
    pass

class ConfigurationError(Exception):
    pass

# YANLIŞ
class taskManager:     # camelCase
class Task_Manager:    # Snake_Case
class TASKMANAGER:     # ALLCAPS
```

### 2.3 Functions/Methods

| Type | Convention | Example |
|------|------------|---------|
| Public function | `snake_case` | `create_task()` |
| Private function | `_snake_case` | `_validate_input()` |
| Async function | `snake_case` or `async_*` | `async def fetch_data()` |
| Property | `snake_case` | `@property def task_count` |

```python
# DOĞRU
def calculate_checksum():
    pass

async def fetch_context():
    pass

def _internal_helper():
    pass

# YANLIŞ
def CalculateChecksum():  # PascalCase
def calculateChecksum():  # camelCase
def CALCULATE_CHECKSUM(): # ALLCAPS
```

### 2.4 Variables

| Type | Convention | Example |
|------|------------|---------|
| Local variable | `snake_case` | `task_count` |
| Instance variable | `snake_case` | `self.task_list` |
| Private variable | `_snake_case` | `self._cache` |
| Constant | `UPPER_SNAKE_CASE` | `MAX_RETRIES` |
| Global (avoid!) | `UPPER_SNAKE_CASE` | `DEFAULT_TIMEOUT` |

```python
# DOĞRU
task_id = "TASK-123"
MAX_RETRIES = 3
_internal_cache = {}

# YANLIŞ
taskId = "TASK-123"     # camelCase
TASKID = "TASK-123"     # ALLCAPS for variable
Task_Id = "TASK-123"    # Mixed
```

### 2.5 Type Variables

```python
from typing import TypeVar

# Convention: Single uppercase letter or descriptive name
T = TypeVar("T")
K = TypeVar("K")  # Key
V = TypeVar("V")  # Value

# For constrained types
TaskT = TypeVar("TaskT", bound="Task")
AdapterT = TypeVar("AdapterT", bound="AdapterProtocol")
```

---

## 3. Special Naming Patterns

### 3.1 Boolean Variables

```python
# DOĞRU - is/has/can/should prefix
is_valid = True
has_permission = False
can_execute = True
should_retry = False

# Veya _enabled/_active suffix
cache_enabled = True
feature_active = False

# YANLIŞ
valid = True           # Ambiguous
permission = False     # Noun, not boolean
retry = False          # Verb, ambiguous
```

### 3.2 Collections

```python
# DOĞRU - Çoğul isim
tasks = []
file_paths = []
error_messages = []

# Dict için key_to_value veya key_value_map
task_to_status = {}
id_to_task_map = {}

# YANLIŞ
task_list = []     # Redundant (we know it's a list)
task_array = []    # Wrong term for Python
taskMap = {}       # camelCase
```

### 3.3 Callbacks/Handlers

```python
# DOĞRU - on_* veya *_handler
on_task_complete = lambda t: print(t)
error_handler = handle_error

# Function naming
def on_message_received():
    pass

def handle_validation_error():
    pass

# YANLIŞ
task_complete_callback = ...  # Too verbose
messageCallback = ...         # camelCase
```

### 3.4 Factory Functions

```python
# DOĞRU - create_* veya make_*
def create_task():
    pass

def make_executor():
    pass

# Singleton/registry - get_*
def get_registry():
    pass

def get_default_config():
    pass

# YANLIŞ
def task():           # Not clear it creates
def new_task():       # Less common pattern
def TaskFactory():    # Class naming for function
```

---

## 4. Configuration Naming

### 4.1 YAML Keys

```yaml
# DOĞRU - snake_case
adapters:
  local_coder:
    default_enabled: true
    max_retries: 3

# YANLIŞ
adapters:
  localCoder:           # camelCase
  local-coder:          # kebab-case
  LocalCoder:           # PascalCase
```

### 4.2 Environment Variables

```bash
# DOĞRU - UPPER_SNAKE_CASE with prefix
YBIS_ENV=production
YBIS_LOG_LEVEL=DEBUG
OPENAI_API_KEY=sk-...

# YANLIŞ
ybis_env=production    # lowercase
YbisEnv=production     # camelCase
```

### 4.3 Feature Flags

```python
# DOĞRU
ENABLE_VECTOR_STORE = True
USE_EXPERIMENTAL_PLANNER = False
SKIP_VERIFICATION = False

# Config'de
features:
  vector_store_enabled: true
  experimental_planner: false
```

---

## 5. Event/Log Naming

### 5.1 Journal Events

```python
# DOĞRU - UPPER_SNAKE_CASE, NOUN_VERB pattern
append_event(path, "TASK_CREATED", {...})
append_event(path, "FILE_WRITE_COMPLETE", {...})
append_event(path, "LLM_REQUEST_SENT", {...})
append_event(path, "VERIFICATION_FAILED", {...})

# YANLIŞ
append_event(path, "taskCreated", {...})      # camelCase
append_event(path, "task_created", {...})     # lowercase
append_event(path, "Created Task", {...})     # Spaces
```

### 5.2 Log Messages

```python
# DOĞRU - Clear, actionable
logger.info("Starting task execution", extra={"task_id": task_id})
logger.error("Failed to connect to database", extra={"error": str(e)})

# YANLIŞ
logger.info("starting")           # Too vague
logger.error("error occurred")    # Not helpful
logger.info(f"Task {task_id}")    # No verb
```

---

## 6. Database Naming

### 6.1 Tables

```sql
-- DOĞRU - snake_case, çoğul
CREATE TABLE tasks (...);
CREATE TABLE task_runs (...);
CREATE TABLE error_patterns (...);

-- YANLIŞ
CREATE TABLE Task (...);          -- PascalCase, tekil
CREATE TABLE task-runs (...);     -- kebab-case
CREATE TABLE tbl_tasks (...);     -- Prefix
```

### 6.2 Columns

```sql
-- DOĞRU - snake_case
task_id TEXT PRIMARY KEY,
created_at TEXT,
is_completed BOOLEAN,

-- YANLIŞ
TaskId TEXT,          -- PascalCase
createdAt TEXT,       -- camelCase
bCompleted BOOLEAN,   -- Hungarian notation
```

---

## 7. API Naming

### 7.1 MCP Tools

```python
# DOĞRU - verb_noun pattern
@mcp_tool
def task_create():
    pass

@mcp_tool
def task_status():
    pass

@mcp_tool
def artifact_read():
    pass

# YANLIŞ
@mcp_tool
def createTask():     # camelCase
    pass

@mcp_tool
def get_task():       # Inconsistent (task_status vs get_task)
    pass
```

### 7.2 REST Endpoints (if applicable)

```python
# DOĞRU - kebab-case for URLs
/api/v1/tasks
/api/v1/tasks/{task_id}
/api/v1/tasks/{task_id}/runs

# YANLIŞ
/api/v1/Tasks            # PascalCase
/api/v1/task_list        # snake_case in URL
```

---

## 8. Test Naming

### 8.1 Test Files

```python
# Pattern: test_<module>.py
test_planner.py
test_local_coder.py
test_verifier.py

# Feature-specific
test_planner_rag.py
test_executor_error_handling.py
```

### 8.2 Test Functions

```python
# Pattern: test_<what>_<scenario>_<expected>
def test_create_task_with_valid_input_returns_task():
    pass

def test_create_task_with_empty_title_raises_validation_error():
    pass

def test_planner_without_context_falls_back_to_heuristic():
    pass

# YANLIŞ
def test_1():           # Meaningless
def testCreateTask():   # camelCase
def test_create():      # Incomplete
```

### 8.3 Fixtures

```python
# Pattern: <noun>_<qualifier>
@pytest.fixture
def sample_task():
    pass

@pytest.fixture
def mock_llm_response():
    pass

@pytest.fixture
def tmp_workspace():
    pass
```

---

## 9. Domain-Specific Terms

### 9.1 YBIS Terminology (Use These)

| Term | NOT This |
|------|----------|
| `task` | job, work_item |
| `run` | execution, attempt |
| `workspace` | project_dir, work_dir |
| `artifact` | output, result_file |
| `syscall` | guarded_op, safe_call |
| `adapter` | integration, connector |
| `gate` | checkpoint, barrier |
| `verifier` | validator, checker |
| `planner` | strategist, analyzer |
| `executor` | implementer, coder |

### 9.2 Status Values

```python
# Task status
class TaskStatus(str, Enum):
    PENDING = "pending"
    CLAIMED = "claimed"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"

# Run status
class RunStatus(str, Enum):
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED = "blocked"

# Gate decision
class GateDecision(str, Enum):
    PASS = "pass"
    BLOCK = "block"
    REQUIRE_APPROVAL = "require_approval"
```

---

## 10. Anti-Patterns

### 10.1 Abbreviation Abuse

```python
# YANLIŞ
cfg = get_config()
ctx = get_context()
mgr = TaskManager()
proc = process_task()

# DOĞRU - Full words (except well-known)
config = get_config()
context = get_context()
manager = TaskManager()
result = process_task()

# Kabul edilebilir kısaltmalar
id, db, api, url, http, json, xml, html
ctx (for context in signatures), cfg (for config in signatures)
```

### 10.2 Type in Name

```python
# YANLIŞ
task_dict = {}
task_list = []
task_string = ""

# DOĞRU - Type hints handle this
tasks: dict[str, Task] = {}
tasks: list[Task] = []
task_id: str = ""
```

### 10.3 Meaningless Names

```python
# YANLIŞ
data = get_data()
info = get_info()
result = process()
temp = calculate()

# DOĞRU
task_context = get_task_context()
verification_report = verify_changes()
token_count = calculate_tokens()
```

---

## 11. Checklist

Before naming anything:

- [ ] Does it follow the correct case convention?
- [ ] Is it using YBIS domain terminology?
- [ ] Is it clear without abbreviations?
- [ ] Is it consistent with similar names in codebase?
- [ ] Does it describe what it IS (nouns) or what it DOES (verbs)?
- [ ] Boolean: Does it have is/has/can/should prefix?
- [ ] Collection: Is it plural?
- [ ] Would someone unfamiliar understand it?
