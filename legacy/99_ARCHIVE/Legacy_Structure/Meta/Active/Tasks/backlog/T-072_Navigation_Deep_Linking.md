# T-072: Configure Deep Linking

**Priority:** P2 (Nice to Have)
**Effort:** 0.5 day
**Assignee:** @Coding
**Source:** COMPREHENSIVE_APP_AUDIT_REPORT.md - Section 1.4

---

## Description

Configure deep linking for all app routes to enable:
- Notification tap navigation
- External link opening
- Share functionality

## Tasks

- [ ] Configure app scheme in app.json
- [ ] Define linking configuration
- [ ] Test deep links on iOS and Android
- [ ] Document available deep links

## Configuration

```json
// app.json
{
  "expo": {
    "scheme": "ybis",
    "android": {
      "intentFilters": [
        {
          "action": "VIEW",
          "data": [{ "scheme": "ybis" }],
          "category": ["BROWSABLE", "DEFAULT"]
        }
      ]
    }
  }
}
```

## Deep Link Routes

| Route | URL |
|-------|-----|
| Chat | `ybis://chat` |
| Specific Chat | `ybis://chat/{id}` |
| Notes | `ybis://notes` |
| Specific Note | `ybis://notes/{id}` |
| Tasks | `ybis://tasks` |
| Flows | `ybis://flows` |
| Settings | `ybis://settings` |

## Acceptance Criteria

- `ybis://` scheme registered
- All main screens accessible via deep link
- Notifications can open specific screens
