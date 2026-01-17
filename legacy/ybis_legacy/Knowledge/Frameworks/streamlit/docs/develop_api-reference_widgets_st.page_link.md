st.page\_link - Streamlit Docs

*star*

#### Tip

Check out our [tutorial](/develop/tutorials/multipage/st.page_link-nav) to learn about building custom, dynamic menus with `st.page_link`.

## st.page\_link

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a link to another page in a multipage app or to an external page.

If another page in a multipage app is specified, clicking st.page\_link
stops the current page execution and runs the specified page as if the
user clicked on it in the sidebar navigation.

If an external page is specified, clicking st.page\_link opens a new
tab to the specified page. The current script run will continue if not
complete.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/widgets/button.py#L882 "View st.page_link source code on GitHub") | |
| --- | --- |
| st.page\_link(page, \*, label=None, icon=None, help=None, disabled=False, use\_container\_width=None, width="content", query\_params=None) | |
| Parameters | |
| page (str, Path, or StreamlitPage) | The file path (relative to the main script) or a StreamlitPage indicating the page to switch to. Alternatively, this can be the URL to an external page (must start with "<http://>" or "<https://>"). |
| label (str) | The label for the page link. Labels are required for external pages. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Display unsupported elements as literal characters by backslash-escaping them. E.g., "1\. Not an ordered list".  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| icon (str or None) | An optional emoji or icon to display next to the button label. If icon is None (default), the icon is inferred from the StreamlitPage object or no icon is displayed. If icon is a string, the following options are valid:   * A single-character emoji. For example, you can set icon="🚨"   or icon="🔥". Emoji short codes are not supported. * An icon from the Material Symbols library (rounded style) in the   format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, icon=":material/thumb\_up:" will display the   Thumb Up icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)    font library. * "spinner": Displays a spinner as an icon. |
| help (str or None) | A tooltip that gets displayed when the link is hovered over. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| disabled (bool) | An optional boolean that disables the page link if set to True. The default is False. |
| use\_container\_width (bool) | *delete* use\_container\_width is deprecated and will be removed in a future release. For use\_container\_width=True, use width="stretch". For use\_container\_width=False, use width="content".  Whether to expand the link's width to fill its parent container. The default is True for page links in the sidebar and False for those in the main app. |
| width ("content", "stretch", or int) | The width of the page-link button. This can be one of the following:   * "content" (default): The width of the button matches the   width of its content, but doesn't exceed the width of the parent   container. * "stretch": The width of the button matches the width of the   parent container. * An integer specifying the width in pixels: The button has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the button matches the width   of the parent container. |
| query\_params (dict, list of tuples, or None) | Query parameters to apply when navigating to the target page. This can be a dictionary or an iterable of key-value tuples. Values can be strings or iterables of strings (for repeated keys). When this is None (default), all non-embed query parameters are cleared during navigation. |

#### Example

**Example 1: Basic usage**

The following example shows how to create page links in a multipage app
that uses the pages/ directory:

```
your-repository/
├── pages/
│   ├── page_1.py
│   └── page_2.py
└── your_app.py
```

```
import streamlit as st

st.page_link("your_app.py", label="Home", icon="🏠")
st.page_link("pages/page_1.py", label="Page 1", icon="1️⃣")
st.page_link("pages/page_2.py", label="Page 2", icon="2️⃣", disabled=True)
st.page_link("http://www.google.com", label="Google", icon="🌎")
```

The default navigation is shown here for comparison, but you can hide
the default navigation using the [client.showSidebarNavigation](https://docs.streamlit.io/develop/api-reference/configuration/config.toml#client)
configuration option. This allows you to create custom, dynamic
navigation menus for your apps!

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-page-link.streamlit.app//?utm_medium=oembed&)

**Example 2: Passing query parameters**

The following example shows how to pass query parameters when creating a
page link in a multipage app:

```
your-repository/
├── page_2.py
└── your_app.py
```

```
import streamlit as st

def page_1():
    st.title("Page 1")
    st.page_link("page_2.py", query_params={"utm_source": "page_1"})

pg = st.navigation([page_1, "page_2.py"])
pg.run()
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-page-link-query-params.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.link\_button](/develop/api-reference/widgets/st.link_button)[*arrow\_forward*Next: st.checkbox](/develop/api-reference/widgets/st.checkbox)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI