st.container - Streamlit Docs

## st.container

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Insert a multi-element container.

Inserts an invisible container into your app that can be used to hold
multiple elements. This allows you to, for example, insert multiple
elements into your app out of order.

To add elements to the returned container, you can use the with
notation (preferred) or just call commands directly on the returned
object. See examples below.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/layouts.py#L59 "View st.container source code on GitHub") | |
| --- | --- |
| st.container(\*, border=None, key=None, width="stretch", height="content", horizontal=False, horizontal\_alignment="left", vertical\_alignment="top", gap="small") | |
| Parameters | |
| border (bool or None) | Whether to show a border around the container. If None (default), a border is shown if the container is set to a fixed height and not shown otherwise. |
| key (str or None) | An optional string to give this container a stable identity.  Additionally, if key is provided, it will be used as CSS class name prefixed with st-key-. |
| width ("stretch", "content", or int) | The width of the container. This can be one of the following:   * "stretch" (default): The width of the container matches the   width of the parent container. * "content": The width of the container matches the width of   its content. * An integer specifying the width in pixels: The container has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the container matches the width   of the parent container. |
| height ("content", "stretch", or int) | The height of the container. This can be one of the following:   * "content" (default): The height of the container matches the   height of its content. * "stretch": The height of the container matches the height of   its content or the height of the parent container, whichever is   larger. If the container is not in a parent container, the height   of the container matches the height of its content. * An integer specifying the height in pixels: The container has a   fixed height. If the content is larger than the specified   height, scrolling is enabled.   Note  Use scrolling containers sparingly. If you use scrolling containers, avoid heights that exceed 500 pixels. Otherwise, the scroll surface of the container might cover the majority of the screen on mobile devices, which makes it hard to scroll the rest of the app. |
| horizontal (bool) | Whether to use horizontal flexbox layout. If this is False (default), the container's elements are laid out vertically. If this is True, the container's elements are laid out horizontally and will overflow to the next line if they don't fit within the container's width. |
| horizontal\_alignment ("left", "center", "right", or "distribute") | The horizontal alignment of the elements inside the container. This can be one of the following:   * "left" (default): Elements are aligned to the left side of   the container. * "center": Elements are horizontally centered inside the   container. * "right": Elements are aligned to the right side of the   container. * "distribute": Elements are distributed evenly in the   container. This increases the horizontal gap between elements to   fill the width of the container. A standalone element is aligned   to the left.  When horizontal is False, "distribute" aligns the   elements the same as "left". |
| vertical\_alignment ("top", "center", "bottom", or "distribute") | The vertical alignment of the elements inside the container. This can be one of the following:   * "top" (default): Elements are aligned to the top of the   container. * "center": Elements are vertically centered inside the   container. * "bottom": Elements are aligned to the bottom of the   container. * "distribute": Elements are distributed evenly in the   container. This increases the vertical gap between elements to   fill the height of the container. A standalone element is aligned   to the top.  When horizontal is True, "distribute" aligns the   elements the same as "top". |
| gap ("small", "medium", "large", or None) | The minimum gap size between the elements inside the container. This can be one of the following:   * "small" (default): 1rem gap between the elements. * "medium": 2rem gap between the elements. * "large": 4rem gap between the elements. * None: No gap between the elements.   The rem unit is relative to the theme.baseFontSize configuration option.  The minimum gap applies to both the vertical and horizontal gaps between the elements. Elements may have larger gaps in one direction if you use a distributed horizontal alignment or fixed height. |

#### Examples

**Example 1: Inserting elements using ``with`` notation**

You can use the with statement to insert any element into a
container.

```
import streamlit as st

with st.container():
    st.write("This is inside the container")

    # You can call any Streamlit command, including custom components:
    st.bar_chart(np.random.randn(50, 3))

st.write("This is outside the container")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-container1.streamlit.app//?utm_medium=oembed&)

**Example 2: Inserting elements out of order**

When you create a container, its position in the app remains fixed and
you can add elements to it at any time. This allows you to insert
elements out of order in your app. You can also write to the container
by calling commands directly on the container object.

```
import streamlit as st

container = st.container(border=True)
container.write("This is inside the container")
st.write("This is outside the container")

container.write("This is inside too")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-container2.streamlit.app//?utm_medium=oembed&)

**Example 3: Grid layout with columns and containers**

You can create a grid with a fixed number of elements per row by using
columns and containers.

```
import streamlit as st

row1 = st.columns(3)
row2 = st.columns(3)

for col in row1 + row2:
    tile = col.container(height=120)
    tile.title(":balloon:")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-container3.streamlit.app//?utm_medium=oembed&)

**Example 4: Vertically scrolling container**

You can create a vertically scrolling container by setting a fixed
height.

```
import streamlit as st

long_text = "Lorem ipsum. " * 1000

with st.container(height=300):
    st.markdown(long_text)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-container4.streamlit.app//?utm_medium=oembed&)

**Example 5: Horizontal container**

You can create a row of widgets using a horizontal container. Use
horizontal\_alignment to specify the alignment of the elements.

```
import streamlit as st

flex = st.container(horizontal=True, horizontal_alignment="right")

for card in range(3):
    flex.button(f"Button {card + 1}")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-container5.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.columns](/develop/api-reference/layout/st.columns)[*arrow\_forward*Next: st.dialog](https://docs.streamlit.io/develop/api-reference/execution-flow/st.dialog)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI