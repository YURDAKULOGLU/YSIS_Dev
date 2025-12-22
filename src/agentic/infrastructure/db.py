import sqlite3
from typing import Dict, List

class TaskDatabase:
    def __init__(self, db_path: str):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal TEXT NOT NULL,
            details TEXT,
            status TEXT NOT NULL,
            priority INTEGER,
            metadata TEXT
        );
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def add_task(self, task: Dict):
        insert_query = """
        INSERT INTO tasks (goal, details, status, priority, metadata)
        VALUES (?, ?, ?, ?, ?);
        """
        self.cursor.execute(insert_query, (
            task['goal'],
            task.get('details', ''),
            task['status'],
            task.get('priority', 0),
            task.get('metadata', '')
        ))
        self.connection.commit()

    def get_task(self, task_id: int) -> Dict:
        select_query = """
        SELECT * FROM tasks WHERE id = ?;
        """
        self.cursor.execute(select_query, (task_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'goal': row[1],
                'details': row[2],
                'status': row[3],
                'priority': row[4],
                'metadata': row[5]
            }
        return None

    def update_task(self, task_id: int, updates: Dict):
        update_query = """
        UPDATE tasks SET
            goal = ?,
            details = ?,
            status = ?,
            priority = ?,
            metadata = ?
        WHERE id = ?;
        """
        self.cursor.execute(update_query, (
            updates.get('goal', ''),
            updates.get('details', ''),
            updates.get('status', ''),
            updates.get('priority', 0),
            updates.get('metadata', ''),
            task_id
        ))
        self.connection.commit()

    def delete_task(self, task_id: int):
        delete_query = """
        DELETE FROM tasks WHERE id = ?;
        """
        self.cursor.execute(delete_query, (task_id,))
        self.connection.commit()

    def get_all_tasks(self) -> List[Dict]:
        select_all_query = """
        SELECT * FROM tasks;
        """
        self.cursor.execute(select_all_query)
        rows = self.cursor.fetchall()
        return [
            {
                'id': row[0],
                'goal': row[1],
                'details': row[2],
                'status': row[3],
                'priority': row[4],
                'metadata': row[5]
            }
            for row in rows
        ]

    def close(self):
        self.connection.close()
