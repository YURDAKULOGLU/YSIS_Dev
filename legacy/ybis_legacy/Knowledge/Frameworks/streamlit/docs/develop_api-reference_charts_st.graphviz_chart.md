st.graphviz\_chart - Streamlit Docs

## st.graphviz\_chart

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a graph using the dagre-d3 library.

Important

You must install graphviz>=0.19.0 to use this command. You can
install all charting dependencies (except Bokeh) as an extra with
Streamlit:

```
pip install streamlit[charts]
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/graphviz_chart.py#L49 "View st.graphviz_chart source code on GitHub") | |
| --- | --- |
| st.graphviz\_chart(figure\_or\_dot, use\_container\_width=None, \*, width="content", height="content") | |
| Parameters | |
| figure\_or\_dot (graphviz.dot.Graph, graphviz.dot.Digraph, graphviz.sources.Source, str) | The Graphlib graph object or dot string to display |
| use\_container\_width (bool) | *delete* use\_container\_width is deprecated and will be removed in a future release. For use\_container\_width=True, use width="stretch". For use\_container\_width=False, use width="content".  Whether to override the figure's native width with the width of the parent container. If use\_container\_width is False (default), Streamlit sets the width of the chart to fit its contents according to the plotting library, up to the width of the parent container. If use\_container\_width is True, Streamlit sets the width of the figure to match the width of the parent container. |
| width ("content", "stretch", or int) | The width of the chart element. This can be one of the following:   * "content" (default): The width of the element matches the   width of its content, but doesn't exceed the width of the parent   container. * "stretch": The width of the element matches the width of the   parent container. * An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |
| height ("content", "stretch", or int) | The height of the chart element. This can be one of the following:   * "content" (default): The height of the element matches the   height of its content. * "stretch": The height of the element matches the height of   its content or the height of the parent container, whichever is   larger. If the element is not in a parent container, the height   of the element matches the height of its content. * An integer specifying the height in pixels: The element has a   fixed height. If the content is larger than the specified   height, scrolling is enabled. |

#### Example

```
import streamlit as st
import graphviz

# Create a graphlib graph object
graph = graphviz.Digraph()
graph.edge("run", "intr")
graph.edge("intr", "runbl")
graph.edge("runbl", "run")
graph.edge("run", "kernel")
graph.edge("kernel", "zombie")
graph.edge("kernel", "sleep")
graph.edge("kernel", "runmem")
graph.edge("sleep", "swap")
graph.edge("swap", "runswap")
graph.edge("runswap", "new")
graph.edge("runswap", "runmem")
graph.edge("new", "runmem")
graph.edge("sleep", "runmem")

st.graphviz_chart(graph)
```

Or you can render the chart from the graph using GraphViz's Dot
language:

```
st.graphviz_chart('''
    digraph {
        run -> intr
        intr -> runbl
        runbl -> run
        run -> kernel
        kernel -> zombie
        kernel -> sleep
        kernel -> runmem
        sleep -> swap
        swap -> runswap
        runswap -> new
        runswap -> runmem
        new -> runmem
        sleep -> runmem
    }
''')
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-graphviz-chart.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.bokeh\_chart](/develop/api-reference/charts/st.bokeh_chart)[*arrow\_forward*Next: st.plotly\_chart](/develop/api-reference/charts/st.plotly_chart)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI