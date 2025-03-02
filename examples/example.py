import os
import sys  # Multiple imports on the same line (bad practice)

MyVariable = 42  # UpperCamelCase variable name (should be lowercase)
anotherVar = "hello"  # MixedCase variable name (should be lowercase)


def MyFunction():  # Function name should be snake_case
    print("This is a test function")

    x = 10   # No space around the equals sign (bad formatting)
    y = 10  # No space after '='
    z = 10

    if (x > 5):  # No space after 'if' and around '>'
        print("x is greater than 5")

    print("Hello")  # Extra spaces inside parentheses

    for i in range(10):
        print(i)  # Statement on the same line as loop (bad style)

    return x, y, z   # Returning multiple values without proper spacing


class myclass:  # Class name should be PascalCase (MyClass)
    def __init__(self):
        pass

    def myMethod(self):  # Method should be snake_case
        print("This is a method")


# Trailing whitespace issue
a = 5

b = "text"  # Unused variable

print("End of example file")
