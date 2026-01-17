"""
Neo4j Graph Store Adapter.

Adapter for Neo4j graph database integration for dependency tracking.
"""

import os
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from ..syscalls.journal import append_event


class GraphStoreAdapter(ABC):
    """Base interface for graph store adapters."""

    @abstractmethod
    def is_available(self) -> bool:
        """Check if adapter is available."""
        ...

    @abstractmethod
    def impact_analysis(self, file_path: str, max_depth: int = 3) -> list[dict[str, Any]]:
        """Find all nodes affected if this file changes."""
        ...

    @abstractmethod
    def find_circular_dependencies(self) -> list[list[str]]:
        """Find circular dependency chains."""
        ...

    @abstractmethod
    def get_critical_nodes(self, min_dependents: int = 3, limit: int = 10) -> list[dict[str, Any]]:
        """Get files with the most dependents."""
        ...


class Neo4jGraphStoreAdapter(GraphStoreAdapter):
    """Neo4j graph store adapter."""

    def __init__(
        self,
        uri: str | None = None,
        user: str | None = None,
        password: str | None = None,
        run_path: Path | None = None,
        trace_id: str | None = None,
    ):
        """
        Initialize Neo4j adapter.

        Args:
            uri: Neo4j URI (default: bolt://localhost:7687)
            user: Neo4j username (default: neo4j)
            password: Neo4j password (default: from env or ybis-graph-2025)
            run_path: Optional run path for journal logging
            trace_id: Optional trace ID for journal logging
        """
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "ybis-graph-2025")
        self._driver = None
        self._available = False
        self.run_path = run_path
        self.trace_id = trace_id
        self._initialize()
        
        # Journal: Neo4j connect
        if self.run_path and self._available:
            append_event(
                self.run_path,
                "NEO4J_CONNECT",
                {
                    "uri": self.uri,
                },
                trace_id=self.trace_id,
            )

    def _initialize(self) -> None:
        """Initialize Neo4j driver."""
        try:
            from neo4j import GraphDatabase

            self._driver = GraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
            )
            # Test connection
            with self._driver.session() as session:
                session.run("RETURN 1")
            self._available = True
        except ImportError:
            self._available = False
        except Exception:
            self._available = False

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

    def close(self) -> None:
        """Close Neo4j connection."""
        if self._driver:
            self._driver.close()

    def is_available(self) -> bool:
        """Check if Neo4j is available."""
        if not self._available:
            self._initialize()
        return self._available

    def initialize_schema(self) -> None:
        """Initialize Neo4j schema (constraints and indexes)."""
        if not self.is_available():
            return

        with self._driver.session() as session:
            # Constraints
            constraints = [
                "CREATE CONSTRAINT IF NOT EXISTS FOR (n:CodeFile) REQUIRE n.path IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (n:DocFile) REQUIRE n.path IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Function) REQUIRE n.qualified_name IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Class) REQUIRE n.qualified_name IS UNIQUE",
            ]

            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception:
                    pass  # Constraint might already exist

            # Indexes
            indexes = [
                "CREATE INDEX IF NOT EXISTS FOR (n:CodeFile) ON (n.name)",
                "CREATE INDEX IF NOT EXISTS FOR (n:DocFile) ON (n.section)",
                "CREATE INDEX IF NOT EXISTS FOR (n:Function) ON (n.file_path)",
            ]

            for index in indexes:
                try:
                    session.run(index)
                except Exception:
                    pass  # Index might already exist

    def impact_analysis(self, file_path: str, max_depth: int = 3) -> list[dict[str, Any]]:
        """Find all nodes affected if this file changes."""
        if not self.is_available():
            return []

        with self._driver.session() as session:
            query = f"""
                MATCH (source {{path: $path}})
                MATCH path = (source)<-[:IMPORTS|REFERENCES|USES*1..{max_depth}]-(affected)
                WITH DISTINCT affected,
                     length(shortestPath((source)<-[*]-(affected))) as distance
                RETURN affected.path as path,
                       labels(affected)[0] as type,
                       distance
                ORDER BY distance, path
            """
            result = session.run(query, path=file_path)
            records = [dict(record) for record in result]
            
            # Journal: Neo4j query
            if self.run_path:
                elapsed_ms = (time.time() - start_time) * 1000
                append_event(
                    self.run_path,
                    "NEO4J_QUERY",
                    {
                        "operation": "impact_analysis",
                        "results_count": len(records),
                        "duration_ms": round(elapsed_ms, 2),
                    },
                    trace_id=self.trace_id,
                )

            return records

    def find_circular_dependencies(self) -> list[list[str]]:
        """Find circular dependency chains."""
        if not self.is_available():
            return []

        with self._driver.session() as session:
            result = session.run("""
                MATCH path = (a:CodeFile)-[:IMPORTS*]->(a)
                WITH [node in nodes(path) | node.path] as cycle
                RETURN DISTINCT cycle
                LIMIT 20
            """)

            return [record["cycle"] for record in result]

    def get_critical_nodes(self, min_dependents: int = 3, limit: int = 10) -> list[dict[str, Any]]:
        """Get files with the most dependents."""
        if not self.is_available():
            return []

        with self._driver.session() as session:
            result = session.run(
                """
                MATCH (n)<-[:IMPORTS|REFERENCES|USES*1..2]-(dependent)
                WITH n, count(DISTINCT dependent) as dependents
                WHERE dependents >= $min_deps
                RETURN n.path as path,
                       labels(n)[0] as type,
                       dependents
                ORDER BY dependents DESC
                LIMIT $limit
            """,
                min_deps=min_dependents,
                limit=limit,
            )

            return [dict(record) for record in result]

    def add_node(self, node_type: str, node_id: str, properties: dict[str, Any] | None = None) -> None:
        """
        Add a node to the Neo4j graph.
        
        Args:
            node_type: Node label (e.g., "CodeFile", "Function", "Class")
            node_id: Unique node identifier (typically file path or qualified name)
            properties: Optional node properties
        """
        if not self.is_available():
            return
        
        properties = properties or {}
        properties["path"] = node_id  # Ensure path property exists
        
        with self._driver.session() as session:
            query = f"""
                MERGE (n:{node_type} {{path: $path}})
                SET n += $properties
            """
            session.run(query, path=node_id, properties=properties)

    def add_edge(
        self,
        from_node_id: str,
        to_node_id: str,
        relationship_type: str,
        properties: dict[str, Any] | None = None,
    ) -> None:
        """
        Add an edge (relationship) between two nodes.
        
        Args:
            from_node_id: Source node identifier
            to_node_id: Target node identifier
            relationship_type: Relationship type (e.g., "IMPORTS", "REFERENCES", "USES")
            properties: Optional relationship properties
        """
        if not self.is_available():
            return
        
        properties = properties or {}
        
        with self._driver.session() as session:
            query = f"""
                MATCH (from), (to)
                WHERE from.path = $from_path AND to.path = $to_path
                MERGE (from)-[r:{relationship_type}]->(to)
                SET r += $properties
            """
            session.run(query, from_path=from_node_id, to_path=to_node_id, properties=properties)
            
            # Journal: Neo4j update
            if self.run_path:
                append_event(
                    self.run_path,
                    "NEO4J_UPDATE",
                    {
                        "operation": "add_edge",
                        "relationship_type": relationship_type,
                    },
                    trace_id=self.trace_id,
                )

    def query(self, cypher_query: str, parameters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """
        Execute a Cypher query and return results.
        
        Args:
            cypher_query: Cypher query string
            parameters: Optional query parameters
            
        Returns:
            List of result dictionaries
        """
        if not self.is_available():
            return []
        
        parameters = parameters or {}
        
        with self._driver.session() as session:
            result = session.run(cypher_query, **parameters)
            return [dict(record) for record in result]


