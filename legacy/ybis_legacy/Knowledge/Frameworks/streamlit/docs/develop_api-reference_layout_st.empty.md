st.empty - Streamlit Docs

## st.empty

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Insert a single-element container.

Inserts a container into your app that can be used to hold a single element.
This allows you to, for example, remove elements at any point, or replace
several elements at once (using a child multi-element container).

To insert/replace/clear an element on the returned container, you can
use with notation or just call methods directly on the returned object.
See examples below.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/empty.py#L28 "View st.empty source code on GitHub") | |
| --- | --- |
| st.empty() | |

#### Examples

Inside a with st.empty(): block, each displayed element will
replace the previous one.

```
import streamlit as st
import time

with st.empty():
    for seconds in range(10):
        st.write(f"⏳ {seconds} seconds have passed")
        time.sleep(1)
    st.write(":material/check: 10 seconds over!")
st.button("Rerun")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-empty.streamlit.app//?utm_medium=oembed&)

You can use an st.empty to replace multiple elements in
succession. Use st.container inside st.empty to display (and
later replace) a group of elements.

```
import streamlit as st
import time

st.button("Start over")

placeholder = st.empty()
placeholder.markdown("Hello")
time.sleep(1)

placeholder.progress(0, "Wait for it...")
time.sleep(1)
placeholder.progress(50, "Wait for it...")
time.sleep(1)
placeholder.progress(100, "Wait for it...")
time.sleep(1)

with placeholder.container():
    st.line_chart({"data": [1, 5, 2, 6]})
    time.sleep(1)
    st.markdown("3...")
    time.sleep(1)
    st.markdown("2...")
    time.sleep(1)
    st.markdown("1...")
    time.sleep(1)

placeholder.markdown("Poof!")
time.sleep(1)

placeholder.empty()
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-empty-placeholder.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.dialog](https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog)[*arrow\_forward*Next: st.expander](/develop/api-reference/layout/st.expander)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI