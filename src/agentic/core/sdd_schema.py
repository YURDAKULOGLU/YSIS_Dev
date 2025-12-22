from pydantic import BaseModel, Field
from typing import List

class Blueprint(BaseModel):
    """Blueprint model for defining system architecture and components."""
    
    name: str = Field(..., description="Name of the blueprint")
    version: str = Field(..., description="Version of the blueprint")
    components: list[str] = Field(..., description="List of components in the blueprint")

class Contract(BaseModel):
    """Contract model for defining technical contracts between system components."""
    
    component_name: str = Field(..., description="Name of the component")
    interface: dict = Field(..., description="Interface definition for the component")
    responsibilities: list[str] = Field(..., description="List of responsibilities of the component")

class TaskState(BaseModel):
    """Task state model for managing tasks in the system."""

    proposed_tasks: List[str] = Field(default_factory=list, description="List of proposed tasks")

    def add_proposed_task(self, task_title: str) -> None:
        """Add a proposed task to the state."""
        self.proposed_tasks.append(task_title)

class Validation(BaseModel):
    """Validation model for ensuring compliance with technical contracts."""
    
    contract_id: str = Field(..., description="ID of the contract being validated")
    validation_results: dict = Field(..., description="Results of the validation process")

# Example usage
if __name__ == "__main__":
    state = TaskState()
    state.add_proposed_task("Mission SDD: Full System Integration")
    print(state.proposed_tasks)
