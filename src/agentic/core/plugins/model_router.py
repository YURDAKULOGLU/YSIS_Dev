"""
ModelRouter - The Brain's Traffic Control

Responsibility:
- Decides which model handles a task based on capability, risk, and hardware.
- Abstracts the provider (Local vs Cloud).
- Currently optimized for RTX 5090 (High-End Local).
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ModelConfig:
    provider: str  # "ollama", "openai", "anthropic"
    model_name: str
    temperature: float = 0.0
    context_window: int = 8192

class ModelRouter:
    """
    Routes intent to the best available model.
    """
    
    def __init__(self, profile: str = "rtx_5090_local"):
        self.profile = profile
        self.active_config = self._load_profile(profile)

    def get_model(self, capability: str) -> ModelConfig:
        """
        Get model configuration for a specific capability.
        
        Capabilities:
        - "PLANNING": Deep reasoning, structured output
        - "CODING": Code generation, refactoring
        - "VERIFICATION": Analysis, spotting errors
        - "FAST": Quick summaries, simple logic
        """
        return self.active_config.get(capability, self.active_config["DEFAULT"])

    def _load_profile(self, profile: str) -> Dict[str, ModelConfig]:
        """
        Hardcoded profiles for now. 
        In v0.5 this will load from YAML.
        """
        
        # --- PROFILE: RTX 5090 (LOCAL BEAST) ---
        if profile == "rtx_5090_local":
            # Qwen 2.5 Coder 32B is incredible for both coding and logic.
            # It fits easily in 24GB VRAM.
            workhorse = ModelConfig(
                provider="ollama", 
                model_name="qwen2.5-coder:32b", 
                context_window=16384  # 5090 can handle large context
            )
            
            fast_chat = ModelConfig(
                provider="ollama", 
                model_name="llama3.1:8b", 
                context_window=8192
            )
            
            return {
                "DEFAULT": workhorse,
                "PLANNING": workhorse,     # 32B is great for planning
                "CODING": workhorse,       # It's specifically trained for this
                "VERIFICATION": workhorse, # Needs high logic
                "FAST": fast_chat          # For simple tasks
            }
            
        # --- PROFILE: HYBRID (FUTURE USE) ---
        elif profile == "hybrid_cloud":
            return {
                "DEFAULT": ModelConfig(provider="openai", model_name="gpt-4o-mini"),
                "PLANNING": ModelConfig(provider="anthropic", model_name="claude-3-5-sonnet"),
                "CODING": ModelConfig(provider="anthropic", model_name="claude-3-5-sonnet"),
                "VERIFICATION": ModelConfig(provider="openai", model_name="gpt-4o"),
                "FAST": ModelConfig(provider="openai", model_name="gpt-4o-mini"),
            }
            
        # Fallback
        return {
            "DEFAULT": ModelConfig(provider="ollama", model_name="qwen2.5-coder:14b")
        }

# Singleton instance for easy import
default_router = ModelRouter(profile=os.getenv("YBIS_MODEL_PROFILE", "rtx_5090_local"))
