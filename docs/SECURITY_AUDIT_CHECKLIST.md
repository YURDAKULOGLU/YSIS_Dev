# Security Audit Checklist

Purpose:
A short, repeatable checklist to run before declaring a release/stable snapshot.

References:
- CONSTITUTION.md
- SECURITY.md
- INTERFACES.md
- TESTING.md
- MIGRATIONS.md

## Scope
Applies to:
- any tagged release
- any "stable snapshot" used as a base in other projects
- any change affecting syscalls, gates, sandbox, approvals, migrations

---

## A) Policy & Profiles
- [ ] `configs/profiles/default.yaml` exists and is valid YAML
- [ ] `configs/profiles/strict.yaml` exists and is valid YAML
- [ ] Default profile: sandbox enabled and network disabled by default
- [ ] Exec allowlist is defined and minimal
- [ ] Protected paths list exists and is not empty
- [ ] Gate thresholds are defined (patch size, approval requirements)

Evidence:
- [ ] A run artifact includes a policy snapshot reference (hash or embedded copy)

---

## B) Syscalls Enforcement
- [ ] No mutating operation bypasses syscalls (spot-check: fs writes, patch apply, exec, git commit)
- [ ] Syscalls validate paths (no traversal like `../`)
- [ ] Syscalls emit evidence artifacts + journal events
- [ ] Syscalls reject writes to protected paths unless approval present

Evidence:
- [ ] `patch_apply_report.json` written on patch application
- [ ] `exec_report.json` (or equivalent) written on command execution
- [ ] `journal/events.jsonl` contains syscall events

---

## C) Sandbox Safety
- [ ] Sandbox is ON by default for exec
- [ ] Network is OFF by default
- [ ] Only allowlisted commands can run
- [ ] Sandbox file mounts are minimal (no full host FS exposure)
- [ ] Secrets are not mounted into sandbox by default

Evidence:
- [ ] Sandbox profile recorded in exec evidence report

---

## D) Approval & Protected Changes
- [ ] Changes to protected paths require approval (enforced by gates)
- [ ] Approval artifact format exists and is stable
- [ ] Gate decision cannot be overridden by debate output

Evidence:
- [ ] `gate_report.json` references approval state when needed

---

## E) Deterministic Gates
- [ ] Same inputs => same gate decision (no randomness)
- [ ] Gate decisions are based on evidence reports + policy snapshot only
- [ ] Golden tests exist for gates/routing stability

Evidence:
- [ ] Golden test suite passes

---

## F) Data Integrity & Immutability
- [ ] Runs are immutable (no overwrite; new run_id per execution)
- [ ] Old run folders remain readable
- [ ] Artifacts are written under the run folder only

Evidence:
- [ ] Two runs of the same task produce two distinct run folders

---

## G) Testing Requirements
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Golden tests pass (gates, routing, approvals)
- [ ] Minimal E2E smoke run passes (docker sandbox if enabled)

---

## H) Migration Safety
- [ ] schema_version present in DB rows and artifacts
- [ ] Migration scripts are idempotent
- [ ] Migration docs updated if schema/layout changed

Evidence:
- [ ] `migration_report.json` exists for migration runs

---

## Release Verdict
- If any item in A–E fails => NO RELEASE.
- If F–H fails => release is blocked until fixed or explicitly approved with documented risk.

