st.html - Streamlit Docs

## st.html

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Insert HTML into your app.

Adding custom HTML to your app impacts safety, styling, and
maintainability. We sanitize HTML with [DOMPurify](https://github.com/cure53/DOMPurify), but inserting HTML remains a
developer risk. Passing untrusted code to st.html or dynamically
loading external code can increase the risk of vulnerabilities in your
app.

st.html content is **not** iframed. By default, JavaScript is
ignored. To execute JavaScript contained in your HTML, set
unsafe\_allow\_javascript=True. Use this with caution and never pass
untrusted input.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/html.py#L39 "View st.html source code on GitHub") | |
| --- | --- |
| st.html(body, \*, width="stretch", unsafe\_allow\_javascript=False) | |
| Parameters | |
| body (any) | The HTML code to insert. This can be one of the following:   * A string of HTML code. * A path to a local file with HTML code. The path can be a str   or Path object. Paths can be absolute or relative to the   working directory (where you execute streamlit run). * Any object. If body is not a string or path, Streamlit will   convert the object to a string. body.\_repr\_html\_() takes   precedence over str(body) when available.   If the resulting HTML content is empty, Streamlit will raise an error.  If body is a path to a CSS file, Streamlit will wrap the CSS content in <style> tags automatically. When the resulting HTML content only contains style tags, Streamlit will send the content to the event container instead of the main container to avoid taking up space in the app. |
| width ("stretch", "content", or int) | The width of the HTML element. This can be one of the following:   * "stretch" (default): The width of the element matches the   width of the parent container. * "content": The width of the element matches the width of its   content, but doesn't exceed the width of the parent container. * An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |
| unsafe\_allow\_javascript (bool) | Whether to execute JavaScript contained in your HTML. If this is False (default), JavaScript is ignored. If this is True, JavaScript is executed. Use this with caution and never pass untrusted input. |

#### Example

```
import streamlit as st

st.html(
    "<p><span style='text-decoration: line-through double red;'>Oops</span>!</p>"
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-html.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.help](/develop/api-reference/text/st.help)[*arrow\_forward*Next: Data elements](/develop/api-reference/data)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI