# Policy Reference (Profiles Schema)

References:
- SECURITY.md
- CONSTITUTION.md
- INTERFACES.md

This document defines the canonical schema for `configs/profiles/*.yaml`.

## 1) Top-level fields
### profile (string)
Human-readable profile name. Example: "default", "strict".

### sandbox (object)
Controls execution isolation.
Fields:
- enabled (bool): must be true by default
- network (bool): must be false by default

Example:
```yaml
sandbox:
  enabled: true
  network: false
```

### exec (object)
Controls command execution restrictions.
Fields:
- allowlist (list[string]): allowed executables/commands

Example:
```yaml
exec:
  allowlist:
    - "python"
    - "pytest"
    - "ruff"
    - "git"
```

### paths (object)
Controls path security.
Fields:
- protected (list[string]): path prefixes that require approval

Example:
```yaml
paths:
  protected:
    - "src/ybis/syscalls/"
    - "src/ybis/orchestrator/gates.py"
```

### gates (object)
Controls deterministic gate thresholds.
Fields (minimum):
- require_approval_on_protected_paths (bool)
- max_patch_lines_without_approval (int)
- require_verifier_pass (bool)

Example:
```yaml
gates:
  require_approval_on_protected_paths: true
  max_patch_lines_without_approval: 400
  require_verifier_pass: true
```

## 2) Recording policy in runs
At run start, the active profile must be recorded as:
- a policy snapshot hash (preferred), or
- an embedded copy under artifacts/policy_snapshot.yaml

Gate decisions must reference this snapshot.

## 3) Default guarantees
Any valid profile MUST guarantee:
- sandbox enabled by default
- network disabled by default
- allowlist exists and is non-empty
- protected paths exists and is non-empty
- verifier pass required for success

## 4) Compatibility & migrations
If profile schema changes:
- increment schema_version in relevant artifacts
- document in MIGRATIONS.md
- add golden tests for gate behavior under the new schema

