from src.agentic.infrastructure.db import TaskDatabase
from src.agentic.core.config import TASKS_DB_PATH

class TaskBoardManager:
    def __init__(self):
        self.task_db = TaskDatabase(TASKS_DB_PATH)

    async def add_task(self, task: dict) -> int:
        """
        Adds a new task to the task board.

        Args:
            task (dict): The task details including goal, status, priority, and metadata.

        Returns:
            int: The ID of the newly added task.
        """
        self.task_db.add_task(task)
        return self.task_db.cursor.lastrowid

    async def get_task(self, task_id: int) -> dict:
        """
        Retrieves a task by its ID.

        Args:
            task_id (int): The ID of the task to retrieve.

        Returns:
            dict: The task details.
        """
        return self.task_db.get_task(task_id)

    async def update_task(self, task_id: int, updates: dict):
        """
        Updates an existing task.

        Args:
            task_id (int): The ID of the task to update.
            updates (dict): The fields to update in the task.
        """
        self.task_db.update_task(task_id, updates)

    async def delete_task(self, task_id: int):
        """
        Deletes a task by its ID.

        Args:
            task_id (int): The ID of the task to delete.
        """
        self.task_db.delete_task(task_id)

    async def get_all_tasks(self) -> list:
        """
        Retrieves all tasks from the task board.

        Returns:
            list: A list of all tasks.
        """
        return self.task_db.get_all_tasks()

    def close(self):
        """
        Closes the database connection.
        """
        self.task_db.close()
