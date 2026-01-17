Inserting and deleting rows and columns, moving ranges of cells — openpyxl 3.1.3 documentation

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](worksheet_properties.html "Additional Worksheet Properties") |
* [previous](formatting.html "Conditional Formatting") |
* [openpyxl 3.1.3 documentation](index.html) »
* Inserting and deleting rows and columns, moving ranges of cells

# Inserting and deleting rows and columns, moving ranges of cells[](#inserting-and-deleting-rows-and-columns-moving-ranges-of-cells "Link to this heading")

## Inserting rows and columns[](#inserting-rows-and-columns "Link to this heading")

You can insert rows or columns using the relevant worksheet methods:

> * [`openpyxl.worksheet.worksheet.Worksheet.insert_rows()`](api/openpyxl.worksheet.worksheet.html#openpyxl.worksheet.worksheet.Worksheet.insert_rows "openpyxl.worksheet.worksheet.Worksheet.insert_rows")
> * [`openpyxl.worksheet.worksheet.Worksheet.insert_cols()`](api/openpyxl.worksheet.worksheet.html#openpyxl.worksheet.worksheet.Worksheet.insert_cols "openpyxl.worksheet.worksheet.Worksheet.insert_cols")
> * [`openpyxl.worksheet.worksheet.Worksheet.delete_rows()`](api/openpyxl.worksheet.worksheet.html#openpyxl.worksheet.worksheet.Worksheet.delete_rows "openpyxl.worksheet.worksheet.Worksheet.delete_rows")
> * [`openpyxl.worksheet.worksheet.Worksheet.delete_cols()`](api/openpyxl.worksheet.worksheet.html#openpyxl.worksheet.worksheet.Worksheet.delete_cols "openpyxl.worksheet.worksheet.Worksheet.delete_cols")

The default is one row or column. For example to insert a row at 7 (before
the existing row 7):

```
>>> ws.insert_rows(7)
```

## Deleting rows and columns[](#deleting-rows-and-columns "Link to this heading")

To delete the columns `F:H`:

```
>>> ws.delete_cols(6, 3)
```

Note

Openpyxl does not manage dependencies, such as formulae, tables, charts,
etc., when rows or columns are inserted or deleted. This is considered to
be out of scope for a library that focuses on managing the file format.
As a result, client code **must** implement the functionality required in
any particular use case.

## Moving ranges of cells[](#moving-ranges-of-cells "Link to this heading")

You can also move ranges of cells within a worksheet:

```
>>> ws.move_range("D4:F10", rows=-1, cols=2)
```

This will move the cells in the range `D4:F10` up one row, and right two
columns. The cells will overwrite any existing cells.

If cells contain formulae you can let openpyxl translate these for you, but
as this is not always what you want it is disabled by default. Also only the
formulae in the cells themselves will be translated. References to the cells
from other cells or defined names will not be updated; you can use the
[Parsing Formulas](formula.html) translator to do this:

```
>>> ws.move_range("G4:H10", rows=1, cols=1, translate=True)
```

This will move the relative references in formulae in the range by one row and one column.

## Merge / Unmerge cells[](#merge-unmerge-cells "Link to this heading")

When you merge cells all cells but the top-left one are **removed** from the
worksheet. To carry the border-information of the merged cell, the boundary cells of the
merged cell are created as MergeCells which always have the value None.
See [Styling Merged Cells](styles.html#styling-merged-cells) for information on formatting merged cells.

```
>>> from openpyxl.workbook import Workbook
>>>
>>> wb = Workbook()
>>> ws = wb.active
>>>
>>> ws.merge_cells('A2:D2')
>>> ws.unmerge_cells('A2:D2')
>>>
>>> # or equivalently
>>> ws.merge_cells(start_row=2, start_column=1, end_row=4, end_column=4)
>>> ws.unmerge_cells(start_row=2, start_column=1, end_row=4, end_column=4)
```

[![Logo](_static/logo.png)](index.html)

### [Table of Contents](index.html)

* [Inserting and deleting rows and columns, moving ranges of cells](#)
  + [Inserting rows and columns](#inserting-rows-and-columns)
  + [Deleting rows and columns](#deleting-rows-and-columns)
  + [Moving ranges of cells](#moving-ranges-of-cells)
  + [Merge / Unmerge cells](#merge-unmerge-cells)

#### Previous topic

[Conditional Formatting](formatting.html "previous chapter")

#### Next topic

[Additional Worksheet Properties](worksheet_properties.html "next chapter")

### This Page

* [Show Source](_sources/editing_worksheets.rst.txt)

### Quick search

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](worksheet_properties.html "Additional Worksheet Properties") |
* [previous](formatting.html "Conditional Formatting") |
* [openpyxl 3.1.3 documentation](index.html) »
* Inserting and deleting rows and columns, moving ranges of cells

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.