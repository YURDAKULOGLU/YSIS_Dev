st.select\_slider - Streamlit Docs

## st.select\_slider

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a slider widget to select items from a list.

This also allows you to render a range slider by passing a two-element
tuple or list as the value.

The difference between st.select\_slider and st.slider is that
select\_slider accepts any datatype and takes an iterable set of
options, while st.slider only accepts numerical or date/time data and
takes a range as input.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/widgets/select_slider.py#L145 "View st.select_slider source code on GitHub") | |
| --- | --- |
| st.select\_slider(label, options=(), value=None, format\_func=special\_internal\_function, key=None, help=None, on\_change=None, args=None, kwargs=None, \*, disabled=False, label\_visibility="visible", width="stretch") | |
| Parameters | |
| label (str) | A short label explaining to the user what this slider is for. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Display unsupported elements as literal characters by backslash-escaping them. E.g., "1\. Not an ordered list".  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives.  For accessibility reasons, you should never set an empty label, but you can hide it with label\_visibility if needed. In the future, we may disallow empty labels by raising an exception. |
| options (Iterable) | Labels for the select options in an Iterable. This can be a list, set, or anything supported by st.dataframe. If options is dataframe-like, the first column will be used. Each label will be cast to str internally by default. |
| value (a supported type or a tuple/list of supported types or None) | The value of the slider when it first renders. If a tuple/list of two values is passed here, then a range slider with those lower and upper bounds is rendered. For example, if set to (1, 10) the slider will have a selectable range between 1 and 10. Defaults to first option. |
| format\_func (function) | Function to modify the display of the labels from the options. argument. It receives the option as an argument and its output will be cast to str. |
| key (str or int) | An optional string or integer to use as the unique key for the widget. If this is omitted, a key will be generated for the widget based on its content. No two widgets may have the same key. |
| help (str or None) | A tooltip that gets displayed next to the widget label. Streamlit only displays the tooltip when label\_visibility="visible". If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| on\_change (callable) | An optional callback invoked when this select\_slider's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| disabled (bool) | An optional boolean that disables the select slider if set to True. The default is False. |
| label\_visibility ("visible", "hidden", or "collapsed") | The visibility of the label. The default is "visible". If this is "hidden", Streamlit displays an empty spacer instead of the label, which can help keep the widget aligned with other widgets. If this is "collapsed", Streamlit displays no label or spacer. |
| width ("stretch" or int) | The width of the slider widget. This can be one of the following:   * "stretch" (default): The width of the widget matches the   width of the parent container. * An integer specifying the width in pixels: The widget has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the widget matches the width   of the parent container. |
|  |  |
| --- | --- |
| Returns | |
| (any value or tuple of any value) | The current value of the slider widget. The return type will match the data type of the value parameter.  This contains copies of the selected options, not the originals. |

#### Examples

```
import streamlit as st

color = st.select_slider(
    "Select a color of the rainbow",
    options=[
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "indigo",
        "violet",
    ],
)
st.write("My favorite color is", color)
```

And here's an example of a range select slider:

```
import streamlit as st

start_color, end_color = st.select_slider(
    "Select a range of color wavelength",
    options=[
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "indigo",
        "violet",
    ],
    value=("red", "blue"),
)
st.write("You selected wavelengths between", start_color, "and", end_color)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-select-slider.streamlit.app//?utm_medium=oembed&)

### Featured videos

Check out our video on how to use one of Streamlit's core functions, the select slider! 🎈

In the video below, we'll take it a step further and make a double-ended slider.

[*arrow\_back*Previous: st.selectbox](/develop/api-reference/widgets/st.selectbox)[*arrow\_forward*Next: st.toggle](/develop/api-reference/widgets/st.toggle)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI