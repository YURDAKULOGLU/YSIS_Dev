# TASK-New-206: Project Structure Cleanup & Standardization

**Goal:** Clean root directory, enforce ARCHITECTURE_V2.md standards, achieve professional repo structure.

**Priority:** HIGH
**Approach:** DOGFOODING - Use OrchestratorGraph to clean itself!

---

## Phase 1: Root Cleanup (Safe Moves)

### 1.1 Move Loose Files → logs/
```bash
mv brain_debug.txt logs/archive/
mv error_plan.json logs/archive/
mv meta_optimization_log.md logs/archive/
mv "Block 1" logs/archive/ || rm "Block 1"
rm nul
```

### 1.2 Move .aider cache → logs/
```bash
mkdir -p logs/aider_cache/
mv .aider.chat.history.md logs/aider_cache/
mv .aider.input.history logs/aider_cache/
```

---

## Phase 2: Directory Consolidation

### 2.1 Meta/ → docs/governance/
```bash
# Meta/ already has governance docs
mv Meta/* docs/governance/ 2>/dev/null || true
rmdir Meta 2>/dev/null || true
```

### 2.2 specs/ → docs/specs/
```bash
mkdir -p docs/specs/
mv specs/* docs/specs/ 2>/dev/null || true
rmdir specs 2>/dev/null || true
```

### 2.3 config/ → src/agentic/config/
```bash
# If config has Python modules
mv config/* src/agentic/config/ 2>/dev/null || true
rmdir config 2>/dev/null || true
```

### 2.4 Workflows/ → docs/workflows/ OR legacy/
```bash
# Determine if active or legacy first
# If legacy:
mv Workflows/ legacy/Workflows/
```

### 2.5 30_INFRASTRUCTURE/ → legacy/
```bash
mv 30_INFRASTRUCTURE/ legacy/30_INFRASTRUCTURE/
```

### 2.6 path/ → DELETE (if empty/useless)
```bash
rm -rf path/
```

### 2.7 .YBIS_Dev/ → legacy/
```bash
mv .YBIS_Dev/ legacy/.YBIS_Dev/
```

---

## Phase 3: Archive Cleanup

### 3.1 Move sandbox archives → legacy/
```bash
mkdir -p legacy/sandbox_archives/
mv .sandbox_hybrid__archived_2025_12_20/ legacy/sandbox_archives/
mv .sandbox_hybrid__archived_2025_12_20_05_46_39/ legacy/sandbox_archives/
```

---

## Phase 4: .gitignore Updates

### 4.1 Add to .gitignore:
```
# Logs
logs/
*.log

# Caches
.aider.tags.cache.v4/
__pycache__/
.pytest_cache/

# Sandboxes
.sandbox/
.sandbox_worker/
.sandbox_hybrid__archived_*/

# Temporary
nul
*.tmp
```

---

## Phase 5: Verification

### 5.1 Expected Final Structure:
```
YBIS_Dev/
├── src/agentic/          # Core code
├── tests/                # All tests
├── docs/                 # All documentation
│   ├── governance/       # (from Meta/)
│   ├── specs/            # (from specs/)
│   └── workflows/        # (from Workflows/ if active)
├── scripts/              # Utility scripts
├── docker/               # Docker config
├── Knowledge/            # Data & tasks
├── legacy/               # Archived code
│   ├── 30_INFRASTRUCTURE/
│   ├── Workflows/        (if legacy)
│   ├── .YBIS_Dev/
│   └── sandbox_archives/
├── logs/                 # Logs & caches (.gitignore'd)
│   ├── archive/          # Old logs
│   └── aider_cache/
├── README.md
├── requirements.txt
├── pyproject.toml
└── docker-compose.yml
```

### 5.2 Tests to Run:
```bash
# After cleanup, verify system still works:
python -m pytest tests/ -v
python src/agentic/core/graphs/orchestrator_graph.py --help
```

---

## Success Criteria

- [ ] Root directory has ≤10 items (only essential dirs + config files)
- [ ] No loose .py, .txt, .json files in root
- [ ] All legacy code in `legacy/`
- [ ] All docs in `docs/`
- [ ] .gitignore prevents future clutter
- [ ] All tests pass after cleanup
- [ ] `du -sh */` shows clean distribution

---

## Execution Method: DOGFOODING

**Submit this to OrchestratorGraph:**
1. SimplePlanner will break into steps
2. AiderExecutor will execute moves
3. SentinelVerifier will run tests
4. System cleans itself! 🐕

**Command:**
```bash
python run_orchestrator.py --task-file Knowledge/Tasks/backlog/TASK-New-206_DETAILED_PLAN.md
```

---

**Created:** 2025-12-21
**Assignee:** OrchestratorGraph (Autonomous)
**ETA:** ~10 minutes
