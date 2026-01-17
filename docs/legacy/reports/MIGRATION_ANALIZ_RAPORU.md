# 🔄 MEVCUT KOD YAPISI → YENİ YAPI MİGRASYON ANALİZİ

**Tarih:** 2025-01-XX  
**Amaç:** Mevcut kod yapısını analiz edip yeni yapıya nasıl migrate edileceğini belirlemek

---

## 📊 MEVCUT YAPI ANALİZİ

### 1. Contracts (Pydantic Models)

**Mevcut:** `src/agentic/core/protocols.py`

**İçerik:**
- `TaskState` - Merkezi state object (task_id, plan, code_result, verification, retry_count, vb.)
- `Plan` - Structured plan (objective, steps, files_to_modify, dependencies, risks)
- `CodeResult` - Execution result (files_modified, commands_run, outputs, success, error)
- `VerificationResult` - Verification result (lint_passed, tests_passed, coverage, errors, warnings)
- `ProposedTask` - Proposed task model
- `TaskPayload` - Universal payload for task assignment

**Sorunlar:**
- ❌ `schema_version` yok
- ❌ Evidence report format'ı yok (verifier_report.json, gate_report.json)
- ❌ Run model yok (sadece TaskState var)
- ❌ Policy snapshot model yok

**Yeni Yapıya Mapping:**
```
src/agentic/core/protocols.py
  → src/ybis/contracts/
    - task.py (Task model with schema_version)
    - run.py (Run model with schema_version)
    - evidence.py (VerifierReport, GateReport, ExecutorReport, PatchApplyReport)
    - policy.py (PolicySnapshot model)
```

---

### 2. Syscalls (Enforcement Point)

**Mevcut:** `src/agentic/core/execution/aci.py` (Agent-Computer Interface)

**İçerik:**
- `AgentComputerInterface` class
- `edit_file()` - File editing with validation
- `run_command()` - Command execution (sandbox + allowlist)
- `find_file()`, `read_file()`, `search_in_file()` - File operations
- Context tracking (opened_files, edited_files, executed_commands)

**Sorunlar:**
- ⚠️ "Syscall" pattern değil, "ACI" pattern
- ❌ Journal events emit etmiyor
- ❌ Evidence artifacts yazmıyor (patch_apply_report.json, exec_report.json)
- ❌ Protected paths kontrolü yok
- ❌ Policy snapshot reference yok

**Yeni Yapıya Mapping:**
```
src/agentic/core/execution/aci.py
  → src/ybis/syscalls/
    - fs.py (fs.read, fs.write_file, fs.apply_patch)
    - exec.py (exec.run - sandbox + allowlist + network policy)
    - git.py (git.status, git.diff, git.commit)
    - approvals.py (approvals.write)
    - journal.py (journal.append_event)
```

**Eklenmesi Gerekenler:**
- Journal event emission (her syscall sonrası)
- Evidence artifact writing (patch_apply_report.json, exec_report.json)
- Protected paths validation
- Policy snapshot reference

---

### 3. Control-Plane (DB Operations)

**Mevcut:** `src/agentic/infrastructure/db.py`

**İçerik:**
- `TaskDatabase` class
- `initialize()` - Create tables
- `add_task()`, `get_all_tasks()`, `update_task_status()`
- SQLite async operations (aiosqlite)

**Sorunlar:**
- ❌ Run table yok (sadece tasks var)
- ❌ Lease table yok (multi-worker için)
- ❌ Worker table yok
- ❌ schema_version yok

**Yeni Yapıya Mapping:**
```
src/agentic/infrastructure/db.py
  → src/ybis/control_plane/
    - db.py (SQLite operations)
    - tasks.py (task.* operations)
    - runs.py (run.* operations)
    - leases.py (lease.* operations)
    - workers.py (worker.* operations)
```

**Eklenmesi Gerekenler:**
- Runs table (run_id, task_id, workflow, status, risk_level, run_path, timestamps, schema_version)
- Leases table (lease_id, task_id, worker_id, ttl, expires_at)
- Workers table (worker_id, heartbeat_at, status)

---

### 4. Orchestrator (LangGraph + Gates)

**Mevcut:** `src/agentic/core/graphs/orchestrator_graph.py`

**İçerik:**
- `OrchestratorGraph` class
- LangGraph state machine
- Nodes: `_spec_node`, `_plan_node`, `_execute_node`, `_verify_node`, `_finalize_node`
- Routing logic (retry, success, failure)

**Sorunlar:**
- ⚠️ Gate logic yok (sadece verification var)
- ❌ Gate report üretmiyor
- ❌ Deterministic decision logic yok (policy snapshot + evidence)
- ❌ Approval step yok

**Yeni Yapıya Mapping:**
```
src/agentic/core/graphs/orchestrator_graph.py
  → src/ybis/orchestrator/
    - graph.py (LangGraph workflows)
    - gates.py (Deterministic gates + risk scoring)
    - routing.py (Deterministic routing logic)
```

**Eklenmesi Gerekenler:**
- `gates.py` - Deterministic gate decisions (PASS/BLOCK/REQUIRE_APPROVAL)
- `gate_report.json` artifact generation
- Policy snapshot reference in decisions
- Approval step in workflow

---

### 5. Verifier

**Mevcut:** 
- `src/agentic/core/plugins/simple_verifier.py`
- `src/agentic/core/plugins/sentinel_enhanced.py`

**İçerik:**
- `SimpleVerifier` - Basic verification (ruff + pytest)
- `SentinelVerifierEnhanced` - Enhanced verification (AST analysis)
- `verify()` method returns `VerificationResult`
- Policy enforcement gate (enforce_gate function)

**Sorunlar:**
- ❌ `verifier_report.json` üretmiyor (sadece VerificationResult object)
- ❌ Deterministic parsing yok
- ❌ Artifact writing yok

**Yeni Yapıya Mapping:**
```
src/agentic/core/plugins/simple_verifier.py
src/agentic/core/plugins/sentinel_enhanced.py
  → src/ybis/orchestrator/verifier.py
    - Verifier adapter (ruff + pytest)
    - Deterministic parsing
    - verifier_report.json artifact writing
```

**Eklenmesi Gerekenler:**
- `verifier_report.json` artifact format
- Deterministic parsing (no randomness)
- Artifact writing under run folder

---

### 6. Sandbox & Allowlist

**Mevcut:**
- `src/agentic/core/execution/sandbox.py`
- `src/agentic/core/execution/command_allowlist.py`

**İçerik:**
- Docker sandbox execution
- Command allowlist enforcement
- Network policy (off by default)

**Sorunlar:**
- ⚠️ Policy profile'dan okumuyor (hardcoded)
- ❌ Policy snapshot reference yok
- ❌ Exec report artifact yazmıyor

**Yeni Yapıya Mapping:**
```
src/agentic/core/execution/sandbox.py
src/agentic/core/execution/command_allowlist.py
  → src/ybis/syscalls/exec.py
    - Sandbox execution (Docker)
    - Allowlist enforcement (policy profile'dan)
    - Network policy (policy profile'dan)
    - exec_report.json artifact writing
```

**Eklenmesi Gerekenler:**
- Policy profile'dan okuma (configs/profiles/*.yaml)
- Policy snapshot reference
- exec_report.json artifact

---

### 7. Workspace Management

**Mevcut:** `src/agentic/core/workspace.py`

**İçerik:**
- `WorkspaceManager` class
- `ensure_directories()` - Create workspace directories
- Legacy structure: `workspaces/active/<TASK_ID>/`

**Sorunlar:**
- ❌ Yeni yapı: `workspaces/<task_id>/runs/<run_id>/` formatı yok
- ❌ Immutable run layout yok
- ❌ Artifacts/journal directories yok

**Yeni Yapıya Mapping:**
```
src/agentic/core/workspace.py
  → src/ybis/data_plane/
    - workspace.py (Workspace + run layout)
    - artifacts.py (Artifact writing)
    - journal.py (Journal writer - append-only)
```

**Eklenmesi Gerekenler:**
- New layout: `workspaces/<task_id>/runs/<run_id>/`
- Artifacts directory: `artifacts/`
- Journal directory: `journal/events.jsonl`
- Immutable run creation

---

## 🎯 MİGRASYON PLANI

### Faz 1: Contracts (Task 02)

**Hedef:** Pydantic models + schema_version

**Adımlar:**
1. `src/ybis/contracts/task.py` oluştur
   - Task model (task_id, title, objective, status, priority, schema_version, timestamps, workspace_path)
2. `src/ybis/contracts/run.py` oluştur
   - Run model (run_id, task_id, workflow, status, risk_level, run_path, timestamps, schema_version)
3. `src/ybis/contracts/evidence.py` oluştur
   - VerifierReport, GateReport, ExecutorReport, PatchApplyReport models
   - Her biri schema_version içermeli
4. `src/ybis/contracts/policy.py` oluştur
   - PolicySnapshot model

**DoD:**
- ✅ Pydantic models compile
- ✅ schema_version enforcement tests pass

---

### Faz 2: Workspace + Run Layout (Task 03)

**Hedef:** Immutable run layout

**Adımlar:**
1. `src/ybis/data_plane/workspace.py` oluştur
   - `create_run_folder(task_id, run_id)` → `workspaces/<task_id>/runs/<run_id>/`
   - `ensure_artifacts_dir(run_path)` → `artifacts/`
   - `ensure_journal_dir(run_path)` → `journal/`
2. `src/ybis/data_plane/journal.py` oluştur
   - `append_event(run_path, event)` → `journal/events.jsonl`

**DoD:**
- ✅ Run folders created deterministically
- ✅ Artifacts/journal directories exist

---

### Faz 3: Syscalls (Task 06-07)

**Hedef:** Syscall pattern implementation

**Adımlar:**
1. `src/ybis/syscalls/fs.py` oluştur
   - `read(path)` - File read
   - `write_file(path, content, run_path)` - File write + journal event + protected path check
   - `apply_patch(patch, run_path)` - Patch apply + patch_apply_report.json
2. `src/ybis/syscalls/exec.py` oluştur
   - `run(command, run_path, policy_snapshot)` - Sandbox + allowlist + network policy + exec_report.json
3. `src/ybis/syscalls/git.py` oluştur
   - `status()`, `diff()`, `commit(allowed_files)`
4. `src/ybis/syscalls/journal.py` oluştur
   - `append_event(run_path, event)` - Append-only journal

**DoD:**
- ✅ patch_apply_report.json emitted
- ✅ exec_report.json emitted
- ✅ Protected path checks work
- ✅ Journal events written

---

### Faz 4: Verifier + Gates (Task 08-09)

**Hedef:** Verifier adapter + deterministic gates

**Adımlar:**
1. `src/ybis/orchestrator/verifier.py` oluştur
   - Ruff + pytest execution
   - Deterministic parsing
   - verifier_report.json writing
2. `src/ybis/orchestrator/gates.py` oluştur
   - Deterministic gate decisions (PASS/BLOCK/REQUIRE_APPROVAL)
   - Policy snapshot + evidence reports = decision
   - gate_report.json writing

**DoD:**
- ✅ verifier_report.json produced
- ✅ gate_report.json produced
- ✅ Deterministic decisions (no randomness)

---

### Faz 5: Control-Plane (Task 05)

**Hedef:** DB operations for tasks/runs/leases/workers

**Adımlar:**
1. `src/ybis/control_plane/db.py` - SQLite connection
2. `src/ybis/control_plane/tasks.py` - task.* operations
3. `src/ybis/control_plane/runs.py` - run.* operations
4. `src/ybis/control_plane/leases.py` - lease.* operations
5. `src/ybis/control_plane/workers.py` - worker.* operations

**DoD:**
- ✅ Integration test for create+claim+run row

---

### Faz 6: Orchestrator Graph (Task 10)

**Hedef:** LangGraph build workflow end-to-end

**Adımlar:**
1. `src/ybis/orchestrator/graph.py` oluştur
   - LangGraph workflow (build, repair, research, debate, evolve)
   - Nodes: resolve_config, init_run, plan, execute, apply_patch, verify, gates_and_risk, finalize, approval
2. Routing logic:
   - verify fail + retries => repair loop
   - verify pass => gates
   - gates PASS => SUCCESS
   - gates REQUIRE_APPROVAL => stop and request approval
   - gates BLOCK => BLOCKED

**DoD:**
- ✅ Full artifact set produced
- ✅ DB run status updates

---

## 📋 DETAYLI KOD MAPPING

| Mevcut Dosya | Yeni Dosya | Değişiklikler |
|--------------|-----------|---------------|
| `src/agentic/core/protocols.py` | `src/ybis/contracts/task.py`<br>`src/ybis/contracts/run.py`<br>`src/ybis/contracts/evidence.py` | schema_version ekle, evidence report models ekle |
| `src/agentic/core/execution/aci.py` | `src/ybis/syscalls/fs.py`<br>`src/ybis/syscalls/exec.py`<br>`src/ybis/syscalls/git.py` | Journal events, evidence artifacts, protected paths |
| `src/agentic/infrastructure/db.py` | `src/ybis/control_plane/db.py`<br>`src/ybis/control_plane/tasks.py`<br>`src/ybis/control_plane/runs.py`<br>`src/ybis/control_plane/leases.py` | Runs, leases, workers tables ekle |
| `src/agentic/core/graphs/orchestrator_graph.py` | `src/ybis/orchestrator/graph.py`<br>`src/ybis/orchestrator/gates.py` | Gates logic ekle, gate_report.json ekle |
| `src/agentic/core/plugins/simple_verifier.py` | `src/ybis/orchestrator/verifier.py` | verifier_report.json artifact ekle |
| `src/agentic/core/execution/sandbox.py` | `src/ybis/syscalls/exec.py` | Policy profile'dan okuma, exec_report.json |
| `src/agentic/core/workspace.py` | `src/ybis/data_plane/workspace.py`<br>`src/ybis/data_plane/journal.py` | New layout, immutable runs |

---

## ⚠️ KRİTİK FARKLAR

### Eski Yapı (Disiplinsiz)
- ❌ Evidence report yok (sadece VerificationResult object)
- ❌ Gate report yok
- ❌ Journal events yok
- ❌ Protected paths kontrolü yok
- ❌ Policy snapshot yok
- ❌ schema_version yok
- ❌ Immutable runs yok (overwrite edilebilir)

### Yeni Yapı (Disiplinli)
- ✅ Evidence reports (verifier_report.json, gate_report.json, exec_report.json, patch_apply_report.json)
- ✅ Journal events (append-only events.jsonl)
- ✅ Protected paths kontrolü (policy profile'dan)
- ✅ Policy snapshot (her run'da kaydedilir)
- ✅ schema_version (her model'de)
- ✅ Immutable runs (her run yeni klasör)

---

## 🚀 SONUÇ

Mevcut kod yapısı **çalışıyor** ama **disiplinsiz**. Yeni yapı **teoride mükemmel** ve **tüm problemlere çözüm var**.

**Migration stratejisi:**
1. Önce contracts (schema_version ekle)
2. Sonra workspace layout (immutable runs)
3. Sonra syscalls (journal + evidence)
4. Sonra verifier + gates (deterministic decisions)
5. Sonra orchestrator (full workflow)

Her faz bağımsız test edilebilir ve aşamalı migration mümkün.

---

**Hazırlayan:** AI Assistant  
**Tarih:** 2025-01-XX  
**Versiyon:** 1.0

