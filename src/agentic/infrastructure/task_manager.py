"""
Unified Task Manager - Single interface for all task frameworks.

Manages tasks across Temporal, Ray, Prefect, SPADE, and Celery using unified interface.
"""

from typing import Dict, Optional, List, Any
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.agentic.core.task_protocol import UnifiedTask, TaskStatus

# Import adapters (with error handling for missing frameworks)
try:
    from src.agentic.infrastructure.adapters.temporal_adapter import TemporalTask
except ImportError:
    TemporalTask = None

try:
    from src.agentic.infrastructure.adapters.ray_adapter import RayTask
except ImportError:
    RayTask = None

try:
    from src.agentic.infrastructure.adapters.prefect_adapter import PrefectTask
except ImportError:
    PrefectTask = None

try:
    from src.agentic.infrastructure.adapters.spade_adapter import SPADETask
except ImportError:
    SPADETask = None

try:
    from src.agentic.infrastructure.adapters.celery_adapter import CeleryTask
except ImportError:
    CeleryTask = None

from src.agentic.core.utils.logging_utils import log_event


class UnifiedTaskManager:
    """Manages tasks across all frameworks using unified interface."""
    
    def __init__(self):
        self.tasks: Dict[str, UnifiedTask] = {}
        self.framework_configs: Dict[str, Dict[str, Any]] = {
            "temporal": {"client": None},
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
            if TemporalTask is None:
                raise ImportError("Temporal is not installed. Install with: pip install temporalio")
            if "workflow_type" not in kwargs:
                raise ValueError("TemporalTask requires 'workflow_type' parameter")
            if "client" not in kwargs:
                raise ValueError("TemporalTask requires 'client' parameter (temporalio.client.Client)")
            task = TemporalTask(task_id, kwargs["workflow_type"], kwargs["client"], **kwargs)
        
        elif framework == "ray":
            if RayTask is None:
                raise ImportError("Ray is not installed. Install with: pip install ray[default]")
            if task_func is None:
                raise ValueError("RayTask requires 'task_func' parameter")
            task = RayTask(task_id, task_func, **kwargs)
        
        elif framework == "prefect":
            if PrefectTask is None:
                raise ImportError("Prefect is not installed. Install with: pip install prefect")
            if task_func is None:
                raise ValueError("PrefectTask requires 'task_func' parameter")
            task = PrefectTask(task_id, task_func, **kwargs)
        
        elif framework == "spade":
            if SPADETask is None:
                raise ImportError("SPADE is not installed. Install with: pip install spade")
            if "agent" not in kwargs or "behaviour_class" not in kwargs:
                raise ValueError("SPADETask requires 'agent' and 'behaviour_class' parameters")
            task = SPADETask(task_id, kwargs["agent"], kwargs["behaviour_class"], **kwargs)
        
        elif framework == "celery":
            if CeleryTask is None:
                raise ImportError("Celery is not installed. Install with: pip install celery[redis]")
            if task_func is None:
                raise ValueError("CeleryTask requires 'task_func' parameter")
            task = CeleryTask(task_id, task_func, **kwargs)
        
        else:
            raise ValueError(f"Unknown framework: {framework}. Supported: temporal, ray, prefect, spade, celery")
        
        self.tasks[task_id] = task
        log_event(f"Created {framework} task: {task_id}", component="task_manager")
        return task
    
    async def start_task(self, task_id: str, *args, **kwargs) -> str:
        """Start a task execution."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        exec_id = await task.start(*args, **kwargs)
        log_event(f"Started task {task_id} (exec_id: {exec_id})", component="task_manager")
        return exec_id
    
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
        result = await task.cancel()
        if result:
            log_event(f"Cancelled task {task_id}", component="task_manager")
        return result
    
    async def retry_task(self, task_id: str) -> str:
        """Retry failed task."""
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        exec_id = await task.retry()
        log_event(f"Retried task {task_id} (exec_id: {exec_id})", component="task_manager")
        return exec_id
    
    def list_tasks(self, framework: Optional[str] = None) -> List[UnifiedTask]:
        """List all tasks, optionally filtered by framework."""
        if framework:
            return [t for t in self.tasks.values() if t.framework == framework]
        return list(self.tasks.values())
    
    def get_task(self, task_id: str) -> Optional[UnifiedTask]:
        """Get task by ID."""
        return self.tasks.get(task_id)

