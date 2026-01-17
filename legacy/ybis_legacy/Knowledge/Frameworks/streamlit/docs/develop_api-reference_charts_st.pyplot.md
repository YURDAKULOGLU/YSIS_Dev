st.pyplot - Streamlit Docs

## st.pyplot

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a matplotlib.pyplot figure.

Important

You must install matplotlib>=3.0.0 to use this command. You can
install all charting dependencies (except Bokeh) as an extra with
Streamlit:

```
pip install streamlit[charts]
```

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/pyplot.py#L38 "View st.pyplot source code on GitHub") | |
| --- | --- |
| st.pyplot(fig=None, clear\_figure=None, \*, width="stretch", use\_container\_width=None, \*\*kwargs) | |
| Parameters | |
| fig (Matplotlib Figure) | The Matplotlib Figure object to render. See <https://matplotlib.org/stable/gallery/index.html> for examples.  Note  When this argument isn't specified, this function will render the global Matplotlib figure object. However, this feature is deprecated and will be removed in a later version. |
| clear\_figure (bool) | If True, the figure will be cleared after being rendered. If False, the figure will not be cleared after being rendered. If left unspecified, we pick a default based on the value of fig.   * If fig is set, defaults to False. * If fig is not set, defaults to True. This simulates Jupyter's   approach to matplotlib rendering. |
| width ("stretch", "content", or int) | The width of the chart element. This can be one of the following:   * "stretch" (default): The width of the element matches the   width of the parent container. * "content": The width of the element matches the   width of its content, but doesn't exceed the width of the parent   container. * An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |
| use\_container\_width (bool) | *delete* use\_container\_width is deprecated and will be removed in a future release. For use\_container\_width=True, use width="stretch". For use\_container\_width=False, use width="content".  Whether to override the figure's native width with the width of the parent container. If use\_container\_width is True (default), Streamlit sets the width of the figure to match the width of the parent container. If use\_container\_width is False, Streamlit sets the width of the chart to fit its contents according to the plotting library, up to the width of the parent container. |
| \*\*kwargs (any) | Arguments to pass to Matplotlib's savefig function. |

#### Example

```
import matplotlib.pyplot as plt
import streamlit as st
from numpy.random import default_rng as rng

arr = rng(0).normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.pyplot(fig)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-pyplot.streamlit.app//?utm_medium=oembed&)

Matplotlib supports several types of "backends". If you're getting an
error using Matplotlib with Streamlit, try setting your backend to "TkAgg":

```
echo "backend: TkAgg" >> ~/.matplotlib/matplotlibrc
```

For more information, see <https://matplotlib.org/faq/usage_faq.html>.

*priority\_high*

#### Warning

Matplotlib [doesn't work well with threads](https://matplotlib.org/3.3.2/faq/howto_faq.html#working-with-threads). So if you're using Matplotlib you should wrap your code with locks. This Matplotlib bug is more prominent when you deploy and share your apps because you're more likely to get concurrent users then. The following example uses [`Rlock`](https://docs.python.org/3/library/threading.html#rlock-objects) from the `threading` module.

`import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from threading import RLock
_lock = RLock()
x = np.random.normal(1, 1, 100)
y = np.random.normal(1, 1, 100)
with _lock:
fig, ax = plt.subplots()
ax.scatter(x, y)
st.pyplot(fig)`

[*arrow\_back*Previous: st.pydeck\_chart](/develop/api-reference/charts/st.pydeck_chart)[*arrow\_forward*Next: st.vega\_lite\_chart](/develop/api-reference/charts/st.vega_lite_chart)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI