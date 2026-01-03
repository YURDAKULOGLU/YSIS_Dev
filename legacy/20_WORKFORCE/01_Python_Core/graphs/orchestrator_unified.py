import os
import sys
import asyncio
import operator
from typing import TypedDict, Annotated, List, Dict, Any, Union
from langgraph.graph import StateGraph, END

# Import MCP Client
# Import MCP Client
from mcp.client.session import ClientSession
from mcp.client.sse import sse_client

# Setup paths
sys.path.insert(0, os.getcwd())
# Ensure .YBIS_Dev is explicitly in path for Agentic package
if os.path.exists(".YBIS_Dev"):
    sys.path.insert(0, os.path.join(os.getcwd(), ".YBIS_Dev"))

# Import Protocols & Plugins
from Agentic.Core.protocols import Plan, CodeResult
from Agentic.Core.plugins.aider_executor import AiderExecutor
from Agentic.Core.plugins.sentinel import SentinelVerifier
# from Agentic.Core.plugins.task_board_manager import TaskBoardManager # REMOVED: Using MCP
import yaml
import re
from pathlib import Path

# Import Tools
from Agentic.Tools.local_rag import local_rag

# --- CONFIG ---
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/sse")

# --- STATE ---
# --- STATE ---
# REFACTORED: Imported from Core.state_unified
from Agentic.Core.state_unified import AgentState

# --- HELPERS ---
async def call_mcp_tool(tool_name: str, arguments: Dict[str, Any] = {}) -> Any:
    """Helper to call MCP tool via SSE."""
    if not ClientSession:
        return None

    try:
        async with sse_client(MCP_SERVER_URL) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                # Parse result - usually it's a list of content
                # FastMCP returns text usually?
                # We assume result is what we need or we parse it.
                # Standard mcp result has .content list
                if hasattr(result, 'content') and isinstance(result.content, list):
                    # Extract text from content list
                    texts = [c.text for c in result.content if hasattr(c, 'text')]
                    return "\n".join(texts)
                return result

                # Check for simple string return from YBIS Server
                if hasattr(result, 'content') and result.content:
                     # Access the first text content
                     return result.content[0].text
                return str(result)
    except Exception as e:
        print(f"[WARN] MCP Call Failed ({tool_name}): {e}")
        return None

# --- NODES ---

async def node_planner(state: AgentState):
    """
    Role: Strategist
    Action: Analyze task (from State or Board) and create a plan.
    """
    task_data = state.get('task_data')
    task_desc = state.get('task')

    # If no task loaded yet, try to fetch from Board via MCP
    if not task_desc:
        print(f"\n[PLANNER] Calling MCP Brain to get task from {MCP_SERVER_URL}...")

        # Parse logic for "get_next_task"
        # The tool returns string like "ID: Description"
        response = await call_mcp_tool("get_next_task")

        if not response or "No IN PROGRESS tasks" in response:
             print("   No tasks in 'IN PROGRESS'. Checking 'NEW'...")
             raise ValueError("CRITICAL: No Task Found. Orchestrator cannot proceed with 'None'.")

        # Parse "TASK-ID: Description"
        try:
            # Handle potential prefixes like "TASK-ID: " or just "ID: "
            # And handle cases where it might return just description if malformed
            if ":" in response:
                task_id, description = response.split(":", 1)
                task_data = {"id": task_id.strip(), "description": description.strip()}
                task_desc = response
            else:
                 task_data = {"id": "UNKNOWN", "description": response}
                 task_desc = response

            print(f"   Picked up: {task_desc}")
        except ValueError:
            print(f"   Failed to parse task response: {response}")
            raise ValueError(f"CRITICAL: Task Parse Error. Response: {response}")

    # RAG Context Enrichment
    print(f"\n[PLANNER] Enriching context with RAG...")
    context = local_rag.search(task_desc, limit=3)

    # Workflow Registry Consult
    print(f"\n[PLANNER] Consulting Workflow Registry...")
    suggested_workflow = await call_mcp_tool("get_suggested_workflow", {"intent": task_desc})
    print(f"   Registry Suggestion: {suggested_workflow[:50]}...")

    context += f"\n\n--- WORKFLOW REGISTRY ---\n{suggested_workflow}"
    print(f"   Context found: {len(context)} chars")

    # Now Plan
    print(f"\n[PLANNER] Analyzing task: {task_desc}")

    # Use Planning Crew (CrewAI)
    from Agentic.Crews.planning_crew import PlanningCrew

    try:
        planner = PlanningCrew()
        # Pass enriched context to the planner
        crew_task = f"Task: {task_desc}\nContext from Codebase:\n{context}"
        crew_output = planner.run(crew_task)

        print(f"\n[PLANNER] Crew Output: {crew_output}")
        plan_steps = [str(crew_output)]

    except Exception as e:
        print(f"[WARN] [PLANNER] CrewAI failed: {e}. Falling back to basic plan.")
        if "MATCHED WORKFLOW" in suggested_workflow:
             plan_steps = ["Follow Registry Workflow: " + suggested_workflow]
        else:
             plan_steps = ["Analyze requirements", "Implement changes", "Verify"]

    # STRICT SANDBOX ENFORCEMENT
    # The user requires all autonomous work to be confined to .YBIS_Dev
    if ".YBIS_Dev" not in task_desc:
        task_desc = f"[STRICT SANDBOX: ALL FILES MUST BE IN .YBIS_Dev/] {task_desc}"

    plan_obj = Plan(
        objective=task_desc,
        steps=plan_steps,
        files_to_modify=[],
        dependencies=[],
        risks=[],
        success_criteria=[],
        metadata={"task_id": task_data['id'] if task_data else "AD-HOC", "source": "CrewAI"}
    )

    return {
        "task": task_desc,
        "task_data": task_data,
        "plan": plan_obj,
        "retry_count": 0,
        "history": [f"Planned: {task_desc}"]
    }

async def node_spec_writer(state: AgentState):
    """
    Role: Product Manager (PM)
    Action: Write a PRD (Spec) based on the task description.
    """
    task_desc = state.get('task', "New Feature Request")
    print(f"\n[SPEC WRITER] drafting PRD for: {task_desc}")

    # Load Template
    tmpl_path = Path(".YBIS_Dev/Veriler/templates/prd-tmpl.yaml")
    if not tmpl_path.exists():
        print("   ⚠️ Template not found, skipping spec generation.")
        return {"history": ["Spec skipped (no template)"]}

    # Mock Logic: In real implementation, this would call LLM to fill template
    # For now, we generate a stub PRD to prove the flow.
    # TODO: Connect to PlanningCrew or specific PM Agent.

    prd_content = f"""# PRD: {task_desc}

## Overview
Automatically generated spec for {task_desc}.

## User Stories
- Story 1: Implement the core logic for {task_desc}
- Story 2: Add verification tests

## Implementation Steps
1. Create `feature.py`.
2. Update `main.py`.
"""

    # Save PRD
    task_data = state.get('task_data') or {}
    task_id = task_data.get('id', 'adhoc')
    prd_path = Path(f"docs/prd/prd-{task_id}.md")
    prd_path.parent.mkdir(parents=True, exist_ok=True)
    prd_path.write_text(prd_content, encoding='utf-8')
    print(f"   ✅ Saved PRD to: {prd_path}")

    return {
        "history": [f"Created Spec: {prd_path.name}"]
    }

async def node_sharder(state: AgentState):
    """
    Role: Architect
    Action: Shard the PRD into individual Story files.
    """
    print(f"\n🧱 [SHARDER] Splitting PRD into Stories...")

    # Locate recent PRD
    task_data = state.get('task_data') or {}
    task_id = task_data.get('id', 'adhoc')
    prd_path = Path(f"docs/prd/prd-{task_id}.md")

    if not prd_path.exists():
        print("   ⚠️ PRD not found, cannot shard.")
        return {"history": ["Sharding failed"]}

    content = prd_path.read_text(encoding='utf-8')

    # Simple Regex to find stories (Mock Implementation)
    # Looking for lines starting with "- Story X:"
    stories = re.findall(r"- Story \d+: (.+)", content)

    generated_stories = []
    for idx, story_title in enumerate(stories, 1):
        story_content = f"""# Story {idx}: {story_title}

## Context
Derived from {prd_path.name}

## Requirements
- Implement {story_title}

## Verification
- [ ] Verify {story_title} works.
"""
        story_file = prd_path.parent / f"story-{task_id}-{idx}.md"
        story_file.write_text(story_content, encoding='utf-8')
        generated_stories.append(str(story_file))
        print(f"   Shard {idx}: {story_file.name}")

    return {
        "history": [f"Sharded {len(generated_stories)} stories"]
    }

async def node_approval(state: AgentState):
    """
    Role: Safety Officer
    Action: Ask Brain (and Human) for permission to proceed with Coding.
    """
    print(f"\\n[APPROVAL] Requesting permission to code...")

    task_desc = state.get('task', "Unknown Task")
    question = f"Ready to implement: {task_desc}. Proceed?"

    # Call Brain's Safety Tool
    approval = await call_mcp_tool("ask_user", {"question": question})

    print(f"   Response: {approval}")

    if approval == "APPROVED":
        return {"history": ["Approved"]}
    else:
        # If denied, we should probably stop or pause.
        # For MVP, we treat denial as a hard stop/failure for this run.
        print("   ❌ Permission DENIED. Stopping execution.")
        # We manipulate state to cause a stop, or we can route to END.
        # Simple hack: Clear the plan so Coder does nothing, or flag it.
        return {
            "plan": None,
            "history": ["Denied"]
        }


async def node_coder(state: AgentState):
    """
    Role: Executor (Aider)
    Action: Execute the plan using Local LLM, strictly following Story Shards if available.
    """
    plan = state.get("plan")
    task_data = state.get("task_data") or {}
    task_id = task_data.get('id', 'adhoc')

    # Inject MCP URL for Aider (even if not used via flag, good practice)
    os.environ['MCP_SERVER_URL'] = MCP_SERVER_URL
    print(f"\n⚡ [CODER] Environment set: MCP_SERVER_URL={MCP_SERVER_URL}")

    # Fetch Repo Tree via MCP to ensure consistent view
    print("   [CODER] Fetching Repo Tree from MCP Brain...")
    repo_tree_context = await call_mcp_tool("get_repo_tree", {"max_depth": 2})
    if not repo_tree_context:
        repo_tree_context = "(Repo tree unavailable)"

    mcp_context_header = f"\nSYSTEM CONTEXT [FROM MCP BRAIN]:\nRepo Structure:\n{repo_tree_context}\n\n"

    # 1. SDD Check: Are there story files?
    story_files = sorted(list(Path(f"docs/prd").glob(f"story-{task_id}-*.md")))

    if story_files:
        print(f"\n⚡ [CODER] SDD MODE ACTIVATED. Found {len(story_files)} stories.")

        results = []
        executor = AiderExecutor()
        sandbox_path = os.getcwd()

        for story_path in story_files:
            print(f"   ▶️ Implementing: {story_path.name}")
            story_content = story_path.read_text(encoding="utf-8")

            # Construct a specific plan object for this story
            story_plan = Plan(
                objective=f"Implement Check: {story_path.name}",
                steps=[f"Read {story_path}", "Implement requirements"],
                files_to_modify=[], # Aider will infer
                dependencies=[],
                risks=[],
                success_criteria=[],
                metadata={"source": "SDD_Story"}
            )

            # Extract prompt from story content and inject MCP context
            prompt = mcp_context_header + f"""
IMPORTANT: YOU ARE IN A STRICT SANDBOX.
- YOU MUST ONLY CREATE/EDIT FILES INSIDE '.YBIS_Dev/'.
- DO NOT TOUCH 'apps/', 'packages/', 'scripts/' OR ANY ROOT FOLDERS.
- IF THE STORY ASKS FOR ROOT FILES, IGNORE IT AND CREATE A MOCK IN '.YBIS_Dev/'.

Implement the following story strictly:

{story_content}"""
            story_plan.objective = prompt

            result = await executor.execute(story_plan, sandbox_path)
            results.append(result)

            if not result.success:
                print(f"   ❌ Failed on {story_path.name}. Stopping.")
                return {
                    "code_result": result, # Return the failed result
                    "history": [f"Failed Story: {story_path.name}"]
                }

        # If all stories passed
        final_result = results[-1] # Simplification
        return {
            "code_result": final_result,
            "history": [f"Completed {len(results)} stories"]
        }

    # 2. Fallback to Old Plan Flow
    if not plan:
        return {"history": ["Coder skipped"]}

    print(f"\n[CODER] Handing off to Aider (Legacy Plan Mode)...")
    if state.get("retry_count", 0) > 0:
        print(f"   🔄 RETRY ATTEMPT {state['retry_count']}")

    # Inject Context into Legacy Plan
    plan.objective = mcp_context_header + plan.objective

    executor = AiderExecutor()
    sandbox_path = os.getcwd()

    result = await executor.execute(state["plan"], sandbox_path)

    return {
        "code_result": result,
        "history": [f"Coded: {result.success}"]
    }

async def node_verifier(state: AgentState):
    """
    Role: Guardian (Sentinel)
    Action: Verify and Update Board.
    """
    if not state.get("code_result"):
        return {"history": ["Verifier skipped"]}

    print(f"\n[VERIFIER] Checking integrity...")
    verifier = SentinelVerifier()
    verification = await verifier.verify(state["code_result"], os.getcwd())

    status = "Passed" if verification.lint_passed else "Failed"
    print(f"   Status: {status}")

    # Update Task Board ONLY if passed
    task_data = state.get("task_data")
    if task_data and status == "Passed":
        print(f"   [DONE] Marking {task_data['id']} as DONE via MCP.")
        await call_mcp_tool("update_task_status", {
            "task_id": task_data['id'],
            "status": "DONE"
        })
    elif status == "Failed":
         print(f"   ❌ Verification failed. Errors: {verification.errors}")

    return {
        "verification": verification,
        "history": [f"Verified: {status}"]
    }

def should_retry(state: AgentState) -> str:
    """Determine if we should retry coding."""
    print(f"[ROUTER] Checking status... Count: {state.get('retry_count')}")

    # If passed, go to end
    if state["verification"] and state["verification"].lint_passed:
        return "end"

    # If failed but retries left
    if state.get("retry_count", 0) < 3:
        return "retry"

    return "end"

# --- GRAPH ---

def build_graph():
    builder = StateGraph(AgentState)
    builder.add_node("planner", node_planner)
    builder.add_node("coder", node_coder)
    builder.add_node("verifier", node_verifier)

    builder.set_entry_point("planner")

    # SDD Pipeline: Planner -> Spec Writer -> Sharder -> Coder -> Verifier
    builder.add_node("spec_writer", node_spec_writer)
    builder.add_node("sharder", node_sharder)
    builder.add_node("approval", node_approval)

    builder.add_edge("planner", "spec_writer")
    builder.add_edge("spec_writer", "sharder")
    builder.add_edge("sharder", "approval")
    builder.add_edge("approval", "coder")
    builder.add_edge("coder", "verifier")

    # Conditional Edge for Retry Loop
    builder.add_conditional_edges(
        "verifier",
        should_retry,
        {
            "retry": "coder",
            "end": END
        }
    )

    return builder.compile()

# --- MAIN RUNNER ---

async def main():
    print("[LAUNCH] YBIS UNIFIED ORCHESTRATOR (LangGraph + Aider + Local LLM)")
    app = build_graph()

    # Start with empty state -> Planner will fetch from Board
    initial_state = {
        "task": None,
        "task_data": None,
        "history": [],
        "plan": None,
        "code_result": None,
        "verification": None
    }

    await app.ainvoke(initial_state)
    print("\n✅ WORKFLOW COMPLETE.")

if __name__ == "__main__":
    asyncio.run(main())
