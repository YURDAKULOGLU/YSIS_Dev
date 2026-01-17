"""
Debate Engine - Multi-persona debate system for resolving blocks.

Implements the logic for personas to discuss a topic and reach consensus.
"""

from typing import Any

from ..contracts.personas import COUNCIL_MEMBERS, Persona
from ..services.policy import get_policy_provider


class DebateResult:
    """Result of a debate session."""

    def __init__(
        self,
        topic: str,
        arguments: list[dict[str, Any]],
        consensus: str,
        summary: str,
    ):
        """
        Initialize debate result.

        Args:
            topic: Debate topic
            arguments: List of arguments from each persona
            consensus: Final consensus decision
            summary: Summary of the debate
        """
        self.topic = topic
        self.arguments = arguments
        self.consensus = consensus
        self.summary = summary

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "topic": self.topic,
            "arguments": self.arguments,
            "consensus": self.consensus,
            "summary": self.summary,
        }


class DebateEngine:
    """
    Debate Engine - Conducts multi-persona debates.

    Iterates through council members to generate arguments and reach consensus.
    """

    def __init__(self, model: str | None = None, api_base: str | None = None):
        """
        Initialize debate engine.

        Args:
            model: Model name (default from policy config)
            api_base: API base URL (default from policy config)
        """
        policy_provider = get_policy_provider()
        if policy_provider._policy is None:
            policy_provider.load_profile()
        llm_config = policy_provider.get_llm_config()

        self.model = model or llm_config.get("planner_model", "ollama/llama3.2:3b")
        self.api_base = api_base or llm_config.get("api_base", "http://localhost:11434")

    def conduct_debate(
        self, topic: str, context: str, rounds: int = 1
    ) -> DebateResult:
        """
        Conduct a debate among council members.

        Args:
            topic: Debate topic/question
            context: Context information (e.g., task details, gate report)
            rounds: Number of debate rounds (default: 1)

        Returns:
            DebateResult with arguments and consensus
        """
        arguments: list[dict[str, Any]] = []
        conversation_history = []

        # First round: Each member gives initial opinion
        for persona in COUNCIL_MEMBERS:
            argument = self._get_persona_argument(
                persona, topic, context, conversation_history
            )
            arguments.append({
                "persona": persona.name,
                "role": persona.role,
                "round": 1,
                "argument": argument,
            })
            conversation_history.append(f"{persona.name} ({persona.role}): {argument}")

        # Additional rounds: Members can respond to each other
        for round_num in range(2, rounds + 1):
            for persona in COUNCIL_MEMBERS:
                response = self._get_persona_response(
                    persona, topic, context, conversation_history
                )
                arguments.append({
                    "persona": persona.name,
                    "role": persona.role,
                    "round": round_num,
                    "argument": response,
                })
                conversation_history.append(f"{persona.name} ({persona.role}): {response}")

        # Generate consensus
        consensus, summary = self._reach_consensus(topic, context, conversation_history)

        return DebateResult(
            topic=topic,
            arguments=arguments,
            consensus=consensus,
            summary=summary,
        )

    def _get_persona_argument(
        self, persona: Persona, topic: str, context: str, history: list[str]
    ) -> str:
        """
        Get initial argument from a persona.

        Args:
            persona: Persona to generate argument
            topic: Debate topic
            context: Context information
            history: Conversation history

        Returns:
            Persona's argument
        """
        try:
            import litellm

            from ..services.resilience import ollama_retry

            prompt = f"""You are {persona.name}, a {persona.role}.

{persona.system_prompt}

Topic: {topic}

Context:
{context}

Provide your expert opinion on this topic. Be concise but thorough. Consider your role and expertise."""

            @ollama_retry
            def _call_llm():
                return litellm.completion(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": persona.system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    api_base=self.api_base,
                )

            response = _call_llm()

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"[Error generating argument: {e!s}]"

    def _get_persona_response(
        self, persona: Persona, topic: str, context: str, history: list[str]
    ) -> str:
        """
        Get response from a persona based on conversation history.

        Args:
            persona: Persona to generate response
            topic: Debate topic
            context: Context information
            history: Conversation history

        Returns:
            Persona's response
        """
        try:
            import litellm

            from ..services.resilience import ollama_retry

            history_text = "\n".join(history[-5:])  # Last 5 messages

            prompt = f"""You are {persona.name}, a {persona.role}.

{persona.system_prompt}

Topic: {topic}

Context:
{context}

Previous discussion:
{history_text}

Provide your response to the discussion. You can agree, disagree, or add new points."""

            @ollama_retry
            def _call_llm():
                return litellm.completion(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": persona.system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                    api_base=self.api_base,
                )

            response = _call_llm()

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"[Error generating response: {e!s}]"

    def _reach_consensus(
        self, topic: str, context: str, history: list[str]
    ) -> tuple[str, str]:
        """
        Reach consensus based on debate.

        Args:
            topic: Debate topic
            context: Context information
            history: Full conversation history

        Returns:
            Tuple of (consensus_decision, summary)
        """
        try:
            import litellm

            from ..services.resilience import ollama_retry

            history_text = "\n".join(history)

            prompt = f"""You are a neutral moderator analyzing a debate among expert council members.

Topic: {topic}

Context:
{context}

Debate History:
{history_text}

Based on the arguments presented, determine the consensus:
- "OVERRIDE_BLOCK": Unanimous or strong majority support for proceeding despite initial block (very rare, requires strong justification)
- "CONFIRM_BLOCK": Consensus confirms the block should remain (default if Security Officer objects)
- "REQUIRE_APPROVAL": Mixed opinions, requires human approval

Provide your decision and a brief summary (2-3 sentences) explaining the consensus."""

            @ollama_retry
            def _call_llm():
                return litellm.completion(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a neutral moderator. Analyze debates and reach consensus decisions.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    api_base=self.api_base,
                )

            response = _call_llm()

            result_text = response.choices[0].message.content.strip()

            # Parse consensus decision
            consensus = "CONFIRM_BLOCK"  # Default
            if "OVERRIDE_BLOCK" in result_text.upper():
                consensus = "OVERRIDE_BLOCK"
            elif "REQUIRE_APPROVAL" in result_text.upper():
                consensus = "REQUIRE_APPROVAL"

            summary = result_text

            return consensus, summary

        except Exception as e:
            return "CONFIRM_BLOCK", f"[Error reaching consensus: {e!s}]"

