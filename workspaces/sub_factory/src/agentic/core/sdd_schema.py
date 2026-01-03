
from pydantic import BaseModel, Field
from src.agentic.core.utils.logging_utils import log_event


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

    proposed_tasks: list[str] = Field(default_factory=list, description="List of proposed tasks")

    def add_proposed_task(self, task_title: str) -> None:
        """Add a proposed task to the state."""
        self.proposed_tasks.append(task_title)

class Validation(BaseModel):
    """Validation model for ensuring compliance with technical contracts."""

    contract_id: str = Field(..., description="ID of the contract being validated")
    validation_results: dict = Field(..., description="Results of the validation process")

# Example usage
if __name__ == "__main__":
    from src.agentic.core.config import PROJECT_ROOT

    # Verify that src/agentic/core/sdd_schema.py exists in the repository.
    sdd_schema_path = PROJECT_ROOT / "src" / "agentic" / "core" / "sdd_schema.py"
    if sdd_schema_path.exists():
        state = TaskState()
        state.add_proposed_task("Mission SDD: Full System Integration")
        state.add_proposed_task("Follow-up Task: Validate Self-Propagation Protocol")
        # Ensure the state object contains the proposed task without running any shell scripts
        assert "Mission SDD: Full System Integration" in state.proposed_tasks
        assert "Follow-up Task: Validate Self-Propagation Protocol" in state.proposed_tasks
    else:
        log_event(f"{sdd_schema_path} dosyası bulunamadı.", component="sdd_schema", level="warning")
