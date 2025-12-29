# Code Standards (Immutable)

> **Critical rules that all code (human or AI-written) MUST follow**

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

**Created:** 2025-12-20
**Status:** IMMUTABLE
**Enforcement:** STRICT
