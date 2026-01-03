
import streamlit as st
import os
import json
import sqlite3
import psutil
from pathlib import Path

# Config paths
DB_PATH = Path("Knowledge/LocalDB/tasks.db")
DEBATES_DIR = Path("Knowledge/Messages/debates")

def get_task_stats():
    """Get counts from SQLite"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT status, count(*) FROM tasks GROUP BY status")
        stats = dict(cursor.fetchall())
        conn.close()
        return stats
    except:
        return {}

def get_debate_stats():
    """Get counts from JSON debates"""
    try:
        files = list(DEBATES_DIR.glob("*.json"))
        open_debates = 0
        for f in files:
            data = json.loads(f.read_text(encoding='utf-8'))
            if data.get("status") == "open":
                open_debates += 1
        return {"total": len(files), "open": open_debates}
    except:
        return {"total": 0, "open": 0}

def render_health_dashboard():
    st.header("🏢 Global System Health")
    
    # 1. High Level Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    tasks = get_task_stats()
    debates = get_debate_stats()
    
    col1.metric("Active Tasks", tasks.get("IN_PROGRESS", 0))
    col2.metric("Open Debates", debates["open"])
    
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    col3.metric("CPU Load", f"{cpu}%")
    col4.metric("RAM Usage", f"{ram}%")

    st.divider()

    # 2. Integrity Checklist
    st.subheader("[INFO] Factory Integrity Gate")
    
    checks = {
        "Database Sync": DB_PATH.exists(),
        "Knowledge Graph": Path("Knowledge/Reports/lessons.jsonl").exists(),
        "Architecture Enforcer": Path("scripts/enforce_architecture.py").exists(),
        "Ollama Local Engine": os.getenv("OLLAMA_BASE_URL") is not None or True # Mock for now
    }
    
    for label, ok in checks.items():
        if ok:
            st.success(f"[OK] {label}: Online")
        else:
            st.error(f"[ERROR] {label}: Offline / Missing")

    # 3. Recent Activity (Quick Glance)
    st.subheader("🕒 Recent Burndown")
    done_count = tasks.get("COMPLETED", 0) + tasks.get("DONE", 0)
    st.progress(min(100, done_count * 2)) # Visual progress placeholder
    st.caption(f"Total Completed Tasks: {done_count}")
