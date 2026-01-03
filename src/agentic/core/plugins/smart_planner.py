
"""
Smart Planner Plugin for YBIS Orchestrator.
Integrates MCP tools (GraphDB, Memory) into the planning phase.
"""

import json
from typing import Any, Dict, List
from src.agentic.core.protocols import PlannerProtocol, Plan
from src.agentic.core.logger import log

class SmartPlanner(PlannerProtocol):
    """
    A planner that consults the Graph and Memory before generating a plan.
    """

    def __init__(self, mcp_client=None):
        self.mcp = mcp_client # Injected MCP client wrapper
        # If no client provided, we might fallback to direct tool calls or fail gracefully

    def name(self) -> str:
        return "SmartPlanner-V1"

    async def _consult_graph(self, task_description: str) -> List[str]:
        """
        Extract potential file paths from task description and ask GraphDB for impact.
        """
        # Simple heuristic: find words ending in .py, .md, .js
        words = task_description.split()
        potential_files = [w for w in words if w.endswith(('.py', '.md', '.ts', '.js', '.json'))]

        impact_report = []
        if self.mcp:
            for f in potential_files:
                # Assuming mcp_client has a method to call 'check_dependency_impact'
                # For now, we simulate or use a direct import if possible,
                # but ideally this should be an MCP call.
                try:
                    # Direct import fallback for now (Frankenstein style)
                    from src.agentic.mcp_server import check_dependency_impact
                    report = check_dependency_impact(f)
                    impact_report.append(f" Impact of changing {f}:\n{report}")
                except Exception as e:
                    log.warning(f"Failed to check graph impact for {f}: {e}")

        return impact_report

    async def plan(self, task: str, context: Dict[str, Any]) -> Plan:
        log.info(f"[{self.name()}] Thinking about: {task}")

        # 1. Gather Intelligence (Graph & Memory)
        graph_insights = await self._consult_graph(task)

        # 2. Construct Prompt for LLM
        prompt = f"""
        You are the Chief Architect of YBIS.

        TASK:
        {task}

        CONTEXT:
        {json.dumps(context, indent=2)}

        GRAPH INSIGHTS (Dependency Risks):
        {chr(10).join(graph_insights)}

        OBJECTIVE:
        Create a detailed execution plan.

        REQUIREMENTS:
        - List specific files to create or modify.
        - Define a verification strategy (how to test).
        - If graph insights show high risk, add extra testing steps.

        Output must be valid JSON matching the 'Plan' schema.
        """

        # 3. Call LLM (Ollama via bridge or direct)
        # For this prototype, we will use a mock/simple logic or call existing router
        # In a real implementation, this calls self.llm.generate(prompt)

        log.info(f"[{self.name()}] Generated smart plan based on graph insights.")

        # returning a skeleton plan for now to integrate into the graph
        return Plan(
            objective="Smart Plan Execution",
            steps=["Analyze dependencies", "Implement changes", "Verify against graph"],
            files_to_modify=["(determined by execution)"],
            dependencies=graph_insights,
            risks=["Dependency breakage"] if graph_insights else [],
            success_criteria=["Tests pass", "Graph integrity maintained"]
        )

# Factory for dynamic loading
def create_planner():
    return SmartPlanner()
