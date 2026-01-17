st.link\_button - Streamlit Docs

## st.link\_button

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a link button element.

When clicked, a new tab will be opened to the specified URL. This will
create a new session for the user if directed within the app.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/widgets/button.py#L717 "View st.link_button source code on GitHub") | |
| --- | --- |
| st.link\_button(label, url, \*, help=None, type="secondary", icon=None, disabled=False, use\_container\_width=None, width="content", shortcut=None) | |
| Parameters | |
| label (str) | A short label explaining to the user what this button is for. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Display unsupported elements as literal characters by backslash-escaping them. E.g., "1\. Not an ordered list".  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| url (str) | The url to be opened on user click |
| help (str or None) | A tooltip that gets displayed when the button is hovered over. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| type ("primary", "secondary", or "tertiary") | An optional string that specifies the button type. This can be one of the following:   * "primary": The button's background is the app's primary color   for additional emphasis. * "secondary" (default): The button's background coordinates   with the app's background color for normal emphasis. * "tertiary": The button is plain text without a border or   background for subtlety. |
| icon (str or None) | An optional emoji or icon to display next to the button label. If icon is None (default), no icon is displayed. If icon is a string, the following options are valid:   * A single-character emoji. For example, you can set icon="🚨"   or icon="🔥". Emoji short codes are not supported. * An icon from the Material Symbols library (rounded style) in the   format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, icon=":material/thumb\_up:" will display the   Thumb Up icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)    font library. * "spinner": Displays a spinner as an icon. |
| disabled (bool) | An optional boolean that disables the link button if set to True. The default is False. |
| use\_container\_width (bool) | *delete* use\_container\_width is deprecated and will be removed in a future release. For use\_container\_width=True, use width="stretch". For use\_container\_width=False, use width="content".  Whether to expand the button's width to fill its parent container. If use\_container\_width is False (default), Streamlit sizes the button to fit its contents. If use\_container\_width is True, the width of the button matches its parent container.  In both cases, if the contents of the button are wider than the parent container, the contents will line wrap. |
| width ("content", "stretch", or int) | The width of the link button. This can be one of the following:   * "content" (default): The width of the button matches the   width of its content, but doesn't exceed the width of the parent   container. * "stretch": The width of the button matches the width of the   parent container. * An integer specifying the width in pixels: The button has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the button matches the width   of the parent container. |
| shortcut (str or None) | An optional keyboard shortcut that triggers the button. This can be one of the following strings:   * A single alphanumeric key like "K" or "4". * A function key like "F11". * A special key like "Enter", "Esc", or "Tab". * Any of the above combined with modifiers. For example, you can use   "Ctrl+K" or "Cmd+Shift+O".   Important  The keys "C" and "R" are reserved and can't be used, even with modifiers. Punctuation keys like "." and "," aren't currently supported.  For a list of supported keys and modifiers, see the documentation for [st.button](https://docs.streamlit.io/develop/api-reference/widgets/st.button). |

#### Example

```
import streamlit as st

st.link_button("Go to gallery", "https://streamlit.io/gallery")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-link-button.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.form\_submit\_button](https://docs.streamlit.io/develop/api-reference/execution-flow/st.form_submit_button)[*arrow\_forward*Next: st.page\_link](/develop/api-reference/widgets/st.page_link)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI