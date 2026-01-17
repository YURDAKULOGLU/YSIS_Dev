# Repository Cleanup Plan

**Date:** 2026-01-09  
**Policy:** Never delete anything. Move deprecated/orphaned files to `legacy/` instead.

## Current State Analysis
### Validation Snapshot (2026-01-09)
- Legacy content consolidated under `legacy/ybis_legacy/` (code + docs + scripts).
- `legacy/ybis_legacy/docs/00_GENESIS/` moved to `legacy/ybis_legacy/docs/00_GENESIS/` (legacy reference).
- Doc graph is generated via `python scripts/build_doc_graph.py`.

### Root Directory Issues (Verified by current tree)
1. **Non-canonical root files (move to docs/reports or legacy):**
   - `404_CAUSES_EXPLAINED.md`, `FINAL_IMPROVEMENTS.md`, `FULL_BRAIN_DUMP.md`
   - `LATEST_ORGANS_UPDATE.md`, `LIBRARY_RECOMMENDATIONS.md`
   - `MIGRATION_TECHNICAL_SPEC.md`, `MIMARI_ISIMLENDIRME_ONERILERI.md`
   - `SCRAPER_PERFORMANCE_OPTIMIZATION.md`, `SCRIPT_IMPROVEMENTS.md`
   - `SYSTEM_EVALUATION.md`, `retry_logic.md`
   - `AGENT_READ_THIS_FIRST.md` (move under `docs/` if still needed)
   - `__init__.py` at root (move to legacy/orphaned_root_files/)

2. **Non-canonical root directories (move or merge):**
   - `adapters/`, `contracts/`, `control_plane/`, `data_plane/`, `orchestrator/`,
     `services/`, `syscalls/`, `utils/` -> merge into `src/ybis/` or move to legacy
   - `config/` -> merge into `configs/` or move to legacy
   - `codebase/`, `templates/`, `examples/`, `docker/` -> move to legacy unless still used
  - `platform_data/knowledge/` -> active data root; `legacy/ybis_legacy/Knowledge` is archive

3. **Canonical root allowlist (keep):**
   - `README.md`, `AGENTS.md`
   - `pyproject.toml`, `requirements.txt`, `docker-compose.yml`
   - `.github/`, `configs/`, `docs/`, `legacy/`, `logs/`
   - `scripts/`, `src/`, `tests/`, `vendors/`
   - `platform_data/`, `workspaces/` (runtime data)

4. **Cache/venv directories (ignore via gitignore):**
   - `.venv/`, `.pytest_cache/`, `.ruff_cache/`, `.sandbox/`, `.sandbox_worker/`

5. **Stray files (move to legacy/orphaned_root_files/):**
   - `code`, `nul`, `path` (junk stubs)
   - `api.js`, `retry_config.js`
   - `workflow-registry.yaml` (move to `configs/` only if active)
## Cleanup Plan

### Phase 1: Create Archive Structure

```bash
# Create archive directories
mkdir -p legacy/orphaned_root_files/
mkdir -p legacy/orphaned_root_dirs/
mkdir -p docs/reports/
mkdir -p logs/archive/
```

### Phase 2: Move Non-Canonical Root Files

**To `docs/reports/` or legacy:**
- `404_CAUSES_EXPLAINED.md`
- `FINAL_IMPROVEMENTS.md`
- `FULL_BRAIN_DUMP.md`
- `LATEST_ORGANS_UPDATE.md`
- `LIBRARY_RECOMMENDATIONS.md`
- `MIGRATION_TECHNICAL_SPEC.md`
- `MIMARI_ISIMLENDIRME_ONERILERI.md`
- `SCRAPER_PERFORMANCE_OPTIMIZATION.md`
- `SCRIPT_IMPROVEMENTS.md`
- `SYSTEM_EVALUATION.md`
- `retry_logic.md`
- `AGENT_READ_THIS_FIRST.md`
- `__init__.py`
### Phase 3: Move Orphaned Directories

**To `legacy/orphaned_root_dirs/` or merge:**
- `adapters/` (merge into `src/ybis/adapters/` or legacy)
- `contracts/`, `control_plane/`, `data_plane/` (merge into `src/ybis/` or legacy)
- `orchestrator/`, `services/`, `syscalls/`, `utils/` (merge into `src/ybis/` or legacy)
- `config/` (merge into `configs/` or legacy)
- `codebase/`, `templates/`, `examples/`, `docker/` (legacy unless actively used)
- `platform_data/knowledge/` (active data root; archive in `legacy/ybis_legacy/Knowledge`)
### Phase 4: Move Analysis Reports

**To `docs/reports/`:**
- All `*_REPORT.md`
- All `*_ANALYSIS.md`
- All `*_SUMMARY.md`
- All `*_RESULTS.md`
- All `*_PLAN.md` (if reports)
- `yeni_yapi.md`
- `YENI_YAPI_ANALIZ_RAPORU.md`
- `temp_brainstorm_append.md`

### Phase 5: Move Core Docs to docs/
**To `docs/`:**
- `AI_START_HERE.md`
- `ARCHITECTURE.md`
- `ARCHITECTURE_V2.md`
- `DOC_INDEX.md`
- `SYSTEM_STATE.md`
- `TASKS_FOR_EXECUTOR.md`

**Keep at root:**
- `AGENTS.md` (canonical entry point)
### Phase 6: Move Logs

**To `logs/archive/`:**
- `listener.err`, `listener.log`
- `production.log`
- `scraper_run.log`
- `worker_test.err`, `worker_test.log`, `worker.out`

### Phase 7: Clean Junk Files

**Move to `legacy/orphaned_root_files/`:**
- `code`
- `nul`
- `path`
- `api.js` -> `legacy/orphaned_root_files/`
- `retry_config.js` -> `legacy/orphaned_root_files/`
- `workflow-registry.yaml` -> `configs/` or legacy
### Phase 8: Update .gitignore

Add to `.gitignore`:
```
# Root junk files
/code
/nul
/path

# Root log files
/*.log
/*.err
/worker.out
```
## Execution Order

1. **Create archive structure** (Phase 1)
2. **Move non-canonical root files** (Phase 2) - Low risk
3. **Move orphaned directories** (Phase 3) - High risk (check imports)
4. **Move analysis reports** (Phase 4) - Low risk
5. **Move core docs** (Phase 5) - Medium risk (update references)
6. **Move logs** (Phase 6) - Low risk
7. **Clean junk files** (Phase 7) - Low risk (verify empty first)
8. **Update .gitignore** (Phase 8)
9. **Regenerate doc graph** (`python scripts/build_doc_graph.py`)

## Verification

After cleanup:
- Root should only contain: `README.md`, `AGENTS.md`, `pyproject.toml`, `requirements.txt`, `docker-compose.yml`, `.gitignore`, `.editorconfig`, `.pre-commit-config.yaml`, `.github/`, `configs/`, `docs/`, `legacy/`, `logs/`, `scripts/`, `src/`, `tests/`, `vendors/`, `platform_data/`, `workspaces/`
- All code in `src/ybis/`
- All scripts in `scripts/`
- All docs in `docs/`
- All legacy in `legacy/`
- All reports in `docs/reports/`
- All logs in `logs/`
- Doc graph generates cleanly: `python scripts/build_doc_graph.py`

## Rollback Plan

All moves are reversible via git. Before executing:
1. Commit current state
2. Create branch: `cleanup/repo-organization`
3. Execute moves incrementally
4. Test after each phase
5. Merge if successful












