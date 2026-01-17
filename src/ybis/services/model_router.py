"""
Model Router - Routes LLM requests to appropriate models based on cost/latency policies.

Provides intelligent model selection based on:
- Task complexity (tier)
- Cost constraints
- Latency requirements
- Model availability
"""


from ..services.policy import get_policy_provider


class ModelRouter:
    """
    Model Router - Routes LLM requests to appropriate models.

    Routing strategies:
    - Cost optimization: Use cheaper models for simple tasks
    - Latency optimization: Use faster models for real-time needs
    - Quality optimization: Use best models for critical tasks
    """

    def __init__(self):
        """Initialize model router."""
        self.policy = get_policy_provider()

    def get_model_for_task(
        self,
        task_tier: int | None = None,
        task_type: str = "planning",
        cost_constraint: str | None = None,
        latency_constraint: str | None = None,
    ) -> str:
        """
        Get appropriate model for task.

        Args:
            task_tier: Task tier (0=simple, 1=medium, 2=complex)
            task_type: Task type (planning, coding, verification, etc.)
            cost_constraint: Cost constraint (low, medium, high)
            latency_constraint: Latency constraint (fast, medium, slow)

        Returns:
            Model name (e.g., "ollama/llama3.2:3b")
        """
        policy_config = self.policy.get_policy()
        llm_config = policy_config.get("llm", {})
        router_config = policy_config.get("model_router", {})

        # Get model tiers from policy
        tiers = router_config.get("tiers", {})

        # Determine tier if not provided
        if task_tier is None:
            task_tier = self._infer_tier(task_type)

        # Get model for tier
        tier_config = tiers.get(f"tier_{task_tier}", {})

        # Apply constraints
        if cost_constraint == "low":
            model = tier_config.get("cost_optimized", tier_config.get("default"))
        elif latency_constraint == "fast":
            model = tier_config.get("latency_optimized", tier_config.get("default"))
        else:
            model = tier_config.get("default")

        # Fallback to LLM config defaults
        if not model:
            if task_type == "planning":
                model = llm_config.get("planner_model", "ollama/llama3.2:3b")
            elif task_type == "coding":
                model = llm_config.get("coder_model", "ollama/qwen2.5-coder:32b")
            else:
                model = llm_config.get("planner_model", "ollama/llama3.2:3b")

        return model

    def _infer_tier(self, task_type: str) -> int:
        """
        Infer task tier from task type.

        Args:
            task_type: Task type

        Returns:
            Task tier (0, 1, or 2)
        """
        # Simple heuristic: planning is usually tier 0, coding is tier 1-2
        if task_type in ["planning", "spec"]:
            return 0
        elif task_type in ["coding", "execution"]:
            return 1
        else:
            return 2

    def get_api_base(self, model: str) -> str:
        """
        Get API base URL for model.

        Args:
            model: Model name

        Returns:
            API base URL
        """
        policy_config = self.policy.get_policy()
        llm_config = policy_config.get("llm", {})

        # Check if model is Ollama (local)
        if model.startswith("ollama/"):
            return llm_config.get("api_base", "http://localhost:11434")

        # Check for other providers
        if "openai" in model.lower():
            return llm_config.get("openai_api_base", "https://api.openai.com/v1")
        elif "anthropic" in model.lower():
            return llm_config.get("anthropic_api_base", "https://api.anthropic.com/v1")

        # Default: Ollama
        return llm_config.get("api_base", "http://localhost:11434")

    def get_model_cost(self, model: str, tokens: int) -> float:
        """
        Estimate cost for model usage.

        Args:
            model: Model name
            tokens: Number of tokens

        Returns:
            Estimated cost (in USD, or 0.0 for local models)
        """
        # Local models (Ollama) are free
        if model.startswith("ollama/"):
            return 0.0

        # For cloud models, estimate based on model type
        # This is a simplified estimation
        if "gpt-4" in model.lower():
            # GPT-4: ~$0.03 per 1K tokens
            return (tokens / 1000) * 0.03
        elif "gpt-3.5" in model.lower():
            # GPT-3.5: ~$0.002 per 1K tokens
            return (tokens / 1000) * 0.002
        elif "claude" in model.lower():
            # Claude: ~$0.015 per 1K tokens
            return (tokens / 1000) * 0.015
        else:
            # Unknown model: assume free or low cost
            return 0.0

    def get_model_latency_estimate(self, model: str) -> float:
        """
        Estimate latency for model (in seconds).

        Args:
            model: Model name

        Returns:
            Estimated latency in seconds
        """
        # Local models (Ollama) are typically faster
        if model.startswith("ollama/"):
            if "3b" in model or "1b" in model:
                return 0.5  # Fast small models
            elif "7b" in model or "8b" in model:
                return 1.0  # Medium models
            else:
                return 2.0  # Large models

        # Cloud models have network latency
        if "gpt-4" in model.lower():
            return 3.0  # GPT-4 is slower
        elif "gpt-3.5" in model.lower():
            return 1.5  # GPT-3.5 is faster
        elif "claude" in model.lower():
            return 2.0  # Claude is medium

        # Default: assume medium latency
        return 2.0


# Global model router instance
_model_router: ModelRouter | None = None


def get_model_router() -> ModelRouter:
    """Get global model router instance."""
    global _model_router
    if _model_router is None:
        _model_router = ModelRouter()
    return _model_router


