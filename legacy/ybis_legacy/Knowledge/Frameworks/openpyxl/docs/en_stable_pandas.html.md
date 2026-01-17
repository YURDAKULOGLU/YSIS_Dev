Working with Pandas and NumPy — openpyxl 3.1.3 documentation

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](optimized.html "Optimised Modes") |
* [previous](images.html "Working with Images") |
* [openpyxl 3.1.3 documentation](index.html) »
* Working with Pandas and NumPy

# Working with Pandas and NumPy[](#working-with-pandas-and-numpy "Link to this heading")

openpyxl is able to work with the popular libraries [Pandas](http://pandas.pydata.org) and [NumPy](http://numpy.org)

## NumPy Support[](#numpy-support "Link to this heading")

openpyxl has builtin support for the NumPy types float, integer and boolean.
DateTimes are supported using the Pandas’ Timestamp type.

## Working with Pandas Dataframes[](#working-with-pandas-dataframes "Link to this heading")

The [`openpyxl.utils.dataframe.dataframe_to_rows()`](api/openpyxl.utils.dataframe.html#openpyxl.utils.dataframe.dataframe_to_rows "openpyxl.utils.dataframe.dataframe_to_rows") function provides a
simple way to work with Pandas Dataframes:

```
from openpyxl.utils.dataframe import dataframe_to_rows
wb = Workbook()
ws = wb.active

for r in dataframe_to_rows(df, index=True, header=True):
    ws.append(r)
```

While Pandas itself supports conversion to Excel, this gives client code
additional flexibility including the ability to stream dataframes straight to
files.

To convert a dataframe into a worksheet highlighting the header and index:

```
wb = Workbook()
ws = wb.active

for r in dataframe_to_rows(df, index=True, header=True):
    ws.append(r)

for cell in ws['A'] + ws[1]:
    cell.style = 'Pandas'

wb.save("pandas_openpyxl.xlsx")
```

Alternatively, if you just want to convert the data you can use write-only mode:

```
from openpyxl.cell.cell import WriteOnlyCell
wb = Workbook(write_only=True)
ws = wb.create_sheet()

cell = WriteOnlyCell(ws)
cell.style = 'Pandas'

 def format_first_row(row, cell):

    for c in row:
        cell.value = c
        yield cell

rows = dataframe_to_rows(df)
first_row = format_first_row(next(rows), cell)
ws.append(first_row)

for row in rows:
    row = list(row)
    cell.value = row[0]
    row[0] = cell
    ws.append(row)

wb.save("openpyxl_stream.xlsx")
```

This code will work just as well with a standard workbook.

## Converting a worksheet to a Dataframe[](#converting-a-worksheet-to-a-dataframe "Link to this heading")

To convert a worksheet to a Dataframe you can use the values property. This
is very easy if the worksheet has no headers or indices:

```
df = DataFrame(ws.values)
```

If the worksheet does have headers or indices, such as one created by Pandas,
then a little more work is required:

```
from itertools import islice
data = ws.values
cols = next(data)[1:]
data = list(data)
idx = [r[0] for r in data]
data = (islice(r, 1, None) for r in data)
df = DataFrame(data, index=idx, columns=cols)
```

[![Logo](_static/logo.png)](index.html)

### [Table of Contents](index.html)

* [Working with Pandas and NumPy](#)
  + [NumPy Support](#numpy-support)
  + [Working with Pandas Dataframes](#working-with-pandas-dataframes)
  + [Converting a worksheet to a Dataframe](#converting-a-worksheet-to-a-dataframe)

#### Previous topic

[Working with Images](images.html "previous chapter")

#### Next topic

[Optimised Modes](optimized.html "next chapter")

### This Page

* [Show Source](_sources/pandas.rst.txt)

### Quick search

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](optimized.html "Optimised Modes") |
* [previous](images.html "Working with Images") |
* [openpyxl 3.1.3 documentation](index.html) »
* Working with Pandas and NumPy

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.