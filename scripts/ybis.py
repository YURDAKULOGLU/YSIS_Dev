#!/usr/bin/env python3
"""
YBIS Unified CLI - DB-Driven Execution Tool
Implements STABILIZATION_PROTOCOL v3.0 with Frontmatter Standard

Philosophy: SQLite is the Brain, Filesystem is the Workbench
"""

import argparse
import sqlite3
import json
import sys
from pathlib import Path
from datetime import datetime
import shutil

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

DB_PATH = "Knowledge/LocalDB/tasks.db"
WORKSPACE_BASE = Path("workspaces")
WORKSPACE_ACTIVE = WORKSPACE_BASE / "active"
WORKSPACE_ARCHIVE = WORKSPACE_BASE / "archive"


class YBISCli:
    """Unified CLI for DB-driven task execution."""

    def __init__(self):
        self.db_path = DB_PATH
        self._ensure_workspaces()

    def _ensure_workspaces(self):
        """Ensure workspace directories exist."""
        WORKSPACE_ACTIVE.mkdir(parents=True, exist_ok=True)
        WORKSPACE_ARCHIVE.mkdir(parents=True, exist_ok=True)

    def _get_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)

    def _generate_frontmatter_plan(self, task_id: str, task_goal: str, target_files: list = None) -> str:
        """Generate PLAN.md with YAML frontmatter."""
        if target_files is None:
            target_files = []

        frontmatter = f"""---
id: {task_id}
type: PLAN
status: DRAFT
created_at: {datetime.now().isoformat()}
target_files: {json.dumps(target_files)}
---

# Task: {task_goal}

## Objective


## Approach


## Steps

1.
2.
3.

## Risks & Mitigations


## Success Criteria

"""
        return frontmatter

    def _generate_frontmatter_result(self, task_id: str, task_goal: str, status: str = "SUCCESS") -> str:
        """Generate RESULT.md with YAML frontmatter."""
        frontmatter = f"""---
id: {task_id}
type: RESULT
status: {status}
completed_at: {datetime.now().isoformat()}
---

# Task Result: {task_goal}

## Summary


## Changes Made


## Files Modified


## Tests Run


## Verification


## Notes

"""
        return frontmatter

    def create_task(self, goal: str, details: str = "", priority: str = "MEDIUM"):
        """Create a new task in the database."""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            import random
            task_id = f"TASK-New-{random.randint(1000, 9999)}"
            
            cursor.execute("""
                INSERT INTO tasks (id, goal, details, priority, status, assignee, created_at, updated_at)
                VALUES (?, ?, ?, ?, 'BACKLOG', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
            """, (task_id, goal, details, priority))
            
            conn.commit()
            print(f"[SUCCESS] Task created: {task_id}")
            print(f"[INFO] Goal: {goal}")
            
        except Exception as e:
            print(f"[ERROR] Failed to create task: {e}")
        finally:
            conn.close()

    def claim_task(self, task_id: str, agent_id: str):
        """
        Claim a task from BACKLOG.

        1. Update DB: status='IN_PROGRESS', assignee=agent_id
        2. Create workspace: workspaces/active/<TASK_ID>/
        3. Generate PLAN.md with frontmatter
        4. Update metadata with workspace path
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Check if task exists and is available
            cursor.execute("SELECT id, goal, status FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()

            if not row:
                print(f"[ERROR] Task {task_id} not found")
                return False

            if row[2] != "BACKLOG":
                print(f"[ERROR] Task {task_id} is already {row[2]}")
                return False

            # Claim task atomically
            cursor.execute("""
                UPDATE tasks
                SET status = 'IN_PROGRESS', assignee = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ? AND status = 'BACKLOG'
            """, (agent_id, task_id))

            if cursor.rowcount == 0:
                print(f"[ERROR] Task {task_id} was claimed by another agent")
                return False

            # Create workspace
            workspace_path = WORKSPACE_ACTIVE / task_id
            workspace_path.mkdir(parents=True, exist_ok=True)
            (workspace_path / "docs").mkdir(exist_ok=True)
            (workspace_path / "artifacts").mkdir(exist_ok=True)

            # Generate PLAN.md with frontmatter
            plan_content = self._generate_frontmatter_plan(task_id, row[1])
            (workspace_path / "docs" / "PLAN.md").write_text(plan_content, encoding='utf-8')

            # Create RUNBOOK.md
            runbook_content = f"# Task Execution Log: {task_id}\n\n## Started\n{datetime.now().isoformat()}\n\n## Log\n\n"
            (workspace_path / "docs" / "RUNBOOK.md").write_text(runbook_content, encoding='utf-8')

            # Update metadata
            metadata = {"workspace": str(workspace_path).replace("\\", "/")}
            cursor.execute("""
                UPDATE tasks SET metadata = ? WHERE id = ?
            """, (json.dumps(metadata), task_id))

            conn.commit()

            print(f"[SUCCESS] Task {task_id} claimed by {agent_id}")
            print(f"[INFO] Workspace: {workspace_path}")
            print(f"[INFO] Edit plan: {workspace_path / 'docs' / 'PLAN.md'}")

            return True

        except Exception as e:
            print(f"[ERROR] Failed to claim task: {e}")
            return False
        finally:
            conn.close()

    def complete_task(self, task_id: str, status: str = "SUCCESS"):
        """
        Complete a task.

        1. Generate RESULT.md with frontmatter
        2. Update DB: status='COMPLETED', final_status=status
        3. Archive workspace
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        try:
            # Get task info
            cursor.execute("SELECT goal, metadata FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()

            if not row:
                print(f"[ERROR] Task {task_id} not found")
                return False

            # Get workspace path
            metadata = json.loads(row[1]) if row[1] else {}
            workspace_rel = metadata.get("workspace")

            if not workspace_rel:
                print(f"[ERROR] No workspace found for task {task_id}")
                return False

            workspace_path = Path(workspace_rel)

            if not workspace_path.exists():
                print(f"[ERROR] Workspace not found: {workspace_path}")
                return False

            # Generate RESULT.md
            result_content = self._generate_frontmatter_result(task_id, row[0], status)
            (workspace_path / "artifacts" / "RESULT.md").write_text(result_content, encoding='utf-8')

            # Archive workspace
            now = datetime.now()
            archive_path = WORKSPACE_ARCHIVE / str(now.year) / f"{now.month:02d}" / task_id
            archive_path.parent.mkdir(parents=True, exist_ok=True)

            shutil.move(str(workspace_path), str(archive_path))

            # Update DB
            metadata["workspace"] = str(archive_path).replace("\\", "/")
            metadata["archived_at"] = now.isoformat()

            cursor.execute("""
                UPDATE tasks
                SET status = 'COMPLETED', final_status = ?, metadata = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (status, json.dumps(metadata), task_id))

            conn.commit()

            print(f"[SUCCESS] Task {task_id} completed with status: {status}")
            print(f"[INFO] Archived to: {archive_path}")

            return True

        except Exception as e:
            print(f"[ERROR] Failed to complete task: {e}")
            return False
        finally:
            conn.close()

    def list_tasks(self, status: str = None):
        """List tasks with optional status filter."""
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if status:
            cursor.execute("""
                SELECT id, goal, status, priority, assignee
                FROM tasks WHERE status = ?
                ORDER BY priority DESC, id
            """, (status,))
        else:
            cursor.execute("""
                SELECT id, goal, status, priority, assignee
                FROM tasks
                ORDER BY status, priority DESC, id
            """)

        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No tasks found.")
            return

        print(f"\n{'ID':<20} {'STATUS':<12} {'PRIORITY':<8} {'ASSIGNEE':<15} {'GOAL'}")
        print("-" * 100)
        for row in rows:
            print(f"{row['id']:<20} {row['status']:<12} {row['priority'] or 'N/A':<8} {row['assignee'] or 'None':<15} {row['goal'][:40]}")

    def show_workspace(self, task_id: str):
        """Show workspace info for a task."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT metadata FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        conn.close()

        if not row or not row[0]:
            print(f"[ERROR] No workspace found for task {task_id}")
            return

        metadata = json.loads(row[0])
        workspace = metadata.get("workspace")

        if workspace:
            print(f"[INFO] Workspace: {workspace}")
            workspace_path = Path(workspace)
            if workspace_path.exists():
                print("\n[FILES]")
                for f in workspace_path.rglob("*"):
                    if f.is_file():
                        print(f"  {f.relative_to(workspace_path)}")
        else:
            print(f"[ERROR] No workspace path in metadata")

    def _load_mcp_tools(self):
        try:
            from agentic import mcp_server
            return mcp_server
        except Exception as e:
            print(f"[ERROR] MCP tools unavailable: {e}")
            return None

    def send_message(self, to: str, subject: str, content: str, from_agent: str,
                     message_type: str, priority: str, reply_to: str | None,
                     tags: str | None):
        """Send a message via MCP messaging tools."""
        tools = self._load_mcp_tools()
        if not tools:
            return
        result = tools.send_message(
            to=to,
            subject=subject,
            content=content,
            from_agent=from_agent,
            message_type=message_type,
            priority=priority,
            reply_to=reply_to,
            tags=tags
        )
        print(result)

    def read_inbox(self, agent_id: str, status: str | None, limit: int):
        """Read inbox via MCP messaging tools."""
        tools = self._load_mcp_tools()
        if not tools:
            return
        result = tools.read_inbox(agent_id=agent_id, status=status, limit=limit)
        print(result)

    def ack_message(self, message_id: str, agent_id: str, action: str):
        """Acknowledge a message via MCP messaging tools."""
        tools = self._load_mcp_tools()
        if not tools:
            return
        result = tools.ack_message(message_id=message_id, agent_id=agent_id, action=action)
        print(result)

    def start_debate(self, topic: str, proposal: str, agent_id: str):
        """Start a debate by sending an MCP debate message."""
        tools = self._load_mcp_tools()
        if not tools:
            return
        result = tools.send_message(
            to="all",
            subject=topic,
            content=proposal,
            from_agent=agent_id,
            message_type="debate",
            priority="HIGH",
            reply_to=None,
            tags="debate"
        )
        print(result)

def main():
    parser = argparse.ArgumentParser(description="YBIS Unified CLI - DB-Driven Execution")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # claim command
    claim_parser = subparsers.add_parser("claim", help="Claim a task from BACKLOG")
    claim_parser.add_argument("task_id", help="Task ID to claim")
    claim_parser.add_argument("--agent", default="cli-user", help="Agent ID")

    # create command
    create_parser = subparsers.add_parser("create", help="Create a new task")
    create_parser.add_argument("goal", help="Task Goal")
    create_parser.add_argument("--details", default="", help="Task Details")
    create_parser.add_argument("--priority", default="MEDIUM", help="Priority (LOW, MEDIUM, HIGH)")

    # complete command
    complete_parser = subparsers.add_parser("complete", help="Complete a task")
    complete_parser.add_argument("task_id", help="Task ID to complete")
    complete_parser.add_argument("--status", default="SUCCESS", help="Final status")

    # list command
    list_parser = subparsers.add_parser("list", help="List tasks")
    list_parser.add_argument("--status", help="Filter by status")

    # workspace command
    ws_parser = subparsers.add_parser("workspace", help="Show workspace for task")
    ws_parser.add_argument("task_id", help="Task ID")

    # message command
    msg_parser = subparsers.add_parser("message", help="Messaging via MCP tools")
    msg_sub = msg_parser.add_subparsers(dest="msg_command", help="Message commands")

    # message send
    send_parser = msg_sub.add_parser("send", help="Send a message")
    send_parser.add_argument("--to", required=True, help="Recipient")
    send_parser.add_argument("--subject", required=True, help="Subject")
    send_parser.add_argument("--content", required=True, help="Content")
    send_parser.add_argument("--from", dest="from_agent", default="cli-user", help="Sender")
    send_parser.add_argument("--type", dest="message_type", default="direct", help="Type")
    send_parser.add_argument("--priority", default="NORMAL", help="Priority")
    send_parser.add_argument("--reply-to", help="Reply to ID")
    send_parser.add_argument("--tags", help="Tags")

    # message read
    read_parser = msg_sub.add_parser("read", help="Read inbox")
    read_parser.add_argument("--agent", required=True, help="Agent ID")
    read_parser.add_argument("--status", help="Filter status")
    read_parser.add_argument("--limit", type=int, default=50, help="Limit")

    # message ack
    ack_parser = msg_sub.add_parser("ack", help="Acknowledge message")
    ack_parser.add_argument("--id", required=True, help="Message ID")
    ack_parser.add_argument("--agent", required=True, help="Agent ID")
    ack_parser.add_argument("--action", default="noted", help="Action")

    # debate command
    debate_parser = subparsers.add_parser("debate", help="Debate management")
    debate_sub = debate_parser.add_subparsers(dest="debate_cmd", help="Debate commands")
    
    start_db = debate_sub.add_parser("start", help="Start a new debate")
    start_db.add_argument("--topic", required=True, help="Debate topic")
    start_db.add_argument("--proposal", required=True, help="Debate proposal content")
    start_db.add_argument("--agent", default="cli-user", help="Agent starting the debate")

    args = parser.parse_args()

    cli = YBISCli()

    if args.command == "create":
        cli.create_task(args.goal, args.details, args.priority)
    elif args.command == "claim":
        cli.claim_task(args.task_id, args.agent)
    elif args.command == "complete":
        cli.complete_task(args.task_id, args.status)
    elif args.command == "list":
        cli.list_tasks(args.status)
    elif args.command == "workspace":
        cli.show_workspace(args.task_id)
    elif args.command == "message":
        if args.msg_command == "send":
            cli.send_message(
                to=args.to,
                subject=args.subject,
                content=args.content,
                from_agent=args.from_agent,
                message_type=args.message_type,
                priority=args.priority,
                reply_to=args.reply_to,
                tags=args.tags
            )
        elif args.msg_command == "read":
            cli.read_inbox(
                agent_id=args.agent,
                status=args.status,
                limit=args.limit
            )
        elif args.msg_command == "ack":
            cli.ack_message(
                message_id=args.id,
                agent_id=args.agent,
                action=args.action
            )
    elif args.command == "debate":
        if args.debate_cmd == "start":
            # UPDATED: Use MCP tool for debate start
            cli.send_message(
                to="broadcast",
                subject=f"New Debate: {args.topic}",
                content=f"Debate started.\nProposal:\n{args.proposal}",
                from_agent=args.agent,
                message_type="debate",
                priority="HIGH",
                reply_to=None,
                tags="debate"
            )
            print(f"[SUCCESS] Debate started via MCP Messaging")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
