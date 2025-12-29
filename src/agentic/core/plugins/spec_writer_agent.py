"""
SpecWriterAgent - LLM-powered specification generator

Generates comprehensive specifications using templates and LLM enhancement.
Part of the Spec-Driven Development (SDD) pipeline.
"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from dataclasses import dataclass

from src.agentic.core.plugins.spec_templates import get_template, list_templates
from src.agentic.core.config import USE_LITELLM, LITELLM_QUALITY


@dataclass
class SpecAnalysis:
    """Analysis of task to determine spec characteristics"""
    spec_type: str  # feature, refactor, bugfix, architecture
    confidence: float  # 0.0-1.0
    key_entities: List[str]  # Identified entities (files, classes, etc.)
    complexity: str  # simple, moderate, complex
    estimated_hours: float
    reasoning: str  # Why this spec type was chosen


@dataclass
class SpecContent:
    """Generated specification content"""
    spec_type: str
    content: str
    placeholders_filled: Dict[str, str]
    warnings: List[str]
    suggestions: List[str]


class SpecWriterAgent:
    """
    LLM-powered agent for generating comprehensive task specifications.

    Workflow:
    1. Analyze task goal/details → determine spec type
    2. Select appropriate template
    3. Use LLM to fill placeholders intelligently
    4. Present spec for review
    5. Save to workspace/SPEC.md

    Features:
    - Template-based generation (feature/refactor/bugfix/architecture)
    - LLM-powered placeholder filling
    - Interactive review and editing
    - Validation and quality checks
    """

    def __init__(self, llm_provider=None, quality: str = None):
        """
        Initialize SpecWriterAgent.

        Args:
            llm_provider: LLM provider instance (optional, will auto-select)
            quality: LLM quality level (high/medium/low)
        """
        self.llm_provider = llm_provider
        self.quality = quality or LITELLM_QUALITY
        self._provider_initialized = False

    async def _ensure_provider(self):
        """Lazy-load LLM provider if needed"""
        if self._provider_initialized:
            return

        if self.llm_provider is None:
            if USE_LITELLM:
                from src.agentic.core.litellm_provider import LiteLLMProvider
                self.llm_provider = LiteLLMProvider(quality=self.quality)
            else:
                from src.agentic.core.litellm_provider import OllamaProvider
                self.llm_provider = OllamaProvider()

        self._provider_initialized = True

    async def analyze_task(self, task_id: str, goal: str, details: str = "") -> SpecAnalysis:
        """
        Analyze task to determine appropriate spec type.

        Args:
            task_id: Task identifier
            goal: Task goal/title
            details: Additional task details

        Returns:
            SpecAnalysis with spec type, confidence, entities, complexity
        """
        await self._ensure_provider()

        # Build analysis prompt
        prompt = f"""Analyze this task and determine the appropriate specification type.

Task ID: {task_id}
Goal: {goal}
Details: {details}

Available spec types:
- feature: New functionality or capability
- refactor: Code improvement/restructuring without changing behavior
- bugfix: Fixing incorrect behavior
- architecture: System-wide architectural changes

Analyze and provide:
1. Spec type (one of: feature, refactor, bugfix, architecture)
2. Confidence (0.0-1.0)
3. Key entities (files, classes, modules mentioned or implied)
4. Complexity (simple/moderate/complex)
5. Estimated hours (rough estimate)
6. Reasoning (why this spec type)

Format your response as JSON:
{{
    "spec_type": "...",
    "confidence": 0.0,
    "key_entities": ["..."],
    "complexity": "...",
    "estimated_hours": 0.0,
    "reasoning": "..."
}}"""

        response = await self.llm_provider.generate(
            prompt=prompt,
            temperature=0.3,
            max_tokens=1000
        )

        # Parse response
        content = response.get("content", "{}")
        analysis_data = self._parse_json_response(content)

        return SpecAnalysis(
            spec_type=analysis_data.get("spec_type", "feature"),
            confidence=analysis_data.get("confidence", 0.5),
            key_entities=analysis_data.get("key_entities", []),
            complexity=analysis_data.get("complexity", "moderate"),
            estimated_hours=analysis_data.get("estimated_hours", 8.0),
            reasoning=analysis_data.get("reasoning", "Default analysis")
        )

    async def generate_spec(
        self,
        task_id: str,
        goal: str,
        details: str = "",
        spec_type: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> SpecContent:
        """
        Generate comprehensive specification for task.

        Args:
            task_id: Task identifier
            goal: Task goal/title
            details: Additional task details
            spec_type: Override auto-detected spec type
            context: Additional context (files, dependencies, etc.)

        Returns:
            SpecContent with filled specification
        """
        await self._ensure_provider()

        # Auto-detect spec type if not provided
        if spec_type is None:
            analysis = await self.analyze_task(task_id, goal, details)
            spec_type = analysis.spec_type
            print(f"[SpecWriter] Auto-detected spec type: {spec_type} (confidence: {analysis.confidence:.2f})")
        else:
            spec_type = spec_type.lower().strip()

        # Get template
        template = get_template(spec_type)

        # Extract placeholders from template
        placeholders = self._extract_placeholders(template)
        print(f"[SpecWriter] Found {len(placeholders)} placeholders to fill")

        # Fill placeholders using LLM
        filled_values = await self._fill_placeholders(
            template=template,
            placeholders=placeholders,
            task_id=task_id,
            goal=goal,
            details=details,
            spec_type=spec_type,
            context=context or {}
        )

        # Apply filled values to template
        spec_content = self._apply_values(template, filled_values)

        # Validate and collect warnings
        warnings, suggestions = self._validate_spec(spec_content, spec_type)

        return SpecContent(
            spec_type=spec_type,
            content=spec_content,
            placeholders_filled=filled_values,
            warnings=warnings,
            suggestions=suggestions
        )

    async def _fill_placeholders(
        self,
        template: str,
        placeholders: List[str],
        task_id: str,
        goal: str,
        details: str,
        spec_type: str,
        context: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Use LLM to intelligently fill template placeholders.

        Args:
            template: Template string
            placeholders: List of placeholder names
            task_id: Task ID
            goal: Task goal
            details: Task details
            spec_type: Spec type
            context: Additional context

        Returns:
            Dict mapping placeholder names to filled values
        """
        # Build comprehensive prompt
        context_str = "\n".join([f"- {k}: {v}" for k, v in context.items()])

        prompt = f"""You are a technical specification writer. Fill in the placeholders for a {spec_type} specification.

Task Information:
- ID: {task_id}
- Goal: {goal}
- Details: {details}

Additional Context:
{context_str if context_str else "None"}

Template placeholders to fill:
{', '.join(placeholders)}

Requirements:
1. Be specific and concrete (avoid vague descriptions)
2. Use technical terminology appropriate for developers
3. Include measurable criteria where applicable
4. Consider realistic constraints and dependencies
5. Provide actionable information

For each placeholder, provide a clear, specific value. Format as JSON:
{{
    "placeholder_name": "filled value",
    ...
}}

Important:
- For timestamps: use ISO format (2025-12-28T23:00:00)
- For estimates: use format like "2-3 hours" or "1-2 days"
- For requirements: be specific and testable
- For steps: provide concrete action items
- For risks: include both likelihood and impact"""

        response = await self.llm_provider.generate(
            prompt=prompt,
            temperature=0.4,
            max_tokens=3000
        )

        # Parse response
        content = response.get("content", "{}")
        filled_values = self._parse_json_response(content)

        # Fill in standard placeholders automatically
        auto_filled = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "task_name": goal,
            "feature_name": goal,
            "refactor_name": goal,
            "bug_name": goal,
            "architecture_name": goal,
            "description": details or goal
        }

        # Merge auto-filled with LLM-filled (LLM takes precedence for duplicates)
        result = {**auto_filled, **filled_values}

        # Ensure all placeholders have values (fill missing with defaults)
        for placeholder in placeholders:
            if placeholder not in result:
                result[placeholder] = self._get_default_value(placeholder)

        return result

    def _extract_placeholders(self, template: str) -> List[str]:
        """
        Extract all {placeholder} names from template.

        Args:
            template: Template string

        Returns:
            List of unique placeholder names
        """
        pattern = r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}'
        matches = re.findall(pattern, template)
        return list(set(matches))  # Unique placeholders

    def _apply_values(self, template: str, values: Dict[str, str]) -> str:
        """
        Apply filled values to template placeholders.

        Args:
            template: Template string
            values: Dict of placeholder values

        Returns:
            Template with placeholders replaced
        """
        result = template
        for key, value in values.items():
            placeholder = f"{{{key}}}"
            result = result.replace(placeholder, str(value))
        return result

    def _validate_spec(self, spec_content: str, spec_type: str) -> Tuple[List[str], List[str]]:
        """
        Validate generated spec and collect warnings/suggestions.

        Args:
            spec_content: Generated spec content
            spec_type: Spec type

        Returns:
            Tuple of (warnings, suggestions)
        """
        warnings = []
        suggestions = []

        # Check for unfilled placeholders
        unfilled = re.findall(r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}', spec_content)
        if unfilled:
            warnings.append(f"Unfilled placeholders: {', '.join(set(unfilled))}")

        # Check for too-short sections
        if spec_content.count('\n') < 20:
            warnings.append("Specification seems too short (< 20 lines)")

        # Check for empty checkboxes (should have some)
        if '- [ ]' not in spec_content:
            suggestions.append("Consider adding checkboxes for trackable items")

        # Check for timeline section
        if 'Timeline' not in spec_content and 'Estimate' not in spec_content:
            warnings.append("Missing timeline/estimate section")

        # Check for success criteria
        if 'Success Criteria' not in spec_content and 'Acceptance' not in spec_content:
            warnings.append("Missing success criteria section")

        # Spec-type specific validations
        if spec_type == 'feature':
            if 'Requirements' not in spec_content:
                warnings.append("Feature spec missing Requirements section")
        elif spec_type == 'bugfix':
            if 'Reproduction' not in spec_content:
                warnings.append("Bug spec missing Reproduction Steps")
        elif spec_type == 'architecture':
            if 'Diagram' not in spec_content:
                suggestions.append("Consider adding architecture diagrams")

        return warnings, suggestions

    def _get_default_value(self, placeholder: str) -> str:
        """Get default value for unfilled placeholder"""
        defaults = {
            "estimate": "TBD",
            "total_estimate": "TBD",
            "timeline": "TBD",
            "severity": "Medium",
            "priority": "Medium",
            "reporter": "System",
            "report_date": datetime.now().strftime("%Y-%m-%d")
        }
        return defaults.get(placeholder, "[TO BE FILLED]")

    def _parse_json_response(self, content: str) -> Dict[str, Any]:
        """Parse JSON from LLM response (handles code blocks)"""
        import json

        # Try to extract JSON from code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1)
        else:
            # Try to find raw JSON object
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group(0)

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print(f"[SpecWriter] Warning: Failed to parse JSON response")
            return {}

    async def save_spec(
        self,
        spec_content: SpecContent,
        workspace_path: Path,
        filename: str = "SPEC.md"
    ) -> Path:
        """
        Save generated spec to workspace.

        Args:
            spec_content: Generated spec
            workspace_path: Workspace directory
            filename: Output filename

        Returns:
            Path to saved spec file
        """
        # Ensure workspace exists
        workspace_path = Path(workspace_path)
        workspace_path.mkdir(parents=True, exist_ok=True)

        # Save spec
        spec_file = workspace_path / filename
        spec_file.write_text(spec_content.content, encoding='utf-8')

        print(f"[SpecWriter] Saved spec to: {spec_file}")
        return spec_file

    async def generate_and_save(
        self,
        task_id: str,
        goal: str,
        details: str = "",
        workspace_path: Optional[Path] = None,
        spec_type: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Tuple[SpecContent, Path]:
        """
        Complete workflow: analyze, generate, and save spec.

        Args:
            task_id: Task ID
            goal: Task goal
            details: Task details
            workspace_path: Workspace path (auto-created if None)
            spec_type: Override spec type
            context: Additional context

        Returns:
            Tuple of (SpecContent, Path to saved file)
        """
        # Auto-create workspace if not provided
        if workspace_path is None:
            workspace_path = Path(f"workspaces/active/{task_id}")

        # Generate spec
        spec = await self.generate_spec(
            task_id=task_id,
            goal=goal,
            details=details,
            spec_type=spec_type,
            context=context
        )

        # Print warnings and suggestions
        if spec.warnings:
            print(f"[SpecWriter] Warnings:")
            for warning in spec.warnings:
                print(f"  - {warning}")

        if spec.suggestions:
            print(f"[SpecWriter] Suggestions:")
            for suggestion in spec.suggestions:
                print(f"  - {suggestion}")

        # Save spec
        spec_file = await self.save_spec(spec, workspace_path)

        return spec, spec_file


__all__ = [
    "SpecWriterAgent",
    "SpecAnalysis",
    "SpecContent"
]
