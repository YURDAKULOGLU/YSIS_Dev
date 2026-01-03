"""
Neo4j Graph Database Driver for YBIS Dependency Tracking
Implements PROJECT NEO schema and operations.
"""

import os
from typing import List, Dict, Any, Optional
from neo4j import GraphDatabase
from datetime import datetime


class GraphDB:
    """Neo4j driver for YBIS dependency graph."""

    def __init__(self, uri: str = None, user: str = None, password: str = None):
        """Initialize Neo4j connection."""
        self.uri = uri or os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.user = user or os.getenv("NEO4J_USER", "neo4j")
        self.password = password or os.getenv("NEO4J_PASSWORD", "ybis-graph-2025")

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.user, self.password)
        )

    def close(self):
        """Close database connection."""
        if self.driver:
            self.driver.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ========== SCHEMA INITIALIZATION ==========

    def initialize_schema(self):
        """Create constraints and indexes."""
        with self.driver.session() as session:
            # Constraints (unique)
            constraints = [
                "CREATE CONSTRAINT IF NOT EXISTS FOR (n:CodeFile) REQUIRE n.path IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (n:DocFile) REQUIRE n.path IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Function) REQUIRE n.qualified_name IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Class) REQUIRE n.qualified_name IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Agent) REQUIRE n.id IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Tool) REQUIRE n.name IS UNIQUE",
                "CREATE CONSTRAINT IF NOT EXISTS FOR (n:Task) REQUIRE n.id IS UNIQUE",
            ]

            for constraint in constraints:
                session.run(constraint)

            # Indexes (performance)
            indexes = [
                "CREATE INDEX IF NOT EXISTS FOR (n:CodeFile) ON (n.name)",
                "CREATE INDEX IF NOT EXISTS FOR (n:DocFile) ON (n.section)",
                "CREATE INDEX IF NOT EXISTS FOR (n:Function) ON (n.file_path)",
            ]

            for index in indexes:
                session.run(index)

    # ========== NODE CREATION ==========

    def create_code_file(self, path: str, **properties):
        """Create or update CodeFile node."""
        with self.driver.session() as session:
            session.run("""
                MERGE (f:CodeFile {path: $path})
                SET f += $props
                SET f.last_scanned = datetime()
            """, path=path, props=properties)

    def create_doc_file(self, path: str, **properties):
        """Create or update DocFile node."""
        with self.driver.session() as session:
            session.run("""
                MERGE (d:DocFile {path: $path})
                SET d += $props
                SET d.last_scanned = datetime()
            """, path=path, props=properties)

    def create_function(self, qualified_name: str, file_path: str, **properties):
        """Create or update Function node."""
        with self.driver.session() as session:
            session.run("""
                MERGE (fn:Function {qualified_name: $qname})
                SET fn.file_path = $file_path
                SET fn += $props
            """, qname=qualified_name, file_path=file_path, props=properties)

    def create_class(self, qualified_name: str, file_path: str, **properties):
        """Create or update Class node."""
        with self.driver.session() as session:
            session.run("""
                MERGE (c:Class {qualified_name: $qname})
                SET c.file_path = $file_path
                SET c += $props
            """, qname=qualified_name, file_path=file_path, props=properties)

    # ========== RELATIONSHIP CREATION ==========

    def create_import(self, from_path: str, to_path: str):
        """Create IMPORTS relationship between code files."""
        with self.driver.session() as session:
            session.run("""
                MATCH (from:CodeFile {path: $from})
                MATCH (to:CodeFile {path: $to})
                MERGE (from)-[r:IMPORTS]->(to)
                SET r.strength = coalesce(r.strength, 0) + 1
                SET r.last_seen = datetime()
            """, **{"from": from_path, "to": to_path})

    def create_defines(self, file_path: str, entity_qname: str, entity_type: str):
        """Create DEFINES relationship (CodeFile -> Function/Class)."""
        with self.driver.session() as session:
            session.run(f"""
                MATCH (f:CodeFile {{path: $file_path}})
                MATCH (e:{entity_type} {{qualified_name: $qname}})
                MERGE (f)-[:DEFINES]->(e)
            """, file_path=file_path, qname=entity_qname)

    def create_reference(self, from_path: str, to_path: str, ref_type: str = "markdown_link"):
        """Create REFERENCES relationship between docs/code."""
        with self.driver.session() as session:
            session.run("""
                MATCH (from {path: $from})
                MATCH (to {path: $to})
                MERGE (from)-[r:REFERENCES]->(to)
                SET r.link_type = $ref_type
                SET r.last_seen = datetime()
            """, **{"from": from_path, "to": to_path, "ref_type": ref_type})

    # ========== ANALYSIS QUERIES ==========

    def impact_analysis(self, file_path: str, max_depth: int = 5) -> List[Dict[str, Any]]:
        """
        Find all nodes affected if this file changes.
        Returns nodes that depend on (import/reference) this file.
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (source {path: $path})
                MATCH path = (source)<-[:IMPORTS|REFERENCES|USES*1..$depth]-(affected)
                WITH DISTINCT affected,
                     length(shortestPath((source)<-[*]-(affected))) as distance
                RETURN affected.path as path,
                       labels(affected)[0] as type,
                       distance
                ORDER BY distance, path
            """, path=file_path, depth=max_depth)

            return [dict(record) for record in result]

    def find_circular_dependencies(self, relationship_type: str = "IMPORTS") -> List[List[str]]:
        """Find circular dependency chains."""
        with self.driver.session() as session:
            result = session.run(f"""
                MATCH path = (a:CodeFile)-[:{relationship_type}*]->(a)
                WITH [node in nodes(path) | node.path] as cycle
                RETURN DISTINCT cycle
                LIMIT 20
            """)

            return [record["cycle"] for record in result]

    def get_critical_nodes(self, min_dependents: int = 3, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Find nodes with many dependents (breaking these affects many files).
        High centrality = critical infrastructure.
        """
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)<-[:IMPORTS|REFERENCES|USES*1..2]-(dependent)
                WITH n, count(DISTINCT dependent) as dependents
                WHERE dependents >= $min_deps
                RETURN n.path as path,
                       labels(n)[0] as type,
                       dependents
                ORDER BY dependents DESC
                LIMIT $limit
            """, min_deps=min_dependents, limit=limit)

            return [dict(record) for record in result]

    def get_orphaned_docs(self) -> List[str]:
        """Find documentation files not referenced by anything."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (d:DocFile)
                WHERE NOT (d)-[:REFERENCES]->() AND NOT ()-[:REFERENCES]->(d)
                RETURN d.path as path
                ORDER BY path
            """)

            return [record["path"] for record in result]

    def shortest_path(self, from_path: str, to_path: str) -> Optional[List[str]]:
        """Find shortest dependency path between two nodes."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (from {path: $from})
                MATCH (to {path: $to})
                MATCH path = shortestPath((from)-[*]-(to))
                RETURN [node in nodes(path) | node.path] as path_nodes
            """, **{"from": from_path, "to": to_path})

            record = result.single()
            return record["path_nodes"] if record else None

    # ========== UTILITY ==========

    def clear_all(self):
        """Clear entire graph (DANGEROUS - use with caution)."""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def get_stats(self) -> Dict[str, int]:
        """Get graph statistics."""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)
                RETURN labels(n)[0] as label, count(n) as count
            """)

            stats = {record["label"]: record["count"] for record in result}

            # Count relationships
            rel_result = session.run("""
                MATCH ()-[r]->()
                RETURN type(r) as rel_type, count(r) as count
            """)

            stats["_relationships"] = {record["rel_type"]: record["count"] for record in rel_result}

            return stats


if __name__ == "__main__":
    # Test connection
    with GraphDB() as db:
        print("[TEST] Initializing schema...")
        db.initialize_schema()

        print("[TEST] Creating test nodes...")
        db.create_code_file("src/test.py", name="test.py", language="python")
        db.create_code_file("src/main.py", name="main.py", language="python")
        db.create_import("src/main.py", "src/test.py")

        print("[TEST] Getting stats...")
        stats = db.get_stats()
        print(stats)

        print("[TEST] Impact analysis...")
        impact = db.impact_analysis("src/test.py")
        print(f"Files affected: {len(impact)}")

        print("[OK] Neo4j connection successful!")
