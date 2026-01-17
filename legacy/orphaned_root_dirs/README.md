# Orphaned Root Directories Archive

**Purpose:** Archive for root-level directories that were moved from root to maintain clean repository structure.

**Policy:** Never delete anything. These directories are kept for historical reference.

## Directories

### `codebase/`
- **Status:** Legacy
- **Original Location:** Root
- **Reason:** Legacy codebase structure, replaced by `src/ybis/`
- **Note:** Contains old structure before migration

### `templates/`
- **Status:** Legacy (if not actively used)
- **Original Location:** Root
- **Reason:** Templates should be in `templates/` at root (if canonical) or `docs/templates/`
- **Note:** Check if this is duplicate of root `templates/` or legacy

### `examples/`
- **Status:** Legacy
- **Original Location:** Root
- **Reason:** Examples should be in `docs/examples/` or `scripts/examples/`
- **Note:** Contains example scripts and runbooks

### `docker/`
- **Status:** Legacy (if not actively used)
- **Original Location:** Root
- **Reason:** Docker configs should be at root or in `.github/workflows/`
- **Note:** Check if duplicate of root `docker-compose.yml`

### `adapters/`
- **Status:** Legacy (duplicate)
- **Original Location:** Root
- **Reason:** Duplicate of `src/ybis/adapters/`
- **Note:** Moved here because canonical version exists in `src/ybis/adapters/`

### `contracts/`
- **Status:** Legacy (duplicate)
- **Original Location:** Root
- **Reason:** Duplicate of `src/ybis/contracts/`
- **Note:** Moved here because canonical version exists in `src/ybis/contracts/`

### `control_plane/`
- **Status:** Legacy (duplicate)
- **Original Location:** Root
- **Reason:** Duplicate of `src/ybis/control_plane/`
- **Note:** Moved here because canonical version exists in `src/ybis/control_plane/`

### `data_plane/`
- **Status:** Legacy (duplicate)
- **Original Location:** Root
- **Reason:** Duplicate of `src/ybis/data_plane/`
- **Note:** Moved here because canonical version exists in `src/ybis/data_plane/`

### `orchestrator/`
- **Status:** Legacy (duplicate)
- **Original Location:** Root
- **Reason:** Duplicate of `src/ybis/orchestrator/`
- **Note:** Moved here because canonical version exists in `src/ybis/orchestrator/`

### `services/`
- **Status:** Legacy (duplicate)
- **Original Location:** Root
- **Reason:** Duplicate of `src/ybis/services/`
- **Note:** Moved here because canonical version exists in `src/ybis/services/`

### `syscalls/`
- **Status:** Legacy (duplicate)
- **Original Location:** Root
- **Reason:** Duplicate of `src/ybis/syscalls/`
- **Note:** Moved here because canonical version exists in `src/ybis/syscalls/`

### `utils/`
- **Status:** Legacy (duplicate)
- **Original Location:** Root
- **Reason:** Duplicate of `src/ybis/utils/` (if exists) or legacy
- **Note:** Moved here because canonical version should be in `src/ybis/utils/`

### `config/`
- **Status:** Legacy (duplicate)
- **Original Location:** Root
- **Reason:** Duplicate of `configs/`
- **Note:** Moved here because canonical version exists in `configs/`

### `Knowledge/`
- **Status:** Legacy (if not actively used)
- **Original Location:** Root
- **Reason:** Knowledge base should be in `docs/` or `legacy/`
- **Note:** Contains old knowledge base structure

## Migration Notes

- All these directories were moved from root to maintain clean repository structure
- Canonical versions exist in proper locations (`src/ybis/`, `configs/`, `docs/`)
- These are kept for historical reference and potential code scavenging
- Never delete - always archive


