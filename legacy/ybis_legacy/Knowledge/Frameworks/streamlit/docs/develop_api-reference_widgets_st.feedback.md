st.feedback - Streamlit Docs

## st.feedback

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a feedback widget.

A feedback widget is an icon-based button group available in three
styles, as described in options. It is commonly used in chat and AI
apps to allow users to rate responses.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/widgets/button_group.py#L298 "View st.feedback source code on GitHub") | |
| --- | --- |
| st.feedback(options="thumbs", \*, key=None, default=None, disabled=False, on\_change=None, args=None, kwargs=None, width="content") | |
| Parameters | |
| options ("thumbs", "faces", or "stars") | The feedback options displayed to the user. options can be one of the following:   * "thumbs" (default): Streamlit displays a thumb-up and   thumb-down button group. * "faces": Streamlit displays a row of five buttons with   facial expressions depicting increasing satisfaction from left to   right. * "stars": Streamlit displays a row of star icons, allowing the   user to select a rating from one to five stars. |
| key (str or int) | An optional string or integer to use as the unique key for the widget. If this is omitted, a key will be generated for the widget based on its content. No two widgets may have the same key. |
| default (int or None) | Default feedback value. This must be consistent with the feedback type in options:   * 0 or 1 if options="thumbs". * Between 0 and 4, inclusive, if options="faces" or   options="stars". |
| disabled (bool) | An optional boolean that disables the feedback widget if set to True. The default is False. |
| on\_change (callable) | An optional callback invoked when this feedback widget's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| width ("content", "stretch", or int) | The width of the feedback widget. This can be one of the following:   * "content" (default): The width of the widget matches the   width of its content, but doesn't exceed the width of the parent   container. * "stretch": The width of the widget matches the width of the   parent container. * An integer specifying the width in pixels: The widget has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the widget matches the width   of the parent container. |
|  |  |
| --- | --- |
| Returns | |
| (int or None) | An integer indicating the user's selection, where 0 is the lowest feedback. Higher values indicate more positive feedback. If no option was selected, the widget returns None.   * For options="thumbs", a return value of 0 indicates   thumbs-down, and 1 indicates thumbs-up. * For options="faces" and options="stars", return values   range from 0 (least satisfied) to 4 (most satisfied). |

#### Examples

Display a feedback widget with stars, and show the selected sentiment:

```
import streamlit as st

sentiment_mapping = ["one", "two", "three", "four", "five"]
selected = st.feedback("stars")
if selected is not None:
    st.markdown(f"You selected {sentiment_mapping[selected]} star(s).")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-feedback-stars.streamlit.app//?utm_medium=oembed&)

Display a feedback widget with thumbs, and show the selected sentiment:

```
import streamlit as st

sentiment_mapping = [":material/thumb_down:", ":material/thumb_up:"]
selected = st.feedback("thumbs")
if selected is not None:
    st.markdown(f"You selected: {sentiment_mapping[selected]}")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-feedback-thumbs.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.color\_picker](/develop/api-reference/widgets/st.color_picker)[*arrow\_forward*Next: st.multiselect](/develop/api-reference/widgets/st.multiselect)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI