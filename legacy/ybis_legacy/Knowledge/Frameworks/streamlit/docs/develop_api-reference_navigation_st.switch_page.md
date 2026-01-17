st.switch\_page - Streamlit Docs

## st.switch\_page

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Programmatically switch the current page in a multipage app.

When st.switch\_page is called, the current page execution stops and
the specified page runs as if the user clicked on it in the sidebar
navigation. The specified page must be recognized by Streamlit's multipage
architecture (your main Python file or a Python file in a pages/
folder). Arbitrary Python scripts cannot be passed to st.switch\_page.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/commands/execution_control.py#L187 "View st.switch_page source code on GitHub") | |
| --- | --- |
| st.switch\_page(page, \*, query\_params=None) | |
| Parameters | |
| page (str, Path, or st.Page) | The file path (relative to the main script) or an st.Page indicating the page to switch to. |
| query\_params (dict, list of tuples, or None) | Query parameters to apply when navigating to the target page. This can be a dictionary or an iterable of key-value tuples. Values can be strings or iterables of strings (for repeated keys). When this is None (default), all non-embed query parameters are cleared during navigation. |

#### Examples

**Example 1: Basic usage**

The following example shows how to switch to a different page in a
multipage app that uses the pages/ directory:

```
your-repository/
├── pages/
│   ├── page_1.py
│   └── page_2.py
└── your_app.py
```

```
import streamlit as st

if st.button("Home"):
    st.switch_page("your_app.py")
if st.button("Page 1"):
    st.switch_page("pages/page_1.py")
if st.button("Page 2"):
    st.switch_page("pages/page_2.py")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-switch-page.streamlit.app//?utm_medium=oembed&)

**Example 2: Passing query parameters**

The following example shows how to pass query parameters when switching to a
different page. This example uses st.navigation to create a multipage app.

```
your-repository/
├── page_2.py
└── your_app.py
```

```
import streamlit as st

def page_1():
    st.title("Page 1")
    if st.button("Switch to Page 2"):
        st.switch_page("page_2.py", query_params={"utm_source": "page_1"})

pg = st.navigation([page_1, "page_2.py"])
pg.run()
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-switch-page-query-params.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.page\_link](https://docs.streamlit.io/develop/api-reference/widgets/st.page_link)[*arrow\_forward*Next: Execution flow](/develop/api-reference/execution-flow)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI