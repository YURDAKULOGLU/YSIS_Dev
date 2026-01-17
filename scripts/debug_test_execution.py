#!/usr/bin/env python3
"""Debug test execution - Find what's taking so long."""

import sys
import time
import subprocess
from pathlib import Path

# Fix Windows encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def debug_test_execution():
    """Debug test execution step by step."""
    print("=" * 60)
    print("DEBUGGING TEST EXECUTION")
    print("=" * 60)
    print()
    
    test_file = "tests/adapters/test_adapter_protocol.py"
    
    # Step 1: Check if test file exists
    print("Step 1: Checking test file...")
    test_path = project_root / test_file
    if test_path.exists():
        print(f"✅ Test file exists: {test_path}")
        print(f"   Size: {test_path.stat().st_size} bytes")
    else:
        print(f"❌ Test file not found: {test_path}")
        return
    print()
    
    # Step 2: Build command
    print("Step 2: Building pytest command...")
    cmd = [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short", "--no-header"]
    print(f"Command: {' '.join(cmd)}")
    print()
    
    # Step 3: Start subprocess with timing
    print("Step 3: Starting subprocess...")
    start_time = time.time()
    
    try:
        process = subprocess.Popen(
            cmd,
            cwd=project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,  # Line buffered
        )
        
        init_time = time.time() - start_time
        print(f"✅ Process started in {init_time:.2f}s")
        print(f"   PID: {process.pid}")
        print()
        
        # Step 4: Monitor output in real-time
        print("Step 4: Monitoring output (first 30 seconds)...")
        print("-" * 60)
        
        output_lines = []
        stderr_lines = []
        timeout = 30  # 30 second monitoring window
        
        import select
        import threading
        
        def read_stdout():
            for line in process.stdout:
                output_lines.append(line)
                print(f"[STDOUT] {line.rstrip()}")
        
        def read_stderr():
            for line in process.stderr:
                stderr_lines.append(line)
                print(f"[STDERR] {line.rstrip()}")
        
        stdout_thread = threading.Thread(target=read_stdout, daemon=True)
        stderr_thread = threading.Thread(target=read_stderr, daemon=True)
        
        stdout_thread.start()
        stderr_thread.start()
        
        # Wait for process or timeout
        elapsed = 0
        while process.poll() is None and elapsed < timeout:
            time.sleep(1)
            elapsed += 1
            if elapsed % 5 == 0:
                print(f"[INFO] Still running... ({elapsed}s elapsed)")
        
        if process.poll() is None:
            print(f"\n⚠️  Process still running after {timeout}s")
            print("   Checking what it's doing...")
            
            # Try to get process info
            try:
                import psutil
                proc = psutil.Process(process.pid)
                print(f"   CPU: {proc.cpu_percent()}%")
                print(f"   Memory: {proc.memory_info().rss / 1024 / 1024:.2f} MB")
                print(f"   Status: {proc.status()}")
                print(f"   Threads: {proc.num_threads()}")
            except ImportError:
                print("   (Install psutil for detailed process info)")
            
            # Kill process
            print("\n⚠️  Killing process...")
            process.kill()
            process.wait()
        else:
            return_code = process.returncode
            total_time = time.time() - start_time
            print(f"\n✅ Process completed in {total_time:.2f}s")
            print(f"   Exit code: {return_code}")
            print(f"   Output lines: {len(output_lines)}")
            print(f"   Error lines: {len(stderr_lines)}")
            
            if output_lines:
                print("\nLast 10 output lines:")
                for line in output_lines[-10:]:
                    print(f"  {line.rstrip()}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_test_execution()

