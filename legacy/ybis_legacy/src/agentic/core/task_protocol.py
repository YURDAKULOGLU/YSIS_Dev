"""
Unified Task Protocol - Common interface for all task management frameworks.

Allows YBIS to use Temporal, Ray, Prefect, SPADE, or Celery through a single interface.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from enum import Enum


class TaskStatus(Enum):
    """Unified task status across all frameworks."""
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

