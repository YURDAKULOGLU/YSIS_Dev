st.text\_input - Streamlit Docs

## st.text\_input

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a single-line text input widget.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/widgets/text_widgets.py#L127 "View st.text_input source code on GitHub") | |
| --- | --- |
| st.text\_input(label, value="", max\_chars=None, key=None, type="default", help=None, autocomplete=None, on\_change=None, args=None, kwargs=None, \*, placeholder=None, disabled=False, label\_visibility="visible", icon=None, width="stretch") | |
| Parameters | |
| label (str) | A short label explaining to the user what this input is for. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Display unsupported elements as literal characters by backslash-escaping them. E.g., "1\. Not an ordered list".  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives.  For accessibility reasons, you should never set an empty label, but you can hide it with label\_visibility if needed. In the future, we may disallow empty labels by raising an exception. |
| value (object or None) | The text value of this widget when it first renders. This will be cast to str internally. If None, will initialize empty and return None until the user provides input. Defaults to empty string. |
| max\_chars (int or None) | Max number of characters allowed in text input. |
| key (str or int) | An optional string or integer to use as the unique key for the widget. If this is omitted, a key will be generated for the widget based on its content. No two widgets may have the same key. |
| type ("default" or "password") | The type of the text input. This can be either "default" (for a regular text input), or "password" (for a text input that masks the user's typed value). Defaults to "default". |
| help (str or None) | A tooltip that gets displayed next to the widget label. Streamlit only displays the tooltip when label\_visibility="visible". If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| autocomplete (str) | An optional value that will be passed to the <input> element's autocomplete property. If unspecified, this value will be set to "new-password" for "password" inputs, and the empty string for "default" inputs. For more details, see <https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/autocomplete> |
| on\_change (callable) | An optional callback invoked when this text input's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| placeholder (str or None) | An optional string displayed when the text input is empty. If None, no text is displayed. |
| disabled (bool) | An optional boolean that disables the text input if set to True. The default is False. |
| label\_visibility ("visible", "hidden", or "collapsed") | The visibility of the label. The default is "visible". If this is "hidden", Streamlit displays an empty spacer instead of the label, which can help keep the widget aligned with other widgets. |
| icon (str, None) | An optional emoji or icon to display within the input field to the left of the value. If icon is None (default), no icon is displayed. If icon is a string, the following options are valid:   * A single-character emoji. For example, you can set icon="🚨"   or icon="🔥". Emoji short codes are not supported. * An icon from the Material Symbols library (rounded style) in the   format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, icon=":material/thumb\_up:" will display the   Thumb Up icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)    font library. * "spinner": Displays a spinner as an icon. |
| width ("stretch" or int) | The width of the text input widget. This can be one of the following:   * "stretch" (default): The width of the widget matches the   width of the parent container. * An integer specifying the width in pixels: The widget has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the widget matches the width   of the parent container. |
|  |  |
| --- | --- |
| Returns | |
| (str or None) | The current value of the text input widget or None if no value has been provided by the user. |

#### Example

```
import streamlit as st

title = st.text_input("Movie title", "Life of Brian")
st.write("The current movie title is", title)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-text-input.streamlit.app//?utm_medium=oembed&)

  

Text input widgets can customize how to hide their labels with the `label_visibility` parameter. If "hidden", the label doesn’t show but there is still empty space for it above the widget (equivalent to `label=""`). If "collapsed", both the label and the space are removed. Default is "visible". Text input widgets can also be disabled with the `disabled` parameter, and can display an optional placeholder text when the text input is empty using the `placeholder` parameter:

`import streamlit as st
# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
st.session_state.visibility = "visible"
st.session_state.disabled = False
col1, col2 = st.columns(2)
with col1:
st.checkbox("Disable text input widget", key="disabled")
st.radio(
"Set text input label visibility 👉",
key="visibility",
options=["visible", "hidden", "collapsed"],
)
st.text_input(
"Placeholder for the other text input widget",
"This is a placeholder",
key="placeholder",
)
with col2:
text_input = st.text_input(
"Enter some text 👇",
label_visibility=st.session_state.visibility,
disabled=st.session_state.disabled,
placeholder=st.session_state.placeholder,
)
if text_input:
st.write("You entered: ", text_input)`

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-text-input1.streamlit.app/?utm_medium=oembed)

[*arrow\_back*Previous: st.text\_area](/develop/api-reference/widgets/st.text_area)[*arrow\_forward*Next: st.audio\_input](/develop/api-reference/widgets/st.audio_input)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI