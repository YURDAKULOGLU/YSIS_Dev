# SECURITY & POLICY PROFILES

References:
- CONSTITUTION.md
- INTERFACES.md

## Baseline
- Sandbox ON by default
- Network OFF by default
- Exec allowlist enforced
- Path traversal prevention
- Protected paths require approval

## Profiles
Profiles live under configs/profiles/*.yaml

### default
- reasonable allowlist
- protected paths enforced
- approval required for protected/high-risk

### strict
- minimal allowlist
- core paths broadly protected
- lower patch-size threshold before approval

