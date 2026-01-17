import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.ybis.contracts import Task
from src.ybis.control_plane import ControlPlaneDB

async def seed_backlog():
    db_path = "platform_data/control_plane.db"
    db = ControlPlaneDB(db_path)
    await db.initialize()

    evolution_tasks = [
        # BATCH 18
        {
            "task_id": "BATCH-18-1",
            "title": "Tiered Execution (Cost Optimization)",
            "objective": "Update gates.py and graph.py to detect diff size and bypass heavy checks for small changes (Tier 0/1/2).",
            "priority": "HIGH"
        },
        {
            "task_id": "BATCH-18-2",
            "title": "Lesson Engine (Self-Supervised Governance)",
            "objective": "Implement services/lesson_engine.py to cluster failure signatures and auto-generate AUTO_RULES.md.",
            "priority": "HIGH"
        },
        {
            "task_id": "BATCH-18-3",
            "title": "Staleness Detector (Maintenance Mode)",
            "objective": "Implement services/staleness.py using Pyan to identify downstream files affected by core changes and auto-create fix tasks.",
            "priority": "MEDIUM"
        },
        {
            "task_id": "BATCH-18-4",
            "title": "Advanced Metrics (Dog Scales)",
            "objective": "Track GPU latency and token usage in Run model and add a Performance tab to the Streamlit Dashboard.",
            "priority": "MEDIUM"
        },
        
        # BATCH 19
        {
            "task_id": "BATCH-19-1",
            "title": "The Judge Persona",
            "objective": "Create adapters/judge_adapter.py using high-reasoning models (DeepSeek R1) to judge code against the spirit of the Constitution.",
            "priority": "MEDIUM"
        },
        {
            "task_id": "BATCH-19-2",
            "title": "Constitutional Gate Node",
            "objective": "Add a constitution_node to the LangGraph that blocks technically correct but philosophically non-compliant code.",
            "priority": "MEDIUM"
        },
        
        # BATCH 20
        {
            "task_id": "BATCH-20-1",
            "title": "Knowledge Graph Service (Deep Memory)",
            "objective": "Implement services/graph_memory.py using NetworkX to store relationships between Users, Tickets, and Files.",
            "priority": "LOW"
        },
        {
            "task_id": "BATCH-20-2",
            "title": "Relationship Extractor",
            "objective": "Implement an extraction pipeline in ingestor.py to find and store edges in the Knowledge Graph using LLM analysis.",
            "priority": "LOW"
        },
        
        # BATCH 21
        {
            "task_id": "BATCH-21-1",
            "title": "Remote Worker Protocol",
            "objective": "Implement UnifiedTask abstraction and update worker.py to support remote connections over HTTP/WebSocket.",
            "priority": "LOW"
        },
        {
            "task_id": "BATCH-21-2",
            "title": "Hive Dispatcher (Task Router)",
            "objective": "Implement services/router.py to intelligently dispatch tasks between CPU and GPU nodes based on Tier.",
            "priority": "LOW"
        },
        
        # BATCH 22
        {
            "task_id": "BATCH-22-1",
            "title": "Intent Parser (Singularity Interface)",
            "objective": "Create services/intent_parser.py to convert vague human requests into concrete technical specifications through dialogue.",
            "priority": "MEDIUM"
        },
        {
            "task_id": "BATCH-22-2",
            "title": "Autonomous Roadmap Management",
            "objective": "Enable the system to read logs and debt to auto-create Roadmap Epics in the backlog.",
            "priority": "LOW"
        }
    ]

    for t_data in evolution_tasks:
        task = Task(
            task_id=t_data["task_id"],
            title=t_data["title"],
            objective=t_data["objective"],
            priority=t_data["priority"],
            status="pending"
        )
        await db.register_task(task)
        print(f"[OK] Registered: {task.task_id} - {task.title}")

    print("\n[SUCCESS] Evolution Plan seeded into Control Plane Backlog.")

if __name__ == "__main__":
    asyncio.run(seed_backlog())
