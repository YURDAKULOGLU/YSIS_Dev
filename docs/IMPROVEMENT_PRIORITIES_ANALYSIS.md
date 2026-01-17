# YBIS Improvement Priorities Analysis

## Mevcut Durum Kontrolü

### ✅ 1. Feedback Loop - **VAR!** (Ama sadece task içinde)

**Durum:**
- ✅ Verifier errors → spec_node/plan_node feedback loop VAR
- ✅ `docs/FEEDBACK_LOOP_IMPLEMENTATION.md` dokümante edilmiş
- ❌ Cross-task feedback YOK (bir task'tan diğerine öğrenme yok)

**Ne Var:**
```python
# src/ybis/orchestrator/graph.py
# spec_node ve plan_node verifier feedback'i alıyor
verifier_feedback = load_verifier_errors()
if verifier_feedback:
    # Feedback'i prompt'a ekle
    task_objective += f"\n⚠️ FEEDBACK: {verifier_feedback}"
```

**Ne Eksik:**
- Task sonuçlarını bir sonraki task'a input verme
- Başarılı pattern'ları kaydetme
- Cross-task learning

**Öncelik:** Enhancement (Mevcut sistemi genişlet)

---

### ⚠️ 2. Memory/Learning - **KISMI VAR** (API var, adapter yok)

**Durum:**
- ✅ Memory API mevcut (`add_to_memory`, `search_memory`)
- ✅ MCP tools mevcut
- ❌ MemoryStoreAdapter implementasyonu YOK
- ❌ Vector store entegrasyonu YOK

**Ne Var:**
```python
# src/ybis/services/mcp_tools/memory_tools.py
async def add_to_memory(data: str, ...) -> str:
    # API var ama adapter eksik
    try:
        from ...adapters.memory_store import MemoryStoreAdapter
        adapter = MemoryStoreAdapter()  # ❌ Not implemented
    except ImportError:
        return "MEMORY ERROR: Adapter not implemented"
```

**Ne Eksik:**
- MemoryStoreAdapter implementation
- Vector store (ChromaDB, FAISS)
- Persistent storage
- RAG integration

**Öncelik:** HIGH (API var, implementasyon gerekli)

---

### ⚠️ 3. Auto-Test Pipeline - **KISMI VAR** (Test tools var, pre-commit yok)

**Durum:**
- ✅ Test tools mevcut (`run_tests`, `run_linter`)
- ✅ Verifier node test çalıştırıyor
- ⚠️ `pre-commit` dependency var ama `.pre-commit-config.yaml` YOK
- ❌ Pre-commit hook YOK
- ❌ Auto-test gate YOK

**Ne Var:**
```python
# src/ybis/services/mcp_tools/test_tools.py
async def run_tests(...) -> str:
    # Test çalıştırma var
    result = subprocess.run(["pytest", ...])
```

**Ne Eksik:**
- `.pre-commit-config.yaml` dosyası
- Pre-commit hook installer
- Auto-test gate (test başarısız olursa block)
- Test coverage threshold enforcement

**Öncelik:** HIGH (Hızlı implement edilebilir)

---

### ❌ 4. Rollback Mekanizması - **YOK**

**Durum:**
- ❌ Git worktree YOK
- ❌ Automatic rollback YOK
- ❌ Worktree isolation YOK

**Ne Var:**
- ✅ Klasör isolation (`workspaces/<task_id>/runs/<run_id>/`)
- ❌ Git worktree YOK
- ❌ Rollback mekanizması YOK

**Ne Eksik:**
- `init_git_worktree()` function
- `cleanup_worktree()` function
- `merge_worktree()` function (sadece success'te)
- Automatic rollback on failure

**Öncelik:** MEDIUM (Orta effort, önemli güvenlik özelliği)

---

### ⚠️ 5. Metrics/Observability - **KISMI VAR** (Logging var, dashboard yok)

**Durum:**
- ✅ Comprehensive logging var (`src/ybis/orchestrator/logging.py`)
- ✅ Langfuse/OpenTelemetry adapters enabled
- ❌ Dashboard YOK
- ❌ Real-time monitoring YOK
- ❌ Step-level metrics YOK

**Ne Var:**
```python
# src/ybis/orchestrator/logging.py
log_workflow_event(...)
log_node_execution(...)
log_llm_call(...)
log_state_transition(...)
```

**Ne Eksik:**
- Step-level timing
- Failure point tracking
- Metrics dashboard (web UI)
- Prometheus metrics export
- Real-time monitoring

**Öncelik:** MEDIUM (Logging var, dashboard eklemek kolay)

---

### ❌ 6. Dependency Tracking - **YOK**

**Durum:**
- ❌ `depends_on` column YOK (schema.sql'de yok)
- ❌ Task dependency resolution YOK
- ❌ Auto-start dependent tasks YOK

**Ne Var:**
- ✅ Tasks table var
- ❌ Dependency tracking YOK

**Ne Eksik:**
- `depends_on` column in tasks table
- Dependency resolution logic
- Auto-start when dependencies complete
- Dependency graph visualization

**Öncelik:** LOW (Nice-to-have, düşük impact)

---

## Öncelik Sırası (Güncellenmiş)

| # | Feature | Durum | Impact | Effort | Öncelik |
|---|---------|-------|--------|--------|---------|
| 1 | **Auto-Test Gate** | ⚠️ Kısmi | HIGH | LOW | 🔥 **1. YAP** |
| 2 | **Error Knowledge Base** | ❌ Yok | HIGH | MEDIUM | 🔥 **2. YAP** |
| 2b | **Feedback Loop Enhancement** | ✅ Var (task içi) | HIGH | MEDIUM | 🟡 **2b. YAP** |
| 3 | **Metrics Dashboard** | ⚠️ Kısmi | MEDIUM | LOW | 🟡 **3. YAP** |
| 4 | **Memory/RAG** | ⚠️ API var | HIGH | HIGH | 🟡 **4. YAP** |
| 5 | **Rollback** | ❌ Yok | MEDIUM | MEDIUM | 🟡 **5. YAP** |
| 6 | **Dependencies** | ❌ Yok | LOW | MEDIUM | ⚪ **6. YAP** |

---

## Hemen Yapılabilecekler (Quick Wins)

### 1. Auto-Test Gate (1-2 saat)
```bash
# 1. Create .pre-commit-config.yaml
# 2. Add test gate to gate_node
# 3. Install pre-commit hooks
```

### 2. Metrics Dashboard (2-3 saat)
```bash
# 1. Add step-level timing to logging
# 2. Create simple Flask dashboard
# 3. Export metrics to JSON/CSV
```

### 3. Feedback Loop Enhancement (3-4 saat)
```bash
# 1. Add task result analysis
# 2. Store outcomes in memory (when memory ready)
# 3. Query memory before spec generation
```

---

## Task'lar Oluşturuldu

Tüm improvement task'ları oluşturuldu:
- T-1: Auto-Test Gate
- T-2: Feedback Loop Enhancement
- T-3: Metrics Dashboard
- T-4: Memory/RAG Implementation
- T-5: Rollback Mechanism
- T-6: Task Dependencies

**Çalıştırma:**
```bash
python scripts/ybis_run.py <task_id> --workflow self_develop
```

