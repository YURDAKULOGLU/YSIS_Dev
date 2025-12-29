"""
YBIS Observability Module (Langfuse Integration)
Provides tracing capabilities for LLM calls and agent workflows.
Gracefully degrades if Langfuse is not configured.
"""

import os
import functools
from typing import Optional, Any
import logging

# Silent logging
logger = logging.getLogger(__name__)

LANGFUSE_AVAILABLE = False
try:
    from langfuse import Langfuse
    from langfuse.decorators import observe, langfuse_context
    LANGFUSE_AVAILABLE = True
except ImportError:
    pass

class YBISTracer:
    """Singleton Tracer for YBIS"""
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(YBISTracer, cls).__new__(cls)
            cls._instance._init_tracer()
        return cls._instance

    def _init_tracer(self):
        self.enabled = False
        self.client = None
        
        # Check config
        public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
        secret_key = os.getenv("LANGFUSE_SECRET_KEY")
        
        if LANGFUSE_AVAILABLE and public_key and secret_key:
            try:
                self.client = Langfuse()
                self.enabled = True
            except Exception:
                self.enabled = False
        else:
            self.enabled = False

    def trace_generation(self, name: str, model: str, input_data: Any, output_data: Any, metadata: Optional[dict] = None):
        """Manually log a generation trace"""
        if not self.enabled or not self.client:
            return

        try:
            self.client.generation(
                name=name,
                model=model,
                input=input_data,
                output=output_data,
                metadata=metadata
            )
        except Exception as e:
            logger.warning(f"Failed to log trace: {e}")

    def flush(self):
        """Flush pending traces"""
        if self.enabled and self.client:
            self.client.flush()

# Decorator for easy tracing
def trace_span(name: Optional[str] = None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not LANGFUSE_AVAILABLE:
                return func(*args, **kwargs)
            
            # If enabled, use the native decorator logic manually or via SDK
            # For simplicity, we delegate to native @observe if available
            try:
                return observe(name=name)(func)(*args, **kwargs)
            except Exception:
                return func(*args, **kwargs)
        return wrapper
    return decorator

# Global accessor
tracer = YBISTracer()
