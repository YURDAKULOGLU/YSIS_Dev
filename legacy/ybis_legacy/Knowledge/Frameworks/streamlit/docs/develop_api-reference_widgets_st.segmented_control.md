st.segmented\_control - Streamlit Docs

## st.segmented\_control

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a segmented control widget.

A segmented control widget is a linear set of segments where each of
the passed options functions like a toggle button.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/widgets/button_group.py#L744 "View st.segmented_control source code on GitHub") | |
| --- | --- |
| st.segmented\_control(label, options, \*, selection\_mode="single", default=None, format\_func=None, key=None, help=None, on\_change=None, args=None, kwargs=None, disabled=False, label\_visibility="visible", width="content") | |
| Parameters | |
| label (str) | A short label explaining to the user what this widget is for. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Display unsupported elements as literal characters by backslash-escaping them. E.g., "1\. Not an ordered list".  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives.  For accessibility reasons, you should never set an empty label, but you can hide it with label\_visibility if needed. In the future, we may disallow empty labels by raising an exception. |
| options (Iterable of V) | Labels for the select options in an Iterable. This can be a list, set, or anything supported by st.dataframe. If options is dataframe-like, the first column will be used. Each label will be cast to str internally by default and can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| selection\_mode ("single" or "multi") | The selection mode for the widget. If this is "single" (default), only one option can be selected. If this is "multi", multiple options can be selected. |
| default (Iterable of V, V, or None) | The value of the widget when it first renders. If the selection\_mode is multi, this can be a list of values, a single value, or None. If the selection\_mode is "single", this can be a single value or None. |
| format\_func (function) | Function to modify the display of the options. It receives the raw option as an argument and should output the label to be shown for that option. This has no impact on the return value of the command. The output can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| key (str or int) | An optional string or integer to use as the unique key for the widget. If this is omitted, a key will be generated for the widget based on its content. Multiple widgets of the same type may not share the same key. |
| help (str or None) | A tooltip that gets displayed next to the widget label. Streamlit only displays the tooltip when label\_visibility="visible". If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| on\_change (callable) | An optional callback invoked when this widget's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| disabled (bool) | An optional boolean that disables the widget if set to True. The default is False. |
| label\_visibility ("visible", "hidden", or "collapsed") | The visibility of the label. The default is "visible". If this is "hidden", Streamlit displays an empty spacer instead of the label, which can help keep the widget aligned with other widgets. If this is "collapsed", Streamlit displays no label or spacer. |
| width ("content", "stretch", or int) | The width of the segmented control widget. This can be one of the following:   * "content" (default): The width of the widget matches the   width of its content, but doesn't exceed the width of the parent   container. * "stretch": The width of the widget matches the width of the   parent container. * An integer specifying the width in pixels: The widget has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the widget matches the width   of the parent container. |
|  |  |
| --- | --- |
| Returns | |
| (list of V, V, or None) | If the selection\_mode is multi, this is a list of selected options or an empty list. If the selection\_mode is "single", this is a selected option or None.  This contains copies of the selected options, not the originals. |

#### Examples

**Example 1: Multi-select segmented control**

Display a multi-select segmented control widget, and show the
selection:

```
import streamlit as st

options = ["North", "East", "South", "West"]
selection = st.segmented_control(
    "Directions", options, selection_mode="multi"
)
st.markdown(f"Your selected options: {selection}.")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-segmented-control-multi.streamlit.app//?utm_medium=oembed&)

**Example 2: Single-select segmented control with icons**

Display a single-select segmented control widget with icons:

```
import streamlit as st

option_map = {
    0: ":material/add:",
    1: ":material/zoom_in:",
    2: ":material/zoom_out:",
    3: ":material/zoom_out_map:",
}
selection = st.segmented_control(
    "Tool",
    options=option_map.keys(),
    format_func=lambda option: option_map[option],
    selection_mode="single",
)
st.write(
    "Your selected option: "
    f"{None if selection is None else option_map[selection]}"
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-segmented-control-single.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.radio](/develop/api-reference/widgets/st.radio)[*arrow\_forward*Next: st.selectbox](/develop/api-reference/widgets/st.selectbox)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI