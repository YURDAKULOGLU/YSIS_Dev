# Code Standards V1.3 (Immutable)

> **Critical rules that all code (human or AI-written) MUST follow**
>
> **Updated:** 2025-12-31 - Added rules from Pipeline Stabilization Debate

---

## 1. Windows Console Compatibility (CRITICAL)

**Problem:** Windows console (cmd.exe, PowerShell) uses cp1254 encoding which cannot render Unicode emojis and special characters.

**Rule:** **NO EMOJIS OR UNICODE DECORATIONS IN CODE**

### ❌ FORBIDDEN:
```python
# BAD - Will crash on Windows console
print("🎯 Task started")
print("✅ Success!")
print("→ Next step")
print("📊 Results:")
```

### ✅ ALLOWED:
```python
# GOOD - ASCII only
print("[TASK] Task started")
print("[OK] Success!")
print("[NEXT] Next step")
print("[RESULTS] Results:")
```

### Scope:
- **All print() statements**
- **All log messages**
- **All string literals in code**
- **All comments** (use ASCII only)
- **Documentation markdown** (use ASCII alternatives: `->, <=, >=`)

### Exceptions:
- **README.md and documentation FOR HUMANS ONLY** can use emojis (not parsed by Python)
- **Task specification files** (.md in Knowledge/Tasks/) - use ASCII arrows `->` not `→`

---

## 2. Path Management (from SYSTEM_STATE.md)

**Rule:** NEVER hardcode paths.

### ❌ FORBIDDEN:
```python
path = "C:/Projeler/YBIS_Dev/src"
path = "../Knowledge/LocalDB"
```

### ✅ ALLOWED:
```python
from src.agentic.core.config import PROJECT_ROOT, DATA_DIR
path = PROJECT_ROOT / "src"
path = DATA_DIR / "tasks.db"
```

---

## 3. Async Execution (from SYSTEM_STATE.md)

**Rule:** Long-running tasks MUST use auto_dispatcher.

### ❌ FORBIDDEN:
```bash
python run_stress_test.py  # Blocks shell
```

### ✅ ALLOWED:
```bash
python src/agentic/core/auto_dispatcher.py run_stress_test.py
```

---

## 4. Verification Gate (from SYSTEM_STATE.md)

**Rule:** NO code commits without passing Sentinel verification.

### ❌ FORBIDDEN:
```python
# Commit without verification
os.system("git add . && git commit -m 'fix'")
```

### ✅ ALLOWED:
```python
# Verify first
verification = await sentinel.verify(code_result, sandbox_path)
if not verification.tests_passed:
    raise Exception("Tests failed - cannot commit")
# Then commit
```

---

## 6. Clean Output - No Editing Artifacts (CRITICAL)

**Problem:** AI code editors (Aider, Cursor, etc.) sometimes leave editing artifacts in the final output (markdown syntax, search/replace markers, merge conflict markers).

**Rule:** **CODE FILES MUST CONTAIN ONLY VALID PYTHON - NO EDITING ARTIFACTS**

### ❌ FORBIDDEN:

```python
# BAD - Markdown code fence left in Python file
def foo():
    return "bar"

```
Some explanation text
```

# BAD - Search/replace markers left in code
def foo():
    return "bar"

<<<<<<< SEARCH
old_code()
======= REPLACE
new_code()
>>>>>>>

# BAD - Merge conflict markers
def foo():
<<<<<<< HEAD
    return "old"
=======
    return "new"
>>>>>>> branch
```

### ✅ ALLOWED:

```python
# GOOD - Clean Python code only
def foo():
    return "bar"

def baz():
    return "qux"
```

### Forbidden Patterns:

1. **Markdown code fences:** ` ``` ` at start of line
2. **Search/replace markers:** `<<<<<<< SEARCH`, `======= REPLACE`, `>>>>>>>`
3. **Merge conflict markers:** `<<<<<<< HEAD`, `<<<<<<< ORIGINAL`, `<<<<<<< UPDATED`
4. **Diff markers:** `--- a/file.py`, `+++ b/file.py` (in code, not in diffs)

### Scope:

- **All Python files** (`.py`)
- **All code files** (not documentation `.md` files)
- **Applies to:** AI-generated code, human code, refactored code

### Detection:

SentinelVerifierEnhanced automatically checks for these patterns and **BLOCKS** code with artifacts.

---

## Enforcement

### For AI Agents:
- **Pre-commit hook:** Check for emojis and artifacts in `.py` files
- **Aider prompt:** Include "NO EMOJIS - ASCII only, NO MARKDOWN ARTIFACTS" in system prompt
- **Sentinel:** Automatic detection of:
  - Emoji violations
  - Import path errors
  - Aider artifacts (markdown, search/replace markers)

### For Humans:
- **Code review:** Reject PRs with emojis or artifacts in code
- **Linter rule:** Add custom rule to detect non-ASCII and artifacts in code

---

## Violation Handling:

**If emoji found in code:**
1. Verification MUST fail
2. Error message: "CODE_STANDARDS violation: Emoji found in {file}:{line}"
3. Retry with error feedback to AI
4. Agent must fix before proceeding

**If Aider artifact found in code:**
1. Verification MUST fail
2. Error message: "AIDER ARTIFACT in {file}:{line} - {description}"
3. Retry with error feedback to AI
4. Agent must remove artifacts before proceeding

---

## 7. MANDATORY TEST PARITY (Section 3.1) - NEW

**Problem:** Code without tests cannot be verified for correctness and leads to regressions.

**Rule:** **NO NEW .py FILE WITHOUT CORRESPONDING TEST FILE**

### Requirements:
- Every new `.py` file in `src/` MUST have a corresponding `tests/unit/test_<name>.py`
- Tests must be created in the SAME commit/PR as the code
- `verify_code.py` enforces this rule automatically

### FORBIDDEN:
```bash
# Creating code without tests
git add src/new_module.py
git commit -m "add new module"  # BLOCKED - no tests
```

### ALLOWED:
```bash
# Creating code WITH tests
git add src/new_module.py tests/unit/test_new_module.py
git commit -m "add new module with tests"  # OK
```

---

## 8. NO MAGIC NUMBERS (PLR2004)

**Problem:** Magic numbers make code hard to understand and maintain.

**Rule:** **ALL NUMERIC CONSTANTS MUST BE NAMED**

### FORBIDDEN:
```python
# BAD - What does 500 mean?
doc_preview = doc[:500] + "..."
if retry_count > 3:
    raise Exception("Too many retries")
```

### ALLOWED:
```python
# GOOD - Self-documenting
DOC_PREVIEW_MAX_LENGTH = 500
MAX_RETRY_COUNT = 3

doc_preview = doc[:DOC_PREVIEW_MAX_LENGTH] + "..."
if retry_count > MAX_RETRY_COUNT:
    raise Exception("Too many retries")
```

**Enforcement:** Ruff PLR2004 (enabled by default)

---

## 9. NO GLOBAL STATEMENT (PLW0603)

**Problem:** Global statements make code hard to test and reason about.

**Rule:** **USE CLASS-BASED PATTERNS INSTEAD OF GLOBAL**

### FORBIDDEN:
```python
# BAD - Global mutable state
_instance = None

def get_instance():
    global _instance  # VIOLATION
    if _instance is None:
        _instance = MyClass()
    return _instance
```

### ALLOWED:
```python
# GOOD - Class-based singleton
class _SingletonHolder:
    _instance: MyClass | None = None

    @classmethod
    def get_instance(cls) -> MyClass:
        if cls._instance is None:
            cls._instance = MyClass()
        return cls._instance

def get_instance() -> MyClass:
    return _SingletonHolder.get_instance()
```

**Enforcement:** Ruff PLW0603 (enabled by default)

---

## 10. PRE-COMMIT MUST PASS

**Problem:** Bypassing pre-commit hooks leads to broken builds and lint errors.

**Rule:** **git commit --no-verify IS FORBIDDEN (except emergencies)**

### FORBIDDEN:
```bash
# BAD - Bypassing hooks
git commit --no-verify -m "quick fix"
```

### ALLOWED:
```bash
# GOOD - Let hooks run
git commit -m "fix: resolved issue"

# EMERGENCY ONLY (must log reason):
git commit --no-verify -m "EMERGENCY: [reason] - pre-commit broken by repo state"
```

**Exception Conditions:**
- Pre-commit hook itself is broken (not the code)
- MUST log the reason in commit message
- MUST fix and re-enable hooks in next commit

---

## 11. LIVE OUTPUT FOR LONG-RUNNING PROCESSES

**Problem:** Silent processes make debugging impossible when they hang or fail.

**Rule:** **PROCESSES > 30 SECONDS MUST STREAM OUTPUT**

### Requirements:
- Live output to console with timestamps
- Output must be written to log file simultaneously
- Must show elapsed time on completion

### FORBIDDEN:
```python
# BAD - Silent execution
result = await asyncio.wait_for(process.wait(), timeout=300)
# No idea what happened for 5 minutes
```

### ALLOWED:
```python
# GOOD - Live streaming
print("[Process] === LIVE OUTPUT START ===")
async for line in process.stdout:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {line}")
    log_file.write(f"[{ts}] {line}")
elapsed = time.time() - start
print(f"[Process] === END === (elapsed: {elapsed:.1f}s, exit: {process.returncode})")
```

---

## 12. PARSE TOOL OUTPUT FOR SUCCESS DETECTION

**Problem:** Exit code alone is not sufficient to determine if a tool succeeded.

**Rule:** **PARSE STDOUT/STDERR FOR SUCCESS INDICATORS**

### Requirements:
- Check for tool-specific success markers (e.g., "Applied edit to")
- Check for failure signatures in output
- Don't rely only on exit code

### Example (Aider):
```python
# Check Aider's actual output
applied_edits = re.findall(r"Applied edit to ([^\n]+)", stdout)
if applied_edits:
    actual_files = {path: "Modified" for path in applied_edits}
elif exit_code == 0:
    # Exit code OK but no edits - might be a no-op
    actual_files = {}
```

---

## 13. POST-COMMIT MEMORY TRIGGER (Section 4.2)

**Problem:** RAG index becomes stale, leading to context drift in AI assistants.

**Rule:** **EVERY SUCCESSFUL TASK MUST TRIGGER RAG DELTA-INGESTION**

### Requirements:
- After task completion, index modified files into RAG
- Keep Knowledge Base (ChromaDB) fresh
- Maximum staleness: 1 hour

### Implementation:
```python
# After successful task commit
if task.status == "COMPLETED":
    for file in task.modified_files:
        rag.add_code_file(file)
    print(f"[RAG] Delta-ingested {len(task.modified_files)} files")
```

---

**Created:** 2025-12-20
**Updated:** 2025-12-31 (V1.3 - Pipeline Stabilization Rules)
**Status:** IMMUTABLE
**Enforcement:** STRICT
