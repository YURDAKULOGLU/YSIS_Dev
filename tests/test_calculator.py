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
