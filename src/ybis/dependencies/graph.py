"""
YBIS Dependency Graph Builder & Analyzer

Tüm proje dosyalarını tarar, bağımlılık graph'ı oluşturur,
değişikliklerin etkisini analiz eder.
"""

import json
import logging
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

from .schema import Dependency, DependencyType, FileNode, FileType, extract_all_dependencies


@dataclass
class ChangeImpact:
    """Bir değişikliğin etkisi"""
    changed_file: str
    directly_affected: list[str]      # Direkt bağımlılar
    indirectly_affected: list[str]    # Transitif bağımlılar
    critical_updates_needed: list[str] # Kritik güncelleme gereken
    suggested_actions: list[str]       # Önerilen aksiyonlar


class DependencyGraph:
    """Proje dependency graph'ı"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.nodes: dict[str, FileNode] = {}
        self.graph_file = project_root / "platform_data" / "dependency_graph.json"

    def scan_project(self, patterns: list[str] = None) -> int:
        """Projeyi tara ve graph'ı oluştur"""
        if patterns is None:
            patterns = [
                "src/**/*.py",
                "docs/**/*.md",
                "tests/**/*.py",
                "configs/**/*.yaml",
                "configs/**/*.json",
                ".claude/**/*.md",
            ]

        file_count = 0

        for pattern in patterns:
            for file_path in self.project_root.glob(pattern):
                if self._should_skip(file_path):
                    continue

                # Always use forward slashes for consistency
                rel_path = str(file_path.relative_to(self.project_root)).replace("\\", "/")
                self._process_file(rel_path, file_path)
                file_count += 1

        # Build reverse dependencies (dependents)
        self._build_reverse_deps()

        return file_count

    def _should_skip(self, path: Path) -> bool:
        """Skip edilecek dosyalar"""
        skip_patterns = [
            "__pycache__",
            ".git",
            "node_modules",
            ".venv",
            "venv",
            ".pytest_cache",
        ]
        return any(p in str(path) for p in skip_patterns)

    def _process_file(self, rel_path: str, abs_path: Path):
        """Tek dosyayı işle"""
        try:
            content = abs_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return

        # Determine file type
        file_type = self._detect_file_type(rel_path)

        # Extract dependencies
        deps = extract_all_dependencies(rel_path, content)

        # Get last modified from git
        last_modified = self._get_git_modified(rel_path)

        # Create node
        self.nodes[rel_path] = FileNode(
            path=rel_path,
            file_type=file_type,
            dependencies=deps,
            last_modified=last_modified,
        )

    def _detect_file_type(self, path: str) -> FileType:
        """Dosya türünü belirle"""
        if path.endswith(".py"):
            if "test" in path.lower():
                return FileType.TEST
            return FileType.CODE_PYTHON
        elif path.endswith(".ts") or path.endswith(".tsx"):
            return FileType.CODE_TYPESCRIPT
        elif path.endswith(".md"):
            return FileType.DOC_MARKDOWN
        elif path.endswith(".yaml") or path.endswith(".yml"):
            return FileType.CONFIG_YAML
        elif path.endswith(".json"):
            return FileType.CONFIG_JSON
        return FileType.CODE_PYTHON

    def _get_git_modified(self, rel_path: str) -> str | None:
        """Git'ten son değişiklik tarihini al"""
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--format=%ci", rel_path],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except Exception:
            pass
        return None

    def _build_reverse_deps(self):
        """Her dosya için kendisine bağımlı olanları bul"""
        for path, node in self.nodes.items():
            for dep in node.dependencies:
                # Normalize target path
                target = self._normalize_path(dep.target)
                if target in self.nodes:
                    self.nodes[target].dependents.append(path)

    def _normalize_path(self, path: str) -> str:
        """Path'i normalize et"""
        # Normalize slashes (Windows vs Unix)
        path = path.replace("\\", "/")
        # Remove leading ./
        path = path.lstrip("./")

        # Direct match
        if path in self.nodes:
            return path

        # Try with backslashes (Windows paths in nodes)
        win_path = path.replace("/", "\\")
        if win_path in self.nodes:
            return win_path

        # Handle relative paths in docs
        if path.startswith("docs/") or path.startswith("src/"):
            # Try both slash types
            if path in self.nodes:
                return path
            win_path = path.replace("/", "\\")
            if win_path in self.nodes:
                return win_path

        # Try common prefixes
        for prefix in ["docs/", "src/", ""]:
            candidate = prefix + path
            if candidate in self.nodes:
                return candidate
            win_candidate = candidate.replace("/", "\\")
            if win_candidate in self.nodes:
                return win_candidate

        return path

    # ========================================================================
    # IMPACT ANALYSIS
    # ========================================================================

    def analyze_change(self, changed_file: str) -> ChangeImpact:
        """Bir dosya değiştiğinde etkiyi analiz et"""
        changed_file = self._normalize_path(changed_file)

        if changed_file not in self.nodes:
            return ChangeImpact(
                changed_file=changed_file,
                directly_affected=[],
                indirectly_affected=[],
                critical_updates_needed=[],
                suggested_actions=["File not in dependency graph"]
            )

        node = self.nodes[changed_file]

        # Direct dependents
        direct = list(node.dependents)

        # Transitive dependents (BFS)
        indirect = []
        visited = set(direct)
        queue = list(direct)

        while queue:
            current = queue.pop(0)
            if current in self.nodes:
                for dep in self.nodes[current].dependents:
                    if dep not in visited:
                        visited.add(dep)
                        indirect.append(dep)
                        queue.append(dep)

        # Critical updates
        critical = []
        for dep_path in direct:
            if dep_path in self.nodes:
                dep_node = self.nodes[dep_path]
                for dep in dep_node.dependencies:
                    if dep.target == changed_file and dep.critical:
                        critical.append(dep_path)

        # Generate suggestions
        suggestions = self._generate_suggestions(changed_file, direct, indirect, critical)

        return ChangeImpact(
            changed_file=changed_file,
            directly_affected=direct,
            indirectly_affected=indirect,
            critical_updates_needed=critical,
            suggested_actions=suggestions,
        )

    def _generate_suggestions(
        self,
        changed: str,
        direct: list[str],
        indirect: list[str],
        critical: list[str]
    ) -> list[str]:
        """Değişiklik için öneriler oluştur"""
        suggestions = []

        if critical:
            suggestions.append(f"CRITICAL: Update these files immediately: {', '.join(critical)}")

        # Doc updates
        doc_deps = [d for d in direct if d.endswith(".md")]
        if doc_deps:
            suggestions.append(f"Update documentation: {', '.join(doc_deps)}")

        # Test updates
        test_deps = [d for d in direct if "test" in d.lower()]
        if test_deps:
            suggestions.append(f"Run/update tests: {', '.join(test_deps)}")

        # Config updates
        config_deps = [d for d in direct if d.endswith((".yaml", ".json"))]
        if config_deps:
            suggestions.append(f"Check configs: {', '.join(config_deps)}")

        if not suggestions:
            suggestions.append("No immediate action required")

        return suggestions

    # ========================================================================
    # STALENESS DETECTION
    # ========================================================================

    def detect_stale_files(self, since_commit: str = "HEAD~10") -> list[tuple[str, str, list[str]]]:
        """Son commit'lerden beri stale olmuş dosyaları bul"""
        # Get changed files
        try:
            result = subprocess.run(
                ["git", "diff", "--name-only", since_commit],
                cwd=self.project_root,
                capture_output=True,
                text=True,
            )
            changed_files = result.stdout.strip().split("\n") if result.stdout.strip() else []
        except Exception:
            changed_files = []

        stale_files = []

        for changed in changed_files:
            if changed in self.nodes:
                impact = self.analyze_change(changed)
                if impact.directly_affected:
                    for affected in impact.directly_affected:
                        stale_files.append((
                            affected,
                            changed,
                            self.nodes[affected].dependencies[0].reason if self.nodes.get(affected) and self.nodes[affected].dependencies else "dependency"
                        ))

        return stale_files

    # ========================================================================
    # PERSISTENCE
    # ========================================================================

    def save(self):
        """Graph'ı dosyaya kaydet"""
        self.graph_file.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "generated_at": datetime.now().isoformat(),
            "file_count": len(self.nodes),
            "nodes": {}
        }

        for path, node in self.nodes.items():
            data["nodes"][path] = {
                "file_type": node.file_type.value,
                "dependencies": [
                    {
                        "target": d.target,
                        "type": d.dep_type.value,
                        "reason": d.reason,
                        "critical": d.critical,
                    }
                    for d in node.dependencies
                ],
                "dependents": node.dependents,
                "last_modified": node.last_modified,
            }

        self.graph_file.write_text(json.dumps(data, indent=2))

    def load(self) -> bool:
        """Graph'ı dosyadan yükle"""
        if not self.graph_file.exists():
            return False

        try:
            data = json.loads(self.graph_file.read_text())
            for path, node_data in data.get("nodes", {}).items():
                self.nodes[path] = FileNode(
                    path=path,
                    file_type=FileType(node_data["file_type"]),
                    dependencies=[
                        Dependency(
                            target=d["target"],
                            dep_type=DependencyType(d["type"]),
                            reason=d.get("reason", ""),
                            critical=d.get("critical", False),
                        )
                        for d in node_data.get("dependencies", [])
                    ],
                    dependents=node_data.get("dependents", []),
                    last_modified=node_data.get("last_modified"),
                )
            return True
        except Exception:
            return False

    # ========================================================================
    # VISUALIZATION
    # ========================================================================

    def to_mermaid(self, focus_file: str = None, max_depth: int = 2) -> str:
        """Mermaid diagram oluştur"""
        lines = ["graph TD"]

        if focus_file and focus_file in self.nodes:
            # Focus mode - sadece bir dosya ve bağımlılıkları
            node = self.nodes[focus_file]
            focus_id = self._to_id(focus_file)

            lines.append(f"    {focus_id}[{Path(focus_file).name}]")
            lines.append(f"    style {focus_id} fill:#f96")

            for dep in node.dependencies[:10]:
                dep_id = self._to_id(dep.target)
                lines.append(f"    {dep_id}[{Path(dep.target).name}]")
                lines.append(f"    {focus_id} --> {dep_id}")

            for dependent in node.dependents[:10]:
                dep_id = self._to_id(dependent)
                lines.append(f"    {dep_id}[{Path(dependent).name}]")
                lines.append(f"    {dep_id} --> {focus_id}")

        else:
            # Full graph (limited)
            shown = set()
            for path, node in list(self.nodes.items())[:50]:
                path_id = self._to_id(path)
                if path_id not in shown:
                    lines.append(f"    {path_id}[{Path(path).name}]")
                    shown.add(path_id)

                for dep in node.dependencies[:5]:
                    dep_id = self._to_id(dep.target)
                    if dep_id not in shown:
                        lines.append(f"    {dep_id}[{Path(dep.target).name}]")
                        shown.add(dep_id)
                    lines.append(f"    {path_id} --> {dep_id}")

        return "\n".join(lines)

    def _to_id(self, path: str) -> str:
        """Path'i mermaid ID'ye çevir"""
        return path.replace("/", "_").replace(".", "_").replace("-", "_")
