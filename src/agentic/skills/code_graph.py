"""
Code Graph Skill
Parses Python code into a Knowledge Graph structure using Tree-Sitter.
Extracts Classes, Functions, and Calls.
"""

import os
from pathlib import Path
from typing import List, Dict, Any, Tuple
from tree_sitter_languages import get_language, get_parser

class CodeGraphParser:
    def __init__(self):
        self.language = get_language("python")
        self.parser = get_parser("python")

    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a python file and return AST nodes."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            
            tree = self.parser.parse(bytes(code, "utf8"))
            root = tree.root_node
            
            classes = self._extract_classes(root, file_path)
            functions = self._extract_functions(root, file_path)
            # calls = self._extract_calls(root) # Advanced: Future scope
            
            return {
                "file_path": file_path,
                "classes": classes,
                "functions": functions,
                "code": code
            }
        except Exception as e:
            print(f"[ERROR] Failed to parse {file_path}: {e}")
            return {}

    def _extract_classes(self, node, file_path) -> List[Dict]:
        classes = []
        # Query for class definitions
        query = self.language.query("""
        (class_definition
            name: (identifier) @name
        ) @class
        """ ) # Removed unnecessary escape for newline
        
        captures = query.captures(node)
        for capture in captures:
            if capture[1] == "name":
                class_name = capture[0].text.decode("utf8")
                classes.append({
                    "name": class_name,
                    "id": f"{file_path}::{class_name}",
                    "type": "Class"
                })
        return classes

    def _extract_functions(self, node, file_path) -> List[Dict]:
        functions = []
        # Query for function definitions
        query = self.language.query("""
        (function_definition
            name: (identifier) @name
        ) @function
        """ ) # Removed unnecessary escape for newline
        
        captures = query.captures(node)
        for capture in captures:
            if capture[1] == "name":
                func_name = capture[0].text.decode("utf8")
                functions.append({
                    "name": func_name,
                    "id": f"{file_path}::{func_name}",
                    "type": "Function"
                })
        return functions

# --- Neo4j Integration ---

from src.agentic.infrastructure.graph_db import GraphDB

class CodeGraphIngestor:
    def __init__(self):
        self.parser = CodeGraphParser()

    def ingest_directory(self, root_dir: str):
        """Walk directory and ingest all python files."""
        print(f"🚀 Ingesting Code Graph from: {root_dir}")
        count = 0
        
        # Verify DB connection first
        try:
            with GraphDB() as db:
                db.driver.verify_connectivity()
        except Exception as e:
            print(f"❌ Neo4j not available: {e}")
            return

        path_obj = Path(root_dir)
        for file_path in path_obj.rglob("*.py"):
            # Skip ignored dirs
            if any(part.startswith(".") or part == "__pycache__" for part in file_path.parts):
                continue
                
            data = self.parser.parse_file(str(file_path))
            if data:
                self._save_to_graph(data)
                count += 1
                if count % 10 == 0:
                    print(f"   Processed {count} files...")
        
        print(f"✅ Ingestion Complete. {count} files processed.")

    def _save_to_graph(self, data: Dict):
        """Save parsed data to Neo4j."""
        file_path = data["file_path"].replace("\\", "/")
        
        # Use a fresh connection for each file to ensure safe closing
        with GraphDB() as db:
            # 1. Create File Node
            db.driver.execute_query("""
                MERGE (f:CodeFile {path: $path})
                SET f.language = 'python'
            """, path=file_path)
            
            # 2. Create Class Nodes & Relations
            for cls in data.get("classes", []):
                db.driver.execute_query("""
                    MERGE (c:Class {id: $id})
                    SET c.name = $name
                    WITH c
                    MATCH (f:CodeFile {path: $path})
                    MERGE (c)-[:DEFINED_IN]->(f)
                """, id=cls["id"], name=cls["name"], path=file_path)
                
            # 3. Create Function Nodes & Relations
            for func in data.get("functions", []):
                db.driver.execute_query("""
                    MERGE (fn:Function {id: $id})
                    SET fn.name = $name
                    WITH fn
                    MATCH (f:CodeFile {path: $path})
                    MERGE (fn)-[:DEFINED_IN]->(f)
                """, id=func["id"], name=func["name"], path=file_path)
