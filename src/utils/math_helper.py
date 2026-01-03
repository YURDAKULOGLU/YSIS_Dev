import math

def calculate_factorial(n):
    """Calculate factorial of a number using math.factorial."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return math.factorial(n)

if __name__ == "__main__":
    print("Factorial of 5 is:", calculate_factorial(5))
