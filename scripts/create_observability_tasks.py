#!/usr/bin/env python3
"""
Create Comprehensive Observability Tasks - Add all missing observability features.

This script creates tasks for:
1. Graph visualization
2. Metrics collection (Prometheus)
3. Real-time monitoring dashboard
4. Streaming output
"""

import sys
import asyncio
import json
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def create_observability_tasks():
    """Create comprehensive observability tasks."""
    print("=" * 60)
    print("Creating Observability Enhancement Tasks")
    print("=" * 60)
    print()
    
    tasks = [
        {
            "title": "Feature: Add Workflow Graph Visualization",
            "objective": """
# Problem Statement
YBIS needs visual representation of workflow execution to help users understand
workflow structure, node status, and execution flow. Currently, workflows are only
visible through logs and artifacts.

# Context
- System: YBIS workflow execution
- Current state: Workflows execute but no visual representation
- Need: Interactive graph visualization for workflows

# Requirements
1. Create workflow graph visualization component:
   - Visual representation of workflow nodes and connections
   - Node status indicators (pending/running/success/error)
   - Real-time status updates during execution
   - Interactive node details (click to see artifacts)

2. Integrate with dashboard:
   - Add graph visualization to `src/ybis/services/dashboard.py`
   - Show workflow graph for current/active runs
   - Allow navigation between nodes

3. Use existing libraries:
   - NetworkX for graph structure
   - Graphviz or D3.js for visualization
   - Streamlit for dashboard integration

4. Add graph export:
   - Export workflow graph as PNG/SVG
   - Export as JSON for external tools

# Success Criteria
- [ ] Workflow graph visualization component created
- [ ] Graph shows nodes and connections correctly
- [ ] Real-time status updates work
- [ ] Integrated into dashboard
- [ ] Graph export works (PNG/SVG/JSON)
- [ ] Documentation updated

# Dependencies
- Dashboard service (`src/ybis/services/dashboard.py`)
- Workflow registry (`src/ybis/workflows/registry.py`)
- NetworkX or graphviz library

# Risks
- Risk: Performance impact of real-time updates
  Mitigation: Use efficient graph libraries, limit update frequency
- Risk: Complex workflows may be hard to visualize
  Mitigation: Add zoom, pan, and filtering capabilities

# Implementation Notes
- Use LangGraph's built-in graph structure
- Consider using `graphviz` for static graphs
- Consider using `plotly` or `networkx` for interactive graphs
- Add caching for large workflows
""",
            "priority": "HIGH"
        },
        {
            "title": "Feature: Add Prometheus Metrics Collection",
            "objective": """
# Problem Statement
YBIS needs metrics collection for monitoring performance, success rates, and costs.
Currently, metrics are only available in journal logs, making aggregation and
monitoring difficult.

# Context
- System: YBIS workflow execution
- Current state: Metrics in journal logs only
- Need: Prometheus metrics endpoint for monitoring

# Requirements
1. Implement Prometheus metrics:
   - Workflow execution metrics (count, duration, success rate)
   - Node execution metrics (count, duration, success rate per node type)
   - LLM call metrics (count, tokens, cost, latency per model)
   - Error metrics (count, type, frequency)

2. Add metrics endpoint:
   - `/metrics` endpoint for Prometheus scraping
   - Use `prometheus_client` library
   - Expose metrics in standard format

3. Aggregate metrics:
   - Per-task metrics
   - Per-workflow metrics
   - Per-node-type metrics
   - Overall system metrics

4. Add metrics to dashboard:
   - Show metrics in dashboard
   - Create metrics visualization
   - Add alerts for thresholds

# Success Criteria
- [ ] Prometheus metrics implemented
- [ ] Metrics endpoint available at `/metrics`
- [ ] All key metrics collected (workflow, node, LLM, errors)
- [ ] Metrics aggregated correctly
- [ ] Dashboard shows metrics
- [ ] Documentation updated

# Dependencies
- `prometheus_client` library
- Dashboard service
- Metrics aggregation logic

# Risks
- Risk: High cardinality metrics
  Mitigation: Use labels carefully, aggregate where possible
- Risk: Performance impact
  Mitigation: Use efficient metrics collection, batch updates

# Implementation Notes
- Use `prometheus_client` for metrics
- Add metrics to `src/ybis/services/metrics.py` (new file)
- Integrate with existing logging
- Consider using `prometheus-fastapi-instrumentator` for FastAPI
""",
            "priority": "HIGH"
        },
        {
            "title": "Feature: Add Real-Time Monitoring Dashboard",
            "objective": """
# Problem Statement
YBIS needs real-time monitoring to track workflow execution, node status, and
system health. Currently, users must poll for status updates.

# Context
- System: YBIS workflow execution
- Current state: Status updates via polling only
- Need: Real-time monitoring with live updates

# Requirements
1. Implement streaming output:
   - Stream workflow execution logs in real-time
   - Stream node status updates
   - Stream LLM call progress
   - Use Server-Sent Events (SSE) or WebSocket

2. Create real-time dashboard:
   - Live workflow status board
   - Real-time node execution status
   - Live metrics updates
   - Real-time alerts

3. Add WebSocket support:
   - WebSocket endpoint for real-time updates
   - Client reconnection handling
   - Message queuing for missed updates

4. Add alerts:
   - Alert on workflow failures
   - Alert on node errors
   - Alert on performance degradation
   - Alert on cost thresholds

# Success Criteria
- [ ] Streaming output works for workflow execution
- [ ] Real-time dashboard shows live updates
- [ ] WebSocket connection stable
- [ ] Alerts work correctly
- [ ] Documentation updated

# Dependencies
- Dashboard service
- WebSocket library (e.g., `websockets`, `fastapi-websocket`)
- Event bus (optional, for distributed alerts)

# Risks
- Risk: WebSocket connection issues
  Mitigation: Implement reconnection logic, message queuing
- Risk: Performance impact of real-time updates
  Mitigation: Throttle updates, use efficient protocols

# Implementation Notes
- Use FastAPI WebSocket for real-time updates
- Consider using Redis pub/sub for distributed updates
- Add rate limiting for updates
- Use efficient serialization (MessagePack or JSON)
""",
            "priority": "MEDIUM"
        },
        {
            "title": "Feature: Add Dependency Graph Visualization",
            "objective": """
# Problem Statement
YBIS needs dependency graph visualization to help users understand code
dependencies, impact analysis, and change propagation.

# Context
- System: YBIS code analysis
- Current state: Dependency analysis exists but no visualization
- Need: Visual representation of code dependencies

# Requirements
1. Create dependency graph visualization:
   - Visual representation of code dependencies
   - Module/file dependency graph
   - Function/class dependency graph
   - Impact analysis visualization

2. Integrate with existing code graph:
   - Use `src/ybis/services/code_graph.py`
   - Visualize dependencies from Pyan analysis
   - Show circular dependencies
   - Highlight critical paths

3. Add interactive features:
   - Click to see file details
   - Filter by dependency type
   - Search for specific modules
   - Export graph as image

4. Add to dashboard:
   - Dependency graph page in dashboard
   - Integration with impact analysis
   - Real-time updates on code changes

# Success Criteria
- [ ] Dependency graph visualization created
- [ ] Graph shows code dependencies correctly
- [ ] Interactive features work
- [ ] Integrated into dashboard
- [ ] Export functionality works
- [ ] Documentation updated

# Dependencies
- Code graph service (`src/ybis/services/code_graph.py`)
- NetworkX or graphviz
- Dashboard service

# Risks
- Risk: Large codebases may have complex graphs
  Mitigation: Add filtering, clustering, and zoom capabilities
- Risk: Performance with large graphs
  Mitigation: Use efficient graph libraries, lazy loading

# Implementation Notes
- Use existing Pyan analysis results
- Consider using `pyvis` for interactive graphs
- Add graph simplification for large codebases
- Cache graph generation results
""",
            "priority": "MEDIUM"
        }
    ]
    
    # Connect to MCP
    server_params = StdioServerParameters(
        command="python",
        args=["scripts/ybis_mcp_server.py"],
        env=None,
    )
    
    created_tasks = []
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            
            for task_info in tasks:
                print(f"Creating task: {task_info['title']}")
                result = await session.call_tool(
                    "task_create",
                    arguments={
                        "title": task_info["title"],
                        "objective": task_info["objective"],
                        "priority": task_info["priority"],
                    }
                )
                
                task_data = json.loads(result.content[0].text)
                task_id = task_data["task_id"]
                created_tasks.append({
                    "task_id": task_id,
                    "title": task_info["title"],
                    "priority": task_info["priority"],
                })
                
                print(f"  ✅ Created: {task_id}")
                print()
    
    print("=" * 60)
    print("✅ All Observability Tasks Created!")
    print("=" * 60)
    print()
    print("Created tasks:")
    for task in created_tasks:
        print(f"  - {task['task_id']}: {task['title']} ({task['priority']})")
    print()
    print("To run all tasks:")
    for task in created_tasks:
        print(f"  python scripts/ybis_run.py {task['task_id']} --workflow self_develop")
    print("=" * 60)
    
    return created_tasks


if __name__ == "__main__":
    try:
        tasks = asyncio.run(create_observability_tasks())
        print(f"\n✅ Created {len(tasks)} observability tasks")
    except KeyboardInterrupt:
        print("\n⚠️  Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

