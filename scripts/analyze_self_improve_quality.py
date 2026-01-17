#!/usr/bin/env python3
"""
Analyze Self-Improve Workflow Quality.

Evaluates:
1. Reflection quality (real issues detected?)
2. Plan quality (valid files, specific steps, no hallucinations)
3. Implementation quality (actual changes made?)
4. Test results (lint + tests passed?)
5. RAG usage (codebase context used?)
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def analyze_reflection(reflection_path: Path) -> Dict[str, Any]:
    """Analyze reflection report quality."""
    if not reflection_path.exists():
        return {"score": 0, "issues": ["Reflection report not found"]}

    try:
        reflection = json.loads(reflection_path.read_text())
    except Exception as e:
        return {"score": 0, "issues": [f"Failed to parse reflection: {e}"]}

    score = 0
    issues = []
    strengths = []

    # Check system health
    health = reflection.get("system_health", {})
    if health:
        score += 1
        strengths.append("System health assessed")
    else:
        issues.append("No system health data")

    # Check recent metrics
    metrics = reflection.get("recent_metrics", {})
    if metrics and metrics.get("total_runs", 0) > 0:
        score += 1
        strengths.append(f"Analyzed {metrics.get('total_runs')} recent runs")
    else:
        issues.append("No recent metrics or empty history")

    # Check error patterns
    error_patterns = reflection.get("error_patterns", {})
    if error_patterns.get("total_errors", 0) > 0:
        score += 2
        strengths.append(f"Detected {error_patterns.get('total_errors')} errors")
        top_patterns = error_patterns.get("top_patterns", [])
        if top_patterns:
            score += 1
            strengths.append(f"Identified {len(top_patterns)} top error patterns")
    else:
        issues.append("No error patterns detected")

    # Check issues identified
    issues_list = reflection.get("issues_identified", [])
    if issues_list:
        score += 2
        strengths.append(f"Identified {len(issues_list)} issues")
        # Check if issues have severity
        has_severity = any(i.get("severity") for i in issues_list)
        if has_severity:
            score += 1
            strengths.append("Issues prioritized by severity")
    else:
        issues.append("No issues identified")

    # Check opportunities
    opportunities = reflection.get("opportunities_identified", [])
    if opportunities:
        score += 1
        strengths.append(f"Identified {len(opportunities)} opportunities")

    max_score = 8
    return {
        "score": min(score, max_score),
        "max_score": max_score,
        "percentage": (score / max_score) * 100,
        "issues": issues,
        "strengths": strengths,
    }


def analyze_plan(plan_path: Path) -> Dict[str, Any]:
    """Analyze improvement plan quality."""
    if not plan_path.exists():
        return {"score": 0, "issues": ["Plan not found"]}

    try:
        plan = json.loads(plan_path.read_text())
    except Exception as e:
        return {"score": 0, "issues": [f"Failed to parse plan: {e}"]}

    score = 0
    issues = []
    strengths = []

    # Check objective
    objective = plan.get("objective", "")
    if objective and len(objective) > 20:
        score += 1
        strengths.append("Objective is specific")
    else:
        issues.append("Objective is vague or missing")

    # Check files
    files = plan.get("files", [])
    invalid_files = ["all", "of", "the", "existing", "code"]
    valid_files = [f for f in files if f not in invalid_files and not f.endswith("__")]

    if len(valid_files) > 0:
        score += 2
        strengths.append(f"{len(valid_files)} valid files referenced")
        # Check if files exist
        existing_files = []
        for f in valid_files:
            full_path = project_root / f
            if full_path.exists():
                existing_files.append(f)
        if existing_files:
            score += 1
            strengths.append(f"{len(existing_files)} files actually exist")
        else:
            issues.append("Referenced files don't exist")
    else:
        if files:
            issues.append(f"All {len(files)} files are invalid")
        else:
            issues.append("No files referenced")

    # Check steps
    steps = plan.get("steps", [])
    if len(steps) > 0:
        score += 1
        strengths.append(f"{len(steps)} steps defined")
        # Check for duplicates
        step_descriptions = [s.get("description", "") for s in steps]
        unique_steps = len(set(step_descriptions))
        if unique_steps == len(steps):
            score += 1
            strengths.append("No duplicate steps")
        else:
            issues.append(f"{len(steps) - unique_steps} duplicate steps found")

        # Check step quality
        specific_steps = 0
        for step in steps:
            action = step.get("action", "")
            description = step.get("description", "")
            if len(action) > 30 and len(description) > 50:
                specific_steps += 1
        if specific_steps > 0:
            score += 1
            strengths.append(f"{specific_steps} steps are specific and detailed")
    else:
        issues.append("No steps defined")

    # Check instructions
    instructions = plan.get("instructions", "")
    if instructions and len(instructions) > 50:
        score += 1
        strengths.append("Instructions are detailed")
    else:
        issues.append("Instructions are vague or missing")

    max_score = 8
    return {
        "score": min(score, max_score),
        "max_score": max_score,
        "percentage": (score / max_score) * 100,
        "issues": issues,
        "strengths": strengths,
        "file_count": len(valid_files),
        "step_count": len(steps),
    }


def analyze_implementation(impl_path: Path) -> Dict[str, Any]:
    """Analyze implementation report quality."""
    if not impl_path.exists():
        return {"score": 0, "issues": ["Implementation report not found"]}

    try:
        impl = json.loads(impl_path.read_text())
    except Exception as e:
        return {"score": 0, "issues": [f"Failed to parse implementation: {e}"]}

    score = 0
    issues = []
    strengths = []

    # Check status
    status = impl.get("status", "")
    if status == "success" or status == "completed":
        score += 2
        strengths.append("Implementation completed successfully")
    elif status == "failed":
        issues.append("Implementation failed")
    else:
        issues.append(f"Unknown status: {status}")

    # Check files changed
    files_changed = impl.get("files_modified", []) or impl.get("files_changed", [])
    if len(files_changed) > 0:
        score += 2
        strengths.append(f"{len(files_changed)} files modified")
    else:
        issues.append("No files were modified")

    # Check for errors
    error = impl.get("error")
    if error:
        issues.append(f"Implementation error: {error}")
    else:
        score += 1
        strengths.append("No errors during implementation")

    max_score = 5
    return {
        "score": min(score, max_score),
        "max_score": max_score,
        "percentage": (score / max_score) * 100,
        "issues": issues,
        "strengths": strengths,
        "files_changed": len(files_changed),
    }


def analyze_test(test_path: Path) -> Dict[str, Any]:
    """Analyze test report quality."""
    if not test_path.exists():
        return {"score": 0, "issues": ["Test report not found"]}

    try:
        test = json.loads(test_path.read_text())
    except Exception as e:
        return {"score": 0, "issues": [f"Failed to parse test report: {e}"]}

    score = 0
    issues = []
    strengths = []

    # Check lint
    lint_passed = test.get("lint_passed", False)
    if lint_passed:
        score += 2
        strengths.append("Lint checks passed")
    else:
        issues.append("Lint checks failed")

    # Check tests
    tests_passed = test.get("tests_passed", False)
    if tests_passed:
        score += 2
        strengths.append("Tests passed")
    else:
        issues.append("Tests failed")

    # Check for errors
    errors = test.get("errors", [])
    if errors:
        issues.append(f"{len(errors)} test errors found")
    else:
        score += 1
        strengths.append("No test errors")

    max_score = 5
    return {
        "score": min(score, max_score),
        "max_score": max_score,
        "percentage": (score / max_score) * 100,
        "issues": issues,
        "strengths": strengths,
    }


def check_rag_usage(plan_path: Path) -> Dict[str, Any]:
    """Check if RAG was used in planning."""
    if not plan_path.exists():
        return {"used": False, "evidence": "Plan not found"}

    try:
        plan = json.loads(plan_path.read_text())
    except Exception:
        return {"used": False, "evidence": "Failed to parse plan"}

    # Check if files reference actual codebase
    files = plan.get("files", [])
    valid_files = [f for f in files if f.startswith("src/ybis")]
    
    if valid_files:
        return {
            "used": True,
            "evidence": f"Plan references {len(valid_files)} actual codebase files",
            "files": valid_files[:5],  # First 5
        }
    else:
        return {
            "used": False,
            "evidence": "No codebase files referenced (may indicate RAG not used)",
        }


def main():
    """Main analysis function."""
    import argparse

    parser = argparse.ArgumentParser(description="Analyze self-improve workflow quality")
    parser.add_argument("run_path", help="Path to run artifacts directory")
    args = parser.parse_args()

    run_path = Path(args.run_path)
    artifacts_dir = run_path / "artifacts" if (run_path / "artifacts").exists() else run_path

    print("=" * 70)
    print("Self-Improve Workflow Quality Analysis")
    print("=" * 70)
    print()

    # Analyze each phase
    reflection_result = analyze_reflection(artifacts_dir / "reflection_report.json")
    plan_result = analyze_plan(artifacts_dir / "improvement_plan.json")
    impl_result = analyze_implementation(artifacts_dir / "implementation_report.json")
    test_result = analyze_test(artifacts_dir / "test_report.json")
    rag_check = check_rag_usage(artifacts_dir / "improvement_plan.json")
    
    # Ensure all results have required keys
    for result in [reflection_result, plan_result, impl_result, test_result]:
        if "max_score" not in result:
            result["max_score"] = 10
        if "percentage" not in result:
            result["percentage"] = 0
        if "strengths" not in result:
            result["strengths"] = []
        if "issues" not in result:
            result["issues"] = []

    # Print results
    print("1. REFLECTION QUALITY")
    print("-" * 70)
    print(f"Score: {reflection_result['score']}/{reflection_result['max_score']} ({reflection_result['percentage']:.1f}%)")
    if reflection_result['strengths']:
        print("Strengths:")
        for s in reflection_result['strengths']:
            print(f"  ✓ {s}")
    if reflection_result['issues']:
        print("Issues:")
        for i in reflection_result['issues']:
            print(f"  ✗ {i}")
    print()

    print("2. PLAN QUALITY")
    print("-" * 70)
    print(f"Score: {plan_result['score']}/{plan_result['max_score']} ({plan_result['percentage']:.1f}%)")
    print(f"Files: {plan_result.get('file_count', 0)}, Steps: {plan_result.get('step_count', 0)}")
    if plan_result['strengths']:
        print("Strengths:")
        for s in plan_result['strengths']:
            print(f"  ✓ {s}")
    if plan_result['issues']:
        print("Issues:")
        for i in plan_result['issues']:
            print(f"  ✗ {i}")
    print()

    print("3. IMPLEMENTATION QUALITY")
    print("-" * 70)
    print(f"Score: {impl_result['score']}/{impl_result['max_score']} ({impl_result['percentage']:.1f}%)")
    print(f"Files Changed: {impl_result.get('files_changed', 0)}")
    if impl_result['strengths']:
        print("Strengths:")
        for s in impl_result['strengths']:
            print(f"  ✓ {s}")
    if impl_result['issues']:
        print("Issues:")
        for i in impl_result['issues']:
            print(f"  ✗ {i}")
    print()

    print("4. TEST QUALITY")
    print("-" * 70)
    print(f"Score: {test_result['score']}/{test_result['max_score']} ({test_result['percentage']:.1f}%)")
    if test_result['strengths']:
        print("Strengths:")
        for s in test_result['strengths']:
            print(f"  ✓ {s}")
    if test_result['issues']:
        print("Issues:")
        for i in test_result['issues']:
            print(f"  ✗ {i}")
    print()

    print("5. RAG USAGE")
    print("-" * 70)
    if rag_check['used']:
        print("✓ RAG appears to be used")
        print(f"  {rag_check['evidence']}")
        if rag_check.get('files'):
            print("  Sample files:")
            for f in rag_check['files']:
                print(f"    - {f}")
    else:
        print("✗ RAG may not be used")
        print(f"  {rag_check['evidence']}")
    print()

    # Overall score
    total_score = (
        reflection_result['score'] +
        plan_result['score'] +
        impl_result['score'] +
        test_result['score']
    )
    total_max = (
        reflection_result['max_score'] +
        plan_result['max_score'] +
        impl_result['max_score'] +
        test_result['max_score']
    )
    overall_percentage = (total_score / total_max) * 100

    print("=" * 70)
    print("OVERALL QUALITY SCORE")
    print("=" * 70)
    print(f"Total: {total_score}/{total_max} ({overall_percentage:.1f}%)")
    print()

    if overall_percentage >= 80:
        print("🎉 EXCELLENT QUALITY")
    elif overall_percentage >= 60:
        print("✅ GOOD QUALITY")
    elif overall_percentage >= 40:
        print("⚠️  MODERATE QUALITY - Needs Improvement")
    else:
        print("❌ POOR QUALITY - Significant Issues")

    return 0 if overall_percentage >= 60 else 1


if __name__ == "__main__":
    sys.exit(main())

