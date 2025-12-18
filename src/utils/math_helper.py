def calculate_factorial(n):
    """Compute factorial using recursion"""
    if n == 0:
        return 1
    else:
        return n * calculate_factorial(n - 1)

if __name__ == "__main__":
    print("Factorial of 5 is:", calculate_factorial(5))
