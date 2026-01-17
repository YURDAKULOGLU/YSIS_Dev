"""
Lesson Engine
Parses historical lessons and synthesizes automated rules for the factory.
Enables self-supervised evolution.

CONSTITUTION COMPLIANT: Local-First (Ollama), with graceful fallback.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional
import requests

from src.agentic.core.utils.logging_utils import log_event

LESSONS_FILE = Path("Knowledge/Logs/lessons.jsonl")
RULES_FILE = Path("docs/governance/AUTO_RULES.md")
OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")


class LessonEngine:
    """
    LLM-powered lesson analysis engine.
    Uses LOCAL Ollama first (Constitution: Local-First principle).
    Falls back to simple text analysis if Ollama unavailable.
    """

    def __init__(self):
        self.model = os.getenv("YBIS_LESSON_MODEL", "qwen2.5-coder:7b")
        self.ollama_available = self._check_ollama()
        
        if not self.ollama_available:
            log_event(
                "Ollama not available - falling back to simple analysis",
                component="lesson_engine",
                level="warning"
            )

    def _check_ollama(self) -> bool:
        """Check if Ollama is running and accessible."""
        try:
            response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def _call_llm(self, prompt: str) -> Optional[str]:
        """Call local Ollama LLM. Returns None if unavailable."""
        if not self.ollama_available:
            return None
        
        try:
            response = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=60
            )
            if response.status_code == 200:
                return response.json().get("response", "")
        except Exception as e:
            log_event(f"LLM call failed: {e}", component="lesson_engine", level="warning")
        
        return None

    def load_lessons(self) -> List[Dict]:
        """Load lessons from JSONL file."""
        if not LESSONS_FILE.exists():
            return []

        lessons = []
        with open(LESSONS_FILE, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        lessons.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return lessons

    def generate_postmortem(self, lesson: Dict) -> str:
        """Generate a postmortem using local LLM or simple analysis."""
        prompt = (
            "Analyze this task failure and provide a brief postmortem:\n\n"
            f"Task ID: {lesson.get('task_id', 'unknown')}\n"
            f"Status: {lesson.get('status', 'unknown')}\n"
            f"Final Status: {lesson.get('final_status', 'unknown')}\n"
            f"Errors: {', '.join(lesson.get('errors', []))}\n\n"
            "Provide: 1) Root cause 2) Fix suggestion"
        )

        llm_response = self._call_llm(prompt)
        if llm_response:
            return llm_response

        # Fallback: Simple text-based analysis
        errors = lesson.get('errors', [])
        if errors:
            return f"Errors detected: {'; '.join(errors[:3])}"
        return "No detailed analysis available (Ollama offline)"

    def cluster_errors(self, lessons: List[Dict]) -> Dict[str, List[str]]:
        """Cluster similar errors. Uses LLM if available, else simple grouping."""
        # Simple fallback: Group by error signature
        clusters: Dict[str, List[str]] = {}
        
        for lesson in lessons:
            errors = lesson.get('errors', [])
            task_id = lesson.get('task_id', 'unknown')
            
            for error in errors:
                # Simple signature: first 50 chars
                signature = error[:50] if len(error) > 50 else error
                if signature not in clusters:
                    clusters[signature] = []
                clusters[signature].append(task_id)
        
        # If LLM available, try to get better clustering
        if self.ollama_available and clusters:
            prompt = (
                "Group these error signatures into logical categories:\n"
                f"{list(clusters.keys())}\n"
                "Return JSON: {{'category_name': ['signature1', 'signature2']}}"
            )
            llm_response = self._call_llm(prompt)
            if llm_response:
                try:
                    return json.loads(llm_response)
                except json.JSONDecodeError:
                    pass
        
        return clusters

    def propose_rules(self, clusters: Dict[str, List[str]]) -> List[Dict]:
        """Propose rules based on error clusters."""
        proposed_rules = []
        
        for cluster_id, items in clusters.items():
            rule = {
                "cluster_id": cluster_id[:30],
                "occurrences": len(items) if isinstance(items, list) else 1,
                "confidence_score": min(1.0, len(items) * 0.2) if isinstance(items, list) else 0.5,
                "rule": f"Prevent: {cluster_id[:50]}"
            }
            
            # Try to get better rule from LLM
            if self.ollama_available:
                prompt = f"Suggest a rule to prevent this error: {cluster_id}"
                llm_response = self._call_llm(prompt)
                if llm_response:
                    rule["rule"] = llm_response[:200]
            
            proposed_rules.append(rule)
        
        return proposed_rules

    def detect_regression(self, lessons: List[Dict]) -> List[str]:
        """Detect recurring error patterns (regression)."""
        error_counts: Dict[str, int] = {}
        
        for lesson in lessons:
            signature = lesson.get('signature', '')
            if signature:
                error_counts[signature] = error_counts.get(signature, 0) + 1
        
        # Regression = same error 3+ times
        regressions = [sig for sig, count in error_counts.items() if count >= 3]
        return regressions

    def generate_rules(self) -> None:
        """Analyze lessons and update AUTO_RULES.md"""
        lessons = self.load_lessons()
        if not lessons:
            log_event("No lessons to analyze", component="lesson_engine")
            return

        # Generate postmortems for failed lessons
        for lesson in lessons:
            if lesson.get('final_status') == 'FAILED':
                lesson['postmortem'] = self.generate_postmortem(lesson)

        # Cluster errors
        clusters = self.cluster_errors(lessons)

        # Propose rules based on clusters
        proposed_rules = self.propose_rules(clusters)

        # Detect regressions
        regressions = self.detect_regression(lessons)

        # Group by category
        categories: Dict[str, List[str]] = {}
        for lesson in lessons:
            cat = lesson.get("category", "General")
            if cat not in categories:
                categories[cat] = []
            if lesson.get("lesson"):
                categories[cat].append(lesson["lesson"])

        # Generate markdown output
        content = "# Auto-Generated Governance Rules\n\n"
        content += "> **DO NOT EDIT MANUALLY.** This file is updated by the Lesson Engine.\n"
        content += "> Based on past failures and successes.\n\n"

        if regressions:
            content += "## REGRESSIONS DETECTED\n"
            for reg in regressions:
                content += f"- **RECURRING:** {reg}\n"
            content += "\n"

        for cat, rule_list in categories.items():
            content += f"## {cat}\n"
            for rule in set(rule_list):  # Deduplicate
                content += f"- **Rule:** {rule}\n"
            content += "\n"

        # Add proposed rules
        if proposed_rules:
            content += "## Proposed Rules (Auto-Generated)\n"
            for rule in proposed_rules:
                content += f"- **{rule['cluster_id']}**\n"
                content += f"  - Rule: {rule['rule']}\n"
                content += f"  - Confidence: {rule['confidence_score']:.2f}\n"
                content += f"  - Occurrences: {rule['occurrences']}\n\n"

        RULES_FILE.parent.mkdir(parents=True, exist_ok=True)
        RULES_FILE.write_text(content, encoding="utf-8")
        log_event(f"Updated {RULES_FILE}", component="lesson_engine", level="success")


if __name__ == "__main__":
    engine = LessonEngine()
    engine.generate_rules()
