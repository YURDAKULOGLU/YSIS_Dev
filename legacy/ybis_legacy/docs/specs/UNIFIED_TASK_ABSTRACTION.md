# Unified Task Abstraction Layer

> Tüm framework'lerdeki (Temporal, Ray, Prefect, SPADE, Celery) task'ları ortak paydada toplamak için unified interface.

---

## Problem

Farklı framework'ler farklı task objeleri kullanıyor:
- **Temporal:** `WorkflowExecution`
- **Ray:** `ObjectRef` veya `ActorHandle`
- **Prefect:** `FlowRun` veya `TaskRun`
- **SPADE:** `Behaviour` veya `Message`
- **Celery:** `AsyncResult`

**Sorun:** Her framework'ün kendi task objesi var, ortak bir interface yok.

**Çözüm:** Unified Task Abstraction Layer - Tüm framework'leri tek interface'den yönet.

---

## Unified Task Interface

### 1. Task Protocol (Abstract Base)

```python
# src/agentic/core/protocols/task_protocol.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    RETRYING = "retrying"

class UnifiedTask(ABC):
    """Unified task interface for all frameworks."""
    
    def __init__(self, task_id: str, framework: str, metadata: Dict[str, Any] = None):
        self.task_id = task_id
        self.framework = framework  # "temporal", "ray", "prefect", "spade", "celery"
        self.metadata = metadata or {}
        self.status = TaskStatus.PENDING
    
    @abstractmethod
    async def start(self, *args, **kwargs) -> str:
        """Start task execution. Returns execution ID."""
        pass
    
    @abstractmethod
    async def get_status(self) -> TaskStatus:
        """Get current task status."""
        pass
    
    @abstractmethod
    async def get_result(self) -> Any:
        """Get task result (blocks until complete)."""
        pass
    
    @abstractmethod
    async def cancel(self) -> bool:
        """Cancel task execution."""
        pass
    
    @abstractmethod
    async def retry(self) -> str:
        """Retry failed task. Returns new execution ID."""
        pass
    
    @abstractmethod
    def get_native_object(self) -> Any:
        """Get native framework object (for advanced usage)."""
        pass
```

---

## Framework Adapters

### 2. Temporal Adapter

```python
# src/agentic/infrastructure/adapters/temporal_adapter.py
from temporalio.client import Client
from temporalio.workflow import WorkflowExecution
from src.agentic.core.protocols.task_protocol import UnifiedTask, TaskStatus

class TemporalTask(UnifiedTask):
    """Temporal workflow adapter."""
    
    def __init__(self, task_id: str, workflow_type: str, client: Client, **kwargs):
        super().__init__(task_id, "temporal", kwargs)
        self.workflow_type = workflow_type
        self.client = client
        self.execution: Optional[WorkflowExecution] = None
    
    async def start(self, *args, **kwargs) -> str:
        handle = await self.client.start_workflow(
            self.workflow_type,
            *args,
            id=self.task_id,
            **kwargs
        )
        self.execution = handle
        self.status = TaskStatus.RUNNING
        return handle.id
    
    async def get_status(self) -> TaskStatus:
        if not self.execution:
            return TaskStatus.PENDING
        
        desc = await self.execution.describe()
        if desc.status.name == "RUNNING":
            return TaskStatus.RUNNING
        elif desc.status.name == "COMPLETED":
            return TaskStatus.COMPLETED
        elif desc.status.name == "FAILED":
            return TaskStatus.FAILED
        elif desc.status.name == "CANCELLED":
            return TaskStatus.CANCELLED
        return TaskStatus.PENDING
    
    async def get_result(self) -> Any:
        if not self.execution:
            raise RuntimeError("Task not started")
        return await self.execution.result()
    
    async def cancel(self) -> bool:
        if not self.execution:
            return False
        await self.execution.cancel()
        self.status = TaskStatus.CANCELLED
        return True
    
    async def retry(self) -> str:
        # Temporal automatically retries, but we can restart
        return await self.start()
    
    def get_native_object(self) -> WorkflowExecution:
        return self.execution
```

---

### 3. Ray Adapter

```python
# src/agentic/infrastructure/adapters/ray_adapter.py
import ray
from ray import ObjectRef
from src.agentic.core.protocols.task_protocol import UnifiedTask, TaskStatus

class RayTask(UnifiedTask):
    """Ray task adapter."""
    
    def __init__(self, task_id: str, task_func, **kwargs):
        super().__init__(task_id, "ray", kwargs)
        self.task_func = task_func
        self.object_ref: Optional[ObjectRef] = None
    
    async def start(self, *args, **kwargs) -> str:
        self.object_ref = self.task_func.remote(*args, **kwargs)
        self.status = TaskStatus.RUNNING
        return self.task_id
    
    async def get_status(self) -> TaskStatus:
        if not self.object_ref:
            return TaskStatus.PENDING
        
        # Ray doesn't have direct status, check if done
        try:
            # Non-blocking check
            ready, _ = ray.wait([self.object_ref], timeout=0.01, num_returns=1)
            if ready:
                return TaskStatus.COMPLETED
            return TaskStatus.RUNNING
        except Exception:
            return TaskStatus.FAILED
    
    async def get_result(self) -> Any:
        if not self.object_ref:
            raise RuntimeError("Task not started")
        return await self.object_ref
    
    async def cancel(self) -> bool:
        if not self.object_ref:
            return False
        ray.cancel(self.object_ref)
        self.status = TaskStatus.CANCELLED
        return True
    
    async def retry(self) -> str:
        # Restart Ray task
        return await self.start()
    
    def get_native_object(self) -> ObjectRef:
        return self.object_ref
```

---

### 4. Prefect Adapter

```python
# src/agentic/infrastructure/adapters/prefect_adapter.py
from prefect import flow, task
from prefect.client.schemas.objects import FlowRun, TaskRun
from src.agentic.core.protocols.task_protocol import UnifiedTask, TaskStatus

class PrefectTask(UnifiedTask):
    """Prefect flow/task adapter."""
    
    def __init__(self, task_id: str, flow_func, **kwargs):
        super().__init__(task_id, "prefect", kwargs)
        self.flow_func = flow_func
        self.flow_run: Optional[FlowRun] = None
    
    async def start(self, *args, **kwargs) -> str:
        self.flow_run = await self.flow_func(*args, **kwargs)
        self.status = TaskStatus.RUNNING
        return str(self.flow_run.id)
    
    async def get_status(self) -> TaskStatus:
        if not self.flow_run:
            return TaskStatus.PENDING
        
        state = self.flow_run.state
        if state.is_running():
            return TaskStatus.RUNNING
        elif state.is_completed():
            return TaskStatus.COMPLETED
        elif state.is_failed():
            return TaskStatus.FAILED
        elif state.is_cancelled():
            return TaskStatus.CANCELLED
        return TaskStatus.PENDING
    
    async def get_result(self) -> Any:
        if not self.flow_run:
            raise RuntimeError("Task not started")
        return self.flow_run.state.result()
    
    async def cancel(self) -> bool:
        if not self.flow_run:
            return False
        await self.flow_run.cancel()
        self.status = TaskStatus.CANCELLED
        return True
    
    async def retry(self) -> str:
        # Prefect has built-in retry, but we can restart
        return await self.start()
    
    def get_native_object(self) -> FlowRun:
        return self.flow_run
```

---

### 5. SPADE Adapter

```python
# src/agentic/infrastructure/adapters/spade_adapter.py
from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
from src.agentic.core.protocols.task_protocol import UnifiedTask, TaskStatus

class SPADETask(UnifiedTask):
    """SPADE agent behaviour adapter."""
    
    def __init__(self, task_id: str, agent: Agent, behaviour_class, **kwargs):
        super().__init__(task_id, "spade", kwargs)
        self.agent = agent
        self.behaviour_class = behaviour_class
        self.behaviour: Optional[OneShotBehaviour] = None
    
    async def start(self, *args, **kwargs) -> str:
        self.behaviour = self.behaviour_class()
        self.agent.add_behaviour(self.behaviour)
        self.status = TaskStatus.RUNNING
        return self.task_id
    
    async def get_status(self) -> TaskStatus:
        if not self.behaviour:
            return TaskStatus.PENDING
        
        if self.behaviour.is_done():
            if self.behaviour.exit_code == 0:
                return TaskStatus.COMPLETED
            else:
                return TaskStatus.FAILED
        return TaskStatus.RUNNING
    
    async def get_result(self) -> Any:
        if not self.behaviour:
            raise RuntimeError("Task not started")
        
        # Wait for completion
        while not self.behaviour.is_done():
            await asyncio.sleep(0.1)
        
        return self.behaviour.result if hasattr(self.behaviour, 'result') else None
    
    async def cancel(self) -> bool:
        if not self.behaviour:
            return False
        self.behaviour.kill()
        self.status = TaskStatus.CANCELLED
        return True
    
    async def retry(self) -> str:
        return await self.start()
    
    def get_native_object(self) -> OneShotBehaviour:
        return self.behaviour
```

---

### 6. Celery Adapter

```python
# src/agentic/infrastructure/adapters/celery_adapter.py
from celery.result import AsyncResult
from src.agentic.core.protocols.task_protocol import UnifiedTask, TaskStatus

class CeleryTask(UnifiedTask):
    """Celery task adapter."""
    
    def __init__(self, task_id: str, task_func, **kwargs):
        super().__init__(task_id, "celery", kwargs)
        self.task_func = task_func
        self.async_result: Optional[AsyncResult] = None
    
    async def start(self, *args, **kwargs) -> str:
        self.async_result = self.task_func.delay(*args, **kwargs)
        self.status = TaskStatus.RUNNING
        return self.async_result.id
    
    async def get_status(self) -> TaskStatus:
        if not self.async_result:
            return TaskStatus.PENDING
        
        if self.async_result.ready():
            if self.async_result.successful():
                return TaskStatus.COMPLETED
            else:
                return TaskStatus.FAILED
        return TaskStatus.RUNNING
    
    async def get_result(self) -> Any:
        if not self.async_result:
            raise RuntimeError("Task not started")
        return self.async_result.get()
    
    async def cancel(self) -> bool:
        if not self.async_result:
            return False
        self.async_result.revoke(terminate=True)
        self.status = TaskStatus.CANCELLED
        return True
    
    async def retry(self) -> str:
        return await self.start()
    
    def get_native_object(self) -> AsyncResult:
        return self.async_result
```

---

## Task Manager (Unified Interface)

### 7. Unified Task Manager

```python
# src/agentic/infrastructure/task_manager.py
from typing import Dict, Optional, List
from src.agentic.core.protocols.task_protocol import UnifiedTask, TaskStatus
from src.agentic.infrastructure.adapters.temporal_adapter import TemporalTask
from src.agentic.infrastructure.adapters.ray_adapter import RayTask
from src.agentic.infrastructure.adapters.prefect_adapter import PrefectTask
from src.agentic.infrastructure.adapters.spade_adapter import SPADETask
from src.agentic.infrastructure.adapters.celery_adapter import CeleryTask

class UnifiedTaskManager:
    """Manages tasks across all frameworks using unified interface."""
    
    def __init__(self):
        self.tasks: Dict[str, UnifiedTask] = {}
        self.framework_configs = {
            "temporal": {"client": None},  # Will be initialized
            "ray": {"initialized": False},
            "prefect": {},
            "spade": {},
            "celery": {"app": None}
        }
    
    def create_task(
        self,
        task_id: str,
        framework: str,
        task_func=None,
        **kwargs
    ) -> UnifiedTask:
        """Create a unified task for specified framework."""
        
        if framework == "temporal":
            task = TemporalTask(task_id, kwargs.get("workflow_type"), **kwargs)
        elif framework == "ray":
            task = RayTask(task_id, task_func, **kwargs)
        elif framework == "prefect":
            task = PrefectTask(task_id, task_func, **kwargs)
        elif framework == "spade":
            task = SPADETask(task_id, kwargs.get("agent"), kwargs.get("behaviour_class"), **kwargs)
        elif framework == "celery":
            task = CeleryTask(task_id, task_func, **kwargs)
        else:
            raise ValueError(f"Unknown framework: {framework}")
        
        self.tasks[task_id] = task
        return task
    
    async def start_task(self, task_id: str, *args, **kwargs) -> str:
        """Start a task execution."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return await task.start(*args, **kwargs)
    
    async def get_task_status(self, task_id: str) -> TaskStatus:
        """Get task status."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return await task.get_status()
    
    async def get_task_result(self, task_id: str) -> Any:
        """Get task result."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return await task.get_result()
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel task execution."""
        task = self.tasks.get(task_id)
        if not task:
            return False
        return await task.cancel()
    
    async def retry_task(self, task_id: str) -> str:
        """Retry failed task."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        return await task.retry()
    
    def list_tasks(self, framework: Optional[str] = None) -> List[UnifiedTask]:
        """List all tasks, optionally filtered by framework."""
        if framework:
            return [t for t in self.tasks.values() if t.framework == framework]
        return list(self.tasks.values())
```

---

## Usage Example

```python
# src/agentic/core/plugins/unified_executor.py
from src.agentic.infrastructure.task_manager import UnifiedTaskManager

class UnifiedExecutor:
    """Executor that can use any framework via unified interface."""
    
    def __init__(self):
        self.task_manager = UnifiedTaskManager()
        self.default_framework = "temporal"  # Or "ray", "prefect", etc.
    
    async def execute_task(self, task_id: str, framework: str = None, **kwargs):
        """Execute task using specified framework (or default)."""
        framework = framework or self.default_framework
        
        # Create unified task
        task = self.task_manager.create_task(
            task_id=task_id,
            framework=framework,
            task_func=self._task_function,
            **kwargs
        )
        
        # Start execution
        exec_id = await self.task_manager.start_task(task_id, **kwargs)
        
        # Wait for result
        result = await self.task_manager.get_task_result(task_id)
        
        return result
    
    def _task_function(self, *args, **kwargs):
        """Actual task implementation."""
        # This will be wrapped by framework-specific adapters
        pass
```

---

## Framework Selection Strategy

```python
# src/agentic/core/plugins/framework_selector.py
class FrameworkSelector:
    """Select optimal framework based on task requirements."""
    
    def select_framework(
        self,
        task_complexity: str,
        requires_durable_state: bool,
        requires_distributed: bool,
        requires_agent_communication: bool,
        requires_visualization: bool
    ) -> str:
        """Select best framework for task."""
        
        if requires_durable_state:
            return "temporal"  # Best for durable workflows
        
        if requires_distributed:
            return "ray"  # Best for distributed execution
        
        if requires_agent_communication:
            return "spade"  # Best for agent-to-agent messaging
        
        if requires_visualization:
            return "prefect"  # Best for workflow visualization
        
        # Default: Temporal (most robust)
        return "temporal"
```

---

## Benefits

1. **Unified Interface:** Tüm framework'ler tek interface'den yönetilir
2. **Framework Agnostic:** Kod framework'den bağımsız
3. **Easy Switching:** Framework değiştirmek kolay
4. **Multi-Framework:** Aynı anda birden fazla framework kullanılabilir
5. **Type Safety:** Protocol-based, type-safe

---

## Next Steps

1. ✅ Create `TaskProtocol` (abstract base)
2. ✅ Create framework adapters (Temporal, Ray, Prefect, SPADE, Celery)
3. ✅ Create `UnifiedTaskManager`
4. ✅ Create `FrameworkSelector`
5. ⏳ Integrate with existing orchestrator
6. ⏳ Add framework-specific configuration
7. ⏳ Add monitoring/logging for all frameworks

