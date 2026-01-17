def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b

def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    return a * b

def divide(a: float, b: float) -> float:
    """Return the division of two numbers with ZeroDivisionError handling."""
    try:
        return a / b
    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero.")
