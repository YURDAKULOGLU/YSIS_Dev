# Neo4j Graph Store Adapter

**Type:** Graph Store  
**Maturity:** Beta  
**Default Enabled:** No

## Overview

Neo4j Graph Store provides code dependency tracking and analysis. It builds a graph of code relationships (imports, references, dependencies) and enables impact analysis, circular dependency detection, and critical file identification.

## Features

- ✅ Code dependency graph
- ✅ Impact analysis (what breaks if file changes)
- ✅ Circular dependency detection
- ✅ Critical file identification
- ✅ Relationship tracking (imports, references, uses)

## Installation

### Prerequisites

1. **Neo4j Server:** Install Neo4j Community Edition or use Neo4j Aura
2. **Python Package:** Install Neo4j driver

```bash
# Install adapter dependencies
pip install -e ".[adapters-neo4j]"

# Or install directly
pip install "neo4j>=5.0.0,<6.0.0"
```

### Setup

#### Local Neo4j

```bash
# Using Docker
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/ybis-graph-2025 \
  neo4j:latest
```

#### Neo4j Aura (Cloud)

1. Create account at https://neo4j.com/cloud/aura/
2. Create database instance
3. Get connection URI and credentials

## Configuration

### Policy Configuration

```yaml
# configs/profiles/default.yaml
adapters:
  neo4j_graph:
    enabled: true  # Enable Neo4j adapter
```

### Environment Variables

```bash
export NEO4J_URI="bolt://localhost:7687"  # or Neo4j Aura URI
export NEO4J_USER="neo4j"
export NEO4J_PASSWORD="ybis-graph-2025"
```

## Usage

### Via Dependency Tools

Neo4j adapter is used automatically by dependency analysis MCP tools:

```python
# Via MCP tool
from src.ybis.services.mcp_tools.dependency_tools import check_dependency_impact

result = check_dependency_impact("src/config.py", max_depth=3)
```

### Direct Usage

```python
from src.ybis.adapters.graph_store_neo4j import Neo4jGraphStoreAdapter

adapter = Neo4jGraphStoreAdapter()
if adapter.is_available():
    # Initialize schema
    adapter.initialize_schema()
    
    # Impact analysis
    affected = adapter.impact_analysis("src/config.py", max_depth=3)
    
    # Circular dependencies
    cycles = adapter.find_circular_dependencies()
    
    # Critical files
    critical = adapter.get_critical_nodes(min_dependents=5)
```

## Graph Population

The graph must be populated before use. Use a graph ingestion script:

```python
# scripts/ingest_graph.py (to be created)
from src.ybis.adapters.graph_store_neo4j import Neo4jGraphStoreAdapter
import ast
from pathlib import Path

adapter = Neo4jGraphStoreAdapter()
adapter.initialize_schema()

# Scan codebase and populate graph
for py_file in Path("src").rglob("*.py"):
    # Parse imports, create nodes and relationships
    # ...
```

## Capabilities

- **Impact Analysis:** Find all files affected by a change
- **Circular Dependencies:** Detect dependency cycles
- **Critical Files:** Identify high-impact files
- **Dependency Paths:** Find shortest paths between files

## Limitations

- Requires Neo4j server (local or cloud)
- Graph must be populated manually (no auto-sync yet)
- Beta maturity (may have limitations)

## Troubleshooting

### Connection Failed

**Error:** `ServiceUnavailable` or connection timeout

**Solution:**
```bash
# Check Neo4j is running
docker ps | grep neo4j

# Or check connection
cypher-shell -u neo4j -p ybis-graph-2025 "RETURN 1"
```

### Empty Graph

**Error:** No results from queries

**Solution:**
- Graph must be populated first
- Run graph ingestion script
- Check that nodes and relationships were created

### Schema Errors

**Error:** Constraint or index creation fails

**Solution:**
```python
# Re-initialize schema
adapter = Neo4jGraphStoreAdapter()
adapter.initialize_schema()
```

## See Also

- [Adapter Catalog](../../configs/adapters.yaml)
- [Dependency Tools](../../src/ybis/services/mcp_tools/dependency_tools.py)
- [Neo4j Documentation](https://neo4j.com/docs/)

