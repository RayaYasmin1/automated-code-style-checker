import os
import sys
import time
import subprocess
import psutil
import re
import ast
import difflib

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
        print(f"Syntax error in file '{file_path}': {e}")
    except Exception as e:
        print(f"An error occurred while running the custom tool: {e}")
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
        print(f"An error occurred while running flake8: {e}")
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
        print(f"An error occurred while running autopep8: {e}")
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
        print(f"Syntax error in file '{file_path}': {e}")
        return ""
    except Exception as e:
        print(f"An error occurred while fixing custom violations: {e}")
        return ""

def benchmark_tool(custom_tool_function, flake8_function, autopep8_function, file_path):
    """Benchmark the custom tool, Flake8, and autopep8."""
    process = psutil.Process()

    # Run custom tool
    start_time = time.time()
    start_memory = process.memory_info().rss
    custom_violations = custom_tool_function(file_path)
    custom_time = time.time() - start_time
    custom_memory = process.memory_info().rss - start_memory

    # Run flake8
    start_time = time.time()
    start_memory = process.memory_info().rss
    flake8_violations = flake8_function(file_path)
    flake8_time = time.time() - start_time
    flake8_memory = process.memory_info().rss - start_memory

    # Run autopep8
    start_time = time.time()
    start_memory = process.memory_info().rss
    autopep8_output = autopep8_function(file_path)
    autopep8_time = time.time() - start_time
    autopep8_memory = process.memory_info().rss - start_memory

    return custom_violations, flake8_violations, autopep8_output, custom_time, flake8_time, autopep8_time, custom_memory, flake8_memory, autopep8_memory

def display_violations(violations, tool_name):
    """Display violations found by a tool."""
    if violations:
        print(f"\n{tool_name} Violations ({len(violations)} found):")
        for v in violations:
            print(f"Line {v['line_number']}, Column {v['column_number']}: {v['message']}")
    else:
        print(f"\n{tool_name}: No violations found. Your code is clean!")

def main():
    """Main function to run the code style checker."""
    print("Welcome to the Automated Code Style Checker!")
    print("This tool checks your Python file for PEP 8 violations and provides feedback.\n")

    while True:
        # Ask the user for the file path
        file_path = input("Enter the path to your Python file (or type 'exit' to quit): ").strip()

        # Allow the user to exit
        if file_path.lower() == 'exit':
            print("Exiting the program. Goodbye!")
            break

        # Normalize the file path
        file_path = os.path.normpath(file_path)

        # Check if the file exists and is a Python file
        if not os.path.isfile(file_path):
            print(f"Error: File '{file_path}' not found. Please try again.\n")
            continue
        if not file_path.endswith('.py'):
            print(f"Error: '{file_path}' is not a Python file. Please provide a .py file.\n")
            continue

        try:
            # Run the custom tool and display results
            print("\nRunning custom code style checker...")
            custom_violations = run_custom_tool(file_path)
            display_violations(custom_violations, "Custom Tool")

            # Run flake8 and display results
            print("\nRunning flake8...")
            flake8_violations = run_flake8(file_path)
            display_violations(flake8_violations, "Flake8")

            # Run autopep8 and display results
            print("\nRunning autopep8 to fix violations...")
            autopep8_output = run_autopep8(file_path)
            if autopep8_output:
                print("\nautopep8 output:")
                print(autopep8_output)
            else:
                print("\nautopep8: No fixes were applied.")

            # Fix custom violations
            print("\nFixing custom violations...")
            custom_diff = fix_custom_violations(file_path)
            if custom_diff:
                print("\nCustom Tool Fixes Applied:")
                print(custom_diff)
            else:
                print("\nCustom Tool: No fixes were applied.")

            # Benchmark the tools
            print("\nBenchmarking tools...")
            custom_violations, flake8_violations, autopep8_output, custom_time, flake8_time, autopep8_time, custom_memory, flake8_memory, autopep8_memory = benchmark_tool(
                run_custom_tool, run_flake8, run_autopep8, file_path)

            print(f"\nCustom Tool Execution Time: {custom_time:.6f} seconds")
            print(f"Flake8 Execution Time: {flake8_time:.6f} seconds")
            print(f"autopep8 Execution Time: {autopep8_time:.6f} seconds")

            print(f"\nCustom Tool Memory Usage: {custom_memory / 1024:.2f} KB")
            print(f"Flake8 Memory Usage: {flake8_memory / 1024:.2f} KB")
            print(f"autopep8 Memory Usage: {autopep8_memory / 1024:.2f} KB")

        except SyntaxError as e:
            print(f"\nSyntax error in file '{file_path}': {e}")
        except Exception as e:
            print(f"\nAn error occurred while processing the file '{file_path}': {e}")
            print("Skipping this file and continuing to the next one.\n")

        # Ask the user if they want to check another file
        another_file = input("\nDo you want to check another file? (yes/no): ").strip().lower()
        if another_file != 'yes':
            print("Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()