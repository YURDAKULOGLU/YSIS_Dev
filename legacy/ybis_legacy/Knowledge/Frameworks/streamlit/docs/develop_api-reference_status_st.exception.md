st.exception - Streamlit Docs

## st.exception

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display an exception.

When accessing the app through localhost, in the lower-right corner
of the exception, Streamlit displays links to Google and ChatGPT that
are prefilled with the contents of the exception message.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/exception.py#L51 "View st.exception source code on GitHub") | |
| --- | --- |
| st.exception(exception, width="stretch") | |
| Parameters | |
| exception (Exception) | The exception to display. |
| width ("stretch" or int) | The width of the exception element. This can be one of the following:   * "stretch" (default): The width of the element matches the   width of the parent container. * An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |

#### Example

```
import streamlit as st

e = RuntimeError("This is an exception of type RuntimeError")
st.exception(e)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-status-exception.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.error](/develop/api-reference/status/st.error)[*arrow\_forward*Next: st.progress](/develop/api-reference/status/st.progress)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI