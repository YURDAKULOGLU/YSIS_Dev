"""
AutoGen Adapter - Multi-agent conversations.

Provides agent-based debate and collaboration through conversations.
Complements YBIS's existing debate system (council_reviewer_node).
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)

# Try to import AutoGen from vendors/ (local clone) first
try:
    import sys
    from pathlib import Path

    vendors_path = Path(__file__).parent.parent.parent.parent / "vendors" / "autogen"
    if vendors_path.exists():
        sys.path.insert(0, str(vendors_path))
        try:
            from autogen import ConversableAgent, GroupChat, GroupChatManager

            AUTOGEN_LOCAL_CLONE_AVAILABLE = True
            logger.info("Using AutoGen from vendors/ (local clone)")
        except ImportError:
            AUTOGEN_LOCAL_CLONE_AVAILABLE = False
    else:
        AUTOGEN_LOCAL_CLONE_AVAILABLE = False
except (ImportError, Exception) as e:
    AUTOGEN_LOCAL_CLONE_AVAILABLE = False
    logger.debug(f"AutoGen local clone not available: {e}")

# Try to import AutoGen from pip
if not AUTOGEN_LOCAL_CLONE_AVAILABLE:
    try:
        from autogen import ConversableAgent, GroupChat, GroupChatManager

        AUTOGEN_PIP_AVAILABLE = True
        logger.info("Using AutoGen from pip")
    except ImportError:
        AUTOGEN_PIP_AVAILABLE = False
        logger.warning("AutoGen not installed. Install with: pip install pyautogen or clone to vendors/autogen")

# Combined availability
AUTOGEN_AVAILABLE = AUTOGEN_LOCAL_CLONE_AVAILABLE or AUTOGEN_PIP_AVAILABLE


class AutoGenAdapter:
    """
    AutoGen Adapter - Multi-agent conversations.

    Provides agent-based debate and collaboration:
    - Multiple agents discussing and debating solutions
    - Group chat with manager coordination
    - Consensus building through conversation

    Use cases:
    - Code review debates (alternative to council_reviewer_node)
    - Solution exploration through discussion
    - Multi-perspective analysis
    """

    def __init__(self, llm_model: str | None = None, api_base: str | None = None):
        """
        Initialize AutoGen adapter.

        Args:
            llm_model: LLM model name (default from policy)
            api_base: API base URL (default from policy)
        """
        if not AUTOGEN_AVAILABLE:
            raise ImportError(
                "AutoGen not available. Install with: pip install pyautogen or clone to vendors/autogen"
            )

        from ..services.policy import get_policy_provider

        policy_provider = get_policy_provider()
        if policy_provider._policy is None:
            policy_provider.load_profile()
        llm_config = policy_provider.get_llm_config()

        self.llm_model = llm_model or llm_config.get("planner_model", "ollama/llama3.2:3b")
        self.api_base = api_base or llm_config.get("api_base", "http://localhost:11434")

        # Configure AutoGen LLM config
        try:
            # AutoGen expects OpenAI-compatible config
            # For Ollama, we need to configure it differently
            self.llm_config = {
                "model": self.llm_model,
                "api_base": self.api_base,
                "api_type": "open_ai",
            }
        except Exception as e:
            logger.warning(f"Failed to configure AutoGen LLM: {e}")
            self.llm_config = None

    def create_debate_group(
        self,
        agents: list[dict[str, Any]],
        topic: str,
    ) -> GroupChat:
        """
        Create a debate group with multiple agents.

        Args:
            agents: List of agent definitions (name, system_message, etc.)
            topic: Debate topic/question

        Returns:
            GroupChat instance
        """
        logger.info(f"Creating AutoGen debate group: {len(agents)} agents, topic={topic[:50]}")
        if not AUTOGEN_AVAILABLE:
            raise ImportError("AutoGen not available")

        # Create agents
        conversable_agents = []
        for agent_def in agents:
            agent = ConversableAgent(
                name=agent_def.get("name", "Agent"),
                system_message=agent_def.get("system_message", ""),
                llm_config=self.llm_config,
            )
            conversable_agents.append(agent)

        # Create group chat
        group_chat = GroupChat(
            agents=conversable_agents,
            messages=[],
            max_round=10,  # Maximum conversation rounds
        )

        logger.info("AutoGen debate group created successfully")
        return group_chat

    def run_debate(
        self,
        group_chat: GroupChat,
        initial_message: str,
    ) -> dict[str, Any]:
        """
        Run a debate/conversation in the group.

        Args:
            group_chat: GroupChat instance
            initial_message: Initial message to start debate

        Returns:
            Debate results
        """
        logger.info(f"Running AutoGen debate: {len(group_chat.agents)} agents, message={initial_message[:50]}")
        try:
            # Create group chat manager
            manager = GroupChatManager(
                groupchat=group_chat,
                llm_config=self.llm_config,
            )

            # Start conversation
            result = manager.initiate_chat(
                message=initial_message,
                max_turns=10,
            )

            debate_result = {
                "status": "completed",
                "messages": [str(msg) for msg in group_chat.messages],
                "consensus": result.summary if hasattr(result, "summary") else None,
            }
            logger.info(f"AutoGen debate completed: {len(debate_result['messages'])} messages")
            return debate_result
        except Exception as e:
            logger.error(f"AutoGen debate failed: {e}")
            return {
                "status": "failed",
                "error": str(e),
            }

    def is_available(self) -> bool:
        """Check if AutoGen adapter is available."""
        available = AUTOGEN_AVAILABLE and self.llm_config is not None
        logger.debug(f"AutoGen adapter available: {available}")
        return available


# Global instance
_autogen_adapter: AutoGenAdapter | None = None


def get_autogen_adapter(llm_model: str | None = None, api_base: str | None = None) -> AutoGenAdapter | None:
    """
    Get global AutoGen adapter instance.

    Args:
        llm_model: LLM model name (default from policy)
        api_base: API base URL (default from policy)

    Returns:
        AutoGenAdapter if available, else None
    """
    global _autogen_adapter

    if not AUTOGEN_AVAILABLE:
        return None

    if _autogen_adapter is None:
        try:
            _autogen_adapter = AutoGenAdapter(llm_model=llm_model, api_base=api_base)
        except Exception as e:
            logger.warning(f"Failed to initialize AutoGen adapter: {e}")
            return None

    return _autogen_adapter
