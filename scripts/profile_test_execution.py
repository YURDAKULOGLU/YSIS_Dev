#!/usr/bin/env python3
"""Profile test execution to find bottlenecks."""

import sys
import time
import cProfile
import pstats
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def profile_test():
    """Profile test execution."""
    print("Profiling test execution...")
    print("=" * 60)
    
    # Import and run test
    import pytest
    
    # Profile pytest execution
    profiler = cProfile.Profile()
    profiler.enable()
    
    start_time = time.time()
    
    # Run test
    exit_code = pytest.main([
        "tests/adapters/test_adapter_protocol.py",
        "-v",
        "--tb=short",
    ])
    
    elapsed = time.time() - start_time
    profiler.disable()
    
    print(f"\nTest completed in {elapsed:.2f}s")
    print(f"Exit code: {exit_code}")
    print("\n" + "=" * 60)
    print("TOP 20 FUNCTIONS BY TIME:")
    print("=" * 60)
    
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(20)
    
    print("\n" + "=" * 60)
    print("TOP 20 FUNCTIONS BY CALL COUNT:")
    print("=" * 60)
    
    stats.sort_stats('ncalls')
    stats.print_stats(20)

if __name__ == "__main__":
    profile_test()

