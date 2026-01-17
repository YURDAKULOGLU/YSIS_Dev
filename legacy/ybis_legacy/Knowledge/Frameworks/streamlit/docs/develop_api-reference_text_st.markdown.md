st.markdown - Streamlit Docs

## st.markdown

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display string formatted as Markdown.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/markdown.py#L40 "View st.markdown source code on GitHub") | |
| --- | --- |
| st.markdown(body, unsafe\_allow\_html=False, \*, help=None, width="stretch", text\_alignment="left") | |
| Parameters | |
| body (any) | The text to display as GitHub-flavored Markdown. Syntax information can be found at: <https://github.github.com/gfm>. If anything other than a string is passed, it will be converted into a string behind the scenes using str(body).  This also supports:   * Emoji shortcodes, such as :+1: and :sunglasses:.   For a list of all supported codes,   see <https://share.streamlit.io/streamlit/emoji-shortcodes>. * Streamlit logo shortcode. Use :streamlit: to add a little   Streamlit flair to your text. * A limited set of typographical symbols. "<- -> <-> -- >= <= ~="   becomes "← → ↔ — ≥ ≤ ≈" when parsed as Markdown. * Google Material Symbols (rounded style), using the syntax   :material/icon\_name:, where "icon\_name" is the name of the   icon in snake case. For a complete list of icons, see Google's   [Material Symbols](https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Rounded)   font library. * LaTeX expressions, by wrapping them in "$" or "$$" (the "$$"   must be on their own lines). Supported LaTeX functions are listed   at <https://katex.org/docs/supported.html>. * Colored text and background colors for text, using the syntax   :color[text to be colored] and :color-background[text to be colored],   respectively. color must be replaced with any of the following   supported colors: red, orange, yellow, green, blue, violet, gray/grey,   rainbow, or primary. For example, you can use   :orange[your text here] or :blue-background[your text here].   If you use "primary" for color, Streamlit will use the default   primary accent color unless you set the theme.primaryColor   configuration option. * Colored badges, using the syntax :color-badge[text in the badge].   color must be replaced with any of the following supported   colors: red, orange, yellow, green, blue, violet, gray/grey, or primary.   For example, you can use :orange-badge[your text here] or   :blue-badge[your text here]. * Small text, using the syntax :small[text to show small]. |
| unsafe\_allow\_html (bool) | Whether to render HTML within body. If this is False (default), any HTML tags found in body will be escaped and therefore treated as raw text. If this is True, any HTML expressions within body will be rendered.  Adding custom HTML to your app impacts safety, styling, and maintainability.  Note  If you only want to insert HTML or CSS without Markdown text, we recommend using st.html instead. |
| help (str or None) | A tooltip that gets displayed next to the Markdown. If this is None (default), no tooltip is displayed.  The tooltip can optionally contain GitHub-flavored Markdown, including the Markdown directives described in the body parameter of st.markdown. |
| width ("stretch", "content", or int) | The width of the Markdown element. This can be one of the following:   * "stretch" (default): The width of the element matches the   width of the parent container. * "content": The width of the element matches the width of its   content, but doesn't exceed the width of the parent container. * An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |
| text\_alignment ("left", "center", "right", or "justify") | The horizontal alignment of the text within the element. This can be one of the following:   * "left" (default): Text is aligned to the left edge. * "center": Text is centered. * "right": Text is aligned to the right edge. * "justify": Text is justified (stretched to fill the available   width with the last line left-aligned).   Note  For text alignment to have a visible effect, the element's width must be wider than its content. If you use width="content" with short text, the alignment may not be noticeable. |

#### Examples

```
import streamlit as st

st.markdown("*Streamlit* is **really** ***cool***.")
st.markdown('''
    :red[Streamlit] :orange[can] :green[write] :blue[text] :violet[in]
    :gray[pretty] :rainbow[colors] and :blue-background[highlight] text.''')
st.markdown("Here's a bouquet &mdash;\
            :tulip::cherry_blossom::rose::hibiscus::sunflower::blossom:")

multi = '''If you end a line with two spaces,
a soft return is used for the next line.

Two (or more) newline characters in a row will result in a hard return.
'''
st.markdown(multi)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-markdown.streamlit.app//?utm_medium=oembed&)

`import streamlit as st
md = st.text_area('Type in your markdown string (without outer quotes)',
"Happy Streamlit-ing! :balloon:")
st.code(f"""
import streamlit as st
st.markdown('''{md}''')
""")
st.markdown(md)`

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-markdown1.streamlit.app/?utm_medium=oembed)

[*arrow\_back*Previous: st.subheader](/develop/api-reference/text/st.subheader)[*arrow\_forward*Next: st.badge](/develop/api-reference/text/st.badge)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI