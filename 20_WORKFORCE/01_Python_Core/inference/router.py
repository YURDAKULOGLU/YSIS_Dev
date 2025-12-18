from enum import Enum
from typing import Optional, List, Tuple
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# --- Configuration ---
class YBISConfig(BaseModel):
    # LangSmith
    langsmith_api_key: str = os.getenv("LANGSMITH_API_KEY", "")
    langsmith_project: str = "ybis-agentic"
    langsmith_tracing: bool = True
    
    # Anthropic (Cloud)
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    cloud_model: str = "claude-3-5-sonnet-20240620"
    
    # Ollama (Local)
    ollama_host: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    local_primary_model: str = "llama3.2:latest" # Changed to tool-compatible model
    local_fast_model: str = "llama3.2:3b"
    local_fallback_model: str = "qwen2.5-coder:14b" # Updated to match available model
    
    # Routing
    prefer_local: bool = True
    cloud_tasks: List[str] = ["architecture", "critical_decision", "complex_debug"]
    
    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "../../../.env")
        extra = "allow"

config = YBISConfig()

if config.langsmith_tracing and config.langsmith_api_key:
    os.environ["LANGSMITH_TRACING"] = "true"
    os.environ["LANGSMITH_API_KEY"] = config.langsmith_api_key
    os.environ["LANGSMITH_PROJECT"] = config.langsmith_project

# --- Enums ---
class TaskType(str, Enum):
    ARCHITECTURE = "architecture"
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    QUICK_FIX = "quick_fix"
    DOCUMENTATION = "documentation"
    TESTING = "testing"
    CRITICAL_DECISION = "critical_decision"

class TaskComplexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class RoutingDecision(BaseModel):
    model: str
    runtime: str  # "local" or "cloud"
    reason: str

import requests # Import requests for checking Ollama models

class IntelligentRouter:
    def __init__(self, config: YBISConfig):
        self.config = config
    
    def _get_ollama_models(self) -> List[str]:
        """Fetches a list of available models from the Ollama server."""
        try:
            response = requests.get(f"{self.config.ollama_host.replace('/v1', '')}/api/tags")
            response.raise_for_status()
            return [m['name'] for m in response.json()['models']]
        except requests.exceptions.RequestException as e:
            print(f"WARNING: Could not connect to Ollama server or fetch models: {e}")
            return []

    def route(
        self, 
        task_type: TaskType,
        complexity: TaskComplexity = TaskComplexity.MEDIUM,
        force_cloud: bool = False,
        force_local: bool = False
    ) -> Tuple[str, RoutingDecision]:
        """
        Returns (model_name_string, decision).
        Format: 'ollama:model_name' or 'anthropic:model_name'
        """
        
        # 1. Cloud forced or Critical
        use_cloud = force_cloud or (
            not force_local and 
            (complexity == TaskComplexity.CRITICAL or task_type in [TaskType.ARCHITECTURE, TaskType.CRITICAL_DECISION]) and
            self.config.anthropic_api_key
        )

        if use_cloud and self.config.anthropic_api_key:
            model_name = f"anthropic:{self.config.cloud_model}"
            return model_name, RoutingDecision(model=self.config.cloud_model, runtime="cloud", reason="Cloud routing")

        # 2. Local fallback or preference
        available_ollama_models = self._get_ollama_models()

        # Try local primary model
        if self.config.prefer_local and self.config.local_primary_model in available_ollama_models:
            model_name = f"ollama:{self.config.local_primary_model}"
            return model_name, RoutingDecision(model=self.config.local_primary_model, runtime="local", reason="Primary local model")
        
        # Try local fast model
        if self.config.prefer_local and self.config.local_fast_model in available_ollama_models and task_type in [TaskType.QUICK_FIX, TaskType.CODE_REVIEW, TaskType.TESTING]:
            model_name = f"ollama:{self.config.local_fast_model}"
            return model_name, RoutingDecision(model=self.config.local_fast_model, runtime="local", reason="Fast local model")

        # Fallback to local fallback model
        if self.config.prefer_local and self.config.local_fallback_model in available_ollama_models:
            model_name = f"ollama:{self.config.local_fallback_model}"
            return model_name, RoutingDecision(model=self.config.local_fallback_model, runtime="local", reason="Fallback local model (primary not found)")

        # If all local options fail, try to fall back to cloud if API key is present
        if self.config.anthropic_api_key:
            model_name = f"anthropic:{self.config.cloud_model}"
            return model_name, RoutingDecision(model=self.config.cloud_model, runtime="cloud", reason="Local models unavailable, falling back to cloud")
            
        raise Exception("No available LLM model to route to (local models not found and no cloud API key).")