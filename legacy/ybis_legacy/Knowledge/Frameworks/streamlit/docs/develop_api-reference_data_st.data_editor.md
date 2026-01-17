st.data\_editor - Streamlit Docs

*star*

#### Tip

This page only contains information on the `st.data_editor` API. For an overview of working with dataframes and to learn more about the data editor's capabilities and limitations, read [Dataframes](/develop/concepts/design/dataframes).

## st.data\_editor

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a data editor widget.

The data editor widget allows you to edit dataframes and many other data structures in a table-like UI.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/widgets/data_editor.py#L654 "View st.data_editor source code on GitHub") | |
| --- | --- |
| st.data\_editor(data, \*, width="stretch", height="auto", use\_container\_width=None, hide\_index=None, column\_order=None, column\_config=None, num\_rows="fixed", disabled=False, key=None, on\_change=None, args=None, kwargs=None, row\_height=None, placeholder=None) | |
| Parameters | |
| data (Anything supported by st.dataframe) | The data to edit in the data editor.  Note   * Styles from pandas.Styler will only be applied to non-editable columns. * Text and number formatting from column\_config always takes   precedence over text and number formatting from pandas.Styler. * If your dataframe starts with an empty column, you should set   the column datatype in the underlying dataframe to ensure your   intended datatype, especially for integers versus floats. * Mixing data types within a column can make the column uneditable. * Additionally, the following data types are not yet supported for editing:   complex, tuple, bytes, bytearray,   memoryview, dict, set, frozenset,   fractions.Fraction, pandas.Interval, and   pandas.Period. * To prevent overflow in JavaScript, columns containing   datetime.timedelta and pandas.Timedelta values will   default to uneditable, but this can be changed through column   configuration. |
| width ("stretch", "content", or int) | The width of the data editor. This can be one of the following:   * "stretch" (default): The width of the editor matches the   width of the parent container. * "content": The width of the editor matches the width of its   content, but doesn't exceed the width of the parent container. * An integer specifying the width in pixels: The editor has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the editor matches the width   of the parent container. |
| height ("auto", "content", "stretch", or int) | The height of the data editor. This can be one of the following:   * "auto" (default): Streamlit sets the height to show at most   ten rows. * "content": The height of the editor matches the height of   its content. The height is capped at 10,000 pixels to prevent   performance issues with very large dataframes. * "stretch": The height of the editor expands to fill the   available vertical space in its parent container. When multiple   elements with stretch height are in the same container, they   share the available vertical space evenly. The editor will   maintain a minimum height to display up to three rows, but   otherwise won't exceed the available height in its parent   container. * An integer specifying the height in pixels: The editor has a   fixed height.   Vertical scrolling within the editor is enabled when the height does not accommodate all rows. |
| use\_container\_width (bool) | *delete* use\_container\_width is deprecated and will be removed in a future release. For use\_container\_width=True, use width="stretch".  Whether to override width with the width of the parent container. If this is True (default), Streamlit sets the width of the data editor to match the width of the parent container. If this is False, Streamlit sets the data editor's width according to width. |
| hide\_index (bool or None) | Whether to hide the index column(s). If hide\_index is None (default), the visibility of index columns is automatically determined based on the data. |
| column\_order (Iterable[str] or None) | The ordered list of columns to display. If this is None (default), Streamlit displays all columns in the order inherited from the underlying data structure. If this is a list, the indicated columns will display in the order they appear within the list. Columns may be omitted or repeated within the list.  For example, column\_order=("col2", "col1") will display "col2" first, followed by "col1", and will hide all other non-index columns.  column\_order does not accept positional column indices and can't move the index column(s). |
| column\_config (dict or None) | Configuration to customize how columns are displayed. If this is None (default), columns are styled based on the underlying data type of each column.  Column configuration can modify column names, visibility, type, width, format, editing properties like min/max, and more. If this is a dictionary, the keys are column names (strings) and/or positional column indices (integers), and the values are one of the following:   * None to hide the column. * A string to set the display label of the column. * One of the column types defined under st.column\_config. For   example, to show a column as dollar amounts, use   st.column\_config.NumberColumn("Dollar values", format="$ %d").   See more info on the available column types and config options   [here](https://docs.streamlit.io/develop/api-reference/data/st.column_config).   To configure the index column(s), use "\_index" as the column name, or use a positional column index where 0 refers to the first index column. |
| num\_rows ("fixed" or "dynamic") | Specifies if the user can add and delete rows in the data editor. If "fixed", the user cannot add or delete rows. If "dynamic", the user can add and delete rows in the data editor, but column sorting is disabled. Defaults to "fixed". |
| disabled (bool or Iterable[str | int]) | Controls the editing of columns. This can be one of the following:   * False (default): All columns that support editing are editable. * True: All columns are disabled for editing. * An Iterable of column names and/or positional indices: The   specified columns are disabled for editing while the remaining   columns are editable where supported. For example,   disabled=["col1", "col2"] will disable editing for the   columns named "col1" and "col2".   To disable editing for the index column(s), use "\_index" as the column name, or use a positional column index where 0 refers to the first index column. |
| key (str) | An optional string to use as the unique key for this widget. If this is omitted, a key will be generated for the widget based on its content. No two widgets may have the same key. |
| on\_change (callable) | An optional callback invoked when this data\_editor's value changes. |
| args (list or tuple) | An optional list or tuple of args to pass to the callback. |
| kwargs (dict) | An optional dict of kwargs to pass to the callback. |
| row\_height (int or None) | The height of each row in the data editor in pixels. If row\_height is None (default), Streamlit will use a default row height, which fits one line of text. |
| placeholder (str or None) | The text that should be shown for missing values. If this is None (default), missing values are displayed as "None". To leave a cell empty, use an empty string (""). Other common values are "null", "NaN" and "-". |
|  |  |
| --- | --- |
| Returns | |
| (pandas.DataFrame, pandas.Series, pyarrow.Table, numpy.ndarray, list, set, tuple, or dict.) | The edited data. The edited data is returned in its original data type if it corresponds to any of the supported return types. All other data types are returned as a pandas.DataFrame. |

#### Examples

**Example 1: Basic usage**

```
import pandas as pd
import streamlit as st

df = pd.DataFrame(
    [
        {"command": "st.selectbox", "rating": 4, "is_widget": True},
        {"command": "st.balloons", "rating": 5, "is_widget": False},
        {"command": "st.time_input", "rating": 3, "is_widget": True},
    ]
)
edited_df = st.data_editor(df)

favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-data-editor.streamlit.app//?utm_medium=oembed&)

**Example 2: Allowing users to add and delete rows**

You can allow your users to add and delete rows by setting num\_rows
to "dynamic":

```
import streamlit as st
import pandas as pd

df = pd.DataFrame(
    [
        {"command": "st.selectbox", "rating": 4, "is_widget": True},
        {"command": "st.balloons", "rating": 5, "is_widget": False},
        {"command": "st.time_input", "rating": 3, "is_widget": True},
    ]
)
edited_df = st.data_editor(df, num_rows="dynamic")

favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-data-editor1.streamlit.app//?utm_medium=oembed&)

**Example 3: Data editor configuration**

You can customize the data editor via column\_config, hide\_index,
column\_order, or disabled:

```
import pandas as pd
import streamlit as st

df = pd.DataFrame(
    [
        {"command": "st.selectbox", "rating": 4, "is_widget": True},
        {"command": "st.balloons", "rating": 5, "is_widget": False},
        {"command": "st.time_input", "rating": 3, "is_widget": True},
    ]
)
edited_df = st.data_editor(
    df,
    column_config={
        "command": "Streamlit Command",
        "rating": st.column_config.NumberColumn(
            "Your rating",
            help="How much do you like this command (1-5)?",
            min_value=1,
            max_value=5,
            step=1,
            format="%d ⭐",
        ),
        "is_widget": "Widget ?",
    },
    disabled=["command", "is_widget"],
    hide_index=True,
)

favorite_command = edited_df.loc[edited_df["rating"].idxmax()]["command"]
st.markdown(f"Your favorite command is **{favorite_command}** 🎈")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-data-editor-config.streamlit.app//?utm_medium=oembed&)

### Configuring columns

You can configure the display and editing behavior of columns in `st.dataframe` and `st.data_editor` via the [Column configuration API](/develop/api-reference/data/st.column_config). We have developed the API to let you add images, charts, and clickable URLs in dataframe and data editor columns. Additionally, you can make individual columns editable, set columns as categorical and specify which options they can take, hide the index of the dataframe, and much more.

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-column-config-overview.streamlit.app/?utm_medium=oembed&)

[*arrow\_back*Previous: st.dataframe](/develop/api-reference/data/st.dataframe)[*arrow\_forward*Next: st.column\_config](/develop/api-reference/data/st.column_config)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI