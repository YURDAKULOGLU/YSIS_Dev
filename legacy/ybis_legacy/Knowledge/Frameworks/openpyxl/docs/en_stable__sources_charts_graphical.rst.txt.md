Advanced Options with Graphical Properties
==========================================
Many advanced options require using the Graphical Properties of OOXML. This
is a much more abstract API than the chart API itself and may require
considerable studying of the OOXML specification to get right. It is often
unavoidable to look at the XML source of some charts you've made. However, as
openpyxl tries very hard to implement the OOXML specification correctly, you
should be able to do most things quite easily. To things easier to read,
openpyxl includes some aliases for some of the more obscure element or
attribute names, eg. `GraphicalProperties for `spPr` or `line` for `line`.
Make the chart background transparent
-------------------------------------
::
from openpyxl.chart.shapes import GraphicalProperties
chart.graphical\_properties = GraphicalProperties()
chart.graphical\_properties.noFill = True
Remove the border from a chart
------------------------------
::
from openpyxl.chart.shapes import GraphicalProperties
chart.graphical\_properties = GraphicalProperties()
chart.graphical\_properties.line.noFill = True
chart.graphical\_properties.line.prstDash = None
Reusing XML
-----------
Due to the high degree of abstraction, DrawingML is used in different office
programs, it can be tedious and frustrating to set the relevant properties
for the desired effect. Fortunately, because openpyxl is very close to the
specification, it is often possible to use XML from source. For example,
adding a single, formatted data label to a series.
::
xml = """


"""
from openpyxl.chart.text import RichText
from openpyxl.xml.functions import fromstring
xml = fromstring(txt)
text\_props = RichText.from\_tree(xml)
# Assuming that this is for the third data series for a chart and we want to add a label below the fourth data point.
highlight = chart.series[2]
highlight.graphicalProperties.line.prstDash = "solid"
highlight.graphicalProperties.ln.solidFill = "0070C0"
highlight.graphicalProperties.line.width = 40000 # make the line thicker than normal
highlight.dLbls = DataLabelList()
highlight = DataLabel(idx=3, showSerName=True, dLblPos="b", txPr=text\_props)
highlight.dLbls.dLbl.append(label)
.. image:: highlighted.png
:alt: "Highlighting a single value on a single series"