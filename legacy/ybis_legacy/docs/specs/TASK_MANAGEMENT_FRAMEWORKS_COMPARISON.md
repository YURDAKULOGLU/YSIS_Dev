# Task Management Framework Comparison

> Hangi framework'ü kullanmalıyız? Her birinin ne işe yaradığı ve ne zaman kullanılacağı.

---

## Framework'ler ve Kullanım Alanları

### 1. **Temporal** - Durable Workflows (ÖNERİLEN)

**Ne İşe Yarar:**
- **Durable State:** Task'lar crash olsa bile state kaybolmaz, kaldığı yerden devam eder
- **Automatic Retries:** Otomatik retry mekanizması (exponential backoff)
- **Long-Running Workflows:** Saatlerce süren işlemler için ideal
- **State Persistence:** Her adımın state'i kaydedilir, geri dönülebilir

**Ne Zaman Kullanılır:**
- ✅ Task'lar crash'te kaybolmamalı (şu anki IN_PROGRESS sorunu)
- ✅ Uzun süren işlemler (plan → execute → verify → commit)
- ✅ Automatic retry gerekiyor
- ✅ Multi-step workflows (plan, execute, verify, commit)

**Ne Zaman KULLANILMAZ:**
- ❌ Basit one-shot task'lar için overkill
- ❌ Real-time response gereken durumlar (biraz overhead var)

**Örnek Kullanım:**
```python
# Task workflow: Plan → Execute → Verify → Commit
# Her adım crash olsa bile kaldığı yerden devam eder
@workflow.defn
class TaskWorkflow:
    async def run(self, task_id: str):
        plan = await plan_task(task_id)      # Crash olsa bile state kaydedilir
        result = await execute_task(plan)    # Retry otomatik
        verified = await verify_task(result) # Her adım durable
        return commit_task(verified)
```

**YBIS İçin Uygun mu?**
✅ **EVET** - Şu anki IN_PROGRESS sorununu çözer, task'lar crash'te kaybolmaz

---

### 2. **Ray** - Distributed Task Execution

**Ne İşe Yarar:**
- **Distributed Computing:** Birden fazla makinede paralel çalışma
- **Actor Model:** Her agent bir "actor", birbirleriyle mesajlaşır
- **Resource Management:** GPU, CPU allocation
- **Fault Tolerance:** Worker crash olsa bile task başka worker'a geçer

**Ne Zaman Kullanılır:**
- ✅ Birden fazla agent aynı anda çalışmalı (parallel execution)
- ✅ GPU allocation gerekiyor (LLM inference)
- ✅ Distributed system (birden fazla makine)
- ✅ Resource management (kim hangi kaynağı kullanıyor)

**Ne Zaman KULLANILMAZ:**
- ❌ Single-node development (overkill)
- ❌ Basit task queue yeterliyse

**Örnek Kullanım:**
```python
# 3 agent paralel çalışıyor
@ray.remote
class Agent:
    async def work(self, task):
        # Agent çalışıyor
        return result

# Paralel execution
agents = [Agent.remote() for _ in range(3)]
results = ray.get([agent.work.remote(task) for agent in agents])
```

**YBIS İçin Uygun mu?**
⚠️ **ŞİMDİLİK HAYIR** - Single-node çalışıyoruz, distributed gerek yok (gelecekte olabilir)

---

### 3. **Prefect** - Modern Workflow Orchestration

**Ne İşe Yarar:**
- **Workflow Visualization:** Task'ların dependency graph'ı görselleştirilir
- **Task Dependencies:** Task A bitmeden Task B başlamaz
- **Scheduling:** Cron-like scheduling
- **Monitoring:** Task'ların durumu UI'da görünür

**Ne Zaman Kullanılır:**
- ✅ Complex task dependencies (A → B → C)
- ✅ Scheduled tasks (her gün saat 10'da çalış)
- ✅ Workflow visualization gerekiyor
- ✅ Task monitoring UI gerekiyor

**Ne Zaman KULLANILMAZ:**
- ❌ Basit linear workflows (plan → execute → verify)
- ❌ Durable state gerekmeyen durumlar

**Örnek Kullanım:**
```python
@flow
def task_workflow():
    plan = plan_task()      # Task 1
    result = execute_task(plan)  # Task 2 (plan bitmeden başlamaz)
    verify = verify_task(result) # Task 3 (execute bitmeden başlamaz)
    return commit_task(verify)
```

**YBIS İçin Uygun mu?**
⚠️ **ŞİMDİLİK HAYIR** - Workflow'umuz zaten linear (LangGraph var), visualization gerek yok

---

### 4. **SPADE** - Multi-Agent Framework

**Ne İşe Yarar:**
- **Agent Communication:** Agent'lar birbirleriyle mesajlaşır (XMPP protocol)
- **BDI Model:** Belief-Desire-Intention (agent'ın inançları, istekleri, niyetleri)
- **Distributed Agents:** Agent'lar farklı makinelerde olabilir
- **Agent Coordination:** Agent'lar birbirlerini koordine eder

**Ne Zaman Kullanılır:**
- ✅ Agent'lar birbirleriyle konuşmalı (mesajlaşma)
- ✅ Distributed agent system
- ✅ Agent coordination gerekiyor
- ✅ BDI model gerekiyor

**Ne Zaman KULLANILMAZ:**
- ❌ Centralized orchestration yeterliyse (LangGraph var)
- ❌ Agent'lar birbirleriyle konuşmuyorsa

**Örnek Kullanım:**
```python
# Agent 1: Planner
class PlannerAgent(Agent):
    async def plan(self, task):
        # Plan yap
        message = Message(to="executor@localhost", body=plan)
        await self.send(message)

# Agent 2: Executor
class ExecutorAgent(Agent):
    async def setup(self):
        self.add_behaviour(ReceivePlanBehaviour())
```

**YBIS İçin Uygun mu?**
❌ **HAYIR** - Agent'lar birbirleriyle mesajlaşmıyor, LangGraph orchestration yeterli

---

### 5. **Celery** - Distributed Task Queue

**Ne İşe Yarar:**
- **Task Queue:** Task'lar queue'ya atılır, worker'lar alır
- **Background Processing:** Async task execution
- **Scheduling:** Cron-like scheduling
- **Redis Backend:** Redis kullanır (zaten var)

**Ne Zaman Kullanılır:**
- ✅ Background task processing (email gönder, log parse et)
- ✅ Scheduled tasks (her gün saat 10'da çalış)
- ✅ Task queue gerekiyor (task'lar sıraya girsin)
- ✅ Worker pool (N worker, task'ları paylaş)

**Ne Zaman KULLANILMAZ:**
- ❌ Durable state gerekiyorsa (Temporal daha iyi)
- ❌ Complex workflows (Prefect daha iyi)
- ❌ Real-time coordination (Ray daha iyi)

**Örnek Kullanım:**
```python
@celery.task
def process_task(task_id):
    # Task işleniyor
    return result

# Task queue'ya at
process_task.delay(task_id)

# Worker'lar otomatik alır ve işler
```

**YBIS İçin Uygun mu?**
⚠️ **ŞİMDİLİK HAYIR** - Task queue yeterli değil, durable state gerekiyor (Temporal daha iyi)

---

## Karşılaştırma Tablosu

| Framework | Durable State | Retry | Multi-Agent | Distributed | Use Case |
|-----------|---------------|-------|-------------|-------------|----------|
| **Temporal** | ✅ ✅ ✅ | ✅ ✅ ✅ | ⚠️ | ✅ | Long-running workflows |
| **Ray** | ⚠️ | ⚠️ | ✅ ✅ ✅ | ✅ ✅ ✅ | Distributed parallel execution |
| **Prefect** | ⚠️ | ✅ | ⚠️ | ⚠️ | Workflow visualization |
| **SPADE** | ❌ | ❌ | ✅ ✅ ✅ | ✅ | Agent communication |
| **Celery** | ❌ | ✅ | ⚠️ | ✅ | Task queue |

---

## YBIS İçin ÖNERİ: **Temporal**

**Neden Temporal?**

1. **Şu Anki Sorun:** Task'lar IN_PROGRESS'te takılı kalıyor, crash'te kayboluyor
   - ✅ Temporal: Durable state, crash'te kaldığı yerden devam eder

2. **Workflow Yapımız:** Plan → Execute → Verify → Commit
   - ✅ Temporal: Multi-step workflows için ideal

3. **Retry Gereksinimi:** Task fail olursa otomatik retry
   - ✅ Temporal: Built-in retry mekanizması

4. **State Management:** Her adımın state'i kaydedilmeli
   - ✅ Temporal: Her adımın state'i persistent

**Diğer Framework'ler Neden Değil?**

- **Ray:** Distributed gerek yok, single-node yeterli
- **Prefect:** Workflow visualization gerek yok, LangGraph var
- **SPADE:** Agent communication gerek yok, LangGraph orchestration yeterli
- **Celery:** Task queue yeterli değil, durable state gerekiyor

---

## Implementation Plan

### Phase 1: Temporal Integration (ÖNCELİK)

1. **Install Temporal:**
   ```bash
   pip install temporalio
   docker run -p 7233:7233 temporalio/auto-setup:latest
   ```

2. **Create Temporal Workflow:**
   ```python
   # src/agentic/infrastructure/temporal_workflow.py
   @workflow.defn
   class TaskWorkflow:
       @workflow.run
       async def run(self, task_id: str) -> str:
           # Plan → Execute → Verify → Commit
           plan = await workflow.execute_activity(plan_task, task_id)
           result = await workflow.execute_activity(execute_task, plan)
           verified = await workflow.execute_activity(verify_task, result)
           return await workflow.execute_activity(commit_task, verified)
   ```

3. **Replace SQLite Task Management:**
   - Mevcut `claim_task()` → Temporal workflow start
   - IN_PROGRESS sorunu → Temporal durable state
   - Manual retry → Temporal automatic retry

### Phase 2: (Gelecekte) Ray Integration

Eğer gelecekte:
- Multiple agents paralel çalışmalı
- Distributed system gerekiyor
- GPU allocation gerekiyor

O zaman Ray eklenebilir. Şimdilik gerek yok.

---

## Sonuç

**ÖNERİLEN:** **Temporal** - Şu anki sorunları çözer, durable workflows sağlar

**KURULMAYACAK:**
- ❌ Ray (şimdilik gerek yok)
- ❌ Prefect (LangGraph yeterli)
- ❌ SPADE (agent communication gerek yok)
- ❌ Celery (Temporal daha iyi)

**KURULACAK:**
- ✅ Temporal (durable workflows, retry, state management)

---

**Not:** Eğer gelecekte ihtiyaç olursa (distributed, parallel execution), Ray eklenebilir. Ama şimdilik Temporal yeterli.

