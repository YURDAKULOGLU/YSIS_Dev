import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os
from pathlib import Path

# Add parent directory to path to import the script
sys.path.append(str(Path(__file__).parent.parent))

# Import the module to be tested
import verify_doc_integrity as auditor

class TestIntegrityAuditor(unittest.TestCase):

    def setUp(self):
        # Mock configuration for testing
        self.mock_config = {
            "dependencies": [
                {
                    "source": "test_source.md",
                    "target": "test_target.md",
                    "status": "active",
                    "source_hash": "auto_managed"
                }
            ],
            "settings": {
                "auto_update_hashes": True
            }
        }

    @patch("verify_doc_integrity.load_lock_file")
    @patch("verify_doc_integrity.glob.glob")
    @patch("verify_doc_integrity.calculate_hash")
    @patch("verify_doc_integrity.save_lock_file")
    def test_auto_managed_hash_update(self, mock_save, mock_calc_hash, mock_glob, mock_load):
        """Test that 'auto_managed' triggers a hash update."""
        
        # Setup Mocks
        mock_load.return_value = self.mock_config
        mock_glob.return_value = ["/root/test_source.md"]
        mock_calc_hash.return_value = "new_hash_123"
        
        # Run Verification
        # We need to capture stdout/stderr to prevent clutter
        with patch('sys.stdout', new=MagicMock()):
            with self.assertRaises(SystemExit) as cm:
                auditor.verify_chain()
            
            # Assert Exit Code 0 (Success)
            self.assertEqual(cm.exception.code, 0)

        # Assert save_lock_file was called (meaning config was updated)
        mock_save.assert_called_once()
        
        # Verify the config passed to save has the new hash
        saved_config = mock_save.call_args[0][0]
        self.assertEqual(saved_config["dependencies"][0]["source_hash"], "new_hash_123")

    @patch("verify_doc_integrity.load_lock_file")
    @patch("verify_doc_integrity.glob.glob")
    @patch("verify_doc_integrity.calculate_hash")
    def test_hash_mismatch_failure(self, mock_calc_hash, mock_glob, mock_load):
        """Test that a hash mismatch causes a failure (SystemExit 1)."""
        
        # Config with a FIXED hash
        self.mock_config["dependencies"][0]["source_hash"] = "old_hash_fixed"
        
        mock_load.return_value = self.mock_config
        mock_glob.return_value = ["/root/test_source.md"]
        mock_calc_hash.return_value = "different_hash_now" # CHANGED!
        
        # Run Verification
        with patch('sys.stdout', new=MagicMock()):
            with self.assertRaises(SystemExit) as cm:
                auditor.verify_chain()
            
            # Assert Exit Code 1 (Failure)
            self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
