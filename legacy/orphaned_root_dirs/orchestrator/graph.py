class Task:
    def __init__(self, name, function, dependencies=None):
        if dependencies is None:
            dependencies = []
        self.name = name
        self.function = function
        self.dependencies = dependencies

class ControlPlaneDB:
    def __init__(self):
        # Initialize database connection and other related configurations here
        pass

    def send_signal(self, signal):
        # Send signal to the control plane
        print(f"Sending signal: {signal}")

from data_plane.workspace import Workspace

class OrchestratorGraph(TaskGraph):
    def __init__(self, db, workspace):
        super().__init__()
        self.db = db
        self.workspace = workspace

    def execute_task(self, task_name):
        if task_name not in self.tasks:
            raise ValueError(f"Task {task_name} does not exist.")
        
        for dependency in self.dependencies[task_name]:
            self.execute_task(dependency)
        
        print(f"Executing {task_name}")
        self.tasks[task_name].function()
        self.db.send_signal(f"Executed {task_name}")

    def execute_all_tasks(self):
        for task_name in self.tasks:
            try:
                self.execute_task(task_name)
            except ValueError as e:
                print(e)

# Example usage
def task1():
    print("Task 1 executed")

def task2():
    print("Task 2 executed")

def task3():
    print("Task 3 executed")

task1_obj = Task("task1", task1)
task2_obj = Task("task2", task2, dependencies=["task1"])
task3_obj = Task("task3", task3)

db = ControlPlaneDB()
workspace = Workspace()

graph = OrchestratorGraph(db, workspace)
graph.add_task(task1_obj.name, task1_obj)
graph.add_task(task2_obj.name, task2_obj, dependencies=task2_obj.dependencies)
graph.add_task(task3_obj.name, task3_obj, dependencies=task3_obj.dependencies)

graph.execute_all_tasks()