Chartsheets — openpyxl 3.1.3 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](anchors.html "Positioning Charts with Anchors") |
* [previous](gauge.html "Gauge Charts") |
* [openpyxl 3.1.3 documentation](../index.html) »
* [Charts](introduction.html) »
* Chartsheets

# Chartsheets[](#chartsheets "Link to this heading")

Chartsheets are special worksheets which only contain charts. All the data
for the chart must be on a different worksheet.

```
from openpyxl import Workbook

from openpyxl.chart import PieChart, Reference, Series

wb = Workbook()
ws = wb.active
cs = wb.create_chartsheet()

rows = [
    ["Bob", 3],
    ["Harry", 2],
    ["James", 4],
]

for row in rows:
    ws.append(row)


chart = PieChart()
labels = Reference(ws, min_col=1, min_row=1, max_row=3)
data = Reference(ws, min_col=2, min_row=1, max_row=3)
chart.series = (Series(data),)
chart.title = "PieChart"

cs.add_chart(chart)

wb.save("demo.xlsx")
```

!["Sample chartsheet"](../_images/chartsheet.png)

By default in Microsoft Excel, charts are chartsheets are designed to fit the
page format of the active printer. By default in openpyxl, charts are designed
to fit window in which they’re displayed. You can flip between these using
the zoomToFit attribute of the active view, typically
cs.sheetViews.sheetView[0].zoomToFit

[![Logo](../_static/logo.png)](../index.html)

#### Previous topic

[Gauge Charts](gauge.html "previous chapter")

#### Next topic

[Positioning Charts with Anchors](anchors.html "next chapter")

### This Page

* [Show Source](../_sources/charts/chartsheet.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](anchors.html "Positioning Charts with Anchors") |
* [previous](gauge.html "Gauge Charts") |
* [openpyxl 3.1.3 documentation](../index.html) »
* [Charts](introduction.html) »
* Chartsheets

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.