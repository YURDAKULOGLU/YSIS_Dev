from adapters import *
from contracts import *

from control_plane.db import ControlPlaneDB
from data_plane.journal import JournalWriter
from orchestrator.planner import planner

# Initialize the ControlPlaneDB
control_plane_db = ControlPlaneDB()

# Create a new JournalWriter instance
journal_writer = JournalWriter()

# Plan the task
planner.plan_task()