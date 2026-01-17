"""
Comprehensive logging for workflow execution, nodes, and LLM calls.
"""

import time
from collections.abc import Callable
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any

from ..services.observability import get_observability_service
from ..syscalls.journal import append_event


def log_workflow_start(state: dict[str, Any]) -> None:
    """Log workflow start."""
    run_path = state.get("run_path")
    if not run_path:
        return
    
    trace_id = state.get("trace_id", f"{state.get('task_id')}-{state.get('run_id')}")
    workflow_name = state.get("workflow_name", "unknown")
    
    # Log to journal
    append_event(
        run_path,
        "WORKFLOW_START",
        {
            "workflow": workflow_name,
            "task_id": state.get("task_id"),
            "run_id": state.get("run_id"),
            "timestamp": datetime.now().isoformat(),
        },
        trace_id,
    )
    
    # Log to observability
    observability = get_observability_service()
    observability.trace_generation(
        name="workflow_start",
        model="ybis",
        input_data={"workflow": workflow_name, "task_id": state.get("task_id")},
        output_data=None,
        metadata={
            "run_id": state.get("run_id"),
            "trace_id": trace_id,
            "workflow": workflow_name,
        },
    )


def log_workflow_end(state: dict[str, Any], status: str, duration: float) -> None:
    """Log workflow end."""
    run_path = state.get("run_path")
    if not run_path:
        return
    
    trace_id = state.get("trace_id", f"{state.get('task_id')}-{state.get('run_id')}")
    workflow_name = state.get("workflow_name", "unknown")
    
    # Log to journal
    append_event(
        run_path,
        "WORKFLOW_END",
        {
            "workflow": workflow_name,
            "status": status,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
        },
        trace_id,
    )
    
    # Log to observability
    observability = get_observability_service()
    observability.trace_generation(
        name="workflow_end",
        model="ybis",
        input_data={"workflow": workflow_name, "status": status},
        output_data=None,
        metadata={
            "run_id": state.get("run_id"),
            "trace_id": trace_id,
            "duration": duration,
            "status": status,
        },
    )


def log_node_execution(node_name: str):
    """Decorator to log node execution."""
    def decorator(node_func: Callable) -> Callable:
        @wraps(node_func)
        def wrapper(state: dict[str, Any]) -> dict[str, Any]:
            run_path = state.get("run_path")
            trace_id = state.get("trace_id", f"{state.get('task_id')}-{state.get('run_id')}")
            start_time = time.time()
            
            # Log node enter (NODE_ENTER for spec compatibility)
            if run_path:
                state_keys = list(state.keys())[:10]  # Limit to first 10 keys
                append_event(
                    run_path,
                    "NODE_ENTER",
                    {
                        "node_name": node_name,
                        "state_keys": state_keys,
                    },
                    trace_id,
                )
                # Also log NODE_START for backward compatibility
                append_event(
                    run_path,
                    "NODE_START",
                    {
                        "node": node_name,
                        "task_id": state.get("task_id"),
                        "run_id": state.get("run_id"),
                        "timestamp": datetime.now().isoformat(),
                    },
                    trace_id,
                )
            
            try:
                # Execute node
                result = node_func(state)
                duration = time.time() - start_time
                
                # Log node exit (NODE_EXIT for spec compatibility)
                if run_path:
                    append_event(
                        run_path,
                        "NODE_EXIT",
                        {
                            "node_name": node_name,
                            "status": result.get("status", "unknown"),
                            "duration_ms": round(duration * 1000, 2),
                        },
                        trace_id,
                    )
                    # Also log NODE_SUCCESS for backward compatibility
                    append_event(
                        run_path,
                        "NODE_SUCCESS",
                        {
                            "node": node_name,
                            "duration": duration,
                            "status": result.get("status", "unknown"),
                            "timestamp": datetime.now().isoformat(),
                        },
                        trace_id,
                    )
                
                return result
            except Exception as e:
                duration = time.time() - start_time
                
                # Log node error (NODE_ERROR for spec compatibility)
                if run_path:
                    error_msg = str(e)
                    traceback_summary = ""
                    if hasattr(e, "__traceback__"):
                        import traceback
                        traceback_summary = "".join(traceback.format_tb(e.__traceback__))[:500]
                    
                    append_event(
                        run_path,
                        "NODE_ERROR",
                        {
                            "node_name": node_name,
                            "error": error_msg[:500],
                            "error_type": type(e).__name__,
                            "traceback_summary": traceback_summary,
                            "duration_ms": round(duration * 1000, 2),
                        },
                        trace_id,
                    )
                raise
        
        return wrapper
    return decorator


def log_llm_call(
    model: str,
    messages: list[dict[str, Any]],
    response: Any,
    metadata: dict[str, Any] | None = None,
    run_path: Path | None = None,
    trace_id: str | None = None,
) -> None:
    """
    Log LLM call to both journal and observability.
    
    Args:
        model: Model identifier
        messages: LLM messages
        response: LLM response
        metadata: Optional metadata (tokens, cost, duration, etc.)
        run_path: Optional run path for journal logging
        trace_id: Optional trace ID
    """
    # Extract response content
    response_content = ""
    if hasattr(response, "choices") and response.choices:
        response_content = response.choices[0].message.content or ""
    
    # Extract usage if available
    usage = {}
    if hasattr(response, "usage"):
        usage = {
            "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
            "completion_tokens": getattr(response.usage, "completion_tokens", 0),
            "total_tokens": getattr(response.usage, "total_tokens", 0),
        }
    
    # Log to journal
    if run_path:
        append_event(
            run_path,
            "LLM_CALL",
            {
                "model": model,
                "messages": messages,
                "response": response_content[:500],  # Truncate for journal
                "usage": usage,
                "metadata": metadata or {},
                "timestamp": datetime.now().isoformat(),
            },
            trace_id,
        )
    
    # Log to observability
    observability = get_observability_service()
    observability.trace_generation(
        name="llm_call",
        model=model,
        input_data={"messages": messages},
        output_data={"response": response_content},
        metadata={
            **(metadata or {}),
            "usage": usage,
            "trace_id": trace_id,
        },
    )


def log_state_transition(
    old_state: dict[str, Any],
    new_state: dict[str, Any],
) -> None:
    """Log state transition."""
    run_path = new_state.get("run_path")
    if not run_path:
        return
    
    trace_id = new_state.get("trace_id", f"{new_state.get('task_id')}-{new_state.get('run_id')}")
    
    # Find changes
    changes = {}
    for key in new_state:
        old_value = old_state.get(key)
        new_value = new_state.get(key)
        if old_value != new_value:
            # Don't log large objects
            if isinstance(new_value, (str, int, float, bool, type(None))):
                changes[key] = {"old": old_value, "new": new_value}
            else:
                changes[key] = {"changed": True}
    
    if changes:
        append_event(
            run_path,
            "STATE_TRANSITION",
            {
                "changes": changes,
                "timestamp": datetime.now().isoformat(),
            },
            trace_id,
        )


def llm_call_with_logging(
    model: str,
    messages: list[dict[str, Any]],
    run_path: Path | None = None,
    trace_id: str | None = None,
    **kwargs: Any,
) -> Any:
    """
    Wrapper for litellm.completion with logging.
    
    Args:
        model: Model identifier
        messages: LLM messages
        run_path: Optional run path for logging
        trace_id: Optional trace ID
        **kwargs: Additional arguments for litellm.completion
    
    Returns:
        LLM response
    """
    import litellm
    
    start_time = time.time()
    
    try:
        response = litellm.completion(model=model, messages=messages, **kwargs)
        duration = time.time() - start_time
        
        # Extract usage
        usage = {}
        if hasattr(response, "usage"):
            usage = {
                "prompt_tokens": getattr(response.usage, "prompt_tokens", 0),
                "completion_tokens": getattr(response.usage, "completion_tokens", 0),
                "total_tokens": getattr(response.usage, "total_tokens", 0),
            }
        
        # Calculate cost (rough estimate)
        cost = 0.0
        if usage.get("total_tokens"):
            # Rough cost estimate (adjust based on model)
            if "gpt-4" in model.lower():
                cost = (usage["prompt_tokens"] * 0.03 + usage["completion_tokens"] * 0.06) / 1000
            elif "gpt-3.5" in model.lower():
                cost = (usage["prompt_tokens"] * 0.0015 + usage["completion_tokens"] * 0.002) / 1000
            # For Ollama/local models, cost is 0
        
        # Log LLM call
        log_llm_call(
            model=model,
            messages=messages,
            response=response,
            metadata={
                "duration": duration,
                "cost": cost,
                **usage,
            },
            run_path=run_path,
            trace_id=trace_id,
        )
        
        return response
    except Exception as e:
        duration = time.time() - start_time
        
        # Log error
        if run_path:
            append_event(
                run_path,
                "LLM_ERROR",
                {
                    "model": model,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "duration": duration,
                    "timestamp": datetime.now().isoformat(),
                },
                trace_id,
            )
        
        # Log to observability
        observability = get_observability_service()
        observability.trace_generation(
            name="llm_error",
            model=model,
            input_data={"messages": messages},
            output_data=None,
            metadata={
                "error": str(e),
                "error_type": type(e).__name__,
                "duration": duration,
                "trace_id": trace_id,
            },
        )
        
        raise

