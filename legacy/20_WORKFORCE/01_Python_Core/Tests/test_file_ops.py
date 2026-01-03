import os
import shutil
import pytest
from Agentic.Tools.file_ops import file_ops

TEST_DIR = "test_sandbox"

@pytest.fixture
def setup_sandbox():
    os.makedirs(TEST_DIR, exist_ok=True)
    yield
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)

def test_write_read_file(setup_sandbox):
    path = os.path.join(TEST_DIR, "test.txt")
    content = "Hello World"

    # Write
    result = file_ops.write_file(path, content)
    assert "Successfully wrote" in result
    assert os.path.exists(path)

    # Read
    read_content = file_ops.read_file(path)
    assert read_content == content

def test_list_dir(setup_sandbox):
    path1 = os.path.join(TEST_DIR, "file1.txt")
    path2 = os.path.join(TEST_DIR, "file2.txt")
    file_ops.write_file(path1, "1")
    file_ops.write_file(path2, "2")

    listing = file_ops.list_dir(TEST_DIR)
    assert "file1.txt" in listing
    assert "file2.txt" in listing
