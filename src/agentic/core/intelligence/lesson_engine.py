"""
Lesson Engine
Parses historical lessons and synthesizes automated rules for the factory.
Enables self-supervised evolution.
"""

import json
import os  # Import the os module to use os.getenv
from pathlib import Path

import openai  # Assuming OpenAI's GPT model is used

from src.agentic.core.utils.logging_utils import log_event

LESSONS_FILE = Path("Knowledge/Reports/lessons.jsonl")
RULES_FILE = Path("docs/governance/AUTO_RULES.md")

class LessonEngine:
    def __init__(self):
        self.llm_model = "gpt-3.5-turbo"  # Specify the LLM model to use
        self.openai_api_key = os.getenv("OPENAI_API_KEY")  # Ensure API key is set in environment

        if not self.openai_api_key:
            raise ValueError("OpenAI API key not found in environment variables")

        openai.api_key = self.openai_api_key

    def load_lessons(self) -> list[dict]:
        if not LESSONS_FILE.exists():
            return []

        lessons = []
        with open(LESSONS_FILE, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    lessons.append(json.loads(line))
        return lessons

    def generate_postmortem(self, lesson: dict) -> str:
        """Generate a postmortem using the LLM."""
        prompt = (
            "Analyze the following task failure and provide a detailed postmortem:\n\n"
            f"Task ID: {lesson['task_id']}\n"
            f"Status: {lesson['status']}\n"
            f"Final Status: {lesson['final_status']}\n"
            f"Errors: {', '.join(lesson.get('errors', []))}\n"
        )

        response = openai.ChatCompletion.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()

    def cluster_errors(self, lessons: list[dict]) -> dict:
        """Cluster similar errors using the LLM."""
        error_texts = [', '.join(lesson.get('errors', [])) for lesson in lessons]
        prompt = (
            "Cluster the following error texts into groups of similar issues:\n\n"
            f"{error_texts}\n"
        )

        response = openai.ChatCompletion.create(
            model=self.llm_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return json.loads(response.choices[0].message['content'].strip())

    def propose_rules(self, clusters: dict) -> list[dict]:
        """Propose rules with confidence scores based on error clusters."""
        proposed_rules = []
        for cluster_id, errors in clusters.items():
            prompt = (
                "Based on the following clustered errors, propose a rule to prevent similar issues:\n\n"
                f"Cluster ID: {cluster_id}\n"
                f"Errors: {errors}\n"
            )

            response = openai.ChatCompletion.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            rule_content = response.choices[0].message['content'].strip()
            proposed_rules.append({
                "cluster_id": cluster_id,
                "rule": rule_content,
                "confidence_score": 1.0  # Placeholder for confidence score logic
            })
        return proposed_rules

    def generate_rules(self):
        """Analyze lessons and update AUTO_RULES.md"""
        lessons = self.load_lessons()
        if not lessons:
            return

        # Generate postmortems for each lesson
        for lesson in lessons:
            lesson['postmortem'] = self.generate_postmortem(lesson)

        # Cluster errors
        clusters = self.cluster_errors(lessons)

        # Propose rules based on clusters
        proposed_rules = self.propose_rules(clusters)

        # Simple grouping by category for now
        categories = {}
        for lesson in lessons:
            cat = lesson.get("category", "General")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(lesson.get("lesson", ""))

        content = "# 🤖 Auto-Generated Governance Rules\n\n"
        content += "> **DO NOT EDIT MANUALLY.** This file is updated by the Lesson Engine.\n"
        content += "> Based on past failures and successes.\n\n"

        for cat, rule_list in categories.items():
            content += f"## {cat}\n"
            for rule in set(rule_list):  # Deduplicate
                content += f"- **Rule:** {rule}\n"
            content += "\n"

        # Add proposed rules
        content += "## Proposed Rules\n"
        for rule in proposed_rules:
            content += f"- **Cluster ID:** {rule['cluster_id']}\n"
            content += f"  - **Rule:** {rule['rule']}\n"
            content += f"  - **Confidence Score:** {rule['confidence_score']:.2f}\n\n"

        RULES_FILE.parent.mkdir(parents=True, exist_ok=True)
        RULES_FILE.write_text(content, encoding="utf-8")
        log_event(f"Updated {RULES_FILE}", component="lesson_engine", level="success")

if __name__ == "__main__":
    engine = LessonEngine()
    engine.generate_rules()
