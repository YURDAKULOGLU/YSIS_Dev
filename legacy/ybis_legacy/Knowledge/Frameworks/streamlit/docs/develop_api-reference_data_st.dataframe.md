st.dataframe - Streamlit Docs

*star*

#### Tip

Learn more in our [Dataframes](/develop/concepts/design/dataframes) guide and check out our tutorial, [Get dataframe row-selections from users](/develop/tutorials/elements/dataframe-row-selections).

## st.dataframe

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a dataframe as an interactive table.

This command works with a wide variety of collection-like and
dataframe-like object types.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/arrow.py#L321 "View st.dataframe source code on GitHub") | |
| --- | --- |
| st.dataframe(data=None, width="stretch", height="auto", \*, use\_container\_width=None, hide\_index=None, column\_order=None, column\_config=None, key=None, on\_select="ignore", selection\_mode="multi-row", row\_height=None, placeholder=None) | |
| Parameters | |
| data (dataframe-like, collection-like, or None) | The data to display.  Dataframe-like objects include dataframe and series objects from popular libraries like Dask, Modin, Numpy, pandas, Polars, PyArrow, Snowpark, Xarray, and more. You can use database cursors and clients that comply with the [Python Database API Specification v2.0 (PEP 249)](https://peps.python.org/pep-0249/). Additionally, you can use anything that supports the [Python dataframe interchange protocol](https://data-apis.org/dataframe-protocol/latest/).  For example, you can use the following:   * pandas.DataFrame, pandas.Series, pandas.Index,   pandas.Styler, and pandas.Array * polars.DataFrame, polars.LazyFrame, and polars.Series * snowflake.snowpark.dataframe.DataFrame,   snowflake.snowpark.table.Table   If a data type is not recognized, Streamlit will convert the object to a pandas.DataFrame or pyarrow.Table using a .to\_pandas() or .to\_arrow() method, respectively, if available.  If data is a pandas.Styler, it will be used to style its underlying pandas.DataFrame. Streamlit supports custom cell values, colors, and font weights. It does not support some of the more exotic styling options, like bar charts, hovering, and captions. For these styling options, use column configuration instead. Text and number formatting from column\_config always takes precedence over text and number formatting from pandas.Styler.  Collection-like objects include all Python-native Collection types, such as dict, list, and set.  If data is None, Streamlit renders an empty table. |
| width ("stretch", "content", or int) | The width of the dataframe element. This can be one of the following:   * "stretch" (default): The width of the element matches the   width of the parent container. * "content": The width of the element matches the width of its   content, but doesn't exceed the width of the parent container. * An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |
| height ("auto", "content", "stretch", or int) | The height of the dataframe element. This can be one of the following:   * "auto" (default): Streamlit sets the height to show at most   ten rows. * "content": The height of the element matches the height of   its content. The height is capped at 10,000 pixels to prevent   performance issues with very large dataframes. * "stretch": The height of the element expands to fill the   available vertical space in its parent container. When multiple   elements with stretch height are in the same container, they   share the available vertical space evenly. The dataframe will   maintain a minimum height to display up to three rows, but   otherwise won't exceed the available height in its parent   container. * An integer specifying the height in pixels: The element has a   fixed height.   Vertical scrolling within the dataframe element is enabled when the height does not accommodate all rows. |
| use\_container\_width (bool) | *delete* use\_container\_width is deprecated and will be removed in a future release. For use\_container\_width=True, use width="stretch".  Whether to override width with the width of the parent container. If this is True (default), Streamlit sets the width of the dataframe to match the width of the parent container. If this is False, Streamlit sets the dataframe's width according to width. |
| hide\_index (bool or None) | Whether to hide the index column(s). If hide\_index is None (default), the visibility of index columns is automatically determined based on the data and other configurations. |
| column\_order (Iterable[str] or None) | The ordered list of columns to display. If this is None (default), Streamlit displays all columns in the order inherited from the underlying data structure. If this is a list, the indicated columns will display in the order they appear within the list. Columns may be omitted or repeated within the list.  For example, column\_order=("col2", "col1") will display "col2" first, followed by "col1", and will hide all other non-index columns.  column\_order does not accept positional column indices and can't move the index column(s). |
| column\_config (dict or None) | Configuration to customize how columns are displayed. If this is None (default), columns are styled based on the underlying data type of each column.  Column configuration can modify column names, visibility, type, width, format, and more. If this is a dictionary, the keys are column names (strings) and/or positional column indices (integers), and the values are one of the following:   * None to hide the column. * A string to set the display label of the column. * One of the column types defined under st.column\_config. For   example, to show a column as dollar amounts, use   st.column\_config.NumberColumn("Dollar values", format="$ %d").   See more info on the available column types and config options   [here](https://docs.streamlit.io/develop/api-reference/data/st.column_config).   To configure the index column(s), use "\_index" as the column name, or use a positional column index where 0 refers to the first index column. |
| key (str) | An optional string to use for giving this element a stable identity. If key is None (default), this element's identity will be determined based on the values of the other parameters.  Additionally, if selections are activated and key is provided, Streamlit will register the key in Session State to store the selection state. The selection state is read-only. |
| on\_select ("ignore" or "rerun" or callable) | How the dataframe should respond to user selection events. This controls whether or not the dataframe behaves like an input widget. on\_select can be one of the following:   * "ignore" (default): Streamlit will not react to any selection   events in the dataframe. The dataframe will not behave like an   input widget. * "rerun": Streamlit will rerun the app when the user selects   rows, columns, or cells in the dataframe. In this case,   st.dataframe will return the selection data as a dictionary. * A callable: Streamlit will rerun the app and execute the   callable as a callback function before the rest of the app.   In this case, st.dataframe will return the selection data   as a dictionary. |
| selection\_mode ("single-row", "multi-row", "single-column", "multi-column", "single-cell", "multi-cell", or Iterable of these) | The types of selections Streamlit should allow when selections are enabled with on\_select. This can be one of the following:   * "multi-row" (default): Multiple rows can be selected at a time. * "single-row": Only one row can be selected at a time. * "multi-column": Multiple columns can be selected at a time. * "single-column": Only one column can be selected at a time. * "multi-cell": A rectangular range of cells can be selected. * "single-cell": Only one cell can be selected at a time. * An Iterable of the above options: The table will allow   selection based on the modes specified. For example, to allow the   user to select multiple rows and multiple cells, use   ["multi-row", "multi-cell"].   When column selections are enabled, column sorting is disabled. |
| row\_height (int or None) | The height of each row in the dataframe in pixels. If row\_height is None (default), Streamlit will use a default row height, which fits one line of text. |
| placeholder (str or None) | The text that should be shown for missing values. If this is None (default), missing values are displayed as "None". To leave a cell empty, use an empty string (""). Other common values are "null", "NaN" and "-". |
|  |  |
| --- | --- |
| Returns | |
| (element or dict) | If on\_select is "ignore" (default), this command returns an internal placeholder for the dataframe element that can be used with the .add\_rows() method. Otherwise, this command returns a dictionary-like object that supports both key and attribute notation. The attributes are described by the DataframeState dictionary schema. |

#### Examples

**Example 1: Display a dataframe**

```
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(
    rng(0).standard_normal((50, 20)), columns=("col %d" % i for i in range(20))
)

st.dataframe(df)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-dataframe.streamlit.app//?utm_medium=oembed&)

**Example 2: Use Pandas Styler**

You can also pass a Pandas Styler object to change the style of
the rendered DataFrame:

```
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(
    rng(0).standard_normal((10, 20)), columns=("col %d" % i for i in range(20))
)

st.dataframe(df.style.highlight_max(axis=0))
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-dataframe1.streamlit.app//?utm_medium=oembed&)

**Example 3: Use column configuration**

You can customize a dataframe via column\_config, hide\_index, or column\_order.

```
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(
    {
        "name": ["Roadmap", "Extras", "Issues"],
        "url": [
            "https://roadmap.streamlit.app",
            "https://extras.streamlit.app",
            "https://issues.streamlit.app",
        ],
        "stars": rng(0).integers(0, 1000, size=3),
        "views_history": rng(0).integers(0, 5000, size=(3, 30)).tolist(),
    }
)

st.dataframe(
    df,
    column_config={
        "name": "App name",
        "stars": st.column_config.NumberColumn(
            "Github Stars",
            help="Number of stars on GitHub",
            format="%d ⭐",
        ),
        "url": st.column_config.LinkColumn("App URL"),
        "views_history": st.column_config.LineChartColumn(
            "Views (past 30 days)", y_min=0, y_max=5000
        ),
    },
    hide_index=True,
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-dataframe-config.streamlit.app//?utm_medium=oembed&)

**Example 4: Customize your index**

You can use column configuration to format your index.

```
from datetime import datetime, date
import numpy as np
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    year = datetime.now().year
    df = pd.DataFrame(
        {
            "Date": [date(year, month, 1) for month in range(1, 4)],
            "Total": np.random.randint(1000, 5000, size=3),
        }
    )
    df.set_index("Date", inplace=True)
    return df

df = load_data()
config = {
    "_index": st.column_config.DateColumn("Month", format="MMM YYYY"),
    "Total": st.column_config.NumberColumn("Total ($)"),
}

st.dataframe(df, column_config=config)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-dataframe-config-index.streamlit.app//?utm_medium=oembed&)

## Dataframe selections

### DataframeState

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

The schema for the dataframe event state.

The event state is stored in a dictionary-like object that supports both
key and attribute notation. Event states cannot be programmatically
changed or set through Session State.

Only selection events are supported at this time.

|  |  |
| --- | --- |
| Attributes | |
| selection (dict) | The state of the on\_select event. This attribute returns a dictionary-like object that supports both key and attribute notation. The attributes are described by the DataframeSelectionState dictionary schema. |

### DataframeSelectionState

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

The schema for the dataframe selection state.

The selection state is stored in a dictionary-like object that supports both
key and attribute notation. Selection states cannot be programmatically
changed or set through Session State.

Warning

If a user sorts a dataframe, row selections will be reset. If your
users need to sort and filter the dataframe to make selections, direct
them to use the search function in the dataframe toolbar instead.

|  |  |
| --- | --- |
| Attributes | |
| rows (list[int]) | The selected rows, identified by their integer position. The integer positions match the original dataframe, even if the user sorts the dataframe in their browser. For a pandas.DataFrame, you can retrieve data from its integer position using methods like .iloc[] or .iat[]. |
| columns (list[str]) | The selected columns, identified by their names. |
| cells (list[tuple[int, str]]) | The selected cells, provided as a tuple of row integer position and column name. For example, the first cell in a column named "col 1" is represented as (0, "col 1"). Cells within index columns are not returned. |

#### Example

The following example has multi-row and multi-column selections enabled.
Try selecting some rows. To select multiple columns, hold CMD (macOS)
or Ctrl (Windows) while selecting columns. Hold Shift to select a
range of columns.

```
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(
    rng(0).standard_normal((12, 5)), columns=["a", "b", "c", "d", "e"]
)

event = st.dataframe(
    df,
    key="data",
    on_select="rerun",
    selection_mode=["multi-row", "multi-column", "multi-cell"],
)

event.selection
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-dataframe-events-selection-state.streamlit.app//?utm_medium=oembed&)

## element.add\_rows

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

*delete*

#### Deprecation notice

We plan to deprecate `.add_rows()`. Please leave [feedback](https://github.com/streamlit/streamlit/issues/13063).

Concatenate a dataframe to the bottom of the current one.

Important

add\_rows is deprecated and might be removed in a future version.
If you have a specific use-case that requires the add\_rows
functionality, please tell us via this
[issue on Github](<https://github.com/streamlit/streamlit/issues/13063>).

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/arrow.py#L910 "View st.add_rows source code on GitHub") | |
| --- | --- |
| element.add\_rows(data=None, \*\*kwargs) | |
| Parameters | |
| data (pandas.DataFrame, pandas.Styler, pyarrow.Table, numpy.ndarray, pyspark.sql.DataFrame, snowflake.snowpark.dataframe.DataFrame, Iterable, dict, or None) | Table to concat. Optional. |
| \*\*kwargs (pandas.DataFrame, numpy.ndarray, Iterable, dict, or None) | The named dataset to concat. Optional. You can only pass in 1 dataset (including the one in the data parameter). |

#### Example

```
import time
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df1 = pd.DataFrame(
    rng(0).standard_normal(size=(50, 20)), columns=("col %d" % i for i in range(20))
)

df2 = pd.DataFrame(
    rng(1).standard_normal(size=(50, 20)), columns=("col %d" % i for i in range(20))
)

my_table = st.table(df1)
time.sleep(1)
my_table.add_rows(df2)
```

You can do the same thing with plots. For example, if you want to add
more data to a line chart:

```
# Assuming df1 and df2 from the example above still exist...
my_chart = st.line_chart(df1)
time.sleep(1)
my_chart.add_rows(df2)
```

And for plots whose datasets are named, you can pass the data with a
keyword argument where the key is the name:

```
my_chart = st.vega_lite_chart(
    {
        "mark": "line",
        "encoding": {"x": "a", "y": "b"},
        "datasets": {
            "some_fancy_name": df1,  # <-- named dataset
        },
        "data": {"name": "some_fancy_name"},
    }
)
my_chart.add_rows(some_fancy_name=df2)  # <-- name used as keyword
```

## Interactivity

Dataframes displayed with `st.dataframe` are interactive. End users can sort, resize, search, and copy data to their clipboard. For on overview of features, read our [Dataframes](/develop/concepts/design/dataframes#additional-ui-features) guide.

## Configuring columns

You can configure the display and editing behavior of columns in `st.dataframe` and `st.data_editor` via the [Column configuration API](/develop/api-reference/data/st.column_config). We have developed the API to let you add images, charts, and clickable URLs in dataframe and data editor columns. Additionally, you can make individual columns editable, set columns as categorical and specify which options they can take, hide the index of the dataframe, and much more.

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-column-config-overview.streamlit.app/?utm_medium=oembed&)

[*arrow\_back*Previous: Data elements](/develop/api-reference/data)[*arrow\_forward*Next: st.data\_editor](/develop/api-reference/data/st.data_editor)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI