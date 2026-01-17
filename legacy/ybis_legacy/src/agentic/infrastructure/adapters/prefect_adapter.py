"""
Prefect Adapter for Unified Task Abstraction.

Wraps Prefect flows/tasks in UnifiedTask interface.
"""

from typing import Optional, Any, Callable

try:
    from prefect import flow
    from prefect.client.schemas.objects import FlowRun
    PREFECT_AVAILABLE = True
except ImportError:
    PREFECT_AVAILABLE = False
    flow = None
    FlowRun = None

from src.agentic.core.task_protocol import UnifiedTask, TaskStatus


class PrefectTask(UnifiedTask):
    """Prefect flow/task adapter."""
    
    def __init__(self, task_id: str, flow_func: Callable, **kwargs):
        if not PREFECT_AVAILABLE:
            raise ImportError("Prefect is not installed. Install with: pip install prefect")
        
        super().__init__(task_id, "prefect", kwargs)
        self.flow_func = flow_func
        self.flow_run: Optional[FlowRun] = None
    
    async def start(self, *args, **kwargs) -> str:
        """Start Prefect flow."""
        self.flow_run = await self.flow_func(*args, **kwargs)
        self.status = TaskStatus.RUNNING
        return str(self.flow_run.id)
    
    async def get_status(self) -> TaskStatus:
        """Get flow status."""
        if not self.flow_run:
            return TaskStatus.PENDING
        
        try:
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
        except Exception:
            return TaskStatus.FAILED
    
    async def get_result(self) -> Any:
        """Get flow result."""
        if not self.flow_run:
            raise RuntimeError("Task not started")
        return self.flow_run.state.result()
    
    async def cancel(self) -> bool:
        """Cancel flow."""
        if not self.flow_run:
            return False
        try:
            await self.flow_run.cancel()
            self.status = TaskStatus.CANCELLED
            return True
        except Exception:
            return False
    
    async def retry(self) -> str:
        """Retry flow (restart)."""
        return await self.start()
    
    def get_native_object(self) -> Optional[FlowRun]:
        """Get native Prefect FlowRun."""
        return self.flow_run

