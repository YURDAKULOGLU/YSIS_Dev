"""
Lesson Engine
Parses historical lessons and synthesizes automated rules for the factory.
Enables self-supervised evolution.
"""

import json
from pathlib import Path
from src.agentic.core.utils.logging_utils import log_event
from typing import List, Dict

LESSONS_FILE = Path("Knowledge/Reports/lessons.jsonl")
RULES_FILE = Path("docs/governance/AUTO_RULES.md")

class LessonEngine:
    def __init__(self):
        pass

    def load_lessons(self) -> List[Dict]:
        if not LESSONS_FILE.exists():
            return []
        
        lessons = []
        with open(LESSONS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    lessons.append(json.loads(line))
        return lessons

    def generate_rules(self):
        """Analyze lessons and update AUTO_RULES.md"""
        lessons = self.load_lessons()
        if not lessons:
            return

        # Simple grouping by category for now
        # Future: Use LLM to generalize rules
        categories = {}
        for l in lessons:
            cat = l.get("category", "General")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(l.get("lesson", ""))

        content = "# 🤖 Auto-Generated Governance Rules\n\n"
        content += "> **DO NOT EDIT MANUALLY.** This file is updated by the Lesson Engine.\n"
        content += "> Based on past failures and successes.\n\n"

        for cat, rule_list in categories.items():
            content += f"## {cat}\n"
            for rule in set(rule_list): # Deduplicate
                content += f"- **Rule:** {rule}\n"
            content += "\n"

        RULES_FILE.parent.mkdir(parents=True, exist_ok=True)
        RULES_FILE.write_text(content, encoding="utf-8")
        log_event(f"Updated {RULES_FILE}", component="lesson_engine", level="success")

if __name__ == "__main__":
    engine = LessonEngine()
    engine.generate_rules()
