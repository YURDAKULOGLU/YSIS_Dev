st.code - Streamlit Docs

## st.code

Streamlit VersionVersion 1.52.0Version 1.51.0Version 1.50.0Version 1.49.0Version 1.48.0Version 1.47.0Version 1.46.0Version 1.45.0Version 1.44.0Version 1.43.0Version 1.42.0Version 1.41.0Version 1.40.0Version 1.39.0Version 1.38.0Version 1.37.0Version 1.36.0Version 1.35.0Version 1.34.0Version 1.33.0Version 1.32.0Version 1.31.0Version 1.30.0Version 1.29.0Version 1.28.0Version 1.27.0Version 1.26.0Version 1.25.0Version 1.24.0Version 1.23.0Version 1.22.0

Display a code block with optional syntax highlighting.

| Function signature[[source]](https://github.com/streamlit/streamlit/blob/1.52.0/lib/streamlit/elements/code.py#L36 "View st.code source code on GitHub") | |
| --- | --- |
| st.code(body, language="python", \*, line\_numbers=False, wrap\_lines=False, height="content", width="stretch") | |
| Parameters | |
| body (str) | The string to display as code or monospace text. |
| language (str or None) | The language that the code is written in, for syntax highlighting. This defaults to "python". If this is None, the code will be plain, monospace text.  For a list of available language values, see [react-syntax-highlighter](https://github.com/react-syntax-highlighter/react-syntax-highlighter/blob/master/AVAILABLE_LANGUAGES_PRISM.MD) on GitHub. |
| line\_numbers (bool) | An optional boolean indicating whether to show line numbers to the left of the code block. This defaults to False. |
| wrap\_lines (bool) | An optional boolean indicating whether to wrap lines. This defaults to False. |
| height ("content", "stretch", or int) | The height of the code block element. This can be one of the following:   * "content" (default): The height of the element matches the   height of its content. * "stretch": The height of the element matches the height of   its content or the height of the parent container, whichever is   larger. If the element is not in a parent container, the height   of the element matches the height of its content. * An integer specifying the height in pixels: The element has a   fixed height. If the content is larger than the specified   height, scrolling is enabled.   Note  Use scrolling containers sparingly. If you use scrolling containers, avoid heights that exceed 500 pixels. Otherwise, the scroll surface of the container might cover the majority of the screen on mobile devices, which makes it hard to scroll the rest of the app. |
| width ("stretch", "content", or int) | The width of the code block element. This can be one of the following:   * "stretch" (default): The width of the element matches the   width of the parent container. * "content": The width of the element matches the width of its   content, but doesn't exceed the width of the parent container. * An integer specifying the width in pixels: The element has a   fixed width. If the specified width is greater than the width of   the parent container, the width of the element matches the width   of the parent container. |

#### Examples

```
import streamlit as st

code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language="python")
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-code.streamlit.app//?utm_medium=oembed&)

```
import streamlit as st
code = '''Is it a crown or boat?
                        ii
                      iiiiii
WWw                 .iiiiiiii.                ...:
 WWWWWWw          .iiiiiiiiiiii.         ........
  WWWWWWWWWWw    iiiiiiiiiiiiiiii    ...........
   WWWWWWWWWWWWWWwiiiiiiiiiiiiiiiii............
    WWWWWWWWWWWWWWWWWWwiiiiiiiiiiiiii.........
     WWWWWWWWWWWWWWWWWWWWWWwiiiiiiiiii.......
      WWWWWWWWWWWWWWWWWWWWWWWWWWwiiiiiii....
       WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWwiiii.
          -MMMWWWWWWWWWWWWWWWWWWWWWWMMM-
'''
st.code(code, language=None)
```

[Built with Streamlit 🎈](https://streamlit.io)

[Fullscreen *open\_in\_new*](https://doc-code-ascii.streamlit.app//?utm_medium=oembed&)

[*arrow\_back*Previous: st.caption](/develop/api-reference/text/st.caption)[*arrow\_forward*Next: st.divider](/develop/api-reference/text/st.divider)

*forum*

### Still have questions?

Our [forums](https://discuss.streamlit.io) are full of helpful information and Streamlit experts.

*forum* Ask AI