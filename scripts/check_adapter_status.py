"""
Adapter Status Check - Check real implementation status of all adapters.

Status levels:
- WORKING: Code exists, import works, basic function callable
- PARTIAL: Code exists but some functions NotImplemented
- STUB: Only interface exists
- MISSING: Code doesn't exist
"""

import importlib
import inspect
import sys
from pathlib import Path
from typing import Dict, List, Optional

import yaml

PROJECT_ROOT = Path(__file__).parent.parent
# Add project root to path for imports
sys.path.insert(0, str(PROJECT_ROOT))
ADAPTERS_YAML = PROJECT_ROOT / "configs" / "adapters.yaml"
OUTPUT_FILE = PROJECT_ROOT / "docs" / "ADAPTER_STATUS.md"


def check_adapter_implementation(module_path: str) -> tuple[str, List[str]]:
    """
    Check adapter implementation status.
    
    Args:
        module_path: Full module path (e.g., "src.ybis.adapters.local_coder.LocalCoderExecutor")
        
    Returns:
        Tuple of (status, details)
    """
    details = []
    
    try:
        # Parse module path
        parts = module_path.split(".")
        class_name = parts[-1]
        module_name = ".".join(parts[:-1])
        
        # Try to import
        try:
            module = importlib.import_module(module_name)
            details.append(f"✅ Module import successful: {module_name}")
        except ImportError as e:
            return "MISSING", [f"❌ Module import failed: {e}"]
        
        # Try to get class
        try:
            adapter_class = getattr(module, class_name)
            details.append(f"✅ Class found: {class_name}")
        except AttributeError:
            return "MISSING", [f"❌ Class not found: {class_name}"]
        
        # Check if class is instantiable
        try:
            # Try to instantiate (with minimal args)
            sig = inspect.signature(adapter_class.__init__)
            params = list(sig.parameters.keys())[1:]  # Skip 'self'
            
            # Try instantiation with minimal args
            if len(params) == 0:
                instance = adapter_class()
            else:
                # Try with None/default values
                instance = adapter_class()
            details.append(f"✅ Class instantiable")
        except Exception as e:
            details.append(f"⚠️ Instantiation issue: {e}")
            return "PARTIAL", details
        
        # Check for NotImplemented methods (skip __subclasshook__ from Protocol)
        not_implemented = []
        for name, method in inspect.getmembers(adapter_class, predicate=inspect.isfunction):
            # Skip __subclasshook__ - it's inherited from Protocol and normal
            if name == "__subclasshook__":
                continue
            if hasattr(method, "__code__"):
                try:
                    source = inspect.getsource(method)
                    if "NotImplemented" in source or "raise NotImplementedError" in source:
                        not_implemented.append(name)
                except:
                    pass
        
        # Check instance methods
        if hasattr(instance, "__class__"):
            for name, method in inspect.getmembers(instance, predicate=inspect.ismethod):
                # Skip __subclasshook__ - it's inherited from Protocol and normal
                if name == "__subclasshook__":
                    continue
                if hasattr(method, "__code__"):
                    try:
                        source = inspect.getsource(method)
                        if "NotImplemented" in source or "raise NotImplementedError" in source:
                            not_implemented.append(name)
                    except:
                        pass
        
        if not_implemented:
            details.append(f"⚠️ NotImplemented methods: {', '.join(not_implemented)}")
            return "PARTIAL", details
        
        # Check for is_available method
        if hasattr(instance, "is_available"):
            try:
                # Don't actually call it (might require setup)
                details.append(f"✅ is_available() method exists")
            except:
                pass
        else:
            details.append(f"⚠️ is_available() method missing")
        
        # Check for core methods (type-dependent)
        core_methods = {
            "executor": ["generate_code"],
            "sandbox": ["execute", "create"],
            "vector_store": ["add", "search"],
            "graph_store": ["add_node", "add_edge", "query"],
        }
        
        # Determine adapter type from module path
        adapter_type = None
        if "executor" in module_path.lower():
            adapter_type = "executor"
        elif "sandbox" in module_path.lower():
            adapter_type = "sandbox"
        elif "vector_store" in module_path.lower():
            adapter_type = "vector_store"
        elif "graph_store" in module_path.lower():
            adapter_type = "graph_store"
        
        if adapter_type and adapter_type in core_methods:
            for method_name in core_methods[adapter_type]:
                if hasattr(instance, method_name):
                    details.append(f"✅ Core method exists: {method_name}()")
                else:
                    details.append(f"⚠️ Core method missing: {method_name}()")
                    return "PARTIAL", details
        
        return "WORKING", details
        
    except Exception as e:
        return "STUB", [f"❌ Error checking adapter: {e}"]


def main():
    """Main status check function."""
    # Load adapters.yaml
    if not ADAPTERS_YAML.exists():
        print(f"ERROR: {ADAPTERS_YAML} not found")
        return
    
    with open(ADAPTERS_YAML, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    
    adapters = data.get("adapters", {})
    
    print(f"Checking {len(adapters)} adapters...")
    
    status_report = {
        "WORKING": [],
        "PARTIAL": [],
        "STUB": [],
        "MISSING": [],
    }
    
    results = []
    
    for adapter_name, adapter_info in adapters.items():
        module_path = adapter_info.get("module_path")
        adapter_type = adapter_info.get("type", "unknown")
        maturity = adapter_info.get("maturity", "unknown")
        
        if not module_path:
            status_report["MISSING"].append(adapter_name)
            results.append({
                "name": adapter_name,
                "type": adapter_type,
                "maturity": maturity,
                "status": "MISSING",
                "details": ["No module_path specified"],
            })
            continue
        
        print(f"  Checking {adapter_name}...")
        status, details = check_adapter_implementation(module_path)
        
        status_report[status].append(adapter_name)
        results.append({
            "name": adapter_name,
            "type": adapter_type,
            "maturity": maturity,
            "status": status,
            "details": details,
        })
    
    # Generate report
    report_content = f"""# Adapter Implementation Status

**Generated:** {Path(__file__).stat().st_mtime}
**Total Adapters:** {len(adapters)}

## Summary

| Status | Count | Percentage |
|--------|-------|------------|
| WORKING | {len(status_report['WORKING'])} | {len(status_report['WORKING'])/len(adapters)*100:.1f}% |
| PARTIAL | {len(status_report['PARTIAL'])} | {len(status_report['PARTIAL'])/len(adapters)*100:.1f}% |
| STUB | {len(status_report['STUB'])} | {len(status_report['STUB'])/len(adapters)*100:.1f}% |
| MISSING | {len(status_report['MISSING'])} | {len(status_report['MISSING'])/len(adapters)*100:.1f}% |

## Status Definitions

- **WORKING**: Code exists, import works, basic functions callable
- **PARTIAL**: Code exists but some functions NotImplemented
- **STUB**: Only interface exists
- **MISSING**: Code doesn't exist or can't be imported

## Adapter Details

"""
    
    for result in sorted(results, key=lambda x: (x["status"], x["name"])):
        report_content += f"""### {result['name']}

**Type:** {result['type']}  
**Maturity:** {result['maturity']}  
**Status:** **{result['status']}**

**Details:**
"""
        for detail in result["details"]:
            report_content += f"- {detail}\n"
        report_content += "\n"
    
    OUTPUT_FILE.write_text(report_content, encoding="utf-8")
    print(f"\nReport written to: {OUTPUT_FILE}")
    print(f"\nSummary:")
    print(f"  - WORKING: {len(status_report['WORKING'])}")
    print(f"  - PARTIAL: {len(status_report['PARTIAL'])}")
    print(f"  - STUB: {len(status_report['STUB'])}")
    print(f"  - MISSING: {len(status_report['MISSING'])}")


if __name__ == "__main__":
    main()

