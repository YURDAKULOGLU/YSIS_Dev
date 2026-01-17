Comments — openpyxl 3.1.3 documentation

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](datetime.html "Dates and Times") |
* [previous](pivot.html "Pivot Tables") |
* [openpyxl 3.1.3 documentation](index.html) »
* Comments

# Comments[](#comments "Link to this heading")

Warning

Openpyxl currently supports the reading and writing of comment text only.
Formatting information is lost. Comment dimensions are lost upon reading,
but can be written. Comments are not currently supported if
read\_only=True is used.

## Adding a comment to a cell[](#adding-a-comment-to-a-cell "Link to this heading")

Comments have a text attribute and an author attribute, which must both be set

```
>>> from openpyxl import Workbook
>>> from openpyxl.comments import Comment
>>> wb = Workbook()
>>> ws = wb.active
>>> comment = ws["A1"].comment
>>> comment = Comment('This is the comment text', 'Comment Author')
>>> comment.text
'This is the comment text'
>>> comment.author
'Comment Author'
```

If you assign the same comment to multiple cells then openpyxl will automatically create copies

```
>>> from openpyxl import Workbook
>>> from openpyxl.comments import Comment
>>> wb=Workbook()
>>> ws=wb.active
>>> comment = Comment("Text", "Author")
>>> ws["A1"].comment = comment
>>> ws["B2"].comment = comment
>>> ws["A1"].comment is comment
True
>>> ws["B2"].comment is comment
False
```

## Loading and saving comments[](#loading-and-saving-comments "Link to this heading")

Comments present in a workbook when loaded are stored in the comment
attribute of their respective cells automatically. Formatting information
such as font size, bold and italics are lost, as are the original dimensions
and position of the comment’s container box.

Comments remaining in a workbook when it is saved are automatically saved to
the workbook file.

Comment dimensions can be specified for write-only. Comment dimension are
in pixels.

```
>>> from openpyxl import Workbook
>>> from openpyxl.comments import Comment
>>> from openpyxl.utils import units
>>>
>>> wb=Workbook()
>>> ws=wb.active
>>>
>>> comment = Comment("Text", "Author")
>>> comment.width = 300
>>> comment.height = 50
>>>
>>> ws["A1"].comment = comment
>>>
>>> wb.save('commented_book.xlsx')
```

If needed, `openpyxl.utils.units` contains helper functions for converting
from other measurements such as mm or points to pixels:

```
>>> from openpyxl import Workbook
>>> from openpyxl.comments import Comment
>>> from openpyxl.utils import units
>>>
>>> wb=Workbook()
>>> ws=wb.active
>>>
>>> comment = Comment("Text", "Author")
>>> comment.width = units.points_to_pixels(300)
>>> comment.height = units.points_to_pixels(50)
>>>
>>> ws["A1"].comment = comment
```

[![Logo](_static/logo.png)](index.html)

### [Table of Contents](index.html)

* [Comments](#)
  + [Adding a comment to a cell](#adding-a-comment-to-a-cell)
  + [Loading and saving comments](#loading-and-saving-comments)

#### Previous topic

[Pivot Tables](pivot.html "previous chapter")

#### Next topic

[Dates and Times](datetime.html "next chapter")

### This Page

* [Show Source](_sources/comments.rst.txt)

### Quick search

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](datetime.html "Dates and Times") |
* [previous](pivot.html "Pivot Tables") |
* [openpyxl 3.1.3 documentation](index.html) »
* Comments

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.