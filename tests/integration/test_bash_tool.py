import unittest
import subprocess
from unittest.mock import patch
from src.tools.bash_tool import bash_tool

class TestBashTool(unittest.TestCase):
    def test_successful_command(self):
        """Test bash tool with a successful command execution"""
        result = bash_tool.invoke("echo 'Hello World'")
        self.assertEqual(result.strip(), "Hello World")

    @patch('subprocess.run')
    def test_command_with_error(self, mock_run):
        """Test bash tool when command fails"""
        # Configure mock to raise CalledProcessError
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd="invalid_command",
            output="",
            stderr="Command not found"
        )
        
        result = bash_tool.invoke("invalid_command")
        self.assertIn("Command failed with exit code 1", result)
        self.assertIn("Command not found", result)

    @patch('subprocess.run')
    def test_command_with_exception(self, mock_run):
        """Test bash tool when an unexpected exception occurs"""
        # Configure mock to raise a generic exception
        mock_run.side_effect = Exception("Unexpected error")
        
        result = bash_tool.invoke("some_command")
        self.assertIn("Error executing command: Unexpected error", result)

    def test_command_with_output(self):
        """Test bash tool with a command that produces output"""
        # Create a temporary file and write to it
        result = bash_tool.invoke("echo 'test content' > test_file.txt && cat test_file.txt && rm test_file.txt")
        self.assertEqual(result.strip(), "test content")

if __name__ == '__main__':
    unittest.main() 