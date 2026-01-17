"""
Local Coder - Native Ollama-based code executor.

Implements ExecutorProtocol using LiteLLM + Ollama for code generation.
Uses "Rewrite" strategy: LLM returns full file content after changes.
"""

import logging
import time
from pathlib import Path

from ..contracts import ExecutorProtocol, ExecutorReport, Plan, RunContext
from ..services.file_cache import get_file_cache
from ..services.llm_cache import get_llm_cache
from ..services.llm_cache_gptcache import get_llm_cache_hybrid
from ..services.policy import get_policy_provider
from ..services.resilience import resilient
from ..syscalls import write_file
from ..syscalls.journal import append_event

logger = logging.getLogger(__name__)


class LocalCoderExecutor:
    """
    Local Coder Executor - Uses Ollama for code generation.

    Strategy: Rewrite entire file with changes applied.
    """

    def __init__(self, model: str | None = None, api_base: str | None = None):
        """
        Initialize local coder.

        Args:
            model: Model name (default from policy config)
            api_base: API base URL (default from policy config)
        """
        policy_provider = get_policy_provider()
        llm_config = policy_provider.get_llm_config()

        self.model = model or llm_config.get("coder_model", "ollama/qwen2.5-coder:32b")
        self.api_base = api_base or llm_config.get("api_base", "http://localhost:11434")

    def is_available(self) -> bool:
        """
        Check if Local Coder is available (Ollama is running).

        Returns:
            True if Ollama is accessible, False otherwise
        """
        logger.debug(f"Checking LocalCoder availability: model={self.model}, api_base={self.api_base}")
        try:
            import httpx

            # Try to ping Ollama API
            response = httpx.get(f"{self.api_base}/api/tags", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    def generate_code(self, ctx: RunContext, plan: Plan, error_context: str | None = None) -> ExecutorReport:
        """
        Generate code using Ollama.

        Args:
            ctx: Run context
            plan: Execution plan
            error_context: Optional error context from previous attempts

        Returns:
            ExecutorReport with execution results
        """
        files_changed = []
        errors = []

        from ..constants import PROJECT_ROOT

        # Use worktree if available (ctx.run_path is already a worktree)
        # Otherwise fall back to PROJECT_ROOT
        code_root = ctx.run_path
        if not (code_root / ".git").exists():
            # Not a worktree, use PROJECT_ROOT
            code_root = PROJECT_ROOT

        # STRICT: Only modify files in plan.files
        # Filter out any files not explicitly in the plan
        # BLOCK critical files completely - executor is not mature enough
        protected_files = {
            "pyproject.toml",
            "requirements.txt",
            "setup.py",
            "setup.cfg",
            ".gitignore",
            ".env",
            ".env.example",
            "docker-compose.yml",
            "Dockerfile",
        }

        # Invalid patterns (directories, globs, etc.)
        invalid_patterns = [
            "all", "of", "the", "existing", "code",
            "tests",  # Directory, not a file
            "*.rst",  # Glob pattern
            "pytest.ini",  # Config file
        ]
        allowed_extensions = {".py", ".md", ".yaml", ".yml", ".json", ".toml", ".txt"}

        plan_files = plan.files or []
        explicit_paths = {f for f in plan_files if "/" in f or "\\" in f}
        explicit_basenames = {Path(f).name for f in explicit_paths}
        filtered_files = []
        for file_path_str in plan_files:
            if ("/" not in file_path_str and "\\" not in file_path_str) and Path(
                file_path_str
            ).name in explicit_basenames:
                logger.info(f"Skipping ambiguous basename (explicit path exists): {file_path_str}")
                continue
            filtered_files.append(file_path_str)

        validated_files = []
        for file_path_str in filtered_files:
            # Skip invalid patterns
            if not file_path_str or file_path_str in invalid_patterns or file_path_str.endswith("*"):
                logger.warning(f"Skipping invalid file pattern: {file_path_str}")
                continue
            suffix = Path(file_path_str).suffix
            if suffix and suffix not in allowed_extensions:
                logger.warning(f"Skipping unsupported file extension: {file_path_str}")
                continue

            # BLOCK protected files completely (executor is not mature enough)  
            file_name = Path(file_path_str).name
            if file_name in protected_files:
                logger.warning(f"BLOCKED: Protected file {file_path_str}. Executor is not allowed to modify critical config files.")
                # Journal: Protected file blocked
                append_event(
                    ctx.run_path,
                    "FILE_SKIPPED_PROTECTED",
                    {
                        "file": file_path_str,
                        "reason": "Protected file - executor not allowed to modify critical config files",
                    },
                    trace_id=ctx.trace_id,
                )
                continue

            # Check if file exists in PROJECT_ROOT
            possible_paths = [
                file_path_str,
                f"src/ybis/{file_path_str}",
                file_path_str.replace("\\", "/"),
            ]
            if file_path_str.startswith("/"):
                possible_paths.append(file_path_str[1:])

            found = False
            for path_attempt in possible_paths:
                if (PROJECT_ROOT / path_attempt).exists():
                    validated_files.append(path_attempt)
                    found = True
                    break

            if not found:
                # Try to resolve by filename in src/ybis
                file_matches = list((PROJECT_ROOT / "src" / "ybis").rglob(file_name))
                if len(file_matches) == 1:
                    resolved = file_matches[0].relative_to(PROJECT_ROOT)
                    validated_files.append(str(resolved))
                    found = True
                elif len(file_matches) > 1:
                    logger.warning(
                        f"Multiple matches for {file_name}, skipping: {file_path_str}"
                    )
                    continue

            if not found:
                suffix = Path(file_path_str).suffix
                if suffix and suffix not in allowed_extensions:
                    logger.warning(
                        f"Skipping unsupported file extension for creation: {file_path_str}"
                    )
                    continue
                # Allow creation of new files (default to services/ if no path)
                if "/" not in file_path_str and "\\" not in file_path_str:
                    services_dir = PROJECT_ROOT / "src" / "ybis" / "services"
                    if services_dir.exists():
                        create_path = Path("src/ybis/services") / file_name
                        validated_files.append(str(create_path))
                        append_event(
                            ctx.run_path,
                            "FILE_MARKED_FOR_CREATE",
                            {
                                "file": str(create_path),
                                "reason": "defaulted_to_services_dir",
                            },
                            trace_id=ctx.trace_id,
                        )
                        continue

                validated_files.append(file_path_str)
                append_event(
                    ctx.run_path,
                    "FILE_MARKED_FOR_CREATE",
                    {
                        "file": file_path_str,
                        "reason": "not_found_in_project",
                    },
                    trace_id=ctx.trace_id,
                )

        if not validated_files:
            return ExecutorReport(
                task_id=ctx.task_id,
                run_id=ctx.run_id,
                success=False,
                files_changed=[],
                commands_run=[],
                error="No valid files found in plan to modify",
            )
        append_event(
            ctx.run_path,
            "PLAN_FILES_RESOLVED",
            {
                "plan_files": plan_files,
                "validated_files": validated_files,
            },
            trace_id=ctx.trace_id,
        )

        # Only process validated files from plan
        for file_path_str in validated_files:
            try:
                file_path = Path(file_path_str)

                if file_path.is_absolute():
                    try:
                        relative_path = file_path.relative_to(PROJECT_ROOT)
                        file_path = (code_root / relative_path).resolve()
                    except ValueError:
                        file_path = file_path.resolve()
                else:
                    file_path = (code_root / file_path).resolve()

                # Read current file content with caching
                file_cache = get_file_cache()
                current_content = None

                # Try cache first
                if file_path.exists():
                    current_content = file_cache.get(file_path)
                    if current_content is None:
                        current_content = file_path.read_text(encoding="utf-8")
                        file_cache.set(file_path, current_content)
                else:
                    # Try reading from PROJECT_ROOT
                    project_file = PROJECT_ROOT / file_path_str
                    if project_file.exists():
                        current_content = file_cache.get(project_file)
                        if current_content is None:
                            current_content = project_file.read_text(encoding="utf-8")
                            file_cache.set(project_file, current_content)
                        logger.info(f"File not in worktree, read from PROJECT_ROOT: {file_path_str}")

                        # Also copy to worktree for consistency
                        file_path.parent.mkdir(parents=True, exist_ok=True)
                        file_path.write_text(current_content, encoding="utf-8")

                        # Journal event
                        append_event(
                            ctx.run_path,
                            "FILE_SYNCED_FROM_PROJECT_ROOT",
                            {
                                "file": file_path_str,
                                "content_length": len(current_content),
                            },
                            trace_id=ctx.trace_id,
                        )
                    else:
                        current_content = ""
                        logger.warning(f"File not found in worktree or PROJECT_ROOT: {file_path_str}")

                # Generate new content using LLM
                new_content = self._generate_file_content(
                    ctx, file_path, current_content, plan.objective, plan.instructions, error_context
                )

                # Write file using syscall
                write_file(file_path, new_content, ctx)
                files_changed.append(str(file_path))

            except Exception as e:
                errors.append(f"Failed to modify {file_path_str}: {e!s}")

        return ExecutorReport(
            task_id=ctx.task_id,
            run_id=ctx.run_id,
            success=len(errors) == 0,
            files_changed=files_changed,
            commands_run=[f"LocalCoder: {self.model}"],
            error="\n".join(errors) if errors else None,
        )

    def _generate_file_content(
        self, ctx: RunContext, file_path: Path, current_content: str, objective: str, instructions: str, error_context: str | None = None
    ) -> str:
        """
        Generate file content using LLM.

        Args:
            file_path: Path to file
            current_content: Current file content
            objective: Task objective
            instructions: Additional instructions
            error_context: Optional error context from previous attempts

        Returns:
            New file content
        """
        try:
            import litellm

            error_prompt = ""
            if error_context:
                error_prompt = f"\n\nPrevious attempt failed with errors:\n{error_context}\nPlease fix these errors."

            # Calculate file size to determine strategy
            line_count = current_content.count('\n') + 1

            # For large files (>1000 lines), use focused editing strategy
            if line_count > 1000:
                # Extract relevant context (first 200 lines + last 200 lines)
                lines = current_content.split('\n')
                context_lines = [*lines[:200], '... (middle content preserved, not shown) ...', *lines[-200:]]
                context_content = '\n'.join(context_lines)

                prompt = f"""You are a code editor. Apply MINIMAL changes to the specified file.

CRITICAL RULES:
- PRESERVE all existing code structure, imports, classes, and functions
- ONLY modify the specific parts mentioned in the instructions
- Do NOT rewrite the entire file - only change what's necessary
- Keep all existing functionality intact
- Maintain the same code style and structure
- Do NOT add new files or modify other files

File: {file_path.name} ({line_count} lines - showing context only)
Objective: {objective}
Instructions: {instructions}
{error_prompt}

File context (first 200 + last 200 lines):
```
{context_content}
```

IMPORTANT: Return the COMPLETE file content, but ONLY modify the parts specified in the instructions. Preserve all other code exactly as it is. Do not include explanations or markdown code blocks."""
            else:
                # For smaller files, show full content but emphasize preservation
                prompt = f"""You are a code editor. Apply MINIMAL changes to the specified file.

CRITICAL RULES:
- PRESERVE all existing code structure, imports, classes, and functions
- ONLY modify the specific parts mentioned in the instructions
- Do NOT rewrite the entire file - only change what's necessary
- Keep all existing functionality intact
- Maintain the same code style and structure
- Do NOT add new files or modify other files

File: {file_path.name}
Objective: {objective}
Instructions: {instructions}
{error_prompt}

Current file content (PRESERVE THIS STRUCTURE):
```
{current_content}
```

IMPORTANT: Return the COMPLETE file content, but ONLY modify the parts specified in the instructions. Preserve all other code exactly as it is. Do not include explanations or markdown code blocks."""

            # Check LLM cache first
            # Use hybrid cache (GPTCache if available, else exact-match)
            try:
                llm_cache = get_llm_cache_hybrid()
            except Exception:
                # Fallback to exact-match cache
                llm_cache = get_llm_cache()
            cached_response = llm_cache.get(self.model, prompt, temperature=0.0)

            if cached_response:
                logger.info(f"Using cached LLM response for {file_path.name}")
                new_content = cached_response
                elapsed_ms = 0  # Cache hit, no time spent
            else:
                # Journal: LLM request
                start_time = time.time()
                append_event(
                    ctx.run_path,
                    "LLM_REQUEST",
                    {
                        "model": self.model,
                        "file": file_path.name,
                        "prompt_length": len(prompt),
                        "input_content_length": len(current_content),
                    },
                    trace_id=ctx.trace_id,
                )

                @resilient(
                    breaker_name="ollama",
                    rate_limit=(2.0, 5),  # 2 req/sec, burst of 5
                )
                def _call_llm():
                    return litellm.completion(
                        model=self.model,
                        messages=[
                            {"role": "user", "content": prompt},
                        ],
                        api_base=self.api_base,
                        timeout=30,
                    )

                response = _call_llm()
                elapsed_ms = (time.time() - start_time) * 1000

                new_content = response.choices[0].message.content.strip()

                # Cache the response
                llm_cache.set(self.model, prompt, new_content, temperature=0.0)

            # Journal: LLM response
            append_event(
                ctx.run_path,
                "LLM_RESPONSE",
                {
                    "model": self.model,
                    "file": file_path.name,
                    "output_length": len(new_content),
                    "input_output_ratio": len(new_content) / len(current_content) if current_content else 0,
                    "response_time_ms": round(elapsed_ms, 2),
                },
                trace_id=ctx.trace_id,
            )

            # Journal: Empty response check
            if not new_content or len(new_content.strip()) < 10:
                append_event(
                    ctx.run_path,
                    "LLM_EMPTY_RESPONSE",
                    {
                        "model": self.model,
                        "file": file_path.name,
                        "input_length": len(current_content),
                    },
                    trace_id=ctx.trace_id,
                )
                logger.warning(f"LLM returned empty response for {file_path.name}")
                return current_content

            # Remove markdown code blocks if present
            if new_content.startswith("```"):
                lines = new_content.split("\n")
                # Remove first line (```python or ```)
                if lines[0].startswith("```"):
                    lines = lines[1:]
                # Remove last line (```)
                if lines and lines[-1].strip() == "```":
                    lines = lines[:-1]
                new_content = "\n".join(lines)

            file_suffix = file_path.suffix.lower()
            if file_suffix == ".py":
                # STRICT VALIDATION: Reject responses that are explanations, not code
                # Check for common explanation patterns
                explanation_patterns = [
                    "certainly", "please provide", "i can", "i will", "here is",
                    "here's", "let me", "i'll", "i would", "to apply", "to fix",
                    "the file", "the code", "you can", "we can", "we need"
                ]
                first_line_lower = new_content.split('\n')[0].lower() if new_content else ""
                if any(pattern in first_line_lower for pattern in explanation_patterns):
                    logger.error(
                        f"LLM returned explanation instead of code for {file_path.name}. "
                        f"First line: {new_content.split(chr(10))[0][:100]}"
                    )
                    # Journal: Explanation pattern detected
                    append_event(
                        ctx.run_path,
                        "LLM_EXPLANATION_DETECTED",
                        {
                            "model": self.model,
                            "file": file_path.name,
                            "first_line": new_content.split('\n')[0][:100] if new_content else "",
                        },
                        trace_id=ctx.trace_id,
                    )
                    # Return original content to prevent breaking the file
                    logger.warning(f"Returning original content for {file_path.name} to prevent breakage")
                    return current_content

            # Validation: Check if generated content is suspiciously different
            # If file was large and new content is much smaller, it's likely hallucination
            if line_count > 1000:
                new_line_count = new_content.count('\n') + 1
                size_ratio = len(new_content) / len(current_content) if current_content else 1.0

                # If new content is less than 50% of original, it's likely wrong
                if size_ratio < 0.5:
                    logger.warning(
                        f"Generated content for {file_path.name} is {size_ratio:.1%} of original size "
                        f"({new_line_count} vs {line_count} lines). This may be a hallucination. "
                        f"Returning original content to prevent breakage."
                    )
                    # Journal: Content validation failed
                    append_event(
                        ctx.run_path,
                        "CONTENT_VALIDATION_FAIL",
                        {
                            "file": file_path.name,
                            "original_size": len(current_content),
                            "new_size": len(new_content),
                            "ratio": round(size_ratio, 3),
                        },
                        trace_id=ctx.trace_id,
                    )
                    # Return original to prevent breaking the file
                    return current_content

            if file_suffix == ".py":
                # Additional validation: Check if response starts with Python keywords or imports
                # Valid Python files should start with imports, docstrings, or code
                valid_starts = ["import ", "from ", '"""', "'''", "#", "class ", "def ", "@"]
                first_non_empty_line = next((line for line in new_content.split('\n') if line.strip()), "")
                if (
                    first_non_empty_line
                    and not any(first_non_empty_line.strip().startswith(start) for start in valid_starts)
                    and (len(first_non_empty_line) > 100 or " " in first_non_empty_line[:20])
                ):
                    logger.warning(
                        f"Generated content for {file_path.name} doesn't start with valid Python. "
                        f"First line: {first_non_empty_line[:100]}. Returning original content."
                    )
                    return current_content

            return new_content

        except ImportError as e:
            raise ImportError("LiteLLM not installed. Run: pip install litellm") from e
        except Exception as e:
            raise Exception(f"LLM generation failed: {e!s}") from e


# Type check: LocalCoderExecutor implements ExecutorProtocol
def _type_check() -> None:
    """Type check helper."""
    _: ExecutorProtocol = LocalCoderExecutor()  # Type check only
