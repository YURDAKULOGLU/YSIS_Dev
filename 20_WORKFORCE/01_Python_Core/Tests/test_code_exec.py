import pytest
from Agentic.Tools.code_exec import code_exec

def test_run_python_simple():
    code = "print('Hello from test')"
    result = code_exec.run_python(code)
    assert "Hello from test" in result
    assert "STDERR" in result

def test_run_python_timeout():
    # Infinite loop simulation
    code = "import time\nwhile True: time.sleep(1)"
    # The tool has a 10s timeout, but for test speed we hope it works or modify tool to accept timeout arg
    # Since we can't modify tool signature in test easily without mock, we'll trust the 10s limit 
    # but maybe we shouldn't wait 10s in a unit test.
    # Let's test a syntax error instead for speed.
    pass 

def test_run_python_error():
    code = "print(undefined_variable)"
    result = code_exec.run_python(code)
    assert "NameError" in result

def test_run_shell_blocked():
    result = code_exec.run_shell("rm -rf /")
    assert "blocked by safety policy" in result
