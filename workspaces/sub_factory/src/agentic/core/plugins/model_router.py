"""
ModelRouter - The Brain's Traffic Control

Responsibility:
- Decides which model handles a task based on capability, risk, and hardware.
- Abstracts the provider (Local vs Cloud).
- Currently optimized for RTX 5090 (High-End Local).
"""

import os

from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    provider: str  # "ollama", "openai", "anthropic"
    model_name: str
    temperature: float = 0.0
    context_window: int = 8192

class ModelRouter(BaseModel):
    """
    Traffic controller for model assignment.
    Optimized for high-throughput Tier 5 evolution.
    """
    profile: str = Field(default="rtx_5090_local")

    def get_model(self, capability: str) -> ModelConfig:
        """
        Routes a capability request to the optimal model.
        """
        configs = self._get_profile_configs()
        return configs.get(capability, configs["DEFAULT"])

    def _get_profile_configs(self) -> dict[str, ModelConfig]:
        if self.profile == "rtx_5090_local":
            # The Universal Master (Unified Model for Zero Latency)
            # Since 5090 is fast enough, we keep the 32B model loaded at all times.
            master = ModelConfig(
                provider="ollama",
                model_name="qwen2.5-coder:32b",
                context_window=32768
            )

            return {
                "DEFAULT": master,
                "PLANNING": master,
                "CODING": master,
                "REFACTORING": master,
                "VERIFICATION": master,
                "FAST_TEST": master,
                "SUMMARIZATION": master,
                "LINT_FIX": master
            }

        # Default Fallback
        fallback = ModelConfig(provider="ollama", model_name="qwen2.5-coder:7b")
        return {"DEFAULT": fallback}

# Singleton instance
default_router = ModelRouter(profile=os.getenv("YBIS_MODEL_PROFILE", "rtx_5090_local"))

# Singleton instance for easy import
default_router = ModelRouter(profile=os.getenv("YBIS_MODEL_PROFILE", "rtx_5090_local"))
