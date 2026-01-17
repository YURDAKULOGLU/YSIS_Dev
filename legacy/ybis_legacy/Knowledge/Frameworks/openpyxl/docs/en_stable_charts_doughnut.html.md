Doughnut Charts — openpyxl 3.1.3 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](radar.html "Radar Charts") |
* [previous](pie.html "Pie Charts") |
* [openpyxl 3.1.3 documentation](../index.html) »
* [Charts](introduction.html) »
* Doughnut Charts

# Doughnut Charts[](#doughnut-charts "Link to this heading")

Doughnut charts are similar to pie charts except that they use a ring instead
of a circle. They can also plot several series of data as concentric rings.

```
from openpyxl import Workbook

from openpyxl.chart import (
    DoughnutChart,
    Reference,
    Series,
)
from openpyxl.chart.series import DataPoint

data = [
    ['Pie', 2014, 2015],
    ['Plain', 40, 50],
    ['Jam', 2, 10],
    ['Lime', 20, 30],
    ['Chocolate', 30, 40],
]

wb = Workbook()
ws = wb.active

for row in data:
    ws.append(row)

chart = DoughnutChart()
labels = Reference(ws, min_col=1, min_row=2, max_row=5)
data = Reference(ws, min_col=2, min_row=1, max_row=5)
chart.add_data(data, titles_from_data=True)
chart.set_categories(labels)
chart.title = "Doughnuts sold by category"
chart.style = 26

# Cut the first slice out of the doughnut
slices = [DataPoint(idx=i) for i in range(4)]
plain, jam, lime, chocolate = slices
chart.series[0].data_points = slices
plain.graphicalProperties.solidFill = "FAE1D0"
jam.graphicalProperties.solidFill = "BB2244"
lime.graphicalProperties.solidFill = "22DD22"
chocolate.graphicalProperties.solidFill = "61210B"
chocolate.explosion = 10

ws.add_chart(chart, "E1")

from copy import deepcopy

chart2 = deepcopy(chart)
chart2.title = None
data = Reference(ws, min_col=3, min_row=1, max_row=5)
series2 = Series(data, title_from_data=True)
series2.data_points = slices
chart2.series.append(series2)

ws.add_chart(chart2, "E17")

wb.save("doughnut.xlsx")
```

!["Sample doughnut charts"](../_images/doughnut.png)

[![Logo](../_static/logo.png)](../index.html)

#### Previous topic

[Pie Charts](pie.html "previous chapter")

#### Next topic

[Radar Charts](radar.html "next chapter")

### This Page

* [Show Source](../_sources/charts/doughnut.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](radar.html "Radar Charts") |
* [previous](pie.html "Pie Charts") |
* [openpyxl 3.1.3 documentation](../index.html) »
* [Charts](introduction.html) »
* Doughnut Charts

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.