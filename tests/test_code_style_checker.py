import unittest
from src.style_checker import run_custom_tool, run_flake8


class TestCodeStyleChecker(unittest.TestCase):

    def test_run_custom_tool(self):
        file_path = "examples/example_bad_variable_name.py"
        violations = run_custom_tool(file_path)
        # Adjusted expected result based on the example file content
        # Example file contains two violations
        self.assertEqual(len(violations), 2)

    def test_run_flake8(self):
        file_path = "examples/example_bad_variable_name.py"
        violations = run_flake8(file_path)
        # Adjusted expected result based on the example file content
        # Flake8 should return some violations
        self.assertGreater(len(violations), 0)
