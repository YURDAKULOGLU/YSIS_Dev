---
id: TASK-New-9148
type: PLAN
status: APPROVED
created_at: 2025-12-28T23:19:10.983345
updated_at: 2025-12-29T03:00:00
target_files:
  - src/agentic/core/plugins/spec_writer_agent.py
  - src/agentic/core/plugins/spec_validator.py
  - src/agentic/core/workflows/spec_first_workflow.py
  - scripts/run_orchestrator.py
---

# Task: Spec Kit (SDD) Pipeline

## Objective

**Goal:** Implement Specification-Driven Development (SDD) pipeline that enforces spec-first workflow.

**Context:**
- Current YBIS creates code without formal specifications
- GPT-Pilot and modern AI systems use spec-first approaches
- Need to integrate existing `spec_writer.py` into orchestrator workflow
- Specs should guide planning, execution, and validation

**Success Definition:**
- SPEC.md required BEFORE planning
- Plans validated against specs
- Specs auto-update with code changes
- Contract generation from specs
- Template-based spec generation
- Zero regression in existing workflow

---

## Research Summary

**Existing Components:**
1. `src/agentic/skills/spec_writer.py` - Basic spec kit generator
2. `tools/gpt-pilot/core/agents/spec_writer.py` - Full SpecWriter agent
3. SimplePlannerV2 - Current planning system

**Key Patterns from GPT-Pilot:**
- Spec creation precedes all development
- Templates for common patterns
- Spec updates during iterations
- Validation against specs before execution

**YBIS Integration Points:**
1. Orchestrator workflow (run_orchestrator.py)
2. Planning phase (SimplePlannerV2)
3. Execution phase (Aider/Executor)
4. Task management (ybis.py)

---

## Approach

### Strategy: Spec-First Orchestration

```
┌─────────────────────────────────┐
│  Task Created/Claimed           │
└────────────┬────────────────────┘
             │
      ┌──────▼───────┐
      │  SPEC Check  │  ← Does SPEC.md exist?
      └──────┬───────┘
             │  No
      ┌──────▼──────────────┐
      │  SpecWriterAgent    │  ← Generate SPEC.md
      └──────┬──────────────┘
             │
      ┌──────▼──────────────┐
      │  User Review/Edit   │  ← Approve spec
      └──────┬──────────────┘
             │  Approved
      ┌──────▼──────────────┐
      │  SimplePlannerV2    │  ← Plan WITH spec context
      └──────┬──────────────┘
             │
      ┌──────▼──────────────┐
      │  SpecValidator      │  ← Validate plan vs spec
      └──────┬──────────────┘
             │  Valid
      ┌──────▼──────────────┐
      │  Executor           │  ← Execute with spec contract
      └──────┬──────────────┘
             │
      ┌──────▼──────────────┐
      │  Spec Updater       │  ← Update spec if code changed
      └─────────────────────┘
```

**Benefits:**
- Design before implementation (better architecture)
- Clear contracts (fewer misunderstandings)
- Living documentation (specs stay current)
- Easier onboarding (specs explain the code)

---

## Steps

### **Phase 1: SpecWriterAgent (3-4 hours)**

**1.1 Create SpecWriterAgent Class**

File: `src/agentic/core/plugins/spec_writer_agent.py`

```python
class SpecWriterAgent:
    """
    Generates professional technical specifications.

    Features:
    - Template-based spec generation
    - Multiple spec types (Architecture, API, Schema)
    - LLM-assisted spec enhancement
    - User review/edit workflow
    """

    async def generate_spec(
        self,
        task: Task,
        context: Dict[str, Any]
    ) -> Path:
        """
        Generate SPEC.md for task.

        Steps:
        1. Analyze task goal/details
        2. Select appropriate template
        3. Use LLM to fill in details
        4. Present to user for review
        5. Save to workspace/SPEC.md

        Returns:
            Path to generated SPEC.md
        """

    async def update_spec(
        self,
        spec_path: Path,
        changes: Dict[str, Any]
    ) -> None:
        """Update existing spec with code changes"""

    def _get_template(self, task_type: str) -> str:
        """Get spec template based on task type"""
```

**1.2 Spec Templates**

File: `src/agentic/core/plugins/spec_templates.py`

```python
SPEC_TEMPLATES = {
    "feature": """# SPEC: {feature_name}

## Overview
{description}

## Requirements
- Functional requirement 1
- Functional requirement 2

## API Contract
### Endpoints
- POST /api/v1/{resource}
  - Input: {schema}
  - Output: {schema}

## Data Model
### {Entity}
- field1: type
- field2: type

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2
""",

    "refactor": """# SPEC: {refactor_name}

## Objective
{description}

## Current State
- File: {target_file}
- Issues: {problems}

## Target State
- Improved: {improvements}

## Migration Strategy
- Step 1
- Step 2

## Success Criteria
- [ ] No regression
- [ ] Tests pass
""",

    "bugfix": """# SPEC: {bug_name}

## Bug Description
{description}

## Root Cause
{cause}

## Proposed Fix
{solution}

## Test Plan
- [ ] Reproduce bug
- [ ] Apply fix
- [ ] Verify fix
- [ ] Add regression test
"""
}
```

**Expected Output:**
- `spec_writer_agent.py` (~300 lines)
- `spec_templates.py` (~200 lines)
- LLM-powered spec generation

---

### **Phase 2: SpecValidator (2-3 hours)**

**2.1 Create Validation System**

File: `src/agentic/core/plugins/spec_validator.py`

```python
class SpecValidator:
    """
    Validates plans and code against specifications.

    Checks:
    - Plan steps align with spec requirements
    - Files to modify match spec scope
    - Success criteria are measurable
    - Dependencies declared in spec
    """

    async def validate_plan_against_spec(
        self,
        plan: Plan,
        spec_path: Path
    ) -> ValidationResult:
        """
        Validate plan matches spec.

        Checks:
        1. All spec requirements addressed in plan
        2. Plan steps don't exceed spec scope
        3. Files to modify are in spec scope
        4. Dependencies match spec

        Returns:
            ValidationResult with errors/warnings
        """

    async def validate_code_against_spec(
        self,
        spec_path: Path,
        modified_files: List[str]
    ) -> ValidationResult:
        """Validate executed code matches spec contracts"""

    def _parse_spec(self, spec_path: Path) -> SpecDocument:
        """Parse SPEC.md into structured format"""
```

**2.2 Spec Document Model**

```python
@dataclass
class SpecDocument:
    """Structured representation of SPEC.md"""
    overview: str
    requirements: List[str]
    api_contracts: List[APIContract]
    data_models: List[DataModel]
    success_criteria: List[str]
    dependencies: List[str]

@dataclass
class APIContract:
    endpoint: str
    method: str
    input_schema: Dict
    output_schema: Dict

@dataclass
class ValidationResult:
    valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
```

**Expected Output:**
- `spec_validator.py` (~350 lines)
- Comprehensive spec validation
- Structured spec parsing

---

### **Phase 3: Workflow Integration (2-3 hours)**

**3.1 Create SpecFirstWorkflow**

File: `src/agentic/core/workflows/spec_first_workflow.py`

```python
class SpecFirstWorkflow:
    """
    Orchestrates spec-first development workflow.

    Phases:
    1. Check for SPEC.md
    2. Generate spec if missing (SpecWriterAgent)
    3. User review/approval
    4. Plan with spec context
    5. Validate plan against spec
    6. Execute with spec contract
    7. Update spec if code changed
    """

    async def run(
        self,
        task: Task,
        workspace_path: Path
    ) -> WorkflowResult:
        """Execute full spec-first workflow"""

        # 1. Ensure spec exists
        spec_path = await self._ensure_spec(task, workspace_path)

        # 2. Plan with spec
        plan = await self._plan_with_spec(task, spec_path)

        # 3. Validate plan
        validation = await self._validate_plan(plan, spec_path)
        if not validation.valid:
            # Fix plan or regenerate
            pass

        # 4. Execute
        result = await self._execute(plan)

        # 5. Update spec if needed
        await self._update_spec_if_needed(spec_path, result)

        return result

    async def _ensure_spec(
        self,
        task: Task,
        workspace_path: Path
    ) -> Path:
        """Ensure SPEC.md exists, generate if not"""
        spec_path = workspace_path / "SPEC.md"

        if not spec_path.exists():
            # Generate spec
            spec_writer = SpecWriterAgent()
            spec_path = await spec_writer.generate_spec(task, {})

            # Ask user to review
            await self._request_spec_approval(spec_path)

        return spec_path
```

**3.2 Modify SimplePlannerV2**

Update `src/agentic/core/plugins/simple_planner_v2.py`:

```python
async def plan(self, task: str, context: Dict[str, Any]) -> Plan:
    """Generate plan with spec context (if available)"""

    # Check for SPEC.md in context
    spec_content = context.get('spec_content', None)

    if spec_content:
        # Include spec in prompt
        prompt = self._build_prompt_with_spec(task, spec_content, context)
    else:
        # Original behavior
        prompt = self._build_prompt(task, context)

    # Generate plan...
```

**Expected Output:**
- `spec_first_workflow.py` (~400 lines)
- Updated `simple_planner_v2.py` (+50 lines)
- End-to-end spec-first flow

---

### **Phase 4: Orchestrator Integration (2 hours)**

**4.1 Update run_orchestrator.py**

Modify `scripts/run_orchestrator.py`:

```python
# Add feature flag
USE_SPEC_FIRST = os.getenv("YBIS_USE_SPEC_FIRST", "false").lower() == "true"

async def run_task_workflow(task_id: str):
    """Run task with optional spec-first workflow"""

    if USE_SPEC_FIRST:
        # Use spec-first workflow
        from src.agentic.core.workflows.spec_first_workflow import SpecFirstWorkflow

        workflow = SpecFirstWorkflow()
        result = await workflow.run(task, workspace_path)
    else:
        # Original workflow
        result = await run_original_workflow(task)

    return result
```

**4.2 Add Config Flags**

File: `src/agentic/core/config.py`

```python
# Spec-First Development Feature Flags
USE_SPEC_FIRST = os.getenv("YBIS_USE_SPEC_FIRST", "false").lower() == "true"
SPEC_REQUIRE_APPROVAL = os.getenv("YBIS_SPEC_REQUIRE_APPROVAL", "true").lower() == "true"
SPEC_AUTO_UPDATE = os.getenv("YBIS_SPEC_AUTO_UPDATE", "true").lower() == "true"
SPEC_TEMPLATE = os.getenv("YBIS_SPEC_TEMPLATE", "auto")  # auto|feature|refactor|bugfix
```

**Expected Output:**
- Updated `run_orchestrator.py` (+50 lines)
- Updated `config.py` (+8 lines)
- Feature-flagged integration

---

### **Phase 5: Testing (2-3 hours)**

**5.1 Test Suite**

File: `workspaces/active/TASK-New-9148/tests/test_spec_writer.py`

```python
class TestSpecWriterAgent:
    """Test spec generation"""

    @pytest.mark.asyncio
    async def test_generate_spec_from_task(self):
        """Test spec generation from task"""

    @pytest.mark.asyncio
    async def test_template_selection(self):
        """Test correct template selected"""

    @pytest.mark.asyncio
    async def test_llm_enhancement(self):
        """Test LLM enhances spec"""
```

File: `workspaces/active/TASK-New-9148/tests/test_spec_validator.py`

```python
class TestSpecValidator:
    """Test spec validation"""

    @pytest.mark.asyncio
    async def test_validate_plan_matches_spec(self):
        """Test plan validation against spec"""

    @pytest.mark.asyncio
    async def test_detect_spec_violations(self):
        """Test violation detection"""
```

File: `workspaces/active/TASK-New-9148/tests/test_spec_workflow.py`

```python
class TestSpecFirstWorkflow:
    """Test complete spec-first workflow"""

    @pytest.mark.asyncio
    async def test_full_workflow_with_spec(self):
        """Test end-to-end workflow"""

    @pytest.mark.asyncio
    async def test_spec_auto_generation(self):
        """Test automatic spec generation"""
```

**Expected Output:**
- 25+ tests across 3 modules
- >85% code coverage
- Integration tests for full workflow

---

### **Phase 6: Documentation (1 hour)**

**6.1 Documentation Files**
- RUNBOOK.md (execution log)
- RESULT.md (deliverables)
- SPEC_GUIDE.md (usage guide for users)

**6.2 Configuration Guide**

```bash
# Enable spec-first workflow
export YBIS_USE_SPEC_FIRST=true

# Require user approval of generated specs
export YBIS_SPEC_REQUIRE_APPROVAL=true

# Auto-update specs when code changes
export YBIS_SPEC_AUTO_UPDATE=true

# Template selection (auto, feature, refactor, bugfix)
export YBIS_SPEC_TEMPLATE=auto
```

---

## Risks & Mitigations

### Risk 1: User Friction (Spec approval step)
**Impact:** HIGH
**Mitigation:**
- Make approval optional (flag)
- Auto-approve for simple tasks
- Quick review UI
- Templates pre-fill most content

### Risk 2: Spec-Plan Mismatch
**Impact:** MEDIUM
**Mitigation:**
- Validation layer catches mismatches
- Clear error messages
- Suggest plan fixes
- Allow spec override

### Risk 3: Performance Overhead
**Impact:** LOW
**Mitigation:**
- Spec generation cached
- Validation is fast (text parsing)
- Feature-flagged (can disable)
- Lazy loading

### Risk 4: Breaking Existing Workflow
**Impact:** HIGH
**Mitigation:**
- Feature flag (default OFF)
- Backward compatible
- Fallback to original flow
- Gradual rollout

---

## Success Criteria

### Must-Have:
- ✅ SpecWriterAgent implemented
- ✅ Spec templates (feature, refactor, bugfix)
- ✅ SpecValidator operational
- ✅ SpecFirstWorkflow integrated
- ✅ SimplePlannerV2 spec-aware
- ✅ Feature-flagged integration
- ✅ Zero regression in existing workflow
- ✅ Tests passing (>85% coverage)
- ✅ Documentation complete

### Metrics:
- **Quality:** Plans match specs (>90%)
- **Usability:** Spec generation <30s
- **Reliability:** Validation catches mismatches (>95%)
- **Performance:** <100ms overhead per task

---

## Timeline

**Total Estimated Time:** 13-18 hours (2-3 days)

- Phase 1 (SpecWriterAgent): 3-4 hours
- Phase 2 (SpecValidator): 2-3 hours
- Phase 3 (Workflow Integration): 2-3 hours
- Phase 4 (Orchestrator Integration): 2 hours
- Phase 5 (Testing): 2-3 hours
- Phase 6 (Documentation): 1 hour

---

## Dependencies

### Completed:
- ✅ TASK-New-9134 (Optimization Trinity)
- ✅ TASK-New-6383 (SWE-agent ACI)
- ✅ SimplePlannerV2 operational

### Required:
- Existing `spec_writer.py` (basic version)
- LiteLLM / LLM provider
- Orchestrator workflow

### Blockers:
- None currently

---

**Status:** Ready to begin implementation
**Next Step:** Phase 1 - Create SpecWriterAgent
