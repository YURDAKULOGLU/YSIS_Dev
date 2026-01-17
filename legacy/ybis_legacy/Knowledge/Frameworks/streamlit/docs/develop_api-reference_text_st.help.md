st.help - Streamlit Docs

## st.help

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display help and other information for a given object.

Depending on the type of object that is passed in, this displays the
object's name, type, value, signature, docstring, and member variables,
methods — as well as the values/docstring of members and methods.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/doc_string.py#L47 "View st.help source code on GitHub") | |
| --- | --- |
| st.help(obj=, \*, width="stretch") | |
| Parameters | |
| obj (any) | The object whose information should be displayed. If left unspecified, this call will display help for Streamlit itself. |
| width ("stretch" or int) | The width of the help element. This can be one of the following:   * "stretch" (default): The width of the element matches the   width of the parent container. * An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |

#### Example

Don't remember how to initialize a dataframe? Try this:

```
import streamlit as st
import pandas

st.help(pandas.DataFrame)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-string.streamlit.app//?utm_medium=oembed&)

Want to quickly check what data type is output by a certain function?
Try:

```
import streamlit as st

x = my_poorly_documented_function()
st.help(x)
```

Want to quickly inspect an object? No sweat:

```
class Dog:
  '''A typical dog.'''

  def __init__(self, breed, color):
    self.breed = breed
    self.color = color

  def bark(self):
    return 'Woof!'


fido = Dog("poodle", "white")

st.help(fido)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-string1.streamlit.app//?utm_medium=oembed&)

And if you're using Magic, you can get help for functions, classes,
and modules without even typing st.help:

```
import streamlit as st
import pandas

# Get help for Pandas read_csv:
pandas.read_csv

# Get help for Streamlit itself:
st
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-string2.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.text](/develop/api-reference/text/st.text)[*arrow\_forward*Next: st.html](/develop/api-reference/text/st.html)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI