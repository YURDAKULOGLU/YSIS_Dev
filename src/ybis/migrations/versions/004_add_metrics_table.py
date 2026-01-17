"""
Migration 004: Metrics tracking table
"""

import sqlite3

from src.ybis.migrations.base import Migration


def up(conn: sqlite3.Connection):
    """Create metrics table."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_name TEXT NOT NULL,
            metric_value REAL NOT NULL,
            labels TEXT,
            timestamp TEXT NOT NULL
        )
    """)

    conn.execute("CREATE INDEX IF NOT EXISTS idx_metrics_name ON metrics(metric_name)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics(timestamp)")


def down(conn: sqlite3.Connection):
    """Drop metrics table."""
    conn.execute("DROP TABLE IF EXISTS metrics")


migration = Migration(
    version=4,
    name="add_metrics_table",
    up=up,
    down=down,
)

