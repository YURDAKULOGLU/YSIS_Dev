Working with Images — openpyxl 3.1.3 documentation

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](pandas.html "Working with Pandas and NumPy") |
* [previous](charts/graphical.html "Advanced Options with Graphical Properties") |
* [openpyxl 3.1.3 documentation](index.html) »
* Working with Images

# Working with Images[](#working-with-images "Link to this heading")

## Inserting an image[](#inserting-an-image "Link to this heading")

```
>>> from openpyxl import Workbook
>>> from openpyxl.drawing.image import Image
>>>
>>> wb = Workbook()
>>> ws = wb.active
>>> ws['A1'] = 'You should see three logos below'
>>>
>>> # create an image
>>> img = Image('logo.png')
>>>
>>> # add to worksheet and anchor next to cells
>>> ws.add_image(img, 'A1')
>>> wb.save('logo.xlsx')
```

[![Logo](_static/logo.png)](index.html)

### [Table of Contents](index.html)

* [Working with Images](#)
  + [Inserting an image](#inserting-an-image)

#### Previous topic

[Advanced Options with Graphical Properties](charts/graphical.html "previous chapter")

#### Next topic

[Working with Pandas and NumPy](pandas.html "next chapter")

### This Page

* [Show Source](_sources/images.rst.txt)

### Quick search

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](pandas.html "Working with Pandas and NumPy") |
* [previous](charts/graphical.html "Advanced Options with Graphical Properties") |
* [openpyxl 3.1.3 documentation](index.html) »
* Working with Images

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.