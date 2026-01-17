# Sandbox Profile Validation Matrix

**Version:** 1.0  
**Date:** 2026-01-08  
**Status:** Active

This document defines the known-good profile matrix for sandbox configurations, ensuring safety guarantees across different execution environments.

---

## Profile Safety Guarantees

All profiles MUST guarantee:
1. **Sandbox enabled by default** (`sandbox.enabled: true`)
2. **Network disabled by default** (`sandbox.network: false`)
3. **Non-empty allowlist** (`exec.allowlist` must contain at least one command)
4. **Non-empty protected paths** (`paths.protected` must contain at least one path)
5. **Verifier pass required** (`gates.require_verifier_pass: true`)

---

## Known-Good Profile Matrix

### Profile: `default`

**Sandbox Configuration:**
- `sandbox.enabled: true` ✅
- `sandbox.type: "e2b"` (E2B cloud sandbox)
- `sandbox.network: false` ✅

**Safety Level:** **HIGH**
- ✅ Isolated cloud execution
- ✅ Network disabled
- ✅ Automatic cleanup
- ⚠️ Requires E2B API key (external dependency)

**Use Cases:**
- Production tasks requiring isolation
- Tasks that may need network access (can be enabled per-task)
- High-security requirements

**Known Issues:**
- E2B service dependency (may be unavailable)
- Falls back to local execution if E2B unavailable

---

### Profile: `e2e`

**Sandbox Configuration:**
- `sandbox.enabled: true` ✅
- `sandbox.type: "local"` (subprocess execution)
- `sandbox.network: false` ✅

**Safety Level:** **MEDIUM**
- ✅ Network disabled
- ✅ Allowlist enforced
- ⚠️ Local execution (no isolation)
- ⚠️ No automatic cleanup

**Use Cases:**
- End-to-end testing
- Local development
- CI/CD pipelines

**Known Issues:**
- No process isolation (runs on host)
- File system access not restricted
- Requires careful allowlist management

---

### Profile: `strict`

**Sandbox Configuration:**
- `sandbox.enabled: true` ✅
- `sandbox.type: "local"` (subprocess execution)
- `sandbox.network: false` ✅

**Safety Level:** **HIGH** (for local mode)
- ✅ Network disabled
- ✅ Minimal allowlist
- ✅ Broad protected paths
- ⚠️ Local execution (no isolation)

**Use Cases:**
- High-security local tasks
- Code review workflows
- Sensitive data processing

**Known Issues:**
- No process isolation
- Requires strict allowlist management

---

## Sandbox Type Safety Comparison

| Sandbox Type | Isolation | Network Control | Cleanup | Safety Level | Status |
|-------------|-----------|----------------|---------|--------------|--------|
| `e2b`       | ✅ High   | ✅ Enforced    | ✅ Auto | **HIGH**     | ✅ **Available** |
| `local`     | ❌ None   | ✅ Enforced    | ❌ None | **MEDIUM**   | ✅ **Available** |
| `docker`    | ✅ High   | ✅ Enforced    | ✅ Auto | **HIGH**     | ⚠️ **Planned Only** |

**Note:** `docker` type is **planned but not yet implemented**. Profiles using `docker` will fail validation.

---

## Profile Validation Rules

### Rule 1: Sandbox Must Be Enabled
```yaml
sandbox:
  enabled: true  # REQUIRED
```

**Validation:** `sandbox.enabled` must be `true` or missing (defaults to `true`).

### Rule 2: Network Must Be Disabled by Default
```yaml
sandbox:
  network: false  # REQUIRED (default)
```

**Validation:** `sandbox.network` must be `false` or missing (defaults to `false`).

### Rule 3: Allowlist Must Be Non-Empty
```yaml
exec:
  allowlist:
    - "python"
    - "pytest"
    # At least one command required
```

**Validation:** `exec.allowlist` must be a list with at least one element.

### Rule 4: Protected Paths Must Be Non-Empty
```yaml
paths:
  protected:
    - "src/ybis/contracts/"
    # At least one path required
```

**Validation:** `paths.protected` must be a list with at least one element.

### Rule 5: Verifier Pass Required
```yaml
gates:
  require_verifier_pass: true  # REQUIRED
```

**Validation:** `gates.require_verifier_pass` must be `true` or missing (defaults to `true`).

---

## Profile Compatibility Matrix

| Profile | Sandbox Type | Network | Allowlist | Protected Paths | Verifier Pass | Status |
|---------|-------------|---------|-----------|----------------|---------------|--------|
| `default` | `e2b` | ❌ | ✅ | ✅ | ✅ | ✅ **VALID** |
| `e2e` | `local` | ❌ | ✅ | ✅ | ✅ | ✅ **VALID** |
| `strict` | `local` | ❌ | ✅ | ✅ | ✅ | ✅ **VALID** |

---

## Validation Checklist

Before using a profile in production:

- [ ] Sandbox enabled (`sandbox.enabled: true`)
- [ ] Network disabled (`sandbox.network: false`)
- [ ] Allowlist non-empty (`exec.allowlist` has items)
- [ ] Protected paths non-empty (`paths.protected` has items)
- [ ] Verifier pass required (`gates.require_verifier_pass: true`)
- [ ] Sandbox type is valid (`e2b` or `local` - `docker` is planned but not implemented)
- [ ] Adapter configuration matches sandbox type
  - `e2b` type → `adapters.e2b_sandbox.enabled: true`
  - `local` type → `adapters.e2b_sandbox.enabled: false`

---

## See Also

- [Policy Reference](../POLICY_REFERENCE.md)
- [Security Documentation](../SECURITY.md)
- [Sandbox Profile Validation Script](../../scripts/validate_sandbox_profiles.py)

