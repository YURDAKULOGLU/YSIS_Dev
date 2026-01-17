class TaskExecutor:
    def __init__(self, tasks):
        self.tasks = tasks

    def execute_tasks(self):
        for task in self.tasks:
            print(f"Executing task: {task}")
            # Add logic to actually execute the task here
            task_result = self.run_task(task)
            print(f"Task result: {task_result}")

    def run_task(self, task):
        # Placeholder for actual task execution logic
        return f"Result of {task}"

if __name__ == "__main__":
    tasks = ["task1", "task2", "task3"]
    executor = TaskExecutor(tasks)
    executor.execute_tasks()