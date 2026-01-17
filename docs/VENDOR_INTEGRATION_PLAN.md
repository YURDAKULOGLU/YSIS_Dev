# Vendor Integration Plan: BMAD, Spec Kit & n8n

**Date:** 2026-01-09  
**Status:** ✅ BMAD Cloned | ✅ Spec Kit Cloned | ✅ n8n Cloned

---

## ✅ Completed: Spec Kit Integration

**Status:** ✅ **CLONED** (zaten vendors'da vardı)

**Repository:** `vendors/spec-kit/`  
**Source:** https://github.com/github/spec-kit  
**Description:** Spec-Driven Development toolkit with `/speckit.*` commands

**Key Features:**
- `/speckit.specify` - Feature description → structured spec
- `/speckit.plan` - Spec → implementation plan
- `/speckit.tasks` - Plan → executable task list
- Template-based generation
- Branch management
- Constitutional compliance
- Quality validation

**Spec-Kit vs YBIS Comparison:**

| Feature | Spec-Kit | YBIS | Integration Opportunity |
|---------|----------|------|------------------------|
| Spec Generation | `/speckit.specify` command | `spec_node()` in graph | ✅ Use spec-kit templates |
| Spec Template | `templates/spec-template.md` (detailed) | `templates/spec_template.md` (basic) | ✅ Replace with spec-kit template |
| Plan Generation | `/speckit.plan` with research phase | `plan_node()` (direct) | ✅ Add research phase from spec-kit |
| Validation | Quality checklist + validation | `spec_validator.py` (basic) | ✅ Enhance with spec-kit validation |
| Branch Management | Auto branch creation | Manual | ✅ Integrate branch management |
| Constitutional Check | Built-in | Manual | ✅ Add constitutional validation |

**Integration Strategy:**

### Phase 1: Template Integration
1. Copy spec-kit templates to YBIS:
   - `vendors/spec-kit/templates/spec-template.md` → `templates/spec_template.md` (replace)
   - `vendors/spec-kit/templates/plan-template.md` → `templates/plan_template.md` (new)
   - `vendors/spec-kit/templates/checklist-template.md` → `templates/checklist_template.md` (new)

2. Update `spec_node()` to use spec-kit template:
   ```python
   # src/ybis/orchestrator/graph.py
   def _load_spec_template() -> str:
       # Try spec-kit template first
       spec_kit_template = PROJECT_ROOT / "vendors" / "spec-kit" / "templates" / "spec-template.md"
       if spec_kit_template.exists():
           return spec_kit_template.read_text()
       # Fallback to YBIS template
       return (PROJECT_ROOT / "templates" / "spec_template.md").read_text()
   ```

### Phase 2: Validation Enhancement
1. Integrate spec-kit's quality checklist:
   - `vendors/spec-kit/templates/checklist-template.md` → YBIS validation
   - Add checklist generation to `spec_validator.py`

2. Add constitutional compliance check:
   - Spec-kit has built-in constitution checking
   - YBIS has `docs/CONSTITUTION.md`
   - Integrate spec-kit's constitutional validation logic

### Phase 3: Command Integration
1. Create MCP tools for spec-kit commands:
   - `speckit_specify` - MCP tool wrapper for `/speckit.specify`
   - `speckit_plan` - MCP tool wrapper for `/speckit.plan`
   - `speckit_tasks` - MCP tool wrapper for `/speckit.tasks`

2. Integrate into YBIS workflow:
   - Option A: Use spec-kit commands directly in `spec_node()` and `plan_node()`
   - Option B: Create adapter that calls spec-kit scripts

### Phase 4: Branch Management
1. Integrate spec-kit's branch management:
   - Auto branch creation from feature description
   - Feature numbering (001, 002, 003...)
   - Semantic branch naming

---

## ✅ Completed: BMAD Integration

**Status:** ✅ **CLONED**

**Repository:** `vendors/BMAD-METHOD/`  
**Description:** Multi-agent collaboration framework

**Integration Points:**
- Workflow registry pattern (for Gap 2)
- Multi-agent role system (Analyst, PM, Architect, Developer, QA)
- Workflow-based task execution

---

## ✅ Completed: n8n Integration

**Status:** ✅ **CLONED**

**Repository:** `vendors/n8n/`  
**Description:** Workflow automation platform

**Integration Points:**
- External system integrations
- Event-driven workflows
- AI workflow builder

---

## Integration Priority

### 🔴 High Priority (Gap Fixes)
1. **Spec-Kit Template Integration** → Fixes spec quality gap
2. **Spec-Kit Validation** → Enhances verification quality (Gap 3)
3. **BMAD Workflow Registry** → Fixes workflow definition gap (Gap 2)

### 🟡 Medium Priority
4. **Spec-Kit Branch Management** → Improves workflow
5. **n8n Event Integration** → External system connectivity
6. **BMAD Multi-Agent Roles** → Enhanced agent collaboration

### 🟢 Low Priority
7. **Spec-Kit Command Wrappers** → MCP tool integration
8. **n8n Workflow Builder** → Advanced automation

---

## Next Steps

1. ✅ **Spec-Kit templates** → Copy to YBIS templates
2. ✅ **Spec-Kit validation** → Integrate into `spec_validator.py`
3. ⏭️ **BMAD workflow registry** → Create `src/ybis/orchestrator/workflow_registry.py`
4. ⏭️ **Adapter creation** → `src/ybis/adapters/spec_kit.py`, `src/ybis/adapters/bmad.py`
