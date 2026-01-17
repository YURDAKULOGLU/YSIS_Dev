st.time\_input - Streamlit Docs

## st.time\_input

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a time input widget.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/widgets/time_widgets.py#L540 "View st.time_input source code on GitHub") | |
| --- | --- |
| st.time\_input(label, value="now", key=None, help=None, on\_change=None, args=None, kwargs=None, \*, disabled=False, label\_visibility="visible", step=0:15:00, width="stretch") | |
| Parameters | |
| label (str) | A short label explaining to the user what this time input is for. The label can optionally contain GitHub-flavored Markdown of the following types: Bold, Italics, Strikethroughs, Inline Code, Links, and Images. Images display like icons, with a max height equal to the font height.  Unsupported Markdown elements are unwrapped so only their children (text contents) render. Display unsupported elements as literal characters by backslash-escaping them. E.g., "1\. Not an ordered list".  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives.  For accessibility reasons, you should never set an empty label, but you can hide it with label\_visibility if needed. In the future, we may disallow empty labels by raising an exception. |
| value ("now", datetime.time, datetime.datetime, str, or None) | The value of this widget when it first renders. This can be one of the following:   * "now" (default): The widget initializes with the current time. * A datetime.time or datetime.datetime object: The widget   initializes with the given time, ignoring any date if included. * An ISO-formatted time (hh:mm[:ss.sss]) or datetime   (YYYY-MM-DD hh:mm[:ss]) string: The widget initializes with the   given time, ignoring any date if included. * None: The widget initializes with no time and returns   None until the user selects a time. |
| key (str or int) | An optional string or integer to use as the unique key for the widget. If this is omitted, a key will be generated for the widget based on its content. No two widgets may have the same key. |
| help (str or None) | A tooltip that gets displayed next to the widget label. Streamlit only displays the tooltip when label\_visibility="visible". If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| on\_change (callable) | An optional callback invoked when this time\_input's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| disabled (bool) | An optional boolean that disables the time input if set to True. The default is False. |
| label\_visibility ("visible", "hidden", or "collapsed") | The visibility of the label. The default is "visible". If this is "hidden", Streamlit displays an empty spacer instead of the label, which can help keep the widget aligned with other widgets. If this is "collapsed", Streamlit displays no label or spacer. |
| step (int or timedelta) | The stepping interval in seconds. This defaults to 900 (15 minutes). You can also pass a datetime.timedelta object. The value must be between 60 seconds and 23 hours. |
| width ("stretch" or int) | The width of the time input widget. This can be one of the following:   * "stretch" (default): The width of the widget matches the   width of the parent container. * An integer specifying the width in pixels: The widget has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the widget matches the width   of the parent container. |
|  |  |
| --- | --- |
| Returns | |
| (datetime.time or None) | The current value of the time input widget or None if no time has been selected. |

#### Example

**Example 1: Basic usage**

```
import datetime
import streamlit as st

t = st.time_input("Set an alarm for", datetime.time(8, 45))
st.write("Alarm is set for", t)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-time-input.streamlit.app//?utm_medium=oembed&)

**Example 2: Empty initial value**

To initialize an empty time input, use None as the value:

```
import datetime
import streamlit as st

t = st.time_input("Set an alarm for", value=None)
st.write("Alarm is set for", t)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-time-input-empty.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.datetime\_input](/develop/api-reference/widgets/st.datetime_input)[*arrow\_forward*Next: st.chat\_input](https://docs.streamlit.io/develop/api-reference/chat/st.chat_input)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI