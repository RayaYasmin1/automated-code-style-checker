import unittest
from src.style_checker import run_custom_tool, run_flake8

class TestCodeStyleChecker(unittest.TestCase):

    def test_run_custom_tool(self):
        file_path = "examples/example_bad_variable_name.py"
        violations = run_custom_tool(file_path)
        # Adjusted expected result based on the example file content
        self.assertEqual(len(violations), 2)  # Example file contains two violations

    def test_run_flake8(self):
        file_path = "examples/example_bad_variable_name.py"
        violations = run_flake8(file_path)
        # Adjusted expected result based on the example file content
        self.assertGreater(len(violations), 0)  # Flake8 should return some violations
