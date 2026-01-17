st.altair\_chart - Streamlit Docs

## st.altair\_chart

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a chart using the Vega-Altair library.

[Vega-Altair](https://altair-viz.github.io/) is a declarative
statistical visualization library for Python, based on Vega and
Vega-Lite.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/vega_charts.py#L1738 "View st.altair_chart source code on GitHub") | |
| --- | --- |
| st.altair\_chart(altair\_chart, \*, width=None, height="content", use\_container\_width=None, theme="streamlit", key=None, on\_select="ignore", selection\_mode=None) | |
| Parameters | |
| altair\_chart (altair.Chart) | The Altair chart object to display. See <https://altair-viz.github.io/gallery/> for examples of graph descriptions. |
| width ("stretch", "content", int, or None) | The width of the chart element. This can be one of the following:   * "stretch": The width of the element matches the width of the   parent container. * "content": The width of the element matches the width of its   content, but doesn't exceed the width of the parent container. * An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. * None (default): Streamlit uses "stretch" for most charts,   and uses "content" for the following multi-view charts:  + Facet charts: the spec contains "facet" or encodings for     "row", "column", or "facet".   + Horizontal concatenation charts: the spec contains     "hconcat".   + Repeat charts: the spec contains "repeat". |
| height ("content", "stretch", or int) | The height of the chart element. This can be one of the following:   * "content" (default): The height of the element matches the   height of its content. * "stretch": The height of the element matches the height of   its content or the height of the parent container, whichever is   larger. If the element is not in a parent container, the height   of the element matches the height of its content. * An integer specifying the height in pixels: The element has a   fixed height. If the content is larger than the specified   height, scrolling is enabled. |
| use\_container\_width (bool or None) | *delete* use\_container\_width is deprecated and will be removed in a future release. For use\_container\_width=True, use width="stretch".  Whether to override the chart's native width with the width of the parent container. This can be one of the following:   * None (default): Streamlit will use the parent container's   width for all charts except those with known incompatibility   (altair.Facet, altair.HConcatChart, and   altair.RepeatChart). * True: Streamlit sets the width of the chart to match the   width of the parent container. * False: Streamlit sets the width of the chart to fit its   contents according to the plotting library, up to the width of   the parent container. |
| theme ("streamlit" or None) | The theme of the chart. If theme is "streamlit" (default), Streamlit uses its own design default. If theme is None, Streamlit falls back to the default behavior of the library.  The "streamlit" theme can be partially customized through the configuration options theme.chartCategoricalColors and theme.chartSequentialColors. Font configuration options are also applied. |
| key (str) | An optional string to use for giving this element a stable identity. If key is None (default), this element's identity will be determined based on the values of the other parameters.  Additionally, if selections are activated and key is provided, Streamlit will register the key in Session State to store the selection state. The selection state is read-only. |
| on\_select ("ignore", "rerun", or callable) | How the figure should respond to user selection events. This controls whether or not the figure behaves like an input widget. on\_select can be one of the following:   * "ignore" (default): Streamlit will not react to any selection   events in the chart. The figure will not behave like an input   widget. * "rerun": Streamlit will rerun the app when the user selects   data in the chart. In this case, st.altair\_chart will return   the selection data as a dictionary. * A callable: Streamlit will rerun the app and execute the   callable as a callback function before the rest of the app.   In this case, st.altair\_chart will return the selection data   as a dictionary.   To use selection events, the object passed to altair\_chart must include selection parameters. To learn about defining interactions in Altair and how to declare selection-type parameters, see [Interactive Charts](https://altair-viz.github.io/user_guide/interactions.html) in Altair's documentation. |
| selection\_mode (str or Iterable of str) | The selection parameters Streamlit should use. If selection\_mode is None (default), Streamlit will use all selection parameters defined in the chart's Altair spec.  When Streamlit uses a selection parameter, selections from that parameter will trigger a rerun and be included in the selection state. When Streamlit does not use a selection parameter, selections from that parameter will not trigger a rerun and not be included in the selection state.  Selection parameters are identified by their name property. |
|  |  |
| --- | --- |
| Returns | |
| (element or dict) | If on\_select is "ignore" (default), this command returns an internal placeholder for the chart element that can be used with the .add\_rows() method. Otherwise, this command returns a dictionary-like object that supports both key and attribute notation. The attributes are described by the VegaLiteState dictionary schema. |

#### Example

```
import altair as alt
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(rng(0).standard_normal((60, 3)), columns=["a", "b", "c"])

chart = (
    alt.Chart(df)
    .mark_circle()
    .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
)

st.altair_chart(chart)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-vega-lite-chart.streamlit.app//?utm_medium=oembed&)

## Chart selections

### VegaLiteState

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

The schema for the Vega-Lite event state.

The event state is stored in a dictionary-like object that supports both
key and attribute notation. Event states cannot be programmatically
changed or set through Session State.

Only selection events are supported at this time.

|  |  |
| --- | --- |
| Attributes | |
| selection (dict) | The state of the on\_select event. This attribute returns a dictionary-like object that supports both key and attribute notation. The name of each Vega-Lite selection parameter becomes an attribute in the selection dictionary. The format of the data within each attribute is determined by the selection parameter definition within Vega-Lite. |

#### Examples

The following two examples have equivalent definitions. Each one has a
point and interval selection parameter include in the chart definition.
The point selection parameter is named "point\_selection". The interval
or box selection parameter is named "interval\_selection".

**Example 1: Chart selections with ``st.altair\_chart``**

```
import altair as alt
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=["a", "b", "c"])

point_selector = alt.selection_point("point_selection")
interval_selector = alt.selection_interval("interval_selection")
chart = (
    alt.Chart(df)
    .mark_circle()
    .encode(
        x="a",
        y="b",
        size="c",
        color="c",
        tooltip=["a", "b", "c"],
        fillOpacity=alt.condition(point_selector, alt.value(1), alt.value(0.3)),
    )
    .add_params(point_selector, interval_selector)
)

event = st.altair_chart(chart, key="alt_chart", on_select="rerun")

event
```

**Example 2: Chart selections with ``st.vega\_lite\_chart``**

```
import pandas as pd
import streamlit as st
from numpy.random import default_rng as rng

df = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=["a", "b", "c"])

spec = {
    "mark": {"type": "circle", "tooltip": True},
    "params": [
        {"name": "interval_selection", "select": "interval"},
        {"name": "point_selection", "select": "point"},
    ],
    "encoding": {
        "x": {"field": "a", "type": "quantitative"},
        "y": {"field": "b", "type": "quantitative"},
        "size": {"field": "c", "type": "quantitative"},
        "color": {"field": "c", "type": "quantitative"},
        "fillOpacity": {
            "condition": {"param": "point_selection", "value": 1},
            "value": 0.3,
        },
    },
}

event = st.vega_lite_chart(df, spec, key="vega_chart", on_select="rerun")

event
```

Try selecting points in this interactive example. When you click a point,
the selection will appear under the attribute, "point\_selection", which
is the name given to the point selection parameter. Similarly, when you
make an interval selection, it will appear under the attribute
"interval\_selection". You can give your selection parameters other
names if desired.

If you hold Shift while selecting points, existing point selections
will be preserved. Interval selections are not preserved when making
additional selections.

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-chart-events-vega-lite-state.streamlit.app//?utm_medium=oembed&)

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

## Theming

Altair charts are displayed using the Streamlit theme by default. This theme is sleek, user-friendly, and incorporates Streamlit's color palette. The added benefit is that your charts better integrate with the rest of your app's design.

The Streamlit theme is available from Streamlit 1.16.0 through the `theme="streamlit"` keyword argument. To disable it, and use Altair's native theme, use `theme=None` instead.

Let's look at an example of charts with the Streamlit theme and the native Altair theme:

`import altair as alt
from vega_datasets import data
source = data.cars()
chart = alt.Chart(source).mark_circle().encode(
x='Horsepower',
y='Miles_per_Gallon',
color='Origin',
).interactive()
tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])
with tab1:
# Use the Streamlit theme.
# This is the default. So you can also omit the theme argument.
st.altair_chart(chart, theme="streamlit", use_container_width=True)
with tab2:
# Use the native Altair theme.
st.altair_chart(chart, theme=None, use_container_width=True)`

Click the tabs in the interactive app below to see the charts with the Streamlit theme enabled and disabled.

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-altair-chart.streamlit.app/?utm_medium=oembed)

If you're wondering if your own customizations will still be taken into account, don't worry! You can still make changes to your chart configurations. In other words, although we now enable the Streamlit theme by default, you can overwrite it with custom colors or fonts. For example, if you want a chart line to be green instead of the default red, you can do it!

Here's an example of an Altair chart where manual color passing is done and reflected:

See the code*expand\_more*

`import altair as alt
import streamlit as st
from vega_datasets import data
source = data.seattle_weather()
scale = alt.Scale(
domain=["sun", "fog", "drizzle", "rain", "snow"],
range=["#e7ba52", "#a7a7a7", "#aec7e8", "#1f77b4", "#9467bd"],
)
color = alt.Color("weather:N", scale=scale)
# We create two selections:
# - a brush that is active on the top panel
# - a multi-click that is active on the bottom panel
brush = alt.selection_interval(encodings=["x"])
click = alt.selection_multi(encodings=["color"])
# Top panel is scatter plot of temperature vs time
points = (
alt.Chart()
.mark_point()
.encode(
alt.X("monthdate(date):T", title="Date"),
alt.Y(
"temp_max:Q",
title="Maximum Daily Temperature (C)",
scale=alt.Scale(domain=[-5, 40]),
),
color=alt.condition(brush, color, alt.value("lightgray")),
size=alt.Size("precipitation:Q", scale=alt.Scale(range=[5, 200])),
)
.properties(width=550, height=300)
.add_selection(brush)
.transform_filter(click)
)
# Bottom panel is a bar chart of weather type
bars = (
alt.Chart()
.mark_bar()
.encode(
x="count()",
y="weather:N",
color=alt.condition(click, color, alt.value("lightgray")),
)
.transform_filter(brush)
.properties(
width=550,
)
.add_selection(click)
)
chart = alt.vconcat(points, bars, data=source, title="Seattle Weather: 2012-2015")
tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])
with tab1:
st.altair_chart(chart, theme="streamlit", use_container_width=True)
with tab2:
st.altair_chart(chart, theme=None, use_container_width=True)`

Notice how the custom colors are still reflected in the chart, even when the Streamlit theme is enabled 👇

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-altair-custom-colors.streamlit.app/?utm_medium=oembed)

For many more examples of Altair charts with and without the Streamlit theme, check out the [altair.streamlit.app](https://altair.streamlit.app).

[*arrow\_back*Previous: st.scatter\_chart](/develop/api-reference/charts/st.scatter_chart)[*arrow\_forward*Next: st.bokeh\_chart](/develop/api-reference/charts/st.bokeh_chart)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI