# Documentation Health Check Command

**Purpose:** Comprehensive documentation consistency and health validation  
**Trigger:** Weekly, before major releases, or when inconsistencies suspected  
**Workflow:** documentation-maintenance.yaml (validation phase)

---

## 🎯 When to Use

### Scheduled Triggers
- 📅 Weekly health check (every Monday)
- 📅 Before major releases
- 📅 End of each development phase

### Manual Triggers
- 🔍 When inconsistencies suspected
- 🔍 After major refactoring
- 🔍 When new team members onboard

---

## 📋 Health Check Process

### 1. Package Version Audit
```bash
# Check all package versions across documents
- tech-stack.md: React 19.1.0, Expo SDK 54, RN 0.81.4
- DEVELOPMENT_LOG.md: Consistent version references
- YBIS_PROJE_ANAYASASI.md: Correct tech stack mentions
- Architecture_better.md: Accurate version info
```

### 2. Date Consistency Check
```bash
# Validate all timestamps
- DOCUMENTATION_INDEX.md: Last updated date
- README.md: Last updated date
- tech-stack.md: Last updated date
- DEVELOPMENT_LOG.md: Entry dates
- tasks.md: Last updated date
```

### 3. Cross-Reference Validation
```bash
# Test all internal links
- constitution.md → YBIS_PROJE_ANAYASASI.md
- START_HERE.md → QUICKSTART.md
- All relative links work
- Navigation links functional
```

### 4. Content Duplication Scan
```bash
# Identify duplicate information
- Package versions: Only in tech-stack.md
- Architecture decisions: Only in DEVELOPMENT_LOG.md
- Tasks: Only in tasks.md
- Principles: Only in YBIS_PROJE_ANAYASASI.md
```

### 5. Formatting Consistency
```bash
# Check formatting standards
- Headers: Consistent format
- Code blocks: Proper language tags
- Lists: Consistent bullet points
- Tables: Consistent formatting
```

---

## 🔍 Detailed Validation

### Package Version Matrix
| Document | React | Expo SDK | RN | Status |
|----------|-------|----------|----|---------| 
| tech-stack.md | 19.1.0 | 54 | 0.81.4 | ✅ |
| DEVELOPMENT_LOG.md | 19.1.0 | 54 | 0.81.4 | ✅ |
| YBIS_PROJE_ANAYASASI.md | 19.1.0 | 54 | 0.81.4 | ✅ |
| Architecture_better.md | 19.1.0 | 54 | 0.81.4 | ✅ |

### Date Audit
| Document | Last Updated | Status |
|----------|--------------|---------|
| DOCUMENTATION_INDEX.md | 2025-01-23 | ✅ |
| README.md | 2025-01-23 | ✅ |
| tech-stack.md | 2025-01-23 | ✅ |
| DEVELOPMENT_LOG.md | 2025-01-23 | ✅ |
| tasks.md | 2025-01-23 | ✅ |

### Cross-Reference Check
| Reference | Target | Status |
|-----------|--------|---------|
| constitution.md | YBIS_PROJE_ANAYASASI.md | ✅ |
| START_HERE.md | QUICKSTART.md | ✅ |
| All relative links | Working | ✅ |
| Navigation links | Functional | ✅ |

---

## 🚨 Issue Detection

### Common Problems
1. **Version Mismatches**
   - React 19.2 vs 19.1.0
   - Expo SDK version conflicts
   - Package dependency issues

2. **Path Issues**
   - Turkish characters in paths
   - Broken relative links
   - Missing file references

3. **Content Drift**
   - Outdated information
   - Inconsistent terminology
   - Missing updates

4. **Formatting Issues**
   - Inconsistent headers
   - Mixed bullet styles
   - Table formatting problems

### Issue Severity
- 🔴 **Critical:** Broken links, version conflicts
- 🟡 **Warning:** Outdated dates, formatting issues
- 🟢 **Info:** Minor inconsistencies, suggestions

---

## 📊 Health Score Calculation

### Scoring System
- **Package Consistency:** 25 points
- **Date Accuracy:** 25 points
- **Cross-References:** 25 points
- **Content Quality:** 25 points

### Health Levels
- 🟢 **Healthy (90-100):** All checks pass
- 🟡 **Warning (70-89):** Minor issues found
- 🔴 **Critical (0-69):** Major issues require attention

---

## 🔧 Auto-Fix Capabilities

### Automatic Fixes
- ✅ Update "Last Updated" dates
- ✅ Fix relative path issues
- ✅ Standardize package versions
- ✅ Correct formatting inconsistencies

### Manual Fixes Required
- 🔧 Content updates
- 🔧 Architecture decision documentation
- 🔧 Task status updates
- 🔧 New principle additions

---

## 📝 Health Report Template

```markdown
# Documentation Health Report

**Date:** {{date}}
**Health Score:** {{score}}/100
**Status:** {{status}}

## Package Version Consistency
- [x] React 19.1.0 consistent across all files
- [x] Expo SDK 54 consistent
- [x] React Native 0.81.4 consistent
- [x] All dependencies accurate

## Date Accuracy
- [x] All "Last Updated" dates current
- [x] DEVELOPMENT_LOG.md entries dated
- [x] Consistent date format

## Cross-Reference Health
- [x] All internal links work
- [x] Navigation functional
- [x] No broken references

## Content Quality
- [x] No duplicate information
- [x] Consistent formatting
- [x] Clear status indicators
- [x] Actionable content only

## Issues Found
{{issues_list}}

## Fixes Applied
{{fixes_list}}

## Recommendations
{{recommendations}}

## Next Health Check
**Scheduled:** {{next_check_date}}
**Trigger:** {{next_trigger}}
```

---

## 🔄 Integration with Workflows

### AI Workflow Integration
- **Bootstrap:** Validate AI_BASLANGIC_REHBERI.md paths
- **System Guide:** Check AI_SYSTEM_GUIDE.md references
- **Constitution:** Verify YBIS_PROJE_ANAYASASI.md rules

### Development Workflow
- **Pre-commit:** Quick consistency check
- **Post-update:** Full health validation
- **Release:** Comprehensive audit

### Quality Assurance
- **Daily:** Basic consistency check
- **Weekly:** Full health check
- **Monthly:** Comprehensive audit

---

## 📈 Continuous Improvement

### Metrics Tracking
- Health score trends
- Issue frequency
- Fix application time
- Consistency improvements

### Process Optimization
- Automated fix suggestions
- Preventive measures
- Workflow improvements
- Tool enhancements

---

**Last Updated:** 2025-10-10  
**Maintained By:** AI Documentation Maintenance System  
**Next Health Check:** Weekly
