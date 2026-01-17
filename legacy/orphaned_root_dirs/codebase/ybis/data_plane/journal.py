from adapters import *
from contracts import *

# Initialize ControlPlaneDB
control_plane_db = ControlPlaneDB()

# Create a new JournalWriter instance
journal_writer = JournalWriter(control_plane_db)

# Plan the task using planner.py from the orchestrator directory
task_plan = orchestrator.planner.plan_task(journal_writer)