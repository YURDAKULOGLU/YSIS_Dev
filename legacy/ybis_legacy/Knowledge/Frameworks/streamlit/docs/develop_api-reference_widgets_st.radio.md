st.radio - Streamlit Docs

## st.radio

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a radio button widget.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/widgets/radio.py#L150 "View st.radio source code on GitHub") | |
| --- | --- |
| st.radio(label, options, index=0, format\_func=special\_internal\_function, key=None, help=None, on\_change=None, args=None, kwargs=None, \*, disabled=False, horizontal=False, captions=None, label\_visibility="visible", width="content") | |
| Parameters | |
| label (str) | A short label explaining to the user what this radio group is for. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Display unsupported elements as literal characters by backslash-escaping them. E.g., "1\. Not an ordered list".  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives.  For accessibility reasons, you should never set an empty label, but you can hide it with label\_visibility if needed. In the future, we may disallow empty labels by raising an exception. |
| options (Iterable) | Labels for the select options in an Iterable. This can be a list, set, or anything supported by st.dataframe. If options is dataframe-like, the first column will be used. Each label will be cast to str internally by default.  Labels can include markdown as described in the label parameter and will be cast to str internally by default. |
| index (int or None) | The index of the preselected option on first render. If None, will initialize empty and return None until the user selects an option. Defaults to 0 (the first option). |
| format\_func (function) | Function to modify the display of radio options. It receives the raw option as an argument and should output the label to be shown for that option. This has no impact on the return value of the radio. |
| key (str or int) | An optional string or integer to use as the unique key for the widget. If this is omitted, a key will be generated for the widget based on its content. No two widgets may have the same key. |
| help (str or None) | A tooltip that gets displayed next to the widget label. Streamlit only displays the tooltip when label\_visibility="visible". If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| on\_change (callable) | An optional callback invoked when this radio's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| disabled (bool) | An optional boolean that disables the radio button if set to True. The default is False. |
| horizontal (bool) | An optional boolean, which orients the radio group horizontally. The default is false (vertical buttons). |
| captions (iterable of str or None) | A list of captions to show below each radio button. If None (default), no captions are shown. |
| label\_visibility ("visible", "hidden", or "collapsed") | The visibility of the label. The default is "visible". If this is "hidden", Streamlit displays an empty spacer instead of the label, which can help keep the widget aligned with other widgets. If this is "collapsed", Streamlit displays no label or spacer. |
| width ("content", "stretch", or int) | The width of the radio button widget. This can be one of the following:   * "content" (default): The width of the widget matches the   width of its content, but doesn't exceed the width of the parent   container. * "stretch": The width of the widget matches the width of the   parent container. * An integer specifying the width in pixels: The widget has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the widget matches the width   of the parent container. |
|  |  |
| --- | --- |
| Returns | |
| (any) | The selected option or None if no option is selected.  This is a copy of the selected option, not the original. |

#### Example

```
import streamlit as st

genre = st.radio(
    "What's your favorite movie genre",
    [":rainbow[Comedy]", "***Drama***", "Documentary :movie_camera:"],
    captions=[
        "Laugh out loud.",
        "Get the popcorn.",
        "Never stop learning.",
    ],
)

if genre == ":rainbow[Comedy]":
    st.write("You selected comedy.")
else:
    st.write("You didn't select comedy.")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-radio.streamlit.app//?utm_medium=oembed&)

To initialize an empty radio widget, use None as the index value:

```
import streamlit as st

genre = st.radio(
    "What's your favorite movie genre",
    [":rainbow[Comedy]", "***Drama***", "Documentary :movie_camera:"],
    index=None,
)

st.write("You selected:", genre)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-radio-empty.streamlit.app//?utm_medium=oembed&)

  

Widgets can customize how to hide their labels with the `label_visibility` parameter. If "hidden", the label doesn’t show but there is still empty space for it above the widget (equivalent to `label=""`). If "collapsed", both the label and the space are removed. Default is "visible". Radio buttons can also be disabled with the `disabled` parameter, and oriented horizontally with the `horizontal` parameter:

`import streamlit as st
# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
st.session_state.visibility = "visible"
st.session_state.disabled = False
st.session_state.horizontal = False
col1, col2 = st.columns(2)
with col1:
st.checkbox("Disable radio widget", key="disabled")
st.checkbox("Orient radio options horizontally", key="horizontal")
with col2:
st.radio(
"Set label visibility 👇",
["visible", "hidden", "collapsed"],
key="visibility",
label_visibility=st.session_state.visibility,
disabled=st.session_state.disabled,
horizontal=st.session_state.horizontal,
)`

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-radio1.streamlit.app/?utm_medium=oembed)

### Featured videos

Check out our video on how to use one of Streamlit's core functions, the radio button! 🔘

In the video below, we'll take it a step further and learn how to combine a [button](/develop/api-reference/widgets/st.button), [checkbox](/develop/api-reference/widgets/st.checkbox) and radio button!

[*arrow\_back*Previous: st.pills](/develop/api-reference/widgets/st.pills)[*arrow\_forward*Next: st.segmented\_control](/develop/api-reference/widgets/st.segmented_control)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI