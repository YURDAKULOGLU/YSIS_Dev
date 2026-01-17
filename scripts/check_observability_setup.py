#!/usr/bin/env python3
"""
Check Observability Setup - Verify Langfuse and OpenTelemetry configuration.

This script checks if observability adapters are properly configured and available.
"""

import sys
import os
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def check_observability_setup():
    """Check observability setup status."""
    print("=" * 60)
    print("YBIS Observability Setup Check")
    print("=" * 60)
    print()
    
    # Check environment variables
    print("1. Environment Variables:")
    print("-" * 60)
    
    langfuse_public = os.getenv("LANGFUSE_PUBLIC_KEY")
    langfuse_secret = os.getenv("LANGFUSE_SECRET_KEY")
    langfuse_host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
    
    otel_service = os.getenv("OTEL_SERVICE_NAME", "ybis")
    otel_exporter = os.getenv("OTEL_EXPORTER", "console")
    otel_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    jaeger_endpoint = os.getenv("JAEGER_ENDPOINT")
    
    print("Langfuse:")
    print(f"  LANGFUSE_PUBLIC_KEY: {'✅ Set' if langfuse_public else '❌ Not set'}")
    print(f"  LANGFUSE_SECRET_KEY: {'✅ Set' if langfuse_secret else '❌ Not set'}")
    print(f"  LANGFUSE_HOST: {langfuse_host}")
    
    print()
    print("OpenTelemetry:")
    print(f"  OTEL_SERVICE_NAME: {otel_service}")
    print(f"  OTEL_EXPORTER: {otel_exporter}")
    if otel_exporter == "otlp":
        print(f"  OTEL_EXPORTER_OTLP_ENDPOINT: {otel_endpoint or '❌ Not set'}")
    elif otel_exporter == "jaeger":
        print(f"  JAEGER_ENDPOINT: {jaeger_endpoint or '❌ Not set'}")
    
    print()
    
    # Check adapters
    print("2. Adapter Availability:")
    print("-" * 60)
    
    try:
        from src.ybis.services.observability import get_observability_service
        
        obs = get_observability_service()
        print(f"Total adapters: {len(obs._adapters)}")
        print()
        
        for adapter in obs._adapters:
            adapter_name = adapter.__class__.__name__
            is_available = adapter.is_available()
            status = "✅ Available" if is_available else "❌ Not available"
            print(f"  - {adapter_name}: {status}")
            
            if not is_available:
                if "Langfuse" in adapter_name:
                    print("    → Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY")
                elif "OpenTelemetry" in adapter_name:
                    print("    → OpenTelemetry will work with console exporter by default")
        
        if len(obs._adapters) == 0:
            print("  ⚠️  No adapters loaded!")
            print("  → Check configs/profiles/default.yaml")
            print("  → Ensure adapters are enabled")
    except Exception as e:
        print(f"  ❌ Error checking adapters: {e}")
    
    print()
    
    # Check profile configuration
    print("3. Profile Configuration:")
    print("-" * 60)
    
    try:
        import yaml
        profile_path = project_root / "configs" / "profiles" / "default.yaml"
        if profile_path.exists():
            with open(profile_path) as f:
                profile = yaml.safe_load(f)
            
            adapters = profile.get("adapters", {})
            langfuse_enabled = adapters.get("langfuse_observability", {}).get("enabled", False)
            otel_enabled = adapters.get("opentelemetry_observability", {}).get("enabled", False)
            
            print(f"  langfuse_observability: {'✅ Enabled' if langfuse_enabled else '❌ Disabled'}")
            print(f"  opentelemetry_observability: {'✅ Enabled' if otel_enabled else '❌ Disabled'}")
        else:
            print("  ❌ Profile file not found")
    except Exception as e:
        print(f"  ❌ Error reading profile: {e}")
    
    print()
    
    # Summary
    print("=" * 60)
    print("Summary:")
    print("=" * 60)
    
    langfuse_ready = langfuse_public and langfuse_secret
    otel_ready = True  # OpenTelemetry works with console exporter by default
    
    if langfuse_ready and otel_ready:
        print("✅ Observability is properly configured!")
        print()
        print("Next steps:")
        print("  1. Run a workflow to generate traces")
        print("  2. Check Langfuse dashboard: https://cloud.langfuse.com")
        print("  3. Check OpenTelemetry traces (console or backend)")
    elif langfuse_ready:
        print("⚠️  Langfuse is ready, but OpenTelemetry needs configuration")
    elif otel_ready:
        print("⚠️  OpenTelemetry is ready, but Langfuse needs API keys")
    else:
        print("❌ Observability needs configuration")
        print()
        print("To enable Langfuse:")
        print("  export LANGFUSE_PUBLIC_KEY='your-key'")
        print("  export LANGFUSE_SECRET_KEY='your-key'")
        print()
        print("To enable OpenTelemetry:")
        print("  export OTEL_EXPORTER='console'  # or 'otlp', 'jaeger'")
        print("  export OTEL_SERVICE_NAME='ybis'")
    
    print("=" * 60)


if __name__ == "__main__":
    try:
        check_observability_setup()
    except KeyboardInterrupt:
        print("\n⚠️  Cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

