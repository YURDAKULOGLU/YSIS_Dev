"""
YBIS CONTROL CENTER (Streamlit)
The central cockpit for the Autonomous Factory.
"""

import streamlit as st
import json
import os
import sys
import pandas as pd
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Imports from our bridges
try:
    from src.agentic.bridges.mem0_bridge import Mem0Bridge
    from src.agentic.bridges.crewai_bridge import CrewAIBridge
except ImportError:
    st.error("❌ Bridges not found. Run from project root.")

st.set_page_config(
    page_title="YBIS Control Center",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR ---
st.sidebar.title("🏭 YBIS Factory")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Dashboard", "Task Board", "Memory Bank", "Research Lab", "System Health"])

# --- HELPERS ---
def load_tasks():
    try:
        with open("Knowledge/LocalDB/tasks.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"backlog": [], "in_progress": [], "done": []}

def save_tasks(data):
    with open("Knowledge/LocalDB/tasks.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# --- PAGES ---

if page == "Dashboard":
    st.title("🚀 Factory Status")
    
    col1, col2, col3 = st.columns(3)
    tasks = load_tasks()
    
    col1.metric("Backlog Tasks", len(tasks.get("backlog", [])))
    col2.metric("In Progress", len(tasks.get("in_progress", [])))
    col3.metric("Completed", len(tasks.get("done", [])))
    
    st.markdown("### 📢 Active Signals")
    # Mock signals for now, connect to log file later
    st.info("System is operational. RTX 5090 detected.")
    
    st.markdown("### 📝 Quick Task Add")
    with st.form("quick_add"):
        new_task = st.text_input("New Task Goal")
        submitted = st.form_submit_button("Add to Backlog")
        if submitted and new_task:
            import random
            task_id = f"TASK-New-{random.randint(1000,9999)}"
            tasks["backlog"].append({
                "id": task_id,
                "goal": new_task,
                "details": "Added via Dashboard",
                "assignee": "Unassigned",
                "priority": "MEDIUM"
            })
            save_tasks(tasks)
            st.success(f"Task {task_id} added!")
            st.rerun()

elif page == "Task Board":
    st.title("📋 Kanban Board")
    tasks = load_tasks()
    
    col_backlog, col_wip, col_done = st.columns(3)
    
    with col_backlog:
        st.header("Backlog")
        for t in tasks.get("backlog", []):
            with st.expander(f"📌 {t['id']}"):
                st.write(f"**Goal:** {t['goal']}")
                st.caption(f"Priority: {t.get('priority', 'Normal')}")
    
    with col_wip:
        st.header("In Progress")
        for t in tasks.get("in_progress", []):
            with st.container(border=True):
                st.markdown(f"### 🔨 {t['id']}")
                st.write(t['goal'])
                st.progress(50) # Mock progress
    
    with col_done:
        st.header("Done")
        for t in tasks.get("done", []):
            st.success(f"✅ {t['goal']}")

elif page == "Memory Bank":
    st.title("🧠 Mem0 Neural Link")
    
    query = st.text_input("Search Memories", placeholder="e.g. 'project preferences'...")
    
    if query:
        with st.spinner("Searching neural database..."):
            try:
                mem = Mem0Bridge(user_id="default_user") # Or test_user
                # Using the bridge we fixed
                results = mem.search(query, limit=5)
                
                if results:
                    for r in results:
                        st.info(r)
                else:
                    st.warning("No memories found.")
            except Exception as e:
                st.error(f"Memory Error: {e}")
                
    st.markdown("---")
    st.subheader("Add New Memory")
    new_mem = st.text_area("Observation")
    if st.button("Store Memory"):
        if new_mem:
            try:
                mem = Mem0Bridge(user_id="default_user")
                mem.add(new_mem)
                st.success("Memory Stored.")
            except Exception as e:
                st.error(f"Store Error: {e}")

elif page == "Research Lab":
    st.title("🔬 Research Agent (CrewAI)")
    
    topic = st.text_input("Research Topic")
    
    if st.button("Deploy Agents"):
        if topic:
            with st.status("Agents are working...", expanded=True) as status:
                st.write("Initializing Crew...")
                try:
                    bridge = CrewAIBridge(model_name="qwen2.5-coder:32b")
                    st.write("Agents Deployed (Researcher + Writer)...")
                    result = bridge.create_research_crew(topic)
                    status.update(label="Research Complete!", state="complete", expanded=False)
                    st.markdown("### 📄 Report")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Crew Failure: {e}")
                    status.update(label="Mission Failed", state="error")

elif page == "System Health":
    st.title("❤️ System Health")
    
    import psutil
    import torch
    
    # --- Resources ---
    st.subheader("Resources")
    col1, col2, col3 = st.columns(3)
    
    # CPU
    cpu = psutil.cpu_percent(interval=1)
    col1.metric("CPU Usage", f"{cpu}%")
    
    # RAM
    ram = psutil.virtual_memory()
    col2.metric("RAM Usage", f"{ram.percent}%", f"{ram.used / (1024**3):.1f} GB Used")
    
    # Disk
    disk = psutil.disk_usage('/')
    col3.metric("Disk Usage", f"{disk.percent}%", f"{disk.free / (1024**3):.1f} GB Free")
    
    # --- Hardware ---
    st.subheader("Hardware Acceleration")
    col_gpu, col_torch = st.columns(2)
    
    col_torch.metric("PyTorch Version", str(torch.__version__))
    
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_mem = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        col_gpu.success(f"GPU: {gpu_name} ({gpu_mem:.1f} GB VRAM)")
    else:
        col_gpu.error("Running on CPU (Slow)")
        
    st.markdown("### Logs")
    log_file = Path("worker.out")
    if log_file.exists():
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            st.code("".join(lines[-20:])) # Show last 20 lines