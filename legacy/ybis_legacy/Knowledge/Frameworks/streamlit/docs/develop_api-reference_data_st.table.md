st.table - Streamlit Docs

*star*

#### Tip

Static tables with `st.table` are the most basic way to display dataframes. For the majority of cases, we recommend using [`st.dataframe`](/develop/api-reference/data/st.dataframe) to display interactive dataframes, and [`st.data_editor`](/develop/api-reference/data/st.data_editor) to let users edit dataframes.

## st.table

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a static table.

While st.dataframe is geared towards large datasets and interactive
data exploration, st.table is useful for displaying small, styled
tables without sorting or scrolling. For example, st.table may be
the preferred way to display a confusion matrix or leaderboard.
Additionally, st.table supports Markdown.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/arrow.py#L801 "View st.table source code on GitHub") | |
| --- | --- |
| st.table(data=None, \*, border=True) | |
| Parameters | |
| data (Anything supported by st.dataframe) | The table data.  All cells including the index and column headers can optionally contain GitHub-flavored Markdown. Syntax information can be found at: <https://github.github.com/gfm>.  See the body parameter of [st.markdown](https://docs.streamlit.io/develop/api-reference/text/st.markdown) for additional, supported Markdown directives. |
| border (bool or "horizontal") | Whether to show borders around the table and between cells. This can be one of the following:   * True (default): Show borders around the table and between cells. * False: Don't show any borders. * "horizontal": Show only horizontal borders between rows. |

#### Examples

**Example 1: Display a confusion matrix as a static table**

```
import pandas as pd
import streamlit as st

confusion_matrix = pd.DataFrame(
    {
        "Predicted Cat": [85, 3, 2, 1],
        "Predicted Dog": [2, 78, 4, 0],
        "Predicted Bird": [1, 5, 72, 3],
        "Predicted Fish": [0, 2, 1, 89],
    },
    index=["Actual Cat", "Actual Dog", "Actual Bird", "Actual Fish"],
)
st.table(confusion_matrix)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-table-confusion.streamlit.app//?utm_medium=oembed&)

**Example 2: Display a product leaderboard with Markdown and horizontal borders**

```
import streamlit as st

product_data = {
    "Product": [
        ":material/devices: Widget Pro",
        ":material/smart_toy: Smart Device",
        ":material/inventory: Premium Kit",
    ],
    "Category": [":blue[Electronics]", ":green[IoT]", ":violet[Bundle]"],
    "Stock": ["🟢 Full", "🟡 Low", "🔴 Empty"],
    "Units sold": [1247, 892, 654],
    "Revenue": [125000, 89000, 98000],
}
st.table(product_data, border="horizontal")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-table-horizontal-border.streamlit.app//?utm_medium=oembed&)

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

[*arrow\_back*Previous: st.column\_config](/develop/api-reference/data/st.column_config)[*arrow\_forward*Next: st.metric](/develop/api-reference/data/st.metric)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI