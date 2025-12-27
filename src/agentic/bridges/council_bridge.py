"""
LLM Council Bridge for YBIS
Wraps the llm-council 3-stage deliberation system.
Enables multi-LLM consensus decision-making for critical tasks.
"""

import sys
from pathlib import Path
from typing import Dict, Any, Optional
import asyncio

# Add llm-council to path (parent dir, not backend)
COUNCIL_ROOT = Path(__file__).parent.parent.parent.parent / "tools" / "llm-council"
sys.path.insert(0, str(COUNCIL_ROOT))

class CouncilBridge:
    """
    Bridge to LLM Council 3-stage deliberation system.

    Stage 1: Collect responses from multiple LLMs
    Stage 2: Anonymous peer review (models rank each other's responses)
    Stage 3: Chairman synthesizes final consensus answer
    """

    def __init__(self, use_local: bool = True):
        """
        Initialize Council Bridge.

        Args:
            use_local: If True, use local Ollama models instead of OpenRouter
        """
        self.use_local = use_local

        try:
            # Import council functions from backend package
            from backend.council import (
                stage1_collect_responses,
                stage2_collect_rankings,
                stage3_synthesize_final,
                calculate_aggregate_rankings
            )

            self.stage1 = stage1_collect_responses
            self.stage2 = stage2_collect_rankings
            self.stage3 = stage3_synthesize_final
            self.calculate_rankings = calculate_aggregate_rankings

            print(f"[CouncilBridge] Initialized (local={'Ollama' if use_local else 'OpenRouter'})")

        except ImportError as e:
            print(f"[CouncilBridge] ERROR: Could not import council: {e}")
            print(f"[CouncilBridge] Council path: {COUNCIL_ROOT}")
            raise

    async def ask_council_async(
        self,
        question: str,
        return_stages: bool = False
    ) -> Dict[str, Any]:
        """
        Ask the council a question and get consensus answer.

        Args:
            question: The question to deliberate on
            return_stages: If True, return all 3 stages; if False, just final answer

        Returns:
            Dict with 'answer' and optionally 'stage1', 'stage2', 'stage3'
        """
        try:
            # Stage 1: Collect individual responses
            print(f"[CouncilBridge] Stage 1: Collecting responses...")
            stage1_results = await self.stage1(question)

            if not stage1_results:
                return {
                    "answer": "ERROR: No responses collected from council models",
                    "error": True
                }

            print(f"[CouncilBridge] Stage 1: Got {len(stage1_results)} responses")

            # Stage 2: Collect rankings (peer review)
            print(f"[CouncilBridge] Stage 2: Collecting peer rankings...")
            stage2_results, label_to_model = await self.stage2(question, stage1_results)

            print(f"[CouncilBridge] Stage 2: Got {len(stage2_results)} rankings")

            # Calculate aggregate rankings
            aggregate = self.calculate_rankings(stage2_results, label_to_model)

            # Stage 3: Chairman synthesis
            print(f"[CouncilBridge] Stage 3: Synthesizing final answer...")
            final_answer = await self.stage3(
                question,
                stage1_results,
                stage2_results,
                aggregate,
                label_to_model
            )

            print(f"[CouncilBridge] Complete!")

            result = {"answer": final_answer}

            if return_stages:
                result["stage1"] = stage1_results
                result["stage2"] = stage2_results
                result["aggregate_rankings"] = aggregate
                result["label_to_model"] = label_to_model

            return result

        except Exception as e:
            print(f"[CouncilBridge] ERROR in deliberation: {e}")
            import traceback
            traceback.print_exc()
            return {
                "answer": f"ERROR: Council deliberation failed: {str(e)}",
                "error": True
            }

    def ask_council(
        self,
        question: str,
        return_stages: bool = False
    ) -> Dict[str, Any]:
        """
        Synchronous wrapper for ask_council_async.
        Use this for simple blocking calls.
        """
        return asyncio.run(self.ask_council_async(question, return_stages))

    def quick_consensus(self, question: str) -> str:
        """
        Quick consensus - just return the final answer string.

        Args:
            question: The question

        Returns:
            Final consensus answer as string
        """
        result = self.ask_council(question, return_stages=False)
        return result.get("answer", "ERROR: No answer")


# Convenience function
def ask_council(question: str, use_local: bool = True) -> str:
    """
    Quick function to ask council a question.

    Example:
        answer = ask_council("Should we use Cognee or MemGPT?")
    """
    bridge = CouncilBridge(use_local=use_local)
    return bridge.quick_consensus(question)


if __name__ == "__main__":
    # Test
    print("="*60)
    print("Testing Council Bridge")
    print("="*60)

    bridge = CouncilBridge(use_local=False)  # Use OpenRouter for test

    test_question = "What are the key benefits of using Neo4j for dependency tracking?"

    print(f"\nQuestion: {test_question}\n")

    result = bridge.ask_council(test_question, return_stages=True)

    print(f"\nFinal Answer:\n{result['answer']}\n")

    if 'stage1' in result:
        print(f"Participated: {len(result['stage1'])} models")
        print(f"Rankings: {len(result['stage2'])} peer reviews")
