#!/usr/bin/env python3
"""
YBIS Dependency Graph Ingestion
Scans codebase and documentation, populates Neo4j graph.
"""

import ast
import sys
import re
from pathlib import Path
from typing import Set, List, Dict
import frontmatter

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agentic.infrastructure.graph_db import GraphDB


class DependencyScanner:
    """Scan codebase and build dependency graph."""

    def __init__(self):
        self.db = GraphDB()
        self.base_path = Path(".")

    def scan_all(self):
        """Full scan: code + docs."""
        print("[INFO] Initializing graph schema...")
        self.db.initialize_schema()

        print("[INFO] Scanning Python code...")
        self.scan_python_code()

        print("[INFO] Scanning documentation...")
        self.scan_documentation()

        print("[INFO] Linking docs to code...")
        self.link_docs_to_code()

        print("[SUCCESS] Graph ingestion complete")
        self._print_stats()

    def scan_python_code(self):
        """Scan all Python files, extract imports and structure."""
        # Scan ALL Python directories, not just src/
        python_files = []
        for scan_dir in ["src", "scripts", "tests", "workspaces/sub_factory"]:
            if Path(scan_dir).exists():
                python_files.extend(Path(scan_dir).rglob("*.py"))

        for i, py_file in enumerate(python_files, 1):
            print(f"  [{i}/{len(python_files)}] {py_file}", end="\r")

            try:
                # Read file
                content = py_file.read_text(encoding='utf-8')

                # Parse AST
                tree = ast.parse(content)

                # Create CodeFile node
                self.db.create_code_file(
                    path=str(py_file),
                    name=py_file.name,
                    extension=".py",
                    language="python",
                    lines_of_code=len(content.splitlines())
                )

                # Extract imports
                imports = self._extract_imports(tree, py_file)
                for imp in imports:
                    self.db.create_import(str(py_file), imp)

                # Extract functions and classes
                self._extract_definitions(tree, py_file)

            except Exception as e:
                print(f"\n[WARN] Failed to parse {py_file}: {e}")

        print("\n")

    def _extract_imports(self, tree: ast.AST, current_file: Path) -> Set[str]:
        """Extract import statements and resolve to file paths."""
        imports = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Convert module name to potential file path
                    module_path = alias.name.replace('.', '/')

                    # Check if module starts with 'src' (internal import)
                    if alias.name.startswith('src.'):
                        potential_file = Path(f"{module_path}.py")
                    else:
                        potential_file = Path(f"src/{module_path}.py")

                    if potential_file.exists():
                        imports.add(str(potential_file))

            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    # Relative imports
                    if node.level > 0:
                        # Handle relative imports (from ..module import)
                        parent_parts = current_file.parent.parts[node.level:]
                        module_path = '/'.join(parent_parts)
                        if node.module:
                            module_path += '/' + node.module.replace('.', '/')
                    else:
                        module_path = node.module.replace('.', '/')

                    # Check if module starts with 'src' (internal import)
                    if node.module and node.module.startswith('src.'):
                        potential_file = Path(f"{module_path}.py")
                    else:
                        potential_file = Path(f"src/{module_path}.py")

                    if potential_file.exists():
                        imports.add(str(potential_file))

        return imports

    def _extract_definitions(self, tree: ast.AST, file_path: Path):
        """Extract function and class definitions."""
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                qname = f"{file_path.stem}.{node.name}"

                self.db.create_function(
                    qualified_name=qname,
                    file_path=str(file_path),
                    name=node.name,
                    line_start=node.lineno,
                    line_end=node.end_lineno or node.lineno,
                    is_async=isinstance(node, ast.AsyncFunctionDef)
                )

                self.db.create_defines(str(file_path), qname, "Function")

            elif isinstance(node, ast.ClassDef):
                qname = f"{file_path.stem}.{node.name}"

                self.db.create_class(
                    qualified_name=qname,
                    file_path=str(file_path),
                    name=node.name,
                    line_start=node.lineno
                )

                self.db.create_defines(str(file_path), qname, "Class")

    def scan_documentation(self):
        """Scan markdown documentation."""
        doc_files = list(Path("docs").rglob("*.md"))
        doc_files.extend(Path(".").glob("*.md"))  # Root-level docs

        for i, doc_file in enumerate(doc_files, 1):
            print(f"  [{i}/{len(doc_files)}] {doc_file}", end="\r")

            try:
                # Parse frontmatter + content
                with open(doc_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)

                # Get section (docs/specs, docs/governance, etc)
                section = str(doc_file.parent) if doc_file.parent != Path(".") else "root"

                # Create DocFile node
                self.db.create_doc_file(
                    path=str(doc_file),
                    name=doc_file.name,
                    section=section,
                    word_count=len(post.content.split())
                )

                # Extract markdown links
                links = self._extract_markdown_links(post.content)
                for link in links:
                    resolved = self._resolve_doc_link(doc_file, link)
                    if resolved:
                        self.db.create_reference(str(doc_file), str(resolved), "markdown_link")

            except Exception as e:
                print(f"\n[WARN] Failed to parse {doc_file}: {e}")

        print("\n")

    def _extract_markdown_links(self, content: str) -> List[str]:
        """Extract markdown links from content."""
        # Match [text](link.md) or [text](path/to/file.py)
        pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        matches = re.findall(pattern, content)
        return [link for _, link in matches if link.endswith(('.md', '.py'))]

    def _resolve_doc_link(self, source_file: Path, link: str) -> Path:
        """Resolve relative markdown link to absolute path."""
        if link.startswith('http'):
            return None  # External link

        # Resolve relative to source file
        target = (source_file.parent / link).resolve()

        if target.exists():
            return target

        return None

    def link_docs_to_code(self):
        """Create references from docs to code files (via backtick refs)."""
        # Scan docs for references to code files
        doc_files = list(Path("docs").rglob("*.md"))
        doc_files.extend(Path(".").glob("*.md"))
        doc_files.extend(Path("agents").rglob("*.md"))
        doc_files.extend(Path("Knowledge").rglob("*.md"))
        
        # Patterns to find code references in docs (both slash formats)
        patterns = [
            r'`(src[/\\][^`]+\.py)`',           # `src/path/file.py` or `src\path\file.py`
            r'`(scripts[/\\][^`]+\.py)`',       # `scripts/file.py`
            r'`(tests[/\\][^`]+\.py)`',         # `tests/file.py`
            r'\*\*(src[/\\][^\*]+\.py)\*\*',    # **src/path/file.py**
            r'(?:^|\s)(src[/\\]\S+\.py)',       # src/path/file.py (plain text)
        ]
        
        refs_created = 0
        for doc_file in doc_files:
            try:
                content = doc_file.read_text(encoding='utf-8')
                
                for pattern in patterns:
                    matches = re.findall(pattern, content)
                    for match in matches:
                        # Normalize ALL paths to use backslash (Windows) for consistency with Neo4j
                        code_path = match.replace('/', '\\')
                        doc_path = str(doc_file).replace('/', '\\')
                        
                        # Check if code file exists
                        if Path(code_path).exists():
                            self.db.create_reference(doc_path, code_path, "code_reference")
                            refs_created += 1
                            
            except Exception as e:
                pass  # Skip unreadable files
        
        print(f"  Created {refs_created} doc-to-code references")

    def scan_function_calls(self):
        """Scan function calls to create USES relationships."""
        # This is a simplified version - full call graph is complex
        # We focus on important patterns
        
        python_files = []
        for scan_dir in ["src", "scripts"]:
            if Path(scan_dir).exists():
                python_files.extend(Path(scan_dir).rglob("*.py"))
        
        uses_created = 0
        for py_file in python_files:
            try:
                content = py_file.read_text(encoding='utf-8')
                tree = ast.parse(content)
                
                # Get all function calls
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        # Handle attribute calls like self.method() or module.func()
                        if isinstance(node.func, ast.Attribute):
                            func_name = node.func.attr
                            # Try to resolve the caller
                            if isinstance(node.func.value, ast.Name):
                                caller = node.func.value.id
                                # Look for functions with this name
                                self._create_uses_if_exists(str(py_file), f"{caller}.{func_name}")
                                uses_created += 1
                        # Handle direct calls like func()
                        elif isinstance(node.func, ast.Name):
                            func_name = node.func.id
                            self._create_uses_if_exists(str(py_file), func_name)
                            uses_created += 1
                            
            except Exception:
                pass  # Skip unparseable files
        
        print(f"  Created {uses_created} function call links")
    
    def _create_uses_if_exists(self, from_file: str, func_name: str):
        """Create USES relationship if function exists in graph."""
        # We can't directly check Neo4j for every call (too slow)
        # So we just record the call pattern - analysis can be done later
        pass  # Placeholder for now - full implementation needs batch processing
    
    def _print_stats(self):
        """Print graph statistics."""
        stats = self.db.get_stats()

        print("\n[GRAPH STATS]")
        for label, count in sorted(stats.items()):
            if label != "_relationships":
                print(f"  {label}: {count}")

        if "_relationships" in stats:
            print("\n[RELATIONSHIPS]")
            for rel_type, count in sorted(stats["_relationships"].items()):
                print(f"  {rel_type}: {count}")


def main():
    scanner = DependencyScanner()

    try:
        scanner.scan_all()
    finally:
        scanner.db.close()


if __name__ == "__main__":
    main()
