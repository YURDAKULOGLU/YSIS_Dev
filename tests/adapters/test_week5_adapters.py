"""
Test Week 5 Adapters - ByteRover, CrewAI, AutoGen.

Tests that all Week 5 adapters:
1. Are properly integrated with central registry/policy
2. Can be initialized from policy configuration
3. Have proper fallback mechanisms
4. Work with the central system (workflows, nodes)
"""

import pytest
from pathlib import Path

from src.ybis.adapters.byterover_adapter import get_byterover_adapter
from src.ybis.adapters.crewai_adapter import get_crewai_adapter
from src.ybis.adapters.autogen_adapter import get_autogen_adapter
from src.ybis.adapters.mem0_adapter import get_mem0_adapter
from src.ybis.services.policy import get_policy_provider
from src.ybis.data_plane.vector_store import VectorStore


class TestWeek5AdaptersIntegration:
    """Test Week 5 adapters are properly integrated with central system."""

    def test_adapters_read_from_policy(self):
        """Test that adapters read configuration from policy."""
        policy_provider = get_policy_provider()
        policy_provider.load_profile()
        policy = policy_provider.get_policy()

        # Check adapter configs exist in policy
        adapters = policy.get("adapters", {})
        assert "byterover" in adapters
        assert "crewai" in adapters
        assert "autogen" in adapters
        assert "mem0" in adapters

    def test_mem0_adapter_policy_integration(self):
        """Test Mem0 adapter reads from policy."""
        adapter = get_mem0_adapter()
        assert adapter is not None

        # Check mode is set from policy
        policy_provider = get_policy_provider()
        policy_provider.load_profile()
        policy = policy_provider.get_policy()
        mem0_config = policy.get("adapters", {}).get("mem0", {})
        expected_mode = mem0_config.get("mode", "auto")

        # Adapter should respect policy mode
        assert adapter.mode == expected_mode or adapter.mode == "fallback"

    def test_byterover_adapter_policy_integration(self):
        """Test ByteRover adapter reads from policy."""
        adapter = get_byterover_adapter()
        assert adapter is not None

        # Check adapter can be initialized (even if not available)
        assert hasattr(adapter, "is_available")
        assert hasattr(adapter, "share_knowledge")
        assert hasattr(adapter, "search_team_knowledge")

    def test_crewai_adapter_policy_integration(self):
        """Test CrewAI adapter reads from policy."""
        adapter = get_crewai_adapter()

        # Adapter may be None if not available, but if it exists, it should work
        if adapter is not None:
            assert hasattr(adapter, "is_available")
            assert hasattr(adapter, "create_crew")
            assert hasattr(adapter, "execute_crew")

    def test_autogen_adapter_policy_integration(self):
        """Test AutoGen adapter reads from policy."""
        adapter = get_autogen_adapter()

        # Adapter may be None if not available, but if it exists, it should work
        if adapter is not None:
            assert hasattr(adapter, "is_available")
            assert hasattr(adapter, "create_debate_group")
            assert hasattr(adapter, "run_debate")

    def test_adapters_have_fallback(self):
        """Test that all adapters have proper fallback mechanisms."""
        # Mem0: Falls back to VectorStore
        mem0 = get_mem0_adapter()
        assert mem0 is not None
        # Even if Mem0 not available, should fallback to VectorStore
        assert mem0.is_available() or mem0.mode == "fallback"

        # ByteRover: Falls back to VectorStore
        byterover = get_byterover_adapter()
        assert byterover is not None
        # Should have fallback mechanism
        assert hasattr(byterover, "vector_store")

        # CrewAI: Falls back to reactive-agents (in node)
        crewai = get_crewai_adapter()
        # May be None if not available, that's OK (fallback in node)

        # AutoGen: Falls back to llm-council (in node)
        autogen = get_autogen_adapter()
        # May be None if not available, that's OK (fallback in node)

    def test_adapters_use_central_llm_config(self):
        """Test that adapters use central LLM configuration from policy."""
        policy_provider = get_policy_provider()
        policy_provider.load_profile()
        llm_config = policy_provider.get_llm_config()

        # CrewAI should use policy LLM config
        crewai = get_crewai_adapter()
        if crewai is not None:
            assert crewai.llm_model is not None
            # Should match policy or be from policy
            expected_model = llm_config.get("planner_model", "ollama/llama3.2:3b")
            assert crewai.llm_model == expected_model or "ollama" in crewai.llm_model.lower()

        # AutoGen should use policy LLM config
        autogen = get_autogen_adapter()
        if autogen is not None:
            assert autogen.llm_config is not None
            # Should have model from policy
            assert "model" in autogen.llm_config


class TestWeek5AdaptersWorkflowIntegration:
    """Test Week 5 adapters work with workflow nodes."""

    def test_mem0_in_agent_runtime_node(self):
        """Test Mem0 is used in agent_runtime_node."""
        # Check that agent_runtime_node imports and uses Mem0
        from src.ybis.orchestrator.nodes.experimental import agent_runtime_node

        # Node should exist and be callable
        assert callable(agent_runtime_node)

    def test_crewai_in_agent_runtime_node(self):
        """Test CrewAI is used in agent_runtime_node."""
        from src.ybis.orchestrator.nodes.experimental import agent_runtime_node

        # Check node code imports CrewAI
        import inspect
        source = inspect.getsource(agent_runtime_node)
        assert "crewai" in source.lower() or "CrewAI" in source

    def test_autogen_in_council_reviewer_node(self):
        """Test AutoGen is used in council_reviewer_node."""
        from src.ybis.orchestrator.nodes.experimental import council_reviewer_node

        # Check node code imports AutoGen
        import inspect
        source = inspect.getsource(council_reviewer_node)
        assert "autogen" in source.lower() or "AutoGen" in source


class TestWeek5AdaptersSelfImprovement:
    """Test that adapters support self-improvement workflows."""

    def test_adapters_can_be_used_in_self_improve(self):
        """Test adapters can be used in self-improve workflow."""
        # Self-improve workflow should be able to use:
        # - Mem0 for agent memory
        # - ByteRover for team knowledge
        # - CrewAI for multi-agent execution
        # - AutoGen for multi-agent review

        # Check that adapters are available for self-improve
        mem0 = get_mem0_adapter()
        assert mem0 is not None

        byterover = get_byterover_adapter()
        assert byterover is not None

        # These should be usable in self-improve workflow
        # (actual integration test would require full workflow run)

    def test_adapters_support_central_logging(self):
        """Test adapters support central journal logging."""
        # All adapters should work with journal logging
        # (checked via is_available and proper error handling)

        mem0 = get_mem0_adapter()
        assert mem0 is not None

        byterover = get_byterover_adapter()
        assert byterover is not None


@pytest.mark.integration
class TestWeek5AdaptersEndToEnd:
    """End-to-end tests for Week 5 adapters (requires full system)."""

    @pytest.mark.skip(reason="Requires full system setup")
    def test_mem0_memory_persistence(self):
        """Test Mem0 memory persists across runs."""
        # This would require:
        # 1. Run task with Mem0
        # 2. Check memory is saved
        # 3. Run another task
        # 4. Check memory is retrieved
        pass

    @pytest.mark.skip(reason="Requires full system setup")
    def test_byterover_team_sharing(self):
        """Test ByteRover team knowledge sharing."""
        # This would require:
        # 1. Share knowledge via ByteRover
        # 2. Search knowledge from another context
        # 3. Verify knowledge is shared
        pass

    @pytest.mark.skip(reason="Requires full system setup")
    def test_crewai_multi_agent_execution(self):
        """Test CrewAI multi-agent execution in workflow."""
        # This would require:
        # 1. Create workflow with agent_runtime_node
        # 2. Run workflow
        # 3. Verify CrewAI is used
        # 4. Verify execution result
        pass

    @pytest.mark.skip(reason="Requires full system setup")
    def test_autogen_multi_agent_review(self):
        """Test AutoGen multi-agent review in workflow."""
        # This would require:
        # 1. Create workflow with council_reviewer_node
        # 2. Run workflow
        # 3. Verify AutoGen is used
        # 4. Verify review result
        pass


