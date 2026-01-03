# Documentation Consistency Checklist

**Purpose:** Ensure all project documentation stays consistent and up-to-date
**Use:** Run after any documentation updates
**Frequency:** After each documentation maintenance workflow

---

## ✅ Package Version Consistency

### tech-stack.md
- [ ] All package versions match package.json files
- [ ] React version: 19.1.0 (not 19.2)
- [ ] Expo SDK version: 54
- [ ] React Native version: 0.81.4
- [ ] All dependencies listed with correct versions

### Cross-File Consistency
- [ ] DEVELOPMENT_LOG.md mentions correct package versions
- [ ] YBIS_PROJE_ANAYASASI.md references correct tech stack
- [ ] Architecture_better.md has consistent version references
- [ ] QUICKSTART.md uses correct package versions

---

## ✅ Date Consistency

### Last Updated Dates
- [ ] DOCUMENTATION_INDEX.md: Current date
- [ ] README.md: Current date
- [ ] tech-stack.md: Current date
- [ ] DEVELOPMENT_LOG.md: Current date
- [ ] tasks.md: Current date

### Historical Dates
- [ ] DEVELOPMENT_LOG.md entries have correct dates
- [ ] Architecture decisions dated correctly
- [ ] Task completion dates accurate

---

## ✅ Cross-Reference Consistency

### File References
- [ ] All `constitution.md` references → `YBIS_PROJE_ANAYASASI.md`
- [ ] All `START_HERE.md` references → `QUICKSTART.md`
- [ ] All relative links work
- [ ] No broken internal links

### Navigation Links
- [ ] DOCUMENTATION_INDEX.md links work
- [ ] README.md navigation links work
- [ ] Role-based navigation accurate

---

## ✅ Content Consistency

### No Duplicates
- [ ] Package versions only in tech-stack.md
- [ ] Architecture decisions only in DEVELOPMENT_LOG.md
- [ ] Tasks only in tasks.md
- [ ] Principles only in YBIS_PROJE_ANAYASASI.md

### Formatting Consistency
- [ ] Headers use consistent format
- [ ] Code blocks use consistent language tags
- [ ] Lists use consistent bullet points
- [ ] Tables use consistent formatting

---

## ✅ Status Indicators

### Document Status
- [ ] ✅ Complete - Finished documents
- [ ] 🟢 Active - Regularly updated documents
- [ ] ⚠️ Mandatory - Critical reading documents
- [ ] 📋 Reference - When needed documents

### Health Check
- [ ] No duplicates across files
- [ ] Each file has single purpose
- [ ] Clear navigation
- [ ] Actionable content only
- [ ] Up-to-date dates
- [ ] Cross-references use relative links

---

## ✅ AI Workflow Integration

### Bootstrap Process
- [ ] AI_BASLANGIC_REHBERI.md paths correct
- [ ] AI_SYSTEM_GUIDE.md references correct
- [ ] All 4-layer loading process files exist

### Agent References
- [ ] @pm, @dev, @architect, @qa references consistent
- [ ] Workflow references point to correct files
- [ ] Command references accurate

---

## 🚨 Common Issues to Check

### Version Mismatches
- [ ] React 19.2 vs 19.1.0 inconsistencies
- [ ] Expo SDK version mismatches
- [ ] Package dependency conflicts

### Path Issues
- [ ] Turkish characters in paths
- [ ] Relative vs absolute path confusion
- [ ] Missing file references

### Content Drift
- [ ] Outdated information
- [ ] Inconsistent terminology
- [ ] Missing updates after changes

---

## 📋 Validation Report Template

```markdown
# Documentation Consistency Report

**Date:** {{date}}
**Trigger:** {{workflow_name}}
**Status:** {{overall_status}}

## Issues Found
- [ ] Issue 1: [description]
- [ ] Issue 2: [description]

## Fixes Applied
- [x] Fix 1: [description]
- [x] Fix 2: [description]

## Validation Results
- [x] Package versions consistent
- [x] Dates current
- [x] Cross-references work
- [x] No duplicates
- [x] Formatting consistent

## Next Review
**Scheduled:** {{next_review_date}}
**Trigger:** {{next_trigger}}
```

---

**Last Updated:** 2025-10-10
**Maintained By:** AI Documentation Maintenance System
**Next Review:** After next documentation update
