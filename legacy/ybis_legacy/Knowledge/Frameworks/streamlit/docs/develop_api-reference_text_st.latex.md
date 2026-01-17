st.latex - Streamlit Docs

## st.latex

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display mathematical expressions formatted as LaTeX.

Supported LaTeX functions are listed at
<https://katex.org/docs/supported.html>.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/markdown.py#L283 "View st.latex source code on GitHub") | |
| --- | --- |
| st.latex(body, \*, help=None, width="stretch") | |
| Parameters | |
| body (str or SymPy expression) | The string or SymPy expression to display as LaTeX. If str, it's a good idea to use raw Python strings since LaTeX uses backslashes a lot. |
| help (str or None) | A tooltip that gets displayed next to the LaTeX expression. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| width ("stretch", "content", or int) | The width of the LaTeX element. This can be one of the following:   * "stretch" (default): The width of the element matches the   width of the parent container. * "content": The width of the element matches the width of its   content, but doesn't exceed the width of the parent container. * An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |

#### Example

```
import streamlit as st

st.latex(r'''
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    ''')
```

![](/images/api/st.latex.png)

[*arrow\_back*Previous: st.echo](/develop/api-reference/text/st.echo)[*arrow\_forward*Next: st.text](/develop/api-reference/text/st.text)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI