# Legacy Contamination Analysis

**Date:** 2026-01-09  
**Purpose:** Identify files in new structure (`src/ybis/`) that are influenced by or mixed with legacy patterns.

## Summary

Analysis of `src/ybis/data_plane/git_workspace.py` and related files to identify legacy contamination.

## Findings

### 1. Git Worktree Implementation

**File:** `src/ybis/data_plane/git_workspace.py`  
**Status:** ✅ **CLEAN** - New implementation, not directly importing from legacy

**Legacy Equivalent:** `legacy/ybis_legacy/src/agentic/core/plugins/git_manager.py` (GitWorktreeManager)

**Differences:**
- **New:** Uses GitPython adapter pattern, lazy imports, journal events
- **Legacy:** Uses subprocess git commands, direct file operations
- **New:** Simpler API (`init_git_worktree`, `cleanup_git_worktree`)
- **Legacy:** More complex class-based API with merge strategies

**Conclusion:** New implementation is a clean rewrite, not a copy. No contamination.

### 2. Sentinel V2

**File:** `src/ybis/orchestrator/sentinel.py`  
**Status:** ⚠️ **COMMENT REFERENCE** - Mentions legacy but doesn't import

**Legacy Reference:**
```python
# Line 4: "Ports advanced verification logic from legacy sentinel_enhanced.py."
```

**Legacy Equivalent:** `legacy/ybis_legacy/src/agentic/core/plugins/sentinel_enhanced.py`

**Analysis:**
- No direct imports from legacy
- Comment indicates inspiration but implementation is new
- Checks for legacy imports as architectural violation (line 43, 228, 254)

**Conclusion:** Clean implementation with documentation reference. No contamination.

### 3. Deprecated Scripts

**Files:** `scripts/run_next.py`, `scripts/run_production.py`, `scripts/run_graph.py`, `scripts/runners/orchestrator_main.py`

**Status:** ✅ **REMOVED** - Deprecated scripts have been deleted

**Action Taken:**
- All deprecated wrapper scripts removed
- References updated in documentation
- New entry points: `scripts/ybis_run.py` and `scripts/ybis_worker.py`

**Conclusion:** Cleaned up. No longer present in codebase.

### 4. Workspace Management

**File:** `src/ybis/data_plane/workspace.py`  
**Status:** ✅ **CLEAN** - New implementation

**Legacy Equivalent:** `legacy/ybis_legacy/src/agentic/core/workspace.py` (WorkspaceManager)

**Differences:**
- **New:** Simple function-based API, uses git_workspace adapter
- **Legacy:** Class-based with PLAN.md/RESULT.md stub generation
- **New:** Focus on run structure (artifacts/, journal/)
- **Legacy:** Focus on task workspace (docs/, artifacts/)

**Conclusion:** Different purpose and implementation. No contamination.

## Recommendations

### High Priority

1. ~~**Fix Deprecated Scripts:**~~ ✅ **COMPLETED**
   - Deprecated scripts removed
   - Documentation updated

### Medium Priority

2. **Documentation:**
   - Add note in `sentinel.py` that legacy reference is for historical context only
   - Consider removing comment if it causes confusion

### Low Priority

3. **Code Review:**
   - Verify no other files have hidden legacy dependencies
   - Run `grep -r "from.*legacy\|import.*legacy" src/ybis/` regularly

## Verification

```bash
# Check for legacy imports in new structure
grep -r "from.*legacy\|import.*legacy" src/ybis/
# Result: Only comments, no actual imports

# Check for agentic imports
grep -r "from.*agentic\|import.*agentic\|src\.agentic" src/ybis/
# Result: No matches

# Check scripts for legacy references
grep -r "from.*legacy\|import.*legacy\|from.*agentic" scripts/
# Result: Only deprecated wrappers with broken references
```

## Conclusion

**Overall Status:** ✅ **CLEAN**

The new structure (`src/ybis/`) is clean and does not import from legacy. The only issues are:
1. Deprecated scripts with broken references (not legacy contamination)
2. Comment references to legacy (documentation only, not code dependency)

No action required for legacy contamination. Fix deprecated script references.

