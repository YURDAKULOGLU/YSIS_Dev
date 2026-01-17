Optimised Modes — openpyxl 3.1.3 documentation

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](performance.html "Performance") |
* [previous](pandas.html "Working with Pandas and NumPy") |
* [openpyxl 3.1.3 documentation](index.html) »
* Optimised Modes

# Optimised Modes[](#optimised-modes "Link to this heading")

## Read-only mode[](#read-only-mode "Link to this heading")

Sometimes, you will need to open or write extremely large XLSX files,
and the common routines in openpyxl won’t be able to handle that load.
Fortunately, there are two modes that enable you to read and write unlimited
amounts of data with (near) constant memory consumption.

Introducing `openpyxl.worksheet._read_only.ReadOnlyWorksheet`:

```
from openpyxl import load_workbook
wb = load_workbook(filename='large_file.xlsx', read_only=True)
ws = wb['big_data']

for row in ws.rows:
    for cell in row:
        print(cell.value)

# Close the workbook after reading
wb.close()
```

Warning

* `openpyxl.worksheet._read_only.ReadOnlyWorksheet` is read-only
* Unlike a normal workbook, a read-only workbook will use lazy loading.
  The workbook must be explicitly closed with the `close()` method.

Cells returned are not regular [`openpyxl.cell.cell.Cell`](api/openpyxl.cell.cell.html#openpyxl.cell.cell.Cell "openpyxl.cell.cell.Cell") but
`openpyxl.cell._read_only.ReadOnlyCell`.

### Worksheet dimensions[](#worksheet-dimensions "Link to this heading")

Read-only mode relies on applications and libraries that created the file
providing correct information about the worksheets, specifically the used
part of it, known as the dimensions. Some applications set this incorrectly.
You can check the apparent dimensions of a worksheet using
ws.calculate\_dimension(). If this returns a range that you know is
incorrect, say A1:A1 then simply resetting the max\_row and max\_column
attributes should allow you to work with the file:

```
ws.reset_dimensions()
```

## Write-only mode[](#write-only-mode "Link to this heading")

Here again, the regular [`openpyxl.worksheet.worksheet.Worksheet`](api/openpyxl.worksheet.worksheet.html#openpyxl.worksheet.worksheet.Worksheet "openpyxl.worksheet.worksheet.Worksheet") has been replaced
by a faster alternative, the `openpyxl.worksheet._write_only.WriteOnlyWorksheet`.
When you want to dump large amounts of data make sure you have lxml installed.

```
>>> from openpyxl import Workbook
>>> wb = Workbook(write_only=True)
>>> ws = wb.create_sheet()
>>>
>>> # now we'll fill it with 100 rows x 200 columns
>>>
>>> for irow in range(100):
...     ws.append(['%d' % i for i in range(200)])
>>> # save the file
>>> wb.save('new_big_file.xlsx')
```

If you want to have cells with styles or comments then use a `openpyxl.cell.WriteOnlyCell()`

```
>>> from openpyxl import Workbook
>>> wb = Workbook(write_only = True)
>>> ws = wb.create_sheet()
>>> from openpyxl.cell import WriteOnlyCell
>>> from openpyxl.comments import Comment
>>> from openpyxl.styles import Font
>>> cell = WriteOnlyCell(ws, value="hello world")
>>> cell.font = Font(name='Courier', size=36)
>>> cell.comment = Comment(text="A comment", author="Author's Name")
>>> ws.append([cell, 3.14, None])
>>> wb.save('write_only_file.xlsx')
```

This will create a write-only workbook with a single sheet, and append
a row of 3 cells: one text cell with a custom font and a comment, a
floating-point number, and an empty cell (which will be discarded
anyway).

Warning

* Unlike a normal workbook, a newly-created write-only workbook
  does not contain any worksheets; a worksheet must be specifically
  created with the `create_sheet()` method.
* In a write-only workbook, rows can only be added with
  `append()`. It is not possible to write (or read) cells at
  arbitrary locations with `cell()` or `iter_rows()`.
* It is able to export unlimited amount of data (even more than Excel can
  handle actually), while keeping memory usage under 10Mb.
* A write-only workbook can only be saved once. After
  that, every attempt to save the workbook or append() to an existing
  worksheet will raise an [`openpyxl.utils.exceptions.WorkbookAlreadySaved`](api/openpyxl.utils.exceptions.html#openpyxl.utils.exceptions.WorkbookAlreadySaved "openpyxl.utils.exceptions.WorkbookAlreadySaved")
  exception.
* Everything that appears in the file before the actual cell data must be created
  before cells are added because it must written to the file before then.
  For example, freeze\_panes should be set before cells are added.

[![Logo](_static/logo.png)](index.html)

### [Table of Contents](index.html)

* [Optimised Modes](#)
  + [Read-only mode](#read-only-mode)
    - [Worksheet dimensions](#worksheet-dimensions)
  + [Write-only mode](#write-only-mode)

#### Previous topic

[Working with Pandas and NumPy](pandas.html "previous chapter")

#### Next topic

[Performance](performance.html "next chapter")

### This Page

* [Show Source](_sources/optimized.rst.txt)

### Quick search

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](performance.html "Performance") |
* [previous](pandas.html "Working with Pandas and NumPy") |
* [openpyxl 3.1.3 documentation](index.html) »
* Optimised Modes

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.