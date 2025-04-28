import unittest
from src.custom_rules import check_variable_naming, check_unused_imports, check_unused_variables

class TestCustomRules(unittest.TestCase):
    def test_check_variable_naming(self):
        file_path = "examples/example_bad_variable_name.py"  # <-- changed path
        violations = check_variable_naming(file_path)
        self.assertGreater(len(violations), 0)

    def test_check_unused_imports(self):
        file_path = "examples/example_bad_variable_name.py"  # <-- changed path
        violations = check_unused_imports(file_path)
        self.assertGreater(len(violations), 0)

    def test_check_unused_variables(self):
        file_path = "examples/example_bad_variable_name.py"  # <-- changed path
        violations = check_unused_variables(file_path)
        self.assertGreater(len(violations), 0)

if __name__ == "__main__":
    unittest.main()
