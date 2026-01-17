
def calculate_sum(x: int, y: int) -> int:
    """Calculate the sum of two integers.

    Args:
        x (int): The first integer.
        y (int): The second integer.

    Returns:
        int: The sum of the two integers.
    """
    return x + y

def print_sum(x: int, y: int) -> None:
    """Print the sum of two integers.

    Args:
        x (int): The first integer.
        y (int): The second integer.
    """
    z = calculate_sum(x, y)
    print("The sum of x and y is:", z)

print_sum(10, 20)
