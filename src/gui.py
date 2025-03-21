import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import psutil
import time
import re
import ast
import difflib  # For generating diffs

# Import custom rules
from custom_rules import (
    check_variable_naming,
    check_function_naming,
    check_class_naming,
    check_indentation,
    check_blank_lines_between_functions,
    check_docstrings,
    check_line_length,
    check_imports_order,
    check_trailing_whitespace,
    check_multiple_statements,
    check_comparison_is,
    check_semicolons,
    check_mutable_default_args,
    check_end_blank_line,
    check_unused_imports,
    check_unused_variables,
)

def run_custom_tool(file_path):
    """Run the custom code style checker tool on the specified file."""
    violations = []
    try:
        violations.extend(check_variable_naming(file_path))
        violations.extend(check_function_naming(file_path))
        violations.extend(check_class_naming(file_path))
        violations.extend(check_indentation(file_path))
        violations.extend(check_blank_lines_between_functions(file_path))
        violations.extend(check_docstrings(file_path))
        violations.extend(check_line_length(file_path))
        violations.extend(check_imports_order(file_path))
        violations.extend(check_trailing_whitespace(file_path))
        violations.extend(check_multiple_statements(file_path))
        violations.extend(check_comparison_is(file_path))
        violations.extend(check_semicolons(file_path))
        violations.extend(check_mutable_default_args(file_path))
        violations.extend(check_end_blank_line(file_path))
        violations.extend(check_unused_imports(file_path))
        violations.extend(check_unused_variables(file_path))
    except SyntaxError as e:
        messagebox.showerror("Syntax Error", f"Invalid Python syntax in file: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while running the custom tool: {e}")
    return violations

def run_flake8(file_path):
    """Run Flake8 on the specified file and return violations."""
    violations = []
    try:
        # Run flake8 with the file path
        result = subprocess.run(['flake8', file_path], capture_output=True, text=True)
        print(f"Flake8 Raw Output: {result.stdout}")  # Debug statement
        for line in result.stdout.splitlines():
            print(f"Processing line: {line}")  # Debug statement
            # Flake8 output format: file_path:line_number:column_number:error_code message
            match = re.match(r"^(.*):(\d+):(\d+):\s*(\w+\d+)\s*(.*)$", line)
            if match:
                file_part, line_number, column_number, error_code, message = match.groups()
                violation = {
                    'file_path': file_part.strip(),
                    'line_number': int(line_number.strip()),
                    'column_number': int(column_number.strip()),
                    'message': f"{error_code} {message.strip()}",
                }
                violations.append(violation)
            else:
                print(f"Skipping invalid line: {line}")  # Debug if something unexpected appears
        print(f"Violations List: {violations}")  # Debug statement
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while running flake8: {e}")
    return violations

def run_autopep8(file_path):
    """Run autopep8 on the specified file and return the diff output."""
    try:
        # Run autopep8 in diff mode to capture changes
        diff_result = subprocess.run(['autopep8', '--diff', file_path], capture_output=True, text=True)
        print("autopep8 diff output:", diff_result.stdout)  # Debug statement

        if diff_result.stdout:
            # If there are changes, apply them using --in-place
            subprocess.run(['autopep8', '--in-place', file_path], capture_output=True, text=True)
        return diff_result.stdout
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while running autopep8: {e}")
        return ""

def fix_custom_violations(file_path):
    """Fix custom tool violations in the specified file."""
    try:
        print(f"Fixing custom violations for file: {file_path}")  # Debug statement

        with open(file_path, 'r') as file:
            original_code = file.readlines()

        # Print original code for debugging
        print("Original Code:")
        print(''.join(original_code))

        # Parse the source code into an AST
        tree = ast.parse(''.join(original_code))

        # Debug: Print the AST before modification
        print("AST Before Modification:")
        print(ast.dump(tree, indent=4))

        # Track all used names in the code
        used_names = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used_names.add(node.id)

        # Fix variable naming (snake_case)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if not re.match(r'^[a-z_][a-z0-9_]*$', target.id):
                            target.id = re.sub(r'([A-Z])', r'_\1', target.id).lower()

        # Fix function naming (snake_case)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                    node.name = re.sub(r'([A-Z])', r'_\1', node.name).lower()

        # Fix class naming (CapWords)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not re.match(r'^[A-Z][A-Za-z0-9]*$', node.name):
                    node.name = node.name.title().replace('_', '')

        # Fix indentation (ensure 4 spaces per level)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.If, ast.For, ast.While)):
                for child in ast.iter_child_nodes(node):
                    if hasattr(child, 'col_offset'):
                        # Ensure indentation is a multiple of 4 spaces
                        child.col_offset = (child.col_offset // 4) * 4

        # Remove unused imports
        new_body = []
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                # For Import nodes, keep only used names
                if isinstance(node, ast.Import):
                    names_to_keep = [alias for alias in node.names if alias.name in used_names]
                    if names_to_keep:
                        node.names = names_to_keep
                        new_body.append(node)
                # For ImportFrom nodes, keep only used names
                elif isinstance(node, ast.ImportFrom):
                    names_to_keep = [alias for alias in node.names if alias.name in used_names]
                    if names_to_keep:
                        node.names = names_to_keep
                        new_body.append(node)
            else:
                new_body.append(node)

        # Update the tree's body with the filtered nodes
        tree.body = new_body

        # Add blank lines before functions/classes
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if node.lineno > 1 and not original_code[node.lineno - 2].strip():
                    continue  # Already has a blank line
                original_code.insert(node.lineno - 1, '\n')

        # Add docstrings only if they don't already exist
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if not ast.get_docstring(node):
                    docstring = "This is a docstring."  # Replace with a more appropriate message
                    node.body.insert(0, ast.Expr(value=ast.Str(s=docstring)))

        # Debug: Print the AST after modification
        print("AST After Modification:")
        print(ast.dump(tree, indent=4))

        # Convert the modified AST back to source code
        fixed_code = ast.unparse(tree)

        # Print fixed code for debugging
        print("Fixed Code:")
        print(fixed_code)

        # Write the fixed code back to the file
        with open(file_path, 'w') as file:
            file.write(fixed_code)

        # Generate a diff to show changes
        diff = difflib.unified_diff(
            original_code,
            fixed_code.splitlines(keepends=True),
            fromfile='original/' + file_path,
            tofile='fixed/' + file_path,
        )
        diff_output = ''.join(diff)
        print("Generated diff output:", diff_output)  # Debug statement
        return diff_output
    except SyntaxError as e:
        messagebox.showerror("Syntax Error", f"Invalid Python syntax in file: {e}")
        return ""
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while fixing custom violations: {e}")
        return ""

class CodeStyleCheckerApp:
    """GUI application for checking and fixing code style violations."""

    def __init__(self, root):
        """Initialize the GUI application."""
        self.root = root
        self.root.title("Automated Code Style Checker")
        self.root.geometry("1000x800")  # Increase the size of the main window

        # File Selection
        self.file_path = None
        self.file_label = tk.Label(root, text="Selected File: None", font=("Arial", 12))
        self.file_label.pack(pady=10)

        self.select_file_button = tk.Button(root, text="Select Python File", command=self.select_file)
        self.select_file_button.pack(pady=10)

        # Run Checks
        self.run_checks_button = tk.Button(root, text="Run Checks", command=self.run_checks, state=tk.DISABLED)
        self.run_checks_button.pack(pady=10)

        # Display Results
        self.results_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30)
        self.results_text.pack(pady=10)

        # Fix Violations
        self.fix_violations_button = tk.Button(root, text="Fix Violations", command=self.fix_violations, state=tk.DISABLED)
        self.fix_violations_button.pack(pady=10)

        # Exit
        self.exit_button = tk.Button(root, text="Exit", command=root.quit)
        self.exit_button.pack(pady=10)

    def select_file(self):
        """Select a Python file for analysis."""
        self.file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if self.file_path:
            self.file_label.config(text=f"Selected File: {self.file_path}")
            self.run_checks_button.config(state=tk.NORMAL)
            self.fix_violations_button.config(state=tk.NORMAL)

    def run_checks(self):
        """Run custom tool and Flake8 checks on the selected file."""
        if not self.file_path:
            messagebox.showerror("Error", "No file selected!")
            return

        self.results_text.delete(1.0, tk.END)  # Clear previous results

        # Initialize process for memory tracking
        process = psutil.Process()

        # Run custom tool
        start_time = time.time()
        start_memory = process.memory_info().rss  # Memory usage before running the tool
        custom_violations = run_custom_tool(self.file_path)
        custom_time = time.time() - start_time
        custom_memory = process.memory_info().rss - start_memory  # Memory usage after running the tool

        # Display custom tool violations
        self.results_text.insert(tk.END, f"Custom Tool Violations ({len(custom_violations)} found):\n")
        for v in custom_violations:
            self.results_text.insert(tk.END, f"Line {v['line_number']}, Column {v['column_number']}: {v['message']}\n")

        # Run flake8
        start_time = time.time()
        start_memory = process.memory_info().rss  # Memory usage before running Flake8
        flake8_violations = run_flake8(self.file_path)
        flake8_time = time.time() - start_time
        flake8_memory = process.memory_info().rss - start_memory  # Memory usage after running Flake8

        # Display flake8 violations
        self.results_text.insert(tk.END, f"\nFlake8 Violations ({len(flake8_violations)} found):\n")
        if flake8_violations:
            for v in flake8_violations:
                self.results_text.insert(tk.END, f"Line {v['line_number']}, Column {v['column_number']}: {v['message']}\n")
        else:
            self.results_text.insert(tk.END, "No Flake8 violations found.\n")

        # Display benchmarking results
        self.results_text.insert(tk.END, "\nBenchmarking Results:\n")
        self.results_text.insert(tk.END, f"Custom Tool Execution Time: {custom_time:.6f} seconds\n")
        self.results_text.insert(tk.END, f"Custom Tool Memory Usage: {custom_memory / 1024:.2f} KB\n")  # Memory usage in KB
        self.results_text.insert(tk.END, f"Flake8 Execution Time: {flake8_time:.6f} seconds\n")
        self.results_text.insert(tk.END, f"Flake8 Memory Usage: {flake8_memory / 1024:.2f} KB\n")  # Memory usage in KB

    def fix_violations(self):
        """Fix violations in the selected file using custom tool and autopep8."""
        if not self.file_path:
            messagebox.showerror("Error", "No file selected!")
            return

        # Fix custom tool violations
        print("Running custom tool fixes...")  # Debug statement
        custom_diff = fix_custom_violations(self.file_path)
        print("Custom tool diff output:", custom_diff)  # Debug statement

        self.results_text.insert(tk.END, "\nCustom Tool Fixes Applied:\n")
        self.results_text.insert(tk.END, custom_diff)

        # Always run autopep8 to fix other PEP 8 violations
        print("Running autopep8...")  # Debug statement
        autopep8_output = run_autopep8(self.file_path)
        print("autopep8 output:", autopep8_output)  # Debug statement

        if autopep8_output:
            self.results_text.insert(tk.END, "\nautopep8 Output (Fixes Applied):\n")
            self.results_text.insert(tk.END, autopep8_output)
        else:
            self.results_text.insert(tk.END, "\nautopep8: No fixes were applied.\n")

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = CodeStyleCheckerApp(root)
    root.mainloop()