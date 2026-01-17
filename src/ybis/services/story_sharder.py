"""
Story Sharder - Breaks large tasks into smaller stories.

Splits complex tasks into manageable sub-tasks (stories).
"""

import json
from typing import Any

from ..services.policy import get_policy_provider


class StorySharder:
    """
    Story Sharder - Splits tasks into stories.

    Breaks down large tasks into smaller, manageable sub-tasks.
    """

    def __init__(self):
        """Initialize story sharder."""
        self.policy = get_policy_provider()

    def shard_task(self, task_objective: str, max_story_size: int = 5) -> list[dict[str, Any]]:
        """
        Shard a task into smaller stories.

        Args:
            task_objective: Original task objective
            max_story_size: Maximum number of steps per story

        Returns:
            List of story dictionaries
        """
        # For now, use simple heuristic-based sharding
        # Full implementation would use LLM to intelligently split tasks

        # Simple splitting by sentences or bullet points
        lines = task_objective.split("\n")
        stories = []

        current_story = {
            "objective": "",
            "steps": [],
            "dependencies": [],
        }

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Check if line is a step indicator (bullet, number, etc.)
            if line.startswith("-") or line.startswith("*") or line[0].isdigit():
                # This is a step
                if len(current_story["steps"]) >= max_story_size:
                    # Start new story
                    if current_story["objective"]:
                        stories.append(current_story)
                    current_story = {
                        "objective": "",
                        "steps": [],
                        "dependencies": [],
                    }

                current_story["steps"].append(line)
            else:
                # This is part of the objective
                if current_story["objective"]:
                    current_story["objective"] += " " + line
                else:
                    current_story["objective"] = line

        # Add last story
        if current_story["objective"] or current_story["steps"]:
            stories.append(current_story)

        # If no stories were created, create a single story
        if not stories:
            stories.append(
                {
                    "objective": task_objective,
                    "steps": [],
                    "dependencies": [],
                }
            )

        return stories

    async def shard_with_llm(self, task_objective: str) -> list[dict[str, Any]]:
        """
        Shard task using LLM for intelligent splitting.

        Args:
            task_objective: Original task objective

        Returns:
            List of story dictionaries
        """
        try:
            import litellm

            from ..services.policy import get_policy_provider

            policy = get_policy_provider()
            llm_config = policy.get_llm_config()

            model = llm_config.get("planner_model", "ollama/llama3.2:3b")
            api_base = llm_config.get("api_base", "http://localhost:11434")

            prompt = f"""Break down this task into smaller, manageable stories (sub-tasks).

Task: {task_objective}

Return a JSON array of stories, where each story has:
- objective: Clear goal for this story
- steps: List of specific steps to complete this story
- dependencies: List of story indices this story depends on (empty if none)

Format:
[
  {{
    "objective": "Story 1 objective",
    "steps": ["Step 1", "Step 2"],
    "dependencies": []
  }},
  {{
    "objective": "Story 2 objective",
    "steps": ["Step 1", "Step 2"],
    "dependencies": [0]
  }}
]

Return only valid JSON, no markdown formatting."""

            response = litellm.completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                api_base=api_base,
            )

            content = response.choices[0].message.content.strip()

            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()

            stories = json.loads(content)

            return stories

        except Exception as e:
            # Fallback to heuristic sharding
            print(f"[WARNING] LLM sharding failed: {e}. Using heuristic sharding.")
            return self.shard_task(task_objective)


# Global story sharder instance
_story_sharder: StorySharder | None = None


def get_story_sharder() -> StorySharder:
    """Get global story sharder instance."""
    global _story_sharder
    if _story_sharder is None:
        _story_sharder = StorySharder()
    return _story_sharder


