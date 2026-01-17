st.caption - Streamlit Docs

## st.caption

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display text in small font.

This should be used for captions, asides, footnotes, sidenotes, and
other explanatory text.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/markdown.py#L186 "View st.caption source code on GitHub") | |
| --- | --- |
| st.caption(body, unsafe\_allow\_html=False, \*, help=None, width="stretch", text\_alignment="left") | |
| Parameters | |
| body (str) | The text to display as GitHub-flavored Markdown. Syntax information can be found at: <https://github.github.com/gfm>.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| unsafe\_allow\_html (bool) | Whether to render HTML within body. If this is False (default), any HTML tags found in body will be escaped and therefore treated as raw text. If this is True, any HTML expressions within body will be rendered.  Adding custom HTML to your app impacts safety, styling, and maintainability.  Note  If you only want to insert HTML or CSS without Markdown text, we recommend using st.html instead. |
| help (str or None) | A tooltip that gets displayed next to the caption. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| width ("stretch", "content", or int) | The width of the caption element. This can be one of the following:   * "stretch" (default): The width of the element matches the   width of the parent container. * "content": The width of the element matches the width of its   content, but doesn't exceed the width of the parent container. * An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |
| text\_alignment ("left", "center", "right", or "justify") | The horizontal alignment of the text within the element. This can be one of the following:   * "left" (default): Text is aligned to the left edge. * "center": Text is centered. * "right": Text is aligned to the right edge. * "justify": Text is justified (stretched to fill the available   width with the last line left-aligned).   Note  For text alignment to have a visible effect, the element's width must be wider than its content. If you use width="content" with short text, the alignment may not be noticeable. |

#### Examples

```
import streamlit as st

st.caption("This is a string that explains something above.")
st.caption("A caption with _italics_ :blue[colors] and emojis :sunglasses:")
```

![](/images/api/st.caption.png)

[*arrow\_back*Previous: st.badge](/develop/api-reference/text/st.badge)[*arrow\_forward*Next: st.code](/develop/api-reference/text/st.code)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI