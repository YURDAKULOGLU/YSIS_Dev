"""
Celery Adapter for Unified Task Abstraction.

Wraps Celery tasks in UnifiedTask interface.
"""

from typing import Optional, Any, Callable

try:
    from celery.result import AsyncResult
    CELERY_AVAILABLE = True
except ImportError:
    CELERY_AVAILABLE = False
    AsyncResult = None

from src.agentic.core.task_protocol import UnifiedTask, TaskStatus


class CeleryTask(UnifiedTask):
    """Celery task adapter."""
    
    def __init__(self, task_id: str, task_func: Callable, **kwargs):
        if not CELERY_AVAILABLE:
            raise ImportError("Celery is not installed. Install with: pip install celery[redis]")
        
        super().__init__(task_id, "celery", kwargs)
        self.task_func = task_func
        self.async_result: Optional[AsyncResult] = None
    
    async def start(self, *args, **kwargs) -> str:
        """Start Celery task."""
        self.async_result = self.task_func.delay(*args, **kwargs)
        self.status = TaskStatus.RUNNING
        return self.async_result.id
    
    async def get_status(self) -> TaskStatus:
        """Get task status."""
        if not self.async_result:
            return TaskStatus.PENDING
        
        try:
            if self.async_result.ready():
                if self.async_result.successful():
                    return TaskStatus.COMPLETED
                else:
                    return TaskStatus.FAILED
            return TaskStatus.RUNNING
        except Exception:
            return TaskStatus.FAILED
    
    async def get_result(self) -> Any:
        """Get task result."""
        if not self.async_result:
            raise RuntimeError("Task not started")
        return self.async_result.get()
    
    async def cancel(self) -> bool:
        """Cancel Celery task."""
        if not self.async_result:
            return False
        try:
            self.async_result.revoke(terminate=True)
            self.status = TaskStatus.CANCELLED
            return True
        except Exception:
            return False
    
    async def retry(self) -> str:
        """Retry task (restart)."""
        return await self.start()
    
    def get_native_object(self) -> Optional[AsyncResult]:
        """Get native Celery AsyncResult."""
        return self.async_result

