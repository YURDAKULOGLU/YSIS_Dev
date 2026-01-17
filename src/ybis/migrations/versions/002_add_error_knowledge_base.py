"""
Migration 002: Error Knowledge Base tables
"""

import sqlite3

from src.ybis.migrations.base import Migration


def up(conn: sqlite3.Connection):
    """Create error KB tables."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS error_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT NOT NULL,
            run_id TEXT,
            step TEXT,
            error_type TEXT NOT NULL,
            error_message TEXT NOT NULL,
            stack_trace TEXT,
            context TEXT,
            created_at TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS error_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_type TEXT NOT NULL,
            error_message_pattern TEXT NOT NULL,
            occurrence_count INTEGER DEFAULT 1,
            suggested_fix TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_error_records_type ON error_records(error_type)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_error_records_task ON error_records(task_id)")


def down(conn: sqlite3.Connection):
    """Drop error KB tables."""
    conn.execute("DROP TABLE IF EXISTS error_patterns")
    conn.execute("DROP TABLE IF EXISTS error_records")


migration = Migration(
    version=2,
    name="add_error_knowledge_base",
    up=up,
    down=down,
)

