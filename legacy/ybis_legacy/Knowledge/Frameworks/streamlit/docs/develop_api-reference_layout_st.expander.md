st.expander - Streamlit Docs

## st.expander

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Insert a multi-element container that can be expanded/collapsed.

Inserts a container into your app that can be used to hold multiple elements
and can be expanded or collapsed by the user. When collapsed, all that is
visible is the provided label.

To add elements to the returned container, you can use the with notation
(preferred) or just call methods directly on the returned object. See
examples below.

Note

All content within the expander is computed and sent to the
frontend, even if the expander is closed.

To follow best design practices and maintain a good appearance on
all screen sizes, don't nest expanders.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/layouts.py#L730 "View st.expander source code on GitHub") | |
| --- | --- |
| st.expander(label, expanded=False, \*, icon=None, width="stretch") | |
| Parameters | |
| label (str) | A string to use as the header for the expander. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Display unsupported elements as literal characters by backslash-escaping them. E.g., "1\. Not an ordered list".  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| expanded (bool) | If True, initializes the expander in "expanded" state. Defaults to False (collapsed). |
| icon (str, None) | An optional emoji or icon to display next to the expander label. If icon is None (default), no icon is displayed. If icon is a string, the following options are valid:   * A single-character emoji. For example, you can set icon="🚨"   or icon="🔥". Emoji short codes are not supported. * An icon from the Material Symbols library (rounded style) in the   format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, icon=":material/thumb\_up:" will display the   Thumb Up icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)    font library. * "spinner": Displays a spinner as an icon. |
| width ("stretch" or int) | The width of the expander container. This can be one of the following:   * "stretch" (default): The width of the container matches the   width of the parent container. * An integer specifying the width in pixels: The container has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the container matches the width   of the parent container. |

#### Examples

You can use the with notation to insert any element into an expander

```
import streamlit as st

st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

with st.expander("See explanation"):
    st.write('''
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    ''')
    st.image("https://static.streamlit.io/examples/dice.jpg")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-expander.streamlit.app//?utm_medium=oembed&)

Or you can just call methods directly on the returned objects:

```
import streamlit as st

st.bar_chart({"data": [1, 5, 2, 6, 2, 1]})

expander = st.expander("See explanation")
expander.write('''
    The chart above shows some numbers I picked for you.
    I rolled actual dice for these, so they're *guaranteed* to
    be random.
''')
expander.image("https://static.streamlit.io/examples/dice.jpg")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-expander.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.empty](/develop/api-reference/layout/st.empty)[*arrow\_forward*Next: st.form](https://docs.streamlit.io/develop/api-reference/execution-flow/st.form)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI