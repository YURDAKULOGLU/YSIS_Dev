"""
Framework Adapters for Unified Task Abstraction.

Provides adapters for:
- Temporal (durable workflows)
- Ray (distributed execution)
- Prefect (workflow orchestration)
- SPADE (multi-agent communication)
- Celery (task queue)
"""

from .temporal_adapter import TemporalTask
from .ray_adapter import RayTask
from .prefect_adapter import PrefectTask
from .spade_adapter import SPADETask
from .celery_adapter import CeleryTask

__all__ = [
    "TemporalTask",
    "RayTask",
    "PrefectTask",
    "SPADETask",
    "CeleryTask",
]

