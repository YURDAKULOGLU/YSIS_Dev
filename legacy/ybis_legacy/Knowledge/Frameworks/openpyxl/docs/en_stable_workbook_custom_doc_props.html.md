Custom Document Properties — openpyxl 3.1.3 documentation

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](protection.html "Protection") |
* [previous](defined_names.html "Defined Names") |
* [openpyxl 3.1.3 documentation](index.html) »
* Custom Document Properties

# Custom Document Properties[](#custom-document-properties "Link to this heading")

It is possible to add one or more CustomDocumentProperty objects to a workbook.
These require a unique name (string) and can be one of 6 types:

> * StringProperty
> * IntProperty
> * FloatProperty
> * DateTimeProperty
> * BoolProperty
> * LinkProperty

LinkProperties are always associated with a defined name range.

These properties are globally for a workbook and accessed from the custom\_doc\_props attribute.

## Sample use[](#sample-use "Link to this heading")

Looping over all the custom properties (“custom\_doc\_props”):

```
>>> for prop in wb.custom_doc_props.props:
>>>    print(f"{prop.name}: {prop.value}")
```

Adding a new property:

```
from openpyxl.packaging.custom import (
    BoolProperty,
    DateTimeProperty,
    FloatProperty,
    IntProperty,
    LinkProperty,
    StringProperty,
    CustomPropertyList,
)

props = CustomePropertyList()
props.append(StringProperty(name="PropName1", value="Something"))
```

## Deleting properties[](#deleting-properties "Link to this heading")

```
wb.custom_doc_props.append(StringProperty(name="PropName6", value="Something"))
# check the property
prop = wb.custom_doc_props["PropName6"]

# delete the string property:
del prop["PropName6"]

# save the file
wb.save('outfile.xlsx')
```

Note

Currently not all possible property types are supported. If openpyxl cannot read a particular type, it will provide a warning and ignore it.

[![Logo](_static/logo.png)](index.html)

### [Table of Contents](index.html)

* [Custom Document Properties](#)
  + [Sample use](#sample-use)
  + [Deleting properties](#deleting-properties)

#### Previous topic

[Defined Names](defined_names.html "previous chapter")

#### Next topic

[Protection](protection.html "next chapter")

### This Page

* [Show Source](_sources/workbook_custom_doc_props.rst.txt)

### Quick search

### Navigation

* [index](genindex.html "General Index")
* [modules](py-modindex.html "Python Module Index") |
* [next](protection.html "Protection") |
* [previous](defined_names.html "Defined Names") |
* [openpyxl 3.1.3 documentation](index.html) »
* Custom Document Properties

© Copyright 2010 - 2024, See AUTHORS.
Created using [Sphinx](https://www.sphinx-doc.org/) 7.3.7.