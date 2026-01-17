"""
Ray Adapter for Unified Task Abstraction.

Wraps Ray tasks/actors in UnifiedTask interface.
"""

from typing import Optional, Any

try:
    import ray
    from ray import ObjectRef
    RAY_AVAILABLE = True
except ImportError:
    RAY_AVAILABLE = False
    ray = None
    ObjectRef = None

from src.agentic.core.task_protocol import UnifiedTask, TaskStatus


class RayTask(UnifiedTask):
    """Ray task adapter."""
    
    def __init__(self, task_id: str, task_func, **kwargs):
        if not RAY_AVAILABLE:
            raise ImportError("Ray is not installed. Install with: pip install ray[default]")
        
        super().__init__(task_id, "ray", kwargs)
        self.task_func = task_func
        self.object_ref: Optional[ObjectRef] = None
    
    async def start(self, *args, **kwargs) -> str:
        """Start Ray task."""
        if not ray.is_initialized():
            ray.init(ignore_reinit_error=True)
        
        self.object_ref = self.task_func.remote(*args, **kwargs)
        self.status = TaskStatus.RUNNING
        return self.task_id
    
    async def get_status(self) -> TaskStatus:
        """Get task status."""
        if not self.object_ref:
            return TaskStatus.PENDING
        
        try:
            # Non-blocking check
            ready, _ = ray.wait([self.object_ref], timeout=0.01, num_returns=1)
            if ready:
                return TaskStatus.COMPLETED
            return TaskStatus.RUNNING
        except Exception:
            return TaskStatus.FAILED
    
    async def get_result(self) -> Any:
        """Get task result."""
        if not self.object_ref:
            raise RuntimeError("Task not started")
        return await self.object_ref
    
    async def cancel(self) -> bool:
        """Cancel Ray task."""
        if not self.object_ref:
            return False
        try:
            ray.cancel(self.object_ref)
            self.status = TaskStatus.CANCELLED
            return True
        except Exception:
            return False
    
    async def retry(self) -> str:
        """Retry task (restart)."""
        return await self.start()
    
    def get_native_object(self) -> Optional[ObjectRef]:
        """Get native Ray ObjectRef."""
        return self.object_ref

