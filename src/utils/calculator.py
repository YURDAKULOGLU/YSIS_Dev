class Calculator:
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Subtract two numbers."""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Divide two numbers. Raises ValueError if divisor is zero."""
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

    def power(self, base: float, exponent: float) -> float:
        """Raise base to the power of exponent."""
        if base == 0 and exponent < 0:
            raise ValueError("Cannot raise zero to a negative power.")
        if base < 0 and not isinstance(exponent, int):
            raise ValueError("Cannot raise a negative number to a non-integer power.")
        return base ** exponent

    def power(self, base: float, exponent: float) -> float:
        """Raise base to the power of exponent."""
        if base == 0 and exponent < 0:
            raise ValueError("Cannot raise zero to a negative power.")
        if base < 0 and not isinstance(exponent, int):
            raise ValueError("Cannot raise a negative number to a non-integer power.")
        return base ** exponent
