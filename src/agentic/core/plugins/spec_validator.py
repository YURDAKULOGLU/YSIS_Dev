"""
SpecValidator - Validation engine for Spec-Driven Development

Validates plans and implementations against specifications.
Ensures compliance with requirements and success criteria.
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ValidationLevel(Enum):
    """Validation severity levels"""
    ERROR = "error"  # Blocking issue
    WARNING = "warning"  # Non-blocking concern
    INFO = "info"  # Informational


@dataclass
class ValidationIssue:
    """Single validation issue"""
    level: ValidationLevel
    message: str
    section: str  # Which spec section
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of spec validation"""
    passed: bool
    score: float  # 0.0-1.0 compliance score
    issues: List[ValidationIssue] = field(default_factory=list)
    requirements_met: int = 0
    requirements_total: int = 0
    criteria_met: int = 0
    criteria_total: int = 0
    summary: str = ""

    def add_issue(self, level: ValidationLevel, message: str, section: str, suggestion: str = None):
        """Add validation issue"""
        self.issues.append(ValidationIssue(level, message, section, suggestion))

    @property
    def errors(self) -> List[ValidationIssue]:
        """Get error-level issues"""
        return [i for i in self.issues if i.level == ValidationLevel.ERROR]

    @property
    def warnings(self) -> List[ValidationIssue]:
        """Get warning-level issues"""
        return [i for i in self.issues if i.level == ValidationLevel.WARNING]

    @property
    def infos(self) -> List[ValidationIssue]:
        """Get info-level issues"""
        return [i for i in self.issues if i.level == ValidationLevel.INFO]


@dataclass
class ParsedSpec:
    """Parsed specification content"""
    spec_type: str
    task_id: str
    overview: str
    requirements: List[str]  # Functional requirements
    nonfunctional_requirements: List[str]  # Performance, security, etc.
    success_criteria: List[str]  # Acceptance criteria
    implementation_steps: List[str]
    dependencies: List[str]
    risks: List[str]
    constraints: Dict[str, Any]  # Timeline, budget, technical constraints
    raw_content: str


class SpecValidator:
    """
    Validates plans and implementations against specifications.

    Features:
    - Parse SPEC.md files (extract requirements, criteria, constraints)
    - Validate plans against specs
    - Validate implementations against specs
    - Score compliance (0.0-1.0)
    - Generate validation reports
    - LLM-assisted semantic validation (optional)
    """

    def __init__(self, llm_provider=None):
        """
        Initialize SpecValidator.

        Args:
            llm_provider: Optional LLM for semantic validation
        """
        self.llm_provider = llm_provider
        self._provider_initialized = False

    async def _ensure_provider(self):
        """Lazy-load LLM provider if needed"""
        if self._provider_initialized:
            return

        if self.llm_provider is None:
            try:
                from src.agentic.core.config import USE_LITELLM, LITELLM_QUALITY
                if USE_LITELLM:
                    from src.agentic.core.litellm_provider import LiteLLMProvider
                    self.llm_provider = LiteLLMProvider(quality=LITELLM_QUALITY)
                else:
                    from src.agentic.core.litellm_provider import OllamaProvider
                    self.llm_provider = OllamaProvider()
            except Exception as e:
                print(f"[SpecValidator] LLM provider unavailable: {e}")
                self.llm_provider = None

        self._provider_initialized = True

    def parse_spec(self, spec_path: Path) -> ParsedSpec:
        """
        Parse SPEC.md file and extract key sections.

        Args:
            spec_path: Path to SPEC.md

        Returns:
            ParsedSpec with extracted content
        """
        content = spec_path.read_text(encoding='utf-8')

        # Extract frontmatter
        spec_type = self._extract_frontmatter_field(content, "category", "general")
        task_id = self._extract_frontmatter_field(content, "id", "unknown")

        # Extract sections
        overview = self._extract_section(content, ["Overview", "Objective", "Description"])
        requirements = self._extract_checklist_items(content, ["Requirements", "Functional Requirements"])
        nonfunctional = self._extract_checklist_items(content, ["Non-Functional Requirements", "Performance", "Security"])
        success_criteria = self._extract_checklist_items(content, ["Success Criteria", "Acceptance Criteria"])
        steps = self._extract_numbered_items(content, ["Implementation Steps", "Steps", "Migration Strategy"])
        dependencies = self._extract_list_items(content, ["Dependencies", "Prerequisites"])
        risks = self._extract_table_column(content, ["Risks", "Risk Assessment"], "Risk")

        # Extract constraints
        constraints = {
            "timeline": self._extract_section(content, ["Timeline", "Estimate"]),
            "backward_compatible": "backward compatib" in content.lower() or "breaking change" not in content.lower()
        }

        return ParsedSpec(
            spec_type=spec_type,
            task_id=task_id,
            overview=overview,
            requirements=requirements,
            nonfunctional_requirements=nonfunctional,
            success_criteria=success_criteria,
            implementation_steps=steps,
            dependencies=dependencies,
            risks=risks,
            constraints=constraints,
            raw_content=content
        )

    async def validate_plan(
        self,
        spec: ParsedSpec,
        plan_content: str,
        use_llm: bool = True
    ) -> ValidationResult:
        """
        Validate a plan against specification.

        Args:
            spec: Parsed specification
            plan_content: Plan content (PLAN.md)
            use_llm: Use LLM for semantic validation

        Returns:
            ValidationResult with compliance score and issues
        """
        result = ValidationResult(passed=True, score=1.0)

        # 1. Check if plan addresses all requirements
        for req in spec.requirements:
            if not self._requirement_addressed(req, plan_content):
                result.add_issue(
                    ValidationLevel.ERROR,
                    f"Requirement not addressed: {req}",
                    "Requirements",
                    f"Add implementation steps for: {req}"
                )
                result.requirements_total += 1
            else:
                result.requirements_met += 1
                result.requirements_total += 1

        # 2. Check if plan includes all success criteria
        for criterion in spec.success_criteria:
            if not self._criterion_covered(criterion, plan_content):
                result.add_issue(
                    ValidationLevel.WARNING,
                    f"Success criterion not explicitly covered: {criterion}",
                    "Success Criteria",
                    f"Add verification steps for: {criterion}"
                )
                result.criteria_total += 1
            else:
                result.criteria_met += 1
                result.criteria_total += 1

        # 3. Check dependencies mentioned
        for dep in spec.dependencies:
            if dep.strip() and dep.lower() not in plan_content.lower():
                result.add_issue(
                    ValidationLevel.INFO,
                    f"Dependency not mentioned: {dep}",
                    "Dependencies"
                )

        # 4. Check backward compatibility constraint
        if spec.constraints.get("backward_compatible"):
            if "breaking" in plan_content.lower() and "migration" not in plan_content.lower():
                result.add_issue(
                    ValidationLevel.ERROR,
                    "Plan introduces breaking changes without migration strategy",
                    "Compatibility",
                    "Add migration plan or remove breaking changes"
                )

        # 5. Check implementation steps exist
        if not self._has_implementation_steps(plan_content):
            result.add_issue(
                ValidationLevel.ERROR,
                "Plan missing implementation steps",
                "Implementation",
                "Add concrete implementation steps"
            )

        # 6. LLM semantic validation (optional)
        if use_llm and self.llm_provider:
            await self._ensure_provider()
            semantic_issues = await self._validate_semantically(spec, plan_content, "plan")
            for issue in semantic_issues:
                result.add_issue(issue.level, issue.message, issue.section, issue.suggestion)

        # Calculate score
        result.score = self._calculate_score(result)
        result.passed = len(result.errors) == 0 and result.score >= 0.7

        # Generate summary
        result.summary = self._generate_summary(result, "plan")

        return result

    async def validate_implementation(
        self,
        spec: ParsedSpec,
        changed_files: List[str],
        file_contents: Dict[str, str],
        use_llm: bool = True
    ) -> ValidationResult:
        """
        Validate implementation against specification.

        Args:
            spec: Parsed specification
            changed_files: List of modified file paths
            file_contents: Dict mapping file paths to their content
            use_llm: Use LLM for semantic validation

        Returns:
            ValidationResult with compliance score and issues
        """
        result = ValidationResult(passed=True, score=1.0)

        # Combine all changed content for analysis
        all_content = "\n\n".join([
            f"File: {path}\n{content}"
            for path, content in file_contents.items()
        ])

        # 1. Check if requirements are implemented
        for req in spec.requirements:
            if not self._requirement_implemented(req, all_content):
                result.add_issue(
                    ValidationLevel.ERROR,
                    f"Requirement not implemented: {req}",
                    "Requirements"
                )
                result.requirements_total += 1
            else:
                result.requirements_met += 1
                result.requirements_total += 1

        # 2. Check success criteria
        for criterion in spec.success_criteria:
            if not self._criterion_met(criterion, all_content):
                result.add_issue(
                    ValidationLevel.WARNING,
                    f"Success criterion may not be met: {criterion}",
                    "Success Criteria"
                )
                result.criteria_total += 1
            else:
                result.criteria_met += 1
                result.criteria_total += 1

        # 3. Check for tests if spec requires them
        if "test" in spec.raw_content.lower():
            test_files = [f for f in changed_files if "test" in f.lower()]
            if not test_files:
                result.add_issue(
                    ValidationLevel.WARNING,
                    "Spec requires tests but no test files found",
                    "Testing",
                    "Add test files to implementation"
                )

        # 4. Check backward compatibility
        if spec.constraints.get("backward_compatible"):
            if self._has_breaking_changes(all_content):
                result.add_issue(
                    ValidationLevel.ERROR,
                    "Implementation introduces breaking changes",
                    "Compatibility",
                    "Maintain backward compatibility or add migration"
                )

        # 5. LLM semantic validation
        if use_llm and self.llm_provider:
            await self._ensure_provider()
            semantic_issues = await self._validate_semantically(spec, all_content, "implementation")
            for issue in semantic_issues:
                result.add_issue(issue.level, issue.message, issue.section, issue.suggestion)

        # Calculate score
        result.score = self._calculate_score(result)
        result.passed = len(result.errors) == 0 and result.score >= 0.7

        # Generate summary
        result.summary = self._generate_summary(result, "implementation")

        return result

    async def _validate_semantically(
        self,
        spec: ParsedSpec,
        content: str,
        content_type: str
    ) -> List[ValidationIssue]:
        """
        Use LLM to perform semantic validation.

        Args:
            spec: Parsed spec
            content: Content to validate (plan or implementation)
            content_type: "plan" or "implementation"

        Returns:
            List of validation issues
        """
        if not self.llm_provider:
            return []

        prompt = f"""You are a technical specification validator. Analyze whether this {content_type} complies with the specification.

SPECIFICATION:
{spec.raw_content[:2000]}  # First 2000 chars

{content_type.upper()}:
{content[:3000]}  # First 3000 chars

Validation tasks:
1. Check if all requirements are addressed/implemented
2. Verify success criteria can be met
3. Identify any missing components
4. Check for potential issues or gaps

Respond with JSON array of issues (empty if no issues):
[
    {{
        "level": "error|warning|info",
        "message": "Clear issue description",
        "section": "Spec section name",
        "suggestion": "How to fix (optional)"
    }}
]
"""

        try:
            response = await self.llm_provider.generate(
                prompt=prompt,
                temperature=0.2,
                max_tokens=2000
            )

            content = response.get("content", "[]")
            issues_data = self._parse_json_array(content)

            issues = []
            for issue_dict in issues_data:
                level_str = issue_dict.get("level", "info").lower()
                level = {
                    "error": ValidationLevel.ERROR,
                    "warning": ValidationLevel.WARNING,
                    "info": ValidationLevel.INFO
                }.get(level_str, ValidationLevel.INFO)

                issues.append(ValidationIssue(
                    level=level,
                    message=issue_dict.get("message", "Unknown issue"),
                    section=issue_dict.get("section", "General"),
                    suggestion=issue_dict.get("suggestion")
                ))

            return issues
        except Exception as e:
            print(f"[SpecValidator] Semantic validation failed: {e}")
            return []

    # ===== Helper Methods =====

    def _extract_frontmatter_field(self, content: str, field: str, default: str = "") -> str:
        """Extract field from YAML frontmatter"""
        match = re.search(r'^---\s*\n(.*?)\n---', content, re.MULTILINE | re.DOTALL)
        if match:
            frontmatter = match.group(1)
            field_match = re.search(rf'^{field}:\s*(.+)$', frontmatter, re.MULTILINE)
            if field_match:
                return field_match.group(1).strip()
        return default

    def _extract_section(self, content: str, headers: List[str]) -> str:
        """Extract content under specified headers"""
        for header in headers:
            pattern = rf'##\s+{re.escape(header)}\s*\n(.*?)(?=\n##|\Z)'
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return ""

    def _extract_checklist_items(self, content: str, headers: List[str]) -> List[str]:
        """Extract checkbox items from section"""
        section = self._extract_section(content, headers)
        if not section:
            return []

        pattern = r'-\s+\[\s*\]\s+(.+?)(?:\n|$)'
        matches = re.findall(pattern, section)
        return [m.strip() for m in matches]

    def _extract_numbered_items(self, content: str, headers: List[str]) -> List[str]:
        """Extract numbered list items"""
        section = self._extract_section(content, headers)
        if not section:
            return []

        pattern = r'^\d+\.\s+(.+?)(?:\n|$)'
        matches = re.findall(pattern, section, re.MULTILINE)
        return [m.strip() for m in matches]

    def _extract_list_items(self, content: str, headers: List[str]) -> List[str]:
        """Extract bulleted list items"""
        section = self._extract_section(content, headers)
        if not section:
            return []

        pattern = r'^-\s+(.+?)(?:\n|$)'
        matches = re.findall(pattern, section, re.MULTILINE)
        return [m.strip() for m in matches if not m.strip().startswith('[')]

    def _extract_table_column(self, content: str, headers: List[str], column_name: str) -> List[str]:
        """Extract specific column from markdown table"""
        section = self._extract_section(content, headers)
        if not section:
            return []

        # Find table and extract column
        lines = section.split('\n')
        if len(lines) < 2:
            return []

        header_line = lines[0]
        columns = [c.strip() for c in header_line.split('|')]

        try:
            col_index = columns.index(column_name)
        except ValueError:
            return []

        items = []
        for line in lines[2:]:  # Skip header and separator
            if '|' in line:
                cells = [c.strip() for c in line.split('|')]
                if col_index < len(cells):
                    items.append(cells[col_index])

        return items

    def _requirement_addressed(self, requirement: str, plan: str) -> bool:
        """Check if requirement is addressed in plan"""
        # Simple keyword matching (can be enhanced)
        req_keywords = set(re.findall(r'\w+', requirement.lower()))
        plan_lower = plan.lower()

        # At least 50% of keywords should appear
        matches = sum(1 for kw in req_keywords if kw in plan_lower and len(kw) > 3)
        return matches >= len(req_keywords) * 0.5

    def _criterion_covered(self, criterion: str, plan: str) -> bool:
        """Check if success criterion is covered in plan"""
        return self._requirement_addressed(criterion, plan)

    def _requirement_implemented(self, requirement: str, code: str) -> bool:
        """Check if requirement is implemented in code"""
        # More lenient than plan checking
        req_keywords = set(re.findall(r'\w+', requirement.lower()))
        code_lower = code.lower()

        matches = sum(1 for kw in req_keywords if kw in code_lower and len(kw) > 3)
        return matches >= len(req_keywords) * 0.3

    def _criterion_met(self, criterion: str, code: str) -> bool:
        """Check if success criterion is met in code"""
        return self._requirement_implemented(criterion, code)

    def _has_implementation_steps(self, plan: str) -> bool:
        """Check if plan has implementation steps"""
        # Look for numbered lists or step sections
        has_numbers = bool(re.search(r'^\d+\.\s+', plan, re.MULTILINE))
        has_steps = 'step' in plan.lower() or 'phase' in plan.lower()
        return has_numbers or has_steps

    def _has_breaking_changes(self, code: str) -> bool:
        """Detect potential breaking changes in code"""
        # Simple heuristics
        breaking_indicators = [
            r'def\s+\w+\([^)]*\).*?:.*?#.*?breaking',  # Comments mentioning breaking
            r'raise\s+DeprecationWarning',
            r'@deprecated',
        ]

        for pattern in breaking_indicators:
            if re.search(pattern, code, re.IGNORECASE):
                return True
        return False

    def _calculate_score(self, result: ValidationResult) -> float:
        """Calculate compliance score (0.0-1.0)"""
        score = 1.0

        # Deduct for errors (0.2 each)
        score -= len(result.errors) * 0.2

        # Deduct for warnings (0.1 each)
        score -= len(result.warnings) * 0.1

        # Bonus for meeting requirements/criteria
        if result.requirements_total > 0:
            req_score = result.requirements_met / result.requirements_total
            score = score * 0.5 + req_score * 0.5

        return max(0.0, min(1.0, score))

    def _generate_summary(self, result: ValidationResult, content_type: str) -> str:
        """Generate human-readable summary"""
        status = "PASSED" if result.passed else "FAILED"
        summary = f"Validation {status} (score: {result.score:.2%})\n\n"

        if result.requirements_total > 0:
            summary += f"Requirements: {result.requirements_met}/{result.requirements_total} met\n"

        if result.criteria_total > 0:
            summary += f"Success Criteria: {result.criteria_met}/{result.criteria_total} covered\n"

        if result.errors:
            summary += f"\nErrors ({len(result.errors)}):\n"
            for err in result.errors:
                summary += f"  - {err.message}\n"

        if result.warnings:
            summary += f"\nWarnings ({len(result.warnings)}):\n"
            for warn in result.warnings[:3]:  # First 3
                summary += f"  - {warn.message}\n"

        return summary

    def _parse_json_array(self, content: str) -> List[Dict[str, Any]]:
        """Parse JSON array from LLM response"""
        import json

        # Try to extract JSON from code blocks
        json_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1)
        else:
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                content = json_match.group(0)

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return []


__all__ = [
    "SpecValidator",
    "ParsedSpec",
    "ValidationResult",
    "ValidationIssue",
    "ValidationLevel"
]
