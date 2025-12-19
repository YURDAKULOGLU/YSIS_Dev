import unittest
import sys
import os

# Add project root to path
sys.path.insert(0, os.getcwd())

from src.agentic.core.graphs.basic_graph import build_basic_graph

class TestBasicGraph(unittest.TestCase):
    def test_hello_world(self):
        # 1. Build
        app = build_basic_graph()
        
        # 2. Run
        initial_state = {"message": ""}
        result = app.invoke(initial_state)
        
        # 3. Verify
        # " Hello" + " World" = " Hello World"
        self.assertEqual(result["message"], " Hello World")

if __name__ == '__main__':
    unittest.main()