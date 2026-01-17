import sqlite3
from data_plane.workspace import Workspace
from orchestrator.graph import Graph, OrchestratorGraph
from control_plane.control_plane_db import ControlPlaneDB
from executor.local_coder_executor import LocalCoderExecutor
from context.run_context import RunContext
from planner.llm_planner import LLMPlanner
from debate.debate_result import DebateResult

class Task:
    def __init__(self, name, description='', status='pending'):
        self.name = name
        self.description = description
        self.status = status

class TaskDatabase:
    def __init__(self, db_name='tasks.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')
        self.connection.commit()

    def add_task(self, name, description=''):
        self.cursor.execute('INSERT INTO tasks (name, description) VALUES (?, ?)', (name, description))
        self.connection.commit()
        return self.cursor.lastrowid

    def get_tasks(self):
        self.cursor.execute('SELECT * FROM tasks')
        return self.cursor.fetchall()

    def update_task_status(self, task_id, status):
        self.cursor.execute('UPDATE tasks SET status = ? WHERE id = ?', (status, task_id))
        self.connection.commit()

    def close(self):
        self.connection.close()

# Define the task object with its respective attributes
task = Task(name='Sample Task', description='This is a sample task')

# Create an instance of ControlPlaneDB to handle database operations
control_plane_db = ControlPlaneDB()

# Initialize the Workspace struct using data_plane/workspace.py
workspace = Workspace(task)

# Create a Graph and instantiate it as an OrchestratorGraph
graph = Graph()
orchestrator_graph = OrchestratorGraph(graph)

# Create a new instance of the LocalCoderExecutor class
local_coder_executor = LocalCoderExecutor()

# Create a new instance of the RunContext class
run_context = RunContext()

# Set up the database connection
task_db = TaskDatabase()

# Plan the task execution using the LLMPlanner class
llm_planner = LLMPlanner()
planned_task = llm_planner.plan(task)

# Start the debate process using the DebateResult class
debate_result = DebateResult(planned_task)
debate_result.start_debate()

# Execute the planned task
local_coder_executor.execute(planned_task, run_context)