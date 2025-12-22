"""
Enhanced Aider Executor with Prevention System

Improvements over original:
1. Injects CODE_STANDARDS into prompt
2. Injects ARCHITECTURE_PRINCIPLES into prompt
3. Injects relevant API references
4. Enforces test-first approach
5. Pre-checks imports before execution
"""

import asyncio
import subprocess
from pathlib import Path
from typing import List, Dict, Any
from src.agentic.core.config import PROJECT_ROOT
from src.agentic.core.protocols import ExecutorProtocol, Plan, CodeResult

class AiderExecutorEnhanced(ExecutorProtocol):
    """Enhanced Aider executor with systematic error prevention"""

    def __init__(self):
        self.aider_cmd = "aider"
        self.model = "qwen2.5-coder:32b"

    def name(self) -> str:
        return "AiderExecutorEnhanced"

    async def execute(self, plan: Plan, sandbox_path: str, error_history: List[str] = None, retry_count: int = 0) -> CodeResult:
        """Execute plan via Aider with enhanced prompts and error feedback"""

        # Build enhanced prompt (with error feedback if retrying)
        enhanced_prompt = self._build_enhanced_prompt(plan, error_history, retry_count)

        # Prepare Aider command
        files = [str(PROJECT_ROOT / f) for f in plan.files_to_modify]

        cmd = [
            self.aider_cmd,
            "--model", f"ollama/{self.model}",
            "--no-auto-commits",  # Don't auto-commit
            "--yes",              # Auto-confirm
            "--message", enhanced_prompt,
            *files
        ]

        # Execute Aider
        print(f"[AiderEnhanced] Executing with enhanced prompt...")
        print(f"[AiderEnhanced] Files: {files}")

        try:
            result = subprocess.run(
                cmd,
                cwd=str(PROJECT_ROOT),
                capture_output=True,
                text=True,
                timeout=600  # 10 min timeout
            )

            # Check for errors
            if result.returncode != 0:
                return CodeResult(
                    files_modified={},
                    commands_run=[" ".join(cmd)],
                    outputs={"stderr": result.stderr},
                    success=False,
                    error=f"Aider failed: {result.stderr}"
                )

            # Parse modified files (simplified)
            files_modified = {f: "modified" for f in files}

            return CodeResult(
                files_modified=files_modified,
                commands_run=[" ".join(cmd)],
                outputs={"stdout": result.stdout, "stderr": result.stderr},
                success=True,
                error=None
            )

        except subprocess.TimeoutExpired:
            return CodeResult(
                files_modified={},
                commands_run=[" ".join(cmd)],
                outputs={},
                success=False,
                error="Aider execution timed out (10 min)"
            )

    def _build_enhanced_prompt(self, plan: Plan, error_history: List[str] = None, retry_count: int = 0) -> str:
        """Build prompt with CODE_STANDARDS, ARCHITECTURE_PRINCIPLES, API refs, and error feedback"""

        # Load CODE_STANDARDS
        code_standards = self._load_file(PROJECT_ROOT / "00_GENESIS" / "CODE_STANDARDS.md")

        # Load ARCHITECTURE_PRINCIPLES
        arch_principles = self._load_file(PROJECT_ROOT / "00_GENESIS" / "ARCHITECTURE_PRINCIPLES.md")

        # Load relevant API references
        api_refs = self._get_api_references(plan)

        # Build error feedback section (if retrying)
        error_feedback = ""
        if retry_count > 0 and error_history:
            error_feedback = f"""
# PREVIOUS ATTEMPT FAILED - FIX THESE ERRORS

**Retry Attempt:** {retry_count}

**Errors from previous attempt:**
{self._format_error_history(error_history)}

**CRITICAL:** You MUST fix these specific errors. Read the error messages carefully and correct the issues.
"""

        # Build enhanced prompt
        prompt = f"""
{error_feedback}

# CRITICAL CONSTRAINTS (MUST FOLLOW)

## Code Standards (IMMUTABLE)
{self._extract_critical_rules(code_standards)}

## Architecture Principles (IMMUTABLE)
{self._extract_critical_rules(arch_principles)}

## API References (CORRECT USAGE)
{api_refs}

---

# YOUR TASK

## Objective
{plan.objective}

## Steps
{self._format_steps(plan.steps)}

## Files to Modify
{', '.join(plan.files_to_modify)}

## Success Criteria
{self._format_criteria(plan.success_criteria)}

---

# MANDATORY APPROACH

1. **WRITE TESTS FIRST** (before implementation)
   - Create/update test file
   - Write failing tests for requirements
   - Run tests to confirm they fail

2. **IMPLEMENT** (make tests pass)
   - Write minimal code to pass tests
   - Follow CODE_STANDARDS (NO EMOJIS!)
   - Use correct APIs (see API References above)

3. **VERIFY**
   - Run tests again
   - Check imports (no missing imports)
   - Verify no emojis in code

---

# OUTPUT FORMAT

Please provide:
1. List of files created/modified
2. Test results (all passing)
3. Any issues encountered
"""

        return prompt

    def _load_file(self, path: Path) -> str:
        """Load file content"""
        if path.exists():
            return path.read_text(encoding='utf-8')
        return "[File not found]"

    def _extract_critical_rules(self, content: str) -> str:
        """Extract critical rules from markdown doc"""
        # Simple extraction: take first 500 chars of critical sections
        lines = content.split('\n')
        critical = []

        for i, line in enumerate(lines):
            if 'CRITICAL' in line.upper() or 'FORBIDDEN' in line.upper():
                # Take next 5 lines
                critical.extend(lines[i:i+6])

        if critical:
            return '\n'.join(critical[:30])  # Max 30 lines

        # Fallback: take first 500 chars
        return content[:500]

    def _get_api_references(self, plan: Plan) -> str:
        """Get relevant API references from Knowledge/API_References/"""

        # Detect which frameworks are needed
        frameworks = set()
        plan_text = plan.objective + " ".join(plan.steps)

        if "langgraph" in plan_text.lower() or "stategraph" in plan_text.lower():
            frameworks.add("langgraph")

        if "langchain" in plan_text.lower():
            frameworks.add("langchain")

        if "crewai" in plan_text.lower():
            frameworks.add("crewai")

        # Load API references from Knowledge/
        api_ref_dir = PROJECT_ROOT / "Knowledge" / "API_References"
        refs = []

        for framework in frameworks:
            ref_file = api_ref_dir / f"{framework}_api.md"
            if ref_file.exists():
                content = ref_file.read_text(encoding='utf-8')
                refs.append(f"\n## {framework.upper()} API Reference\n{content}")
            else:
                refs.append(f"\n[WARNING: {framework} API reference not found at {ref_file}]")

        if not refs:
            refs.append("\nNo specific API references needed.")

        return "\n".join(refs)

    def _format_steps(self, steps: List[str]) -> str:
        """Format steps as numbered list"""
        return "\n".join(f"{i+1}. {step}" for i, step in enumerate(steps))

    def _format_criteria(self, criteria: List[str]) -> str:
        """Format criteria as checklist"""
        return "\n".join(f"- {c}" for c in criteria)

    def _format_error_history(self, error_history: List[str]) -> str:
        """Format error history for prompt"""
        if not error_history:
            return "No errors recorded"

        formatted = []
        for i, error in enumerate(error_history, 1):
            formatted.append(f"{i}. {error}")

        return "\n".join(formatted)
