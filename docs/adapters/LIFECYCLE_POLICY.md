# Adapter Lifecycle Policy

**Version:** 1.0  
**Date:** 2026-01-08  
**Status:** Active

This document defines the lifecycle management policy for YBIS adapters, including deprecation, version pinning, and CVE response procedures.

---

## Table of Contents

1. [Adapter Maturity Levels](#adapter-maturity-levels)
2. [Version Pinning Strategy](#version-pinning-strategy)
3. [Deprecation Process](#deprecation-process)
4. [CVE Response Procedure](#cve-response-procedure)
5. [Lifecycle States](#lifecycle-states)
6. [Migration Guidelines](#migration-guidelines)

---

## Adapter Maturity Levels

Adapters are classified into three maturity levels:

### Stable
- **Definition:** Production-ready, well-tested, actively maintained
- **Requirements:**
  - Comprehensive test coverage (>80%)
  - Documented usage examples
  - No known critical bugs
  - Active maintenance (updates within 6 months)
- **Default Enablement:** Can be enabled by default in production profiles
- **Examples:** `local_coder`, `e2b_sandbox`, `redis_event_bus`

### Beta
- **Definition:** Functional but may have limitations or known issues
- **Requirements:**
  - Basic test coverage (>50%)
  - Documentation exists
  - Known limitations documented
  - Active development
- **Default Enablement:** Opt-in only (must be explicitly enabled)
- **Examples:** `chroma_vector_store`, `qdrant_vector_store`, `neo4j_graph`, `llamaindex_adapter`

### Experimental
- **Definition:** Early stage, use with caution
- **Requirements:**
  - Minimal test coverage
  - May have breaking changes
  - Not recommended for production
- **Default Enablement:** Never enabled by default
- **Examples:** None currently

---

## Version Pinning Strategy

### Dependency Version Pinning

All adapter dependencies must be pinned to specific versions in `pyproject.toml`:

```toml
[project.optional-dependencies]
adapters-chroma = [
    "chromadb>=0.4.0,<0.5.0",  # Pinned to minor version
    "litellm>=0.1.0,<0.2.0",
]
adapters-neo4j = [
    "neo4j>=5.0.0,<6.0.0",  # Pinned to major version
]
```

### Pinning Rules

1. **Stable Adapters:** Pin to minor version (e.g., `>=1.2.0,<1.3.0`)
   - Allows patch updates automatically
   - Prevents breaking changes from minor updates

2. **Beta Adapters:** Pin to major version (e.g., `>=1.0.0,<2.0.0`)
   - Allows minor and patch updates
   - More flexible for active development

3. **Experimental Adapters:** Pin to exact version (e.g., `==1.2.3`)
   - Maximum stability during experimentation
   - Requires explicit updates

### Version Update Process

1. **Security Updates:** Apply immediately (CVE response)
2. **Patch Updates:** Apply automatically (via dependency update workflow)
3. **Minor Updates:** Review changelog, test, then update
4. **Major Updates:** Full compatibility review, migration plan, then update

---

## Deprecation Process

### When to Deprecate

An adapter should be deprecated when:
- A better alternative exists
- Maintenance burden is too high
- Security concerns cannot be resolved
- Upstream project is abandoned
- Breaking changes make migration impractical

### Deprecation Timeline

1. **Announcement Phase (3 months before removal)**
   - Mark adapter as `deprecated` in `configs/adapters.yaml`
   - Add deprecation notice to adapter documentation
   - Notify users via release notes and messaging

2. **Warning Phase (1 month before removal)**
   - Log warnings when deprecated adapter is used
   - Update documentation with migration guide
   - Provide migration tools if needed

3. **Removal Phase**
   - Remove adapter from catalog
   - Remove from bootstrap registration
   - Update documentation

### Deprecation Markers

In `configs/adapters.yaml`:
```yaml
deprecated_adapter:
  name: "deprecated_adapter"
  type: "executor"
  maturity: "deprecated"  # Special maturity level
  deprecated_since: "2026-01-08"
  removal_date: "2026-04-08"
  replacement: "new_adapter"
  migration_guide: "docs/adapters/migration/deprecated_to_new.md"
```

---

## CVE Response Procedure

### Immediate Actions (Within 24 hours)

1. **Identify Affected Adapters**
   - Check CVE database for adapter dependencies
   - Review `configs/adapters.yaml` for affected versions
   - Identify all adapters using vulnerable dependency

2. **Assess Impact**
   - Determine severity (Critical, High, Medium, Low)
   - Check if adapter is enabled in production
   - Estimate exposure (number of users, systems)

3. **Mitigation Steps**
   - **Critical/High:** Disable adapter automatically via policy update
   - **Medium/Low:** Log warning, recommend update
   - Update `configs/adapters.yaml` with CVE information

### CVE Tracking in Catalog

```yaml
adapter_name:
  name: "adapter_name"
  # ... other fields ...
  cve_status:
    active_cves:
      - cve_id: "CVE-2026-XXXX"
        severity: "critical"
        affected_versions: ">=1.0.0,<1.2.0"
        fixed_version: "1.2.0"
        status: "patched"  # or "unpatched", "investigating"
        reported_date: "2026-01-08"
        patched_date: "2026-01-10"
```

### Automated CVE Checks

- **CI Integration:** Run `safety` or `pip-audit` in CI
- **Blocking:** Critical/High CVEs block adapter enablement
- **Reporting:** CVE status reported in health checks

---

## Lifecycle States

Adapters can be in one of these states:

### Active
- Adapter is available and maintained
- Can be enabled via policy
- Regular updates and bug fixes

### Deprecated
- Adapter is marked for removal
- Still functional but not recommended
- Migration to replacement recommended

### Removed
- Adapter is no longer available
- Removed from catalog and bootstrap
- Documentation archived

### Suspended
- Temporarily disabled due to critical issues
- Cannot be enabled via policy
- Awaiting fix or removal decision

---

## Migration Guidelines

### When Migrating Between Adapters

1. **Plan Migration**
   - Identify all usages of old adapter
   - Create migration task
   - Test migration in development

2. **Execute Migration**
   - Update policy profiles
   - Update code references
   - Run tests

3. **Verify Migration**
   - Run adapter conformance tests
   - Verify functionality
   - Update documentation

### Migration Checklist

- [ ] Old adapter marked as deprecated in catalog
- [ ] New adapter added to catalog
- [ ] Policy profiles updated
- [ ] Code references updated
- [ ] Tests updated
- [ ] Documentation updated
- [ ] Migration guide created
- [ ] Users notified

---

## Policy Enforcement

### Catalog Validation

The adapter catalog validator checks:
- Maturity level is valid (`stable`, `beta`, `experimental`, `deprecated`)
- Deprecation dates are in the future
- CVE status is documented for active CVEs
- Replacement adapters exist for deprecated adapters

### CI Checks

- **CVE Scan:** Run `pip-audit` or `safety` on adapter dependencies
- **Deprecation Check:** Warn if deprecated adapter is enabled
- **Version Pinning:** Verify dependencies are pinned in `pyproject.toml`

### Policy Gates

- **Deprecated Adapters:** Cannot be enabled in production profiles
- **CVE-Blocked Adapters:** Cannot be enabled if critical CVE is unpatched
- **Experimental Adapters:** Require explicit opt-in with warning

---

## Examples

### Example 1: Deprecating an Adapter

```yaml
# configs/adapters.yaml
old_adapter:
  name: "old_adapter"
  type: "executor"
  maturity: "deprecated"
  deprecated_since: "2026-01-08"
  removal_date: "2026-04-08"
  replacement: "new_adapter"
  migration_guide: "docs/adapters/migration/old_to_new.md"
```

### Example 2: CVE Response

```yaml
# configs/adapters.yaml
vulnerable_adapter:
  name: "vulnerable_adapter"
  # ... other fields ...
  cve_status:
    active_cves:
      - cve_id: "CVE-2026-1234"
        severity: "critical"
        affected_versions: ">=1.0.0,<1.3.0"
        fixed_version: "1.3.0"
        status: "unpatched"
        reported_date: "2026-01-08"
```

Policy automatically disables this adapter until CVE is patched.

---

## See Also

- [Adapter Catalog](../../configs/adapters.yaml)
- [Adapter Registry Guide](../ADAPTER_REGISTRY_GUIDE.md)
- [Adapter Conformance Tests](../../tests/adapters/)


