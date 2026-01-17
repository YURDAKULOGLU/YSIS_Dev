"""
Vendor Adapter Conformance Tests.

Tests for vendor adapters (EvoAgentX, reactive-agents, llm-council, aiwaves-agents, Self-Improve-Swarms).
"""

import pytest
from src.ybis.adapters.registry import get_registry
from src.ybis.services.adapter_bootstrap import bootstrap_adapters


class TestVendorAdapters:
    """Test vendor adapter conformance."""

    def setup_method(self):
        """Set up test fixtures."""
        bootstrap_adapters()
        self.registry = get_registry()

    def test_evoagentx_adapter_registered(self):
        """Test that EvoAgentX adapter is registered."""
        adapter = self.registry.get("evoagentx", adapter_type="workflow_evolution")
        
        # Adapter may not be available (vendor not installed)
        if adapter is None:
            pytest.skip("EvoAgentX adapter not available (vendor not installed)")
        
        assert adapter is not None, "EvoAgentX adapter should be registered"
        assert hasattr(adapter, "is_available"), "EvoAgentX adapter must implement is_available()"
        assert hasattr(adapter, "evolve"), "EvoAgentX adapter must implement evolve()"
        assert hasattr(adapter, "score"), "EvoAgentX adapter must implement score()"

    def test_evoagentx_adapter_methods(self):
        """Test that EvoAgentX adapter methods work."""
        adapter = self.registry.get("evoagentx", adapter_type="workflow_evolution")
        
        if adapter is None:
            pytest.skip("EvoAgentX adapter not available")
        
        # Test evolve() - should not raise
        workflow_spec = {"name": "test", "nodes": []}
        metrics = {"lint_passed": True, "tests_passed": True}
        result = adapter.evolve(workflow_spec, metrics)
        assert isinstance(result, dict), "evolve() should return dict"
        assert "name" in result or "_evolution_metadata" in result, "evolve() should return workflow spec"
        
        # Test score() - should not raise
        artifacts = {
            "verifier_report": {"lint_passed": True, "tests_passed": True},
            "gate_report": {"decision": {"value": "PASS"}},
        }
        score = adapter.score(workflow_spec, artifacts)
        assert isinstance(score, float), "score() should return float"
        assert 0.0 <= score <= 1.0, "score() should return value between 0.0 and 1.0"

    def test_reactive_agents_adapter_registered(self):
        """Test that reactive-agents adapter is registered."""
        adapter = self.registry.get("reactive_agents", adapter_type="agent_runtime")
        
        if adapter is None:
            pytest.skip("Reactive-agents adapter not available")
        
        assert adapter is not None, "Reactive-agents adapter should be registered"
        assert hasattr(adapter, "is_available"), "Reactive-agents adapter must implement is_available()"
        assert hasattr(adapter, "run"), "Reactive-agents adapter must implement run()"
        assert hasattr(adapter, "supports_tools"), "Reactive-agents adapter must implement supports_tools()"

    def test_reactive_agents_adapter_methods(self):
        """Test that reactive-agents adapter methods work."""
        adapter = self.registry.get("reactive_agents", adapter_type="agent_runtime")
        
        if adapter is None:
            pytest.skip("Reactive-agents adapter not available")
        
        # Test run() - should not raise
        task = "Test task"
        tools = ["tool1", "tool2"]
        context = {"key": "value"}
        result = adapter.run(task, tools, context)
        assert isinstance(result, dict), "run() should return dict"
        assert "status" in result, "run() should return result with status"
        
        # Test supports_tools() - should not raise
        supports = adapter.supports_tools()
        assert isinstance(supports, bool), "supports_tools() should return bool"

    def test_llm_council_adapter_registered(self):
        """Test that llm-council adapter is registered."""
        adapter = self.registry.get("llm_council", adapter_type="council_review")
        
        if adapter is None:
            pytest.skip("LLM-council adapter not available")
        
        assert adapter is not None, "LLM-council adapter should be registered"
        assert hasattr(adapter, "is_available"), "LLM-council adapter must implement is_available()"
        assert hasattr(adapter, "review"), "LLM-council adapter must implement review()"

    def test_llm_council_adapter_methods(self):
        """Test that llm-council adapter methods work."""
        adapter = self.registry.get("llm_council", adapter_type="council_review")
        
        if adapter is None:
            pytest.skip("LLM-council adapter not available")
        
        # Test review() - should not raise
        prompt = "Review these candidates"
        candidates = ["candidate1", "candidate2"]
        result = adapter.review(prompt, candidates)
        assert isinstance(result, dict), "review() should return dict"
        assert "ranking" in result or "consensus" in result, "review() should return review result"

    def test_aiwaves_agents_adapter_registered(self):
        """Test that aiwaves-agents adapter is registered."""
        adapter = self.registry.get("aiwaves_agents", adapter_type="agent_learning")
        
        if adapter is None:
            pytest.skip("AIWaves-agents adapter not available")
        
        assert adapter is not None, "AIWaves-agents adapter should be registered"
        assert hasattr(adapter, "is_available"), "AIWaves-agents adapter must implement is_available()"
        assert hasattr(adapter, "learn"), "AIWaves-agents adapter must implement learn()"
        assert hasattr(adapter, "update_pipeline"), "AIWaves-agents adapter must implement update_pipeline()"

    def test_aiwaves_agents_adapter_methods(self):
        """Test that aiwaves-agents adapter methods work."""
        adapter = self.registry.get("aiwaves_agents", adapter_type="agent_learning")
        
        if adapter is None:
            pytest.skip("AIWaves-agents adapter not available")
        
        # Test learn() - should not raise
        trajectory = {"states": [], "actions": [], "rewards": []}
        result = adapter.learn(trajectory)
        assert isinstance(result, dict), "learn() should return dict"
        assert "insights" in result or "patterns" in result, "learn() should return learning result"
        
        # Test update_pipeline() - should not raise
        pipeline = {"config": "test"}
        gradients = {"grad1": 0.1}
        result = adapter.update_pipeline(pipeline, gradients)
        assert isinstance(result, dict), "update_pipeline() should return dict"
        assert "config" in result or "_update_metadata" in result, "update_pipeline() should return pipeline"

    def test_self_improve_swarms_adapter_registered(self):
        """Test that Self-Improve-Swarms adapter is registered."""
        adapter = self.registry.get("self_improve_swarms", adapter_type="self_improve_loop")
        
        if adapter is None:
            pytest.skip("Self-Improve-Swarms adapter not available")
        
        assert adapter is not None, "Self-Improve-Swarms adapter should be registered"
        assert hasattr(adapter, "is_available"), "Self-Improve-Swarms adapter must implement is_available()"
        assert hasattr(adapter, "reflect"), "Self-Improve-Swarms adapter must implement reflect()"
        assert hasattr(adapter, "plan"), "Self-Improve-Swarms adapter must implement plan()"
        assert hasattr(adapter, "implement"), "Self-Improve-Swarms adapter must implement implement()"
        assert hasattr(adapter, "test"), "Self-Improve-Swarms adapter must implement test()"
        assert hasattr(adapter, "integrate"), "Self-Improve-Swarms adapter must implement integrate()"

    def test_self_improve_swarms_adapter_methods(self):
        """Test that Self-Improve-Swarms adapter methods work."""
        adapter = self.registry.get("self_improve_swarms", adapter_type="self_improve_loop")
        
        if adapter is None:
            pytest.skip("Self-Improve-Swarms adapter not available")
        
        # Test reflect() - should not raise
        state = {"status": "running"}
        result = adapter.reflect(state)
        assert isinstance(result, dict), "reflect() should return dict"
        assert "insights" in result or "issues" in result, "reflect() should return reflection result"
        
        # Test plan() - should not raise
        reflection = {"insights": []}
        result = adapter.plan(reflection)
        assert isinstance(result, dict), "plan() should return dict"
        assert "tasks" in result or "priorities" in result, "plan() should return plan"
        
        # Test implement() - should not raise
        plan = {"tasks": []}
        result = adapter.implement(plan)
        assert isinstance(result, dict), "implement() should return dict"
        assert "status" in result or "changes" in result, "implement() should return implementation result"
        
        # Test test() - should not raise
        implementation = {"status": "pending"}
        result = adapter.test(implementation)
        assert isinstance(result, dict), "test() should return dict"
        assert "passed" in result or "coverage" in result, "test() should return test result"
        
        # Test integrate() - should not raise
        test_result = {"passed": True}
        result = adapter.integrate(test_result)
        assert isinstance(result, dict), "integrate() should return dict"
        assert "status" in result or "merged_changes" in result, "integrate() should return integration result"

    def test_all_vendor_adapters_graceful_fallback(self):
        """Test that all vendor adapters handle graceful fallback when vendors are not available."""
        vendor_adapters = [
            ("evoagentx", "workflow_evolution"),
            ("reactive_agents", "agent_runtime"),
            ("llm_council", "council_review"),
            ("aiwaves_agents", "agent_learning"),
            ("self_improve_swarms", "self_improve_loop"),
        ]
        
        for adapter_name, adapter_type in vendor_adapters:
            adapter = self.registry.get(adapter_name, adapter_type=adapter_type)
            
            # Even if adapter is None (vendor not installed), it should not raise
            # The adapter should be registered in the catalog
            adapter_info = self.registry.list_adapters(adapter_type=adapter_type)
            adapter_names = [a["name"] for a in adapter_info]
            assert adapter_name in adapter_names, f"{adapter_name} should be registered in catalog"

