st.spinner - Streamlit Docs

## st.spinner

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a loading spinner while executing a block of code.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/spinner.py#L37 "View st.spinner source code on GitHub") | |
| --- | --- |
| st.spinner(text="In progress...", \*, show\_time=False, width="content") | |
| Parameters | |
| text (str) | The text to display next to the spinner. This defaults to "In progress...".  The text can optionally contain GitHub-flavored Markdown. Syntax information can be found at: <https://github.github.com/gfm>.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| show\_time (bool) | Whether to show the elapsed time next to the spinner text. If this is False (default), no time is displayed. If this is True, elapsed time is displayed with a precision of 0.1 seconds. The time format is not configurable. |
| width ("content", "stretch", or int) | The width of the spinner element. This can be one of the following:   * "content" (default): The width of the element matches the   width of its content, but doesn't exceed the width of the parent   container. * "stretch": The width of the element matches the width of the   parent container. * An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |

#### Example

```
import streamlit as st
import time

with st.spinner("Wait for it...", show_time=True):
    time.sleep(5)
st.success("Done!")
st.button("Rerun")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-spinner.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.progress](/develop/api-reference/status/st.progress)[*arrow\_forward*Next: st.status](/develop/api-reference/status/st.status)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI