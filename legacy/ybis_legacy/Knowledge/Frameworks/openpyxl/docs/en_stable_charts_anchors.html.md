Positioning Charts with Anchors — openpyxl 3.1.3 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](graphical.html "Advanced Options with Graphical Properties") |
* [previous](chartsheet.html "Chartsheets") |
* [openpyxl 3.1.3 documentation](../index.html) »
* [Charts](introduction.html) »
* Positioning Charts with Anchors

# Positioning Charts with Anchors[](#positioning-charts-with-anchors "Link to this heading")

You can position charts using one of three different kinds of anchor:

> * OneCell – where the top-left of a chart is anchored to a single cell. This is the default for openpyxl and corresponds to the layout option “Move but don’t size with cells”.
> * TwoCell – where the top-left of a chart is anchored to one cell, and the bottom-right to another cell. This corresponds to the layout option “Move and size with cells”.
> * Absolute – where the chart is placed relative to the worksheet’s top-left corner and not any particular cell.

You can change anchors quite easily on a chart like this. Let’s assume we
have created a bar chart using the sample code:

```
from openpyxl import Workbook
from openpyxl.chart import BarChart, Series, Reference

wb = Workbook(write_only=True)
ws = wb.create_sheet()

rows = [
    ('Number', 'Batch 1', 'Batch 2'),
    (2, 10, 30),
    (3, 40, 60),
    (4, 50, 70),
    (5, 20, 10),
    (6, 10, 40),
    (7, 50, 30),
]


for row in rows:
    ws.append(row)


chart1 = BarChart()
chart1.type = "col"
chart1.style = 10
chart1.title = "Bar Chart"
chart1.y_axis.title = 'Test number'
chart1.x_axis.title = 'Sample length (mm)'

data = Reference(ws, min_col=2, min_row=1, max_row=7, max_col=3)
cats = Reference(ws, min_col=1, min_row=2, max_row=7)
chart1.add_data(data, titles_from_data=True)
chart1.set_categories(cats)
chart1.shape = 4
ws.add_chart(chart1, "A10")

from copy import deepcopy

chart2 = deepcopy(chart1)
chart2.style = 11
chart2.type = "bar"
chart2.title = "Horizontal Bar Chart"

ws.add_chart(chart2, "G10")


chart3 = deepcopy(chart1)
chart3.type = "col"
chart3.style = 12
chart3.grouping = "stacked"
chart3.overlap = 100
chart3.title = 'Stacked Chart'

ws.add_chart(chart3, "A27")


chart4 = deepcopy(chart1)
chart4.type = "bar"
chart4.style = 13
chart4.grouping = "percentStacked"
chart4.overlap = 100
chart4.title = 'Percent Stacked Chart'

ws.add_chart(chart4, "G27")

wb.save("bar.xlsx")
```

Let’s take the first chart. Instead of anchoring it to A10, we want it to
keep it with our table of data, say A9 to C20. We can do this by creating a
TwoCellAnchor for those two cells.:

```
from openpyxl.drawing.spreadsheet_drawing import TwoCellAnchor

anchor = TwoCellAnchor()
anchor._from.col = 0 #A
anchor._from.row = 8 # row 9, using 0-based indexing
anchor.to.col = 2 #C
anchor.to.row = 19 # row 20

chart.anchor = anchor
```

You can also use this to change the anchors of existing charts.

[![Logo](../_static/logo.png)](../index.html)

#### Previous topic

[Chartsheets](chartsheet.html "previous chapter")

#### Next topic

[Advanced Options with Graphical Properties](graphical.html "next chapter")

### This Page

* [Show Source](../_sources/charts/anchors.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](graphical.html "Advanced Options with Graphical Properties") |
* [previous](chartsheet.html "Chartsheets") |
* [openpyxl 3.1.3 documentation](../index.html) »
* [Charts](introduction.html) »
* Positioning Charts with Anchors

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.