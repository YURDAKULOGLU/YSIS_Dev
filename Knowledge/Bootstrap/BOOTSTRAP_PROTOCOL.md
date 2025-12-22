# Bootstrap Protocol: "Company-in-a-Box" Dev Pipeline

**Vision:** Agent'lar yeni agent'ları kurar → Çalışan bir dev hattı emerges
**Principle:** Zincirleme kurulum (Chain Installation)
**Goal:** Self-improving system that builds itself
**Date:** 2025-12-20

---

## Core Principles (Immutable)

### 1. Deterministik Artefakt Üretimi
Her adım MUTLAKA üretir:
- `PLAN.md` (ne kuruyoruz / neden)
- `RUNBOOK.md` (komutlar - copy/paste ready)
- `EVIDENCE/` (log dosyaları - text only, no screenshots)
- `DECISIONS.json` (seçilen sürümler, config)

### 2. Gate-Based Pipeline
Her adım "gate" ile kapanır:
- `lint` + `unit test` + `smoke run`
- Başarısızsa: **rollback veya fix loop** (maks 2 döngü)
- Başarılıysa: **commit + tag + changelog**

**Why:** "Hız = kırmadan hızlı ilerlemek" - 0 cam kırığı!

---

## Current System Stack (3-Layer Architecture)

### Katman A: Orkestrasyon (Beyin)
**Mevcut:**
- ✓ LangGraph (state machine + determinism)
- ✓ CrewAI (multi-agent planning)

**Eklenecek:**
- [ ] AutoGen-style messaging (agent→agent communication)

### Katman B: Çalışma Ortamı (El)
**Mevcut:**
- ✓ Aider (code generation via local LLM)
- ✓ `.sandbox_hybrid/` (local artifacts)

**Eklenecek:**
- [ ] Docker sandbox (standardized environment)
- [ ] E2B (optional - cloud sandbox)

### Katman C: Dev İşi (Bekçi/Şirket)
**Mevcut:**
- ✓ Sentinel (verification system)
- ✓ RAGMemory (ChromaDB + embeddings)

**Eklenecek:**
- [ ] Open SWE / SWE-agent (issue→patch→test→PR)
- [ ] GritQL (deterministic refactoring)
- [ ] OpenHands (browser automation - optional)

---

## Bootstrap Roadmap (Zincirleme Kurulum)

### Phase 0: Foundation (COMPLETE ✓)

**What we have:**
1. ✓ OrchestratorGraph (retry loop + feedback)
2. ✓ Prevention system (emoji, imports, artifacts)
3. ✓ Feedback loop (auto-correction)
4. ✓ CrewAI planner (multi-agent)
5. ✓ RAGMemory (vector storage)

**Dogfooding validation:**
- T-100: Retry loop ✓
- T-102: Plugin architecture ✓
- T-102.1: Feedback loop ✓

**Status:** PRODUCTION READY - Can execute tasks reliably

---

### Phase 1: Memory Integration (T-103.5)

**Goal:** RAG-aware orchestration
**Why First:** Context is critical - sistem hafızasız blind
**Duration:** 1 day

#### Deliverables

**1. PLAN.md**
```markdown
# RAG Integration Plan

## Objective
Connect RAGMemory to OrchestratorGraph for context-aware execution

## Why
- Planners need task history for better plans
- Executors need similar solutions for guidance
- Verifiers need error patterns for prevention

## Architecture
- Planner queries RAG before planning
- Executor queries RAG for similar code
- Verifier indexes results for learning
```

**2. RUNBOOK.md**
```bash
# RAG Integration Commands

# 1. Test RAGMemory standalone
python -c "from src.agentic.core.plugins.rag_memory import RAGMemory; r = RAGMemory(); r.add_text('test'); print(r.query('test'))"

# 2. Index existing task specs
python scripts/index_task_specs.py

# 3. Test context retrieval
python test_rag_integration.py

# 4. Run end-to-end with RAG
python run_with_rag.py T-103
```

**3. Files to Create**
- `src/agentic/core/plugins/rag_aware_planner.py` (wraps SimplePlanner with RAG)
- `scripts/index_task_specs.py` (index Knowledge/Tasks/)
- `test_rag_integration.py` (unit tests)
- `run_with_rag.py` (orchestrator with RAG)

**4. Success Criteria (Gate)**
- [ ] RAGMemory integrated into SimplePlanner
- [ ] Task specs indexed in ChromaDB
- [ ] Context retrieval working (query returns relevant tasks)
- [ ] End-to-end test with RAG passes
- [ ] Smoke test: Task execution improves with context

**5. EVIDENCE/**
```
Knowledge/Bootstrap/T-103.5/EVIDENCE/
├── rag_init.log (ChromaDB initialization)
├── index_tasks.log (indexing results)
├── query_test.log (retrieval accuracy)
└── e2e_with_rag.log (full task execution)
```

**6. DECISIONS.json**
```json
{
  "embedding_model": "all-MiniLM-L6-v2",
  "vector_db": "ChromaDB",
  "index_targets": ["task_specs", "code_results", "error_history"],
  "retrieval_limit": 5,
  "similarity_threshold": 0.7
}
```

---

### Phase 2: Docker Sandbox (T-103)

**Goal:** Standardized execution environment
**Why Second:** Isolated environment after memory is working
**Duration:** 1 day

#### Deliverables

**1. PLAN.md**
```markdown
# Docker Sandbox Setup

## Objective
Create isolated, reproducible execution environment

## Why
- Consistent environment across machines
- No pollution of host system
- Reproducible builds
- Easy cleanup

## Architecture
- Docker Compose for orchestration
- Volume mounts for artifacts
- Network isolation
- Resource limits
```

**2. RUNBOOK.md**
```bash
# Docker Setup Commands

# 1. Install Docker Desktop (Windows)
# Manual: Download from docker.com

# 2. Build sandbox image
docker build -t ybis-sandbox -f docker/Dockerfile.sandbox .

# 3. Start services
docker-compose -f docker/docker-compose.yml up -d

# 4. Test sandbox
docker exec ybis-sandbox python --version

# 5. Run task in sandbox
python run_in_docker.py T-104
```

**3. Files to Create**
- `docker/Dockerfile.sandbox` (Python + tools)
- `docker/docker-compose.yml` (services)
- `src/agentic/core/plugins/docker_executor.py` (executor wrapper)
- `run_in_docker.py` (orchestrator wrapper)

**4. Success Criteria (Gate)**
- [ ] Docker image builds successfully
- [ ] Container starts and runs Python
- [ ] Volume mounts work (artifacts accessible)
- [ ] Task executes inside container
- [ ] Smoke test: Hello World in Docker

**5. EVIDENCE/**
```
Knowledge/Bootstrap/T-103/EVIDENCE/
├── docker_build.log
├── docker_run.log
├── volume_test.log
└── task_in_container.log
```

**6. DECISIONS.json**
```json
{
  "base_image": "python:3.12-slim",
  "tools": ["git", "aider", "pytest"],
  "volumes": [".sandbox_docker:/workspace"],
  "network": "isolated",
  "resource_limits": {"cpus": "2", "memory": "4g"}
}
```

---

### Phase 3: Open SWE Integration (T-104)

**Goal:** Issue → Patch → Test → PR workflow
**Why Third:** Build on Docker + RAG for robust issue fixing
**Duration:** 2 days

#### Deliverables

**1. PLAN.md**
```markdown
# Open SWE Integration

## Objective
Automate issue→patch→test→PR workflow

## Why
- End-to-end automation
- GitHub integration
- Issue-driven development
- PR automation

## Architecture
- SWE-agent for issue analysis
- OrchestratorGraph for execution
- Sentinel for verification
- GitHub API for PR creation
```

**2. RUNBOOK.md**
```bash
# Open SWE Setup

# 1. Install SWE-agent
pip install sweagent

# 2. Configure GitHub token
export GITHUB_TOKEN=your_token_here

# 3. Test on toy repo
python scripts/test_swe_agent.py

# 4. Run issue fix
python run_swe_fix.py --issue 123

# 5. Create PR
python scripts/create_pr.py --branch fix-123
```

**3. Files to Create**
- `src/agentic/core/plugins/swe_agent_wrapper.py`
- `src/agentic/core/plugins/github_api.py`
- `scripts/test_swe_agent.py`
- `run_swe_fix.py`
- `scripts/create_pr.py`

**4. Success Criteria (Gate)**
- [ ] SWE-agent installed and working
- [ ] Can analyze GitHub issue
- [ ] Can generate patch
- [ ] Patch passes tests
- [ ] PR created successfully
- [ ] Smoke test: Fix toy issue end-to-end

**5. EVIDENCE/**
```
Knowledge/Bootstrap/T-104/EVIDENCE/
├── swe_install.log
├── issue_analysis.log
├── patch_generation.log
├── test_results.log
└── pr_creation.log
```

**6. DECISIONS.json**
```json
{
  "swe_agent_version": "latest",
  "github_api": "PyGithub",
  "branch_pattern": "fix-issue-{number}",
  "pr_template": "templates/pr_template.md",
  "auto_merge": false
}
```

---

### Phase 4: GritQL Refactoring (T-105)

**Goal:** Deterministic code transformation
**Why Fourth:** Build on solid foundation for safe refactoring
**Duration:** 1 day

#### Deliverables

**1. PLAN.md**
```markdown
# GritQL Integration

## Objective
Add deterministic refactoring capabilities

## Why
- Safe code transformations
- Migration automation
- Consistent refactoring
- Pattern-based changes

## Architecture
- GritQL for pattern matching
- Transformation rules
- Preview before apply
- Rollback support
```

**2. RUNBOOK.md**
```bash
# GritQL Setup

# 1. Install GritQL
npm install -g @getgrit/launcher

# 2. Initialize patterns
grit init

# 3. Test pattern
grit apply test-pattern --dry-run

# 4. Apply transformation
grit apply migrate-imports

# 5. Verify changes
git diff
```

**3. Files to Create**
- `src/agentic/core/plugins/gritql_refactor.py`
- `.grit/patterns/` (transformation patterns)
- `scripts/test_gritql.py`
- `run_refactor.py`

**4. Success Criteria (Gate)**
- [ ] GritQL installed
- [ ] Can define patterns
- [ ] Dry-run works
- [ ] Transformations apply correctly
- [ ] Rollback works
- [ ] Smoke test: Rename function across repo

**5. EVIDENCE/**
```
Knowledge/Bootstrap/T-105/EVIDENCE/
├── gritql_install.log
├── pattern_test.log
├── transform_preview.log
└── transform_apply.log
```

---

## Bootstrapper Agent Implementation

### Core Loop

```python
class BootstrapperAgent:
    """
    Kurulum yöneticisi - kod üretmez, kurulum yapar
    """

    async def bootstrap_cycle(self, target: str):
        """
        1. Inspect: Sistem durumunu oku
        2. Plan: Sıradaki hedefi planla
        3. Execute: Sandbox'ta kur
        4. Verify: Test/lint/smoke
        5. Commit: Green ise commit
        6. Handoff: Sıradaki task'ı oluştur
        """

        # 1. Inspect
        state = self.inspect_system()
        self.save_artifact("STATE_SNAPSHOT.json", state)

        # 2. Plan
        next_target = self.select_next_target(state, target)
        plan = await self.create_bootstrap_plan(next_target)
        self.save_artifact("PLAN.md", plan)

        # 3. Execute
        result = await self.execute_in_sandbox(plan)
        self.save_artifact("RUNBOOK.md", result.commands)
        self.save_artifact("DECISIONS.json", result.decisions)

        # 4. Verify (GATE)
        verification = await self.verify_installation(result)
        self.save_evidence(verification.logs)

        if not verification.passed:
            if result.retry_count < 2:
                return await self.bootstrap_cycle(target)  # Fix loop
            else:
                return self.rollback()  # Rollback

        # 5. Commit
        await self.commit_and_tag(next_target)

        # 6. Handoff
        await self.create_next_task(next_target)

        return result
```

### Artifact Structure

```
Knowledge/Bootstrap/T-XXX/
├── PLAN.md              # What & Why
├── RUNBOOK.md           # Commands
├── DECISIONS.json       # Versions & Config
├── EVIDENCE/
│   ├── install.log
│   ├── test.log
│   └── smoke.log
└── STATUS.json          # Gate result
```

---

## Testing Strategy

### Unit Tests
- Each component tested standalone
- Mock external dependencies
- Fast execution (<1s per test)

### Integration Tests
- Components tested together
- Real dependencies (Docker, ChromaDB)
- Moderate execution (<30s per test)

### End-to-End Tests
- Full workflow (Issue → PR)
- Real environment
- Slow but comprehensive (<5min)

### Smoke Tests
- Quick sanity check
- Gate for each phase
- Must pass before proceeding

---

## Rollback Strategy

### Auto-Rollback Triggers
1. Gate fails after 2 fix attempts
2. Critical error (data loss risk)
3. Resource exhaustion

### Rollback Process
```bash
# 1. Tag current state
git tag rollback-point-T-XXX

# 2. Revert changes
git reset --hard rollback-point-T-XXX

# 3. Clean artifacts
rm -rf Knowledge/Bootstrap/T-XXX/

# 4. Document failure
echo "Rollback: $(date)" >> Knowledge/Bootstrap/ROLLBACK_LOG.md
```

---

## Success Metrics

### Phase Success
- Gate passed: lint + test + smoke
- Artifacts created: PLAN + RUNBOOK + EVIDENCE + DECISIONS
- Commit tagged: vX.Y.Z-bootstrap-T-XXX

### Overall Success
- All 4 phases complete
- System self-improving
- Dogfooding 100%
- Zero manual intervention

---

## Next Steps (Execution Order)

1. **NOW:** Implement T-103.5 (RAG Integration)
   - Quick win (1 day)
   - High impact (context-aware)
   - Low risk (no external deps)

2. **Then:** Implement T-103 (Docker Sandbox)
   - Foundation for isolation
   - Enables reproducibility
   - Medium complexity

3. **Then:** Implement T-104 (Open SWE)
   - End-to-end automation
   - GitHub integration
   - High complexity

4. **Finally:** Implement T-105 (GritQL)
   - Refactoring automation
   - Safe transformations
   - Low complexity (nice-to-have)

---

**Zincirleme Kurulum Aktif**
**0 Cam Kırığı**
**Mükemmel Sistem**

Let's build this company-in-a-box! 🚀
