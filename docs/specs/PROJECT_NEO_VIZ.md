# PROJECT NEO Visualization Strategy (Sigma.js)

## Goal
Define a visualization stack and UX for 5000+ node graphs (code, docs, tasks) that supports fast "Change Impact" analysis and incremental exploration.

## Requirements
- Render 5000+ nodes and 10k+ edges with interactive pan/zoom.
- Load subgraphs on demand, not the entire graph.
- Provide an "Impact Analysis" flow from a selected node (file, function, task, doc).
- Support filters by node/edge type and depth.
- Remain embeddable in the existing Streamlit dashboard or a minimal web view.

## Recommended Stack
### Core Visualization
- **Sigma.js + graphology** (WebGL-first).
  - Handles large graphs with progressive rendering.
  - Built-in camera controls and efficient edge rendering.
  - Supported by a stable ecosystem and good performance at 10k+ nodes.

### Alternate (Fallback)
- **Cytoscape.js (canvas renderer)**.
  - Strong graph features but heavier for very large graphs.
  - Use only if Sigma.js cannot integrate with the current dashboard.

## Integration Architecture
### Option A: Streamlit + Component
- Use a Streamlit component that hosts a small React app.
- React app loads Sigma.js, receives data via an API endpoint.
- Best for quick integration without replacing the dashboard.

### Option B: Separate Web UI
- Serve a small React page (or static build) alongside Streamlit.
- Dashboard links to the visualization view.
- Cleaner separation for performance and bundle size.

## Data Delivery and Querying
Do not load the full graph. Use **subgraph queries**:
- Query by node id + depth (1 to 4).
- Filter by edge types: `imports`, `calls`, `tests`, `docs`, `owns`, `generates`.
- Server returns a minimal node+edge list with lightweight attributes.

### API Shape (Example)
```
GET /api/graph/subgraph?id=<NODE_ID>&depth=2&edges=imports,tests,docs
Response:
{
  "nodes": [{ "id": "...", "type": "file", "label": "...", "group": "src" }],
  "edges": [{ "id": "...", "source": "...", "target": "...", "type": "imports" }]
}
```

### Neo4j Query Pattern (Pseudo)
```
MATCH p=(n {id:$id})-[r*1..$depth]->(m)
WHERE ALL(rel IN relationships(p) WHERE rel.type IN $edge_types)
RETURN DISTINCT nodes(p), relationships(p)
```

## Change Impact UX
### Primary Flow
1. Search for a node (file/function/task/doc).
2. Select depth (1-4).
3. Toggle edge filters (imports, tests, docs, owns, generates).
4. View affected nodes and paths (highlighted).

### Impact Summary Panel
- Node counts by type.
- Top 5 most central nodes in the subgraph.
- Test coverage visibility (tests connected to selected node).
- Risk flags (e.g., node with many downstream edges).

### Visual Cues
- Color by node type: file, function, test, doc, task.
- Edge styles by relationship type.
- Highlight shortest paths to tests/docs.
- Hover tooltips with metadata (path, last updated, owner).

## Performance Strategy
- Progressive reveal: start with a small subgraph, expand on click.
- Cluster by module/package; collapsed by default.
- Throttle re-renders and keep layout stable.
- Precompute degree or centrality scores for layout hints.
- Cache recent subgraph queries server-side.

## Operational Notes
- Do not assume full graph is available client-side.
- Store only minimal labels and ids in the client.
- Keep payload size small (< 1 MB) for responsiveness.

## Deliverables
- Visualization spec (this document).
- UI sketch or flow description for Change Impact.
- API contract for subgraph retrieval.
- Implementation notes for Streamlit integration.

## Risks
- Full-graph rendering will freeze; must stay subgraph-based.
- Neo4j query latency under load.
- Excessive edge density at higher depths.

## Next Steps
1. Confirm Sigma.js integration path (Streamlit component vs separate web UI).
2. Define node/edge schema for API.
3. Implement a minimal prototype with 1-2 subgraph queries.
