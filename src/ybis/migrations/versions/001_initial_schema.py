"""
Migration 001: Initial schema for control_plane.db
"""

import sqlite3

from src.ybis.migrations.base import Migration


def up(conn: sqlite3.Connection):
    """Create initial tables."""
    # Tasks table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            objective TEXT,
            status TEXT DEFAULT 'pending',
            priority TEXT DEFAULT 'MEDIUM',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Runs table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            run_id TEXT PRIMARY KEY,
            task_id TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TEXT NOT NULL,
            completed_at TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks(task_id)
        )
    """)

    # Create indexes
    conn.execute("CREATE INDEX IF NOT EXISTS idx_runs_task_id ON runs(task_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_runs_status ON runs(status)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)")


def down(conn: sqlite3.Connection):
    """Drop tables."""
    conn.execute("DROP TABLE IF EXISTS runs")
    conn.execute("DROP TABLE IF EXISTS tasks")


migration = Migration(
    version=1,
    name="initial_schema",
    up=up,
    down=down,
)

