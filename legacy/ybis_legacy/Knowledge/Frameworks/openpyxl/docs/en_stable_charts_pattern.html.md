Adding Patterns — openpyxl 3.1.3 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](gauge.html "Gauge Charts") |
* [previous](chart_layout.html "Changing the layout of plot area and legend") |
* [openpyxl 3.1.3 documentation](../index.html) »
* [Charts](introduction.html) »
* Adding Patterns

# Adding Patterns[](#adding-patterns "Link to this heading")

Whole data series and individual data points can be extensively styled through the graphicalProperties. Getting things just right may take some time.

```
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.marker import DataPoint

from openpyxl.drawing.fill import PatternFillProperties, ColorChoice

wb = Workbook()
ws = wb.active

rows = [
    ("Sample",),
    (1,),
    (2,),
    (3,),
    (2,),
    (3,),
    (3,),
    (1,),
    (2,),
]

for r in rows:
    ws.append(r)


c = BarChart()
data = Reference(ws, min_col=1, min_row=1, max_row=8)
c.add_data(data, titles_from_data=True)
c.title = "Chart with patterns"

# set a pattern for the whole series
series = c.series[0]
fill =  PatternFillProperties(prst="pct5")
fill.foreground = ColorChoice(prstClr="red")
fill.background = ColorChoice(prstClr="blue")
series.graphicalProperties.pattFill = fill

# set a pattern for a 6th data point (0-indexed)
pt = DataPoint(idx=5)
pt.graphicalProperties.pattFill = PatternFillProperties(prst="ltHorz")
series.dPt.append(pt)

ws.add_chart(c, "C1")

wb.save("pattern.xlsx")
```

!["Sample bar chart with patterned columns"](../_images/pattern.png)

[![Logo](../_static/logo.png)](../index.html)

#### Previous topic

[Changing the layout of plot area and legend](chart_layout.html "previous chapter")

#### Next topic

[Gauge Charts](gauge.html "next chapter")

### This Page

* [Show Source](../_sources/charts/pattern.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](gauge.html "Gauge Charts") |
* [previous](chart_layout.html "Changing the layout of plot area and legend") |
* [openpyxl 3.1.3 documentation](../index.html) »
* [Charts](introduction.html) »
* Adding Patterns

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.