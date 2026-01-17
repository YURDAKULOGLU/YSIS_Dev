"""
Temporal Adapter for Unified Task Abstraction.

Wraps Temporal workflows in UnifiedTask interface.
"""

from typing import Optional, Any
from temporalio.client import Client
from temporalio.workflow import WorkflowExecution

from src.agentic.core.task_protocol import UnifiedTask, TaskStatus


class TemporalTask(UnifiedTask):
    """Temporal workflow adapter."""
    
    def __init__(self, task_id: str, workflow_type: str, client: Client, **kwargs):
        super().__init__(task_id, "temporal", kwargs)
        self.workflow_type = workflow_type
        self.client = client
        self.execution: Optional[WorkflowExecution] = None
    
    async def start(self, *args, **kwargs) -> str:
        """Start Temporal workflow."""
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
        """Get workflow status."""
        if not self.execution:
            return TaskStatus.PENDING
        
        try:
            desc = await self.execution.describe()
            status_name = desc.status.name if hasattr(desc.status, 'name') else str(desc.status)
            
            if status_name == "RUNNING":
                return TaskStatus.RUNNING
            elif status_name == "COMPLETED":
                return TaskStatus.COMPLETED
            elif status_name == "FAILED":
                return TaskStatus.FAILED
            elif status_name == "CANCELLED":
                return TaskStatus.CANCELLED
            return TaskStatus.PENDING
        except Exception:
            return TaskStatus.FAILED
    
    async def get_result(self) -> Any:
        """Get workflow result."""
        if not self.execution:
            raise RuntimeError("Task not started")
        return await self.execution.result()
    
    async def cancel(self) -> bool:
        """Cancel workflow."""
        if not self.execution:
            return False
        try:
            await self.execution.cancel()
            self.status = TaskStatus.CANCELLED
            return True
        except Exception:
            return False
    
    async def retry(self) -> str:
        """Retry workflow (restart)."""
        return await self.start()
    
    def get_native_object(self) -> Optional[WorkflowExecution]:
        """Get native Temporal WorkflowExecution."""
        return self.execution

