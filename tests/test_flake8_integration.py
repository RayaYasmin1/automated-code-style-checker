import unittest
from src.style_checker import run_flake8


class TestFlake8Integration(unittest.TestCase):

    def test_benchmark(self):
        file_path = "examples/example_bad_variable_name.py"
        flake8_violations = run_flake8(file_path)
        # Adjusted expected result based on the example file content
        # Flake8 should return some violations
        self.assertGreater(len(flake8_violations), 0)
