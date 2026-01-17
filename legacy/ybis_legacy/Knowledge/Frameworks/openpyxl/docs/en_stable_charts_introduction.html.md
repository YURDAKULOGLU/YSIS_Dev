Charts — openpyxl 3.1.3 documentation

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](area.html "Area Charts") |
* [previous](../protection.html "Protection") |
* [openpyxl 3.1.3 documentation](../index.html) »
* Charts

# Charts[](#charts "Link to this heading")

## Chart types[](#chart-types "Link to this heading")

The following charts are available:

* [Area Charts](area.html)
  + [2D Area Charts](area.html#d-area-charts)
  + [3D Area Charts](area.html#id1)
* [Bar and Column Charts](bar.html)
  + [Vertical, Horizontal and Stacked Bar Charts](bar.html#vertical-horizontal-and-stacked-bar-charts)
  + [3D Bar Charts](bar.html#d-bar-charts)
* [Bubble Charts](bubble.html)
* [Line Charts](line.html)
  + [Line Charts](line.html#id1)
  + [3D Line Charts](line.html#d-line-charts)
* [Scatter Charts](scatter.html)
* [Pie Charts](pie.html)
  + [Pie Charts](pie.html#id1)
  + [Projected Pie Charts](pie.html#projected-pie-charts)
  + [3D Pie Charts](pie.html#d-pie-charts)
  + [Gradient Pie Charts](pie.html#gradient-pie-charts)
* [Doughnut Charts](doughnut.html)
* [Radar Charts](radar.html)
* [Stock Charts](stock.html)
* [Surface charts](surface.html)

## Creating a chart[](#creating-a-chart "Link to this heading")

Charts are composed of at least one series of one or more data points. Series
themselves are comprised of references to cell ranges.

```
>>> from openpyxl import Workbook
>>> wb = Workbook()
>>> ws = wb.active
>>> for i in range(10):
...     ws.append([i])
>>>
>>> from openpyxl.chart import BarChart, Reference, Series
>>> values = Reference(ws, min_col=1, min_row=1, max_col=1, max_row=10)
>>> chart = BarChart()
>>> chart.add_data(values)
>>> ws.add_chart(chart, "E15")
>>> wb.save("SampleChart.xlsx")
```

By default the top-left corner of a chart is anchored to cell E15 and the
size is 15 x 7.5 cm (approximately 5 columns by 14 rows). This can be changed
by setting the anchor, width and height properties of the chart. The
actual size will depend on operating system and device. Other anchors are
possible; see [`openpyxl.drawing.spreadsheet_drawing`](../api/openpyxl.drawing.spreadsheet_drawing.html#module-openpyxl.drawing.spreadsheet_drawing "openpyxl.drawing.spreadsheet_drawing") for further information.

## Working with axes[](#working-with-axes "Link to this heading")

* [Axis Limits and Scale](limits_and_scaling.html)
  + [Minima and Maxima](limits_and_scaling.html#minima-and-maxima)
  + [Logarithmic Scaling](limits_and_scaling.html#logarithmic-scaling)
  + [Axis Orientation](limits_and_scaling.html#axis-orientation)
* [Adding a second axis](secondary.html)

## Change the chart layout[](#change-the-chart-layout "Link to this heading")

* [Changing the layout of plot area and legend](chart_layout.html)
  + [Chart layout](chart_layout.html#chart-layout)
    - [Size and position](chart_layout.html#size-and-position)
    - [Mode](chart_layout.html#mode)
    - [Target](chart_layout.html#target)
  + [Legend layout](chart_layout.html#legend-layout)

## Styling charts[](#styling-charts "Link to this heading")

* [Adding Patterns](pattern.html)

## Advanced charts[](#advanced-charts "Link to this heading")

Charts can be combined to create new charts:

* [Gauge Charts](gauge.html)

## Using chartsheets[](#using-chartsheets "Link to this heading")

Charts can be added to special worksheets called chartsheets:

* [Chartsheets](chartsheet.html)

## Positioning charts[](#positioning-charts "Link to this heading")

Position charts using anchors:

* [Positioning Charts with Anchors](anchors.html)

## Advanced chart formatting[](#advanced-chart-formatting "Link to this heading")

Use graphical properties for advanced chart formatting:

* [Advanced Options with Graphical Properties](graphical.html)
  + [Make the chart background transparent](graphical.html#make-the-chart-background-transparent)
  + [Remove the border from a chart](graphical.html#remove-the-border-from-a-chart)
  + [Reusing XML](graphical.html#reusing-xml)

[![Logo](../_static/logo.png)](../index.html)

### [Table of Contents](../index.html)

* [Charts](#)
  + [Chart types](#chart-types)
  + [Creating a chart](#creating-a-chart)
  + [Working with axes](#working-with-axes)
  + [Change the chart layout](#change-the-chart-layout)
  + [Styling charts](#styling-charts)
  + [Advanced charts](#advanced-charts)
  + [Using chartsheets](#using-chartsheets)
  + [Positioning charts](#positioning-charts)
  + [Advanced chart formatting](#advanced-chart-formatting)

#### Previous topic

[Protection](../protection.html "previous chapter")

#### Next topic

[Area Charts](area.html "next chapter")

### This Page

* [Show Source](../_sources/charts/introduction.rst.txt)

### Quick search

### Navigation

* [index](../genindex.html "General Index")
* [modules](../py-modindex.html "Python Module Index") |
* [next](area.html "Area Charts") |
* [previous](../protection.html "Protection") |
* [openpyxl 3.1.3 documentation](../index.html) »
* Charts

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.