"""
Universal LLM Provider using LiteLLM
Supports 100+ AI providers with unified API, caching, and fallbacks.
"""

import os
from typing import Dict, Any, Optional, List
from pathlib import Path
import json
from src.agentic.core.utils.logging_utils import log_event

# Observability
from src.agentic.core.observability.tracer import tracer

try:
    from litellm import completion, acompletion
    from litellm.caching import Cache
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False
    log_event("LiteLLM not installed. Run: pip install litellm", component="litellm_provider", level="warning")

from pydantic import BaseModel


class ProviderConfig(BaseModel):
    """Configuration for an AI provider"""
    name: str
    models: List[str]
    enabled: bool = True
    api_key_env: Optional[str] = None
    supports_caching: bool = False
    supports_structured_output: bool = False
    supports_extended_thinking: bool = False
    supports_video: bool = False
    cost_per_1k_tokens: float = 0.0
    priority: int = 100  # Lower = higher priority


class UniversalLLMProvider:
    """
    Universal AI Provider using LiteLLM.

    Supports:
    - 100+ AI providers (Claude, GPT, Gemini, DeepSeek, etc.)
    - Automatic fallbacks (API -> Ollama)
    - Prompt caching (90% cost savings on Claude)
    - Feature detection (use best available features)
    - Cost tracking
    """

    def __init__(self, default_model: str = "ollama/qwen2.5-coder:32b"):
        if not LITELLM_AVAILABLE:
            raise ImportError("LiteLLM not installed. Run: pip install litellm anthropic openai google-generativeai")

        self.default_model = default_model
        self.cache_enabled = True

        # Setup cache (1 hour TTL)
        if self.cache_enabled:
            try:
                import litellm
                litellm.enable_cache()
                # LiteLLM manages its own cache instance, we just enable it
            except Exception as e:
                # Silent fail for cache in production, it's an optimization not a blocker
                pass

        # Load provider configs
        self.providers = self._load_provider_configs()

    def _load_provider_configs(self) -> Dict[str, ProviderConfig]:
        """Load all available provider configurations"""
        return {
            # TIER 1: Premium API Providers
            "claude": ProviderConfig(
                name="Claude (Anthropic)",
                models=[
                    "claude-3-5-sonnet-20241022",
                    "claude-3-opus-20240229",
                    "claude-3-sonnet-20240229",
                    "claude-3-haiku-20240307"
                ],
                api_key_env="ANTHROPIC_API_KEY",
                supports_caching=True,  # 90% savings!
                supports_structured_output=True,
                supports_extended_thinking=True,
                cost_per_1k_tokens=3.0,
                priority=1  # Highest priority if available
            ),

            "openai": ProviderConfig(
                name="OpenAI",
                models=[
                    "gpt-4o",
                    "gpt-4o-mini",
                    "gpt-4-turbo",
                    "o1-preview",
                    "o1-mini"
                ],
                api_key_env="OPENAI_API_KEY",
                supports_caching=False,  # OpenAI has different caching
                supports_structured_output=True,
                cost_per_1k_tokens=2.5,
                priority=2
            ),

            "gemini": ProviderConfig(
                name="Google Gemini",
                models=[
                    "gemini-2.0-flash-exp",
                    "gemini-1.5-pro",
                    "gemini-1.5-flash"
                ],
                api_key_env="GEMINI_API_KEY",
                supports_video=True,
                supports_extended_thinking=True,
                cost_per_1k_tokens=1.0,
                priority=3
            ),

            "deepseek": ProviderConfig(
                name="DeepSeek",
                models=[
                    "deepseek-chat",
                    "deepseek-coder"
                ],
                api_key_env="DEEPSEEK_API_KEY",
                cost_per_1k_tokens=0.14,  # Very cheap!
                priority=4
            ),

            # TIER 2: Local Ollama (Always available)
            "ollama": ProviderConfig(
                name="Ollama (Local)",
                models=[
                    "ollama/qwen2.5-coder:32b",
                    "ollama/deepseek-coder:33b",
                    "ollama/llama3.1:70b"
                ],
                enabled=True,
                supports_caching=False,
                cost_per_1k_tokens=0.0,  # FREE!
                priority=99  # Fallback
            )
        }

    def is_provider_available(self, provider_name: str) -> bool:
        """Check if a provider is available (API key set)"""
        config = self.providers.get(provider_name)
        if not config or not config.enabled:
            return False

        # Ollama is always available (local)
        if provider_name == "ollama":
            return True

        # Check if API key is set
        if config.api_key_env:
            return bool(os.getenv(config.api_key_env))

        return False

    def get_available_providers(self) -> List[str]:
        """Get list of currently available providers"""
        return [
            name for name in self.providers.keys()
            if self.is_provider_available(name)
        ]

    def select_best_model(self, task_type: str = "general", quality: str = "high") -> str:
        """
        Select best available model based on task type and quality needs.

        Args:
            task_type: "planning", "coding", "verification", "general"
            quality: "high", "medium", "low"

        Returns:
            Model name (e.g., "claude-3-5-sonnet-20241022" or "ollama/qwen2.5-coder:32b")
        """
        available = self.get_available_providers()

        if not available:
            return self.default_model

        # Sort providers by priority
        sorted_providers = sorted(
            [(name, self.providers[name]) for name in available],
            key=lambda x: x[1].priority
        )

        # High quality: use premium providers
        if quality == "high":
            for name, config in sorted_providers:
                if name != "ollama":  # Skip fallback
                    return config.models[0]  # Return first model

        # Medium: use cheaper options or local
        if quality == "medium":
            for name, config in sorted_providers:
                if name in ["gemini", "deepseek", "ollama"]:
                    return config.models[0]

        # Low or fallback: use local
        return self.providers["ollama"].models[0]

    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        use_caching: bool = True,
        use_structured_output: bool = False,
        response_schema: Optional[Dict] = None,
        fallback_models: Optional[List[str]] = None,
        temperature: float = 0.0,
        max_tokens: int = 4096
    ) -> Dict[str, Any]:
        """
        Generate text using LiteLLM with all features.

        Args:
            prompt: Input prompt
            model: Model to use (auto-selects if None)
            use_caching: Enable prompt caching (Claude only)
            use_structured_output: Use JSON schema (Claude/OpenAI)
            response_schema: Pydantic model schema for structured output
            fallback_models: List of fallback models if primary fails
            temperature: Sampling temperature
            max_tokens: Max tokens to generate

        Returns:
            Response dict with:
                - content: Generated text
                - model: Model used
                - cached: Whether response was cached
                - cost: Estimated cost
                - provider: Provider name
        """
        # Auto-select model if not specified
        if model is None:
            model = self.select_best_model()

        # Build fallback chain
        if fallback_models is None:
            fallback_models = [
                "claude-3-5-sonnet-20241022",
                "gpt-4o",
                "ollama/qwen2.5-coder:32b"  # Always have local fallback
            ]

        # Prepare messages
        messages = [{"role": "user", "content": prompt}]

        # Build kwargs
        kwargs = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "fallbacks": fallback_models
        }

        # Add caching if supported
        if use_caching and self._supports_caching(model):
            kwargs["cache"] = {"ttl": 3600}

        # Add structured output if requested
        if use_structured_output and response_schema:
            kwargs["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "response_schema",
                    "schema": response_schema
                }
            }

        try:
            # Call LiteLLM
            response = await acompletion(**kwargs)

            # Extract response data
            result = {
                "content": response.choices[0].message.content,
                "model": response.model,
                "cached": getattr(response, "cached", False),
                "cost": self._calculate_cost(response),
                "provider": self._get_provider_name(response.model),
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }

            # Trace success
            tracer.trace_generation(
                name="llm-generation",
                model=result["model"],
                input_data=prompt,
                output_data=result["content"],
                metadata={
                    "cached": result["cached"],
                    "cost": result["cost"],
                    "provider": result["provider"]
                }
            )

            return result

        except Exception as e:
            # Fallback to local if all fails
            log_event(f"LiteLLM failed: {e}", component="litellm_provider", level="error")

            # Trace failure
            tracer.trace_generation(
                name="llm-generation-failed",
                model=model,
                input_data=prompt,
                output_data=str(e),
                metadata={"error": str(e)}
            )

            log_event("Falling back to local Ollama", component="litellm_provider", level="warning")

            kwargs["model"] = "ollama/qwen2.5-coder:32b"
            kwargs["fallbacks"] = []

            response = await acompletion(**kwargs)

            return {
                "content": response.choices[0].message.content,
                "model": response.model,
                "cached": False,
                "cost": 0.0,
                "provider": "ollama",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }

    def _supports_caching(self, model: str) -> bool:
        """Check if model supports prompt caching"""
        if "claude" in model.lower():
            return True
        return False

    def _get_provider_name(self, model: str) -> str:
        """Extract provider name from model string"""
        if "claude" in model.lower():
            return "claude"
        if "gpt" in model.lower() or "o1" in model.lower():
            return "openai"
        if "gemini" in model.lower():
            return "gemini"
        if "deepseek" in model.lower():
            return "deepseek"
        if "ollama" in model.lower():
            return "ollama"
        return "unknown"

    def _calculate_cost(self, response) -> float:
        """Calculate estimated cost of request"""
        try:
            # LiteLLM provides cost tracking
            if hasattr(response, "_hidden_params"):
                cost = response._hidden_params.get("response_cost", 0.0)
                return cost
        except:
            pass
        return 0.0

    def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all providers"""
        status = {}
        for name, config in self.providers.items():
            status[name] = {
                "name": config.name,
                "enabled": config.enabled,
                "available": self.is_provider_available(name),
                "models": config.models,
                "features": {
                    "caching": config.supports_caching,
                    "structured_output": config.supports_structured_output,
                    "extended_thinking": config.supports_extended_thinking,
                    "video": config.supports_video
                },
                "cost_per_1k": config.cost_per_1k_tokens,
                "priority": config.priority
            }
        return status


# Singleton instance
_default_provider = None

def get_provider() -> UniversalLLMProvider:
    """Get default provider instance"""
    global _default_provider
    if _default_provider is None:
        _default_provider = UniversalLLMProvider()
    return _default_provider
