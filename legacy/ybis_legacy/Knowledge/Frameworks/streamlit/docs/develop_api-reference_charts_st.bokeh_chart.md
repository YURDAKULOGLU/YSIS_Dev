st.bokeh\_chart - Streamlit Docs

## st.bokeh\_chart

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

*delete*

#### Deprecation notice

`st.bokeh_chart` was deprecated in version 1.49.0 and removed in version 1.52.0. Use the [`streamlit-bokeh`](https://github.com/streamlit/streamlit-bokeh) custom component instead.

Display an interactive Bokeh chart.

Bokeh is a charting library for Python. You can find
more about Bokeh at <https://bokeh.pydata.org>.

Important

This command has been deprecated and removed. Please use our custom
component, [streamlit-bokeh](https://github.com/streamlit/streamlit-bokeh), instead. Calling st.bokeh\_chart will
do nothing.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/bokeh_chart.py#L31 "View st.bokeh_chart source code on GitHub") | |
| --- | --- |
| st.bokeh\_chart(figure, use\_container\_width=True) | |
| Parameters | |
| figure (bokeh.plotting.figure.Figure) | A Bokeh figure to plot. |
| use\_container\_width (bool) | Whether to override the figure's native width with the width of the parent container. If use\_container\_width is True (default), Streamlit sets the width of the figure to match the width of the parent container. If use\_container\_width is False, Streamlit sets the width of the chart to fit its contents according to the plotting library, up to the width of the parent container. |

[*arrow\_back*Previous: st.altair\_chart](/develop/api-reference/charts/st.altair_chart)[*arrow\_forward*Next: st.graphviz\_chart](/develop/api-reference/charts/st.graphviz_chart)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI