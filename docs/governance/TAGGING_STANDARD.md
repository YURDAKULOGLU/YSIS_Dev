# Constitution Tagging Standard

> Standard v1.0
> Use short tags in META.json instead of prose compliance statements.

---

## 1. MAPPING
- **§1**: Prime Directives (Principles)
- **§2**: Corporate Hierarchy (Roles)
- **§3**: Operational Protocols (Execution)
- **§4**: Security & Boundaries (Red Lines)
- **§5**: Risk & Quality Gates (New)

## 2. USAGE
In `META.json`:
```json
{
  "constitution_tags": ["§3", "§5"]
}
```
This signals that the task complied with Operational Protocols and passed Quality Gates.
