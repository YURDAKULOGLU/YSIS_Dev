"""
StorySharder - Breaks large tasks into smaller executable stories.

Restored from legacy orchestrator_unified.py pattern.
Ensures Aider never receives tasks larger than ~50 lines of diff.
"""

from dataclasses import dataclass
from pathlib import Path

from src.agentic.core.protocols import Plan


@dataclass
class Story:
    """A single executable story derived from a larger task."""
    id: str
    title: str
    description: str
    files_to_modify: list[str]
    acceptance_criteria: list[str]
    estimated_lines: int
    parent_task_id: str


class StorySharder:
    """
    Breaks large plans into smaller, executable stories.

    Features:
    - Automatic complexity estimation
    - File-based sharding (one story per file group)
    - PRD generation for documentation
    - Story file persistence
    """

    MAX_LINES_PER_STORY = 50  # Aider works best with small changes

    def __init__(self, workspace_path: Path = None):
        self.workspace_path = workspace_path

    def should_shard(self, plan: Plan) -> bool:
        """
        Determine if a plan should be sharded into stories.

        Criteria:
        - Multiple files to modify (>2)
        - Complex steps (>5)
        - Multiple concerns detected
        """
        if len(plan.files_to_modify) > 2:
            return True
        if len(plan.steps) > 5:
            return True

        # Check for multiple concerns in objective
        concerns = ['test', 'refactor', 'add', 'fix', 'update', 'create', 'implement']
        concern_count = sum(1 for c in concerns if c in plan.objective.lower())
        if concern_count > 2:
            return True

        return False

    def estimate_complexity(self, plan: Plan) -> int:
        """Estimate total lines of change for a plan."""
        base_estimate = 20  # Minimum
        file_estimate = len(plan.files_to_modify) * 30
        step_estimate = len(plan.steps) * 10

        return base_estimate + file_estimate + step_estimate

    def shard(self, plan: Plan, task_id: str) -> list[Story]:
        """
        Break a plan into executable stories.

        Sharding strategies:
        1. File-based: One story per file or file group
        2. Step-based: Group related steps into stories
        3. Concern-based: Separate tests from implementation
        """
        stories = []

        # Strategy 1: Separate test files from source files
        source_files = [f for f in plan.files_to_modify if 'test' not in f.lower()]
        test_files = [f for f in plan.files_to_modify if 'test' in f.lower()]

        story_idx = 1

        # Story for source files (grouped by directory)
        if source_files:
            # Group by top-level directory
            dir_groups: dict[str, list[str]] = {}
            for f in source_files:
                parts = Path(f).parts
                top_dir = parts[0] if parts else 'root'
                dir_groups.setdefault(top_dir, []).append(f)

            for dir_name, files in dir_groups.items():
                story = Story(
                    id=f"{task_id}-S{story_idx}",
                    title=f"Implement changes in {dir_name}/",
                    description=self._generate_story_description(plan, files),
                    files_to_modify=files,
                    acceptance_criteria=self._extract_criteria(plan, files),
                    estimated_lines=len(files) * 30,
                    parent_task_id=task_id
                )
                stories.append(story)
                story_idx += 1

        # Story for test files
        if test_files:
            test_file_list = "\n".join(f"- {f}" for f in test_files)
            story = Story(
                id=f"{task_id}-S{story_idx}",
                title="Write/update tests",
                description=f"Create or update tests for the implementation.\n\nFiles:\n{test_file_list}",
                files_to_modify=test_files,
                acceptance_criteria=["All tests pass", "Coverage maintained or improved"],
                estimated_lines=len(test_files) * 40,
                parent_task_id=task_id
            )
            stories.append(story)

        return stories

    def _generate_story_description(self, plan: Plan, files: list[str]) -> str:
        """Generate description for a story."""
        desc = f"## Objective\n{plan.objective}\n\n"
        desc += "## Files to Modify\n"
        for f in files:
            desc += f"- {f}\n"
        desc += "\n## Steps\n"
        for step in plan.steps:
            # Include only steps that seem relevant to these files
            if any(f.split('/')[-1].replace('.py', '') in step.lower() for f in files):
                desc += f"- {step}\n"
            elif not any(f in step.lower() for f in plan.files_to_modify):
                # Generic step, include it
                desc += f"- {step}\n"
        return desc

    def _extract_criteria(self, plan: Plan, files: list[str]) -> list[str]:
        """Extract acceptance criteria relevant to specific files."""
        criteria = []
        for criterion in plan.success_criteria:
            # Include if it mentions any of the files or is generic
            if any(Path(f).stem in criterion.lower() for f in files):
                criteria.append(criterion)
            elif not any(Path(f).stem in criterion.lower() for f in plan.files_to_modify):
                criteria.append(criterion)

        if not criteria:
            criteria = ["Changes compile without errors", "No regressions introduced"]

        return criteria

    def save_stories(self, stories: list[Story], output_dir: Path) -> list[Path]:
        """
        Save stories as markdown files for documentation.

        Returns list of created file paths.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        paths = []

        for story in stories:
            story_path = output_dir / f"story-{story.id}.md"
            content = self._render_story_markdown(story)
            story_path.write_text(content, encoding='utf-8')
            paths.append(story_path)
            print(f"[StorySharder] Created: {story_path.name}")

        return paths

    def _render_story_markdown(self, story: Story) -> str:
        """Render story as markdown."""
        return f"""# Story: {story.title}

**ID:** {story.id}
**Parent Task:** {story.parent_task_id}
**Estimated Lines:** ~{story.estimated_lines}

## Description

{story.description}

## Files to Modify

{chr(10).join(f'- {f}' for f in story.files_to_modify)}

## Acceptance Criteria

{chr(10).join(f'- [ ] {c}' for c in story.acceptance_criteria)}

## Verification

- [ ] Code compiles without errors
- [ ] Ruff check passes
- [ ] Related tests pass
"""

    def generate_prd(self, plan: Plan, task_id: str, output_path: Path) -> Path:
        """
        Generate a PRD (Product Requirements Document) for a task.

        This is the spec that drives the sharding process.
        """
        prd_content = f"""# PRD: {plan.objective}

**Task ID:** {task_id}
**Generated:** Auto-generated from task plan

## Overview

{plan.objective}

## User Stories

"""
        for i, step in enumerate(plan.steps, 1):
            prd_content += f"- Story {i}: {step}\n"

        files_list = chr(10).join(f'- {f}' for f in plan.files_to_modify)
        deps_list = chr(10).join(f'- {d}' for d in plan.dependencies) if plan.dependencies else '- None identified'
        risks_list = chr(10).join(f'- {r}' for r in plan.risks) if plan.risks else '- None identified'
        criteria_list = (
            chr(10).join(f'- [ ] {c}' for c in plan.success_criteria)
            if plan.success_criteria else '- [ ] Task completed successfully'
        )

        prd_content += f"""
## Technical Requirements

### Files to Modify
{files_list}

### Dependencies
{deps_list}

### Risks
{risks_list}

## Success Criteria

{criteria_list}

## Implementation Notes

This PRD was auto-generated. Review and adjust as needed before implementation.
"""

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(prd_content, encoding='utf-8')
        print(f"[StorySharder] Created PRD: {output_path}")
        return output_path

    def stories_to_plans(self, stories: list[Story], original_plan: Plan) -> list[Plan]:
        """Convert stories back to Plan objects for execution."""
        plans = []
        for story in stories:
            plan = Plan(
                objective=f"[{story.id}] {story.title}\n\n{story.description}",
                steps=[f"Implement: {story.title}"],
                files_to_modify=story.files_to_modify,
                dependencies=original_plan.dependencies,
                risks=[],
                success_criteria=story.acceptance_criteria,
                metadata={
                    'story_id': story.id,
                    'parent_task': story.parent_task_id,
                    'source': 'StorySharder'
                }
            )
            plans.append(plan)
        return plans
