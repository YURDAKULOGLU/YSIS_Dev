Additional Worksheet Properties — openpyxl 3.1.3 documentation

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](validation.html "Validating cells") |
* [previous](editing_worksheets.html "Inserting and deleting rows and columns, moving ranges of cells") |
* [openpyxl 3.1.3 documentation](index.html) »
* Additional Worksheet Properties

# Additional Worksheet Properties[](#additional-worksheet-properties "Link to this heading")

These are advanced properties for particular behaviours, the most used ones
are the “fitTopage” page setup property and the tabColor that define the
background color of the worksheet tab.

## Available properties for worksheets[](#available-properties-for-worksheets "Link to this heading")

* “enableFormatConditionsCalculation”
* “filterMode”
* “published”
* “syncHorizontal”
* “syncRef”
* “syncVertical”
* “transitionEvaluation”
* “transitionEntry”
* “tabColor”

## Available fields for page setup properties[](#available-fields-for-page-setup-properties "Link to this heading")

“autoPageBreaks”
“fitToPage”

## Available fields for outlines[](#available-fields-for-outlines "Link to this heading")

* “applyStyles”
* “summaryBelow”
* “summaryRight”
* “showOutlineSymbols”

Search ECMA-376 pageSetup for more details.

Note

By default, outline properties are intitialized so you can directly modify each of their 4 attributes, while page setup properties don’t.
If you want modify the latter, you should first initialize a [`openpyxl.worksheet.properties.PageSetupProperties`](api/openpyxl.worksheet.properties.html#openpyxl.worksheet.properties.PageSetupProperties "openpyxl.worksheet.properties.PageSetupProperties") object with the required parameters.
Once done, they can be directly modified by the routine later if needed.

```
>>> from openpyxl.workbook import Workbook
>>> from openpyxl.worksheet.properties import WorksheetProperties, PageSetupProperties
>>>
>>> wb = Workbook()
>>> ws = wb.active
>>>
>>> wsprops = ws.sheet_properties
>>> wsprops.tabColor = "1072BA"
>>> wsprops.filterMode = False
>>> wsprops.pageSetUpPr = PageSetupProperties(fitToPage=True, autoPageBreaks=False)
>>> wsprops.outlinePr.summaryBelow = False
>>> wsprops.outlinePr.applyStyles = True
>>> wsprops.pageSetUpPr.autoPageBreaks = True
```

## Worksheet Views[](#worksheet-views "Link to this heading")

There are also several convenient properties defined as worksheet views.

You can use [`ws.sheet_view`](api/openpyxl.worksheet.views.html#openpyxl.worksheet.views.SheetView "openpyxl.worksheet.views.SheetView") to set sheet attributes such as zoom, show formulas or if the tab is selected. ws.sheet\_view returns the first view.

```
>>> from openpyxl.workbook import Workbook
>>>
>>> wb = Workbook()
>>> ws = wb.active
>>>
>>> ws.sheet_view.zoomScale = 85 # Sets 85% zoom
>>> ws.sheet_view.showFormulas = True
>>> ws.sheet_view.tabSelected = True
```

Worksheets can have multiple views which are rendered in Excel as “views.xlsx:1”, “views.xlsx:2”.
These correspond to ws.views.sheetView[0] and ws.views.sheetView[1], because they are zero-indexed.

Custom Sheetviews can also be defined.

## Fold (outline)[](#fold-outline "Link to this heading")

```
>>> import openpyxl
>>> wb = openpyxl.Workbook()
>>> ws = wb.create_sheet()
>>> ws.column_dimensions.group('A','D', hidden=True)
>>> ws.row_dimensions.group(1,10, hidden=True)
>>> wb.save('group.xlsx')
```

[![Logo](_static/logo.png)](index.html)

### [Table of Contents](index.html)

* [Additional Worksheet Properties](#)
  + [Available properties for worksheets](#available-properties-for-worksheets)
  + [Available fields for page setup properties](#available-fields-for-page-setup-properties)
  + [Available fields for outlines](#available-fields-for-outlines)
  + [Worksheet Views](#worksheet-views)
  + [Fold (outline)](#fold-outline)

#### Previous topic

[Inserting and deleting rows and columns, moving ranges of cells](editing_worksheets.html "previous chapter")

#### Next topic

[Validating cells](validation.html "next chapter")

### This Page

* [Show Source](_sources/worksheet_properties.rst.txt)

### Quick search

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](validation.html "Validating cells") |
* [previous](editing_worksheets.html "Inserting and deleting rows and columns, moving ranges of cells") |
* [openpyxl 3.1.3 documentation](index.html) »
* Additional Worksheet Properties

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.