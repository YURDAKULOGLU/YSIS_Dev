"""
YBIS CONTROL CENTER (Streamlit)
The central cockpit for the Autonomous Factory.
"""

import streamlit as st
import os
import sys
import pandas as pd
from pathlib import Path
import sqlite3
import json
from datetime import datetime

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
page = st.sidebar.radio("Navigation", ["Dashboard", "Task Board", "Messaging", "Memory Bank", "Research Lab", "System Health"])

# --- HELPERS ---
DB_PATH = Path("Knowledge/LocalDB/tasks.db")
MESSAGES_DIR = Path("Knowledge/Messages")

def _load_mcp_tools():
    try:
        from agentic import mcp_server
        return mcp_server
    except Exception:
        return None

def _parse_metadata(raw):
    if raw is None:
        return {}
    if isinstance(raw, dict):
        return raw
    try:
        return json.loads(raw)
    except Exception:
        return {}

def _parse_frontmatter(content: str):
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    _, fm_text, body = parts
    fm = {}
    for line in fm_text.strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fm[key.strip()] = value.strip()
    return fm, body.strip()

def _read_text(path: Path):
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8", errors="replace")

def _read_json(path: Path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None

def load_tasks_db():
    if not DB_PATH.exists():
        return {"backlog": [], "in_progress": [], "done": []}

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, goal, details, status, priority, assignee, final_status, metadata FROM tasks")
    rows = cursor.fetchall()
    conn.close()

    backlog, in_progress, done = [], [], []
    for row in rows:
        task = dict(row)
        task["metadata"] = _parse_metadata(task.get("metadata"))
        status = (task.get("status") or "").upper()
        if status in ("IN_PROGRESS", "IN PROGRESS"):
            in_progress.append(task)
        elif status in ("DONE", "COMPLETED", "FAILED"):
            done.append(task)
        else:
            backlog.append(task)

    return {"backlog": backlog, "in_progress": in_progress, "done": done}

def add_task_db(goal: str, details: str = "Added via Dashboard"):
    if not DB_PATH.exists():
        return False

    task_id = f"TASK-New-{int(datetime.now().timestamp())}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO tasks (id, goal, details, status, priority, assignee, final_status, metadata, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (task_id, goal, details, "BACKLOG", "MEDIUM", "Unassigned", None, "{}", datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return task_id

# --- PAGES ---

if page == "Dashboard":
    st.title("🚀 Factory Status")
    
    col1, col2, col3 = st.columns(3)
    tasks = load_tasks_db()
    
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
            task_id = add_task_db(new_task)
            if task_id:
                st.success(f"Task {task_id} added!")
            else:
                st.error("Failed to add task (tasks.db missing).")
            st.rerun()

elif page == "Task Board":
    st.title("📋 Kanban Board")
    tasks = load_tasks_db()
    
    col_backlog, col_wip, col_done = st.columns(3)
    
    with col_backlog:
        st.header("Backlog")
        for t in tasks.get("backlog", []):
            with st.expander(f"📌 {t['id']}"):
                st.write(f"**Goal:** {t['goal']}")
                st.caption(f"Priority: {t.get('priority', 'Normal')}")
                if t.get("details"):
                    st.write(t["details"])
    
    with col_wip:
        st.header("In Progress")
        for t in tasks.get("in_progress", []):
            with st.container(border=True):
                st.markdown(f"### 🔨 {t['id']}")
                st.write(t['goal'])
                metadata = t.get("metadata") or {}
                workspace = metadata.get("workspace")
                if workspace:
                    st.caption(f"Workspace: {workspace}")
                st.progress(50)
    
    with col_done:
        st.header("Done")
        for t in tasks.get("done", []):
            st.success(f"✅ {t['goal']}")
            metadata = t.get("metadata") or {}
            workspace = metadata.get("workspace")
            if workspace:
                workspace_path = Path(workspace)
                plan_path = workspace_path / "docs" / "PLAN.md"
                result_path = workspace_path / "artifacts" / "RESULT.md"

                plan_text = _read_text(plan_path)
                result_text = _read_text(result_path)

                if plan_text:
                    fm, body = _parse_frontmatter(plan_text)
                    st.markdown("**PLAN.md**")
                    if fm:
                        st.code(json.dumps(fm, indent=2))
                    st.markdown(body)

                if result_text:
                    fm, body = _parse_frontmatter(result_text)
                    st.markdown("**RESULT.md**")
                    if fm:
                        st.code(json.dumps(fm, indent=2))
                    st.markdown(body)

elif page == "Messaging":
    st.title("Messaging")
    tools = _load_mcp_tools()

    if not tools:
        st.error("MCP tools unavailable. Run from project root and ensure mcp_server is importable.")
    else:
        if "inbox_messages" not in st.session_state:
            st.session_state["inbox_messages"] = []

        with st.container(border=True):
            st.markdown("### MCP Inbox")
            agent_id = st.text_input("Agent ID", value="dashboard")
            status_filter = st.selectbox("Status Filter", ["", "unread", "read", "archived"])
            limit = st.number_input("Limit", min_value=1, max_value=200, value=50, step=1)

            if st.button("Refresh Inbox"):
                raw = tools.read_inbox(agent_id=agent_id, status=status_filter or None, limit=int(limit))
                try:
                    payload = json.loads(raw)
                    messages = payload.get("messages", [])
                    st.session_state["inbox_messages"] = messages
                except Exception:
                    messages = []
                    st.error("Failed to parse inbox response.")

            messages = st.session_state.get("inbox_messages", [])
            if messages:
                st.dataframe(pd.DataFrame(messages))
            else:
                st.info("No messages.")

        with st.container(border=True):
            st.markdown("### Send Message")
            to_agent = st.text_input("To", value="all")
            subject = st.text_input("Subject")
            content = st.text_area("Content", height=160)
            msg_type = st.selectbox("Type", ["direct", "broadcast", "debate", "task_assignment"])
            priority = st.selectbox("Priority", ["NORMAL", "HIGH", "CRITICAL", "LOW"])
            from_agent = st.text_input("From", value="dashboard")
            reply_to = st.text_input("Reply To (message id)", value="")
            tags = st.text_input("Tags (comma-separated)", value="debate" if msg_type == "debate" else "")

            if st.button("Send"):
                result = tools.send_message(
                    to=to_agent,
                    subject=subject,
                    content=content,
                    from_agent=from_agent,
                    message_type=msg_type,
                    priority=priority,
                    reply_to=reply_to or None,
                    tags=tags or None
                )
                st.write(result)

        with st.container(border=True):
            st.markdown("### Start Debate")
            debate_topic = st.text_input("Debate Topic", value="")
            debate_proposal = st.text_area("Proposal", height=200)
            debate_agent = st.text_input("Agent", value="dashboard")
            if st.button("Start Debate"):
                result = tools.send_message(
                    to="all",
                    subject=debate_topic,
                    content=debate_proposal,
                    from_agent=debate_agent,
                    message_type="debate",
                    priority="HIGH",
                    reply_to=None,
                    tags="debate"
                )
                st.write(result)

        with st.container(border=True):
            st.markdown("### Reply to Debate")
            reply_debate_id = st.text_input("Debate ID", value="")
            reply_content = st.text_area("Reply Content", height=160)
            reply_agent = st.text_input("Reply From", value="dashboard")
            if st.button("Send Debate Reply"):
                result = tools.send_message(
                    to="all",
                    subject=reply_debate_id,
                    content=reply_content,
                    from_agent=reply_agent,
                    message_type="debate",
                    priority="NORMAL",
                    reply_to=None,
                    tags="debate"
                )
                st.write(result)

        with st.container(border=True):
            st.markdown("### Acknowledge Message")
            inbox_ids = [m.get("id") for m in st.session_state.get("inbox_messages", []) if m.get("id")]
            ack_id = st.selectbox("Message ID", options=[""] + inbox_ids)
            ack_agent = st.text_input("Agent", value="dashboard")
            ack_action = st.selectbox("Action", ["noted", "will_do", "done", "rejected"])
            if st.button("Acknowledge"):
                if not ack_id:
                    st.error("Select a message to acknowledge.")
                else:
                    result = tools.ack_message(message_id=ack_id, agent_id=ack_agent, action=ack_action)
                    st.write(result)

    with st.expander("Legacy Archive (Read-Only)"):
        if not MESSAGES_DIR.exists():
            st.info("No message archive found.")
        else:
            for box in ["inbox", "outbox", "debates"]:
                box_path = MESSAGES_DIR / box
                if not box_path.exists():
                    continue
                st.markdown(f"**{box}**")
                files = sorted(box_path.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)[:20]
                for path in files:
                    with st.expander(path.name):
                        data = _read_json(path)
                        if data is None:
                            st.write(_read_text(path) or "")
                        else:
                            st.code(json.dumps(data, indent=2))

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
