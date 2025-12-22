import json
from src.agentic.infrastructure.db import TaskDatabase
from src.agentic.core.config import TASKS_DB_PATH, DATA_DIR

def migrate_tasks():
    tasks_json_path = DATA_DIR / "tasks.json"
    db_path = TASKS_DB_PATH

    # Initialize the database
    task_db = TaskDatabase(db_path)

    # Load tasks from JSON file
    with open(tasks_json_path, 'r') as f:
        tasks = json.load(f)

    # Add each task to the SQLite database
    for task in tasks:
        task_db.add_task(task)

    print("Tasks migrated successfully.")

if __name__ == "__main__":
    migrate_tasks()
