# T-101 (P0) Prevent AI Code Quality Regressions

**Context:** T-100 revealed that Aider (and AI agents in general) can produce buggy code:
- Wrong LangGraph API usage (`add_edge` with `condition` parameter)
- Missing imports (`datetime`)
- Incorrect test expectations
- Unicode/emoji issues on Windows

**Goal:** Build systematic prevention so AI-generated code meets quality standards BEFORE merging.

---

## Root Causes

1. **No mandatory tests** - Aider writes code but tests are optional
2. **No validation gates** - Code can be merged without verification
3. **No agent education** - Agents don't know CODE_STANDARDS.md exists
4. **No automated enforcement** - Pre-commit hooks missing

---

## Solution Architecture

### Layer 1: Agent Education (Proactive)

**Create:** `.YBIS_Dev/AGENT_ONBOARDING_CHECKLIST.md`
- Mandatory reading list for ALL agents (human or AI)
- Link to CODE_STANDARDS.md
- Link to SYSTEM_STATE.md
- Link to AI_START_HERE.md

**Update:** `run_t*.py` scripts
- Add header that loads CODE_STANDARDS into prompt
- "CRITICAL: NO EMOJIS IN CODE (Windows compatibility)"
- "CRITICAL: Test coverage required"

### Layer 2: Sentinel Enhancement (Detection)

**Update:** `src/agentic/core/plugins/sentinel.py`

Add checks:
1. **Emoji Detection:**
   ```python
   def check_no_emojis(file_path):
       with open(file_path, 'rb') as f:
           content = f.read()
       # Check for unicode emojis (U+1F300 - U+1F9FF range)
       if re.search(rb'[\xf0-\xf3][\x80-\xbf]{3}', content):
           return False, "Emoji found in code (violates CODE_STANDARDS)"
       return True, None
   ```

2. **Test Coverage Enforcement:**
   ```python
   def check_test_coverage(modified_files):
       for file in modified_files:
           if file.endswith('.py') and 'test_' not in file:
               test_file = find_test_for(file)
               if not test_file:
                   return False, f"No test file for {file}"
       return True, None
   ```

3. **Import Completeness:**
   ```python
   def check_imports(file_path):
       # Use ast to check if all used names are imported
       # Catch undefined names before runtime
       return True, None
   ```

### Layer 3: Pre-commit Hooks (Prevention)

**Create:** `.git/hooks/pre-commit`
```bash
#!/bin/bash
# Run Sentinel on staged files
python src/agentic/core/plugins/sentinel.py --staged

# Block commit if verification fails
if [ $? -ne 0 ]; then
    echo "[BLOCKED] Code standards violation"
    exit 1
fi
```

### Layer 4: Aider Prompt Enhancement (Guidance)

**Create:** `src/agentic/core/plugins/aider_executor.py` update

Inject CODE_STANDARDS into Aider prompt:
```python
def build_aider_prompt(task):
    standards = Path("00_GENESIS/CODE_STANDARDS.md").read_text()
    return f"""
{standards}

CRITICAL RULES (MUST FOLLOW):
- NO emojis in code (Windows console compatibility)
- WRITE TESTS for all code changes
- Use ASCII-only in print statements

Your task:
{task}
"""
```

---

## Implementation Plan

### Step 1: Enhance Sentinel (Priority: P0)
- Add emoji detection
- Add test coverage check
- Add import verification
- Return detailed violation reports

### Step 2: Pre-commit Hook (Priority: P0)
- Create hook script
- Make it executable
- Test with intentional violations

### Step 3: Aider Prompt Injection (Priority: P1)
- Update AiderExecutor to inject CODE_STANDARDS
- Test with a sample task

### Step 4: Agent Onboarding (Priority: P1)
- Create AGENT_ONBOARDING_CHECKLIST.md
- Add to AI_START_HERE.md
- Add to README.md

---

## Acceptance Criteria

- [ ] Sentinel detects emojis in `.py` files and fails verification
- [ ] Sentinel enforces test coverage (fails if no test for modified code)
- [ ] Pre-commit hook blocks commits with violations
- [ ] Aider receives CODE_STANDARDS in every prompt
- [ ] Test: Intentionally add emoji → commit blocked
- [ ] Test: Modify code without test → verification fails

---

## Success Metrics

**Before T-101:**
- Aider produces buggy code → Manual fixes required
- No automated quality gates

**After T-101:**
- Aider code passes quality gates automatically
- Violations caught before commit
- AI agents educated on standards

---

## Files to Modify

- `src/agentic/core/plugins/sentinel.py` (add checks)
- `src/agentic/core/plugins/aider_executor.py` (inject standards)
- `.git/hooks/pre-commit` (new file)
- `.YBIS_Dev/AGENT_ONBOARDING_CHECKLIST.md` (new file)
- `00_GENESIS/CODE_STANDARDS.md` (already exists, may enhance)

---

## Test Plan

1. **Emoji Detection Test:**
   - Add print("🎯 Test") to a .py file
   - Run Sentinel → should fail

2. **Test Coverage Test:**
   - Modify calculator.py without updating test
   - Run Sentinel → should fail

3. **Pre-commit Hook Test:**
   - Stage file with emoji
   - Try to commit → should be blocked

4. **Aider Test:**
   - Run Aider on simple task
   - Check if CODE_STANDARDS in prompt
   - Verify generated code has no emojis

---

**Strategic Value:** This is meta-level work - improving the system that improves the system.

**Dogfooding:** We'll use OrchestratorGraph to implement this, testing the retry loop we just built!

---

**Created:** 2025-12-20
**Priority:** P0 (Prevents future regressions)
**Estimated Complexity:** Medium-High
**Dependencies:** T-100 (uses retry loop)
