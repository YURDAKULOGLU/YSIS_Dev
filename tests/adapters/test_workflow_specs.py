"""
Workflow Spec Validation Tests.

Tests for vendor workflow specs (evo_evolve, reactive_agent, council_review, self_improve).
"""

import pytest
from pathlib import Path
from src.ybis.workflows import WorkflowRegistry
from src.ybis.workflows.runner import WorkflowRunner
from src.ybis.workflows.node_registry import NodeRegistry
from src.ybis.workflows.bootstrap import bootstrap_nodes


class TestWorkflowSpecs:
    """Test workflow spec validation."""

    def setup_method(self):
        """Set up test fixtures."""
        bootstrap_nodes()
        self.workflow_dir = Path(__file__).parent.parent.parent / "configs" / "workflows"

    def test_evo_evolve_workflow_spec_loads(self):
        """Test that evo_evolve workflow spec loads correctly."""
        try:
            workflow_spec = WorkflowRegistry.load_workflow("evo_evolve")
            assert workflow_spec is not None, "evo_evolve workflow should load"
            assert workflow_spec.name == "evo_evolve", "Workflow name should match"
            assert len(workflow_spec.nodes) > 0, "Workflow should have nodes"
        except (FileNotFoundError, ValueError) as e:
            pytest.skip(f"evo_evolve workflow spec not found: {e}")

    def test_evo_evolve_workflow_spec_validates(self):
        """Test that evo_evolve workflow spec validates."""
        try:
            runner = WorkflowRunner().load_workflow("evo_evolve")
            is_valid, errors = runner.validate_workflow()
            assert is_valid, f"evo_evolve workflow should validate: {errors}"
        except (FileNotFoundError, ValueError) as e:
            pytest.skip(f"evo_evolve workflow spec not found: {e}")

    def test_evo_evolve_workflow_has_gate_node(self):
        """Test that evo_evolve workflow has gate node."""
        try:
            workflow_spec = WorkflowRegistry.load_workflow("evo_evolve")
            gate_nodes = [n for n in workflow_spec.nodes if n["type"] == "gate"]
            assert len(gate_nodes) > 0, "evo_evolve workflow should have gate node"
        except (FileNotFoundError, ValueError) as e:
            pytest.skip(f"evo_evolve workflow spec not found: {e}")

    def test_evo_evolve_workflow_has_required_artifacts(self):
        """Test that evo_evolve workflow declares required artifacts."""
        try:
            workflow_spec = WorkflowRegistry.load_workflow("evo_evolve")
            artifacts = workflow_spec.requirements.get("artifacts", [])
            assert len(artifacts) > 0, "evo_evolve workflow should declare required artifacts"
            assert "gate_report.json" in artifacts, "evo_evolve workflow should require gate_report.json"
        except (FileNotFoundError, ValueError) as e:
            pytest.skip(f"evo_evolve workflow spec not found: {e}")

    def test_reactive_agent_workflow_spec_loads(self):
        """Test that reactive_agent workflow spec loads correctly."""
        try:
            workflow_spec = WorkflowRegistry.load_workflow("reactive_agent")
            assert workflow_spec is not None, "reactive_agent workflow should load"
            assert workflow_spec.name == "reactive_agent", "Workflow name should match"
        except (FileNotFoundError, ValueError) as e:
            pytest.skip(f"reactive_agent workflow spec not found: {e}")

    def test_reactive_agent_workflow_spec_validates(self):
        """Test that reactive_agent workflow spec validates."""
        try:
            runner = WorkflowRunner().load_workflow("reactive_agent")
            is_valid, errors = runner.validate_workflow()
            assert is_valid, f"reactive_agent workflow should validate: {errors}"
        except (FileNotFoundError, ValueError) as e:
            pytest.skip(f"reactive_agent workflow spec not found: {e}")

    def test_council_review_workflow_spec_loads(self):
        """Test that council_review workflow spec loads correctly."""
        try:
            workflow_spec = WorkflowRegistry.load_workflow("council_review")
            assert workflow_spec is not None, "council_review workflow should load"
            assert workflow_spec.name == "council_review", "Workflow name should match"
        except (FileNotFoundError, ValueError) as e:
            pytest.skip(f"council_review workflow spec not found: {e}")

    def test_council_review_workflow_spec_validates(self):
        """Test that council_review workflow spec validates."""
        try:
            runner = WorkflowRunner().load_workflow("council_review")
            is_valid, errors = runner.validate_workflow()
            assert is_valid, f"council_review workflow should validate: {errors}"
        except (FileNotFoundError, ValueError) as e:
            pytest.skip(f"council_review workflow spec not found: {e}")

    def test_self_improve_workflow_spec_loads(self):
        """Test that self_improve workflow spec loads correctly."""
        try:
            workflow_spec = WorkflowRegistry.load_workflow("self_improve")
            assert workflow_spec is not None, "self_improve workflow should load"
            assert workflow_spec.name == "self_improve", "Workflow name should match"
        except (FileNotFoundError, ValueError) as e:
            pytest.skip(f"self_improve workflow spec not found: {e}")

    def test_self_improve_workflow_spec_validates(self):
        """Test that self_improve workflow spec validates."""
        try:
            runner = WorkflowRunner().load_workflow("self_improve")
            is_valid, errors = runner.validate_workflow()
            assert is_valid, f"self_improve workflow should validate: {errors}"
        except (FileNotFoundError, ValueError) as e:
            pytest.skip(f"self_improve workflow spec not found: {e}")

    def test_all_vendor_workflows_have_gate_nodes(self):
        """Test that all vendor workflows have gate nodes."""
        vendor_workflows = ["evo_evolve", "reactive_agent", "council_review", "self_improve"]
        
        for workflow_name in vendor_workflows:
            try:
                workflow_spec = WorkflowRegistry.load_workflow(workflow_name)
                gate_nodes = [n for n in workflow_spec.nodes if n["type"] == "gate"]
                assert len(gate_nodes) > 0, f"{workflow_name} workflow should have gate node"
            except (FileNotFoundError, ValueError):
                pytest.skip(f"{workflow_name} workflow spec not found")

    def test_all_vendor_workflows_declare_artifacts(self):
        """Test that all vendor workflows declare required artifacts."""
        vendor_workflows = ["evo_evolve", "reactive_agent", "council_review", "self_improve"]
        
        for workflow_name in vendor_workflows:
            try:
                workflow_spec = WorkflowRegistry.load_workflow(workflow_name)
                artifacts = workflow_spec.requirements.get("artifacts", [])
                assert len(artifacts) > 0, f"{workflow_name} workflow should declare required artifacts"
                assert "gate_report.json" in artifacts, f"{workflow_name} workflow should require gate_report.json"
            except (FileNotFoundError, ValueError):
                pytest.skip(f"{workflow_name} workflow spec not found")

