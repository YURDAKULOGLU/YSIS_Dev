Validating cells — openpyxl 3.1.3 documentation

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](worksheet_tables.html "Worksheet Tables") |
* [previous](worksheet_properties.html "Additional Worksheet Properties") |
* [openpyxl 3.1.3 documentation](index.html) »
* Validating cells

# Validating cells[](#validating-cells "Link to this heading")

Data validators can be applied to ranges of cells but are not enforced or evaluated. Ranges do not have to be contiguous: eg. “A1 B2:B5” is contains A1 and the cells B2 to B5 but not A2 or B2.

## Examples[](#examples "Link to this heading")

```
>>> from openpyxl import Workbook
>>> from openpyxl.worksheet.datavalidation import DataValidation
>>>
>>> # Create the workbook and worksheet we'll be working with
>>> wb = Workbook()
>>> ws = wb.active
>>>
>>> # Create a data-validation object with list validation
>>> dv = DataValidation(type="list", formula1='"Dog,Cat,Bat"', allow_blank=True)
>>>
>>> # Optionally set a custom error message
>>> dv.error ='Your entry is not in the list'
>>> dv.errorTitle = 'Invalid Entry'
>>>
>>> # Optionally set a custom prompt message
>>> dv.prompt = 'Please select from the list'
>>> dv.promptTitle = 'List Selection'
>>>
>>> # Add the data-validation object to the worksheet
>>> ws.add_data_validation(dv)
```

```
>>> # Create some cells, and add them to the data-validation object
>>> c1 = ws["A1"]
>>> c1.value = "Dog"
>>> dv.add(c1)
>>> c2 = ws["A2"]
>>> c2.value = "An invalid value"
>>> dv.add(c2)
>>>
>>> # Or, apply the validation to a range of cells
>>> dv.add('B1:B1048576') # This is the same as for the whole of column B
>>>
>>> # Check with a cell is in the validator
>>> "B4" in dv
True
```

Note

Validations without any cell ranges will be ignored when saving a workbook.

Note

Excel and LibreOffice interpret the parameter showDropDown=True as the dropdown arrow should be hidden.

## Other validation examples[](#other-validation-examples "Link to this heading")

Any whole number:

```
dv = DataValidation(type="whole")
```

Any whole number above 100:

```
dv = DataValidation(type="whole",
                    operator="greaterThan",
                    formula1=100)
```

Any decimal number:

```
dv = DataValidation(type="decimal")
```

Any decimal number between 0 and 1:

```
dv = DataValidation(type="decimal",
                    operator="between",
                    formula1=0,
                    formula2=1)
```

Any date:

```
dv = DataValidation(type="date")
```

or time:

```
dv = DataValidation(type="time")
```

Any string at most 15 characters:

```
dv = DataValidation(type="textLength",
                    operator="lessThanOrEqual"),
                    formula1=15)
```

Cell range validation:

```
from openpyxl.utils import quote_sheetname
dv = DataValidation(type="list",
                    formula1="{0}!$B$1:$B$10".format(quote_sheetname(sheetname))
                    )
```

Custom rule:

```
dv = DataValidation(type="custom",
                    formula1"=SOMEFORMULA")
```

Note

See <http://www.contextures.com/xlDataVal07.html> for custom rules

[![Logo](_static/logo.png)](index.html)

### [Table of Contents](index.html)

* [Validating cells](#)
  + [Examples](#examples)
  + [Other validation examples](#other-validation-examples)

#### Previous topic

[Additional Worksheet Properties](worksheet_properties.html "previous chapter")

#### Next topic

[Worksheet Tables](worksheet_tables.html "next chapter")

### This Page

* [Show Source](_sources/validation.rst.txt)

### Quick search

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](worksheet_tables.html "Worksheet Tables") |
* [previous](worksheet_properties.html "Additional Worksheet Properties") |
* [openpyxl 3.1.3 documentation](index.html) »
* Validating cells

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.