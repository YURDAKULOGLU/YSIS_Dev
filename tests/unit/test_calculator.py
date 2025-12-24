import pytest

from src.utils.calculator import Calculator

ADDITION_RESULT_NORMAL = 3

def test_add_normal():
    calc = Calculator()
    assert calc.add(1, 2) == ADDITION_RESULT_NORMAL

def test_add_zero():
    calc = Calculator()
    assert calc.add(0, 0) == 0

ADDITION_RESULT_NEGATIVE = -2

def test_add_negative():
    calc = Calculator()
    assert calc.add(-1, -1) == ADDITION_RESULT_NEGATIVE

def test_add_type_validation():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.add("a", "b")

def test_subtract_normal():
    calc = Calculator()
    assert calc.subtract(3, 2) == 1

def test_subtract_zero():
    calc = Calculator()
    assert calc.subtract(0, 0) == 0

def test_subtract_negative():
    calc = Calculator()
    assert calc.subtract(-1, -1) == 0

def test_subtract_type_validation():
    calc = Calculator()
    with pytest.raises(TypeError):
        calc.subtract("a", "b")
