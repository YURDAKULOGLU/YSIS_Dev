Optimised Modes
===============
Read-only mode
--------------
Sometimes, you will need to open or write extremely large XLSX files,
and the common routines in openpyxl won't be able to handle that load.
Fortunately, there are two modes that enable you to read and write unlimited
amounts of data with (near) constant memory consumption.
Introducing :class:`openpyxl.worksheet.\_read\_only.ReadOnlyWorksheet`::
from openpyxl import load\_workbook
wb = load\_workbook(filename='large\_file.xlsx', read\_only=True)
ws = wb['big\_data']
for row in ws.rows:
for cell in row:
print(cell.value)
# Close the workbook after reading
wb.close()
.. warning::
\* :class:`openpyxl.worksheet.\_read\_only.ReadOnlyWorksheet` is read-only
\* Unlike a normal workbook, a read-only workbook will use lazy loading.
The workbook must be explicitly closed with the :func:`close()` method.
Cells returned are not regular :class:`openpyxl.cell.cell.Cell` but
:class:`openpyxl.cell.\_read\_only.ReadOnlyCell`.
Worksheet dimensions
++++++++++++++++++++
Read-only mode relies on applications and libraries that created the file
providing correct information about the worksheets, specifically the used
part of it, known as the dimensions. Some applications set this incorrectly.
You can check the apparent dimensions of a worksheet using
`ws.calculate\_dimension()`. If this returns a range that you know is
incorrect, say `A1:A1` then simply resetting the max\_row and max\_column
attributes should allow you to work with the file::
ws.reset\_dimensions()
Write-only mode
---------------
Here again, the regular :class:`openpyxl.worksheet.worksheet.Worksheet` has been replaced
by a faster alternative, the :class:`openpyxl.worksheet.\_write\_only.WriteOnlyWorksheet`.
When you want to dump large amounts of data make sure you have `lxml` installed.
.. :: doctest
>>> from openpyxl import Workbook
>>> wb = Workbook(write\_only=True)
>>> ws = wb.create\_sheet()
>>>
>>> # now we'll fill it with 100 rows x 200 columns
>>>
>>> for irow in range(100):
... ws.append(['%d' % i for i in range(200)])
>>> # save the file
>>> wb.save('new\_big\_file.xlsx') # doctest: +SKIP
If you want to have cells with styles or comments then use a :func:`openpyxl.cell.WriteOnlyCell`
.. :: doctest
>>> from openpyxl import Workbook
>>> wb = Workbook(write\_only = True)
>>> ws = wb.create\_sheet()
>>> from openpyxl.cell import WriteOnlyCell
>>> from openpyxl.comments import Comment
>>> from openpyxl.styles import Font
>>> cell = WriteOnlyCell(ws, value="hello world")
>>> cell.font = Font(name='Courier', size=36)
>>> cell.comment = Comment(text="A comment", author="Author's Name")
>>> ws.append([cell, 3.14, None])
>>> wb.save('write\_only\_file.xlsx')
This will create a write-only workbook with a single sheet, and append
a row of 3 cells: one text cell with a custom font and a comment, a
floating-point number, and an empty cell (which will be discarded
anyway).
.. warning::
\* Unlike a normal workbook, a newly-created write-only workbook
does not contain any worksheets; a worksheet must be specifically
created with the :func:`create\_sheet()` method.
\* In a write-only workbook, rows can only be added with
:func:`append()`. It is not possible to write (or read) cells at
arbitrary locations with :func:`cell()` or :func:`iter\_rows()`.
\* It is able to export unlimited amount of data (even more than Excel can
handle actually), while keeping memory usage under 10Mb.
\* A write-only workbook can only be saved once. After
that, every attempt to save the workbook or append() to an existing
worksheet will raise an :class:`openpyxl.utils.exceptions.WorkbookAlreadySaved`
exception.
\* Everything that appears in the file before the actual cell data must be created
before cells are added because it must written to the file before then.
For example, `freeze\_panes` should be set before cells are added.