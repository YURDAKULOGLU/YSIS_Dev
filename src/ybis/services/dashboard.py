"""
Streamlit Command Center - Web UI for YBIS Factory.

Provides visual dashboard for tasks, runs, workers, and control.
"""

import json
import time

import streamlit as st

from ..constants import PROJECT_ROOT
from ..control_plane import ControlPlaneDB

# Page configuration
st.set_page_config(page_title="YBIS Command Center", layout="wide")


@st.cache_data(ttl=2)
def get_db_data():
    """Get database data (cached for 2 seconds)."""
    import asyncio

    db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
    db = ControlPlaneDB(db_path)

    async def fetch_data():
        await db.initialize()
        tasks = await db.get_pending_tasks()
        blocked = await db.get_blocked_tasks()
        workers = await db.get_workers()
        runs = await db.get_recent_runs(limit=20)
        return tasks, blocked, workers, runs

    return asyncio.run(fetch_data())


def page_overview():
    """Overview page with metrics and task board."""
    st.header("📊 Factory Overview")

    # Fetch data
    try:
        tasks, blocked, workers, runs = get_db_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tasks", len(tasks) + len(blocked))
    with col2:
        active_workers = len([w for w in workers if w["status"] == "BUSY"])
        st.metric("Active Workers", active_workers)
    with col3:
        completed_runs = len([r for r in runs if r.status == "completed"])
        total_runs = len(runs)
        success_rate = (completed_runs / total_runs * 100) if total_runs > 0 else 0
        st.metric("Success Rate", f"{success_rate:.1f}%")
    with col4:
        st.metric("Blocked Tasks", len(blocked))

    st.divider()

    # Task Board (Agile-like columns)
    st.subheader("📋 Task Board")
    col_todo, col_busy, col_blocked, col_done = st.columns(4)

    with col_todo:
        st.markdown("### TODO")
        for task in tasks[:10]:
            with st.container():
                st.markdown(f"**{task.title[:30]}**")
                st.caption(f"{task.task_id}")
                st.text(f"{task.objective[:50]}...")

    with col_busy:
        st.markdown("### BUSY")
        busy_tasks = [w for w in workers if w["status"] == "BUSY"]
        for worker in busy_tasks:
            with st.container():
                st.markdown(f"**{worker['current_task'][:30]}**")
                st.caption(f"Worker: {worker['worker_id']}")

    with col_blocked:
        st.markdown("### BLOCKED")
        for task in blocked[:10]:
            with st.container():
                st.markdown(f"**{task.title[:30]}**")
                st.caption(f"{task.task_id}")
                st.text(f"{task.objective[:50]}...")

    with col_done:
        st.markdown("### DONE")
        done_runs = [r for r in runs if r.status == "completed"][:10]
        for run in done_runs:
            with st.container():
                st.markdown(f"**{run.task_id[:30]}**")
                st.caption(f"Run: {run.run_id}")


def page_run_explorer():
    """Run Explorer page - drill down into specific runs."""
    st.header("🔍 Run Explorer")

    # Fetch runs
    try:
        _, _, _, runs = get_db_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return

    # Run selector
    run_options = {f"{r.task_id} / {r.run_id}": r for r in runs}
    selected = st.selectbox("Select Run", list(run_options.keys()))

    if not selected:
        return

    run = run_options[selected]

    # Run details
    st.subheader("Run Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(f"**Task ID:** {run.task_id}")
        st.write(f"**Run ID:** {run.run_id}")
    with col2:
        st.write(f"**Status:** {run.status}")
        st.write(f"**Workflow:** {run.workflow or 'build'}")
    with col3:
        st.write(f"**Started:** {run.started_at}")
        st.write(f"**Completed:** {run.completed_at or 'N/A'}")

    st.divider()

    # Events Timeline with real-time polling
    st.subheader("📜 Events Timeline")
    
    # Auto-refresh toggle (only for running tasks)
    auto_refresh = st.checkbox("Auto-refresh (2s)", value=(run.status == "running"))
    
    run_path = PROJECT_ROOT / "workspaces" / run.task_id / "runs" / run.run_id
    events_path = run_path / "journal" / "events.jsonl"

    # Create container for events (for auto-scroll)
    events_container = st.container()
    
    if events_path.exists():
        events = []
        last_line_count = st.session_state.get(f"event_count_{run.run_id}", 0)
        
        with open(events_path, encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                if line.strip():
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        
        # Update session state
        current_line_count = len(lines)
        st.session_state[f"event_count_{run.run_id}"] = current_line_count
        
        # Auto-refresh if enabled and new events detected
        if auto_refresh and current_line_count > last_line_count:
            time.sleep(0.1)  # Small delay for smooth scrolling
            st.rerun()
        
        with events_container:
            # Show trace_id if available
            if events:
                trace_id = events[0].get("trace_id")
                if trace_id:
                    st.caption(f"Trace ID: `{trace_id}`")
            
            # Display events in reverse order (newest first) with auto-scroll
            for event in reversed(events):
                event_type = event.get("event_type", "UNKNOWN")
                timestamp = event.get("timestamp", "")[:19] if event.get("timestamp") else ""
                trace_id = event.get("trace_id", "")
                
                with st.expander(f"🔹 {event_type} - {timestamp}", expanded=(event == events[-1] and auto_refresh)):
                    if trace_id:
                        st.caption(f"Trace ID: `{trace_id}`")
                    st.json(event.get("payload", {}))
            
            # Auto-scroll JavaScript (runs on page load/refresh)
            if auto_refresh:
                st.markdown(
                    """
                    <script>
                        setTimeout(function() {
                            window.scrollTo(0, document.body.scrollHeight);
                        }, 100);
                    </script>
                    """,
                    unsafe_allow_html=True,
                )
    else:
        st.info("No events found for this run.")

    st.divider()

    # Diff Viewer (if patch.diff exists)
    patch_path = run_path / "artifacts" / "patch.diff"
    if patch_path.exists():
        st.divider()
        st.subheader("📝 Code Changes (Diff)")
        try:
            diff_content = patch_path.read_text(encoding="utf-8")
            st.code(diff_content, language="diff")
        except Exception as e:
            st.error(f"Error reading patch.diff: {e}")
    
    st.divider()

    # Artifacts
    st.subheader("📦 Artifacts")
    artifacts_dir = run_path / "artifacts"
    if artifacts_dir.exists():
        artifacts = list(artifacts_dir.glob("*.json"))

        # Check for debate report - show it prominently
        debate_path = artifacts_dir / "debate_report.json"
        if debate_path.exists():
            st.divider()
            st.subheader("💬 Council Debate")
            try:
                debate_data = json.loads(debate_path.read_text())
                consensus = debate_data.get("consensus", "UNKNOWN")
                consensus_color = {
                    "OVERRIDE_BLOCK": "green",
                    "CONFIRM_BLOCK": "red",
                    "REQUIRE_APPROVAL": "yellow",
                }.get(consensus, "gray")

                st.markdown(f"**Consensus:** :{consensus_color}[{consensus}]")

                # Show arguments in chat-like interface
                st.markdown("### Debate Arguments")
                arguments = debate_data.get("arguments", [])
                for arg in arguments:
                    persona = arg.get("persona", "Unknown")
                    role = arg.get("role", "")
                    argument_text = arg.get("argument", "")

                    with st.chat_message(name=persona, avatar="👤"):
                        st.caption(f"{role} - Round {arg.get('round', 1)}")
                        st.write(argument_text)

                # Show summary
                summary = debate_data.get("summary", "")
                if summary:
                    st.markdown("### Summary")
                    st.info(summary)

            except Exception as e:
                st.error(f"Error loading debate report: {e}")

        # Other artifacts
        other_artifacts = [a for a in artifacts if a.name != "debate_report.json"]
        for artifact_path in other_artifacts:
            with st.expander(artifact_path.name):
                try:
                    content = json.loads(artifact_path.read_text())
                    st.json(content)
                except Exception:
                    st.text(artifact_path.read_text())
    else:
        st.info("No artifacts found for this run.")


def page_control():
    """Control page - manual task creation and approvals."""
    st.header("🎮 Control Center")

    # Create Task
    st.subheader("➕ Create Task")
    with st.form("create_task"):
        title = st.text_input("Title")
        objective = st.text_area("Objective")
        priority = st.selectbox("Priority", ["LOW", "MEDIUM", "HIGH"])

        if st.form_submit_button("Create Task"):
            if title and objective:
                import asyncio
                import uuid

                from ..contracts import Task
                from ..control_plane import ControlPlaneDB

                db_path = PROJECT_ROOT / "platform_data" / "control_plane.db"
                db = ControlPlaneDB(db_path)

                async def create():
                    await db.initialize()
                    task_id = f"T-{uuid.uuid4().hex[:8]}"
                    task = Task(
                        task_id=task_id,
                        title=title,
                        objective=objective,
                        status="pending",
                        priority=priority,
                    )
                    await db.register_task(task)
                    return task_id

                task_id = asyncio.run(create())
                st.success(f"Task created: {task_id}")
            else:
                st.error("Please fill in title and objective")

    st.divider()

    # Approve Blocked Task
    st.subheader("✅ Approve Blocked Task")
    try:
        _, blocked, _, _ = get_db_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return

    if blocked:
        blocked_options = {f"{t.task_id}: {t.title}": t for t in blocked}
        selected = st.selectbox("Select Blocked Task", list(blocked_options.keys()))

        if selected:
            task = blocked_options[selected]

            with st.form("approve_task"):
                approver = st.text_input("Approver", value="dashboard-user")
                reason = st.text_area("Reason")

                if st.form_submit_button("Approve"):
                    if reason:
                        # Find latest run for this task
                        runs_dir = PROJECT_ROOT / "workspaces" / task.task_id / "runs"
                        if runs_dir.exists():
                            run_dirs = list(runs_dir.glob("R-*"))
                            if run_dirs:
                                latest_run = max(run_dirs, key=lambda p: p.stat().st_mtime)
                                run_id = latest_run.name

                                approval_path = latest_run / "artifacts" / "approval.json"
                                approval_data = {
                                    "task_id": task.task_id,
                                    "run_id": run_id,
                                    "approver": approver,
                                    "reason": reason,
                                    "timestamp": None,  # Would use datetime
                                }

                                approval_path.parent.mkdir(parents=True, exist_ok=True)
                                approval_path.write_text(json.dumps(approval_data, indent=2), encoding="utf-8")

                                st.success(f"Approval written for task {task.task_id}")
                            else:
                                st.error("No runs found for this task")
                        else:
                            st.error("No workspace found for this task")
                    else:
                        st.error("Please provide a reason")
    else:
        st.info("No blocked tasks to approve")


def page_performance():
    """Performance page - metrics and cost tracking."""
    st.header("📈 Performance & Cost Metrics")

    # Fetch data
    try:
        _, _, workers, runs = get_db_data()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return

    # Calculate metrics from runs
    performance_data = []
    for run in runs:
        if run.performance_metrics:
            metrics = run.performance_metrics
            performance_data.append(
                {
                    "run_id": run.run_id,
                    "task_id": run.task_id,
                    "status": run.status,
                    "latency_ms": metrics.latency_ms,
                    "token_count": metrics.token_count,
                    "gpu_load": metrics.gpu_load,
                    "model_type": metrics.model_type,
                    "success_rate": metrics.success_rate,
                }
            )

    if not performance_data:
        st.info("No performance metrics available yet. Metrics are collected during run execution.")
        return

    # Aggregate metrics
    import pandas as pd

    df = pd.DataFrame(performance_data)

    # Overall metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        avg_latency = df["latency_ms"].mean()
        st.metric("Avg Response Time (Ollama)", f"{avg_latency:.1f} ms")
    with col2:
        total_tokens = df["token_count"].sum()
        st.metric("Total Tokens Consumed", f"{total_tokens:,}")
    with col3:
        avg_gpu = df["gpu_load"].mean()
        st.metric("Avg GPU Load", f"{avg_gpu:.1f}%")
    with col4:
        overall_success = df["success_rate"].mean() * 100
        st.metric("Overall Success Rate", f"{overall_success:.1f}%")

    st.divider()

    # Model comparison
    st.subheader("📊 Success Rate by Model Type")
    if "model_type" in df.columns:
        model_stats = df.groupby("model_type").agg(
            {
                "success_rate": "mean",
                "latency_ms": "mean",
                "token_count": "sum",
            }
        ).reset_index()

        model_stats["success_rate"] = model_stats["success_rate"] * 100
        st.dataframe(model_stats, use_container_width=True)

    st.divider()

    # Token consumption by worker
    st.subheader("💰 Token Consumption by Worker")
    # This would require worker_id in performance metrics
    # For now, show per-run token consumption
    token_chart = df[["run_id", "token_count", "model_type"]].head(20)
    st.bar_chart(token_chart.set_index("run_id")["token_count"])

    st.divider()

    # Performance trends
    st.subheader("📈 Performance Trends")
    if len(df) > 1:
        # Show latency trend
        latency_trend = df[["run_id", "latency_ms"]].head(20)
        st.line_chart(latency_trend.set_index("run_id")["latency_ms"])


def main():
    """Main dashboard application."""
    st.sidebar.title("YBIS Command Center")
    page = st.sidebar.selectbox("Navigation", ["Overview", "Run Explorer", "Control", "Performance"])

    if page == "Overview":
        page_overview()
    elif page == "Run Explorer":
        page_run_explorer()
    elif page == "Control":
        page_control()
    elif page == "Performance":
        page_performance()


if __name__ == "__main__":
    main()

