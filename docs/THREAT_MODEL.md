# Threat Model (Syscalls + Sandbox)

References:
- CONSTITUTION.md
- SECURITY.md
- INTERFACES.md

## 1) System Assets
Primary assets:
- Source code in repository (integrity)
- Run evidence artifacts (auditability)
- Control-plane DB (coordination)
- Developer machine / host environment (safety)
- Secrets (API keys, tokens) (confidentiality)

## 2) Trust Boundaries
- Agent logic is NOT trusted by default.
- Only syscalls are trusted to mutate state.
- Sandbox is a boundary between untrusted execution and the host.

Boundaries:
1) Agent (untrusted) -> Syscalls (trusted enforcement)
2) Syscalls -> Filesystem (restricted)
3) Syscalls -> Sandbox exec (restricted)
4) Worker -> Control-plane DB (validated ops)
5) MCP client -> MCP server -> Syscalls (no direct mutation)

## 3) Threats (Top Risks)
### T1: Arbitrary file modification
Risk: agent writes anywhere, including protected paths or secrets.
Mitigation:
- syscalls-only writes
- protected paths + approval gates
- path normalization + traversal prevention

### T2: Arbitrary command execution on host
Risk: agent runs destructive commands.
Mitigation:
- sandbox execution by default
- command allowlist
- network off by default
- minimal mounts

### T3: Data exfiltration / network leakage
Risk: agent sends secrets or code out.
Mitigation:
- sandbox network off
- explicit policy flag required for network
- scrub secrets from logs/artifacts

### T4: Supply chain abuse (third-party code)
Risk: vendor repos introduce malicious content.
Mitigation:
- vendors treated read-only
- pinned revisions
- no direct imports into core
- integrate via adapters with explicit interface contracts

### T5: Gate bypass / non-deterministic decisions
Risk: system declares success without evidence.
Mitigation:
- success defined by verifier_report + gate_report only
- deterministic gates based on evidence + policy snapshot
- golden tests for gate/routing stability

### T6: Control-plane corruption
Risk: DB tampered to mark tasks done.
Mitigation:
- DB not source-of-truth for success
- artifacts are source-of-truth
- reconciliation can detect mismatch

## 4) Security Controls Summary
Mandatory controls:
- syscalls-only mutation
- immutable run folders
- sandbox with allowlist + network off
- deterministic gates + golden tests
- protected paths + approvals
- policy profiles recorded per run

## 5) Residual Risks (Accepted for v1)
- Insider risk (developer can override locally)
- Limited provenance for third-party code unless you add SBOM later
- Secrets handling requires discipline (no auto-injection)

## 6) Future Hardening (post-v1)
- SBOM generation (CycloneDX) + dependency pinning
- Secret scanning (gitleaks)
- Signed artifacts/attestations
- Role-based auth on approvals via MCP

