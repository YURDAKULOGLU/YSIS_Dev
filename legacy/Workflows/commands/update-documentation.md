# Update Documentation Command

**Purpose:** Execute documentation maintenance workflow
**Trigger:** After code changes, architecture decisions, or task completions
**Workflow:** documentation-maintenance.yaml

---

## 🎯 When to Use

### Automatic Triggers
- ✅ Task completion → Update tasks.md + DEVELOPMENT_LOG.md
- ✅ Package update → Update tech-stack.md
- ✅ Architecture decision → Update DEVELOPMENT_LOG.md + Architecture_better.md
- ✅ New principle → Update YBIS_PROJE_ANAYASASI.md

### Manual Triggers
- 🔄 Weekly documentation health check
- 🔄 Before starting new development phase
- 🔄 After major refactoring

---

## 📋 Execution Steps

### 1. Analyze Changes
```bash
# Identify what documentation needs updating
- Review recent code changes
- Check package.json modifications
- Identify completed tasks
- Note architecture decisions
```

### 2. Create Update Plan
```yaml
# Use template: documentation-update-plan-tmpl.yaml
- Change summary
- Affected documents
- Update priority
- Consistency checks
- Validation criteria
```

### 3. Execute Updates
```bash
# Update documents in priority order
1. tech-stack.md (if packages changed)
2. DEVELOPMENT_LOG.md (if decisions/tasks)
3. tasks.md (if tasks completed)
4. YBIS_PROJE_ANAYASASI.md (if principles changed)
5. DOCUMENTATION_INDEX.md (always)
```

### 4. Validate Consistency
```bash
# Use checklist: documentation-consistency-checklist.md
- Package version consistency
- Date consistency
- Cross-reference consistency
- Content consistency
- Status indicators
```

### 5. Update Index
```bash
# Update DOCUMENTATION_INDEX.md
- Last updated dates
- Status indicators
- Health check status
- Navigation links
```

---

## 🔍 Validation Checklist

### Package Versions
- [ ] React 19.1.0 (not 19.2)
- [ ] Expo SDK 54
- [ ] React Native 0.81.4
- [ ] All dependencies consistent

### Dates
- [ ] "Last Updated" dates current
- [ ] DEVELOPMENT_LOG.md entries dated
- [ ] All documents have current timestamps

### Cross-References
- [ ] constitution.md → YBIS_PROJE_ANAYASASI.md
- [ ] START_HERE.md → QUICKSTART.md
- [ ] All relative links work

### Content
- [ ] No duplicate information
- [ ] Consistent formatting
- [ ] Clear status indicators
- [ ] Actionable content only

---

## 🚨 Common Issues

### Version Mismatches
- **Issue:** React 19.2 vs 19.1.0
- **Fix:** Standardize to 19.1.0 everywhere
- **Prevention:** Check tech-stack.md first

### Path Issues
- **Issue:** Turkish characters in paths
- **Fix:** Use relative paths, avoid special chars
- **Prevention:** Test all links

### Content Drift
- **Issue:** Outdated information
- **Fix:** Regular health checks
- **Prevention:** Automated triggers

---

## 📊 Success Metrics

### Documentation Health
- ✅ 0 duplicate information
- ✅ 100% working cross-references
- ✅ Current dates on all documents
- ✅ Consistent package versions

### Update Frequency
- ✅ Daily: DEVELOPMENT_LOG.md
- ✅ Per task: tasks.md
- ✅ Per change: tech-stack.md
- ✅ Per principle: YBIS_PROJE_ANAYASASI.md

### Quality Gates
- ✅ All checklist items pass
- ✅ No broken links
- ✅ Consistent formatting
- ✅ Clear navigation

---

## 🔄 Integration Points

### AI Workflow Integration
- **Bootstrap:** AI_BASLANGIC_REHBERI.md → 4-layer loading
- **System Guide:** AI_SYSTEM_GUIDE.md → Agent roles
- **Constitution:** YBIS_PROJE_ANAYASASI.md → Project rules

### Development Workflow
- **Task Completion:** Auto-trigger documentation update
- **Package Update:** Auto-trigger tech-stack.md update
- **Architecture Decision:** Auto-trigger DEVELOPMENT_LOG.md update

### Quality Assurance
- **Consistency Check:** Run after every update
- **Health Check:** Weekly comprehensive review
- **Validation Report:** Document all changes

---

## 📝 Output Artifacts

### Generated Files
- `documentation-update-plan.md` - Update plan
- `documentation-consistency-report.md` - Validation report
- Updated documentation files

### Updated Files
- `tech-stack.md` - Package versions
- `DEVELOPMENT_LOG.md` - Progress log
- `tasks.md` - Task status
- `YBIS_PROJE_ANAYASASI.md` - Principles
- `DOCUMENTATION_INDEX.md` - Navigation

---

**Last Updated:** 2025-10-10
**Maintained By:** AI Documentation Maintenance System
**Next Review:** After next documentation update
