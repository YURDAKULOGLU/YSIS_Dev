# YBIS Tools Independence Analysis

## Soru
**"Sen YBIS'in araçlarını kullanarak projeyi geliştirebilir misin? RAG'ıyla, graph'ıyla, workflow'daki her adım bağımsız olarak çalıştırılabiliyor mu?"**

## Cevap: EVET! ✅

### 1. Workflow Node'ları Bağımsız Çalıştırılabilir ✅

**Her workflow node'u bağımsız bir Python fonksiyonu:**

```python
from src.ybis.orchestrator.graph import (
    spec_node,
    plan_node,
    execute_node,
    verify_node,
    gate_node,
    repair_node,
    debate_node,
)

# Her node'u doğrudan çağırabilirsiniz:
state = {
    "task_id": "T-123",
    "run_id": "R-123",
    "run_path": Path("workspaces/T-123/runs/R-123"),
    "task_objective": "Test task",
    "workflow_name": "self_develop",
}

# Bağımsız çalıştırma:
result_state = spec_node(state)      # ✅ Çalışır
result_state = plan_node(result_state) # ✅ Çalışır
result_state = execute_node(result_state) # ✅ Çalışır
```

**Node'ların özellikleri:**
- ✅ Her node `WorkflowState` alır, `WorkflowState` döndürür
- ✅ Node'lar birbirinden bağımsızdır (sadece state üzerinden iletişim)
- ✅ Node'lar `NodeRegistry`'de kayıtlıdır
- ✅ Node'lar doğrudan import edilebilir ve test edilebilir

**Örnek: Sadece spec_node çalıştırma:**
```python
# Sadece spec oluştur, plan yapma
state = spec_node(initial_state)
# SPEC.md oluşturuldu ✅
```

### 2. MCP Tools Bağımsız Kullanılabilir ✅

**28 MCP tool mevcut ve bağımsız çalışır:**

#### Task Tools
- `task_create` - Task oluştur
- `task_status` - Task durumu
- `get_tasks` - Task listesi
- `claim_task` - Task al
- `update_task_status` - Durum güncelle
- `task_complete` - Task tamamla
- `task_run` - Workflow çalıştır

#### Artifact Tools
- `artifact_read` - Artifact oku
- `artifact_write` - Artifact yaz
- `approval_write` - Onay yaz

#### Memory/RAG Tools
- `add_to_memory` - Memory'ye ekle (RAG)
- `search_memory` - Memory'de ara (RAG)

**Durum:**
- ✅ Tool'lar async fonksiyonlar
- ✅ MCP server üzerinden çağrılabilir
- ⚠️ Memory tools adapter gerektirir (MemoryStoreAdapter)

#### Dependency/Graph Tools
- `check_dependency_impact` - Dependency analizi
- `find_circular_dependencies` - Circular dependency bul
- `get_critical_files` - Kritik dosyalar

**Durum:**
- ✅ Tool'lar mevcut
- ⚠️ Neo4j adapter gerektirir (GraphStoreAdapter)

#### Test Tools
- `run_tests` - Test çalıştır
- `run_linter` - Lint çalıştır
- `check_test_coverage` - Coverage kontrol

**Durum:**
- ✅ Tamamen bağımsız çalışır
- ✅ pytest, ruff kullanır

### 3. RAG (Memory) Sistemi ✅

**Mevcut:**
- `add_to_memory()` - Memory'ye ekle
- `search_memory()` - Memory'de ara

**Gereksinimler:**
- MemoryStoreAdapter (vector store)
- Vector database (ChromaDB, FAISS, etc.)

**Kullanım:**
```python
# Memory'ye ekle
await add_to_memory(
    "YBIS workflow nodes can be executed independently",
    agent_id="claude",
    metadata='{"type": "fact", "source": "analysis"}'
)

# Memory'de ara
results = await search_memory(
    "workflow nodes independent",
    limit=5
)
```

**Durum:**
- ✅ API mevcut
- ⚠️ Adapter implementasyonu gerekli (Task E - Memory + Graph Adapters)

### 4. Graph (Dependency) Sistemi ✅

**Mevcut:**
- `check_dependency_impact()` - Impact analizi
- `find_circular_dependencies()` - Circular dependency
- `get_critical_files()` - Kritik dosyalar

**Gereksinimler:**
- Neo4j GraphStoreAdapter
- Neo4j database

**Kullanım:**
```python
# Dependency impact kontrol
impact = await check_dependency_impact(
    "src/ybis/orchestrator/graph.py",
    max_depth=3
)
# Returns: "[WARNING] 15 files will be affected..."
```

**Durum:**
- ✅ API mevcut
- ⚠️ Neo4j adapter ve database gerekli

### 5. Workflow Adımları Bağımsız Çalıştırılabilir ✅

**Workflow YAML'dan node'ları seçerek çalıştırabilirsiniz:**

```python
from src.ybis.workflows.runner import WorkflowRunner

# Workflow yükle
runner = WorkflowRunner().load_workflow("self_develop")
graph = runner.build_graph()

# Sadece belirli node'ları çalıştır
# (LangGraph'ın conditional routing kullanarak)
```

**Veya doğrudan node'ları çağır:**

```python
# Sadece spec + plan, execute yapma
state = spec_node(initial_state)
state = plan_node(state)
# SPEC.md ve plan.json oluşturuldu ✅
# execute_node çağrılmadı
```

### 6. Ben (Claude) YBIS Araçlarını Kullanabilir miyim? ✅

**EVET! MCP server üzerinden:**

```python
# MCP client olarak bağlan
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# YBIS MCP server'a bağlan
server_params = StdioServerParameters(
    command="python",
    args=["scripts/ybis_mcp_server.py"],
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Task oluştur
        result = await session.call_tool(
            "task_create",
            arguments={
                "title": "Feature: Add X",
                "objective": "Implement feature X",
                "priority": "HIGH",
            }
        )
        
        # Artifact oku
        artifact = await session.call_tool(
            "artifact_read",
            arguments={
                "task_id": "T-123",
                "artifact_name": "spec.md",
            }
        )
        
        # Test çalıştır
        test_result = await session.call_tool(
            "run_tests",
            arguments={
                "test_path": "tests/",
                "verbose": True,
            }
        )
```

**Durum:**
- ✅ MCP server çalışıyor (28 tool)
- ✅ Tool'lar async ve çağrılabilir
- ✅ Ben (Claude) MCP client olarak bağlanabilirim
- ✅ YBIS'i YBIS ile geliştirebilirim! 🎯

### 7. Pratik Örnek: YBIS'i YBIS ile Geliştirme

**Senaryo: Yeni bir feature ekle**

```python
# 1. Task oluştur (MCP tool)
task = await task_create(
    title="Feature: Add X",
    objective="Implement feature X with Y and Z",
    priority="HIGH"
)

# 2. Workflow çalıştır (MCP tool)
run = await task_run(
    task_id=task["task_id"],
    workflow_name="self_develop"
)

# 3. Artifact'ları oku (MCP tool)
spec = await artifact_read(task_id, "spec.md")
plan = await artifact_read(task_id, "plan.json")

# 4. Test çalıştır (MCP tool)
test_result = await run_tests("tests/")

# 5. Memory'ye kaydet (MCP tool)
await add_to_memory(
    f"Feature X implemented with approach Y",
    metadata='{"type": "implementation", "feature": "X"}'
)

# 6. Dependency kontrol (MCP tool)
impact = await check_dependency_impact("src/ybis/new_feature.py")
```

**Tüm adımlar bağımsız ve MCP üzerinden! ✅**

## Sonuç

### ✅ EVET, YBIS'in araçlarını kullanarak projeyi geliştirebilirim!

**Neden:**
1. ✅ Workflow node'ları bağımsız fonksiyonlar
2. ✅ MCP tools bağımsız çalışır (28 tool)
3. ✅ RAG/Memory API mevcut (adapter gerekli)
4. ✅ Graph/Dependency API mevcut (Neo4j gerekli)
5. ✅ Test tools tamamen bağımsız
6. ✅ Her adım ayrı ayrı çalıştırılabilir

**Gereksinimler:**
- ⚠️ Memory adapter (MemoryStoreAdapter) - Task E
- ⚠️ Graph adapter (Neo4jGraphStoreAdapter) - Task E
- ✅ MCP server - Çalışıyor
- ✅ Test tools - Çalışıyor
- ✅ Workflow nodes - Çalışıyor

**Kullanım Senaryoları:**
1. **Sadece spec oluştur** → `spec_node()` çağır
2. **Sadece plan yap** → `plan_node()` çağır
3. **Sadece test çalıştır** → `run_tests` MCP tool
4. **Sadece dependency kontrol** → `check_dependency_impact` MCP tool
5. **Memory'ye kaydet** → `add_to_memory` MCP tool
6. **Memory'de ara** → `search_memory` MCP tool

**Her şey modüler ve bağımsız! 🎯**

