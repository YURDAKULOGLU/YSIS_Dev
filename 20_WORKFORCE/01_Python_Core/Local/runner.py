from langchain_ollama import ChatOllama
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
import os

class HybridModelRouter:
    """Routes tasks to local or cloud models based on config"""
    
    def __init__(self):
        # Default Config
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.local_model_name = "qwen2.5-coder:14b" # Changed to available model 
        self.cloud_model_name = "claude-3-5-sonnet-20240620"
        
        self.local_model = None
        self.cloud_model = None
        
    def _get_local_model(self):
        if not self.local_model:
            self.local_model = ChatOllama(
                model=self.local_model_name,
                base_url=self.ollama_host,
                num_ctx=32768
            )
        return self.local_model

    def _get_cloud_model(self):
        if not self.cloud_model:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                print("[WARNING] Warning: ANTHROPIC_API_KEY not found. Fallback to local.")
                return self._get_local_model()
                
            self.cloud_model = ChatAnthropic(
                model=self.cloud_model_name,
                api_key=api_key,
                max_tokens=8192
            )
        return self.cloud_model
    
    def route(self, task_type: str):
        """Route to appropriate model based on task"""
        # Critical thinking -> Cloud
        if task_type in ["architecture", "spec_writing"]:
            return self._get_cloud_model()
        
        # Coding -> Local (Cost saving + Speed)
        return self._get_local_model()
    
    def invoke(self, task_type: str, system_prompt: str, user_message: str):
        """Invoke the appropriate model"""
        model = self.route(task_type)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message)
        ]
        
        try:
            response = model.invoke(messages)
            return response.content
        except Exception as e:
            return f"Error invoking model: {str(e)}"

# Singleton instance
runner = HybridModelRouter()
