# Task Execution Report: TEST-001

## Status: SUCCESS

## Files Modified:
- C:\Projeler\YBIS_Dev\tests\unit\test_calculator.py

## Plan Executed:
- Install pytest if not already installed.
- Create a new file named test_calculator.py inside the tests/unit directory.
- Write test cases for the add() function covering normal, edge (zero, negative), and type validation scenarios.
- Write test cases for the subtract() function covering normal, edge (zero, negative), and type validation scenarios.
- Run pytest to ensure all tests pass without errors.

## Error History:
- LINTING FEEDBACK:
PLR2004 Magic value used in comparison, consider replacing `3` with a constant variable
  --> tests\unit\test_calculator.py:8:30
   |
 6 | def test_add_normal():
 7 |     calc = Calculator()
 8 |     assert calc.add(1, 2) == 3
   |                              ^
 9 |
10 | def test_add_zero():
   |

PLR2004 Magic value used in comparison, consider replacing `-2` with a constant variable
  --> tests\unit\test_calculator.py:16:32
   |
14 | def test_add_negative():
15 |     calc = Calculator()
16 |     assert calc.add(-1, -1) == -2
   |                                ^^
17 |
18 | def test_add_type_validation():
   |

Found 2 errors.
