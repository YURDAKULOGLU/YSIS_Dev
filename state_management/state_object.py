from pydantic import BaseModel, Field
from typing import List, Dict

class State(BaseModel):
    """
    The central State object for the entire factory. Supports task chaining.
    """
    proposed_tasks: List[Dict[str, Any]] = Field(default_factory=lambda: [
        {
            "task_name": "Update_Architecture",
            "description": "Güncelleme SQLite + Pydantic + GitManager Tier 4.5 ile yapılmıştır.",
            "status": "PENDING"
        }
    ])

    class Config:
        arbitrary_types_allowed = True
