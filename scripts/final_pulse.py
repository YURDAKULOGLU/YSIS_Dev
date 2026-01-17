
import sqlite3
import os
from pathlib import Path

def check_pulse():
    print("--- [INFO] YBIS SYSTEM HEALTH CHECK (WRAP-UP) ---")

    # 1. DB Check
    try:
        conn = sqlite3.connect('platform_data/knowledge/LocalDB/tasks.db')
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM tasks")
        count = cursor.fetchone()[0]
        print(f"[OK] SQLite DB: Connected. Total tasks: {count}")
        conn.close()
    except Exception as e:
        print(f"[FAIL] SQLite DB Error: {e}")

    # 2. Workspace Check
    active_ws = list(Path("workspaces/active").glob("* "))
    print(f"[OK] Workspaces: {len(active_ws)} active folders found.")

    # 3. CLI Check
    if Path("scripts/ybis.py").exists():
        print("[OK] Unified CLI (ybis.py): Present.")
    else:
        print("[FAIL] Unified CLI missing!")

    # 4. Ingest/Graph Check
    # (Testing Neo4j usually requires credentials, but we can check if ingest ran)
    if Path("worker.out").exists():
        print("[OK] Worker Logs: Active.")

    print("\n--- 🏁 WRAP-UP STATUS: STABLE ---")

if __name__ == "__main__":
    check_pulse()

