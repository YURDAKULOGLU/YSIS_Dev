---
id: TASK-New-404
type: PLAN
status: IN_PROGRESS
created_at: 2025-12-29T00:40:00
target_files:
  - src/dashboard/app.py
  - src/dashboard/components/hive_visualizer.py
---

# Task: Hive Mind Visualization (TASK-New-404)

## Objective
To create a high-impact, real-time visualization of the "Hive Mind" within the Streamlit dashboard. This will show how Agents, Tasks, and Knowledge (Neo4j nodes) are interconnected.

## Approach
We will use `streamlit-agraph` or simple `networkx` + `matplotlib` (fallback) to render the graph. Since we already have a rich Neo4j graph, we will query it for the most recent and important relationships.

## Steps
1.  **Dependencies:** Install `streamlit-agraph`.
2.  **Visualizer Component:** Create `src/dashboard/components/hive_visualizer.py`.
    - Function to fetch data from Neo4j.
    - Function to render the graph.
3.  **App Integration:** Update `src/dashboard/app.py`.
    - Add a new "Hive Mind" section/tab.
    - Inject the visualizer.
4.  **Verification:** Run Streamlit and check the UI.

## Acceptance Criteria
- [ ] New "Hive Mind" tab exists in Dashboard.
- [ ] Displays a graph of Agents and their current Tasks.
- [ ] Data is pulled live from Neo4j.
- [ ] All mandatory artifacts produced.