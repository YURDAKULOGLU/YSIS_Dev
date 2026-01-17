from adapters import *
from contracts import *

# Initialize ControlPlaneDB
from control_plane.db import ControlPlaneDB
control_plane_db = ControlPlaneDB()

# Create a new JournalWriter instance
from data_plane.journal import JournalWriter
journal_writer = JournalWriter()

# Plan the task
from orchestrator.planner import plan_task
planned_task = plan_task()