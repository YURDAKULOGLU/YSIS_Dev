"""
YBIS Universal Dependency Schema

Her dosya (kod, doküman, config) bağımlılıklarını declare edebilir.
Bu sistem değişikliklerin etkisini analiz eder.
"""

import logging
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


class DependencyType(Enum):
    """Bağımlılık türleri"""
    IMPORTS = "imports"           # Python/JS imports
    REFERENCES = "references"     # Doküman referansları
    IMPLEMENTS = "implements"     # Spec'i implement eder
    TESTS = "tests"              # Bu dosyayı test eder
    CONFIGURES = "configures"    # Config dosyası
    EXTENDS = "extends"          # Base class/interface
    USES_SCHEMA = "uses_schema"  # Schema/contract kullanır
    DOCUMENTS = "documents"      # Bu kodu dokümante eder


class FileType(Enum):
    """Dosya türleri"""
    CODE_PYTHON = "python"
    CODE_TYPESCRIPT = "typescript"
    DOC_MARKDOWN = "markdown"
    CONFIG_YAML = "yaml"
    CONFIG_JSON = "json"
    SCHEMA = "schema"
    TEST = "test"


@dataclass
class Dependency:
    """Tek bir bağımlılık"""
    target: str                    # Bağımlı olunan dosya
    dep_type: DependencyType       # Bağımlılık türü
    reason: str = ""               # Neden bağımlı
    critical: bool = False         # Kritik mi (değişince kesin güncelle)


@dataclass
class FileNode:
    """Dependency graph'ta bir dosya"""
    path: str
    file_type: FileType
    dependencies: list[Dependency] = field(default_factory=list)
    dependents: list[str] = field(default_factory=list)  # Bu dosyaya bağımlı olanlar
    last_modified: str | None = None
    staleness: str = "fresh"  # fresh, stale, critical_stale


# ============================================================================
# FRONTMATTER PARSER
# ============================================================================

FRONTMATTER_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL)

def parse_frontmatter(content: str) -> dict:
    """Dosyanın başındaki YAML frontmatter'ı parse et"""
    match = FRONTMATTER_PATTERN.match(content)
    if match:
        try:
            return yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            return {}
    return {}


def extract_dependencies_from_frontmatter(content: str) -> list[Dependency]:
    """Frontmatter'dan bağımlılıkları çıkar"""
    fm = parse_frontmatter(content)
    deps = []

    # depends_on field
    if "depends_on" in fm:
        for dep in fm["depends_on"]:
            if isinstance(dep, str):
                deps.append(Dependency(target=dep, dep_type=DependencyType.REFERENCES))
            elif isinstance(dep, dict):
                deps.append(Dependency(
                    target=dep.get("file", ""),
                    dep_type=DependencyType(dep.get("type", "references")),
                    reason=dep.get("reason", ""),
                    critical=dep.get("critical", False)
                ))

    # implements field (for code files)
    if "implements" in fm:
        for spec in fm["implements"]:
            deps.append(Dependency(
                target=spec,
                dep_type=DependencyType.IMPLEMENTS,
                critical=True
            ))

    # tests field
    if "tests" in fm:
        for test_target in fm["tests"]:
            deps.append(Dependency(
                target=test_target,
                dep_type=DependencyType.TESTS
            ))

    return deps


# ============================================================================
# CODE PARSER (Python imports)
# ============================================================================

PYTHON_IMPORT_PATTERN = re.compile(
    r'^(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))',
    re.MULTILINE
)

def extract_python_imports(content: str, file_path: str) -> list[Dependency]:
    """Python dosyasından import'ları çıkar"""
    deps = []

    # Normalize file_path to Path
    file_path_obj = Path(file_path)

    for match in PYTHON_IMPORT_PATTERN.finditer(content):
        module = match.group(1) or match.group(2)

        # Local imports only (src.ybis.* or relative imports)
        if module.startswith(("src.", "ybis.", ".")):
            # Handle relative imports (e.g., "..contracts", ".utils")
            if module.startswith("."):
                # Count leading dots to determine relative level
                dots = len(module) - len(module.lstrip("."))
                module_name = module.lstrip(".")

                # Resolve relative import from current file's directory
                current_dir = file_path_obj.parent
                for _ in range(dots - 1):
                    current_dir = current_dir.parent

                # Convert module name to path
                if module_name:
                    module_parts = module_name.split(".")
                    target_path = current_dir / "/".join(module_parts)
                else:
                    target_path = current_dir

                # Try __init__.py first, then .py file
                if module_name:
                    init_path = target_path / "__init__.py"
                    py_path = target_path.with_suffix(".py")
                    if init_path.exists():
                        target_path = init_path
                    elif py_path.exists():
                        target_path = py_path
                    else:
                        # Fallback: assume .py file
                        target_path = target_path.with_suffix(".py")
                else:
                    # Just dots (from . import) - use __init__.py
                    target_path = target_path / "__init__.py"

                # Normalize to relative path from project root
                try:
                    from ...constants import PROJECT_ROOT
                    module_path = str(target_path.relative_to(PROJECT_ROOT))
                except ValueError:
                    # If not under project root, use absolute path
                    module_path = str(target_path)
            else:
                # Absolute import (src.ybis.*)
                module_path = module.replace(".", "/") + ".py"

            deps.append(Dependency(
                target=module_path,
                dep_type=DependencyType.IMPORTS,
                reason=f"Python import: {module}"
            ))

    return deps


# ============================================================================
# MARKDOWN LINK PARSER
# ============================================================================

MD_LINK_PATTERN = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
MD_REFERENCE_PATTERN = re.compile(r'`([^`]+\.(py|ts|md|yaml|json))`')

def extract_markdown_references(content: str) -> list[Dependency]:
    """Markdown dosyasından referansları çıkar"""
    deps = []

    # [text](link) format
    for match in MD_LINK_PATTERN.finditer(content):
        link = match.group(2)
        if not link.startswith(("http://", "https://", "#")):
            deps.append(Dependency(
                target=link,
                dep_type=DependencyType.REFERENCES,
                reason=f"Markdown link: {match.group(1)}"
            ))

    # `file.py` format
    for match in MD_REFERENCE_PATTERN.finditer(content):
        deps.append(Dependency(
            target=match.group(1),
            dep_type=DependencyType.REFERENCES,
            reason="Inline code reference"
        ))

    return deps


# ============================================================================
# UNIFIED EXTRACTOR
# ============================================================================

def extract_all_dependencies(file_path: str, content: str) -> list[Dependency]:
    """Dosya türüne göre tüm bağımlılıkları çıkar"""
    deps = []

    # 1. Frontmatter (tüm dosyalar)
    deps.extend(extract_dependencies_from_frontmatter(content))

    # 2. Type-specific extraction
    if file_path.endswith(".py"):
        deps.extend(extract_python_imports(content, file_path))

    elif file_path.endswith(".md"):
        deps.extend(extract_markdown_references(content))

    # Deduplicate
    seen = set()
    unique_deps = []
    for dep in deps:
        key = (dep.target, dep.dep_type)
        if key not in seen:
            seen.add(key)
            unique_deps.append(dep)

    return unique_deps
