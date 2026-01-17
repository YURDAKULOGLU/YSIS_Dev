#!/usr/bin/env python3
"""
Create improvement tasks based on user's priority list.

Priority order:
1. Auto-Test Gate (High Impact, Low Effort)
2. Feedback Loop Enhancement (High Impact, Medium Effort) - Already exists, enhance
3. Metrics Dashboard (Medium Impact, Low Effort)
4. Memory/RAG (High Impact, High Effort)
5. Rollback (Medium Impact, Medium Effort)
6. Dependencies (Low Impact, Medium Effort)
"""

import sys
import asyncio
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def create_tasks():
    """Create improvement tasks."""
    print("=" * 60)
    print("Creating YBIS Improvement Tasks")
    print("=" * 60)
    print()
    
    server_params = StdioServerParameters(
        command="python",
        args=["scripts/ybis_mcp_server.py"],
        env=None,
    )
    
    tasks = []
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            # Task 1: Auto-Test Gate (HIGH priority)
            print("Creating Task 1: Auto-Test Gate...")
            result = await session.call_tool(
                "task_create",
                arguments={
                    "title": "Feature: Auto-Test Gate (Pre-Commit Hook)",
                    "objective": """Implement automatic test execution gate before code changes are applied.

Requirements:
1. Create .pre-commit-config.yaml with:
   - pytest runner (run tests before commit)
   - ruff linter (check code quality)
   - mypy type checker (optional, if type hints exist)
   
2. Integrate with execute_node:
   - Before applying code changes, run tests in sandbox
   - If tests fail, block execution and feed errors to repair_node
   - Only apply changes if all tests pass
   
3. Add test gate to gate_node:
   - Check test coverage threshold (e.g., 80%)
   - Block if coverage drops below threshold
   
4. Create pre-commit hook installer:
   - Script to install pre-commit hooks
   - Document in README

Success Criteria:
- Every code change automatically tested before apply
- Pre-commit hooks prevent bad commits
- Test failures block execution automatically
- Coverage threshold enforced""",
                    "priority": "HIGH",
                }
            )
            task_data = eval(result.content[0].text)
            tasks.append(("T-1", task_data["task_id"]))
            print(f"  ✅ Created: {task_data['task_id']}")
            print()
            
            # Task 2: Feedback Loop Enhancement (HIGH priority)
            print("Creating Task 2: Feedback Loop Enhancement...")
            result = await session.call_tool(
                "task_create",
                arguments={
                    "title": "Enhancement: Cross-Task Feedback Loop",
                    "objective": """Enhance existing feedback loop to work across tasks, not just within a single task.

Current State:
- ✅ Feedback loop exists within a task (verifier → spec/plan)
- ❌ No feedback between different tasks
- ❌ No learning from previous task successes/failures

Requirements:
1. Task Result Analysis:
   - After task completion, analyze results
   - Extract patterns: "This approach worked", "This failed"
   - Store in memory/RAG system
   
2. Next Task Input:
   - When creating new task, search memory for similar tasks
   - Include successful patterns in task objective
   - Include failure patterns as warnings
   
3. Memory Integration:
   - Store task outcomes in persistent memory
   - Query memory before spec/plan generation
   - Include relevant learnings in prompts
   
4. Pattern Extraction:
   - Identify successful code patterns
   - Identify common failure modes
   - Build knowledge base of "what works"

Success Criteria:
- New tasks learn from previous task outcomes
- Successful patterns are reused automatically
- Failure patterns are avoided
- Cross-task knowledge sharing works""",
                    "priority": "HIGH",
                }
            )
            task_data = eval(result.content[0].text)
            tasks.append(("T-2", task_data["task_id"]))
            print(f"  ✅ Created: {task_data['task_id']}")
            print()
            
            # Task 3: Metrics Dashboard (MEDIUM priority)
            print("Creating Task 3: Metrics Dashboard...")
            result = await session.call_tool(
                "task_create",
                arguments={
                    "title": "Feature: Real-Time Metrics Dashboard",
                    "objective": """Create a real-time metrics dashboard for YBIS execution.

Requirements:
1. Structured Logging Enhancement:
   - Add step-level timing (which step, how long)
   - Add failure point tracking (where did it fail)
   - Add resource usage (memory, CPU)
   
2. Metrics Collection:
   - Task success rate
   - Average execution time per step
   - Failure rate by step type
   - Test pass rate
   - Code coverage trends
   
3. Dashboard UI (Simple):
   - Web-based dashboard (Flask/FastAPI + HTML)
   - Real-time updates via WebSocket or polling
   - Show active tasks, recent runs, metrics
   
4. Prometheus Integration:
   - Export metrics to Prometheus
   - Grafana dashboard (optional)
   
Success Criteria:
- Can see which step failed and why
- Can see execution time per step
- Can see task success/failure trends
- Real-time monitoring of active tasks""",
                    "priority": "MEDIUM",
                }
            )
            task_data = eval(result.content[0].text)
            tasks.append(("T-3", task_data["task_id"]))
            print(f"  ✅ Created: {task_data['task_id']}")
            print()
            
            # Task 4: Memory/RAG Implementation (HIGH priority, HIGH effort)
            print("Creating Task 4: Memory/RAG Implementation...")
            result = await session.call_tool(
                "task_create",
                arguments={
                    "title": "Feature: Persistent Memory/RAG System",
                    "objective": """Implement full Memory/RAG system for YBIS.

Current State:
- ✅ Memory API exists (add_to_memory, search_memory)
- ❌ MemoryStoreAdapter not implemented
- ❌ No vector store integration

Requirements:
1. MemoryStoreAdapter Implementation:
   - Implement MemoryStoreAdapter interface
   - Support ChromaDB, FAISS, or similar
   - Store task outcomes, patterns, learnings
   
2. RAG Integration:
   - Index codebase documentation
   - Index successful task patterns
   - Index failure patterns
   - Semantic search for relevant context
   
3. Memory Persistence:
   - Persistent storage (not in-memory)
   - Backup/restore mechanism
   - Memory pruning (old memories)
   
4. Integration with Workflow:
   - spec_node queries memory for similar tasks
   - plan_node uses memory for pattern matching
   - execute_node stores outcomes in memory
   
Success Criteria:
- Memory persists across sessions
- RAG search returns relevant results
- Task patterns are stored and retrieved
- Memory improves task quality over time""",
                    "priority": "HIGH",
                }
            )
            task_data = eval(result.content[0].text)
            tasks.append(("T-4", task_data["task_id"]))
            print(f"  ✅ Created: {task_data['task_id']}")
            print()
            
            # Task 5: Rollback Mechanism (MEDIUM priority)
            print("Creating Task 5: Rollback Mechanism...")
            result = await session.call_tool(
                "task_create",
                arguments={
                    "title": "Feature: Automatic Rollback Mechanism",
                    "objective": """Implement automatic rollback for failed task executions.

Current State:
- ❌ No git worktree isolation
- ❌ No automatic rollback
- ❌ Manual recovery required

Requirements:
1. Git Worktree Integration:
   - Create git worktree for each run
   - Isolate changes in worktree
   - Only merge if verification passes
   
2. Automatic Rollback:
   - If tests fail → revert worktree
   - If gate blocks → revert worktree
   - If execution fails → revert worktree
   - Keep rollback plan in artifacts
   
3. Worktree Manager:
   - init_git_worktree(task_id, run_id)
   - cleanup_worktree(worktree_path)
   - merge_worktree(worktree_path) - only if success
   
4. Integration with execute_node:
   - Execute in worktree, not main codebase
   - Test in worktree
   - Merge only after all checks pass
   
Success Criteria:
- Every run isolated in git worktree
- Automatic rollback on failure
- Main codebase never corrupted
- Rollback plan available in artifacts""",
                    "priority": "MEDIUM",
                }
            )
            task_data = eval(result.content[0].text)
            tasks.append(("T-5", task_data["task_id"]))
            print(f"  ✅ Created: {task_data['task_id']}")
            print()
            
            # Task 6: Task Dependencies (LOW priority)
            print("Creating Task 6: Task Dependencies...")
            result = await session.call_tool(
                "task_create",
                arguments={
                    "title": "Feature: Task Dependency Tracking",
                    "objective": """Implement task dependency system for sequential execution.

Current State:
- ❌ No task dependencies in schema
- ❌ Tasks run independently
- ❌ No automatic task chaining

Requirements:
1. Schema Enhancement:
   - Add `depends_on` column to tasks table
   - Support multiple dependencies (comma-separated)
   - Add `blocked_by` computed field
   
2. Dependency Resolution:
   - Check if dependencies are complete
   - Block task execution if dependencies pending
   - Auto-start task when dependencies complete
   
3. Dependency Graph:
   - Visualize task dependencies
   - Detect circular dependencies
   - Topological sort for execution order
   
4. Integration with Worker:
   - Worker checks dependencies before claiming task
   - Auto-queue dependent tasks when parent completes
   
Success Criteria:
- Tasks can depend on other tasks
- Dependent tasks auto-start when parent completes
- Circular dependencies detected
- Dependency graph visualized""",
                    "priority": "LOW",
                }
            )
            task_data = eval(result.content[0].text)
            tasks.append(("T-6", task_data["task_id"]))
            print(f"  ✅ Created: {task_data['task_id']}")
            print()
            
            # Summary
            print("=" * 60)
            print("✅ All Improvement Tasks Created!")
            print("=" * 60)
            print()
            print("Created tasks:")
            for label, task_id in tasks:
                print(f"  - {task_id}: {label}")
            print()
            print("To run tasks:")
            for label, task_id in tasks:
                print(f"  python scripts/ybis_run.py {task_id} --workflow self_develop")
            print("=" * 60)


if __name__ == "__main__":
    try:
        asyncio.run(create_tasks())
    except KeyboardInterrupt:
        print("\n⚠️  Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

