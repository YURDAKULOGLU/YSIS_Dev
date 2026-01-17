"""
Staleness Detector
Detects outdated code that may be inconsistent with recent changes.

When a critical file changes, this module identifies dependent files
that may need updating to remain consistent.

Uses both:
- Graph DB: For structural dependencies (imports, references)
- Vector DB: For semantic similarity (similar patterns, concepts)
"""

import os
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field

from src.agentic.core.utils.logging_utils import log_event


@dataclass
class StalenessReport:
    """Report of potentially stale files after a change."""
    trigger_file: str
    trigger_commit: Optional[str]
    timestamp: datetime
    stale_candidates: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class StalenessDetector:
    """
    Detects code that may be outdated after changes.
    
    Strategy:
    1. Track "critical patterns" that when changed, affect dependents
    2. Use Graph DB to find structural dependents
    3. Check last-modified dates for staleness
    4. Generate update recommendations
    """
    
    # Patterns that when changed, likely need propagation
    CRITICAL_PATTERNS = {
        "model_router.py": [
            "Which model to use for LLM calls",
            "Model configuration structure",
            "Provider selection logic"
        ],
        "protocols.py": [
            "Protocol interfaces",
            "Data model schemas",
            "Type definitions"
        ],
        "config.py": [
            "Environment variables",
            "Path configurations",
            "Feature flags"
        ],
        "PROJECT_CONTEXT.md": [
            "Available LLM providers",
            "Project structure",
            "Code patterns"
        ]
    }
    
    def __init__(self, graph_db=None):
        """
        Initialize detector.
        
        Args:
            graph_db: Optional GraphDB instance. Will create if not provided.
        """
        self.graph_db = graph_db
        self._staleness_log_path = Path("Knowledge/Logs/staleness.jsonl")
        self._staleness_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _get_graph_db(self):
        """Lazy load GraphDB."""
        if self.graph_db is None:
            try:
                from src.agentic.infrastructure.graph_db import GraphDB
                self.graph_db = GraphDB()
            except Exception as e:
                log_event(f"GraphDB unavailable: {e}", component="staleness", level="warning")
                return None
        return self.graph_db
    
    def detect_stale_after_change(
        self,
        changed_file: str,
        commit_hash: Optional[str] = None
    ) -> StalenessReport:
        """
        After a file changes, find files that may need updating.
        
        Args:
            changed_file: Path to the file that changed
            commit_hash: Optional git commit hash
            
        Returns:
            StalenessReport with candidates and recommendations
        """
        report = StalenessReport(
            trigger_file=changed_file,
            trigger_commit=commit_hash,
            timestamp=datetime.now()
        )
        
        # 1. Check if this is a critical file
        file_name = Path(changed_file).name
        is_critical = file_name in self.CRITICAL_PATTERNS
        
        if is_critical:
            patterns = self.CRITICAL_PATTERNS[file_name]
            report.recommendations.append(
                f"CRITICAL FILE CHANGED: {file_name} affects {patterns}"
            )
        
        # 2. Get structural dependents from Graph
        db = self._get_graph_db()
        if db:
            try:
                dependents = db.impact_analysis(changed_file, max_depth=2)
                for dep in dependents:
                    report.stale_candidates.append({
                        "file": dep.get("path"),
                        "type": dep.get("type"),
                        "distance": dep.get("distance", 1),
                        "reason": "imports/references changed file",
                        "priority": "HIGH" if dep.get("distance", 1) == 1 else "MEDIUM"
                    })
            except Exception as e:
                log_event(f"Graph analysis failed: {e}", component="staleness", level="warning")
        
        # 3. Check for known pattern dependencies
        if is_critical:
            semantic_deps = self._find_semantic_dependents(file_name)
            for dep in semantic_deps:
                if not any(c["file"] == dep["file"] for c in report.stale_candidates):
                    report.stale_candidates.append(dep)
        
        # 4. Add specific recommendations
        if file_name == "model_router.py":
            report.recommendations.extend([
                "Check all files that call get_model() - they may use old model names",
                "Verify PROJECT_CONTEXT.md is updated with new model info",
                "Update lesson_engine.py if LLM call pattern changed"
            ])
        elif file_name == "protocols.py":
            report.recommendations.extend([
                "All plugins implementing protocols may need updates",
                "Check type hints in dependent files"
            ])
        elif file_name == "config.py":
            report.recommendations.extend([
                "Verify all os.getenv() calls match new config keys",
                "Update docker-compose.yml if env vars changed"
            ])
        
        # 5. Log the detection
        self._log_staleness(report)
        
        return report
    
    def _find_semantic_dependents(self, file_name: str) -> List[Dict[str, Any]]:
        """
        Find files that semantically depend on a critical file.
        These may not have direct imports but use similar patterns.
        """
        dependents = []
        
        # Known semantic dependencies (manually curated for now)
        SEMANTIC_MAP = {
            "model_router.py": [
                ("src/agentic/core/plugins/aider_executor_enhanced.py", "Uses model router for LLM selection"),
                ("src/agentic/core/plugins/simple_planner.py", "Uses model router for planning"),
                ("src/agentic/core/intelligence/lesson_engine.py", "May call LLM directly"),
                ("Knowledge/Context/PROJECT_CONTEXT.md", "Documents available models"),
            ],
            "protocols.py": [
                ("src/agentic/core/plugins/sentinel_enhanced.py", "Implements VerifierProtocol"),
                ("src/agentic/core/plugins/simple_planner.py", "Implements PlannerProtocol"),
                ("src/agentic/core/plugins/aider_executor_enhanced.py", "Implements ExecutorProtocol"),
            ],
            "PROJECT_CONTEXT.md": [
                ("src/agentic/core/plugins/aider_executor_enhanced.py", "Injects this context"),
            ],
        }
        
        if file_name in SEMANTIC_MAP:
            for path, reason in SEMANTIC_MAP[file_name]:
                dependents.append({
                    "file": path,
                    "type": "semantic",
                    "distance": 1,
                    "reason": reason,
                    "priority": "MEDIUM"
                })
        
        return dependents
    
    def check_project_consistency(self) -> Dict[str, Any]:
        """
        Full project consistency check.
        
        Returns:
            Dict with consistency status and issues found
        """
        issues = []
        
        # 1. Check if PROJECT_CONTEXT.md matches reality
        context_path = Path("Knowledge/Context/PROJECT_CONTEXT.md")
        if context_path.exists():
            context = context_path.read_text(encoding="utf-8")
            
            # Check if model_router still uses Ollama
            router_path = Path("src/agentic/core/plugins/model_router.py")
            if router_path.exists():
                router_content = router_path.read_text(encoding="utf-8")
                if "ollama" in router_content.lower() and "ollama" not in context.lower():
                    issues.append({
                        "type": "INCONSISTENCY",
                        "file": str(context_path),
                        "message": "PROJECT_CONTEXT doesn't mention Ollama but model_router uses it"
                    })
        
        # 2. Check for orphaned documentation
        db = self._get_graph_db()
        if db:
            try:
                orphaned = db.get_orphaned_docs()
                for doc in orphaned:
                    issues.append({
                        "type": "ORPHANED_DOC",
                        "file": doc,
                        "message": "Documentation not referenced anywhere"
                    })
            except Exception:
                pass
        
        # 3. Check for circular dependencies
        if db:
            try:
                cycles = db.find_circular_dependencies()
                for cycle in cycles[:5]:  # Limit to 5
                    issues.append({
                        "type": "CIRCULAR_DEPENDENCY",
                        "files": cycle,
                        "message": f"Circular import chain of {len(cycle)} files"
                    })
            except Exception:
                pass
        
        return {
            "status": "CONSISTENT" if not issues else "INCONSISTENT",
            "issues": issues,
            "checked_at": datetime.now().isoformat()
        }
    
    def _log_staleness(self, report: StalenessReport) -> None:
        """Log staleness detection for future learning."""
        entry = {
            "trigger_file": report.trigger_file,
            "trigger_commit": report.trigger_commit,
            "timestamp": report.timestamp.isoformat(),
            "candidates_count": len(report.stale_candidates),
            "recommendations": report.recommendations
        }
        
        with self._staleness_log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    
    def get_update_task(self, report: StalenessReport) -> Optional[Dict[str, Any]]:
        """
        Generate a task to update stale files.
        
        Args:
            report: StalenessReport from detect_stale_after_change
            
        Returns:
            Task dict suitable for YBIS task board, or None if no updates needed
        """
        high_priority = [c for c in report.stale_candidates if c.get("priority") == "HIGH"]
        
        if not high_priority:
            return None
        
        files_to_check = [c["file"] for c in high_priority]
        
        return {
            "goal": f"CONSISTENCY-FIX: Update files affected by {Path(report.trigger_file).name} change",
            "details": f"""
The file {report.trigger_file} was modified.
The following dependent files may need updating:

{chr(10).join(f'- {f}' for f in files_to_check)}

Recommendations:
{chr(10).join(f'- {r}' for r in report.recommendations)}

Check each file for consistency with the changed file.
""",
            "priority": "HIGH",
            "files_to_modify": files_to_check,
            "metadata": {
                "trigger": report.trigger_file,
                "auto_generated": True,
                "staleness_detection": True
            }
        }


if __name__ == "__main__":
    # Test staleness detection
    detector = StalenessDetector()
    
    print("=== Testing Staleness Detection ===")
    report = detector.detect_stale_after_change("src/agentic/core/plugins/model_router.py")
    
    print(f"\nTrigger: {report.trigger_file}")
    print(f"Stale candidates: {len(report.stale_candidates)}")
    
    for candidate in report.stale_candidates:
        print(f"  - {candidate['file']} ({candidate['priority']}): {candidate['reason']}")
    
    print(f"\nRecommendations:")
    for rec in report.recommendations:
        print(f"  - {rec}")
    
    print("\n=== Testing Consistency Check ===")
    consistency = detector.check_project_consistency()
    print(f"Status: {consistency['status']}")
    print(f"Issues: {len(consistency['issues'])}")
    for issue in consistency['issues'][:5]:
        print(f"  - [{issue['type']}] {issue.get('message', '')}")

