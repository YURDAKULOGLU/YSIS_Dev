# Deprecated Scripts Archive

**Purpose:** Archive for deprecated scripts that are no longer in active use.

**Policy:** Never delete anything. Move deprecated code here instead.

## Scripts

### `run_next.py`
- **Status:** Deprecated
- **Original Location:** `scripts/run_next.py`
- **Reason:** Replaced by `scripts/ybis_run.py`
- **Note:** References non-existent `run_orchestrator` module

### `run_production.py`
- **Status:** Deprecated
- **Original Location:** `scripts/run_production.py`
- **Reason:** Replaced by `scripts/ybis_worker.py`
- **Note:** References non-existent `run_orchestrator` module

### `run_graph.py`
- **Status:** Deprecated
- **Original Location:** `scripts/run_graph.py`
- **Reason:** Replaced by new orchestrator workflow
- **Note:** References non-existent `scripts/run_orchestrator` module

### `orchestrator_main.py`
- **Status:** Deprecated
- **Original Location:** `scripts/runners/orchestrator_main.py`
- **Reason:** Replaced by new orchestrator structure
- **Note:** References non-existent `scripts/run_orchestrator` module

## Migration Guide

**Old (Deprecated):**
```bash
python scripts/run_next.py
python scripts/run_production.py
```

**New (Active):**
```bash
python scripts/ybis_run.py <task_id>
python scripts/ybis_worker.py
```

## Policy

- **Never delete deprecated code**
- **Move to `legacy/deprecated_scripts/` instead**
- **Update documentation to reflect new entry points**
- **Keep for historical reference and migration purposes**


