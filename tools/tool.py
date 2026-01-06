from langchain.tools import tool


@tool('add', return_direct=False)
def add_two_numbers(a: int, b: int) -> int:
    """Adds two numbers and returns the result"""
    return a + b

@tool('subtract', return_direct=False)
def subtract_two_numbers(a: int, b: int) -> int:
    """Subtracts two numbers and returns the result"""
    return a - b

@tool('multiply', return_direct=False)
def multiply_two_numbers(a: int, b: int) -> int:
    """Multiplies two numbers and returns the result"""
    return a * b

@tool('divide', return_direct=False)
def divide_two_numbers(a: int, b: int) -> int:
    """Divides two numbers and returns the result"""
    return a / b