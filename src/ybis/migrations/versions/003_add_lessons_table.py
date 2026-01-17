"""
Migration 003: Lessons learned table
"""

import sqlite3

from src.ybis.migrations.base import Migration


def up(conn: sqlite3.Connection):
    """Create lessons table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_type TEXT NOT NULL,
            source TEXT,
            content TEXT NOT NULL,
            context TEXT,
            applied_count INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_lessons_type ON lessons(lesson_type)")


def down(conn: sqlite3.Connection):
    """Drop lessons table."""
    conn.execute("DROP TABLE IF EXISTS lessons")


migration = Migration(
    version=3,
    name="add_lessons_table",
    up=up,
    down=down,
)

