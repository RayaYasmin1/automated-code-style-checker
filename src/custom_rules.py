import ast
import re

# Rule 1: Variable Naming (snake_case)
def check_variable_naming(file_path):
    violations = []
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    variable_name = target.id
                    # Check if variable name is in snake_case
                    if not re.match(r'^[a-z_][a-z0-9_]*$', variable_name):
                        violations.append({
                            'line_number': target.lineno,
                            'column_number': target.col_offset,
                            'message': f"Variable '{variable_name}' should be snake_case"
                        })

    return violations


# Rule 2: Function Naming (snake_case)
def check_function_naming(file_path):
    violations = []
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            # Check if function name is in snake_case
            if not re.match(r'^[a-z_][a-z0-9_]*$', function_name):
                violations.append({
                    'line_number': node.lineno,
                    'column_number': node.col_offset,
                    'message': f"Function '{function_name}' should be snake_case"
                })

    return violations


# Rule 3: Class Naming (CapWords)
def check_class_naming(file_path):
    violations = []
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            # Check if class name follows CapWords convention
            if not re.match(r'^[A-Z][A-Za-z0-9]*$', class_name):
                violations.append({
                    'line_number': node.lineno,
                    'column_number': node.col_offset,
                    'message': f"Class '{class_name}' should use CapWords"
                })

    return violations


# Rule 4: Indentation (4 spaces)
def check_indentation(file_path):
    violations = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        if line.startswith(' '):
            if len(line) - len(line.lstrip()) % 4 != 0:
                violations.append({
                    'line_number': idx + 1,
                    'column_number': 0,
                    'message': f"Incorrect indentation at line {idx + 1} (use 4 spaces)"
                })

    return violations


# Rule 5: Blank Lines Between Functions/Classes
def check_blank_lines_between_functions(file_path):
    violations = []
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if hasattr(node, 'lineno') and node.lineno > 1:
                # Check if there's a blank line before functions/classes
                previous_line = node.lineno - 1
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    if lines[previous_line - 1].strip() != "":
                        violations.append({
                            'line_number': node.lineno,
                            'column_number': 0,
                            'message': f"Function/Class '{node.name}' should be preceded by a blank line"
                        })

    return violations


# Rule 6: Docstrings for Functions/Classes
def check_docstrings(file_path):
    violations = []
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if not ast.get_docstring(node):
                violations.append({
                    'line_number': node.lineno,
                    'column_number': 0,
                    'message': f"Function/Class '{node.name}' should have a docstring"
                })

    return violations


# Rule 7: Max Line Length (79 characters)
def check_line_length(file_path):
    violations = []
    max_line_length = 79
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        if len(line) > max_line_length:
            violations.append({
                'line_number': idx + 1,
                'column_number': 0,
                'message': f"Line {idx + 1} exceeds {max_line_length} characters"
            })

    return violations


# Rule 8: Imports Ordering
def check_imports_order(file_path):
    violations = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    imports = []
    for line in lines:
        if line.startswith('import') or line.startswith('from'):
            imports.append(line.strip())

    # Check that imports are ordered correctly: standard, third-party, then local
    for idx, imp in enumerate(imports):
        if idx > 0 and imp < imports[idx - 1]:
            violations.append({
                'line_number': lines.index(imp) + 1,
                'column_number': 0,
                'message': f"Imports should be ordered: {imp} appears before {imports[idx - 1]}"
            })

    return violations


# Rule 9: Trailing Whitespace
def check_trailing_whitespace(file_path):
    violations = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        if line.endswith(" \n") or line.endswith("\t\n"):
            violations.append({
                'line_number': idx + 1,
                'column_number': len(line) - 1,
                'message': f"Trailing whitespace found at the end of line {idx + 1}"
            })

    return violations


# Rule 10: Multiple Statements Per Line
def check_multiple_statements(file_path):
    violations = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        if ';' in line:
            violations.append({
                'line_number': idx + 1,
                'column_number': line.find(';'),
                'message': f"Multiple statements on a single line at line {idx + 1}"
            })

    return violations


# Rule 11: Comparison with `is`
def check_comparison_is(file_path):
    violations = []
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            if isinstance(node.ops[0], ast.Is) and isinstance(node.left, ast.NameConstant) and node.left.value is None:
                violations.append({
                    'line_number': node.lineno,
                    'column_number': node.col_offset,
                    'message': "Use 'is' to compare with 'None' instead of '=='."
                })

    return violations


# Rule 12: Unnecessary Semicolons
def check_semicolons(file_path):
    violations = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    for idx, line in enumerate(lines):
        if line.strip().endswith(';'):
            violations.append({
                'line_number': idx + 1,
                'column_number': len(line) - 1,
                'message': f"Unnecessary semicolon at the end of line {idx + 1}"
            })

    return violations


# Rule 13: Mutable Default Arguments
def check_mutable_default_args(file_path):
    violations = []
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                if isinstance(arg.annotation, ast.List) or isinstance(arg.annotation, ast.Dict):
                    violations.append({
                        'line_number': node.lineno,
                        'column_number': 0,
                        'message': f"Function '{node.name}' has a mutable default argument."
                    })

    return violations


# Rule 14: File End Blank Line
def check_end_blank_line(file_path):
    violations = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if lines[-1].strip() != "":
            violations.append({
                'line_number': len(lines),
                'column_number': 0,
                'message': "File should end with a blank line"
            })

    return violations


