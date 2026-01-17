"""
Programmatic Tool Calling - Code-based tool orchestration (LOCAL).

Implements Programmatic Tool Calling pattern using LOCAL Ollama:
- Tools are defined as Python functions
- Agent orchestrates tools via code (not inference)
- Reduces inference overhead and context pollution
- Uses Ollama (local) instead of Anthropic API
"""

import json
import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)


class ProgrammaticToolOrchestrator:
    """
    Programmatic Tool Orchestrator - Code-based tool execution (LOCAL).

    Allows agents to orchestrate tools via Python code instead of
    inference-based tool calling. Reduces overhead and context pollution.
    Uses LOCAL Ollama (no API key required).
    """

    def __init__(self, model: str | None = None, api_base: str | None = None):
        """
        Initialize orchestrator.

        Args:
            model: Ollama model name (default from policy)
            api_base: Ollama API base URL (default from policy)
        """
        self.model = model
        self.api_base = api_base
        self.tools: dict[str, Callable[..., Any]] = {}
        self.tool_descriptions: dict[str, dict[str, Any]] = {}

    def register_tool(
        self,
        name: str,
        func: Callable[..., Any],
        description: str,
        input_schema: dict[str, Any] | None = None,
    ) -> None:
        """
        Register a tool for programmatic calling.

        Args:
            name: Tool name
            func: Tool function
            description: Tool description
            input_schema: JSON schema for inputs (optional)
        """
        logger.info(f"Registering programmatic tool: {name}")
        self.tools[name] = func
        self.tool_descriptions[name] = {
            "name": name,
            "description": description,
            "input_schema": input_schema or {},
        }

    def generate_tool_code(
        self,
        objective: str,
        available_tools: list[str] | None = None,
        model: str | None = None,
        api_base: str | None = None,
    ) -> str:
        """
        Generate Python code to orchestrate tools for an objective.

        Uses LOCAL Ollama to generate code that calls tools programmatically.

        Args:
            objective: Task objective
            available_tools: List of tool names to use (None = all)
            model: Ollama model to use (default from policy)
            api_base: Ollama API base URL (default from policy)

        Returns:
            Python code string that orchestrates tools
        """
        # Get model from policy if not provided
        if not model or not api_base:
            from ..services.policy import get_policy_provider

            policy_provider = get_policy_provider()
            llm_config = policy_provider.get_llm_config()
            model = model or llm_config.get("coder_model", "ollama/qwen2.5-coder:32b")
            api_base = api_base or llm_config.get("api_base", "http://localhost:11434")

        # Filter tools
        tools_to_use = available_tools or list(self.tools.keys())
        tool_descriptions = {
            name: desc
            for name, desc in self.tool_descriptions.items()
            if name in tools_to_use
        }

        # Build prompt for code generation
        system_prompt = """You are a code generator that creates Python code to orchestrate tools.

Generate Python code that:
1. Calls the available tools in the correct order
2. Handles tool outputs
3. Achieves the objective

Return ONLY the Python code, no explanations. Code should be executable."""

        user_prompt = f"""Objective: {objective}

Available tools:
{json.dumps(tool_descriptions, indent=2)}

Generate Python code to achieve this objective using the tools. Use the tools dict to call functions:
- tools['tool_name'](arg1, arg2, ...)
- Store results in variables
- Return final result as 'result' variable"""

        try:
            import litellm

            from ..services.resilience import ollama_retry

            @ollama_retry
            def _call_llm():
                return litellm.completion(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    api_base=api_base,
                    timeout=30,
                )

            response = _call_llm()
            code = response.choices[0].message.content.strip()

            # Extract code block if wrapped in markdown
            if "```python" in code:
                code = code.split("```python")[1].split("```")[0].strip()
            elif "```" in code:
                code = code.split("```")[1].split("```")[0].strip()

            return code
        except Exception as e:
            logger.error(f"Failed to generate programmatic tool code: {e}")
            raise

    def execute_tool_code(self, code: str, context: dict[str, Any] | None = None) -> Any:
        """
        Execute generated tool orchestration code.

        Args:
            code: Python code string
            context: Optional context dict (available as variables in code)

        Returns:
            Execution result
        """
        # Create safe execution environment
        safe_globals = {
            "__builtins__": __builtins__,
            "json": json,
            "tools": self.tools,
        }

        if context:
            safe_globals.update(context)

        try:
            # Execute code in safe environment
            exec(code, safe_globals)
            return safe_globals.get("result", None)
        except Exception as e:
            logger.error(f"Failed to execute tool code: {e}")
            raise

    def orchestrate(
        self,
        objective: str,
        available_tools: list[str] | None = None,
        context: dict[str, Any] | None = None,
    ) -> Any:
        """
        Orchestrate tools programmatically for an objective.

        Args:
            objective: Task objective
            available_tools: List of tool names to use (None = all)
            context: Optional context dict

        Returns:
            Orchestration result
        """
        # Generate code
        code = self.generate_tool_code(objective, available_tools)

        # Execute code
        result = self.execute_tool_code(code, context)

        return result


# Global instance
_orchestrator: ProgrammaticToolOrchestrator | None = None


def get_programmatic_orchestrator(model: str | None = None, api_base: str | None = None) -> ProgrammaticToolOrchestrator:
    """
    Get global programmatic tool orchestrator (LOCAL - no API key required).

    Args:
        model: Ollama model name (default from policy)
        api_base: Ollama API base URL (default from policy)

    Returns:
        ProgrammaticToolOrchestrator (always available, uses local Ollama)
    """
    global _orchestrator

    if _orchestrator is None:
        try:
            _orchestrator = ProgrammaticToolOrchestrator(model=model, api_base=api_base)
        except Exception as e:
            logger.warning(f"Failed to initialize Programmatic Tool Orchestrator: {e}")
            # Return a basic instance anyway
            _orchestrator = ProgrammaticToolOrchestrator()

    return _orchestrator

