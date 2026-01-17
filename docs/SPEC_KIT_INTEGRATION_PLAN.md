# Spec-Kit Integration Plan for YBIS

**Date:** 2026-01-09  
**Status:** Planning Phase  
**Priority:** 🔴 High (Fixes Gap 3: Verification Quality & Spec Quality)

---

## Executive Summary

Spec-Kit provides a mature Spec-Driven Development (SDD) methodology with structured templates, quality validation, and constitutional compliance checks. Integrating Spec-Kit into YBIS will:

1. **Improve Spec Quality** - Replace basic templates with comprehensive spec-kit templates
2. **Enhance Validation** - Add quality checklists and constitutional compliance
3. **Add Research Phase** - Integrate Phase 0 research workflow from spec-kit
4. **Improve Planning** - Use spec-kit's structured plan generation with contracts/data-model

---

## Current State Analysis

### YBIS Current Implementation

**Spec Generation (`spec_node()`):**
- Location: `src/ybis/orchestrator/graph.py:88-198`
- Template: `templates/spec_template.md` (basic, may not exist)
- Process: LLM generates spec from task objective
- Validation: Basic structure check (`_is_structured_spec()`)
- Issues:
  - No quality checklist
  - No constitutional compliance
  - No user story prioritization
  - No acceptance scenario format

**Plan Generation (`plan_node()`):**
- Location: `src/ybis/orchestrator/graph.py:282-339`
- Process: LLM generates plan from spec
- Output: `plan.json` (structured)
- Issues:
  - No research phase (Phase 0)
  - No contracts/data-model generation
  - No constitutional check
  - No quickstart validation guide

**Spec Validation (`spec_validator.py`):**
- Location: `src/ybis/orchestrator/spec_validator.py`
- Features: Parsing, structure validation, LLM semantic validation
- Missing: Quality checklist, constitutional compliance

### Spec-Kit Capabilities

**Templates:**
- `spec-template.md` - Comprehensive feature spec with user stories, acceptance scenarios, success criteria
- `plan-template.md` - Implementation plan with research phase, contracts, data-model
- `checklist-template.md` - Quality validation checklist
- `tasks-template.md` - Task breakdown by user story

**Commands:**
- `/speckit.specify` - Feature description → structured spec
- `/speckit.plan` - Spec → implementation plan (with research)
- `/speckit.tasks` - Plan → executable task list
- `/speckit.checklist` - Generate quality checklist

**Scripts:**
- `create-new-feature.sh` - Branch management, feature numbering
- `setup-plan.sh` - Plan directory structure
- `update-agent-context.sh` - Agent-specific context updates

---

## Integration Strategy

### Phase 1: Template Integration ⏭️ **IMMEDIATE**

**Goal:** Replace YBIS templates with spec-kit templates

**Tasks:**
1. ✅ Create `templates/` directory (if missing)
2. Copy spec-kit templates:
   ```bash
   # Copy templates
   cp vendors/spec-kit/templates/spec-template.md templates/spec_template.md
   cp vendors/spec-kit/templates/plan-template.md templates/plan_template.md
   cp vendors/spec-kit/templates/checklist-template.md templates/checklist_template.md
   cp vendors/spec-kit/templates/tasks-template.md templates/tasks_template.md
   ```

3. Update `_load_spec_template()` in `src/ybis/orchestrator/graph.py`:
   ```python
   def _load_spec_template() -> str:
       """Load spec template, preferring spec-kit template."""
       # Try spec-kit template first
       spec_kit_template = PROJECT_ROOT / "vendors" / "spec-kit" / "templates" / "spec-template.md"
       if spec_kit_template.exists():
           return spec_kit_template.read_text(encoding="utf-8")
       
       # Try YBIS template
       ybis_template = PROJECT_ROOT / "templates" / "spec_template.md"
       if ybis_template.exists():
           return ybis_template.read_text(encoding="utf-8")
       
       # Fallback to minimal template
       return (
           "# SPEC: <task_id>\n\n"
           "## Objective\n<clear objective>\n\n"
           "## Requirements\n- <requirement 1>\n\n"
           "## Acceptance Criteria\n- <criterion 1>\n"
       )
   ```

4. Update `spec_node()` prompt to use spec-kit template structure:
   - Emphasize user story prioritization (P1, P2, P3)
   - Require acceptance scenarios (Given/When/Then)
   - Include success criteria (measurable, technology-agnostic)
   - Add edge cases section

**Deliverables:**
- ✅ `templates/spec_template.md` (from spec-kit)
- ✅ `templates/plan_template.md` (from spec-kit)
- ✅ Updated `_load_spec_template()` function
- ✅ Enhanced `spec_node()` prompt

---

### Phase 2: Validation Enhancement ⏭️ **HIGH PRIORITY**

**Goal:** Add quality checklists and constitutional compliance

**Tasks:**

1. **Create Constitution File:**
   - Check if `docs/CONSTITUTION.md` exists
   - If not, create from spec-kit's constitution pattern
   - Include: code quality, testing standards, architecture principles

2. **Enhance `spec_validator.py`:**
   ```python
   # Add to spec_validator.py
   def validate_spec_quality(spec_path: Path) -> Dict[str, Any]:
       """Validate spec against spec-kit quality checklist."""
       # Load checklist template
       checklist_template = PROJECT_ROOT / "templates" / "checklist_template.md"
       
       # Check for:
       # - No implementation details
       # - User story prioritization
       # - Acceptance scenarios defined
       # - Success criteria measurable
       # - No [NEEDS CLARIFICATION] markers (or max 3)
       # - Edge cases identified
       
   def check_constitutional_compliance(spec_path: Path, plan_path: Optional[Path] = None) -> Dict[str, Any]:
       """Check spec/plan against constitution."""
       constitution_path = PROJECT_ROOT / "docs" / "CONSTITUTION.md"
       if not constitution_path.exists():
           return {"status": "no_constitution", "violations": []}
       
       # Load constitution
       # Check spec/plan against principles
       # Return violations
   ```

3. **Update `validate_spec_node()`:**
   - Call quality checklist validation
   - Call constitutional compliance check
   - Fail validation if critical issues found

**Deliverables:**
- ✅ `docs/CONSTITUTION.md` (if missing)
- ✅ Enhanced `spec_validator.py` with quality checks
- ✅ Constitutional compliance validation
- ✅ Updated `validate_spec_node()` workflow

---

### Phase 3: Research Phase Integration ⏭️ **MEDIUM PRIORITY**

**Goal:** Add Phase 0 research workflow from spec-kit

**Tasks:**

1. **Create Research Phase in `plan_node()`:**
   ```python
   def plan_node(state: WorkflowState) -> WorkflowState:
       # ... existing code ...
       
       # Phase 0: Research (NEW)
       research_path = ctx.run_path / "research.md"
       if not research_path.exists():
           research_content = _generate_research_phase(spec_content, task_objective)
           research_path.write_text(research_content, encoding="utf-8")
       
       # Phase 1: Design (ENHANCED)
       # Generate data-model.md, contracts/, quickstart.md
       _generate_design_artifacts(spec_content, ctx.run_path)
   ```

2. **Implement Research Generation:**
   - Extract "NEEDS CLARIFICATION" markers from spec
   - Generate research tasks for each unknown
   - Consolidate findings in `research.md`
   - Format: Decision, Rationale, Alternatives

3. **Implement Design Artifacts:**
   - Extract entities → `data-model.md`
   - Extract user actions → API contracts
   - Generate `quickstart.md` validation guide

**Deliverables:**
- ✅ Research phase in `plan_node()`
- ✅ `research.md` generation
- ✅ `data-model.md` generation
- ✅ Contracts directory generation
- ✅ `quickstart.md` validation guide

---

### Phase 4: Branch Management ⏭️ **LOW PRIORITY**

**Goal:** Integrate spec-kit's branch management (optional)

**Tasks:**

1. **Create Branch Management Utility:**
   ```python
   # src/ybis/orchestrator/branch_manager.py
   def create_feature_branch(feature_description: str) -> str:
       """Create semantic branch name with auto-numbering."""
       # Extract short name (2-4 words)
       # Find highest existing number
       # Create branch: {number}-{short-name}
   ```

2. **Integrate into Workflow:**
   - Call before `spec_node()` if branch doesn't exist
   - Use branch name in spec metadata

**Deliverables:**
- ✅ `src/ybis/orchestrator/branch_manager.py`
- ✅ Branch creation in workflow

---

## Additional Vendors Analysis

### Potentially Useful Vendors

**For Spec/Plan Quality:**
- ✅ **spec-kit** - Primary focus (this plan)
- **gpt-pilot** - Code generation from specs (could complement)
- **chatdev** - Multi-agent development (similar to BMAD)

**For Validation/Testing:**
- **promptfoo** - LLM evaluation (could validate spec quality)
- **trulens** - LLM observability (could track spec generation quality)

**For Workflow:**
- ✅ **BMAD-METHOD** - Workflow registry (Gap 2)
- ✅ **n8n** - External integrations

**Recommendation:** Focus on spec-kit first. Other vendors can be integrated later if needed.

---

## Implementation Checklist

### Immediate (Phase 1) ✅ **COMPLETE**
- [x] Create `templates/` directory
- [x] Copy spec-kit templates
- [x] Update `_load_spec_template()`
- [x] Update `spec_node()` prompt
- [ ] Test spec generation with new template (TODO: manual testing)

### High Priority (Phase 2)
- [ ] Create/verify `docs/CONSTITUTION.md`
- [ ] Add quality checklist validation
- [ ] Add constitutional compliance check
- [ ] Update `validate_spec_node()`
- [ ] Test validation workflow

### Medium Priority (Phase 3)
- [ ] Add research phase to `plan_node()`
- [ ] Implement research generation
- [ ] Implement design artifacts (data-model, contracts)
- [ ] Generate quickstart validation guide
- [ ] Test full plan generation

### Low Priority (Phase 4)
- [ ] Create branch management utility
- [ ] Integrate into workflow
- [ ] Test branch creation

---

## Success Criteria

1. ✅ Specs generated with spec-kit template structure
2. ✅ Quality checklist validation passes
3. ✅ Constitutional compliance checked
4. ✅ Research phase generates `research.md`
5. ✅ Plan includes data-model and contracts
6. ✅ Quickstart validation guide created

---

## Risks & Mitigations

**Risk 1:** Spec-kit templates too complex for simple tasks
- **Mitigation:** Keep fallback to minimal template, make template selection configurable

**Risk 2:** Constitutional compliance too strict
- **Mitigation:** Make violations warnings (not errors) initially, allow override

**Risk 3:** Research phase adds latency
- **Mitigation:** Make research phase optional via profile config, cache research results

---

## Next Steps

1. **Start with Phase 1** - Template integration (immediate impact, low risk)
2. **Then Phase 2** - Validation enhancement (high value for Gap 3)
3. **Then Phase 3** - Research phase (adds depth to planning)
4. **Finally Phase 4** - Branch management (nice-to-have)

**Estimated Effort:**
- Phase 1: 2-3 hours
- Phase 2: 4-6 hours
- Phase 3: 6-8 hours
- Phase 4: 2-3 hours
- **Total: 14-20 hours**

