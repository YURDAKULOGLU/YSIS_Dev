st.multiselect - Streamlit Docs

## st.multiselect

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a multiselect widget.

The multiselect widget starts as empty.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/widgets/multiselect.py#L232 "View st.multiselect source code on GitHub") | |
| --- | --- |
| st.multiselect(label, options, default=None, format\_func=special\_internal\_function, key=None, help=None, on\_change=None, args=None, kwargs=None, \*, max\_selections=None, placeholder=None, disabled=False, label\_visibility="visible", accept\_new\_options=False, width="stretch") | |
| Parameters | |
| label (str) | A short label explaining to the user what this select widget is for. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Display unsupported elements as literal characters by backslash-escaping them. E.g., "1\. Not an ordered list".  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives.  For accessibility reasons, you should never set an empty label, but you can hide it with label\_visibility if needed. In the future, we may disallow empty labels by raising an exception. |
| options (Iterable) | Labels for the select options in an Iterable. This can be a list, set, or anything supported by st.dataframe. If options is dataframe-like, the first column will be used. Each label will be cast to str internally by default. |
| default (Iterable of V, V, or None) | List of default values. Can also be a single value. |
| format\_func (function) | Function to modify the display of the options. It receives the raw option as an argument and should output the label to be shown for that option. This has no impact on the return value of the command. |
| key (str or int) | An optional string or integer to use as the unique key for the widget. If this is omitted, a key will be generated for the widget based on its content. No two widgets may have the same key. |
| help (str or None) | A tooltip that gets displayed next to the widget label. Streamlit only displays the tooltip when label\_visibility="visible". If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| on\_change (callable) | An optional callback invoked when this widget's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| max\_selections (int) | The max selections that can be selected at a time. |
| placeholder (str or None) | A string to display when no options are selected. If this is None (default), the widget displays placeholder text based on the widget's configuration:   * "Choose options" is displayed when options are available and   accept\_new\_options=False. * "Choose or add options" is displayed when options are available   and accept\_new\_options=True. * "Add options" is displayed when no options are available and   accept\_new\_options=True. * "No options to select" is displayed when no options are available   and accept\_new\_options=False. The widget is also disabled in   this case. |
| disabled (bool) | An optional boolean that disables the multiselect widget if set to True. The default is False. |
| label\_visibility ("visible", "hidden", or "collapsed") | The visibility of the label. The default is "visible". If this is "hidden", Streamlit displays an empty spacer instead of the label, which can help keep the widget aligned with other widgets. If this is "collapsed", Streamlit displays no label or spacer. |
| accept\_new\_options (bool) | Whether the user can add selections that aren't included in options. If this is False (default), the user can only select from the items in options. If this is True, the user can enter new items that don't exist in options.  When a user enters and selects a new item, it is included in the widget's returned list as a string. The new item is not added to the widget's drop-down menu. Streamlit will use a case-insensitive match from options before adding a new item, and a new item can't be added if a case-insensitive match is already selected. The max\_selections argument is still enforced. |
| width ("stretch" or int) | The width of the multiselect widget. This can be one of the following:   * "stretch" (default): The width of the widget matches the   width of the parent container. * An integer specifying the width in pixels: The widget has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the widget matches the width   of the parent container. |
|  |  |
| --- | --- |
| Returns | |
| (list) | A list of the selected options.  The list contains copies of the selected options, not the originals. |

#### Examples

**Example 1: Use a basic multiselect widget**

You can declare one or more initial selections with the default
parameter.

```
import streamlit as st

options = st.multiselect(
    "What are your favorite colors?",
    ["Green", "Yellow", "Red", "Blue"],
    default=["Yellow", "Red"],
)

st.write("You selected:", options)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-multiselect.streamlit.app//?utm_medium=oembed&)

**Example 2: Let users to add new options**

To allow users to enter and select new options that aren't included in
the options list, use the accept\_new\_options parameter. To
prevent users from adding an unbounded number of new options, use the
max\_selections parameter.

```
import streamlit as st

options = st.multiselect(
    "What are your favorite cat names?",
    ["Jellybeans", "Fish Biscuit", "Madam President"],
    max_selections=5,
    accept_new_options=True,
)

st.write("You selected:", options)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-multiselect-accept-new-options.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.feedback](/develop/api-reference/widgets/st.feedback)[*arrow\_forward*Next: st.pills](/develop/api-reference/widgets/st.pills)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI