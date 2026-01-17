"""
SPADE Adapter for Unified Task Abstraction.

Wraps SPADE agent behaviours in UnifiedTask interface.
"""

import asyncio
from typing import Optional, Any, Type

try:
    from spade.agent import Agent
    from spade.behaviour import OneShotBehaviour, CyclicBehaviour
    SPADE_AVAILABLE = True
except ImportError:
    SPADE_AVAILABLE = False
    Agent = None
    OneShotBehaviour = None
    CyclicBehaviour = None

from src.agentic.core.task_protocol import UnifiedTask, TaskStatus


class SPADETask(UnifiedTask):
    """SPADE agent behaviour adapter."""
    
    def __init__(self, task_id: str, agent: Agent, behaviour_class: Type[OneShotBehaviour], **kwargs):
        if not SPADE_AVAILABLE:
            raise ImportError("SPADE is not installed. Install with: pip install spade")
        
        super().__init__(task_id, "spade", kwargs)
        self.agent = agent
        self.behaviour_class = behaviour_class
        self.behaviour: Optional[OneShotBehaviour] = None
    
    async def start(self, *args, **kwargs) -> str:
        """Start SPADE behaviour."""
        self.behaviour = self.behaviour_class()
        self.agent.add_behaviour(self.behaviour)
        self.status = TaskStatus.RUNNING
        return self.task_id
    
    async def get_status(self) -> TaskStatus:
        """Get behaviour status."""
        if not self.behaviour:
            return TaskStatus.PENDING
        
        try:
            if self.behaviour.is_done():
                if self.behaviour.exit_code == 0:
                    return TaskStatus.COMPLETED
                else:
                    return TaskStatus.FAILED
            return TaskStatus.RUNNING
        except Exception:
            return TaskStatus.FAILED
    
    async def get_result(self) -> Any:
        """Get behaviour result."""
        if not self.behaviour:
            raise RuntimeError("Task not started")
        
        # Wait for completion
        while not self.behaviour.is_done():
            await asyncio.sleep(0.1)
        
        return getattr(self.behaviour, 'result', None)
    
    async def cancel(self) -> bool:
        """Cancel behaviour."""
        if not self.behaviour:
            return False
        try:
            self.behaviour.kill()
            self.status = TaskStatus.CANCELLED
            return True
        except Exception:
            return False
    
    async def retry(self) -> str:
        """Retry behaviour (restart)."""
        return await self.start()
    
    def get_native_object(self) -> Optional[OneShotBehaviour]:
        """Get native SPADE Behaviour."""
        return self.behaviour

