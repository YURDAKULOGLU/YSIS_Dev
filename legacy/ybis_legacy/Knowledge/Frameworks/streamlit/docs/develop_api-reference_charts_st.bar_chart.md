st.bar\_chart - Streamlit Docs

## st.bar\_chart

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a bar chart.

This is syntax-sugar around st.altair\_chart. The main difference
is this command uses the data's own column and indices to figure out
the chart's Altair spec. As a result this is easier to use for many
"just plot this" scenarios, while being less customizable.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/vega_charts.py#L1132 "View st.bar_chart source code on GitHub") | |
| --- | --- |
| st.bar\_chart(data=None, \*, x=None, y=None, x\_label=None, y\_label=None, color=None, horizontal=False, sort=True, stack=None, width="stretch", height="content", use\_container\_width=None) | |
| Parameters | |
| data (Anything supported by st.dataframe) | Data to be plotted. |
| x (str or None) | Column name or key associated to the x-axis data. If x is None (default), Streamlit uses the data index for the x-axis values. |
| y (str, Sequence of str, or None) | Column name(s) or key(s) associated to the y-axis data. If this is None (default), Streamlit draws the data of all remaining columns as data series. If this is a Sequence of strings, Streamlit draws several series on the same chart by melting your wide-format table into a long-format table behind the scenes. |
| x\_label (str or None) | The label for the x-axis. If this is None (default), Streamlit will use the column name specified in x if available, or else no label will be displayed. |
| y\_label (str or None) | The label for the y-axis. If this is None (default), Streamlit will use the column name(s) specified in y if available, or else no label will be displayed. |
| color (str, tuple, Sequence of str, Sequence of tuple, or None) | The color to use for different series in this chart.  For a bar chart with just one series, this can be:   * None, to use the default color. * A hex string like "#ffaa00" or "#ffaa0088". * An RGB or RGBA tuple with the red, green, blue, and alpha   components specified as ints from 0 to 255 or floats from 0.0 to   1.0.   For a bar chart with multiple series, where the dataframe is in long format (that is, y is None or just one column), this can be:   * None, to use the default colors. * The name of a column in the dataset. Data points will be grouped   into series of the same color based on the value of this column.   In addition, if the values in this column match one of the color   formats above (hex string or color tuple), then that color will   be used.  For example: if the dataset has 1000 rows, but this column only   contains the values "adult", "child", and "baby", then those 1000   datapoints will be grouped into three series whose colors will be   automatically selected from the default palette.  But, if for the same 1000-row dataset, this column contained   the values "#ffaa00", "#f0f", "#0000ff", then then those 1000   datapoints would still be grouped into 3 series, but their   colors would be "#ffaa00", "#f0f", "#0000ff" this time around.   For a bar chart with multiple series, where the dataframe is in wide format (that is, y is a Sequence of columns), this can be:   * None, to use the default colors. * A list of string colors or color tuples to be used for each of   the series in the chart. This list should have the same length   as the number of y values (e.g. color=["#fd0", "#f0f", "#04f"]   for three lines).   You can set the default colors in the theme.chartCategoryColors configuration option. |
| horizontal (bool) | Whether to make the bars horizontal. If this is False (default), the bars display vertically. If this is True, Streamlit swaps the x-axis and y-axis and the bars display horizontally. |
| sort (bool or str) | How to sort the bars. This can be one of the following:   * True (default): The bars are sorted automatically along the   independent/categorical axis with Altair's default sorting. This   also correctly sorts ordered categorical columns   (pd.Categorical). * False: The bars are shown in data order without sorting. * The name of a column (e.g. "col1"): The bars are sorted by   that column in ascending order. * The name of a column with a minus-sign prefix (e.g. "-col1"):   The bars are sorted by that column in descending order. |
| stack (bool, "normalize", "center", "layered", or None) | Whether to stack the bars. If this is None (default), Streamlit uses Vega's default. Other values can be as follows:   * True: The bars form a non-overlapping, additive stack within   the chart. * False: The bars display side by side. * "layered": The bars overlap each other without stacking. * "normalize": The bars are stacked and the total height is   normalized to 100% of the height of the chart. * "center": The bars are stacked and shifted to center the   total height around an axis. |
| width ("stretch", "content", or int) | The width of the chart element. This can be one of the following:   * "stretch" (default): The width of the element matches the   width of the parent container. * "content": The width of the element matches the width of its   content, but doesn't exceed the width of the parent container. * An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |
| height ("stretch", "content", or int) | The height of the chart element. This can be one of the following:   * "content" (default): The height of the element matches the   height of its content. * "stretch": The height of the element matches the height of   its content or the height of the parent container, whichever is   larger. If the element is not in a parent container, the height   of the element matches the height of its content. * An integer specifying the height in pixels: The element has a   fixed height. If the content is larger than the specified   height, scrolling is enabled. |
| use\_container\_width (bool or None) | *delete* use\_container\_width is deprecated and will be removed in a future release. For use\_container\_width=True, use width="stretch".  Whether to override the chart's native width with the width of the parent container. This can be one of the following:   * None (default): Streamlit will use the chart's default behavior. * True: Streamlit sets the width of the chart to match the   width of the parent container. * False: Streamlit sets the width of the chart to fit its   contents according to the plotting library, up to the width of   the parent container. |

#### Examples

**Example 1: Basic bar chart from a dataframe**

If you don't use any of the optional parameters, Streamlit plots each
column as a series of bars, uses the index as the x values, and labels
each series with the column name:

```
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=["a", "b", "c"])

st.bar_chart(df)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-bar-chart.streamlit.app//?utm_medium=oembed&)

**Example 2: Bar chart from specific dataframe columns**

You can choose different columns to use for the x and y values. If your
dataframe is in long format (all y-values in one column), you can set
the bar colors from another column.

If the column contains color strings, the colors will be applied
directly and the series will be unlabeled. If the column contains other
values, those values will label each series, and the bar colors will be
selected from the default color palette. You can configure this color
palette in the theme.chartCategoryColors configuration option.

```
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(
    {
        "col1": list(range(20)) * 3,
        "col2": rng(0).standard_normal(60),
        "col3": ["a"] * 20 + ["b"] * 20 + ["c"] * 20,
    }
)

st.bar_chart(df, x="col1", y="col2", color="col3")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-bar-chart1.streamlit.app//?utm_medium=oembed&)

**Example 3: Bar chart from wide-format dataframe**

If your dataframe is in wide format (y-values are in multiple columns),
you can pass a list of columns to the y parameter. Each column
name becomes a series label. To override the default colors, pass a
list of colors to the color parameter, one for each series:

```
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(
    {
        "col1": list(range(20)),
        "col2": rng(0).standard_normal(20),
        "col3": rng(1).standard_normal(20),
    }
)

st.bar_chart(
    df,
    x="col1",
    y=["col2", "col3"],
    color=["#FF0000", "#0000FF"],
)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-bar-chart2.streamlit.app//?utm_medium=oembed&)

**Example 4: Horizontal bar chart**

You can use the horizontal parameter to display horizontal bars
instead of vertical bars. This is useful when you have long labels on
the x-axis, or when you want to display a large number of categories.
This example requires vega\_datasets to be installed.

```
import streamlit as st
from vega_datasets import data

source = data.barley()

st.bar_chart(source, x="variety", y="yield", color="site", horizontal=True)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-bar-chart-horizontal.streamlit.app//?utm_medium=oembed&)

**Example 5: Unstacked bar chart**

You can configure the stacking behavior of the bars by setting the
stack parameter. Set it to False to display bars side by side.
This example requires vega\_datasets to be installed.

```
import streamlit as st
from vega_datasets import data

source = data.barley()

st.bar_chart(source, x="year", y="yield", color="site", stack=False)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-bar-chart-unstacked.streamlit.app//?utm_medium=oembed&)

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

[*arrow\_back*Previous: st.area\_chart](/develop/api-reference/charts/st.area_chart)[*arrow\_forward*Next: st.line\_chart](/develop/api-reference/charts/st.line_chart)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI