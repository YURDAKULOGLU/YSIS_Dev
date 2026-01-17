# Standards Compliance Audit Report

> **Constitution V3.0 Compliance Check**  
> **Date:** 2026-01-12  
> **Status:** ⚠️ Violations Found

---

## Executive Summary

**Total Violations Found:** 25+  
**Critical:** 2  
**High:** 8  
**Medium:** 10  
**Low:** 5+

**Compliance Score:** 75% (Needs Improvement)

---

## CRITICAL VIOLATIONS (Must Fix Immediately)

### 1. File Size Violations (Constitution VI.4)

**Rule:** Modules < 500 lines, Functions < 50 lines, Classes < 300 lines

**Violations:**
- ❌ `src/ybis/orchestrator/graph.py` - **2,471 lines** (5x limit!)
- ❌ `src/ybis/orchestrator/self_improve.py` - **1,116 lines** (2.2x limit)
- ❌ `src/ybis/orchestrator/planner.py` - **600 lines** (1.2x limit)
- ❌ `src/ybis/orchestrator/spec_validator.py` - **576 lines** (1.15x limit)
- ❌ `src/ybis/control_plane/db.py` - **529 lines** (1.05x limit)
- ❌ `src/ybis/cli/__init__.py` - **547 lines** (1.09x limit)

**Impact:** Hard to maintain, test, and understand

**Fix Required:**
- Split `graph.py` into multiple modules (nodes, state, routing)
- Extract self-improve nodes into separate files
- Split planner into smaller components
- Refactor spec_validator into smaller validators

---

### 2. Import Boundary Violations (Constitution III.5)

**Rule:** Lower layers CANNOT import from higher layers

**Violations:**
- ❌ `src/ybis/services/mcp_tools/task_tools.py` - Imports from orchestrator/workflows
- ❌ `src/ybis/services/worker.py` - Imports from orchestrator/workflows

**Impact:** Circular dependency risk, architecture violation

**Fix Required:**
- Use Protocol/Interface pattern (define in `contracts/`)
- Use Dependency Injection
- Use Registry pattern

---

## HIGH PRIORITY VIOLATIONS

### 3. Emoji Usage (Constitution VI.2)

**Rule:** No emojis in code (Windows terminal crashes)

**Violations:**
- ❌ `src/ybis/orchestrator/graph.py:174` - `📚 ERROR KNOWLEDGE BASE INSIGHTS:`
- ❌ `src/ybis/orchestrator/graph.py:226` - `⚠️ FEEDBACK FROM VERIFIER`
- ❌ `src/ybis/orchestrator/graph.py:482` - `📚 SIMILAR ERRORS FROM PAST TASKS:`
- ❌ `src/ybis/orchestrator/graph.py:496` - `⚠️ FEEDBACK FROM VERIFIER`
- ❌ `src/ybis/services/dashboard.py:40` - `📊 Factory Overview`
- ❌ `src/ybis/services/dashboard.py:67` - `📋 Task Board`
- ❌ `src/ybis/services/dashboard.py:105` - `🔍 Run Explorer`
- ❌ `src/ybis/services/dashboard.py:139` - `📜 Events Timeline`
- ❌ `src/ybis/services/dashboard.py:185` - `🔹 {event_type}`
- ❌ `src/ybis/services/dashboard.py:211` - `📝 Code Changes (Diff)`

**Fix Required:**
- Replace all emojis with plain text:
  - `📚` → `[INFO]`
  - `⚠️` → `[WARNING]`
  - `📊` → `[OVERVIEW]`
  - `📋` → `[TASK BOARD]`
  - `🔍` → `[EXPLORER]`
  - `📜` → `[TIMELINE]`
  - `🔹` → `[EVENT]`
  - `📝` → `[CHANGES]`

---

### 4. Silent Error Handling (Constitution IV.5)

**Rule:** No silent failures. All errors logged and recoverable.

**Violations Found:**
- `src/ybis/orchestrator/graph.py` - Bare except
- `src/ybis/adapters/local_coder.py` - Silent exceptions
- `src/ybis/orchestrator/planner.py` - Silent failures
- `src/ybis/services/retry.py` - Silent error handling
- `src/ybis/services/circuit_breaker.py` - Silent failures
- `src/ybis/services/rate_limiter.py` - Silent exceptions
- `src/ybis/services/shutdown_manager.py` - Silent errors
- `src/ybis/cli/__init__.py` - Silent failures
- `src/ybis/services/backup.py` - Silent exceptions
- `src/ybis/migrations/base.py` - Silent failures

**Fix Required:**
- Replace `except:` with `except SpecificError as e:`
- Add logging: `logger.error(..., exc_info=True)`
- Add journal events: `append_event(...)`
- Return fallback values or raise with context

---

### 5. Direct File I/O (Constitution II.2)

**Rule:** All mutations MUST go through `syscalls`. No direct FS writes.

**Potential Violations:**
- `src/ybis/orchestrator/graph.py` - Direct file operations
- `src/ybis/orchestrator/spec_validator.py` - Direct file reads
- `src/ybis/adapters/local_coder.py` - Direct file writes
- `src/ybis/services/llm_cache.py` - Direct file I/O
- `src/ybis/services/rag_cache.py` - Direct file I/O
- `src/ybis/services/backup.py` - Direct file operations
- `src/ybis/services/mcp_tools/artifact_tools.py` - Direct file writes
- `src/ybis/orchestrator/self_improve.py` - Direct file operations
- `src/ybis/services/error_knowledge_base.py` - Direct file I/O
- `src/ybis/services/lesson_engine.py` - Direct file writes
- `src/ybis/services/dashboard.py` - Direct file reads
- `src/ybis/services/mcp_tools/debate_tools.py` - Direct file I/O
- `src/ybis/services/staleness.py` - Direct file operations
- `src/ybis/adapters/e2b_sandbox.py` - Direct file I/O
- `src/ybis/syscalls/fs.py` - This is OK (it IS the syscall)
- `src/ybis/dependencies/graph.py` - Direct file operations
- `src/ybis/syscalls/exec.py` - This is OK (it IS the syscall)
- `src/ybis/data_plane/journal.py` - This is OK (journal writer)
- `src/ybis/orchestrator/artifact_expansion.py` - Direct file operations

**Fix Required:**
- Replace all `path.write_text()` with `write_file(path, content, ctx)`
- Replace all `path.read_text()` with `read_file(path, ctx)` (if syscall exists)
- Ensure all file operations go through `syscalls/fs.py`

---

### 6. Missing Journal Events (Constitution II.5)

**Rule:** Every operation MUST emit journal events. No event = didn't happen.

**Areas to Check:**
- File operations without journal events
- LLM calls without journal events
- Database operations without journal events
- Command executions without journal events
- State transitions without journal events

**Fix Required:**
- Add `append_event()` calls to all operations
- Ensure trace_id is passed through
- Log all mutations, not just successful ones

---

### 7. Type Hints Missing (Constitution IV.4)

**Rule:** All public APIs MUST have complete type hints.

**Areas to Check:**
- Public functions without return types
- Function parameters without types
- Class methods without type hints

**Fix Required:**
- Add type hints to all public functions
- Use `mypy` to check compliance
- Fix all mypy errors

---

### 8. Subprocess Usage (Constitution II.2)

**Rule:** All command execution MUST go through `syscalls/exec.py`.

**Violations:**
- `src/ybis/cli/__init__.py` - Direct subprocess calls
- `src/ybis/orchestrator/self_improve.py` - Direct subprocess.run
- `src/ybis/orchestrator/sentinel.py` - Direct subprocess
- `src/ybis/services/staleness.py` - Direct subprocess
- `src/ybis/dependencies/graph.py` - Direct subprocess
- `src/ybis/services/code_graph.py` - Direct subprocess
- `src/ybis/services/mcp_tools/test_tools.py` - Direct subprocess
- `src/ybis/syscalls/exec.py` - This is OK (it IS the syscall)
- `src/ybis/syscalls/git.py` - This is OK (it IS the syscall)

**Fix Required:**
- Replace `subprocess.run()` with `run_command()` from `syscalls/exec.py`
- Ensure all commands are logged to journal
- Pass `RunContext` for proper logging

---

## MEDIUM PRIORITY VIOLATIONS

### 9. Naming Convention Violations (Constitution VI.2)

**Potential Issues:**
- Check for camelCase in Python code
- Check for inconsistent naming patterns
- Check for abbreviations

**Fix Required:**
- Run `ruff check` with naming rules
- Review `docs/NAMING_CONVENTIONS.md`
- Fix all violations

---

### 10. Directory Discipline (Constitution VI.1)

**Check:**
- Files in wrong directories
- Missing `__init__.py` files
- Incorrect package structure

**Fix Required:**
- Review `docs/CODEBASE_STRUCTURE.md`
- Move files to correct locations
- Add missing `__init__.py` files

---

## LOW PRIORITY VIOLATIONS

### 11. Documentation Missing

**Check:**
- Public functions without docstrings
- Complex logic without comments
- Missing module docstrings

**Fix Required:**
- Add docstrings to all public functions
- Document complex algorithms
- Add module-level docstrings

---

### 12. Test Coverage

**Check:**
- Critical paths without tests
- Missing unit tests
- Missing integration tests

**Fix Required:**
- Add tests for critical paths
- Increase coverage to 60%+ (Constitution V.3)

---

## Priority Fix Order

### Phase 1: Critical (Week 1)
1. ✅ Fix file size violations (split large files)
2. ✅ Fix import boundary violations
3. ✅ Remove all emojis

### Phase 2: High Priority (Week 2)
4. ✅ Fix silent error handling
5. ✅ Replace direct file I/O with syscalls
6. ✅ Add missing journal events
7. ✅ Add type hints to public APIs
8. ✅ Replace subprocess calls with syscalls

### Phase 3: Medium Priority (Week 3)
9. ✅ Fix naming convention violations
10. ✅ Fix directory discipline issues

### Phase 4: Low Priority (Week 4)
11. ✅ Add missing documentation
12. ✅ Increase test coverage

---

## Automated Detection

**Tools to Use:**
- `ruff check` - Linting and naming
- `mypy` - Type checking
- `import-linter` - Import boundary checks
- `scripts/check_emoji.py` - Emoji detection
- Custom script for file size checks
- Custom script for syscall bypass detection

---

## Compliance Checklist

Before marking as compliant:
- [ ] All file size violations fixed
- [ ] All import boundary violations fixed
- [ ] All emojis removed
- [ ] All silent error handling fixed
- [ ] All direct file I/O replaced with syscalls
- [ ] All operations emit journal events
- [ ] All public APIs have type hints
- [ ] All subprocess calls use syscalls
- [ ] All naming conventions followed
- [ ] All directory discipline followed
- [ ] All documentation complete
- [ ] Test coverage > 60%

---

**Last Updated:** 2026-01-12  
**Next Review:** After Phase 1 fixes

