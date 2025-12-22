# T-067: Complete i18n String Coverage

**Priority:** P1 (Important)
**Effort:** 1 day
**Assignee:** @Coding
**Source:** COMPREHENSIVE_APP_AUDIT_REPORT.md - Section 10

---

## Description

Audit and complete internationalization coverage. All user-visible strings should be translated.

## Tasks

- [ ] Audit for hardcoded strings in components
- [ ] Add missing translation keys
- [ ] Translate error messages
- [ ] Add date/time localization
- [ ] Add number formatting
- [ ] Set language preference in AI context
- [ ] **Localize AI System Prompts:** Ensure system prompts (e.g., "You are a helpful assistant") are generated in the user's selected language.

## Files to Audit

- `apps/mobile/app/**/*.tsx`
- `apps/mobile/src/features/**/*.tsx`
- `packages/ui/src/**/*.tsx`

## Known Hardcoded Strings

Search for:
- String literals in JSX
- Error messages in catch blocks
- Toast messages
- Placeholder text

## Localization Improvements

```typescript
// Use date-fns for date formatting
import { format } from 'date-fns';
import { tr, enUS } from 'date-fns/locale';

const locales = { tr, en: enUS };
format(date, 'PPP', { locale: locales[currentLanguage] });
```

## Acceptance Criteria

- No hardcoded user-visible strings
- All strings in en.json and tr.json
- Dates/times formatted per locale

