# automated-code-style-checker

A Python-based tool to check and fix code style violations. This tool enforces custom style rules, integrates with `flake8` and `autopep8`, and provides both a **command-line interface (CLI)** and a **graphical user interface (GUI)** for ease of use.

---

## Features

- **Custom Style Rules**:
  - Variable naming (snake_case).
  - Function naming (snake_case).
  - Class naming (CapWords).
  - Indentation (4 spaces).
  - Blank lines between functions/classes.
  - Docstrings for functions/classes.
  - Line length (79 characters).
  - Imports ordering.
  - Trailing whitespace.
  - Multiple statements per line.
  - Comparison with `is`.
  - Unnecessary semicolons.
  - Mutable default arguments.
  - File end blank line.
  - Unused imports.
  - Unused variables.

- **Integration with External Tools**:
  - Runs `flake8` for additional PEP 8 checks.
  - Uses `autopep8` to automatically fix PEP 8 violations.

- **Benchmarking**:
  - Measures execution time and memory usage for custom checks, `flake8`, and `autopep8`.

- **GUI Support**:
  - Provides a user-friendly interface for selecting files, running checks, and fixing violations.

- **GitHub Actions Integration**:
  - Automatically checks code style on pull requests using a GitHub Actions workflow.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/RayaYasmin1/automated-code-style-checker.git
   cd automated-code-style-checker