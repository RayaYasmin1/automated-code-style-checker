import time
import subprocess
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
    check_end_blank_line
)

# Run custom tool
def run_custom_tool(file_path):
    violations = []
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

    return violations

# Run Flake8
def run_flake8(file_path):
    result = subprocess.run(['flake8', file_path], capture_output=True, text=True)
    violations = []
    for line in result.stdout.splitlines():
        parts = line.split(':')
        if len(parts) >= 3:
            violations.append({
                'line_number': int(parts[1]),
                'column_number': int(parts[2]),
                'message': parts[3]
            })
    return violations

# Benchmark the tools
def benchmark_tool(custom_tool_function, flake8_function, file_path):
    start_time = time.time()
    custom_violations = custom_tool_function(file_path)
    custom_time = time.time() - start_time

    start_time = time.time()
    flake8_violations = flake8_function(file_path)
    flake8_time = time.time() - start_time

    comparison_results = {
        'custom_only': [],
        'flake8_only': [],
        'common': []
    }

    # Compare results
    for custom in custom_violations:
        if custom not in flake8_violations:
            comparison_results['custom_only'].append(custom)
        else:
            comparison_results['common'].append(custom)

    for flake8 in flake8_violations:
        if flake8 not in custom_violations:
            comparison_results['flake8_only'].append(flake8)

    return custom_violations, flake8_violations, custom_time, flake8_time, comparison_results

# Example of running the benchmark
file_path = r'examples/example.py'  # Change to your file path
custom_violations, flake8_violations, custom_time, flake8_time, comparison_results = benchmark_tool(run_custom_tool, run_flake8, file_path)

# Print results
print(f"\nCustom Tool Violations ({len(custom_violations)} found):")
for v in custom_violations:
    print(f"Line {v['line_number']}, Column {v['column_number']}: {v['message']}")

print(f"\nFlake8 Violations ({len(flake8_violations)} found):")
for v in flake8_violations:
    print(f"Line {v['line_number']}, Column {v['column_number']}: {v['message']}")

print(f"\nCustom Tool Execution Time: {custom_time:.6f} seconds")
print(f"Flake8 Execution Time: {flake8_time:.6f} seconds")

# Print comparison results
print("\nComparison Results:")
print(f"Violations detected only by custom tool: {len(comparison_results['custom_only'])}")
print(f"Violations detected only by Flake8: {len(comparison_results['flake8_only'])}")
print(f"Common violations detected by both: {len(comparison_results['common'])}")

print("\nDetails of unique findings:")
if comparison_results['custom_only']:
    print("\nIssues found only by the custom tool:")
    for v in comparison_results['custom_only']:
        print(f"Line {v['line_number']}, Column {v['column_number']}: {v['message']}")

if comparison_results['flake8_only']:
    print("\nIssues found only by Flake8:")
    for v in comparison_results['flake8_only']:
        print(f"Line {v['line_number']}, Column {v['column_number']}: {v['message']}")

if comparison_results['common']:
    print("\nIssues found by both:")
    for v in comparison_results['common']:
        print(f"Line {v['line_number']}, Column {v['column_number']}: {v['message']}")

