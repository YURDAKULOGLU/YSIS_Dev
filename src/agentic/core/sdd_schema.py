from pydantic import BaseModel, Field

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

class Validation(BaseModel):
    """Validation model for ensuring compliance with technical contracts."""
    
    contract_id: str = Field(..., description="ID of the contract being validated")
    validation_results: dict = Field(..., description="Results of the validation process")
