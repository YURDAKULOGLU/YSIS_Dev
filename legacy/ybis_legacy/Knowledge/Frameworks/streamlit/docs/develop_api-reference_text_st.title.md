st.title - Streamlit Docs

## st.title

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display text in title formatting.

Each document should have a single st.title(), although this is not
enforced.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/heading.py#L255 "View st.title source code on GitHub") | |
| --- | --- |
| st.title(body, anchor=None, \*, help=None, width="stretch", text\_alignment="left") | |
| Parameters | |
| body (str) | The text to display as GitHub-flavored Markdown. Syntax information can be found at: <https://github.github.com/gfm>.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| anchor (str or False) | The anchor name of the header that can be accessed with #anchor in the URL. If omitted, it generates an anchor using the body. If False, the anchor is not shown in the UI. |
| help (str or None) | A tooltip that gets displayed next to the title. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| width ("stretch", "content", or int) | The width of the title element. This can be one of the following:   * "stretch" (default): The width of the element matches the   width of the parent container. * "content": The width of the element matches the width of its   content, but doesn't exceed the width of the parent container. * An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |
| text\_alignment ("left", "center", "right", or "justify") | The horizontal alignment of the text within the element. This can be one of the following:   * "left" (default): Text is aligned to the left edge. * "center": Text is centered. * "right": Text is aligned to the right edge. * "justify": Text is justified (stretched to fill the available   width with the last line left-aligned).   Note  For text alignment to have a visible effect, the element's width must be wider than its content. If you use width="content" with short text, the alignment may not be noticeable. |

#### Examples

```
import streamlit as st

st.title("This is a title")
st.title("_Streamlit_ is :blue[cool] :sunglasses:")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-title.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: Text elements](/develop/api-reference/text)[*arrow\_forward*Next: st.header](/develop/api-reference/text/st.header)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI