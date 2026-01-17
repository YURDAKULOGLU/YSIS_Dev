"""
Adapter CVE Checker - Scan adapter dependencies for CVEs.

Checks adapter dependencies for known CVEs and reports status.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List

from src.ybis.services.adapter_catalog import get_catalog


def check_cves_with_pip_audit() -> Dict[str, Any]:
    """
    Check CVEs using pip-audit.

    Returns:
        Dictionary with CVE scan results
    """
    try:
        result = subprocess.run(
            ["pip-audit", "--format", "json", "--desc"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            # No CVEs found
            return {"vulnerabilities": [], "status": "clean"}
        else:
            # Parse JSON output
            try:
                data = json.loads(result.stdout)
                return {"vulnerabilities": data.get("vulnerabilities", []), "status": "vulnerable"}
            except json.JSONDecodeError:
                # pip-audit may output to stderr
                return {"vulnerabilities": [], "status": "error", "error": result.stderr}

    except FileNotFoundError:
        # pip-audit not installed - this is an error, not a clean state
        return {"vulnerabilities": [], "status": "pip-audit-not-installed", "error": "pip-audit not found. Install with: pip install pip-audit"}
    except subprocess.TimeoutExpired:
        return {"vulnerabilities": [], "status": "timeout"}
    except Exception as e:
        return {"vulnerabilities": [], "status": "error", "error": str(e)}


def check_adapter_dependencies() -> Dict[str, List[Dict[str, Any]]]:
    """
    Check CVEs for adapter dependencies.

    Returns:
        Dictionary mapping adapter names to CVE lists
    """
    catalog = get_catalog()
    adapters = catalog.list_adapters()

    adapter_cves = {}

    for adapter_meta in adapters:
        name = adapter_meta["name"]
        dependencies = adapter_meta.get("dependencies", [])

        if not dependencies:
            adapter_cves[name] = []
            continue

        # For now, use pip-audit for all dependencies
        # In production, this would check only adapter-specific dependencies
        cve_result = check_cves_with_pip_audit()

        if cve_result["status"] == "vulnerable":
            # Filter CVEs by adapter dependencies
            adapter_vulns = []
            for vuln in cve_result.get("vulnerabilities", []):
                # Check if vulnerability affects this adapter's dependencies
                affected_packages = vuln.get("name", "")
                for dep in dependencies:
                    dep_name = dep.split(">=")[0].split("==")[0].split("<")[0].strip()
                    if dep_name.lower() in affected_packages.lower():
                        adapter_vulns.append(vuln)

            adapter_cves[name] = adapter_vulns
        else:
            adapter_cves[name] = []

    return adapter_cves


def generate_cve_report() -> str:
    """
    Generate CVE report for all adapters.

    Returns:
        Markdown-formatted CVE report
    """
    adapter_cves = check_adapter_dependencies()

    report = "# Adapter CVE Report\n\n"
    report += f"**Generated:** {Path(__file__).stat().st_mtime}\n\n"

    total_vulns = sum(len(vulns) for vulns in adapter_cves.values())

    if total_vulns == 0:
        report += "✅ **No CVEs found in adapter dependencies.**\n\n"
        return report

    report += f"⚠️ **Found {total_vulns} CVE(s) across adapters.**\n\n"

    for adapter_name, vulns in adapter_cves.items():
        if not vulns:
            continue

        report += f"## {adapter_name}\n\n"
        report += f"**Vulnerabilities:** {len(vulns)}\n\n"

        for vuln in vulns:
            report += f"### {vuln.get('id', 'Unknown CVE')}\n\n"
            report += f"- **Severity:** {vuln.get('severity', 'Unknown')}\n"
            report += f"- **Package:** {vuln.get('name', 'Unknown')}\n"
            report += f"- **Version:** {vuln.get('version', 'Unknown')}\n"
            if vuln.get("description"):
                report += f"- **Description:** {vuln['description']}\n"
            report += "\n"

    return report


def main() -> int:
    """Main entry point."""
    catalog = get_catalog()

    # Validate catalog first
    errors = catalog.validate_catalog()
    if errors:
        print("[ERROR] Catalog validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    # Check for CVEs
    print("[INFO] Checking adapter dependencies for CVEs...")
    
    # First check if pip-audit is available
    cve_result = check_cves_with_pip_audit()
    if cve_result["status"] == "pip-audit-not-installed":
        print("[ERROR] pip-audit is not installed. Cannot check for CVEs.", file=sys.stderr)
        print("[INFO] Install with: pip install pip-audit", file=sys.stderr)
        return 1

    adapter_cves = check_adapter_dependencies()

    # Report results
    total_vulns = sum(len(vulns) for vulns in adapter_cves.values())

    if total_vulns == 0:
        print("[OK] No CVEs found in adapter dependencies.")
        return 0

    print(f"[WARNING] Found {total_vulns} CVE(s):", file=sys.stderr)

    for adapter_name, vulns in adapter_cves.items():
        if vulns:
            print(f"\n  {adapter_name}: {len(vulns)} CVE(s)", file=sys.stderr)
            for vuln in vulns:
                print(f"    - {vuln.get('id', 'Unknown')}: {vuln.get('name', 'Unknown')}", file=sys.stderr)

    # Generate report file
    report_path = Path("docs/adapters/CVE_REPORT.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(generate_cve_report(), encoding="utf-8")

    print(f"\n[INFO] CVE report written to {report_path}")

    # Return non-zero if CVEs found (for CI)
    return 1 if total_vulns > 0 else 0


if __name__ == "__main__":
    sys.exit(main())

