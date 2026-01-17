st.space - Streamlit Docs

## st.space

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Add vertical or horizontal space.

This command adds space in the direction of its parent container. In
a vertical layout, it adds vertical space. In a horizontal layout, it
adds horizontal space.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/space.py#L32 "View st.space source code on GitHub") | |
| --- | --- |
| st.space(size="small") | |
| Parameters | |
| size ("small", "medium", "large", "stretch", or int) | The size of the space. This can be one of the following values:   * "small" (default): 0.75rem, which is the height of a widget   label. This is useful for aligning buttons with labeled widgets. * "medium": 2.5rem, which is the height of a button or   (unlabeled) input field. * "large": 4.25rem, which is the height of a labeled input   field or unlabeled media widget, like st.file\_uploader. * "stretch": Expands to fill remaining space in the container. * An integer: Fixed size in pixels. |

#### Examples

**Example 1: Use vertical space to align elements**

Use small spaces to replace label heights. Use medium spaces to replace
two label heights or a button.

```
import streamlit as st

left, middle, right = st.columns(3)

left.space("medium")
left.button("Left button", width="stretch")

middle.space("small")
middle.text_input("Middle input")

right.audio_input("Right uploader")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-space-vertical.streamlit.app//?utm_medium=oembed&)

**Example 2: Add horizontal space in a container**

Use stretch space to float elements left and right.

```
import streamlit as st

with st.container(horizontal=True):
    st.button("Left")
    st.space("stretch")
    st.button("Right")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-space-horizontal.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.sidebar](/develop/api-reference/layout/st.sidebar)[*arrow\_forward*Next: st.tabs](/develop/api-reference/layout/st.tabs)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI