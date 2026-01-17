st.divider - Streamlit Docs

## st.divider

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a horizontal rule.

Note

You can achieve the same effect with st.write("---") or
even just "---" in your script (via magic).

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/markdown.py#L353 "View st.divider source code on GitHub") | |
| --- | --- |
| st.divider(\*, width="stretch") | |
| Parameters | |
| width ("stretch" or int) | The width of the divider element. This can be one of the following:   * "stretch" (default): The width of the element matches the   width of the parent container. * An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |

#### Example

```
import streamlit as st

st.divider()
```

Here's what it looks like in action when you have multiple elements in the app:

`import streamlit as st
st.write("This is some text.")
st.slider("This is a slider", 0, 100, (25, 75))
st.divider() # 👈 Draws a horizontal rule
st.write("This text is between the horizontal rules.")
st.divider() # 👈 Another horizontal rule`

![](/images/api/st.divider.png)

[*arrow\_back*Previous: st.code](/develop/api-reference/text/st.code)[*arrow\_forward*Next: st.echo](/develop/api-reference/text/st.echo)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI