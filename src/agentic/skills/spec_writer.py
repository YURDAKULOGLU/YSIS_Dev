"""
SPEC WRITER SKILL (MCP Tool)
Generates professional technical specifications based on 'Claude Code' / 'Bmad' standards.
"""

from typing import Dict, Any
from pydantic import BaseModel, Field
import os

class SpecWriterInput(BaseModel):
    project_name: str = Field(..., description="Name of the project")
    description: str = Field(..., description="High-level description of what to build")
    tech_stack: str = Field("Python, React, PostgreSQL", description="Preferred technologies")

def generate_spec(input_data: SpecWriterInput) -> str:
    """
    Generates a full SPEC KIT structure for a project.
    """
    project = input_data.project_name
    desc = input_data.description
    stack = input_data.tech_stack

    # 1. Architecture
    arch_doc = f"""# {project} - ARCHITECTURE.md

## 1. Overview
{desc}

## 2. Tech Stack
- {stack}

## 3. Core Components
- **Frontend:** User Interface
- **Backend:** API & Business Logic
- **Database:** Data Persistence
- **Workers:** Background Jobs (if any)

## 4. Data Flow
[User] -> [Frontend] -> [API] -> [DB]
"""

    # 2. API Spec
    api_doc = f"""# {project} - API.md

## Endpoints

### GET /health
- **Response:** `{{ "status": "ok" }}`

### POST /api/v1/action
- **Input:** JSON body
- **Output:** Result object
"""

    # 3. Database Schema
    db_doc = f"""# {project} - SCHEMA.md

## Tables

### Users
- id (UUID, PK)
- email (VARCHAR, Unique)
- created_at (TIMESTAMP)

### Logs
- id (UUID, PK)
- message (TEXT)
"""

    # Save to disk (simulated 'Kit' generation)
    target_dir = f"specs/{project.lower().replace(' ', '_')}"
    os.makedirs(target_dir, exist_ok=True)

    with open(f"{target_dir}/ARCHITECTURE.md", "w") as f: f.write(arch_doc)
    with open(f"{target_dir}/API.md", "w") as f: f.write(api_doc)
    with open(f"{target_dir}/SCHEMA.md", "w") as f: f.write(db_doc)

    return f"[OK] Spec Kit generated at: {target_dir}/"
