# Define the task object with its respective attributes
class Task:
    def __init__(self, name, description):
        self.name = name
        self.description = description

# Create an instance of ControlPlaneDB to handle database operations
from control_plane_db import ControlPlaneDB
db = ControlPlaneDB()

# Initialize the Workspace struct using data_plane/workspace.py
from data_plane.workspace import Workspace
workspace = Workspace(db)

# Create a Graph and instantiate it as an OrchestratorGraph
from graph import Graph, OrchestratorGraph
graph = Graph()
orchestrator_graph = OrchestratorGraph(graph)

# Execute the plan and send signals to the control plane
task = Task("Sample Task", "This is a sample task for demonstration.")
workspace.execute_plan(task)
db.send_signal(task.name, "Task executed successfully")