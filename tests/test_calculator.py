import pytest
from src.utils.calculator import Calculator

@pytest.fixture
def calculator():
    return Calculator()

def test_add(calculator):
    assert calculator.add(1, 2) == 3

def test_subtract(calculator):
    assert calculator.subtract(5, 3) == 2

def test_multiply(calculator):
    assert calculator.multiply(4, 6) == 24

def test_divide(calculator):
    assert calculator.divide(8, 2) == 4
    with pytest.raises(ValueError):
        calculator.divide(10, 0)

def test_power(calculator):
    assert calculator.power(2, 3) == 8
    assert calculator.power(5, 0) == 1
    assert calculator.power(0, 5) == 0
    assert calculator.power(3, 2.5) == pytest.approx(15.588457)
    with pytest.raises(ValueError):
        calculator.power(0, -1)  # Test for zero base and negative exponent
    with pytest.raises(ValueError):
        calculator.power(-1, 0.5)  # Test for negative base and fractional exponent
    assert calculator.power(2, 0) == 1
    assert calculator.power(10, 3) == 1000
    assert calculator.power(2, -2) == pytest.approx(0.25)

def test_power(calculator):
    assert calculator.power(2, 3) == 8
    assert calculator.power(5, 0) == 1
    assert calculator.power(0, 5) == 0
    assert calculator.power(3, 2.5) == pytest.approx(15.588457)
    with pytest.raises(ValueError):
        calculator.power(0, -1)  # Test for zero base and negative exponent
    with pytest.raises(ValueError):
        calculator.power(-1, 0.5)  # Test for negative base and fractional exponent
    assert calculator.power(2, 0) == 1
    assert calculator.power(10, 3) == 1000
    assert calculator.power(2, -2) == pytest.approx(0.25)
