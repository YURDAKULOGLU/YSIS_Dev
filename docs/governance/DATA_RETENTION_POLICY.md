# Data Retention & Governance Policy

**Version:** 1.0  
**Date:** 2026-01-08  
**Status:** Active

This document defines retention policies for runs, artifacts, and related data in the YBIS platform.

---

## Table of Contents

1. [Retention Periods](#retention-periods)
2. [Data Categories](#data-categories)
3. [Retention Rules](#retention-rules)
4. [Enforcement](#enforcement)
5. [Exceptions](#exceptions)
6. [Archive Process](#archive-process)

---

## Retention Periods

### Default Retention Periods

| Data Category | Retention Period | Archive Location |
|--------------|-----------------|------------------|
| **Successful Runs** | 90 days | `workspaces/archive/<task_id>/runs/<run_id>/` |
| **Failed Runs** | 30 days | `workspaces/archive/<task_id>/runs/<run_id>/` |
| **Abandoned Runs** | 7 days | `workspaces/archive/<task_id>/runs/<run_id>/` |
| **Artifacts** | Same as run | Archived with run |
| **Journal Events** | Same as run | Archived with run |
| **Control Plane DB** | Indefinite | SQLite database (no automatic deletion) |
| **Spec Files** | Indefinite | `docs/specs/` (never deleted) |

### Retention Calculation

- **Start Date:** Run creation timestamp (`created_at` from control plane DB)
- **End Date:** Start date + retention period
- **Archive Date:** When retention period expires, run is moved to archive

---

## Data Categories

### 1. Runs

**Location:** `workspaces/<task_id>/runs/<run_id>/`

**Contents:**
- Artifacts (`artifacts/`)
- Journal events (`journal/events.jsonl`)
- Code changes (git worktree)
- Policy snapshot (`artifacts/policy_snapshot.yaml`)

**Retention:**
- **Successful:** 90 days
- **Failed:** 30 days
- **Abandoned:** 7 days (no completion, no activity)

### 2. Artifacts

**Location:** `workspaces/<task_id>/runs/<run_id>/artifacts/`

**Contents:**
- `plan.json`
- `executor_report.json`
- `verifier_report.json`
- `gate_report.json`
- `spec_validation.json`
- `patch.diff`
- Other evidence files

**Retention:** Same as parent run

### 3. Journal Events

**Location:** `workspaces/<task_id>/runs/<run_id>/journal/events.jsonl`

**Contents:**
- Append-only event log
- Syscall invocations
- State transitions
- Error events

**Retention:** Same as parent run

### 4. Control Plane Database

**Location:** `platform_data/control_plane.sqlite`

**Contents:**
- Tasks table
- Runs table (includes retention_hold column for manual holds)
- Leases table
- Workers table
- Messages table
- Agents table

**Retention:** **Indefinite** (no automatic deletion)
- Historical records preserved for audit
- Can be manually pruned if needed

### 5. Spec Files

**Location:** `docs/specs/<task_id>_SPEC.md`

**Contents:**
- Task specifications
- Requirements
- Acceptance criteria

**Retention:** **Indefinite** (never deleted)
- Specs are documentation, not execution data
- Preserved for reference and compliance

---

## Retention Rules

### Rule 1: Successful Runs

**Definition:** Run with status `SUCCESS` and `gate_report.json` decision `PASS`.

**Retention:** 90 days from `created_at`.

**Archive Action:** Move entire run directory to `workspaces/archive/<task_id>/runs/<run_id>/`.

### Rule 2: Failed Runs

**Definition:** Run with status `FAILED` or `gate_report.json` decision `BLOCK`.

**Retention:** 30 days from `created_at`.

**Archive Action:** Move entire run directory to archive.

**Rationale:** Failed runs may contain debugging information but are less valuable long-term.

### Rule 3: Abandoned Runs

**Definition:** Run with status `PLANNING`, `EXECUTING`, or `VERIFYING` with no activity for 7 days.

**Retention:** 7 days from last activity.

**Archive Action:** Move entire run directory to archive.

**Rationale:** Abandoned runs are likely incomplete and consume disk space.

### Rule 4: Artifacts

**Retention:** Same as parent run.

**Archive Action:** Archived with run directory.

### Rule 5: Control Plane Metadata

**Retention:** Indefinite (no automatic deletion).

**Rationale:** Metadata is small and provides audit trail.

### Rule 6: Spec Files

**Retention:** Indefinite (never deleted).

**Rationale:** Specs are documentation and should be preserved.

---

## Enforcement

### Automated Enforcement

**Script:** `scripts/enforce_retention_policy.py`

**Schedule:** Run daily via CI or cron job.

**Actions:**
1. Scan `workspaces/` for runs exceeding retention period
2. Identify runs to archive based on status and age
3. Move runs to archive directory
4. Update control plane DB with archive status
5. Generate retention report

### Manual Enforcement

**Command:**
```bash
python scripts/enforce_retention_policy.py --dry-run  # Preview
python scripts/enforce_retention_policy.py            # Execute
```

### CI Check

**Workflow:** `.github/workflows/enforcement.yml`

**Check:** Validates that retention policy document hasn't changed without approval.

**Action:** Fails if `docs/governance/DATA_RETENTION_POLICY.md` is modified without CODEOWNER approval.

---

## Exceptions

### Exception 1: Golden Runs

**Definition:** Runs marked as "golden" in control plane DB or artifacts.

**Retention:** **Indefinite** (never archived).

**Marking:**
```json
{
  "run_id": "RUN-123",
  "metadata": {
    "golden": true,
    "golden_reason": "Reference implementation"
  }
}
```

### Exception 2: Protected Tasks

**Definition:** Tasks with `protected: true` in control plane DB.

**Retention:** **Indefinite** (never archived).

**Use Cases:**
- Critical production tasks
- Compliance-required tasks
- Reference implementations

### Exception 3: Manual Hold

**Definition:** Runs with `retention_hold = 1` in the `runs` table (INTEGER column).

**Retention:** **Indefinite** (until hold is removed).

**Storage:** Retention hold is stored in the `runs.retention_hold` INTEGER column (0 = no hold, 1 = hold active).

**Command:**
```bash
# Place hold
python scripts/enforce_retention_policy.py --hold TASK-123/RUN-456

# Remove hold
python scripts/enforce_retention_policy.py --release TASK-123/RUN-456
```

---

## Archive Process

### Archive Structure

```
workspaces/archive/
  <task_id>/
    runs/
      <run_id>/
        artifacts/
        journal/
        (same structure as active run)
```

### Archive Actions

1. **Move Run Directory:**
   ```bash
   mv workspaces/<task_id>/runs/<run_id> workspaces/archive/<task_id>/runs/<run_id>
   ```

2. **Update Control Plane DB:**
   ```sql
   UPDATE runs SET archived = 1, archived_at = CURRENT_TIMESTAMP WHERE run_id = ?;
   ```

3. **Generate Archive Manifest:**
   ```json
   {
     "run_id": "RUN-123",
     "task_id": "TASK-456",
     "archived_at": "2026-01-08T12:00:00Z",
     "retention_period": "90 days",
     "archive_reason": "Retention period expired"
   }
   ```

### Archive Cleanup

**Policy:** Archived runs can be permanently deleted after 1 year.

**Command:**
```bash
python scripts/enforce_retention_policy.py --cleanup-archives
```

**Safety:** Logs all deletions. Use `--dry-run` to preview before executing.

---

## Policy Configuration

### Retention Period Overrides

Retention periods can be overridden per profile:

```yaml
# configs/profiles/default.yaml
retention:
  successful_runs_days: 90
  failed_runs_days: 30
  abandoned_runs_days: 7
```

### Environment Variables

```bash
export YBIS_RETENTION_SUCCESSFUL_DAYS=90
export YBIS_RETENTION_FAILED_DAYS=30
export YBIS_RETENTION_ABANDONED_DAYS=7
```

---

## Compliance

### Audit Trail

All retention actions are logged:
- Archive operations
- Deletion operations
- Policy changes
- Exceptions applied

**Log Location:** `platform_data/retention_audit.log`

### Reporting

**Monthly Report:** Generated automatically showing:
- Runs archived
- Runs deleted
- Disk space reclaimed
- Policy compliance status

---

## See Also

- [Retention Enforcement Script](../../scripts/enforce_retention_policy.py)
- [Policy Reference](../POLICY_REFERENCE.md)
- [Operations Guide](../OPERATIONS.md)

