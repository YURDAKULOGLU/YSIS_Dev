st.number\_input - Streamlit Docs

## st.number\_input

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a numeric input widget.

Note

Integer values exceeding +/- (1<<53) - 1 cannot be accurately
stored or returned by the widget due to serialization constraints
between the Python server and JavaScript client. You must handle
such numbers as floats, leading to a loss in precision.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/widgets/number_input.py#L214 "View st.number_input source code on GitHub") | |
| --- | --- |
| st.number\_input(label, min\_value=None, max\_value=None, value="min", step=None, format=None, key=None, help=None, on\_change=None, args=None, kwargs=None, \*, placeholder=None, disabled=False, label\_visibility="visible", icon=None, width="stretch") | |
| Parameters | |
| label (str) | A short label explaining to the user what this input is for. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Display unsupported elements as literal characters by backslash-escaping them. E.g., "1\. Not an ordered list".  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives.  For accessibility reasons, you should never set an empty label, but you can hide it with label\_visibility if needed. In the future, we may disallow empty labels by raising an exception. |
| min\_value (int, float, or None) | The minimum permitted value. If this is None (default), there will be no minimum for float values and a minimum of - (1<<53) + 1 for integer values. |
| max\_value (int, float, or None) | The maximum permitted value. If this is None (default), there will be no maximum for float values and a maximum of (1<<53) - 1 for integer values. |
| value (int, float, "min" or None) | The value of this widget when it first renders. If this is "min" (default), the initial value is min\_value unless min\_value is None. If min\_value is None, the widget initializes with a value of 0.0 or 0.  If value is None, the widget will initialize with no value and return None until the user provides input. |
| step (int, float, or None) | The stepping interval. Defaults to 1 if the value is an int, 0.01 otherwise. If the value is not specified, the format parameter will be used. |
| format (str or None) | A printf-style format string controlling how the interface should display numbers. The output must be purely numeric. This does not impact the return value of the widget. For more information about the formatting specification, see [sprintf.js](https://github.com/alexei/sprintf.js?tab=readme-ov-file#format-specification).  For example, format="%0.1f" adjusts the displayed decimal precision to only show one digit after the decimal. |
| key (str or int) | An optional string or integer to use as the unique key for the widget. If this is omitted, a key will be generated for the widget based on its content. No two widgets may have the same key. |
| help (str or None) | A tooltip that gets displayed next to the widget label. Streamlit only displays the tooltip when label\_visibility="visible". If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| on\_change (callable) | An optional callback invoked when this number\_input's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| placeholder (str or None) | An optional string displayed when the number input is empty. If None, no placeholder is displayed. |
| disabled (bool) | An optional boolean that disables the number input if set to True. The default is False. |
| label\_visibility ("visible", "hidden", or "collapsed") | The visibility of the label. The default is "visible". If this is "hidden", Streamlit displays an empty spacer instead of the label, which can help keep the widget aligned with other widgets. If this is "collapsed", Streamlit displays no label or spacer. |
| icon (str, None) | An optional emoji or icon to display within the input field to the left of the value. If icon is None (default), no icon is displayed. If icon is a string, the following options are valid:   * A single-character emoji. For example, you can set icon="🚨"   or icon="🔥". Emoji short codes are not supported. * An icon from the Material Symbols library (rounded style) in the   format ":material/icon\_name:" where "icon\_name" is the name   of the icon in snake case.  For example, icon=":material/thumb\_up:" will display the   Thumb Up icon. Find additional icons in the [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)    font library. * "spinner": Displays a spinner as an icon. |
| width ("stretch" or int) | The width of the number input widget. This can be one of the following:   * "stretch" (default): The width of the widget matches the   width of the parent container. * An integer specifying the width in pixels: The widget has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the widget matches the width   of the parent container. |
|  |  |
| --- | --- |
| Returns | |
| (int or float or None) | The current value of the numeric input widget or None if the widget is empty. The return type will match the data type of the value parameter. |

#### Example

```
import streamlit as st

number = st.number_input("Insert a number")
st.write("The current number is ", number)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-number-input.streamlit.app//?utm_medium=oembed&)

To initialize an empty number input, use None as the value:

```
import streamlit as st

number = st.number_input(
    "Insert a number", value=None, placeholder="Type a number..."
)
st.write("The current number is ", number)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-number-input-empty.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.toggle](/develop/api-reference/widgets/st.toggle)[*arrow\_forward*Next: st.slider](/develop/api-reference/widgets/st.slider)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI