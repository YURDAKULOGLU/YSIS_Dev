Custom Document Properties
==========================
It is possible to add one or more CustomDocumentProperty objects to a workbook.
These require a unique name (string) and can be one of 6 types:
\* StringProperty
\* IntProperty
\* FloatProperty
\* DateTimeProperty
\* BoolProperty
\* LinkProperty
LinkProperties are always associated with a defined name range.
These properties are globally for a workbook and accessed from the `custom\_doc\_props` attribute.
Sample use
----------
Looping over all the custom properties ("custom\_doc\_props")::
>>> for prop in wb.custom\_doc\_props.props:
>>> print(f"{prop.name}: {prop.value}")
Adding a new property:
.. code::
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
Deleting properties
-------------------
.. code::
wb.custom\_doc\_props.append(StringProperty(name="PropName6", value="Something"))
# check the property
prop = wb.custom\_doc\_props["PropName6"]
# delete the string property:
del prop["PropName6"]
# save the file
wb.save('outfile.xlsx')
.. note::
Currently not all possible property types are supported. If openpyxl cannot read a particular type, it will provide a warning and ignore it.