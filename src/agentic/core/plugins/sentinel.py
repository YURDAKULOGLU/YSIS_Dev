import os
import sys
import ast
import subprocess
from pathlib import Path
from typing import List, Dict
from src.agentic.core.protocols import VerifierProtocol, CodeResult, VerificationResult

class SentinelVerifier(VerifierProtocol):
    """
    The Sentinel: A rigorous verifier that runs static analysis and tests.
    Upgraded for targeted verification (Smart Test Discovery).
    """

    def name(self) -> str:
        return "Sentinel-Health-Monitor"

    async def verify(self, code_result: CodeResult, sandbox_path: str) -> VerificationResult:
        print("[Sentinel] Starting health check...")
        
        errors = []
        warnings = []
        logs = {}
        files_checked = list(code_result.files_modified.keys())
        
        if not files_checked:
            print("[Sentinel] ⚠️ NO FILES MODIFIED. Marking verification as FAILED.")
            return VerificationResult(
                lint_passed=False,
                tests_passed=False,
                coverage=0.0,
                errors=["No files were modified by the executor."],
                warnings=[],
                logs={"status": "Failed: No changes detected."}
            )

        # 1. Static Analysis (AST Parse & Basic Lint)
        print("[Sentinel] 🔍 Phase 1: Syntax Analysis")
        for file_path in files_checked:
            if file_path.endswith(".py"):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        source = f.read()
                    ast.parse(source)
                except SyntaxError as e:
                    errors.append(f"SyntaxError in {file_path}: {e}")
                except Exception as e:
                    errors.append(f"Error reading {file_path}: {e}")

        if errors:
             print("[Sentinel] ❌ Syntax Errors Found.")
             return VerificationResult(
                lint_passed=False,
                tests_passed=False,
                coverage=0.0,
                errors=errors,
                warnings=warnings,
                logs={"phase": "syntax_check"}
            )

        # 2. Smart Test Discovery & Execution
        print("[Sentinel] 🧪 Phase 2: Targeted Testing")
        tests_to_run = set()
        
        for file_path in files_checked:
            if not file_path.endswith(".py"):
                continue
                
            path_obj = Path(file_path)
            file_name = path_obj.name
            
            # Case A: The file itself is a test
            if file_name.startswith("test_") or file_name.endswith("_test.py"):
                tests_to_run.add(file_path)
                continue
            
            # Case B: It's a source file, look for tests
            # 1. Look in 'tests/' folder at project root
            # 2. Look in same directory
            # 3. Look in 'tests/' subdirectory
            
            potential_test_names = [f"test_{file_name}", f"{path_obj.stem}_test.py"]
            
            # Search Logic (simplified for now)
            # We assume project root is current working dir for this simple implementation
            # In a robust system, we'd scan recursively but carefully
            
            # Check strictly known locations to avoid scanning huge legacy dirs
            candidates = []
            
            # Check standard tests/ folder
            if os.path.exists("tests"):
                for t_name in potential_test_names:
                    t_path = os.path.join("tests", t_name)
                    print(f"[Sentinel DEBUG] Checking path: {t_path}")
                    if os.path.exists(t_path):
                        print(f"[Sentinel DEBUG] Found test: {t_path}")
                        candidates.append(t_path)
            
            # Check adjacent test file
            for t_name in potential_test_names:
                t_path = path_obj.parent / t_name
                if t_path.exists():
                    candidates.append(str(t_path))

            if candidates:
                for c in candidates:
                    tests_to_run.add(str(c))
            else:
                warnings.append(f"No tests found for {file_name}. Verified via Syntax Check only.")

        if tests_to_run:
            print(f"[Sentinel] Found {len(tests_to_run)} relevant test files.")
            for test_file in tests_to_run:
                try:
                    print(f"[Sentinel] Running: {test_file}")
                    # Run pytest on specific file
                    test_result = subprocess.run(
                        [sys.executable, "-m", "pytest", test_file, "-q", "--tb=short", "--disable-warnings"], 
                        capture_output=True, 
                        text=True
                    )
                    
                    if test_result.returncode != 0:
                         print(f"[Sentinel] ❌ Test Failed: {test_file}")
                         # Capture clean error output
                         err_log = test_result.stdout + "\n" + test_result.stderr
                         errors.append(f"Test Failed ({test_file}):\n{err_log[-1000:]}") # Last 1000 chars
                    else:
                         print(f"[Sentinel] ✅ Test Passed: {test_file}")
                         
                except Exception as e:
                    errors.append(f"Failed to execute test {test_file}: {e}")
        else:
            print("[Sentinel] ℹ️ No relevant tests found. Proceeding based on Syntax Check.")

        return VerificationResult(
            lint_passed=len(errors) == 0,
            tests_passed=len(errors) == 0, 
            coverage=1.0 if not errors else 0.0,
            errors=errors,
            warnings=warnings,
            logs=logs
        )

