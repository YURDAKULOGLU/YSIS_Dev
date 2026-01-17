Pivot Tables — openpyxl 3.1.3 documentation

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](comments.html "Comments") |
* [previous](print_settings.html "Print Settings") |
* [openpyxl 3.1.3 documentation](index.html) »
* Pivot Tables

# Pivot Tables[](#pivot-tables "Link to this heading")

openpyxl provides read-support for pivot tables so that they will be
preserved in existing files. The specification for pivot tables, while
extensive, is not very clear and it is not intended that client code should
be able to create pivot tables. However, it should be possible to edit and
manipulate existing pivot tables, eg. change their ranges or whether they
should update automatically settings.

As is the case for charts, images and tables there is currently no management
API for pivot tables so that client code will have to loop over the
`_pivots` list of a worksheet.

## Example[](#example "Link to this heading")

```
from openpyxl import load_workbook
wb = load_workbook("campaign.xlsx")
ws = wb["Results"]
pivot = ws._pivots[0] # any will do as they share the same cache
pivot.cache.refreshOnLoad = True
```

For further information see [`openpyxl.pivot.cache.CacheDefinition`](api/openpyxl.pivot.cache.html#openpyxl.pivot.cache.CacheDefinition "openpyxl.pivot.cache.CacheDefinition")

[![Logo](_static/logo.png)](index.html)

### [Table of Contents](index.html)

* [Pivot Tables](#)
  + [Example](#example)

#### Previous topic

[Print Settings](print_settings.html "previous chapter")

#### Next topic

[Comments](comments.html "next chapter")

### This Page

* [Show Source](_sources/pivot.rst.txt)

### Quick search

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](comments.html "Comments") |
* [previous](print_settings.html "Print Settings") |
* [openpyxl 3.1.3 documentation](index.html) »
* Pivot Tables

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.