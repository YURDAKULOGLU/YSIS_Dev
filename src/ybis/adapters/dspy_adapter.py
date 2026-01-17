"""
DSPy Adapter - Prompt optimization for LLM planner.

Uses DSPy to optimize planner prompts based on past performance.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)

# Try to import DSPy
try:
    import dspy
    from dspy import ChainOfThought, BootstrapFewShot, Signature, InputField, OutputField

    DSPY_AVAILABLE = True
except ImportError:
    DSPY_AVAILABLE = False
    logger.warning("DSPy not installed. Prompt optimization disabled.")


class DSPyPlannerOptimizer:
    """
    DSPy-based prompt optimizer for LLM planner.

    Optimizes planner prompts using DSPy's BootstrapFewShot optimizer.
    Learns from past successful plans to improve future planning.
    """

    def __init__(self):
        """Initialize DSPy optimizer."""
        if not DSPY_AVAILABLE:
            raise ImportError(
                "DSPy not available. Install with: pip install dspy-ai"
            )

        # Configure DSPy (uses LiteLLM by default)
        dspy.configure(lm=dspy.LM(model="ollama/llama3.2:3b"))

        # Define planning signature
        self.signature = Signature(
            "task_objective, task_title -> plan_json",
            task_objective=InputField(desc="Task objective"),
            task_title=InputField(desc="Task title"),
            plan_json=OutputField(desc="JSON plan with files, instructions, steps"),
        )

        # Create ChainOfThought module
        self.module = ChainOfThought(self.signature)

        # Initialize optimizer (will learn from examples)
        self.optimizer = BootstrapFewShot(max_bootstrapped_demos=5)

        # Track if optimizer has been trained
        self._trained = False

    def optimize(self, examples: list[dict[str, Any]] | None = None) -> None:
        """
        Optimize planner prompts using DSPy.

        Args:
            examples: List of example dicts with keys: task_objective, task_title, plan_json
        """
        logger.info(f"DSPy optimization: examples={len(examples) if examples else 0}")
        if not DSPY_AVAILABLE:
            return

        if not examples:
            # No examples provided, skip optimization
            logger.info("No examples provided, skipping DSPy optimization")
            return

        try:
            # Convert examples to DSPy format
            dspy_examples = []
            for ex in examples:
                dspy_examples.append(
                    dspy.Example(
                        task_objective=ex.get("task_objective", ""),
                        task_title=ex.get("task_title", ""),
                        plan_json=ex.get("plan_json", "{}"),
                    ).with_inputs("task_objective", "task_title")
                )

            # Optimize module with examples
            self.optimizer.compile(self.module, trainset=dspy_examples)
            self._trained = True

            logger.info(f"DSPy optimizer trained on {len(dspy_examples)} examples")
        except Exception as e:
            logger.warning(f"DSPy optimization failed: {e}")

    def generate_plan(self, task_objective: str, task_title: str) -> str:
        """
        Generate optimized plan using DSPy.

        Args:
            task_objective: Task objective
            task_title: Task title

        Returns:
            JSON plan string
        """
        if not DSPY_AVAILABLE:
            raise ImportError("DSPy not available")

        try:
            # Use optimized module to generate plan
            result = self.module(
                task_objective=task_objective,
                task_title=task_title,
            )

            return result.plan_json
        except Exception as e:
            logger.error(f"DSPy plan generation failed: {e}")
            raise

    def is_available(self) -> bool:
        """Check if DSPy is available and trained."""
        return DSPY_AVAILABLE and self._trained


# Global instance
_dspy_optimizer: DSPyPlannerOptimizer | None = None


def get_dspy_optimizer() -> DSPyPlannerOptimizer | None:
    """
    Get global DSPy optimizer instance.

    Returns:
        DSPyPlannerOptimizer if available, else None
    """
    global _dspy_optimizer

    if not DSPY_AVAILABLE:
        return None

    if _dspy_optimizer is None:
        try:
            _dspy_optimizer = DSPyPlannerOptimizer()
        except Exception as e:
            logger.warning(f"Failed to initialize DSPy optimizer: {e}")
            return None

    return _dspy_optimizer

