st.popover - Streamlit Docs

## st.popover

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Insert a popover container.

Inserts a multi-element container as a popover. It consists of a button-like
element and a container that opens when the button is clicked.

Opening and closing the popover will not trigger a rerun. Interacting
with widgets inside of an open popover will rerun the app while keeping
the popover open. Clicking outside of the popover will close it.

To add elements to the returned container, you can use the "with"
notation (preferred) or just call methods directly on the returned object.
See examples below.

Note

To follow best design practices, don't nest popovers.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/layouts.py#L864 "View st.popover source code on GitHub") | |
| --- | --- |
| st.popover(label, \*, type="secondary", help=None, icon=None, disabled=False, use\_container\_width=None, width="content") | |
| Parameters | |
| label (str) | The label of the button that opens the popover container. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Display unsupported elements as literal characters by backslash-escaping them. E.g., "1\. Not an ordered list".  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| help (str or None) | A tooltip that gets displayed when the popover button is hovered over. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| type ("primary", "secondary", or "tertiary") | An optional string that specifies the button type. This can be one of the following:   * "primary": The button's background is the app's primary color   for additional emphasis. * "secondary" (default): The button's background coordinates   with the app's background color for normal emphasis. * "tertiary": The button is plain text without a border or   background for subtlety. |
| icon (str) | An optional emoji or icon to display next to the button label. If icon is None (default), no icon is displayed. If icon is a string, the following options are valid:   * A single-character emoji. For example, you can set icon="🚨"   or icon="🔥". Emoji short codes are not supported. * An icon from the Material Symbols library (rounded style) in the   format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, icon=":material/thumb\_up:" will display the   Thumb Up icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)    font library. * "spinner": Displays a spinner as an icon. |
| disabled (bool) | An optional boolean that disables the popover button if set to True. The default is False. |
| use\_container\_width (bool) | *delete* use\_container\_width is deprecated and will be removed in a future release. For use\_container\_width=True, use width="stretch". For use\_container\_width=False, use width="content".  Whether to expand the button's width to fill its parent container. If use\_container\_width is False (default), Streamlit sizes the button to fit its content. If use\_container\_width is True, the width of the button matches its parent container.  In both cases, if the content of the button is wider than the parent container, the content will line wrap.  The popover container's minimum width matches the width of its button. The popover container may be wider than its button to fit the container's content. |
| width (int, "stretch", or "content") | The width of the button. This can be one of the following:   * "content" (default): The width of the button matches the   width of its content, but doesn't exceed the width of the parent   container. * "stretch": The width of the button matches the width of the   parent container. * An integer specifying the width in pixels: The button has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the button matches the width   of the parent container.   The popover container's minimum width matches the width of its button. The popover container may be wider than its button to fit the container's contents. |

#### Examples

You can use the with notation to insert any element into a popover:

```
import streamlit as st

with st.popover("Open popover"):
    st.markdown("Hello World 👋")
    name = st.text_input("What's your name?")

st.write("Your name:", name)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-popover.streamlit.app//?utm_medium=oembed&)

Or you can just call methods directly on the returned objects:

```
import streamlit as st

popover = st.popover("Filter items")
red = popover.checkbox("Show red items.", True)
blue = popover.checkbox("Show blue items.", True)

if red:
    st.write(":red[This is a red item.]")
if blue:
    st.write(":blue[This is a blue item.]")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-popover2.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.form](https://docs.streamlit.io/develop/api-reference/execution-flow/st.form)[*arrow\_forward*Next: st.sidebar](/develop/api-reference/layout/st.sidebar)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI