import unittest
from src.custom_rules import check_custom_violations


class TestExample(unittest.TestCase):

    def test_example(self):
        file_path = "examples/example_bad_variable_name.py"
        violations = check_custom_violations(file_path)
        # Adjusted expected result based on the example file content
        # Example file contains two violations
        self.assertEqual(len(violations), 2)
