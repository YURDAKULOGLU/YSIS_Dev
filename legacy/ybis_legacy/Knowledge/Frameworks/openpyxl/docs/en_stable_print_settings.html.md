Print Settings — openpyxl 3.1.3 documentation

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](pivot.html "Pivot Tables") |
* [previous](filters.html "Using filters and sorts") |
* [openpyxl 3.1.3 documentation](index.html) »
* Print Settings

# Print Settings[](#print-settings "Link to this heading")

openpyxl provides reasonably full support for print settings.

## Edit Print Options[](#edit-print-options "Link to this heading")

```
>>> from openpyxl.workbook import Workbook
>>>
>>> wb = Workbook()
>>> ws = wb.active
>>>
>>> ws.print_options.horizontalCentered = True
>>> ws.print_options.verticalCentered = True
```

## Headers and Footers[](#headers-and-footers "Link to this heading")

Headers and footers use their own formatting language. This is fully
supported when writing them but, due to the complexity and the possibility of
nesting, only partially when reading them. There is support for the font,
size and color for a left, centre/center, or right element. Granular control
(highlighting individuals words) will require applying control codes
manually.

```
>>> from openpyxl.workbook import Workbook
>>>
>>> wb = Workbook()
>>> ws = wb.active
>>>
>>> ws.oddHeader.left.text = "Page &[Page] of &N"
>>> ws.oddHeader.left.size = 14
>>> ws.oddHeader.left.font = "Tahoma,Bold"
>>> ws.oddHeader.left.color = "CC3366"
```

Also supported are evenHeader and evenFooter as well as firstHeader and firstFooter.

## Add Print Titles[](#add-print-titles "Link to this heading")

You can print titles on every page to ensure that the data is properly
labelled.

```
>>> from openpyxl.workbook import Workbook
>>>
>>> wb = Workbook()
>>> ws = wb.active
>>>
>>> ws.print_title_cols = 'A:B' # the first two cols
>>> ws.print_title_rows = '1:1' # the first row
```

## Add a Print Area[](#add-a-print-area "Link to this heading")

You can select a part of a worksheet as the only part that you want to print

```
>>> from openpyxl.workbook import Workbook
>>>
>>> wb = Workbook()
>>> ws = wb.active
>>>
>>> ws.print_area = 'A1:F10'
```

## Change page layout and size[](#change-page-layout-and-size "Link to this heading")

You can adjust the size and print orientation per sheet of a workbook.

```
>>>
>>> wb = Workbook()
>>> ws = wb.active
>>>
>>> ws.page_setup.orientation = ws.ORIENTATION_LANDSCAPE
>>> ws.page_setup.paperSize = ws.PAPERSIZE_A5
```

The table size is stored internally as an integer, a number of alias variables are
also available for common sizes (refer to PAPERSIZE\_\* in [`openpyxl.worksheet.worksheet`](api/openpyxl.worksheet.worksheet.html#module-openpyxl.worksheet.worksheet "openpyxl.worksheet.worksheet") ).
If you need a non-standard size, a full list can be found by searching ECMA-376 pageSetup
and setting that value as the paperSize

[![Logo](_static/logo.png)](index.html)

### [Table of Contents](index.html)

* [Print Settings](#)
  + [Edit Print Options](#edit-print-options)
  + [Headers and Footers](#headers-and-footers)
  + [Add Print Titles](#add-print-titles)
  + [Add a Print Area](#add-a-print-area)
  + [Change page layout and size](#change-page-layout-and-size)

#### Previous topic

[Using filters and sorts](filters.html "previous chapter")

#### Next topic

[Pivot Tables](pivot.html "next chapter")

### This Page

* [Show Source](_sources/print_settings.rst.txt)

### Quick search

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](pivot.html "Pivot Tables") |
* [previous](filters.html "Using filters and sorts") |
* [openpyxl 3.1.3 documentation](index.html) »
* Print Settings

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.